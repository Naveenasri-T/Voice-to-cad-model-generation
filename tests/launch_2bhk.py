"""
Launch the enhanced 2BHK house model in FreeCAD
"""
import os
import subprocess

# FreeCAD path - adjust if your installation path is different
FREECAD_PATH = r"C:\Program Files\FreeCAD 1.0\bin\FreeCAD.exe"
if not os.path.exists(FREECAD_PATH):
    # Try alternative common paths
    alt_paths = [
        r"C:\Program Files\FreeCAD 0.21\bin\FreeCAD.exe",
        r"C:\Program Files (x86)\FreeCAD 1.0\bin\FreeCAD.exe", 
        r"C:\Program Files (x86)\FreeCAD 0.21\bin\FreeCAD.exe"
    ]
    for path in alt_paths:
        if os.path.exists(path):
            FREECAD_PATH = path
            break

def launch_2bhk_house():
    """Launch the 2BHK house model in FreeCAD"""
    script_path = os.path.abspath("2bhk_house_enhanced.py")
    
    if not os.path.exists(script_path):
        print("❌ 2bhk_house_enhanced.py not found! Run test_2bhk.py first.")
        return
    
    if not os.path.exists(FREECAD_PATH):
        print("❌ FreeCAD not found! Please install FreeCAD or update the path.")
        print(f"Looking for: {FREECAD_PATH}")
        return
    
    try:
        print("🚀 Launching 2BHK house model in FreeCAD...")
        subprocess.Popen([FREECAD_PATH, script_path], shell=False)
        print("✅ FreeCAD launched successfully!")
        print("🏠 Your detailed 2BHK house model should open in FreeCAD.")
    except Exception as e:
        print(f"❌ Error launching FreeCAD: {e}")

if __name__ == "__main__":
    launch_2bhk_house()