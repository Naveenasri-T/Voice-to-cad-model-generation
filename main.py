"""
Universal FreeCAD Model Generator - Clean, Flexible, No Hardcoded Values
Supports both 2D and 3D models with dynamic input handling
"""
import streamlit as st
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os
import subprocess
import re
from datetime import datetime
from pathlib import Path

# Enhanced imports with error handling
try:
    from utils.logging_config import get_logger
    from utils.exceptions import ExceptionContext, exception_handler, log_function_call
    from utils.code_cleaning import super_clean_ai_code, validate_python_syntax
    from config.settings import get_config
    ENHANCED_UTILS = True
except ImportError:
    ENHANCED_UTILS = False
    print("Running in basic mode - enhanced utilities not available")

from dotenv import load_dotenv
from groq import Groq

class UniversalModelGenerator:
    """Universal model generator for both 2D and 3D FreeCAD models"""
    
    def __init__(self):
        self.setup_environment()
        self.setup_logging()
        self.setup_configuration()
        self.setup_ai_client()
    
    def setup_environment(self):
        """Setup environment with proper path handling"""
        # Get current directory and find .env file
        current_dir = Path(__file__).parent.absolute()
        env_file = current_dir / ".env"
        
        # Try multiple possible locations for .env
        env_locations = [
            env_file,
            current_dir.parent / ".env",
            Path.cwd() / ".env"
        ]
        
        env_loaded = False
        for env_path in env_locations:
            if env_path.exists():
                load_dotenv(env_path)
                env_loaded = True
                if ENHANCED_UTILS:
                    get_logger("app").info(f"Environment loaded from: {env_path}")
                break
        
        if not env_loaded:
            st.error("⚠️ .env file not found! Please ensure GROQ_API_KEY is set.")
    
    def setup_logging(self):
        """Setup logging with fallback"""
        if ENHANCED_UTILS:
            self.logger = get_logger("app")
            self.ai_logger = get_logger("ai")
            self.error_logger = get_logger("error")
        else:
            import logging
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger("app")
            self.ai_logger = logging.getLogger("ai")
            self.error_logger = logging.getLogger("error")
    
    def setup_configuration(self):
        """Setup configuration with dynamic values"""
        if ENHANCED_UTILS:
            try:
                self.config = get_config()
                return
            except Exception as e:
                self.error_logger.error(f"Enhanced config failed: {e}")
        
        # Fallback configuration
        self.config = self.create_fallback_config()
        
        # Also store model parameters with defaults
        self.model = "llama-3.3-70b-versatile"
        self.temperature = 0.3
        self.max_tokens = 3000
    
    def create_fallback_config(self):
        """Create fallback configuration without hardcoded values"""
        import platform
        
        # Dynamic FreeCAD path detection
        freecad_paths = []
        if platform.system() == "Windows":
            freecad_paths = [
                r"C:\Program Files\FreeCAD 1.0\bin\FreeCAD.exe",
                r"C:\Program Files\FreeCAD 0.21\bin\FreeCAD.exe",
                r"C:\Program Files (x86)\FreeCAD 1.0\bin\FreeCAD.exe",
                r"C:\Program Files (x86)\FreeCAD 0.21\bin\FreeCAD.exe"
            ]
        elif platform.system() == "Linux":
            freecad_paths = [
                "/usr/bin/freecad",
                "/usr/local/bin/freecad",
                "/snap/bin/freecad"
            ]
        elif platform.system() == "Darwin":  # macOS
            freecad_paths = [
                "/Applications/FreeCAD.app/Contents/MacOS/FreeCAD",
                "/usr/local/bin/freecad"
            ]
        
        # Find existing FreeCAD installation
        freecad_path = None
        for path in freecad_paths:
            if Path(path).exists():
                freecad_path = path
                break
        
        class FallbackConfig:
            def __init__(self):
                self.freecad_executable = freecad_path
                self.groq_api_key = os.getenv("GROQ_API_KEY", "")
                self.groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
                self.groq_temperature = float(os.getenv("GROQ_TEMPERATURE", "0.3"))
                self.groq_max_tokens = int(os.getenv("GROQ_MAX_TOKENS", "3000"))
                
                # Dynamic directories
                base_dir = Path(__file__).parent.absolute()
                parent_dir = base_dir.parent
                self.generated_dir = base_dir / "generated"
                self.audio_dir = base_dir / "audio" 
                self.logs_dir = parent_dir / "voice-to-cad-logs"  # Logs outside project
                
                # Create directories
                for directory in [self.generated_dir, self.audio_dir, self.logs_dir]:
                    directory.mkdir(exist_ok=True)
                
        # Audio settings  
        self.audio_sample_rate = int(os.getenv("AUDIO_SAMPLE_RATE", "44100"))
        self.audio_duration = int(os.getenv("AUDIO_DURATION", "5"))
    
    def __getattr__(self, name):
        """Handle attribute access for compatibility"""
        if name == 'groq_api_key':
            return self.groq_api_key
        elif name == 'groq_model':
            return self.groq_model
        elif name == 'groq_temperature':
            return self.groq_temperature
        elif name == 'groq_max_tokens':
            return self.groq_max_tokens
        elif name == 'freecad_executable':
            return self.freecad_executable
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        
        def get_generated_filename(self, prefix="model"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return self.generated_dir / f"{prefix}_{timestamp}.py"
        
        def get_audio_filename(self, prefix="command"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return self.audio_dir / f"{prefix}_{timestamp}.wav"
        
        return FallbackConfig()
    
    def setup_ai_client(self):
        """Setup AI client with error handling"""
        # Handle different config structures
        if hasattr(self.config, 'groq'):
            api_key = self.config.groq.api_key
            model = self.config.groq.model
            temperature = self.config.groq.temperature
            max_tokens = self.config.groq.max_tokens
        else:
            api_key = getattr(self.config, 'groq_api_key', '')
            model = getattr(self.config, 'groq_model', 'llama-3.3-70b-versatile')
            temperature = getattr(self.config, 'groq_temperature', 0.3)
            max_tokens = getattr(self.config, 'groq_max_tokens', 3000)
        
        if not api_key:
            self.client = None
            st.error("🔑 GROQ_API_KEY not found! Please add it to your .env file.")
            st.info("Add this line to your .env file: `GROQ_API_KEY=your_key_here`")
            return
        
        try:
            self.client = Groq(api_key=api_key)
            # Store model parameters for use
            self.model = model
            self.temperature = temperature 
            self.max_tokens = max_tokens
            self.logger.info("Groq client initialized successfully")
        except Exception as e:
            self.client = None
            self.error_logger.error(f"Failed to initialize Groq client: {e}")
            st.error(f"❌ AI Client Error: {e}")
    
    @exception_handler("app", reraise=False) if ENHANCED_UTILS else lambda x: x
    def record_audio(self, duration=None):
        """Record audio with dynamic configuration"""
        
        if not duration:
            if hasattr(self.config, 'audio'):
                duration = self.config.audio.duration
            else:
                duration = getattr(self.config, 'audio_duration', 5)
        
        if hasattr(self.config, 'get_audio_filename'):
            filename = Path(self.config.get_audio_filename())  # Ensure it's a Path object
        else:
            # Fallback filename generation
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_dir = getattr(self.config, 'audio_dir', Path('.') / 'audio')
            Path(audio_dir).mkdir(exist_ok=True)
            filename = Path(audio_dir) / f"command_{timestamp}.wav"
        
        try:
            st.info("🎙 Recording... Speak now!")
            
            if hasattr(self.config, 'audio'):
                sample_rate = self.config.audio.sample_rate
            else:
                sample_rate = getattr(self.config, 'audio_sample_rate', 44100)
                
            audio = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype="int16"
            )
            sd.wait()
            
            wav.write(str(filename), sample_rate, audio)
            
            self.logger.info(f"Audio recorded: {filename}")
            st.success(f"✅ Recording complete: {filename.name}")
            
            return str(filename)
            
        except Exception as e:
            self.error_logger.error(f"Audio recording failed: {e}")
            st.error(f"❌ Recording error: {e}")
            return None
    
    def transcribe_audio(self, file_path):
        """Transcribe audio with error handling"""
        
        if not self.client:
            st.error("❌ AI client not available for transcription")
            return None
        
        if not Path(file_path).exists():
            st.error(f"❌ Audio file not found: {file_path}")
            return None
        
        try:
            with open(file_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-large-v3"
                )
            
            result = transcription.text.lower()
            self.ai_logger.info(f"Transcription successful: {result[:50]}...")
            return result
            
        except Exception as e:
            self.error_logger.error(f"Transcription failed: {e}")
            st.error(f"❌ Transcription error: {e}")
            return None
    
    def generate_universal_freecad_script(self, command_text, model_type="auto"):
        """Generate universal FreeCAD script for any model type"""
        
        if not self.client:
            st.error("❌ AI client not available")
            return None
        
        # Detect model type if auto
        if model_type == "auto":
            model_type = self.detect_model_type(command_text)
        
        # Create dynamic prompt based on input
        prompt = self.create_dynamic_prompt(command_text, model_type)
        
        # Add retry logic for better reliability
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.ai_logger.info(f"Generating {model_type} model for: {command_text} (attempt {attempt + 1})")
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    timeout=30  # Add timeout
                )
                
                raw_code = response.choices[0].message.content
                
                # Clean the code
                if ENHANCED_UTILS:
                    clean_code = super_clean_ai_code(raw_code)
                    is_valid, validation_message = validate_python_syntax(clean_code)
                    
                    if not is_valid:
                        self.error_logger.warning(f"Generated code syntax issues: {validation_message}")
                else:
                    clean_code = self.basic_clean_code(raw_code)
                
                self.ai_logger.info(f"Script generation successful: {len(clean_code)} characters")
                return clean_code
                
            except Exception as e:
                error_msg = str(e)
                self.error_logger.error(f"Script generation failed (attempt {attempt + 1}): {error_msg}")
                
                if attempt < max_retries - 1:
                    st.warning(f"⚠️ Connection issue (attempt {attempt + 1}), retrying...")
                    import time
                    time.sleep(2)  # Wait 2 seconds before retry
                else:
                    # Show more helpful error messages
                    if "connection" in error_msg.lower() or "timeout" in error_msg.lower():
                        st.error("🌐 **Connection Error**: Please check your internet connection and try again.")
                        st.info("💡 **Tip**: Wait a moment and click 'Generate Model' again.")
                    elif "rate" in error_msg.lower() or "limit" in error_msg.lower():
                        st.error("⏱️ **Rate Limit**: Too many requests. Please wait a minute and try again.")
                    elif "unauthorized" in error_msg.lower() or "401" in error_msg:
                        st.error("🔑 **API Key Error**: Please check your GROQ_API_KEY in the .env file.")
                    else:
                        st.error(f"❌ **Generation Error**: {error_msg}")
                    
                    return None
    
    def detect_model_type(self, command_text):
        """Automatically detect if user wants 2D or 3D model"""
        
        command_lower = command_text.lower()
        
        # 2D indicators
        if any(keyword in command_lower for keyword in [
            "2d", "flat", "sketch", "drawing", "plan", "layout", 
            "floor plan", "blueprint", "diagram", "outline"
        ]):
            return "2d"
        
        # 3D indicators  
        if any(keyword in command_lower for keyword in [
            "3d", "solid", "volume", "extrude", "house", "building",
            "bhk", "model", "object", "shape", "cube", "sphere", "cylinder"
        ]):
            return "3d"
        
        # Default to 3D if unclear
        return "3d"
    
    def create_dynamic_prompt(self, command_text, model_type):
        """Create dynamic prompt based on command and model type"""
        
        base_prompt = f"""
You are an expert FreeCAD Python script generator. Create a clean, executable FreeCAD script.

UNIVERSAL RULES:
- Always import: import FreeCAD, Part, Draft, FreeCADGui
- Create document: doc = FreeCAD.newDocument("Generated_Model")
- Use meaningful object names based on the command
- Position objects logically in 3D space
- End with: doc.recompute(), FreeCADGui.activeDocument().activeView().viewAxometric(), FreeCADGui.SendMsgToActiveView('ViewFit')

"""
        
        if model_type == "2d":
            prompt = base_prompt + """
2D MODEL SPECIFICATIONS:
- Use Draft.makeRectangle(), Draft.makeCircle(), Draft.makeLine(), Draft.makePolygon()
- Create sketches and 2D shapes
- Position in XY plane (Z=0)
- Use Draft.makeText() for labels if needed
- Create technical drawings and floor plans
- Use different colors: obj.ViewObject.ShapeColor = (R, G, B)

"""
        else:  # 3D
            prompt = base_prompt + """
3D MODEL SPECIFICATIONS:
- Use Part.makeBox(), Part.makeCylinder(), Part.makeSphere(), Part.makeCone()
- Create solid 3D objects
- Use Part.makeCompound() to combine objects
- Position objects using: obj.Placement.Base = FreeCAD.Vector(x, y, z)
- Create realistic proportions and dimensions
- For buildings/houses: include walls, doors, windows, rooms
- Use appropriate dimensions (meters/millimeters based on object scale)

"""
        
        # Add specific instructions based on command content
        if "house" in command_text.lower() or "bhk" in command_text.lower():
            prompt += """
HOUSE/BUILDING SPECIFIC:
- Create realistic room dimensions
- Include walls with proper thickness
- Add doors (2m height, 0.8m width typically)
- Add windows (1.5m width, 1m height typically)
- Position rooms logically
- Include foundation/floor base
- Create proper architectural layout

"""
        
        prompt += f"""
COMMAND: "{command_text}"

Generate clean, executable FreeCAD Python code that creates this {model_type.upper()} model.
"""
        
        return prompt
    
    def basic_clean_code(self, raw_code):
        """Basic code cleaning as fallback"""
        
        if not raw_code:
            return ""
        
        # Remove code block markers
        cleaned = re.sub(r"^```(?:python)?\s*", "", raw_code, flags=re.IGNORECASE | re.MULTILINE)
        cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.IGNORECASE | re.MULTILINE)
        cleaned = cleaned.replace("```", "")
        
        # Remove explanatory text patterns
        lines = cleaned.split('\n')
        code_lines = []
        
        for line in lines:
            # Skip lines that look like explanations
            if any(phrase in line.lower() for phrase in [
                "here's", "this is", "the following", "this script will",
                "the model includes", "note that", "however", "as you can see"
            ]):
                continue
            
            # Keep lines that look like code
            if (line.strip().startswith('#') or 
                'import' in line or 
                'FreeCAD' in line or
                'Part.' in line or
                'Draft.' in line or
                '=' in line or
                line.strip() == '' or
                'doc.' in line):
                code_lines.append(line)
        
        return '\n'.join(code_lines).strip()
    
    def save_and_run_script(self, script_content, command_text):
        """Save script and run in FreeCAD"""
        
        if not script_content:
            st.error("❌ No script content to save")
            return False
        
        try:
            # Generate filename based on command
            model_name = re.sub(r'[^\w\s-]', '', command_text)[:20]
            model_name = re.sub(r'\s+', '_', model_name.strip())
            
            if hasattr(self.config, 'get_generated_filename'):
                filename = Path(self.config.get_generated_filename(model_name))  # Ensure it's a Path object
            else:
                # Fallback filename generation
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                generated_dir = getattr(self.config, 'generated_dir', Path('.') / 'generated')
                Path(generated_dir).mkdir(exist_ok=True)
                filename = Path(generated_dir) / f"{model_name}_{timestamp}.py"
            
            # Save script
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            self.logger.info(f"Script saved: {filename}")
            st.success(f"✅ Script saved: {filename.name}")
            
            # Run in FreeCAD
            if hasattr(self.config, 'freecad'):
                freecad_path = self.config.freecad.executable_path
            else:
                freecad_path = getattr(self.config, 'freecad_executable', None)
                
            if freecad_path and Path(freecad_path).exists():
                subprocess.Popen([freecad_path, str(filename)])
                st.success("🚀 Model launched in FreeCAD!")
                return True
            else:
                st.error("❌ FreeCAD not found. Please install FreeCAD or update the path.")
                st.info(f"Looking for FreeCAD at: {freecad_path}")
                return False
                
        except Exception as e:
            self.error_logger.error(f"Save/run failed: {e}")
            st.error(f"❌ Error: {e}")
            return False

def main():
    """Main Streamlit application"""
    
    # Initialize generator
    generator = UniversalModelGenerator()
    
    # UI
    st.title("🎯 Universal FreeCAD Model Generator")
    st.subheader("Generate Any 2D/3D Model with Voice or Text")
    
    # Configuration status
    with st.expander("⚙️ System Status"):
        if generator.client:
            st.success("✅ AI Client: Connected")
            
            # Test API connection button
            if st.button("🔍 Test API Connection"):
                with st.spinner("Testing connection..."):
                    try:
                        test_response = generator.client.chat.completions.create(
                            model=generator.model,
                            messages=[{"role": "user", "content": "Test"}],
                            temperature=0.1,
                            max_tokens=10,
                            timeout=10
                        )
                        st.success("🌐 **API Connection**: ✅ Working perfectly!")
                    except Exception as e:
                        st.error(f"🌐 **API Connection**: ❌ {str(e)}")
                        st.info("💡 **Suggestions**: Check internet connection, wait a moment, or verify API key")
        else:
            st.error("❌ AI Client: Not Connected")
            
        # Handle different config structures for FreeCAD
        if hasattr(generator.config, 'freecad'):
            freecad_path = generator.config.freecad.executable_path
        else:
            freecad_path = getattr(generator.config, 'freecad_executable', None)
            
        if freecad_path and Path(freecad_path).exists():
            st.success(f"✅ FreeCAD: {Path(freecad_path).name}")
        else:
            st.error("❌ FreeCAD: Not Found")
            
        # Handle different config structures for directories
        if hasattr(generator.config, 'paths'):
            generated_dir = generator.config.paths.generated_dir
        else:
            generated_dir = getattr(generator.config, 'generated_dir', 'generated')
        
        st.info(f"📁 Generated Files: {generated_dir}")
    
    # Model type selection
    model_type = st.selectbox(
        "🎨 Model Type",
        ["auto", "3d", "2d"],
        format_func=lambda x: {
            "auto": "Auto Detect",
            "3d": "📦 3D Model", 
            "2d": "📐 2D Drawing"
        }[x]
    )
    
    # Voice input
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🎙 Record Command", use_container_width=True):
            audio_file = generator.record_audio()
            if audio_file:
                command_text = generator.transcribe_audio(audio_file)
                if command_text:
                    st.success(f"🗣 Command: *{command_text}*")
                    st.session_state["voice_command"] = command_text
    
    # Text input
    with col2:
        text_command = st.text_input(
            "💬 Or Type Command:",
            placeholder="e.g., Create a 2BHK house, Draw a gear, Make a water bottle"
        )
    
    # Generate button
    if st.button("🏗 Generate Model", type="primary", use_container_width=True):
        
        command = text_command or st.session_state.get("voice_command", "")
        
        if not command:
            st.error("❌ Please provide a command (voice or text)")
            return
        
        if not generator.client:
            st.error("❌ AI client not available. Check your GROQ_API_KEY.")
            return
        
        with st.spinner(f"🤖 Generating {model_type.upper()} model..."):
            script = generator.generate_universal_freecad_script(command, model_type)
        
        if script:
            # Show preview
            with st.expander("📄 Generated Script Preview"):
                st.code(script, language="python")
            
            # Save and run
            success = generator.save_and_run_script(script, command)
            
            if success:
                st.balloons()
                st.success("🎉 Model generated successfully!")
        else:
            st.error("❌ Failed to generate model")
    
    # Examples
    with st.expander("💡 Example Commands"):
        st.write("**🏠 Architecture:**")
        st.write("• Create a 3BHK house with parking")
        st.write("• Design a 2D floor plan for office")
        st.write("• Generate a modern villa")
        
        st.write("**🔧 Mechanical:**")
        st.write("• Create a mechanical gear")
        st.write("• Design a water bottle")
        st.write("• Make a cylindrical tank")
        
        st.write("**📐 2D Drawings:**")
        st.write("• Draw a technical blueprint")
        st.write("• Create a 2D logo design")
        st.write("• Make a floor plan layout")

if __name__ == "__main__":
    main()