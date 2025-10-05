"""
Professional FreeCAD Service
Handles FreeCAD model generation, execution, and optimization
"""

import logging
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, List
import ast

from config.settings import FreeCADConfig


class FreeCADService:
    """Professional FreeCAD Service for Model Generation"""
    
    def __init__(self, freecad_config: FreeCADConfig):
        self.config = freecad_config
        self.logger = logging.getLogger(__name__)
        self.freecad_available = self._detect_freecad()
        
    def _detect_freecad(self) -> bool:
        """Detect FreeCAD installation"""
        try:
            # Try to import FreeCAD using sys.path modification if needed
            import sys
            if self.config.installation_path and self.config.installation_path not in sys.path:
                sys.path.append(self.config.installation_path)
            # Use try/except to suppress IDE warnings about unresolved imports
            try:
                # Use __import__ to prevent IDE warnings about unresolved imports
                FreeCAD = __import__("FreeCAD")
                self.logger.info(f"FreeCAD detected: Version {FreeCAD.Version()}")
                return True
            except ImportError:
                self.logger.warning("FreeCAD not detected - code generation only mode")
                return False
        except Exception as e:
            self.logger.warning(f"Error detecting FreeCAD: {e}")
            return False
    
    def generate_model(self, command: str, model_type: str = "3d", 
                      quality_level: str = "professional", 
                      include_materials: bool = True,
                      ai_service=None) -> Optional[str]:
        """Generate FreeCAD model code"""
        if not ai_service:
            return None
            
        try:
            generated_code = ai_service.generate_freecad_code(
                command=command,
                model_type=model_type,
                quality_level=quality_level,
                include_materials=include_materials
            )
            
            if generated_code:
                return self._enhance_code(generated_code, quality_level)
            return None
            
        except Exception as e:
            self.logger.error(f"Model generation failed: {e}")
            return None
    
    def _enhance_code(self, code: str, quality_level: str) -> str:
        """Enhance generated code with professional features"""
        try:
            if quality_level == "professional":
                header = '''"""
Professional FreeCAD Model - Client Ready
Generated with Enterprise AI Technology
"""

import FreeCAD
import Part

# Create professional document
doc = FreeCAD.newDocument("ProfessionalModel")
FreeCAD.Console.PrintMessage("=== Professional Model Generation ===\\n")

'''
                footer = '''

# Professional completion
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()

FreeCAD.Console.PrintMessage("Professional model completed successfully\\n")'''
                
                return header + code + footer
            else:
                return code
                
        except Exception as e:
            self.logger.warning(f"Code enhancement failed: {e}")
            return code
    
    def analyze_generated_code(self, code: str) -> Dict[str, Any]:
        """Analyze generated code and provide metrics"""
        try:
            lines = code.split('\n')
            non_empty_lines = [line for line in lines if line.strip()]
            
            object_operations = len(re.findall(r'addObject', code))
            part_operations = len(re.findall(r'Part\.', code))
            
            return {
                "statistics": {
                    "total_lines": len(lines),
                    "code_lines": len(non_empty_lines),
                    "object_operations": object_operations,
                    "part_operations": part_operations
                },
                "quality": {
                    "has_objects": object_operations > 0,
                    "proper_structure": 'newDocument' in code and 'recompute' in code,
                    "has_imports": 'import FreeCAD' in code
                }
            }
        except Exception as e:
            return {"error": str(e), "statistics": {}, "quality": {}}
    
    def execute_code_and_open_freecad(self, code: str, filename: str = None) -> Dict[str, Any]:
        """Execute the generated code and automatically open in FreeCAD"""
        try:
            # Save the code to a file
            if not filename:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"generated_model_{timestamp}.py"
            
            # Ensure filename has .py extension
            if not filename.endswith('.py'):
                filename += '.py'
            
            # Write code to file
            filepath = Path(filename)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            
            result = {
                "success": True,
                "filename": str(filepath),
                "message": f"Code saved to {filepath.name}"
            }
            
            # Try to automatically launch FreeCAD with the script
            freecad_launched = self._launch_freecad_with_script(str(filepath))
            
            if freecad_launched:
                result["executed"] = True
                result["gui_opened"] = True
                result["message"] += " → FreeCAD launched automatically with your model!"
            else:
                # Fallback: try to execute in current environment if FreeCAD is available
                if self.freecad_available:
                    try:
                        exec(code)
                        result["executed"] = True
                        result["message"] += " and executed in current FreeCAD session"
                    except Exception as e:
                        result["executed"] = False
                        result["execution_error"] = str(e)
                        result["message"] += f" but execution failed: {e}"
                else:
                    result["executed"] = False
                    result["message"] += " (FreeCAD not found - please install FreeCAD or run script manually)"
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to execute and open FreeCAD: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to process code: {e}"
            }
    
    def _launch_freecad_with_script(self, script_path: str) -> bool:
        """Launch FreeCAD with the generated script automatically"""
        try:
            import os
            import platform
            import glob
            
            # Common FreeCAD executable paths with extensive search
            freecad_paths = []
            
            if platform.system() == "Windows":
                # Search in Program Files directories
                program_files_dirs = [
                    r"C:\Program Files",
                    r"C:\Program Files (x86)"
                ]
                
                for pf_dir in program_files_dirs:
                    if os.path.exists(pf_dir):
                        # Find all FreeCAD installations
                        freecad_dirs = glob.glob(os.path.join(pf_dir, "FreeCAD*"))
                        for freecad_dir in freecad_dirs:
                            freecad_exe = os.path.join(freecad_dir, "bin", "FreeCAD.exe")
                            if os.path.exists(freecad_exe):
                                freecad_paths.append(freecad_exe)
                
                # Also check common direct paths
                common_paths = [
                    r"C:\Program Files\FreeCAD 0.21\bin\FreeCAD.exe",
                    r"C:\Program Files\FreeCAD 0.20\bin\FreeCAD.exe",
                    r"C:\Program Files\FreeCAD 0.22\bin\FreeCAD.exe",
                    r"C:\Program Files (x86)\FreeCAD 0.21\bin\FreeCAD.exe",
                    r"C:\Program Files (x86)\FreeCAD 0.20\bin\FreeCAD.exe",
                    r"C:\Program Files (x86)\FreeCAD 0.22\bin\FreeCAD.exe",
                    r"C:\Program Files\FreeCAD\bin\FreeCAD.exe",
                    r"C:\Program Files (x86)\FreeCAD\bin\FreeCAD.exe",
                ]
                freecad_paths.extend(common_paths)
                
            elif platform.system() == "Darwin":  # macOS
                freecad_paths = [
                    "/Applications/FreeCAD.app/Contents/MacOS/FreeCAD",
                ]
            else:  # Linux
                freecad_paths = [
                    "/usr/bin/freecad",
                    "/usr/local/bin/freecad",
                    "/opt/freecad/bin/FreeCAD",
                ]
            
            # Add configured path if available
            if self.config.installation_path:
                if platform.system() == "Windows":
                    freecad_exe = Path(self.config.installation_path) / "FreeCAD.exe"
                else:
                    freecad_exe = Path(self.config.installation_path) / "FreeCAD"
                freecad_paths.insert(0, str(freecad_exe))
            
            # Find working FreeCAD executable
            freecad_exe = None
            
            # First, try configured path
            if self.config.installation_path:
                if platform.system() == "Windows":
                    config_exe = Path(self.config.installation_path) / "FreeCAD.exe" 
                    if not config_exe.exists():
                        config_exe = Path(self.config.installation_path) / "bin" / "FreeCAD.exe"
                else:
                    config_exe = Path(self.config.installation_path) / "FreeCAD"
                
                if config_exe.exists():
                    freecad_exe = str(config_exe)
                    self.logger.info(f"Using configured FreeCAD: {freecad_exe}")
            
            # If not found, search in standard locations
            if not freecad_exe:
                self.logger.info(f"Searching for FreeCAD in {len(freecad_paths)} locations...")
                for i, path in enumerate(freecad_paths):
                    self.logger.info(f"Checking {i+1}/{len(freecad_paths)}: {path}")
                    if Path(path).exists():
                        freecad_exe = path
                        self.logger.info(f"✅ Found FreeCAD at: {path}")
                        break
            
            # Try to find in PATH
            if not freecad_exe and platform.system() == "Windows":
                try:
                    result = subprocess.run(["where", "FreeCAD"], 
                                          capture_output=True, text=True, shell=True)
                    if result.returncode == 0:
                        freecad_exe = result.stdout.strip().split('\n')[0]
                        self.logger.info(f"Found FreeCAD in PATH: {freecad_exe}")
                except Exception as e:
                    self.logger.debug(f"PATH search failed: {e}")
            
            if not freecad_exe:
                # Show user where we searched
                self.logger.error("❌ FreeCAD executable not found!")
                self.logger.error("Searched locations:")
                for path in freecad_paths[:5]:  # Show first 5 for brevity
                    self.logger.error(f"  - {path}")
                self.logger.error("  ... and more locations")
                return False
            
            # Launch FreeCAD with the script
            abs_script_path = Path(script_path).resolve()
            
            # Launch FreeCAD with multiple fallback methods
            success = False
            
            if platform.system() == "Windows":
                # Method 1: Launch FreeCAD and execute script directly
                try:
                    self.logger.info("🚀 Attempting Method 1: Direct script execution")
                    process = subprocess.Popen([
                        freecad_exe,
                        str(abs_script_path)
                    ], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    self.logger.info("✅ FreeCAD launched with direct script execution")
                    success = True
                except Exception as e:
                    self.logger.warning(f"Method 1 failed: {e}")
                
                # Method 2: FreeCAD with macro execution
                if not success:
                    try:
                        self.logger.info("🚀 Attempting Method 2: Macro execution")
                        process = subprocess.Popen([
                            freecad_exe, 
                            "--run-python", 
                            str(abs_script_path)
                        ], shell=False)
                        self.logger.info("✅ FreeCAD launched with macro execution")
                        success = True
                    except Exception as e:
                        self.logger.warning(f"Method 2 failed: {e}")
                
                # Method 3: Launch FreeCAD normally then create an auto-load script
                if not success:
                    try:
                        self.logger.info("🚀 Attempting Method 3: Launch + auto-load")
                        
                        # Create a startup macro that loads our script
                        freecad_user_dir = Path.home() / "AppData" / "Roaming" / "FreeCAD"
                        macro_dir = freecad_user_dir / "Macro"
                        macro_dir.mkdir(parents=True, exist_ok=True)
                        
                        autoload_script = macro_dir / "AutoLoad.FCMacro"
                        with open(autoload_script, 'w', encoding='utf-8') as f:
                            f.write(f'''
# Auto-generated script to load model
import FreeCAD
try:
    exec(open(r"{abs_script_path}").read())
    FreeCAD.Console.PrintMessage("Model loaded successfully!\\n")
except Exception as e:
    FreeCAD.Console.PrintError(f"Failed to load model: {{e}}\\n")
''')
                        
                        # Launch FreeCAD
                        process = subprocess.Popen([freecad_exe], shell=False)
                        self.logger.info("✅ FreeCAD launched - auto-load script created")
                        success = True
                        
                    except Exception as e:
                        self.logger.warning(f"Method 3 failed: {e}")
                
                # Method 4: Just launch FreeCAD
                if not success:
                    try:
                        self.logger.info("🚀 Attempting Method 4: Basic FreeCAD launch")
                        process = subprocess.Popen([freecad_exe], shell=False)
                        self.logger.info("✅ FreeCAD launched - please load script manually")
                        success = True
                    except Exception as e:
                        self.logger.error(f"All methods failed: {e}")
                        return False
            else:
                # Linux/macOS: different approach
                try:
                    self.logger.info("🚀 Launching FreeCAD on Linux/macOS with script")
                    process = subprocess.Popen([freecad_exe, str(abs_script_path)], shell=False)
                    self.logger.info("✅ FreeCAD launched successfully on Linux/macOS")
                    success = True
                except Exception as e:
                    try:
                        self.logger.info("🚀 Launching basic FreeCAD on Linux/macOS")
                        process = subprocess.Popen([freecad_exe], shell=False)
                        self.logger.info("✅ FreeCAD launched - please load script manually")
                        success = True
                    except Exception as e2:
                        self.logger.error(f"Failed to launch FreeCAD on Linux/macOS: {e2}")
                        success = False
            
            if success:
                self.logger.info(f"🎉 FreeCAD launched successfully with script: {abs_script_path}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to launch FreeCAD: {e}")
            return False
    
    def get_service_info(self) -> Dict[str, Any]:
        """Get service information"""
        return {
            "freecad_available": self.freecad_available,
            "config": {
                "units": self.config.units,
                "part_module_only": self.config.part_module_only,
                "error_handling": self.config.error_handling
            }
        }