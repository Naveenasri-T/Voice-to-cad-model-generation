"""
Configuration settings for Voice-to-CAD Model Generation Application
"""
import os
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv is not available, continue without it
    pass

@dataclass
class AudioConfig:
    """Audio recording configuration"""
    sample_rate: int = 44100
    channels: int = 1
    duration: int = 5
    dtype: str = "int16"
    format: str = "WAV"
    bit_depth: int = 16

@dataclass
class GroqConfig:
    """Groq AI configuration"""
    api_key: str = ""
    model: str = "llama-3.3-70b-versatile"
    temperature: float = 0.3
    max_tokens: int = 2048
    timeout: int = 60

@dataclass
class AIConfig:
    """AI service configuration"""
    api_key: Optional[str] = None
    model_name: str = 'llama-3.3-70b-versatile'
    max_tokens: int = 8000
    temperature: float = 0.1
    timeout: int = 30
    groq: GroqConfig = field(default_factory=GroqConfig)

@dataclass
class FreeCADConfig:
    """FreeCAD configuration"""
    installation_path: Optional[str] = None
    alternative_paths: List[str] = field(default_factory=lambda: [
        r"C:\Program Files\FreeCAD 0.21\bin",
        r"C:\Program Files\FreeCAD 0.20\bin",
        r"C:\Program Files (x86)\FreeCAD 0.21\bin",
        r"C:\Program Files (x86)\FreeCAD 0.20\bin",
        "/usr/lib/freecad-python3/lib/",
        "/usr/lib/freecad/lib/",
        "/Applications/FreeCAD.app/Contents/Resources/lib/"
    ])
    python_path: Optional[str] = None
    working_directory: str = "generated"
    default_document_name: str = "VoiceToCAD_Model"

@dataclass
class UIConfig:
    """UI configuration for Streamlit"""
    title: str = "🏗️ Voice to CAD Model Generator"
    description: str = "Professional CAD Model Generation from Voice Commands"
    theme_color: str = "#1E88E5"
    success_color: str = "#4CAF50"
    error_color: str = "#F44336"
    warning_color: str = "#FF9800"
    
    # Layout settings
    sidebar_width: int = 300
    main_content_width: str = "wide"
    
    # File upload settings
    max_file_size_mb: int = 10
    allowed_audio_formats: List[str] = field(default_factory=lambda: [
        'wav', 'mp3', 'flac', 'ogg', 'm4a'
    ])

@dataclass
class FileConfig:
    """File handling configuration"""
    base_directory: str = "."
    audio_directory: str = "audio"
    generated_directory: str = "generated"
    logs_directory: str = "logs"
    tests_directory: str = "tests"
    
    # File naming
    audio_filename_template: str = "command_{timestamp}.wav"
    generated_filename_template: str = "{description}_{timestamp}.py"
    max_filename_length: int = 100
    encoding: str = "utf-8"
    
    # File permissions
    create_directories: bool = True
    overwrite_existing: bool = True
    backup_existing: bool = False

@dataclass
class Config:
    """Main configuration class"""
    audio: AudioConfig = field(default_factory=AudioConfig)
    ai: AIConfig = field(default_factory=AIConfig)
    freecad: FreeCADConfig = field(default_factory=FreeCADConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    file: FileConfig = field(default_factory=FileConfig)
    
    # Environment settings
    debug: bool = False
    log_level: str = "INFO"
    environment: str = "production"
    
    def create_directories(self) -> None:
        """Create all required directories"""
        if not self.file.create_directories:
            return
            
        directories = [
            self.file.audio_directory,
            self.file.generated_directory,
            self.file.logs_directory,
        ]
        
        for directory in directories:
            path = Path(directory)
            path.mkdir(parents=True, exist_ok=True)
    
    def get_directories(self) -> Dict[str, Path]:
        """Get directories as Path objects"""
        return {
            'audio': Path(self.file.audio_directory),
            'generated': Path(self.file.generated_directory),
            'logs': Path(self.file.logs_directory),
            'tests': Path(self.file.tests_directory)
        }

class ConfigurationManager:
    """Configuration manager for the application"""
    
    def __init__(self):
        self._config = None
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration with environment variable overrides"""
        config = Config()
        
        # Override with environment variables
        config.ai.groq.api_key = os.getenv('GROQ_API_KEY', '')
        config.debug = os.getenv('DEBUG', 'false').lower() == 'true'
        config.log_level = os.getenv('LOG_LEVEL', 'INFO')
        config.environment = os.getenv('ENVIRONMENT', 'production')
        
        # Override FreeCAD path if provided
        freecad_path = os.getenv('FREECAD_PATH')
        if freecad_path:
            config.freecad.installation_path = freecad_path
        
        self._config = config
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        """Ensure all required directories exist"""
        if not self._config.file.create_directories:
            return
            
        directories = [
            self._config.file.audio_directory,
            self._config.file.generated_directory,
            self._config.file.logs_directory,
        ]
        
        for directory in directories:
            path = Path(directory)
            path.mkdir(parents=True, exist_ok=True)
    
    @property
    def config(self) -> Config:
        """Get the current configuration"""
        return self._config
    
    def reload(self) -> None:
        """Reload configuration from environment"""
        self._load_config()
    
    def update_groq_api_key(self, api_key: str) -> None:
        """Update Groq API key"""
        self._config.ai.groq.api_key = api_key
    
    def get_freecad_path(self) -> Optional[str]:
        """Get FreeCAD installation path"""
        if self._config.freecad.installation_path:
            if Path(self._config.freecad.installation_path).exists():
                return self._config.freecad.installation_path
        
        # Try alternative paths
        for path in self._config.freecad.alternative_paths:
            if Path(path).exists():
                self._config.freecad.installation_path = path
                return path
        
        return None
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validate current configuration"""
        issues = []
        warnings = []
        
        # Check Groq API key
        if not self._config.ai.groq.api_key:
            issues.append("Groq API key is not configured")
        
        # Check FreeCAD path
        freecad_path = self.get_freecad_path()
        if not freecad_path:
            warnings.append("FreeCAD installation not found in standard locations")
        
        # Check directories
        for directory in [self._config.file.audio_directory, 
                         self._config.file.generated_directory]:
            if not Path(directory).exists():
                warnings.append(f"Directory does not exist: {directory}")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings,
            'freecad_path': freecad_path
        }

# Global configuration manager instance
_config_manager = ConfigurationManager()

def get_config() -> Config:
    """Get the global configuration"""
    return _config_manager.config

def get_config_manager() -> ConfigurationManager:
    """Get the global configuration manager"""
    return _config_manager

# Export main config object
config = get_config()