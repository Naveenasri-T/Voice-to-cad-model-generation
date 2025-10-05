#!/usr/bin/env python3
"""
Test Professional Model Generation
Generate a sample to show the improved quality
"""
import sys
import os
sys.path.append('.')

# Add the project directory to path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from main import UniversalModelGenerator

def test_professional_model():
    """Test the new professional model generation"""
    
    print("🏗️ Testing Professional Model Generation...")
    
    # Initialize generator
    generator = UniversalModelGenerator()
    
    # Test command
    test_command = "Create a modern 3BHK house with detailed architecture"
    
    print(f"📝 Test Command: {test_command}")
    print("🔄 Generating professional model...")
    
    # Generate the script
    script = generator.generate_universal_freecad_script(test_command, "3d")
    
    if script:
        print("✅ Professional model script generated!")
        print("📄 Script Preview (first 20 lines):")
        print("-" * 50)
        lines = script.split('\n')[:20]
        for i, line in enumerate(lines, 1):
            print(f"{i:2d}: {line}")
        print("-" * 50)
        
        # Check for professional features
        professional_features = [
            ("Arch module", "import Arch" in script),
            ("Professional walls", "Arch.makeWall" in script),
            ("Windows", "Arch.makeWindow" in script or "window" in script.lower()),
            ("Doors", "Arch.makeDoor" in script or "door" in script.lower()),
            ("Materials", "ViewObject.ShapeColor" in script),
            ("Professional standards", "ARCHITECTURAL STANDARDS" in script),
            ("Proper dimensions", "230" in script or "115" in script),  # Wall thicknesses
        ]
        
        print("\n🎯 Professional Features Check:")
        for feature, present in professional_features:
            status = "✅" if present else "❌"
            print(f"{status} {feature}: {'Present' if present else 'Missing'}")
        
        return True
    else:
        print("❌ Failed to generate script")
        return False

if __name__ == "__main__":
    test_professional_model()