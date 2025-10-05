"""
Test script to verify code cleaning and generation
"""
import os
import sys
import py_compile
from dotenv import load_dotenv
from groq import Groq
import re

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def _clean_ai_code(raw_code: str) -> str:
    """Enhanced code cleaning function"""
    if not raw_code:
        return ""
    
    # Remove code block markers
    cleaned = re.sub(r"^```(?:python)?\s*", "", raw_code, flags=re.IGNORECASE | re.MULTILINE)
    cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.IGNORECASE | re.MULTILINE)
    cleaned = cleaned.replace("```", "")
    
    # Remove explanatory text before the first import
    lines = cleaned.split('\n')
    code_start = -1
    
    for i, line in enumerate(lines):
        if line.strip().startswith('import ') or line.strip().startswith('# Import'):
            code_start = i
            break
    
    if code_start >= 0:
        cleaned = '\n'.join(lines[code_start:])
    
    # Remove standalone 'python' keywords
    cleaned = re.sub(r'^python\s*$', '', cleaned, flags=re.MULTILINE)
    
    # Remove any remaining explanatory text at the beginning
    cleaned = re.sub(r'^[^#\n]*(?:Here\'s|This is|The following).*?\n', '', cleaned, flags=re.IGNORECASE)
    
    # Remove explanatory text at the end
    lines = cleaned.split('\n')
    code_end = len(lines)
    
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i].strip()
        if line and not line.startswith('#') and not line.startswith('This ') and not line.startswith('The '):
            if 'import ' in line or 'def ' in line or 'class ' in line or any(keyword in line for keyword in ['doc.', 'Part.', 'FreeCAD']):
                code_end = i + 1
                break
    
    cleaned = '\n'.join(lines[:code_end])
    
    return cleaned.strip()

def test_syntax(code_content, filename="test_generated.py"):
    """Test if the generated code has valid Python syntax"""
    try:
        # Write to temporary file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(code_content)
        
        # Try to compile
        py_compile.compile(filename, doraise=True)
        print(f"✅ {filename}: Valid Python syntax")
        return True
        
    except py_compile.PyCompileError as e:
        print(f"❌ {filename}: Syntax error - {e}")
        return False
    except Exception as e:
        print(f"❌ {filename}: Error - {e}")
        return False

def test_code_generation_and_cleaning():
    """Test code generation with various commands"""
    test_commands = [
        "create a simple cube",
        "generate a 2bhk house",
        "make a cylinder with radius 5",
        "build a 3bhk house with parking"
    ]
    
    print("🧪 Testing Code Generation and Cleaning\n")
    
    for i, command in enumerate(test_commands):
        print(f"Test {i+1}: {command}")
        
        # Generate code
        prompt = f"""
        Create FreeCAD Python code for: {command}
        
        Rules:
        - Import FreeCAD, Part, Draft, FreeCADGui
        - Create document: doc = FreeCAD.newDocument()
        - Use Part.makeBox, Part.makeCylinder etc.
        - End with doc.recompute(), viewAxometric(), ViewFit()
        """
        
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=2000
            )
            
            raw_code = response.choices[0].message.content
            clean_code = _clean_ai_code(raw_code)
            
            # Test syntax
            filename = f"test_generated_{i+1}.py"
            if test_syntax(clean_code, filename):
                print(f"   Generated {len(clean_code)} characters of clean code")
            else:
                print(f"   ❌ Failed syntax test")
                print(f"   First 200 chars: {clean_code[:200]}")
            
        except Exception as e:
            print(f"   ❌ Generation failed: {e}")
        
        print()

if __name__ == "__main__":
    test_code_generation_and_cleaning()
    print("🎯 Testing completed!")