import os
from pathlib import Path
from typing import Dict, Any

import yaml

def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dict containing configuration settings
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid
    """
    config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            
        # Validate required sections
        required_sections = [
            "system",
            "network",
            "anomaly_detection",
            "adaptive_response",
            "ml",
            "blockchain",
            "database",
            "api",
            "monitoring",
            "alerts",
            "security",
        ]
        
        missing_sections = [
            section for section in required_sections if section not in config
        ]
        
        if missing_sections:
            raise ValueError(
                f"Missing required configuration sections: {', '.join(missing_sections)}"
            )
            
        return config
        
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Failed to parse configuration file: {str(e)}")
    except Exception as e:
        raise Exception(f"Error loading configuration: {str(e)}")

def get_config_path() -> Path:
    """Get the path to the configuration file."""
    return Path(os.getenv("CONFIG_PATH", "config/config.yaml")) 