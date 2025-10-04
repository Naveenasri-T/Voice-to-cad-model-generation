"""
Configuration management for Voice-to-CAD application
"""
import os
from dataclasses import dataclass
from typing import List, Optional
from dotenv import load_dotenv

@dataclass
class FreeCADConfig:
    """FreeCAD configuration"""
    executable_path: str
    alternative_paths: List[str]
    default_document_name: str = "VoiceToCAD_Model"
    
@dataclass
class GroqConfig:
    """Groq AI configuration"""
    api_key: str
    model: str = "llama-3.3-70b-versatile"
    temperature: float = 0.3
    max_tokens: int = 2048

@dataclass
class AudioConfig:
    """Audio recording configuration"""
    sample_rate: int = 44100
    channels: int = 1
    duration: int = 5
    dtype: str = "int16"

@dataclass
class PathConfig:
    """Application paths"""
    root_dir: str
    audio_dir: str
    generated_dir: str
    logs_dir: str
    tests_dir: str
    models_dir: str

class Config:
    """Enhanced main configuration class with robust env loading"""
    
    def __init__(self, env_file=".env"):
        self._load_environment_variables()
        self.load_configuration()
    
    def _load_environment_variables(self):
        """Enhanced environment variable loading with multiple path checking"""
        from pathlib import Path
        
        # Get current directory and possible .env locations
        current_dir = Path(__file__).parent.absolute()
        
        env_locations = [
            current_dir / ".env",  # config/.env
            current_dir.parent / ".env",  # project root/.env
            Path.cwd() / ".env",  # current working directory/.env
        ]
        
        env_loaded = False
        loaded_from = None
        
        for env_path in env_locations:
            if env_path.exists():
                load_dotenv(env_path, override=True)
                env_loaded = True
                loaded_from = env_path
                break
        
        if env_loaded:
            print(f"✅ Environment loaded from: {loaded_from}")
        else:
            print("⚠️ No .env file found in expected locations:")
            for location in env_locations:
                print(f"  - {location}")
    
    def validate_api_key(self):
        """Validate that API key is properly loaded"""
        api_key = os.getenv("GROQ_API_KEY", "")
        
        if not api_key:
            return False, "GROQ_API_KEY not found or empty"
        
        if len(api_key) < 10:
            return False, "GROQ_API_KEY appears to be invalid (too short)"
        
        return True, f"API key loaded successfully (length: {len(api_key)})"
    
    def load_configuration(self):
        """Load all configuration from environment and defaults"""
        
        # Root directory
        root_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(root_dir)  # Go up from config dir
        
        # Paths
        parent_dir = os.path.dirname(root_dir)  # Go up to parent directory
        self.paths = PathConfig(
            root_dir=root_dir,
            audio_dir=os.path.join(root_dir, "audio"),
            generated_dir=os.path.join(root_dir, "generated"),
            logs_dir=os.path.join(parent_dir, "voice-to-cad-logs"),  # Logs outside project
            tests_dir=os.path.join(root_dir, "tests"),
            models_dir=os.path.join(root_dir, "models")
        )
        
        # Groq configuration
        self.groq = GroqConfig(
            api_key=os.getenv("GROQ_API_KEY", ""),
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            temperature=float(os.getenv("GROQ_TEMPERATURE", "0.3")),
            max_tokens=int(os.getenv("GROQ_MAX_TOKENS", "2048"))
        )
        
        # FreeCAD configuration
        self.freecad = FreeCADConfig(
            executable_path=os.getenv(
                "FREECAD_PATH", 
                r"C:\Program Files\FreeCAD 1.0\bin\FreeCAD.exe"
            ),
            alternative_paths=[
                r"C:\Program Files\FreeCAD 0.21\bin\FreeCAD.exe",
                r"C:\Program Files (x86)\FreeCAD 1.0\bin\FreeCAD.exe",
                r"C:\Program Files (x86)\FreeCAD 0.21\bin\FreeCAD.exe"
            ]
        )
        
        # Audio configuration
        self.audio = AudioConfig(
            sample_rate=int(os.getenv("AUDIO_SAMPLE_RATE", "44100")),
            channels=int(os.getenv("AUDIO_CHANNELS", "1")),
            duration=int(os.getenv("AUDIO_DURATION", "5")),
            dtype=os.getenv("AUDIO_DTYPE", "int16")
        )
    
    def validate_configuration(self):
        """Validate configuration settings"""
        errors = []
        
        # Check Groq API key with enhanced validation
        api_key_valid, api_key_message = self.validate_api_key()
        if not api_key_valid:
            errors.append(api_key_message)
        else:
            print(api_key_message)
        
        # Check FreeCAD path
        if not os.path.exists(self.freecad.executable_path):
            # Try alternative paths
            found_alternative = False
            for alt_path in self.freecad.alternative_paths:
                if os.path.exists(alt_path):
                    self.freecad.executable_path = alt_path
                    found_alternative = True
                    break
            
            if not found_alternative:
                errors.append("FreeCAD executable not found")
        
        # Create directories if they don't exist
        for dir_path in [
            self.paths.audio_dir,
            self.paths.generated_dir,
            self.paths.logs_dir,
            self.paths.tests_dir,
            self.paths.models_dir
        ]:
            os.makedirs(dir_path, exist_ok=True)
        
        return errors
    
    def get_audio_filename(self, prefix="command"):
        """Get audio filename with timestamp"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.paths.audio_dir, f"{prefix}_{timestamp}.wav")
    
    def get_generated_filename(self, suffix="model"):
        """Get generated filename with timestamp"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.paths.generated_dir, f"{suffix}_{timestamp}.py")

# Global configuration instance
config = Config()

def get_config():
    """Get global configuration instance"""
    return config