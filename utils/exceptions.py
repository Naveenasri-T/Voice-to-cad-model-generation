"""
Exception handling utilities for Voice-to-CAD application
"""
import traceback
import sys
from functools import wraps
from utils.logging_config import get_logger

class VoiceToCADError(Exception):
    """Base exception for Voice-to-CAD application"""
    pass

class AIGenerationError(VoiceToCADError):
    """Error during AI code generation"""
    pass

class FreeCADLaunchError(VoiceToCADError):
    """Error launching FreeCAD"""
    pass

class AudioProcessingError(VoiceToCADError):
    """Error processing audio input"""
    pass

class CodeCleaningError(VoiceToCADError):
    """Error cleaning AI generated code"""
    pass

def exception_handler(logger_type="error", reraise=False):
    """Decorator for handling exceptions with logging"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger(logger_type)
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_msg = f"Error in {func.__name__}: {str(e)}"
                logger.error(error_msg)
                logger.error(f"Traceback: {traceback.format_exc()}")
                
                if reraise:
                    raise
                return None
        return wrapper
    return decorator

def log_function_call(logger_type="app"):
    """Decorator to log function calls"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger(logger_type)
            logger.info(f"Calling {func.__name__}")
            try:
                result = func(*args, **kwargs)
                logger.info(f"Successfully completed {func.__name__}")
                return result
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}")
                raise
        return wrapper
    return decorator

class ExceptionContext:
    """Context manager for exception handling"""
    
    def __init__(self, operation_name, logger_type="error", reraise=True):
        self.operation_name = operation_name
        self.logger = get_logger(logger_type)
        self.reraise = reraise
    
    def __enter__(self):
        self.logger.info(f"Starting operation: {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            error_msg = f"Error in {self.operation_name}: {exc_val}"
            self.logger.error(error_msg)
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            
            if not self.reraise:
                return True  # Suppress exception
        else:
            self.logger.info(f"Successfully completed: {self.operation_name}")
        
        return False

def safe_execute(func, *args, default_return=None, logger_type="error", **kwargs):
    """Safely execute a function with exception handling"""
    logger = get_logger(logger_type)
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error executing {func.__name__}: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return default_return