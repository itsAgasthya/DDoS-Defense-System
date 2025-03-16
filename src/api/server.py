from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.utils.config import load_config
from src.utils.logger import get_logger
from src.anomaly_detection.detector import AnomalyDetector
from src.monitoring.traffic_monitor import TrafficMonitor

logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="DDoS Defense System API",
    description="API for real-time DDoS attack detection and monitoring",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
monitor: Optional[TrafficMonitor] = None
detector: Optional[AnomalyDetector] = None

class MonitoringConfig(BaseModel):
    """Configuration for traffic monitoring."""
    interface: str
    window_size: int = 10
    model_path: str = "models/anomaly_detection"

class AlertConfig(BaseModel):
    """Configuration for alert thresholds."""
    critical_threshold: float = 0.8
    high_threshold: float = 0.5
    medium_threshold: float = 0.2

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup."""
    try:
        # Load configuration
        config = load_config("config/config.yaml")
        
        # Initialize detector
        global detector
        detector = AnomalyDetector(config["anomaly_detection"])
        
        # Load trained models
        model_dir = Path("models/anomaly_detection")
        if model_dir.exists():
            detector.load_models(model_dir)
            logger.info("Loaded trained models successfully")
        else:
            logger.warning("No trained models found. Please train the models first.")
        
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "DDoS Defense System API",
        "status": "running",
        "monitoring_active": monitor is not None and monitor.is_running
    }

@app.post("/monitor/start")
async def start_monitoring(config: MonitoringConfig):
    """Start traffic monitoring."""
    global monitor
    
    if monitor and monitor.is_running:
        raise HTTPException(
            status_code=400,
            detail="Monitoring is already active"
        )
    
    try:
        # Initialize monitor
        monitor = TrafficMonitor(
            detector=detector,
            interface=config.interface,
            window_size=config.window_size
        )
        
        # Start monitoring
        monitor.start()
        
        return {
            "status": "success",
            "message": f"Started monitoring on interface {config.interface}"
        }
        
    except Exception as e:
        logger.error(f"Error starting monitoring: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.post("/monitor/stop")
async def stop_monitoring():
    """Stop traffic monitoring."""
    global monitor
    
    if not monitor or not monitor.is_running:
        raise HTTPException(
            status_code=400,
            detail="Monitoring is not active"
        )
    
    try:
        monitor.stop()
        return {
            "status": "success",
            "message": "Stopped monitoring"
        }
        
    except Exception as e:
        logger.error(f"Error stopping monitoring: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/monitor/status")
async def get_monitoring_status():
    """Get current monitoring status and statistics."""
    if not monitor:
        return {
            "status": "inactive",
            "stats": None
        }
    
    return {
        "status": "active" if monitor.is_running else "stopped",
        "stats": monitor.get_stats()
    }

@app.post("/alerts/config")
async def update_alert_config(config: AlertConfig):
    """Update alert thresholds."""
    if not monitor:
        raise HTTPException(
            status_code=400,
            detail="Monitoring is not initialized"
        )
    
    try:
        # Update thresholds
        monitor.critical_threshold = config.critical_threshold
        monitor.high_threshold = config.high_threshold
        monitor.medium_threshold = config.medium_threshold
        
        return {
            "status": "success",
            "message": "Alert thresholds updated"
        }
        
    except Exception as e:
        logger.error(f"Error updating alert config: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/models/status")
async def get_model_status():
    """Get status of loaded models."""
    if not detector:
        raise HTTPException(
            status_code=500,
            detail="Detector not initialized"
        )
    
    return {
        "loaded_algorithms": list(detector.algorithms.keys()),
        "thresholds": detector.thresholds
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 