"""
Logging configuration for Voice-to-CAD application
"""
import logging
import logging.handlers
import os
from datetime import datetime

class LogManager:
    """Centralized logging management"""
    
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        self.ensure_log_directory()
        self.setup_loggers()
    
    def ensure_log_directory(self):
        """Create logs directory if it doesn't exist"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def setup_loggers(self):
        """Setup different loggers for different components"""
        
        # Main application logger
        self.app_logger = self.create_logger(
            name="voice_to_cad_app",
            log_file="app.log",
            level=logging.INFO
        )
        
        # AI/API logger
        self.ai_logger = self.create_logger(
            name="ai_generation",
            log_file="ai_generation.log",
            level=logging.DEBUG
        )
        
        # Error logger
        self.error_logger = self.create_logger(
            name="error_logger",
            log_file="errors.log",
            level=logging.ERROR
        )
        
        # Test logger
        self.test_logger = self.create_logger(
            name="test_logger",
            log_file="tests.log",
            level=logging.DEBUG
        )
    
    def create_logger(self, name, log_file, level=logging.INFO):
        """Create a configured logger"""
        
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Remove existing handlers to avoid duplicates
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            os.path.join(self.log_dir, log_file),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def get_logger(self, logger_type="app"):
        """Get a specific logger"""
        loggers = {
            "app": self.app_logger,
            "ai": self.ai_logger,
            "error": self.error_logger,
            "test": self.test_logger
        }
        return loggers.get(logger_type, self.app_logger)

# Global logger instance
log_manager = LogManager()

def get_logger(logger_type="app"):
    """Get logger instance"""
    return log_manager.get_logger(logger_type)