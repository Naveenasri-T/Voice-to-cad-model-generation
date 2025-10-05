#!/usr/bin/env python3
"""
Force AI Template Compliance Test
This test forces the AI to follow our exact room-by-room template
"""

import os
import sys
from dotenv import load_dotenv
from groq import Groq

# Load environment
load_dotenv()

def force_detailed_generation():
    """Force AI to generate detailed room-by-room architecture"""
    
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    # Ultra-specific template forcing prompt
    force_prompt = """
You are a FreeCAD expert. Generate EXACTLY this code structure for "3BHK house with parking":

MANDATORY: Copy this EXACT pattern and expand it:

```python
import FreeCAD, Part, Draft, FreeCADGui
import math

doc = FreeCAD.newDocument("Professional_Model")

# STEP 1: Foundation
foundation = doc.addObject("Part::Feature", "Foundation")
foundation.Shape = Part.makeBox(14000, 12000, 600)
foundation.Placement.Base = FreeCAD.Vector(-1000, -1000, -600)
foundation.ViewObject.ShapeColor = (0.3, 0.3, 0.3)

# STEP 2: INDIVIDUAL ROOM FLOORS (MANDATORY)
# Living Room Floor (4m x 5m)
living_room_floor = doc.addObject("Part::Feature", "LivingRoom_Floor")
living_room_floor.Shape = Part.makeBox(4000, 5000, 150)
living_room_floor.Placement.Base = FreeCAD.Vector(0, 0, 0)
living_room_floor.ViewObject.ShapeColor = (0.9, 0.9, 0.8)

# Master Bedroom Floor (4m x 3.5m)
master_bed_floor = doc.addObject("Part::Feature", "MasterBed_Floor")
master_bed_floor.Shape = Part.makeBox(4000, 3500, 150)
master_bed_floor.Placement.Base = FreeCAD.Vector(4200, 0, 0)
master_bed_floor.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

# Bedroom 2 Floor (3m x 3m)
bed2_floor = doc.addObject("Part::Feature", "Bedroom2_Floor")
bed2_floor.Shape = Part.makeBox(3000, 3000, 150)
bed2_floor.Placement.Base = FreeCAD.Vector(4200, 3700, 0)
bed2_floor.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

# Kitchen Floor (3m x 2.5m)
kitchen_floor = doc.addObject("Part::Feature", "Kitchen_Floor")
kitchen_floor.Shape = Part.makeBox(3000, 2500, 150)
kitchen_floor.Placement.Base = FreeCAD.Vector(0, 5200, 0)
kitchen_floor.ViewObject.ShapeColor = (0.8, 0.9, 0.8)

# Bathroom 1 Floor (2m x 2m)
bath1_floor = doc.addObject("Part::Feature", "Bathroom1_Floor")
bath1_floor.Shape = Part.makeBox(2000, 2000, 150)
bath1_floor.Placement.Base = FreeCAD.Vector(8400, 0, 0)
bath1_floor.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

# Bathroom 2 Floor (2m x 2m)
bath2_floor = doc.addObject("Part::Feature", "Bathroom2_Floor")
bath2_floor.Shape = Part.makeBox(2000, 2000, 150)
bath2_floor.Placement.Base = FreeCAD.Vector(8400, 2200, 0)
bath2_floor.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

# Parking Area Floor (5m x 3m)
parking_floor = doc.addObject("Part::Feature", "Parking_Floor")
parking_floor.Shape = Part.makeBox(5000, 3000, 100)
parking_floor.Placement.Base = FreeCAD.Vector(10500, 0, -100)
parking_floor.ViewObject.ShapeColor = (0.7, 0.7, 0.7)
```

CONTINUE this pattern for:
- Room-specific walls for each room
- Windows for each room
- Doors between rooms
- Roof structure

Generate ONLY executable FreeCAD Python code. NO explanations.
"""

    print("🎯 Forcing AI to follow exact template...")
    
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a FreeCAD expert. Generate ONLY executable Python code following the exact pattern provided."},
            {"role": "user", "content": force_prompt}
        ],
        max_tokens=8000,
        temperature=0.0  # Zero temperature for exact compliance
    )
    
    generated_code = response.choices[0].message.content
    
    # Clean the code
    import re
    code_lines = []
    in_code_block = False
    
    for line in generated_code.split('\n'):
        if '```python' in line:
            in_code_block = True
            continue
        elif '```' in line and in_code_block:
            in_code_block = False
            continue
        elif in_code_block or (line.strip() and not line.strip().startswith('#') and ('=' in line or 'import' in line or 'doc.' in line or line.strip().startswith('FreeCAD'))):
            code_lines.append(line)
    
    clean_code = '\n'.join(code_lines)
    
    print(f"📊 Generated Code Length: {len(clean_code)} characters")
    print(f"📝 Lines of Code: {len(clean_code.split())}")
    
    # Check for detailed features
    features = {
        "Individual room floors": "room_floor" in clean_code.lower() or "living_room_floor" in clean_code.lower(),
        "Master bedroom": "master" in clean_code.lower(),
        "Multiple bedrooms": clean_code.lower().count("bedroom") >= 2,
        "Kitchen": "kitchen" in clean_code.lower(),
        "Bathrooms": "bathroom" in clean_code.lower() or "bath" in clean_code.lower(),
        "Parking": "parking" in clean_code.lower(),
        "Room-specific walls": clean_code.lower().count("wall") >= 4,
        "Windows": "window" in clean_code.lower(),
        "Doors": "door" in clean_code.lower(),
        "Detailed positioning": "Placement.Base" in clean_code and "FreeCAD.Vector" in clean_code
    }
    
    present_features = sum(features.values())
    detail_percentage = (present_features / len(features)) * 100
    
    print(f"\n🏗️ Architecture Detail Check:")
    for feature, present in features.items():
        status = "✅" if present else "❌"
        print(f"{status} {feature}: {'Present' if present else 'Missing'}")
    
    print(f"\n📊 Detail Level: {detail_percentage:.1f}% ({present_features}/{len(features)})")
    
    if detail_percentage >= 80:
        print("🏆 EXCELLENT: Highly detailed architectural model!")
    elif detail_percentage >= 60:
        print("✅ GOOD: Decent architectural detail")
    else:
        print("⚠️ BASIC: Needs more architectural detail")
    
    # Save the forced template result
    timestamp = "20251005_112500"  # Fixed timestamp for testing
    filename = f"forced_detailed_3bhk_{timestamp}.py"
    filepath = f"generated/{filename}"
    
    with open(filepath, 'w') as f:
        f.write(clean_code)
    
    print(f"\n💾 Saved to: {filename}")
    
    # Show first 30 lines
    lines = clean_code.split('\n')
    print(f"\n📄 Generated Code Preview (first 30 lines):")
    print("-" * 60)
    for i, line in enumerate(lines[:30], 1):
        print(f"{i:2d}: {line}")
    print("-" * 60)
    
    return clean_code

if __name__ == "__main__":
    print("🔧 FORCE AI TEMPLATE COMPLIANCE TEST")
    print("=" * 50)
    
    try:
        result = force_detailed_generation()
        print(f"\n✅ Force template test completed!")
        print("🎯 Check if the AI followed the room-by-room pattern exactly")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)