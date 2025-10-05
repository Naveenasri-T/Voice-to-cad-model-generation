#!/usr/bin/env python3
"""
Final Test - Clean Professional Models
"""
from main import UniversalModelGenerator

def final_test():
    print("🎯 FINAL TEST - Error-Free Professional Models")
    
    generator = UniversalModelGenerator()
    
    # Test command
    command = "Create a modern 3BHK house with professional architecture"
    
    print(f"📝 Command: {command}")
    script = generator.generate_universal_freecad_script(command, "3d")
    
    if script:
        print("✅ Script generated successfully!")
        
        # Check for common issues
        issues = []
        if "You can" in script:
            issues.append("❌ Contains explanatory text")
        if "`" in script:
            issues.append("❌ Contains markdown backticks")
        if "customize" in script.lower():
            issues.append("❌ Contains customization suggestions")
        
        if issues:
            print("\n🚨 Issues found:")
            for issue in issues:
                print(issue)
        else:
            print("✅ Clean code - No explanatory text!")
            
        # Show first few lines
        lines = script.split('\n')[:15]
        print("\n📄 Generated Code Preview:")
        for i, line in enumerate(lines, 1):
            print(f"{i:2d}: {line}")
            
        return len(issues) == 0
    else:
        print("❌ Generation failed")
        return False

if __name__ == "__main__":
    success = final_test()
    print(f"\n🏆 Status: {'READY FOR FREECAD!' if success else 'Needs more fixes'}")