#!/usr/bin/env python3
"""
Test the improved ultra_cleaner with the problematic file
"""

import sys
sys.path.append('.')

from ultra_cleaner import ultra_clean_code

def test_problematic_file():
    """Test cleaning the file with incomplete variable name"""
    
    print("🔧 Testing Ultra Cleaner with Problematic File")
    print("=" * 50)
    
    # Read the problematic file
    try:
        with open("generated/Create_a_3BHK_house_20251005_112214.py", 'r') as f:
            problematic_code = f.read()
        
        print(f"📄 Original code length: {len(problematic_code)} characters")
        print(f"🔍 Contains 'bath2_wall_': {'bath2_wall_' in problematic_code}")
        
        # Clean the code
        cleaned_code = ultra_clean_code(problematic_code)
        
        print(f"✨ Cleaned code length: {len(cleaned_code)} characters")
        print(f"🔍 Still contains 'bath2_wall_': {'bath2_wall_' in cleaned_code}")
        
        # Save the cleaned version
        with open("generated/cleaned_3bhk_test.py", 'w') as f:
            f.write(cleaned_code)
        
        print("💾 Cleaned code saved to: generated/cleaned_3bhk_test.py")
        
        # Show the end of the cleaned code
        lines = cleaned_code.split('\n')
        print(f"\n📄 Last 10 lines of cleaned code:")
        print("-" * 40)
        for i, line in enumerate(lines[-10:], len(lines)-9):
            print(f"{i:3d}: {line}")
        print("-" * 40)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_problematic_file()
    if success:
        print("✅ Ultra cleaner test completed!")
    else:
        print("❌ Ultra cleaner test failed!")