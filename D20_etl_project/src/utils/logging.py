import logging
from pythonjsonlogger import jsonlogger

def setup_logger(log_level="INFO"):
    logger = logging.getLogger("etl_logger")

    if not logger.handlers:  # Prevent duplicate handlers
        handler = logging.StreamHandler()
        formatter = jsonlogger.JsonFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(log_level)
        logger.propagate = False  # Disable propagation to root to avoid duplicate logs

    return logger

# Expose the configured logger for use in other modules
etl_logger = setup_logger()