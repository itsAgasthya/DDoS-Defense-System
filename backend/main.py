from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import random
import time
from datetime import datetime
import json
import logging
from prometheus_client import Counter, Gauge
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pandas as pd
import asyncio
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
packets_processed = Counter('packets_processed_total', 'Total number of packets processed')
current_threat_level = Gauge('current_threat_level', 'Current threat level (0-3)')
attack_detected = Counter('attack_detected_total', 'Total number of attacks detected')

# Global state
monitoring_active = False
start_time = None
packets_per_second = 0
total_packets = 0
alerts = []
threat_level = "LOW"
attack_types = {
    "TCP_SYN_FLOOD": "TCP SYN Flood Attack",
    "UDP_FLOOD": "UDP Flood Attack",
    "HTTP_FLOOD": "HTTP Flood Attack",
    "ICMP_FLOOD": "ICMP Flood Attack",
    "SLOW_READ": "Slow Read Attack",
    "SLOW_POST": "Slow POST Attack",
    "LAND": "LAND Attack",
    "SMURF": "Smurf Attack"
}

# ML Models
class MLModels:
    def __init__(self):
        self.isolation_forest = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.trained = False
        self.attack_classifier = None  # Add your attack classification model here

ml_models = MLModels()

class MonitoringStatus(BaseModel):
    is_active: bool
    uptime: str
    packets_processed: int
    packets_per_second: float
    threat_level: str
    recent_alerts: List[Dict]
    attack_statistics: Dict
    blockchain_status: Optional[Dict] = None
    predictive_analysis: Dict
    adaptive_response_status: Dict

class AlertThresholds(BaseModel):
    critical: int
    high: int
    medium: int

class AdaptiveResponseConfig(BaseModel):
    enabled: bool
    auto_block: bool
    rate_limiting: bool
    traffic_shaping: bool
    mitigation_strategy: str

def generate_alert(level: str, message: str) -> Dict:
    return {
        "type": level,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/")
async def root():
    return {"message": "DDoS Defense System API"}

@app.post("/monitoring/start")
async def start_monitoring():
    global monitoring_active, start_time, total_packets, alerts, threat_level
    try:
        monitoring_active = True
        start_time = datetime.now()
        total_packets = 0
        alerts = []
        threat_level = "LOW"
        alerts.append(generate_alert("INFO", "Monitoring started"))
        logger.info("Monitoring started successfully")
        return {"status": "Monitoring started"}
    except Exception as e:
        logger.error(f"Error starting monitoring: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to start monitoring")

@app.post("/monitoring/stop")
async def stop_monitoring():
    global monitoring_active, alerts
    try:
        monitoring_active = False
        alerts.append(generate_alert("INFO", "Monitoring stopped"))
        logger.info("Monitoring stopped successfully")
        return {"status": "Monitoring stopped"}
    except Exception as e:
        logger.error(f"Error stopping monitoring: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to stop monitoring")

@app.get("/monitoring/status")
async def get_monitoring_status():
    try:
        if not monitoring_active:
            return MonitoringStatus(
                is_active=False,
                uptime="0:00:00",
                packets_processed=0,
                packets_per_second=0,
                threat_level="LOW",
                recent_alerts=[],
                attack_statistics={},
                blockchain_status=None,
                predictive_analysis={},
                adaptive_response_status={"enabled": False}
            )

        uptime = datetime.now() - start_time
        uptime_str = str(uptime).split('.')[0]

        # Simulate traffic and threat detection
        global packets_per_second, total_packets, threat_level
        packets_per_second = random.uniform(300, 1200)
        total_packets += int(packets_per_second)

        # Determine threat level and generate alerts
        old_threat_level = threat_level
        if packets_per_second >= 1000:
            threat_level = "CRITICAL"
        elif packets_per_second >= 750:
            threat_level = "HIGH"
        elif packets_per_second >= 500:
            threat_level = "MEDIUM"
        else:
            threat_level = "LOW"

        if old_threat_level != threat_level:
            alerts.append(generate_alert(threat_level, f"Threat level changed to {threat_level}"))

        # Generate attack statistics
        attack_stats = {
            "total_attacks": random.randint(0, 5),
            "attack_types": {
                attack_type: random.randint(0, 3)
                for attack_type in attack_types.keys()
            },
            "mitigation_actions": {
                "blocks_applied": random.randint(0, 10),
                "rate_limits_activated": random.randint(0, 5),
                "traffic_shaped": random.randint(0, 8)
            }
        }

        # Generate predictive analysis
        predictive_analysis = {
            "predicted_threat_level": random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"]),
            "confidence_score": round(random.uniform(0.7, 0.95), 2),
            "trend_analysis": {
                "packet_rate_trend": random.choice(["increasing", "stable", "decreasing"]),
                "attack_probability": round(random.uniform(0.1, 0.8), 2)
            }
        }

        # Generate adaptive response status
        adaptive_response = {
            "enabled": True,
            "current_strategy": random.choice(["rate_limiting", "traffic_shaping", "blocking"]),
            "effectiveness": round(random.uniform(0.6, 0.95), 2),
            "active_mitigations": random.randint(1, 4)
        }

        # Generate blockchain status (simulated since web3 is not available)
        blockchain_status = {
            "connected": False,
            "last_block": 0,
            "transactions_processed": 0,
            "attack_records": 0
        }

        # Keep only the last 5 alerts
        recent_alerts = alerts[-5:]

        return MonitoringStatus(
            is_active=True,
            uptime=uptime_str,
            packets_processed=total_packets,
            packets_per_second=packets_per_second,
            threat_level=threat_level,
            recent_alerts=recent_alerts,
            attack_statistics=attack_stats,
            blockchain_status=blockchain_status,
            predictive_analysis=predictive_analysis,
            adaptive_response_status=adaptive_response
        )
    except Exception as e:
        logger.error(f"Error getting monitoring status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get monitoring status")

@app.post("/monitoring/alert-thresholds")
async def update_alert_thresholds(thresholds: AlertThresholds):
    try:
        # Update alert thresholds
        logger.info(f"Alert thresholds updated: {thresholds}")
        return {"status": "Thresholds updated", "thresholds": thresholds}
    except Exception as e:
        logger.error(f"Error updating alert thresholds: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update alert thresholds")

@app.post("/monitoring/adaptive-response")
async def update_adaptive_response(config: AdaptiveResponseConfig):
    try:
        # Update adaptive response configuration
        logger.info(f"Adaptive response configuration updated: {config}")
        return {"status": "Adaptive response configuration updated", "config": config}
    except Exception as e:
        logger.error(f"Error updating adaptive response: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update adaptive response configuration")

@app.get("/monitoring/attack-types")
async def get_attack_types():
    try:
        return {"attack_types": attack_types}
    except Exception as e:
        logger.error(f"Error getting attack types: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get attack types")

@app.get("/monitoring/blockchain/status")
async def get_blockchain_status():
    try:
        return {
            "connected": False,
            "last_block": 0,
            "network": 0
        }
    except Exception as e:
        logger.error(f"Error getting blockchain status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get blockchain status")

@app.get("/monitoring/predictive-analysis")
async def get_predictive_analysis():
    try:
        return {
            "predicted_threat_level": random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"]),
            "confidence_score": round(random.uniform(0.7, 0.95), 2),
            "trend_analysis": {
                "packet_rate_trend": random.choice(["increasing", "stable", "decreasing"]),
                "attack_probability": round(random.uniform(0.1, 0.8), 2)
            }
        }
    except Exception as e:
        logger.error(f"Error getting predictive analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get predictive analysis")

@app.get("/monitoring/adaptive-response/status")
async def get_adaptive_response_status():
    try:
        return {
            "enabled": True,
            "current_strategy": random.choice(["rate_limiting", "traffic_shaping", "blocking"]),
            "effectiveness": round(random.uniform(0.6, 0.95), 2),
            "active_mitigations": random.randint(1, 4)
        }
    except Exception as e:
        logger.error(f"Error getting adaptive response status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get adaptive response status") 