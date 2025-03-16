from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import time
import random

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulated monitoring state
monitoring_active = False
start_time = None
packet_count = 0
current_pps = 0

class ThresholdConfig(BaseModel):
    critical: int
    high: int
    medium: int

# Simulated thresholds
thresholds = ThresholdConfig(
    critical=1000,
    high=750,
    medium=500
)

def get_threat_level(pps: float) -> str:
    if pps >= thresholds.critical:
        return "CRITICAL"
    elif pps >= thresholds.high:
        return "HIGH"
    elif pps >= thresholds.medium:
        return "MEDIUM"
    return "LOW"

@app.get("/monitoring/status")
async def get_status():
    global packet_count, current_pps
    
    if not monitoring_active:
        return {
            "status": "inactive",
            "stats": None
        }

    # Simulate some traffic data
    current_pps = random.uniform(300, 1200)
    packet_count += int(current_pps)
    
    return {
        "status": "active",
        "stats": {
            "packets_processed": packet_count,
            "packets_per_second": current_pps,
            "alerts_triggered": int(current_pps > thresholds.medium),
            "uptime": int(time.time() - start_time) if start_time else 0,
            "current_threat_level": get_threat_level(current_pps),
            "last_alert_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) if current_pps > thresholds.medium else None
        }
    }

@app.post("/monitoring/start")
async def start_monitoring():
    global monitoring_active, start_time, packet_count
    if monitoring_active:
        raise HTTPException(status_code=400, detail="Monitoring is already active")
    
    monitoring_active = True
    start_time = time.time()
    packet_count = 0
    return {"status": "Monitoring started"}

@app.post("/monitoring/stop")
async def stop_monitoring():
    global monitoring_active, start_time
    if not monitoring_active:
        raise HTTPException(status_code=400, detail="Monitoring is not active")
    
    monitoring_active = False
    start_time = None
    return {"status": "Monitoring stopped"}

@app.put("/monitoring/thresholds")
async def update_thresholds(new_thresholds: Dict[str, int]):
    global thresholds
    thresholds = ThresholdConfig(**new_thresholds)
    return {"status": "Thresholds updated", "new_thresholds": new_thresholds} 