#!/usr/bin/env python3
"""
Test Detailed 3BHK House Generation
"""
from main import UniversalModelGenerator

def test_detailed_3bhk():
    print("🏠 Testing DETAILED 3BHK House with Parking Generation")
    
    generator = UniversalModelGenerator()
    
    # Your exact command
    command = "Create a 3BHK house with parking"
    
    print(f"📝 Command: {command}")
    print("🔄 Generating detailed architectural model...")
    
    script = generator.generate_universal_freecad_script(command, "3d")
    
    if script:
        print("✅ Detailed model script generated!")
        
        # Check for detailed features
        detailed_features = [
            ("Individual room floors", "Living_Room_Floor" in script or "living_room_floor" in script),
            ("Master bedroom", "Master" in script or "master" in script),
            ("Multiple bedrooms", "Bedroom2" in script or "bed2" in script),  
            ("Kitchen area", "Kitchen" in script or "kitchen" in script),
            ("Bathrooms", "Bathroom" in script or "bath" in script),
            ("Parking area", "parking" in script.lower()),
            ("Individual walls", "living_wall" in script or "master_wall" in script),
            ("Windows", "window" in script.lower()),
            ("Doors", "door" in script.lower()),
            ("Room-specific colors", "ViewObject.ShapeColor" in script),
            ("Detailed dimensions", "4000" in script and "3000" in script),  # Room dimensions
        ]
        
        print("\n🏗️ Detailed Architecture Features Check:")
        detailed_count = 0
        for feature, present in detailed_features:
            status = "✅" if present else "❌"
            print(f"{status} {feature}: {'Present' if present else 'Missing'}")
            if present:
                detailed_count += 1
        
        detail_percentage = (detailed_count / len(detailed_features)) * 100
        print(f"\n📊 Detail Level: {detail_percentage:.1f}% ({detailed_count}/{len(detailed_features)})")
        
        if detail_percentage >= 80:
            print("🏆 EXCELLENT: Highly detailed architectural model!")
        elif detail_percentage >= 60:
            print("👍 GOOD: Reasonably detailed model")  
        elif detail_percentage >= 40:
            print("⚠️ BASIC: Some detail but needs improvement")
        else:
            print("❌ TOO SIMPLE: Needs major improvement")
        
        # Show code preview
        print(f"\n📄 Generated Code Preview (first 25 lines):")
        print("-" * 60)
        lines = script.split('\n')[:25]
        for i, line in enumerate(lines, 1):
            print(f"{i:2d}: {line}")
        print("-" * 60)
        
        return detail_percentage >= 60
    else:
        print("❌ Script generation failed")
        return False

if __name__ == "__main__":
    success = test_detailed_3bhk()
    print(f"\n🎯 Result: {'READY FOR DETAILED ARCHITECTURE!' if success else 'NEEDS MORE DETAIL ENHANCEMENT'}")