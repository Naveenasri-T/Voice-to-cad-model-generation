"""
Test script to verify the Voice-to-CAD functionality
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from voice_to_cad import generate_script_with_ai, _clean_ai_code

def test_ai_code_generation():
    """Test the AI code generation functionality"""
    print("Testing AI code generation...")
    
    # Test simple command
    test_command = "create a cube with side length 10"
    
    try:
        script = generate_script_with_ai(test_command)
        print(f"✅ Successfully generated script for: {test_command}")
        print(f"Script preview (first 200 chars): {script[:200]}...")
        
        # Save test script
        with open("test_output.py", "w", encoding="utf-8") as f:
            f.write(script)
        print("✅ Test script saved as 'test_output.py'")
        
    except Exception as e:
        print(f"❌ Error generating script: {e}")

def test_code_cleaning():
    """Test the code cleaning function"""
    print("\nTesting code cleaning...")
    
    # Test with code blocks
    dirty_code = """```python
import FreeCAD
doc = FreeCAD.newDocument()
```"""
    
    clean_code = _clean_ai_code(dirty_code)
    print(f"✅ Cleaned code: {clean_code}")

if __name__ == "__main__":
    print("🧪 Running Voice-to-CAD Tests\n")
    test_code_cleaning()
    test_ai_code_generation()
    print("\n✅ All tests completed!")