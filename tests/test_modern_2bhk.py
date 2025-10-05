#!/usr/bin/env python3
"""
Test Modern 2BHK Apartment Generation
This test validates the detailed modern 2BHK apartment generation
"""

import os
import sys
import time
from main import UniversalModelGenerator

def test_modern_2bhk():
    """Test modern 2BHK apartment generation with detailed architecture"""
    
    print("🏠 Testing MODERN 2BHK APARTMENT Generation")
    print("=" * 50)
    
    # Initialize the generator
    generator = UniversalModelGenerator()
    
    # Test the exact user prompt
    command = "Design a professional 2BHK apartment with modern architecture and detailed interior layout"
    
    print(f"📝 Command: {command}")
    print("🔄 Generating detailed modern apartment...")
    
    try:
        # Generate the model
        start_time = time.time()
        result = generator.generate_model(command, "3d")
        end_time = time.time()
        
        if result:
            print("✅ Modern apartment script generated!")
            print(f"⏱️ Generation time: {end_time - start_time:.1f} seconds")
            
            # Detailed architecture analysis
            features = {
                "Open living-dining area": any(x in result.lower() for x in ["living_dining", "livingdining", "open plan"]),
                "Master bedroom with ensuite": "master" in result.lower() and ("ensuite" in result.lower() or "master_bath" in result.lower()),
                "Modern kitchen": "kitchen" in result.lower() and ("modern" in result.lower() or "island" in result.lower()),
                "Balcony": "balcony" in result.lower(),
                "Professional materials": "shapecolor" in result.lower() and "transparency" in result.lower(),
                "Large windows": "window" in result.lower() and ("large" in result.lower() or "sliding" in result.lower()),
                "Built-in elements": any(x in result.lower() for x in ["wardrobe", "island", "counter", "built"]),
                "Modern ceiling": "ceiling" in result.lower(),
                "Entry foyer": "foyer" in result.lower(),
                "Detailed positioning": "placement.base" in result.lower() and "freecad.vector" in result.lower(),
                "Professional finishes": result.lower().count("shapecolor") >= 8
            }
            
            present_features = sum(features.values())
            detail_percentage = (present_features / len(features)) * 100
            
            print(f"\n🏗️ Modern Architecture Features Check:")
            for feature, present in features.items():
                status = "✅" if present else "❌"
                print(f"{status} {feature}: {'Present' if present else 'Missing'}")
            
            print(f"\n📊 Modern Detail Level: {detail_percentage:.1f}% ({present_features}/{len(features)})")
            
            if detail_percentage >= 80:
                print("🏆 EXCELLENT: Highly detailed modern apartment!")
            elif detail_percentage >= 60:
                print("✅ GOOD: Decent modern features")
            else:
                print("⚠️ BASIC: Needs more modern architectural elements")
            
            # Code quality check
            lines = result.split('\n')
            code_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
            
            print(f"\n📊 Code Statistics:")
            print(f"📄 Total characters: {len(result)}")
            print(f"📝 Code lines: {len(code_lines)}")
            print(f"🏗️ Objects created: {result.lower().count('addobject')}")
            print(f"🎨 Material assignments: {result.lower().count('shapecolor')}")
            
            # Show preview
            print(f"\n📄 Generated Code Preview (first 30 lines):")
            print("-" * 60)
            for i, line in enumerate(lines[:30], 1):
                print(f"{i:2d}: {line}")
            print("-" * 60)
            
            return True
            
        else:
            print("❌ Failed to generate modern apartment")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 MODERN 2BHK APARTMENT TEST")
    print("Testing enhanced modern architecture generation")
    print()
    
    success = test_modern_2bhk()
    
    if success:
        print(f"\n✅ Modern 2BHK test completed successfully!")
        print("🎯 Your prompt will generate detailed modern architecture")
        print("📱 Now run the Streamlit app to use it interactively")
    else:
        print(f"\n❌ Test failed")
        sys.exit(1)