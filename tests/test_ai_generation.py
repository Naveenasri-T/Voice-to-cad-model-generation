"""
Test AI code generation functionality
"""
import unittest
import os
import sys
import tempfile
import py_compile

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logging_config import get_logger
from utils.exceptions import ExceptionContext
from config.settings import get_config

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

class TestAIGeneration(unittest.TestCase):
    """Test AI code generation"""
    
    def setUp(self):
        self.config = get_config()
        self.logger = get_logger("test")
        
        if GROQ_AVAILABLE and self.config.groq.api_key:
            self.client = Groq(api_key=self.config.groq.api_key)
        else:
            self.client = None
    
    @unittest.skipIf(not GROQ_AVAILABLE, "Groq not available")
    def test_api_connection(self):
        """Test Groq API connection"""
        if not self.client:
            self.skipTest("No API key configured")
        
        self.logger.info("Testing Groq API connection")
        
        with ExceptionContext("API Connection Test"):
            response = self.client.chat.completions.create(
                model=self.config.groq.model,
                messages=[{"role": "user", "content": "Say hello"}],
                temperature=0.1,
                max_tokens=50
            )
            
            self.assertIsNotNone(response.choices[0].message.content)
            self.logger.info("API connection successful")
    
    def test_code_cleaning_function(self):
        """Test code cleaning functionality"""
        
        # Sample dirty code with explanatory text
        dirty_code = '''
Here's a FreeCAD script for you:

```python
import FreeCAD
import Part

doc = FreeCAD.newDocument()
cube = Part.makeBox(10, 10, 10)
doc.addObject("Part::Feature", "Cube").Shape = cube
doc.recompute()
```

This script creates a simple cube.
'''
        
        # Import the cleaning function
        from voice_to_cad import _clean_ai_code
        
        clean_code = _clean_ai_code(dirty_code)
        
        # Test that explanatory text is removed
        self.assertNotIn("Here's a FreeCAD script", clean_code)
        self.assertNotIn("This script creates", clean_code)
        self.assertNotIn("```", clean_code)
        
        # Test that actual code remains
        self.assertIn("import FreeCAD", clean_code)
        self.assertIn("Part.makeBox", clean_code)
        
        # Test syntax validity
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(clean_code)
            temp_filename = f.name
        
        try:
            py_compile.compile(temp_filename, doraise=True)
            self.logger.info("Cleaned code has valid syntax")
        except py_compile.PyCompileError as e:
            self.fail(f"Cleaned code has invalid syntax: {e}")
        finally:
            os.unlink(temp_filename)

class Test2BHKGeneration(unittest.TestCase):
    """Test 2BHK house generation"""
    
    def setUp(self):
        self.config = get_config()
        self.logger = get_logger("test")
    
    def test_2bhk_prompt_detection(self):
        """Test 2BHK prompt detection"""
        
        # Test commands that should trigger 2BHK generation
        bhk_commands = [
            "create a 2bhk house",
            "generate 2BHK house with parking",
            "build a house with 2 bedrooms",
            "make a home with two bedrooms"
        ]
        
        for command in bhk_commands:
            with self.subTest(command=command):
                # Check if command contains house-related keywords
                is_house_command = any(keyword in command.lower() for keyword in 
                                     ["bhk", "house", "home", "bedroom"])
                self.assertTrue(is_house_command, 
                              f"Command '{command}' should be detected as house command")

if __name__ == "__main__":
    unittest.main(verbosity=2)