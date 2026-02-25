import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logger(name, log_file, level=logging.INFO):
    """Setup logger with file and console handlers"""
    
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if logger.handlers:
        return logger
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=10485760,
        backupCount=5
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

app_logger = setup_logger('app', 'logs/app.log', logging.INFO)
api_logger = setup_logger('api', 'logs/api.log', logging.INFO)