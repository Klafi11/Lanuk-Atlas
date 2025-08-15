import logging 
from logging.handlers import RotatingFileHandler

LOG_FILE = "weather.log"


# Create a single logger instance
logger = logging.getLogger("WeatherApp")
logger.setLevel(logging.INFO)

# Prevent duplicate handlers
if not logger.handlers:
    # File Handler (Log Rotation: 5MB max, keep 3 old logs)
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    # Console Handler (Optional)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)