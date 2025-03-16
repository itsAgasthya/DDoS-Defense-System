import logging
import sys
from pathlib import Path
from typing import Optional, Union

from pythonjsonlogger import jsonlogger

def setup_logging(
    level: Union[int, str] = logging.INFO,
    log_file: Optional[Union[str, Path]] = None,
    use_json: bool = False
) -> None:
    """
    Set up logging configuration for the application.
    
    Args:
        level: Logging level (default: INFO)
        log_file: Optional path to log file
        use_json: Whether to use JSON formatting for logs
    """
    # Convert string level to numeric if needed
    if isinstance(level, str):
        level = getattr(logging, level.upper())
    
    # Create formatter
    if use_json:
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s'
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Add file handler if specified
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Name for the logger
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)

# Example usage
if __name__ == "__main__":
    # Setup basic logging
    setup_logging(level=logging.DEBUG)
    logger = get_logger(__name__)
    
    # Test different log levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    # Test JSON logging
    setup_logging(level=logging.INFO, use_json=True)
    logger.info("This is a JSON formatted log message", extra={
        "custom_field": "custom_value",
        "number": 42
    }) 