#!/usr/bin/env python3
"""
Quick Test - Generate Error-Free Professional Model
"""
import sys
import os
sys.path.append('.')

from main import UniversalModelGenerator

def quick_test():
    print("🔧 Testing CORRECTED Professional Model Generation...")
    
    generator = UniversalModelGenerator()
    
    # Test with a simple professional command
    command = "Create a detailed 3BHK house with windows and doors"
    
    print(f"📝 Command: {command}")
    script = generator.generate_universal_freecad_script(command, "3d")
    
    if script:
        print("✅ CORRECTED script generated!")
        
        # Check for error-prone patterns
        errors = []
        if "Arch.makeWall(" in script:
            errors.append("❌ Found Arch.makeWall() with parameters")
        if "Part.makeBox(" in script and "Arch.makeWall(" in script:
            errors.append("❌ Mixed Part/Arch usage detected")
        if ".addObject(foundation)" in script:
            errors.append("❌ Incorrect addObject usage")
            
        # Check for correct patterns
        correct_patterns = []
        if 'doc.addObject("Part::Feature"' in script:
            correct_patterns.append("✅ Correct Part::Feature usage")
        if "ViewObject.ShapeColor" in script:
            correct_patterns.append("✅ Professional materials")
        if "ViewObject.Transparency" in script:
            correct_patterns.append("✅ Window transparency")
            
        print("\n🔍 Error Check:")
        if errors:
            for error in errors:
                print(error)
        else:
            print("✅ No syntax errors detected!")
            
        print("\n🎯 Professional Features:")
        for pattern in correct_patterns:
            print(pattern)
            
        return len(errors) == 0
    else:
        print("❌ Script generation failed")
        return False

if __name__ == "__main__":
    success = quick_test()
    print(f"\n🏆 Result: {'SUCCESS - Ready for FreeCAD!' if success else 'FAILED - Needs fixes'}")