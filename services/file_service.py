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
        
    def save_generated_code(self, code: str, command: str) -> Path:
        """Save generated FreeCAD code to file with automatic cleaning.

        Returns the saved file as a Path object so callers can use .name, .parent, etc.
        On failure, returns Path('') and logs the error.
        """
        try:
            # Clean the code before saving
            cleaned_code = self._clean_freecad_code(code)

            # Create safe filename from command
            safe_name = self._create_safe_filename(command)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_name}_{timestamp}.py"

            # Ensure filename length limit
            if len(filename) > self.config.max_filename_length:
                filename = filename[:self.config.max_filename_length - 3] + ".py"

            filepath = self.directories['generated'] / filename

            # Ensure parent directory exists
            filepath.parent.mkdir(parents=True, exist_ok=True)

            # Save with proper encoding
            with open(filepath, 'w', encoding=self.config.encoding) as f:
                f.write(cleaned_code)

            self.logger.info(f"Saved generated code: {filepath}")
            return filepath

        except Exception as e:
            self.logger.error(f"Failed to save code: {e}")
            return Path('')
    
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
            

            # ── ViewObject merge fixer ──────────────────────────────────────
            # Only fixes ACTUALLY merged tokens (no dot between ViewObject and var name).
            # Examples of bad tokens we fix:
            #   dim1.ViewObjectdim1.ViewObject  → dim1.ViewObject
            #   obj.ViewObject   obj.ViewObject.LineWidth  → split across lines
            # We do NOT touch valid lines like:
            #   d.ViewObject.FontSize = 260   ← leave alone!

            # Pattern 1 (safe): same-variable merge  dim1.ViewObjectdim1.ViewObject
            code = re.sub(r'(\w+)\.ViewObject\1\.ViewObject', r'\1.ViewObject', code)

            # Pattern 2 (safe, line-by-line): generic cross-variable merge
            # Matches .ViewObject<WORD_NO_DOT>.ViewObject → .ViewObject
            # Key: \w+ means NO dot in the middle, so .ViewObject.FontSize is NOT matched
            code = re.sub(r'\.ViewObject([A-Za-z_]\w*)\.ViewObject', r'.ViewObject', code)

            # Pattern 3 (safe): missing newline before Draft assignment
            code = re.sub(r'(\w+)\.ViewObject(\w+)\s*=\s*Draft', r'\1.ViewObject\n\2 = Draft', code)

            # Pattern 4 (safe, line-by-line only): whitespace-gap merger
            # ONLY matches TWO+ spaces between ViewObject and another var (not a dot)
            # Running line-by-line prevents cross-line corruption
            lines = code.split('\n')
            fixed_lines = []
            for line in lines:
                # Only touch lines that have a bare .ViewObject followed by 2+ spaces then a word
                # Example: "grid_line.ViewObject    grid_line.ViewObject.LineWidth"
                ws_match = re.search(r'(\w+)\.ViewObject\s{2,}(\w+)\.ViewObject', line)
                if ws_match:
                    m = re.match(r'^(\s*)(\w+)\.ViewObject\s{2,}(\w+)\.ViewObject(.*)$', line)
                    if m:
                        indent = m.group(1)
                        var1   = m.group(2)
                        var2   = m.group(3)
                        rest   = m.group(4)
                        fixed_lines.append(f'{indent}{var1}.ViewObject')
                        line = f'{indent}{var2}.ViewObject{rest}'
                fixed_lines.append(line)
            code = '\n'.join(fixed_lines)

            
            # ===== FIX: Wrap problematic LineStyle assignments in try-except =====
            lines = code.split('\n')
            fixed_lines = []
            i = 0
            while i < len(lines):
                line = lines[i]
                # Check if this line sets LineStyle
                if '.ViewObject.LineStyle' in line:
                    # Get the indentation
                    indent = len(line) - len(line.lstrip())
                    indent_str = ' ' * indent
                    # Wrap in try-except
                    fixed_lines.append(f'{indent_str}try:')
                    fixed_lines.append(f'{indent_str}    {line.strip()}')
                    fixed_lines.append(f'{indent_str}except AttributeError:')
                    fixed_lines.append(f'{indent_str}    pass  # LineStyle not supported')
                else:
                    fixed_lines.append(line)
                i += 1
            code = '\n'.join(fixed_lines)
            
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