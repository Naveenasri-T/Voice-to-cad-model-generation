"""
FreeCAD Code Cleaner Utility
Cleans existing generated files to remove deprecated FreeCAD patterns
"""

import re
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def fix_techdraw_issues(code: str) -> str:
    """Fix TechDraw related issues in generated code"""
    
    # Remove problematic TechDraw patterns that cause "argument 1 must be TechDraw.DrawView" errors
    # These patterns try to add objects directly to TechDraw pages incorrectly
    
    # Remove incorrect page.addView() calls
    code = re.sub(r'view\d+\s*=\s*page\.addView\([^)]+\)\n?', '', code)
    
    # Remove problematic TechDraw view creation patterns
    code = re.sub(r'view\d+\.Rotation\s*=.*?\n', '', code)
    code = re.sub(r'view\d+\.Scale\s*=.*?\n', '', code)
    
    # Remove entire TechDraw sections that are problematic
    # Look for TechDraw page creation and remove the whole problematic section
    techdraw_pattern = r'# Create the technical drawing.*?(?=# Recompute and fit the view|doc\.recompute\(\)|$)'
    code = re.sub(techdraw_pattern, '# TechDraw section removed due to compatibility issues\n', code, flags=re.DOTALL)
    
    # Also handle variations
    techdraw_pattern2 = r'page\s*=\s*doc\.addObject\("TechDraw::DrawPage".*?(?=# Recompute|doc\.recompute\(\)|$)'
    code = re.sub(techdraw_pattern2, '# TechDraw section removed due to compatibility issues\n', code, flags=re.DOTALL)
    
    # Remove standalone TechDraw imports if no longer needed
    lines = code.split('\n')
    has_techdraw_usage = any('TechDraw' in line and not line.strip().startswith('#') and 'import' not in line for line in lines)
    
    if not has_techdraw_usage:
        code = re.sub(r'import TechDraw.*?\n', '', code)
        code = re.sub(r'from TechDraw import.*?\n', '', code)
    
    return code

def clean_freecad_file(file_path: str) -> bool:
    """Clean a single FreeCAD Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        original_code = code
        
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
        
        # Fix TechDraw issues - remove problematic TechDraw code
        code = fix_techdraw_issues(code)
        
        # Remove double imports
        if code.count('import FreeCAD') > 1:
            lines = code.split('\n')
            seen_imports = set()
            cleaned_lines = []
            
            for line in lines:
                if line.strip().startswith('import FreeCAD') or line.strip().startswith('import Part'):
                    if line.strip() not in seen_imports:
                        seen_imports.add(line.strip())
                        cleaned_lines.append(line)
                else:
                    cleaned_lines.append(line)
            
            code = '\n'.join(cleaned_lines)
        
        # Remove double document creation
        if code.count('newDocument') > 1:
            lines = code.split('\n')
            cleaned_lines = []
            found_newdoc = False
            
            for line in lines:
                if 'newDocument' in line:
                    if not found_newdoc:
                        cleaned_lines.append(line)
                        found_newdoc = True
                else:
                    cleaned_lines.append(line)
            
            code = '\n'.join(cleaned_lines)
        
        # Clean up multiple empty lines
        code = re.sub(r'\n\s*\n\s*\n', '\n\n', code)
        
        # Only write if changes were made
        if code != original_code:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
            logger.info(f"Cleaned file: {file_path}")
            return True
        else:
            logger.info(f"File already clean: {file_path}")
            return False
            
    except Exception as e:
        logger.error(f"Failed to clean file {file_path}: {e}")
        return False

def clean_all_generated_files(generated_dir: str = "generated") -> dict:
    """Clean all Python files in the generated directory"""
    results = {
        "cleaned": [],
        "already_clean": [],
        "errors": []
    }
    
    generated_path = Path(generated_dir)
    
    if not generated_path.exists():
        logger.warning(f"Generated directory not found: {generated_dir}")
        return results
    
    # Find all Python files
    python_files = list(generated_path.glob("*.py"))
    
    logger.info(f"Found {len(python_files)} Python files to check")
    
    for file_path in python_files:
        try:
            if clean_freecad_file(str(file_path)):
                results["cleaned"].append(str(file_path))
            else:
                results["already_clean"].append(str(file_path))
        except Exception as e:
            results["errors"].append(f"{file_path}: {e}")
            logger.error(f"Error processing {file_path}: {e}")
    
    logger.info(f"Cleaning complete: {len(results['cleaned'])} cleaned, {len(results['already_clean'])} already clean, {len(results['errors'])} errors")
    
    return results

if __name__ == "__main__":
    # Run as standalone script
    logging.basicConfig(level=logging.INFO)
    results = clean_all_generated_files()
    
    print(f"\n=== FreeCAD File Cleaning Results ===")
    print(f"Files cleaned: {len(results['cleaned'])}")
    print(f"Files already clean: {len(results['already_clean'])}")
    print(f"Errors: {len(results['errors'])}")
    
    if results['cleaned']:
        print(f"\nCleaned files:")
        for file in results['cleaned']:
            print(f"  - {file}")
    
    if results['errors']:
        print(f"\nErrors:")
        for error in results['errors']:
            print(f"  - {error}")