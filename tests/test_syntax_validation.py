#!/usr/bin/env python3
"""
Complete test to verify the Empty module name error is fixed
"""

import sys
from pathlib import Path
import tempfile
import ast

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_generated_code_syntax():
    """Test that generated code has valid Python syntax"""
    try:
        from services.ai_service import AIService
        from config.settings import config
        
        print("🔧 Testing Generated Code Syntax Validation...")
        
        ai_service = AIService(config.ai)
        
        # Test with a simple command
        test_command = "Create a simple 2BHK house"
        print(f"🏠 Generating code for: '{test_command}'")
        
        generated_code = ai_service.generate_freecad_code(test_command, "3d")
        
        if not generated_code:
            print("❌ No code generated")
            return False
            
        print(f"✅ Generated {len(generated_code)} characters of code")
        
        # Test syntax by compiling the code
        try:
            ast.parse(generated_code)
            print("✅ Code has valid Python syntax")
        except SyntaxError as e:
            print(f"❌ Syntax error in generated code: {e}")
            print(f"   Line {e.lineno}: {e.text}")
            return False
        
        # Test for empty import issues
        lines = generated_code.split('\n')
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped in ['import', 'from', 'import ', 'from ']:
                print(f"❌ Empty import statement found at line {i}: '{line}'")
                return False
            if stripped.startswith('import ') and len(stripped.replace('import ', '').strip()) == 0:
                print(f"❌ Malformed import statement at line {i}: '{line}'")
                return False
            if stripped.startswith('from ') and 'import' not in stripped:
                print(f"❌ Incomplete from statement at line {i}: '{line}'")
                return False
                
        print("✅ No empty or malformed import statements found")
        
        # Save to temporary file and try to execute imports
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(generated_code)
            temp_file = f.name
        
        try:
            # Try to compile and execute just the import statements
            import_lines = [line for line in lines if line.strip().startswith(('import ', 'from '))]
            import_code = '\n'.join(import_lines)
            
            if import_code:
                exec(compile(import_code, '<test>', 'exec'))
                print("✅ All import statements execute successfully")
        except Exception as e:
            print(f"❌ Import execution failed: {e}")
            return False
        finally:
            # Clean up
            import os
            if os.path.exists(temp_file):
                os.unlink(temp_file)
        
        print("✅ All syntax validation tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during syntax test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🔧 Complete Empty Module Name Error Fix Verification")
    print("=" * 60)
    
    syntax_ok = test_generated_code_syntax()
    
    print("\n" + "=" * 60)
    print(f"Syntax Validation: {'✅ PASS' if syntax_ok else '❌ FAIL'}")
    
    if syntax_ok:
        print("\n🎉 All tests passed! The Empty module name error is fixed!")
        print("Your Voice-to-CAD system should work without syntax errors.")
    else:
        print("\n❌ Some issues remain. Check the errors above.")

if __name__ == "__main__":
    main()