import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger():
    """
    Configures logging to write out to trading_bot.log.
    We separate logs into a file to keep the CLI output clean and readable.
    """
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.INFO)

    # Don't add multiple handlers if already set up
    if logger.handlers:
        return logger

    # Log file format and setup
    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Make sure we don't have unbound logs, rotate after 5MB
    file_handler = RotatingFileHandler(
        "trading_bot.log", maxBytes=5 * 1024 * 1024, backupCount=2
    )
    file_handler.setFormatter(log_format)
    file_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    
    return logger

# Initialize globally accessible logger for the bot package
logger = setup_logger()
