#!/usr/bin/env python3

import argparse
import logging
import os
import sys
from pathlib import Path

import yaml
from fastapi import FastAPI
from prometheus_client import start_http_server

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.logger import setup_logging
from src.utils.config import load_config
from src.anomaly_detection.detector import AnomalyDetector
from src.adaptive_response.responder import AdaptiveResponder
from src.learning.learner import DefenseLearner
from src.predictive.predictor import ThreatPredictor
from src.blockchain.manager import BlockchainManager

app = FastAPI(title="DDoS Defense System", version="0.1.0")

def parse_arguments():
    parser = argparse.ArgumentParser(description="DDoS Defense System")
    parser.add_argument(
        "-c",
        "--config",
        default="config/config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    return parser.parse_args()

def initialize_components(config):
    """Initialize all system components."""
    components = {
        "anomaly_detector": AnomalyDetector(config["anomaly_detection"]),
        "adaptive_responder": AdaptiveResponder(config["adaptive_response"]),
        "defense_learner": DefenseLearner(config["ml"]),
        "threat_predictor": ThreatPredictor(config["ml"]),
        "blockchain_manager": BlockchainManager(config["blockchain"]),
    }
    return components

def setup_monitoring(config):
    """Setup monitoring and metrics collection."""
    if config["monitoring"]["prometheus"]["enabled"]:
        start_http_server(config["monitoring"]["prometheus"]["port"])

def main():
    """Main entry point for the DDoS Defense System."""
    args = parse_arguments()
    
    # Load configuration
    config = load_config(args.config)
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(log_level)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting DDoS Defense System...")
    
    try:
        # Initialize components
        components = initialize_components(config)
        
        # Setup monitoring
        setup_monitoring(config)
        
        # Start the system
        logger.info("System initialized successfully")
        
        # Start the API server
        import uvicorn
        uvicorn.run(
            app,
            host=config["api"]["host"],
            port=config["api"]["port"],
            workers=config["api"]["workers"],
        )
        
    except Exception as e:
        logger.error(f"Failed to start the system: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 