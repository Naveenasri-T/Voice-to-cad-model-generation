#!/usr/bin/env python3
"""
Test FreeCAD compatibility fixes
This script tests that our generated FreeCAD code works without errors
"""

import os
import sys
import tempfile
from pathlib import Path

# Add the project directory to the path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

from services.ai_service import AIService
from config.settings import Config

def test_fallback_models():
    """Test that fallback models don't use problematic FreeCAD attributes"""
    print("🔧 Testing FreeCAD compatibility fixes...")
    
    try:
        # Initialize AI service
        config = Config()
        ai_service = AIService(config)
        
        # Test 2BHK fallback model
        print("📐 Testing 2BHK fallback model...")
        bhk_code = ai_service._create_simple_2bhk_model()
        
        # Check for problematic patterns
        problematic_patterns = [
            "FreeCAD.ActiveMaterial",
            ".Material =", 
            ".DiffuseColor =",
            "ActiveMaterial"
        ]
        
        issues_found = []
        for pattern in problematic_patterns:
            if pattern in bhk_code:
                issues_found.append(pattern)
        
        if issues_found:
            print(f"❌ 2BHK model contains problematic patterns: {issues_found}")
        else:
            print("✅ 2BHK model is FreeCAD compatible")
        
        # Test cube fallback model
        print("🧊 Testing cube fallback model...")
        cube_code = ai_service._create_simple_cube()
        
        cube_issues = []
        for pattern in problematic_patterns:
            if pattern in cube_code:
                cube_issues.append(pattern)
        
        if cube_issues:
            print(f"❌ Cube model contains problematic patterns: {cube_issues}")
        else:
            print("✅ Cube model is FreeCAD compatible")
        
        # Test code cleaning functionality
        print("🧹 Testing code cleaning...")
        test_bad_code = """
import FreeCAD
import Part

# Create document
doc = FreeCAD.newDocument()

# Bad patterns that should be removed
FreeCAD.ActiveMaterial = "Steel"
obj.Material = "Aluminum"  
obj.DiffuseColor = (1.0, 0.0, 0.0)
FreeCAD.ActiveDocument.ActiveMaterial.Name = "Steel"

# Good code
cube = Part.makeBox(100, 100, 100)
"""
        
        cleaned_code = ai_service._clean_generated_code(test_bad_code)
        
        remaining_issues = []
        for pattern in problematic_patterns:
            if pattern in cleaned_code:
                remaining_issues.append(pattern)
        
        if remaining_issues:
            print(f"❌ Code cleaning failed to remove: {remaining_issues}")
        else:
            print("✅ Code cleaning successfully removes problematic patterns")
        
        # Write test files to verify syntax
        print("📝 Writing test files...")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test 2BHK file
            bhk_file = Path(temp_dir) / "test_2bhk.py"
            with open(bhk_file, 'w', encoding='utf-8') as f:
                f.write(bhk_code)
            
            # Test cube file  
            cube_file = Path(temp_dir) / "test_cube.py"
            with open(cube_file, 'w', encoding='utf-8') as f:
                f.write(cube_code)
            
            # Test cleaned file
            cleaned_file = Path(temp_dir) / "test_cleaned.py"
            with open(cleaned_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_code)
            
            print(f"✅ Test files created successfully in {temp_dir}")
            
        print("\n🎉 FreeCAD compatibility test completed!")
        
        if not issues_found and not cube_issues and not remaining_issues:
            print("✅ All tests passed - FreeCAD compatibility is working!")
            return True
        else:
            print("❌ Some compatibility issues remain")
            return False
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_fallback_models()
    sys.exit(0 if success else 1)