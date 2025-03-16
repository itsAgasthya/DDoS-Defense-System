#!/usr/bin/env python3

import argparse
import logging
import signal
import sys
from pathlib import Path

import uvicorn
from src.utils.logger import setup_logging
from src.utils.config import load_config
from src.api.server import app

def parse_args():
    parser = argparse.ArgumentParser(description="Run DDoS Defense monitoring service")
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind the API server"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind the API server"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Setup logging
    setup_logging(
        level=args.log_level,
        log_file="logs/monitor.log"
    )
    logger = logging.getLogger(__name__)
    
    try:
        # Create logs directory
        Path("logs").mkdir(exist_ok=True)
        
        # Start the API server
        logger.info(f"Starting DDoS Defense monitoring service on {args.host}:{args.port}")
        uvicorn.run(
            app,
            host=args.host,
            port=args.port,
            log_level=args.log_level.lower()
        )
        
    except Exception as e:
        logger.error(f"Error starting monitoring service: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 