"""
Professional File Service
Handles file operations for CAD model generation
"""

import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
import re

from config.settings import FileConfig


class FileService:
    """Professional File Management Service"""
    
    def __init__(self, file_config: FileConfig, directories: Dict[str, Path]):
        self.config = file_config
        self.directories = directories
        self.logger = logging.getLogger(__name__)
        
    def save_generated_code(self, code: str, command: str) -> str:
        """Save generated FreeCAD code to file with automatic cleaning"""
        try:
            # Clean the code before saving
            cleaned_code = self._clean_freecad_code(code)
            
            # Create safe filename from command
            safe_name = self._create_safe_filename(command)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_name}_{timestamp}.py"
            
            # Ensure filename length limit
            if len(filename) > self.config.max_filename_length:
                filename = filename[:self.config.max_filename_length-3] + ".py"
            
            filepath = self.directories['generated'] / filename
            
            # Save with proper encoding
            with open(filepath, 'w', encoding=self.config.encoding) as f:
                f.write(cleaned_code)
            
            # CRITICAL: Re-read and apply post-save fixes for patterns that slip through
            with open(filepath, 'r', encoding=self.config.encoding) as f:
                saved_code = f.read()
            
            # Apply aggressive ViewObject fixes
            saved_code = re.sub(r'(\s+)(\w+)\.ViewObject\s{2,}(\w+)\.ViewObject\.', r'\1\2.ViewObject\n\1\3.ViewObject.', saved_code)
            
            # Re-save if fixes were applied
            if saved_code != cleaned_code:
                with open(filepath, 'w', encoding=self.config.encoding) as f:
                    f.write(saved_code)
                self.logger.info(f"Applied post-save fixes to: {filepath}")
            
            self.logger.info(f"Saved generated code: {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Failed to save code: {e}")
            return ""
    
    def _clean_freecad_code(self, code: str) -> str:
        """Clean FreeCAD code to remove deprecated patterns"""
        try:
            # Remove problematic deprecated patterns
            code = re.sub(r'FreeCAD\.Units\.setPreferredUnitSystem\(.*?\)\n?', '', code)
            code = re.sub(r'Units\.setPreferredUnitSystem\(.*?\)\n?', '', code)
            code = re.sub(r'import Units.*?\n', '', code)
            code = re.sub(r'from Units import.*?\n', '', code)
            code = re.sub(r'\.ActiveMaterial.*?\n', '', code)
            code = re.sub(r'\.DiffuseColor\s*=.*?\n', '', code)
            code = re.sub(r'\.Material\s*=.*?\n', '', code)
            code = re.sub(r'App\.setActiveDocument\(.*?\)\n?', '', code)
            code = re.sub(r'FreeCADGui\.showMainWindow\(\)\n?', '', code)
            code = re.sub(r'FreeCADGui\.updateGui\(\)\n?', '', code)
            
            # Fix incomplete FreeCAD statements (edge case from cleaning)
            code = re.sub(r'FreeCAD\.\s*\n', '', code)
            code = re.sub(r'FreeCAD\.\s*$', '', code, flags=re.MULTILINE)
            
            # Remove orphaned comment lines
            code = re.sub(r'# Set the unit system to millimeters\s*\n', '', code)
            code = re.sub(r'# Set unit system.*?\n', '', code)
            
            # Remove duplicate imports to prevent "Empty module name" errors
            lines = code.split('\n')
            seen_imports = set()
            deduplicated_lines = []
            
            for line in lines:
                stripped = line.strip()
                
                # Handle import statements to remove duplicates
                if stripped.startswith('import ') or stripped.startswith('from '):
                    # Normalize the import statement for comparison
                    normalized_import = stripped.split('#')[0].strip()  # Remove inline comments
                    if normalized_import and normalized_import not in seen_imports:
                        seen_imports.add(normalized_import)
                        deduplicated_lines.append(line)
                    # Skip duplicate imports
                else:
                    deduplicated_lines.append(line)
            
            code = '\n'.join(deduplicated_lines)
            
            # Remove empty import lines that cause "Empty module name" errors
            code = re.sub(r'^import\s*$', '', code, flags=re.MULTILINE)
            code = re.sub(r'^from\s*$', '', code, flags=re.MULTILINE)
            code = re.sub(r'^from\s+import\s*$', '', code, flags=re.MULTILINE)
            
            # Fix ViewObject attribute errors (dim1.ViewObjectdim1.ViewObject)
            code = re.sub(r'(\w+)\.ViewObject(\w+)\.ViewObject\.', r'\1.ViewObject.', code)
            
            # Fix missing newlines after ViewObject
            code = re.sub(r'(\w+)\.ViewObject(\w+)\s*=\s*Draft', r'\1.ViewObject\n\2 = Draft', code)
            
            # Fix ViewObject concatenation without proper spacing (e.g., "ViewObject    grid_line.ViewObject")
            # Pattern 1: variable.ViewObject    variable.ViewObject.property = value
            code = re.sub(r'(\w+)\.ViewObject\s{2,}(\w+)\.ViewObject\.', r'\1.ViewObject.\n    \2.ViewObject.', code)
            
            # Pattern 2: More aggressive - any ViewObject followed by multiple spaces then another variable
            code = re.sub(r'\.ViewObject(\s{2,})(\w+)\.ViewObject', r'.ViewObject\n    \2.ViewObject', code)
            
            # Clean up multiple empty lines
            code = re.sub(r'\n\s*\n\s*\n', '\n\n', code)
            
            # Remove empty comment lines left after cleaning
            lines = code.split('\n')
            cleaned_lines = []
            for line in lines:
                stripped = line.strip()
                if stripped == "# Set the unit system to millimeters" or stripped == "#" or stripped == "FreeCAD.":
                    continue
                cleaned_lines.append(line)
            
            return '\n'.join(cleaned_lines)
            
        except Exception as e:
            self.logger.warning(f"Failed to clean code: {e}")
            return code
    
    def _create_safe_filename(self, command: str) -> str:
        """Create safe filename from command"""
        # Remove special characters and limit length
        safe_name = re.sub(r'[^\w\s-]', '', command)
        safe_name = re.sub(r'[-\s]+', '_', safe_name)
        return safe_name[:30].strip('_')
    
    def get_generated_files(self) -> List[Dict[str, Any]]:
        """Get list of generated files"""
        try:
            files = []
            generated_dir = self.directories['generated']
            
            for filepath in generated_dir.glob("*.py"):
                stat = filepath.stat()
                files.append({
                    "name": filepath.name,
                    "path": str(filepath),
                    "size": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_ctime),
                    "modified": datetime.fromtimestamp(stat.st_mtime)
                })
            
            return sorted(files, key=lambda x: x['modified'], reverse=True)
            
        except Exception as e:
            self.logger.error(f"Failed to get generated files: {e}")
            return []