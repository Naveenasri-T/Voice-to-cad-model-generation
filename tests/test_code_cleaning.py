#!/usr/bin/env python3
"""
Test for empty module name fix
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_code_cleaning():
    """Test the code cleaning function"""
    try:
        from services.ai_service import AIService
        from config.settings import config
        
        print("🔧 Testing Code Cleaning for Empty Module Name Fix...")
        
        # Create a sample problematic code with duplicate imports and empty imports
        problematic_code = """import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
# Import necessary modules
import FreeCAD
import Part
import 
from 
from import
import  

# Create a simple cube
cube = doc.addObject("Part::Box", "Cube")
cube.Length = 1000
cube.Width = 1000  
cube.Height = 1000

doc.recompute()
"""
        
        ai_service = AIService(config.ai)
        
        print("🧹 Running code cleaning...")
        cleaned_code = ai_service._clean_generated_code(problematic_code)
        
        print(f"✅ Cleaned code length: {len(cleaned_code)}")
        
        # Check for issues
        issues = []
        if 'import \n' in cleaned_code:
            issues.append("Empty import statement found")
        if 'from \n' in cleaned_code:
            issues.append("Empty from statement found")
        if 'import FreeCAD\nimport FreeCAD' in cleaned_code:
            issues.append("Duplicate imports found")
        
        if issues:
            print("❌ Issues found:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        else:
            print("✅ No issues found in cleaned code!")
            print("📄 Cleaned code preview:")
            print("-" * 50)
            lines = cleaned_code.split('\n')
            for i, line in enumerate(lines[:10], 1):
                print(f"{i:2}: {line}")
            if len(lines) > 10:
                print("... (truncated)")
            print("-" * 50)
            return True
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🔧 Empty Module Name Error Fix Test")
    print("=" * 50)
    
    test_ok = test_code_cleaning()
    
    print("\n" + "=" * 50)
    print(f"Test Result: {'✅ PASS' if test_ok else '❌ FAIL'}")
    
    if test_ok:
        print("🎉 Code cleaning is working properly!")
    else:
        print("⚠️ Code cleaning needs more work.")

if __name__ == "__main__":
    main()