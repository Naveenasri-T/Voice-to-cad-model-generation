"""
Comprehensive test suite for Voice-to-CAD application
"""
import unittest
import os
import sys
import tempfile
import py_compile

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logging_config import get_logger
from utils.exceptions import ExceptionContext, safe_execute
from config.settings import get_config

class TestConfiguration(unittest.TestCase):
    """Test configuration management"""
    
    def setUp(self):
        self.config = get_config()
        self.logger = get_logger("test")
    
    def test_config_loading(self):
        """Test configuration loading"""
        self.logger.info("Testing configuration loading")
        
        # Test that config is loaded
        self.assertIsNotNone(self.config.groq.api_key)
        self.assertIsNotNone(self.config.freecad.executable_path)
        
    def test_directory_creation(self):
        """Test that required directories exist"""
        self.logger.info("Testing directory creation")
        
        directories = [
            self.config.paths.audio_dir,
            self.config.paths.generated_dir,
            self.config.paths.logs_dir,
            self.config.paths.tests_dir,
            self.config.paths.models_dir
        ]
        
        for directory in directories:
            self.assertTrue(os.path.exists(directory), f"Directory {directory} should exist")

class TestLogging(unittest.TestCase):
    """Test logging functionality"""
    
    def test_logger_creation(self):
        """Test logger creation"""
        logger = get_logger("test")
        self.assertIsNotNone(logger)
        
        # Test different logger types
        app_logger = get_logger("app")
        ai_logger = get_logger("ai")
        error_logger = get_logger("error")
        
        self.assertIsNotNone(app_logger)
        self.assertIsNotNone(ai_logger)
        self.assertIsNotNone(error_logger)
    
    def test_logging_output(self):
        """Test logging output"""
        logger = get_logger("test")
        
        # Test different log levels
        logger.debug("Test debug message")
        logger.info("Test info message")
        logger.warning("Test warning message")
        logger.error("Test error message")

class TestExceptionHandling(unittest.TestCase):
    """Test exception handling utilities"""
    
    def test_exception_context(self):
        """Test exception context manager"""
        logger = get_logger("test")
        
        # Test successful operation
        with ExceptionContext("test_operation", reraise=False) as ctx:
            result = 1 + 1
            self.assertEqual(result, 2)
        
        # Test failed operation
        with ExceptionContext("test_failed_operation", reraise=False) as ctx:
            result = 1 / 0  # This should raise an exception
    
    def test_safe_execute(self):
        """Test safe execution utility"""
        
        # Test successful function
        def successful_function(x, y):
            return x + y
        
        result = safe_execute(successful_function, 1, 2)
        self.assertEqual(result, 3)
        
        # Test failing function
        def failing_function():
            raise ValueError("Test error")
        
        result = safe_execute(failing_function, default_return="default")
        self.assertEqual(result, "default")

class TestCodeGeneration(unittest.TestCase):
    """Test code generation and cleaning"""
    
    def setUp(self):
        self.config = get_config()
        self.logger = get_logger("test")
    
    def test_code_syntax_validation(self):
        """Test that generated code has valid Python syntax"""
        
        # Sample clean Python code
        clean_code = '''
import FreeCAD
import Part

doc = FreeCAD.newDocument("Test")
cube = Part.makeBox(10, 10, 10)
doc.addObject("Part::Feature", "Cube").Shape = cube
doc.recompute()
'''
        
        # Test syntax validation
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(clean_code)
            temp_filename = f.name
        
        try:
            py_compile.compile(temp_filename, doraise=True)
            self.logger.info("Code syntax validation passed")
        except py_compile.PyCompileError as e:
            self.fail(f"Code syntax validation failed: {e}")
        finally:
            os.unlink(temp_filename)

if __name__ == "__main__":
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestConfiguration,
        TestLogging,
        TestExceptionHandling,
        TestCodeGeneration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Log results
    logger = get_logger("test")
    if result.wasSuccessful():
        logger.info("All tests passed successfully!")
    else:
        logger.error(f"Tests failed: {len(result.failures)} failures, {len(result.errors)} errors")