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
        """Save generated FreeCAD code to file"""
        try:
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
                f.write(code)
            
            self.logger.info(f"Saved generated code: {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Failed to save code: {e}")
            return ""
    
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