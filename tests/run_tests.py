"""
Test runner for all Voice-to-CAD tests
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logging_config import get_logger

def run_all_tests():
    """Run all tests in the tests directory"""
    
    logger = get_logger("test")
    logger.info("Starting comprehensive test suite")
    
    # Discover and run tests
    test_dir = os.path.dirname(os.path.abspath(__file__))
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir, pattern='test_*.py')
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Log summary
    if result.wasSuccessful():
        logger.info(f"✅ All tests passed! Ran {result.testsRun} tests")
    else:
        logger.error(f"❌ Tests failed: {len(result.failures)} failures, {len(result.errors)} errors")
        
        if result.failures:
            logger.error("Failures:")
            for test, traceback in result.failures:
                logger.error(f"  - {test}: {traceback}")
        
        if result.errors:
            logger.error("Errors:")
            for test, traceback in result.errors:
                logger.error(f"  - {test}: {traceback}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)