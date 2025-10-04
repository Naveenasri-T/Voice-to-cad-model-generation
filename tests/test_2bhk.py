"""
Test script for 2BHK house generation
"""
import os
import sys
from dotenv import load_dotenv
from groq import Groq
import re

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def _clean_ai_code(raw_code: str) -> str:
    if not raw_code:
        return ""
    cleaned = re.sub(r"^```(?:python)?\s*", "", raw_code, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.replace("```", "")
    return cleaned.strip()

def generate_2bhk_house():
    """Generate enhanced 2BHK house model"""
    
    command_text = "create a 2bhk house with proper rooms layout"
    
    prompt = f"""
    You are an expert FreeCAD architect. Create a detailed 2BHK house model with proper rooms and structure.

    MANDATORY 2BHK HOUSE REQUIREMENTS:
    - 2 Bedrooms (each 12x10x10 units)
    - 1 Hall/Living room (15x12x10 units)  
    - 1 Kitchen (10x8x10 units)
    - 1 Bathroom (8x6x10 units)
    - Connecting walls between rooms
    - Doors (2x8x1 units) between rooms
    - Windows (4x6x0.5 units) on exterior walls
    - Foundation/floor base

    CONSTRUCTION RULES:
    - Always import: import FreeCAD, Part, Draft, FreeCADGui
    - Create document: doc = FreeCAD.newDocument("2BHK_House")
    - Use Part.makeBox(length, width, height) for rooms and walls
    - Use Part.cut(wall, door_opening) for door openings
    - Position each room using: obj.Placement.Base = FreeCAD.Vector(x, y, z)
    - Wall thickness: 1 unit
    - Room height: 10 units
    - Create proper layout with connecting passages

    EXACT LAYOUT POSITIONS:
    - Hall: Position(0, 0, 0) - Size(15, 12, 10)
    - Bedroom1: Position(16, 0, 0) - Size(12, 10, 10) 
    - Bedroom2: Position(16, 11, 0) - Size(12, 10, 10)
    - Kitchen: Position(0, 13, 0) - Size(10, 8, 10)
    - Bathroom: Position(11, 13, 0) - Size(8, 6, 10)

    Create each room as separate objects with proper names.
    Add walls between rooms with door openings.
    End with: doc.recompute(), viewAxometric(), ViewFit()

    Command: "{command_text}"
    """
    
    try:
        print("🏠 Generating enhanced 2BHK house model...")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=3000
        )
        
        raw_code = response.choices[0].message.content
        clean_code = _clean_ai_code(raw_code)
        
        # Save the generated script
        with open("2bhk_house_enhanced.py", "w", encoding="utf-8") as f:
            f.write(clean_code)
        
        print("✅ Enhanced 2BHK house script generated!")
        print("📁 Saved as: 2bhk_house_enhanced.py")
        print(f"📝 Script preview:\n{clean_code[:500]}...")
        
        return clean_code
        
    except Exception as e:
        print(f"❌ Error generating 2BHK house: {e}")
        return None

if __name__ == "__main__":
    print("🏗️ Testing Enhanced 2BHK House Generation\n")
    generate_2bhk_house()
    print("\n🎯 Test completed! Check the generated file.")