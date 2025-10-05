"""
Test for preventing syntax errors in generated code
"""
import unittest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.code_cleaning import super_clean_ai_code, validate_python_syntax
from utils.logging_config import get_logger

class TestCodeSyntaxValidation(unittest.TestCase):
    """Test code syntax validation and cleaning"""
    
    def setUp(self):
        self.logger = get_logger("test")
    
    def test_dirty_code_with_explanatory_text(self):
        """Test cleaning code that contains explanatory text like the error we fixed"""
        
        dirty_code = '''
import FreeCAD
import Part
import FreeCADGui

# Create document
doc = FreeCAD.newDocument("Test")

# Create a cube
cube = Part.makeBox(10, 10, 10)
doc.addObject("Part::Feature", "Cube").Shape = cube

doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.viewAxometric()

This script will create a detailed 2BHK house model with proper rooms and structure according to the given requirements. The model includes two bedrooms, a hall, a kitchen, a bathroom, connecting walls between rooms, doors, windows, and a foundation/floor base. The script uses the FreeCAD API to create the model and position each room and object according to the given layout positions.
'''
        
        # Clean the code
        clean_code = super_clean_ai_code(dirty_code)
        
        # Test that explanatory text is removed
        self.assertNotIn("This script will create", clean_code)
        self.assertNotIn("The model includes", clean_code)
        self.assertNotIn("according to the given", clean_code)
        
        # Test that code remains
        self.assertIn("import FreeCAD", clean_code)
        self.assertIn("Part.makeBox", clean_code)
        self.assertIn("doc.recompute()", clean_code)
        
        # Test syntax validation
        is_valid, message = validate_python_syntax(clean_code)
        self.assertTrue(is_valid, f"Cleaned code should have valid syntax: {message}")
        
        self.logger.info("✅ Dirty code cleaning test passed")
    
    def test_code_with_artifacts(self):
        """Test removing various AI artifacts"""
        
        code_with_artifacts = '''
Here's a FreeCAD script for you:

```python
import FreeCAD
import Part

doc = FreeCAD.newDocument()
cube = Part.makeBox(5, 5, 5)
doc.addObject("Part::Feature", "Cube").Shape = cube
doc.recompute()
```

This is a simple script that creates a cube.
Note that you might need to adjust parameters.
However, this should work for most cases.
'''
        
        clean_code = super_clean_ai_code(code_with_artifacts)
        
        # Test artifact removal
        self.assertNotIn("Here's a FreeCAD script", clean_code)
        self.assertNotIn("```", clean_code)
        self.assertNotIn("This is a simple", clean_code)
        self.assertNotIn("Note that", clean_code)
        self.assertNotIn("However,", clean_code)
        
        # Test syntax validation
        is_valid, message = validate_python_syntax(clean_code)
        self.assertTrue(is_valid, f"Cleaned code should have valid syntax: {message}")
        
        self.logger.info("✅ Artifacts removal test passed")
    
    def test_valid_code_unchanged(self):
        """Test that already valid code is not damaged"""
        
        valid_code = '''import FreeCAD
import Part

# Create document
doc = FreeCAD.newDocument("Test")

# Create objects
cube = Part.makeBox(10, 10, 10)
sphere = Part.makeSphere(5)

# Add to document
doc.addObject("Part::Feature", "Cube").Shape = cube
doc.addObject("Part::Feature", "Sphere").Shape = sphere

# Finalize
doc.recompute()'''
        
        clean_code = super_clean_ai_code(valid_code)
        
        # Test that all important parts remain
        self.assertIn("import FreeCAD", clean_code)
        self.assertIn("import Part", clean_code)
        self.assertIn("Part.makeBox", clean_code)
        self.assertIn("Part.makeSphere", clean_code)
        self.assertIn("doc.recompute()", clean_code)
        
        # Test syntax validation
        is_valid, message = validate_python_syntax(clean_code)
        self.assertTrue(is_valid, f"Valid code should remain valid: {message}")
        
        self.logger.info("✅ Valid code preservation test passed")
    
    def test_draw_dynamic_style_error(self):
        """Test the specific type of error we encountered with draw_dynamic.py"""
        
        problematic_code = '''import FreeCAD
import Part

doc = FreeCAD.newDocument("House")
hall = Part.makeBox(15, 12, 10)
doc.addObject("Part::Feature", "Hall").Shape = hall

doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.viewAxometric()
This script will create a detailed 2BHK house model with proper rooms and structure according to the given requirements.'''
        
        clean_code = super_clean_ai_code(problematic_code)
        
        # Test that the problematic text is removed
        self.assertNotIn("This script will create", clean_code)
        self.assertNotIn("according to the given", clean_code)
        
        # Test syntax validation (this should pass now)
        is_valid, message = validate_python_syntax(clean_code)
        self.assertTrue(is_valid, f"Fixed code should have valid syntax: {message}")
        
        self.logger.info("✅ draw_dynamic style error prevention test passed")

if __name__ == "__main__":
    unittest.main(verbosity=2)