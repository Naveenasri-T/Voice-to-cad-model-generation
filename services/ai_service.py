import logging
import json
from typing import Optional, Dict, Any, List
from pathlib import Path
import re

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from google.cloud import speech
    GOOGLE_SPEECH_AVAILABLE = True
except ImportError:
    GOOGLE_SPEECH_AVAILABLE = False

from config.settings import AIConfig

class AIService:
    def __init__(self, ai_config: AIConfig):
        self.config = ai_config
        self.logger = logging.getLogger(__name__)
        self.client = None
        self.provider = ai_config.provider
        self._initialize_client()
        self.construction_standards = self._load_construction_standards()
        
    def _initialize_client(self) -> None:
        if self.provider == 'gemini':
            self._initialize_gemini_client()
        elif self.provider == 'groq':
            self._initialize_groq_client()
        else:
            self.logger.error(f"Unknown AI provider: {self.provider}")
    
    def _load_construction_standards(self) -> Dict[str, Any]:
        """Load construction standards from JSON file"""
        try:
            standards_path = Path(__file__).parent.parent / "config" / "construction_standards.json"
            if standards_path.exists():
                with open(standards_path, 'r') as f:
                    return json.load(f)
            else:
                self.logger.warning("Construction standards file not found, using defaults")
                return {}
        except Exception as e:
            self.logger.error(f"Error loading construction standards: {e}")
            return {}
    
    def _initialize_gemini_client(self) -> None:
        if not GEMINI_AVAILABLE:
            self.logger.error("Google Generative AI library not available - AI functionality disabled")
            return
            
        if not self.config.gemini.api_key:
            self.logger.warning("Gemini API key not configured - limited functionality")
            return
            
        try:
            genai.configure(api_key=self.config.gemini.api_key)
            self.client = genai.GenerativeModel(self.config.gemini.model)
            self.logger.info("Gemini AI client initialized successfully")
            
            # Test connection
            self._test_gemini_connection()
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini client: {e}")
            self.client = None
    
    def _initialize_groq_client(self) -> None:
        if not GROQ_AVAILABLE:
            self.logger.error("Groq library not available - AI functionality disabled")
            return
            
        if not self.config.groq.api_key:
            self.logger.warning("Groq API key not configured - limited functionality")
            return
            
        try:
            self.client = Groq(api_key=self.config.groq.api_key)
            self.logger.info("Groq AI client initialized successfully")
            
            # Test connection
            self._test_groq_connection()
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Groq client: {e}")
            self.client = None
    
    def _test_gemini_connection(self) -> None:
        """Test Gemini service connection"""
        try:
            response = self.client.generate_content("Test connection")
            if response and response.text:
                self.logger.info("Gemini connection test successful")
            else:
                self.logger.warning("Gemini connection test returned empty response")
        except Exception as e:
            self.logger.warning(f"Gemini connection test failed: {e}")
    
    def _test_groq_connection(self) -> None:
        """Test Groq service connection"""
        try:
            # Simple test request
            response = self.client.chat.completions.create(
                model=self.config.groq.model,
                messages=[{"role": "user", "content": "Test connection"}],
                max_tokens=10,
                temperature=0.1
            )
            
            if response and response.choices:
                self.logger.info("Groq connection test successful")
            else:
                self.logger.warning("Groq connection test returned empty response")
                
        except Exception as e:
            self.logger.warning(f"Groq connection test failed: {e}")
    
    def _test_connection(self) -> None:
        """Test AI service connection (legacy method)"""
        if self.provider == 'gemini':
            self._test_gemini_connection()
        elif self.provider == 'groq':
            self._test_groq_connection()
    
    def transcribe_audio(self, audio_file_path: str) -> Optional[str]:
        if not self.client:
            return None
            
        if self.provider == 'gemini':
            # Use Google Speech-to-Text for Gemini provider
            return self._transcribe_with_google_speech(audio_file_path)
        elif self.provider == 'groq':
            # Use Groq's Whisper for transcription
            return self._transcribe_with_groq_whisper(audio_file_path)
        else:
            self.logger.warning(f"Audio transcription not supported for provider: {self.provider}")
            return None
    
    def _transcribe_with_google_speech(self, audio_file_path: str) -> Optional[str]:
        """Transcribe audio using speech_recognition library"""
        try:
            import speech_recognition as sr
            from pydub import AudioSegment
            from pathlib import Path
            import tempfile
            import os
            
            audio_path = Path(audio_file_path)
            if not audio_path.exists():
                self.logger.error(f"Audio file not found: {audio_file_path}")
                return None
            
            # Initialize recognizer
            recognizer = sr.Recognizer()
            
            # Convert audio to WAV format if needed
            temp_wav_path = None
            try:
                # Load audio file
                if audio_path.suffix.lower() not in ['.wav']:
                    # Convert to WAV
                    audio = AudioSegment.from_file(str(audio_path))
                    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                        temp_wav_path = temp_file.name
                        audio.export(temp_wav_path, format='wav')
                    audio_file_to_use = temp_wav_path
                else:
                    audio_file_to_use = str(audio_path)
                
                # Transcribe audio
                with sr.AudioFile(audio_file_to_use) as source:
                    # Adjust for ambient noise
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    # Record the audio
                    audio_data = recognizer.record(source)
                
                # Try Google Web Speech API first (free but requires internet)
                try:
                    text = recognizer.recognize_google(audio_data, language='en-US')
                    self.logger.info(f"Successfully transcribed audio: {text}")
                    return self._clean_transcription(text)
                except sr.RequestError as e:
                    self.logger.warning(f"Google Speech Recognition unavailable: {e}")
                    # Fallback to offline recognition
                    try:
                        text = recognizer.recognize_sphinx(audio_data)
                        self.logger.info(f"Offline transcription successful: {text}")
                        return self._clean_transcription(text)
                    except (sr.RequestError, sr.UnknownValueError):
                        self.logger.warning("Offline speech recognition also failed")
                        return None
                except sr.UnknownValueError:
                    self.logger.warning("Could not understand audio content")
                    return None
                    
            finally:
                # Clean up temporary file
                if temp_wav_path and os.path.exists(temp_wav_path):
                    os.unlink(temp_wav_path)
                    
        except ImportError as e:
            self.logger.error(f"Required audio processing libraries not installed: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Audio transcription failed: {e}")
            return None
    
    def _transcribe_with_groq_whisper(self, audio_file_path: str) -> Optional[str]:
        """Transcribe audio using Groq's Whisper"""
        try:
            audio_path = Path(audio_file_path)
            if not audio_path.exists():
                return None
            
            with open(audio_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-large-v3",
                    language="en",
                    response_format="text",
                    temperature=0.0
                )
            
            if transcription and transcription.strip():
                return self._clean_transcription(transcription)
            return None
                
        except Exception as e:
            self.logger.warning(f"Groq Whisper transcription failed: {e}")
            return None
    
    def _clean_transcription(self, text: str) -> str:
        """
        Clean and enhance transcribed text
        
        Args:
            text: Raw transcribed text
            
        Returns:
            Cleaned and enhanced text
        """
        try:
            # Remove extra whitespace
            cleaned = re.sub(r'\s+', ' ', text.strip())
            
            # Capitalize first letter
            if cleaned:
                cleaned = cleaned[0].upper() + cleaned[1:]
            
            # Ensure proper sentence ending
            if cleaned and not cleaned.endswith(('.', '!', '?')):
                cleaned += '.'
            
            return cleaned
            
        except Exception as e:
            self.logger.warning(f"Text cleaning failed: {e}")
            return text
    
    def generate_freecad_code(self, command: str, model_type: str = "2d", 
                             quality_level: str = "professional", include_materials: bool = False) -> Optional[str]:
        if not self.client:
            return None
        
        # FORCE 2D mode - we only generate blueprints now
        model_type = "2d"
        
        try:
            self.logger.info(f"Generating professional 2D blueprint for: {command}")
            
            # Create intelligent prompt using dynamic configuration
            prompt = self._create_professional_prompt(command, model_type, quality_level, include_materials)
            
            # Validate prompt was created successfully
            if not prompt or not prompt.strip():
                self.logger.error("Failed to create prompt - using fallback")
                prompt = f"Create a complete FreeCAD Python script for: {command}. Include proper imports, document creation, and object positioning."
            
            # Generate code with AI based on provider
            if self.provider == 'gemini':
                generated_code = self._generate_with_gemini(prompt)
            elif self.provider == 'groq':
                generated_code = self._generate_with_groq(prompt)
            else:
                self.logger.error(f"Unknown provider: {self.provider}")
                return None
            
            if generated_code:
                # Clean and validate generated code
                cleaned_code = self._clean_generated_code(generated_code)
                
                # CRITICAL: Check for 3D objects and reject them
                if self._contains_3d_objects(cleaned_code):
                    self.logger.error("Generated code contains 3D objects! Regenerating with 2D-only...")
                    return self._regenerate_as_2d_only(command, model_type)
                
                # Check if output is too simple (just basic rectangle)
                if cleaned_code and not self._has_sufficient_complexity(cleaned_code):
                    self.logger.error("Generated code is too simple! Regenerating with complexity requirement...")
                    return self._regenerate_as_2d_only(command, model_type)
                
                if self._validate_freecad_code(cleaned_code):
                    self.logger.info("Professional FreeCAD code generated successfully")
                    return cleaned_code
                else:
                    self.logger.warning("Generated code failed validation, attempting to fix")
                    # Try to fix common issues
                    fixed_code = self._fix_common_issues(cleaned_code)
                    if self._validate_freecad_code(fixed_code):
                        return fixed_code
                    else:
                        # Return original code with warning - let user decide
                        self.logger.warning("Code validation failed, returning as-is")
                        return cleaned_code
            else:
                self.logger.warning("AI returned empty response for code generation")
                return None
            
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Code generation failed: {error_msg}")
            
            # Enhanced fallback logic
            if "rate limit" in error_msg.lower():
                self.logger.info("Rate limit hit, using intelligent fallback")
                return self._create_intelligent_fallback(command, model_type)
            elif "api" in error_msg.lower():
                self.logger.info("API error, using intelligent fallback")
                return self._create_intelligent_fallback(command, model_type)
            
            return None
    
    def _generate_with_gemini(self, prompt: str) -> Optional[str]:
        """Generate code using Gemini API with safety filter workaround"""
        try:
            # Since Gemini blocks CAD/3D content, use indirect approach
            self.logger.info("Using template-based generation due to Gemini safety restrictions")
            
            # Try a very generic programming request first
            try:
                generic_prompt = "Write Python code for a geometric modeling application that creates shapes"
                
                response = self.client.generate_content(
                    generic_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.1,
                        max_output_tokens=800,
                    ),
                    safety_settings=[
                        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                    ]
                )
                
                if response and hasattr(response, 'text') and response.text:
                    # Post-process the generic response to make it FreeCAD-specific
                    return self._adapt_generic_code_to_freecad(response.text, prompt)
                    
            except Exception as e:
                self.logger.warning(f"Generic Gemini approach failed: {e}")
            
            # If all AI approaches fail, use intelligent template matching
            return self._create_intelligent_template(prompt)
            
        except Exception as e:
            self.logger.error(f"Gemini generation completely failed: {e}")
            return self._create_intelligent_template(prompt)
    
    def _adapt_generic_code_to_freecad(self, generic_code: str, original_prompt: str) -> str:
        """Adapt generic geometric code to FreeCAD specific syntax"""
        # For now, return our intelligent template since Gemini is too restrictive
        return self._create_intelligent_template(original_prompt)
    
    def _create_intelligent_template(self, prompt: str) -> str:
        """Create intelligent FreeCAD template based on prompt analysis"""
        prompt_lower = prompt.lower()
        
        # Advanced prompt analysis
        if any(word in prompt_lower for word in ['house', 'building', 'apartment', 'bhk']):
            return self._generate_house_template(prompt_lower)
        elif any(word in prompt_lower for word in ['cube', 'box', 'rectangular']):
            return self._generate_cube_template(prompt_lower)
        elif any(word in prompt_lower for word in ['cylinder', 'pipe', 'tube']):
            return self._generate_cylinder_template(prompt_lower)
        elif any(word in prompt_lower for word in ['sphere', 'ball', 'round']):
            return self._generate_sphere_template(prompt_lower)
        else:
            return self._generate_generic_template(prompt_lower)
    
    def _generate_house_template(self, prompt: str) -> str:
        # Extract room count if mentioned
        room_count = 2  # default
        if 'bhk' in prompt or 'bedroom' in prompt:
            for word in prompt.split():
                if word.isdigit():
                    room_count = int(word)
                    break
        
        return f'''import FreeCAD
import Part

# Create new document
doc = FreeCAD.newDocument("House_Model")

# House dimensions (in millimeters)
house_length = 10000  # 10 meters
house_width = 8000    # 8 meters
wall_height = 3000    # 3 meters
wall_thickness = 200  # 200mm

# Create foundation
foundation = doc.addObject("Part::Box", "Foundation")
foundation.Length = house_length
foundation.Width = house_width
foundation.Height = 300
foundation.Placement.Base = FreeCAD.Vector(0, 0, 0)

# Create exterior walls
# Front wall
front_wall = doc.addObject("Part::Box", "FrontWall")
front_wall.Length = house_length
front_wall.Width = wall_thickness
front_wall.Height = wall_height
front_wall.Placement.Base = FreeCAD.Vector(0, 0, 300)

# Back wall
back_wall = doc.addObject("Part::Box", "BackWall")
back_wall.Length = house_length
back_wall.Width = wall_thickness
back_wall.Height = wall_height
back_wall.Placement.Base = FreeCAD.Vector(0, house_width - wall_thickness, 300)

# Left wall
left_wall = doc.addObject("Part::Box", "LeftWall")
left_wall.Length = wall_thickness
left_wall.Width = house_width
left_wall.Height = wall_height
left_wall.Placement.Base = FreeCAD.Vector(0, 0, 300)

# Right wall
right_wall = doc.addObject("Part::Box", "RightWall")
right_wall.Length = wall_thickness
right_wall.Width = house_width
right_wall.Height = wall_height
right_wall.Placement.Base = FreeCAD.Vector(house_length - wall_thickness, 0, 300)

# Create interior partitions for {room_count} bedrooms
for i in range({room_count}):
    partition = doc.addObject("Part::Box", f"Partition_{{i+1}}")
    partition.Length = house_length // 2
    partition.Width = wall_thickness
    partition.Height = wall_height
    partition.Placement.Base = FreeCAD.Vector(house_length // 4, (i + 1) * house_width // 3, 300)

# Create roof
roof = doc.addObject("Part::Box", "Roof")
roof.Length = house_length
roof.Width = house_width
roof.Height = 200
roof.Placement.Base = FreeCAD.Vector(0, 0, wall_height + 300)

# Recompute and fit view
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
'''
    
    def _generate_cube_template(self, prompt: str) -> str:
        return '''import FreeCAD
import Part

# Create new document
doc = FreeCAD.newDocument("Cube_Model")

# Create a cube
cube = doc.addObject("Part::Box", "Cube")
cube.Length = 100  # 100mm
cube.Width = 100   # 100mm
cube.Height = 100  # 100mm
cube.Placement.Base = FreeCAD.Vector(0, 0, 0)

# Recompute and fit view
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
'''
    
    def _generate_cylinder_template(self, prompt: str) -> str:
        return '''import FreeCAD
import Part

# Create new document
doc = FreeCAD.newDocument("Cylinder_Model")

# Create a cylinder
cylinder = doc.addObject("Part::Cylinder", "Cylinder")
cylinder.Radius = 50   # 50mm radius
cylinder.Height = 100  # 100mm height
cylinder.Placement.Base = FreeCAD.Vector(0, 0, 0)

# Recompute and fit view
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
'''
    
    def _generate_sphere_template(self, prompt: str) -> str:
        return '''import FreeCAD
import Part

# Create new document
doc = FreeCAD.newDocument("Sphere_Model")

# Create a sphere
sphere = doc.addObject("Part::Sphere", "Sphere")
sphere.Radius = 50  # 50mm radius
sphere.Placement.Base = FreeCAD.Vector(0, 0, 0)

# Recompute and fit view
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
'''
    
    def _generate_generic_template(self, prompt: str) -> str:
        return '''import FreeCAD
import Part

# Create new document
doc = FreeCAD.newDocument("Generic_Model")

# Create a basic object
obj = doc.addObject("Part::Box", "BasicObject")
obj.Length = 100
obj.Width = 100
obj.Height = 100
obj.Placement.Base = FreeCAD.Vector(0, 0, 0)

# Recompute and fit view
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
'''
    
    def _get_basic_freecad_template(self, prompt: str) -> str:
        """Generate a basic FreeCAD template when AI fails"""
        
        # Analyze prompt to create better template
        prompt_lower = prompt.lower()
        
        if 'cube' in prompt_lower or 'box' in prompt_lower:
            object_type = "cube"
            create_code = """cube = doc.addObject("Part::Box", "Cube")
cube.Length = 100
cube.Width = 100  
cube.Height = 100"""
        
        elif 'cylinder' in prompt_lower or 'pipe' in prompt_lower:
            object_type = "cylinder"
            create_code = """cylinder = doc.addObject("Part::Cylinder", "Cylinder")
cylinder.Radius = 50
cylinder.Height = 100"""
        
        elif 'sphere' in prompt_lower or 'ball' in prompt_lower:
            object_type = "sphere"
            create_code = """sphere = doc.addObject("Part::Sphere", "Sphere")
sphere.Radius = 50"""
        
        elif 'house' in prompt_lower or 'building' in prompt_lower:
            object_type = "house structure"
            create_code = """# Create foundation
foundation = doc.addObject("Part::Box", "Foundation")
foundation.Length = 8000
foundation.Width = 6000
foundation.Height = 300

# Create walls
wall1 = doc.addObject("Part::Box", "Wall1")
wall1.Length = 8000
wall1.Width = 200
wall1.Height = 3000
wall1.Placement.Base = FreeCAD.Vector(0, 0, 300)

wall2 = doc.addObject("Part::Box", "Wall2")
wall2.Length = 200
wall2.Width = 6000
wall2.Height = 3000
wall2.Placement.Base = FreeCAD.Vector(0, 0, 300)"""
        
        else:
            object_type = "simple object"
            create_code = """# Create a basic object
obj = doc.addObject("Part::Box", "BasicObject")
obj.Length = 100
obj.Width = 100
obj.Height = 100"""
        
        template = f'''import FreeCAD
import Part

# Create new document
doc = FreeCAD.newDocument("GeneratedModel")

# Create {object_type} (AI fallback for: {prompt[:80]}...)
{create_code}

# Set position at origin
# obj.Placement.Base = FreeCAD.Vector(0, 0, 0)

# Recompute and fit view
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
'''
        return template
    
    def _generate_with_groq(self, prompt: str) -> Optional[str]:
        """Generate code using Groq API"""
        try:
            # Validate prompt is not empty
            if not prompt or not prompt.strip():
                self.logger.error("Empty prompt provided to Groq API")
                return None
            
            # Get system prompt and validate it too
            system_prompt = self._get_system_prompt()
            if not system_prompt or not system_prompt.strip():
                self.logger.error("Empty system prompt")
                system_prompt = "You are a FreeCAD Python code generator. Generate clean, functional FreeCAD Python code."
            
            response = self.client.chat.completions.create(
                model=self.config.groq.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user", 
                        "content": prompt.strip()
                    }
                ],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                top_p=0.95,
                stop=None
            )
            
            if response and response.choices:
                return response.choices[0].message.content
            return None
            
        except Exception as e:
            self.logger.error(f"Groq generation failed: {e}")
            return None
    
    def _fix_common_issues(self, code: str) -> str:
        """Attempt to fix common FreeCAD code issues"""
        try:
            # Remove problematic deprecated patterns first
            code = re.sub(r'Units[.]setPreferredUnitSystem[(].*?[)]', '', code)
            code = re.sub(r'FreeCAD[.]Units[.]setPreferredUnitSystem[(].*?[)]', '', code)
            code = re.sub(r'FreeCAD[.]Units[.]setUnitSystem[(].*?[)]', '', code)  # Fix for setUnitSystem
            code = re.sub(r'Units[.]setUnitSystem[(].*?[)]', '', code)  # Fix for Units.setUnitSystem
            code = re.sub(r'import Units.*?\n', '', code)
            code = re.sub(r'from Units import.*?\n', '', code)
            code = re.sub(r'[.]ActiveMaterial.*?\n', '', code)
            code = re.sub(r'[.]DiffuseColor[ \t]*=.*?\n', '', code)
            code = re.sub(r'[.]Material[ \t]*=.*?\n', '', code)
            code = re.sub(r'App[.]setActiveDocument[(].*?[)]', '', code)
            code = re.sub(r'FreeCADGui[.]showMainWindow[(][)]', '', code)
            code = re.sub(r'FreeCADGui[.]updateGui[(][)]', '', code)
            
            # Fix missing imports
            if 'import FreeCAD' not in code:
                code = 'import FreeCAD\nimport Part\n\n' + code
            
            # Fix missing document creation
            if 'newDocument' not in code:
                lines = code.split('\n')
                import_end = 0
                for i, line in enumerate(lines):
                    if line.strip().startswith('import') or line.strip().startswith('from'):
                        import_end = i + 1
                
                lines.insert(import_end, '\n# Create new document\ndoc = FreeCAD.newDocument("Generated_Model")\n')
                code = '\n'.join(lines)
            
            # Fix missing recompute
            if 'doc.recompute()' not in code:
                code += '\n\n# Finalize model\ndoc.recompute()\n'
            
            # Fix missing ViewFit
            if 'ViewFit' not in code and 'viewIsometric' not in code:
                code += '''
# Set view if GUI is available
if hasattr(FreeCAD, 'Gui') and FreeCAD.Gui:
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    try:
        FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
    except:
        pass
'''
            
            # Clean up empty lines
            lines = code.split('\n')
            cleaned_lines = [line for line in lines if line.strip() or not line]
            code = '\n'.join(cleaned_lines)
            
            return code
            
        except Exception as e:
            self.logger.warning(f"Failed to fix code issues: {e}")
            return code

    def _create_intelligent_fallback(self, command: str, model_type: str) -> str:
        """Create intelligent fallback based on command analysis"""
        try:
            from config.dynamic_building_config import dynamic_config
            
            # Try to get building specification for intelligent fallback
            building_spec = dynamic_config.parse_building_command(command)
            
            if building_spec:
                return self._create_dynamic_fallback(building_spec)
            else:
                return self._create_generic_fallback(command, model_type)
                
        except Exception as e:
            self.logger.warning(f"Intelligent fallback failed: {e}")
            return self._create_intelligent_fallback("simple cube", "3d")

    def _create_dynamic_fallback(self, building_spec) -> str:
        """Create fallback code based on building specification"""
        from config.dynamic_building_config import dynamic_config
        
        standards = dynamic_config.get_construction_standards(building_spec.category, building_spec.region)
        
        code = f'''import FreeCAD
import Part

# Create new document
doc = FreeCAD.newDocument("{building_spec.name.replace(' ', '_')}")
print("Creating {building_spec.name}...")

# Construction standards
WALL_THICKNESS = {standards.get('wall_thickness', {}).get('exterior', 250)}
CEILING_HEIGHT = {standards.get('ceiling_height', 3000)}
DOOR_WIDTH = {standards.get('door_dimensions', {}).get('standard', {}).get('width', 900)}
WINDOW_WIDTH = {standards.get('window_dimensions', {}).get('standard', {}).get('width', 1200)}

# Calculate total building dimensions
total_area = {building_spec.total_area_range[1]} * 1000000  # Convert to mm2
building_width = int((total_area * 0.6) ** 0.5)  # Assume 1:1.6 ratio
building_length = int(total_area / building_width)

print(f"Building dimensions: {{building_width}}mm x {{building_length}}mm")

# Create foundation slab
foundation = Part.makeBox(building_length, building_width, {standards.get('slab_thickness', 150)})
foundation_obj = doc.addObject("Part::Feature", "Foundation")
foundation_obj.Shape = foundation
foundation_obj.ViewObject.ShapeColor = (0.7, 0.7, 0.7)
foundation_obj.Label = "Foundation Slab"

# Create exterior walls
wall_height = CEILING_HEIGHT
'''

        # Add rooms dynamically
        x_offset = 0
        y_offset = 0
        
        for i, room in enumerate(building_spec.rooms):
            width, length, height = dynamic_config.calculate_room_dimensions(room, building_spec.total_area_range[1])
            
            code += f'''
# {room.name.replace('_', ' ').title()}
room_{i}_walls = []
# Create room walls (simplified)
room_{i}_floor = Part.makeBox({width}, {length}, 50)
room_{i}_floor = room_{i}_floor.translate(FreeCAD.Vector({x_offset}, {y_offset}, {standards.get('slab_thickness', 150)}))
room_{i}_obj = doc.addObject("Part::Feature", "{room.name}")
room_{i}_obj.Shape = room_{i}_floor
room_{i}_obj.ViewObject.ShapeColor = (0.9, 0.9, 0.8)
room_{i}_obj.Label = "{room.name.replace('_', ' ').title()} ({room.area_percentage}%)"
'''
            
            # Update offsets for next room (simple grid layout)
            x_offset += width + 200  # Add some spacing
            if x_offset > int((building_spec.total_area_range[1] * 1000000 / int((building_spec.total_area_range[1] * 1000000 * 0.6) ** 0.5)) * 0.7):  # Wrap to next row
                x_offset = 0
                y_offset += length + 200

        code += '''
# Finalize model
doc.recompute()

# Set view if GUI is available
if hasattr(FreeCAD, 'Gui') and FreeCAD.Gui:
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    try:
        FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
    except:
        pass

print("Dynamic building model created successfully!")
'''
        
        return code

    def _create_generic_fallback(self, command: str, model_type: str) -> str:
        """Create generic fallback for non-architectural models"""
        
        # Simple analysis of command
        size = 1000  # Default 1m
        if "large" in command.lower():
            size = 2000
        elif "small" in command.lower():
            size = 500
        
        shape_type = "box"
        if "cylinder" in command.lower() or "pipe" in command.lower():
            shape_type = "cylinder"
        elif "sphere" in command.lower() or "ball" in command.lower():
            shape_type = "sphere"
        
        code = f'''import FreeCAD
import Part

# Create new document
doc = FreeCAD.newDocument("Generic_Model")
print("Creating model for: {command}")

# Create basic shape
'''
        
        if shape_type == "cylinder":
            code += f'''shape = Part.makeCylinder({size//2}, {size})'''
        elif shape_type == "sphere":
            code += f'''shape = Part.makeSphere({size//2})'''
        else:
            code += f'''shape = Part.makeBox({size}, {size}, {size})'''
        
        code += f'''

# Add to document
obj = doc.addObject("Part::Feature", "{shape_type.title()}")
obj.Shape = shape
obj.ViewObject.ShapeColor = (0.6, 0.8, 0.9)
obj.Label = "{command}"

# Finalize
doc.recompute()

if hasattr(FreeCAD, 'Gui') and FreeCAD.Gui:
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    try:
        FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
    except:
        pass

print("Generic model created successfully!")
'''
        
        return code
        return """You are an expert FreeCAD architect and engineer. Generate professional, accurate FreeCAD Python code for architectural and engineering models.

CORE PRINCIPLES:
- Create structurally accurate and professionally detailed models
- Follow real-world architectural standards and building codes
- Use proper FreeCAD Python API with clean, readable code
- Include appropriate materials, colors, and realistic dimensions
- Generate code that executes without errors in FreeCAD

TECHNICAL REQUIREMENTS:
- Import FreeCAD and Part modules
- Create new document with descriptive name
- Use millimeters as the unit system
- Build models with proper geometric relationships
- Include walls, doors, windows, and structural elements
- Add appropriate colors and labels for clarity
- End with doc.recompute() and ViewFit commands
- Avoid deprecated or invalid FreeCAD attributes

CODE QUALITY:
- Write clean, well-commented Python code
- Use meaningful variable names
- Group related operations logically
- Include error handling where appropriate
- Follow professional coding standards

ARCHITECTURAL ACCURACY:
- Respect minimum room sizes and building codes
- Use realistic wall thicknesses and ceiling heights
- Position doors and windows appropriately
- Include structural elements like slabs and beams
- Consider functional layouts and circulation

Generate production-ready FreeCAD code that creates professional architectural models."""

    def _create_professional_prompt(self, command: str, model_type: str, quality_level: str, include_materials: bool) -> str:
        """Create enhanced professional prompt using dynamic building configuration"""
        try:
            from config.dynamic_building_config import dynamic_config
            
            # Try to parse command and get building specification
            building_spec = dynamic_config.parse_building_command(command)
            
            if building_spec:
                # Use dynamic prompt for known building types
                return dynamic_config.generate_dynamic_prompt(building_spec)
            else:
                # Fallback to enhanced generic prompt
                return self._create_enhanced_generic_prompt(command, model_type, quality_level, include_materials)
                
        except Exception as e:
            self.logger.warning(f"Failed to create dynamic prompt: {e}")
            return self._create_enhanced_generic_prompt(command, model_type, quality_level, include_materials)
    
    def _create_enhanced_generic_prompt(self, command: str, model_type: str, quality_level: str, include_materials: bool) -> str:
        """Create enhanced prompt with intelligent analysis"""
        
        # Analyze if this is an architectural command
        architectural_keywords = ['house', 'building', 'apartment', 'room', 'bhk', 'parking', 'garden', 'floor', 'wall', 'door', 'window']
        is_architectural = any(keyword.lower() in command.lower() for keyword in architectural_keywords)
        
        if is_architectural:
            return self._create_smart_architectural_prompt(command, model_type, quality_level, include_materials)
        else:
            return self._create_general_engineering_prompt(command, model_type, quality_level, include_materials)
    
    def _create_smart_architectural_prompt(self, command: str, model_type: str, quality_level: str, include_materials: bool) -> str:
        """Create intelligent architectural prompt that analyzes the command"""
        
        # Parse architectural requirements from command
        command_lower = command.lower()
        
        # Extract BHK information and determine rooms
        bhk_match = None
        rooms_needed = []
        
        for bhk_type in ['1bhk', '2bhk', '3bhk', '4bhk', '1 bhk', '2 bhk', '3 bhk', '4 bhk']:
            if bhk_type in command_lower:
                bhk_match = bhk_type.replace(' ', '')
                break
        
        # Get construction standards
        standards = self.construction_standards.get('construction_standards', {})
        materials = self.construction_standards.get('materials', {})
        
        # Intelligent room planning based on BHK
        if bhk_match:
            bhk_num = int(bhk_match[0])
            if bhk_num == 1:
                rooms_needed = ['Living Room', 'Bedroom', 'Kitchen', 'Bathroom']
            elif bhk_num == 2:
                rooms_needed = ['Living Room', 'Master Bedroom', 'Bedroom 2', 'Kitchen', 'Bathroom 1', 'Bathroom 2']
            elif bhk_num == 3:
                rooms_needed = ['Living Room', 'Master Bedroom', 'Bedroom 2', 'Bedroom 3', 'Kitchen', 'Dining Room', 'Bathroom 1', 'Bathroom 2', 'Bathroom 3']
            elif bhk_num == 4:
                rooms_needed = ['Living Room', 'Master Bedroom', 'Bedroom 2', 'Bedroom 3', 'Bedroom 4', 'Kitchen', 'Dining Room', 'Bathroom 1', 'Bathroom 2', 'Bathroom 3', 'Study Room']
        
        # Intelligent model type detection
        model_type = self._detect_model_type(command_lower)
        
        # Extract features based on model type
        features_needed = []
        if model_type == 'architectural':
            if any(word in command_lower for word in ['parking', 'garage', 'car']):
                features_needed.append('Parking Area')
            if any(word in command_lower for word in ['garden', 'landscap', 'yard']):
                features_needed.append('Garden')
            if 'balcony' in command_lower:
                features_needed.append('Balcony')
            if any(word in command_lower for word in ['terrace', 'rooftop']):
                features_needed.append('Terrace')
            if any(word in command_lower for word in ['swimming', 'pool']):
                features_needed.append('Swimming Pool')
            if any(word in command_lower for word in ['compound', 'boundary', 'wall']):
                features_needed.append('Compound Wall')
        elif model_type == 'civil':
            if any(word in command_lower for word in ['bridge', 'span', 'pier']):
                features_needed.append('Bridge Structure')
            if any(word in command_lower for word in ['beam', 'column', 'slab']):
                features_needed.append('Structural Elements')
        elif model_type == 'mechanical':
            if any(word in command_lower for word in ['gear', 'shaft', 'bearing']):
                features_needed.append('Mechanical Components')
            if any(word in command_lower for word in ['motor', 'engine', 'pump']):
                features_needed.append('Drive System')
        
        # Enhanced material and color system
        material_instruction = ""
        if include_materials:
            # Define HIGHLY DISTINCT colors for easy identification
            component_colors = {
                'foundation': '(0.4, 0.4, 0.4)',  # Dark gray foundation
                'exterior_walls': '(0.9, 0.85, 0.7)',  # Light cream walls
                'interior_walls': '(1.0, 1.0, 1.0)',  # Pure white partitions
                'doors': '(0.7, 0.4, 0.1)',  # Distinct brown doors
                'windows': '(0.3, 0.6, 1.0)',  # Bright blue windows
                'window_frames': '(0.8, 0.8, 0.8)',  # Silver frames
                'roof': '(0.8, 0.2, 0.1)',  # Bright red roof
                'balcony': '(0.7, 0.9, 0.7)',  # Light green balcony
                'parking': '(0.2, 0.2, 0.2)',  # Very dark parking
                'garden': '(0.1, 0.8, 0.1)',  # Bright green garden
                'compound_wall': '(0.6, 0.6, 0.6)',  # Medium gray boundary
                'terrace': '(0.9, 0.7, 0.5)'  # Light orange terrace
            }
            
            material_instruction = f"""
HIGHLY VISIBLE COLOR DIFFERENTIATION FOR EASY IDENTIFICATION:
- Foundation: Dark gray concrete {component_colors['foundation']}
- Exterior Walls: Light cream finish {component_colors['exterior_walls']} 
- Interior Walls: Pure white partitions {component_colors['interior_walls']}
- Doors: Distinct brown wood {component_colors['doors']}
- Windows: Bright blue glass {component_colors['windows']} with silver frames {component_colors['window_frames']}
- Roof: Bright red tiles {component_colors['roof']}
- Balcony: Light green concrete {component_colors['balcony']}
- Parking Area: Very dark asphalt {component_colors['parking']}
- Garden Area: Bright green grass {component_colors['garden']}
- Compound Wall: Medium gray boundary {component_colors['compound_wall']}
- Terrace: Light orange tiles {component_colors['terrace']}

COMPONENT IDENTIFICATION GUIDE:
- DARK GRAY = Foundation base
- LIGHT CREAM = Main building walls
- BRIGHT RED = Roof structure
- BROWN = Doors and entrances
- BRIGHT BLUE = Windows and openings
- BRIGHT GREEN = Garden/landscape areas
- VERY DARK = Parking surfaces

CONSTRUCTION SPECIFICATIONS (Professional Standards):
- Foundation Depth: 1500mm
- Exterior Wall Thickness: {standards.get('wall_thickness', {}).get('residential', {}).get('exterior', 230)}mm
- Interior Wall Thickness: {standards.get('wall_thickness', {}).get('residential', {}).get('interior', 150)}mm
- Ceiling Height: {standards.get('ceiling_height', {}).get('residential', 3000)}mm
- Door Dimensions: {standards.get('door_dimensions', {}).get('standard', {}).get('width', 900)}mm x {standards.get('door_dimensions', {}).get('standard', {}).get('height', 2100)}mm
- Window Dimensions: {standards.get('window_dimensions', {}).get('standard', {}).get('width', 1200)}mm x {standards.get('window_dimensions', {}).get('standard', {}).get('height', 1200)}mm
- Roof Slab Thickness: {standards.get('slab_thickness', {}).get('residential', 150)}mm"""

        # Calculate dimensions based on model type and requirements
        if model_type == 'architectural':
            total_rooms = len(rooms_needed)
            # Parametric calculation instead of hardcoded minimums
            area_per_room = 15  # square meters average
            total_area = total_rooms * area_per_room * 1000000  # Convert to mm2
            building_length = int((total_area * 1.6) ** 0.5)  # Golden ratio proportions
            building_width = int(building_length / 1.6)
        else:
            building_length = 10000  # Default 10m
            building_width = 8000   # Default 8m
        
        # Create component colors for material differentiation
        component_colors = {
            'foundation': '(0.4, 0.4, 0.4)',
            'exterior_walls': '(0.9, 0.85, 0.7)', 
            'interior_walls': '(1.0, 1.0, 1.0)',
            'doors': '(0.7, 0.4, 0.1)',
            'windows': '(0.3, 0.6, 1.0)',
            'roof': '(0.8, 0.2, 0.1)'
        }
        
        # Return the parametric prompt
        return self._create_parametric_prompt(command, model_type, bhk_match, rooms_needed, features_needed, building_length, building_width, component_colors)
        
    def _detect_model_type(self, command_lower: str) -> str:
        """Detect the type of model to generate based on command"""
        # Architectural keywords
        if any(word in command_lower for word in ['house', 'bhk', 'villa', 'apartment', 'building', 'room', 'home']):
            return 'architectural'
        # Civil engineering keywords  
        elif any(word in command_lower for word in ['bridge', 'beam', 'column', 'slab', 'foundation', 'structure']):
            return 'civil'
        # Mechanical keywords
        elif any(word in command_lower for word in ['gear', 'shaft', 'bearing', 'motor', 'engine', 'mechanism']):
            return 'mechanical'
        # Infrastructure keywords
        elif any(word in command_lower for word in ['road', 'street', 'drainage', 'pavement', 'infrastructure']):
            return 'infrastructure'
        else:
            return 'architectural'  # Default to architectural
    
    def _create_parametric_prompt(self, command: str, model_type: str, bhk_match: str, rooms_needed: list, features_needed: list, building_length: int, building_width: int, component_colors: dict) -> str:
        """Create the parametric AI Design Engineer prompt"""
        
        return f"""AI DESIGN ENGINEER - PARAMETRIC CAD GENERATION SYSTEM

INTELLIGENT DESIGN PRINCIPLES - NO HARDCODING ALLOWED:
User Command: "{command}"
Detected Type: {bhk_match.upper() if bhk_match else 'CUSTOM ARCHITECTURE'}
Required Spaces: {', '.join(rooms_needed) if rooms_needed else 'Auto-detected from context'}
Features: {', '.join(features_needed) if features_needed else 'Standard architectural elements'}

PARAMETRIC GENERATION RULES:
You are an expert AI Design Engineer. Generate a professional 3D CAD model using ONLY computed parameters.

CRITICAL: NO HARDCODED VALUES ALLOWED!
- All dimensions must be computed from relationships and ratios
- Use parametric scaling based on building type and user requirements
- Derive positions and sizes from mathematical relationships
- Auto-scale elements proportionally

PARAMETRIC COMPUTATION SYSTEM:

1. DYNAMIC PARAMETER CALCULATION:
   - Base parameters from user context
   - total_area_needed = len(rooms) * 15 (15 sqm per room minimum)
   - building_length = math.sqrt(total_area_needed * 1.6) (Golden ratio proportion)
   - building_width = building_length / 1.6
   - wall_height = building_length * 0.15 (Height proportional to length)
   - foundation_depth = wall_height * 0.5 (Foundation depth ratio)
   
   Room proportions (no hardcoded sizes):
   - living_room_ratio = 0.25 (25% of total area)
   - master_bedroom_ratio = 0.20 (20% of total area)
   - kitchen_ratio = 0.15 (15% of total area)
   - bathroom_ratio = 0.08 (8% of total area per bathroom)

2. INTELLIGENT ARCHITECTURAL LOGIC:
   - Generate integrated building design (NOT separate boxes)
   - Use proportional relationships for all dimensions
   - Create connected spaces with shared walls
   - Position rooms based on functional adjacencies
   - Scale all elements proportionally to building size

3. ENGINEERING STANDARDS APPLICATION:
   - Wall thickness = building_length * 0.012 (exterior)
   - Wall thickness = building_length * 0.008 (interior)
   - Door height = wall_height * 0.7
   - Window height = wall_height * 0.4
   - Roof thickness = building_length * 0.008

4. DYNAMIC POSITIONING SYSTEM:
   - Foundation: covers entire building footprint
   - Exterior walls: form continuous perimeter
   - Interior walls: divide spaces proportionally
   - Openings: positioned at optimal locations
   - External features: scaled to building proportions

MATERIAL SPECIFICATIONS:
- Foundation: Reinforced concrete with proper curing
- Walls: Brick masonry with cement mortar
- Roof: RCC slab with waterproof treatment
- Doors: Wooden frames with proper hardware
- Windows: Aluminum frames with glass panels

PARAMETRIC FREECAD IMPLEMENTATION:

```python
import FreeCAD
import Part
import math

# Create document
doc = FreeCAD.newDocument("Parametric_Architecture")

# STEP 1: COMPUTE ALL PARAMETERS (NO HARDCODING)
rooms_needed = {len(rooms_needed)}
total_area = rooms_needed * 15000  # 15 sqm per room in mm2
building_length = int(math.sqrt(total_area * 1.6))  # Golden ratio
building_width = int(building_length / 1.6)
wall_height = int(building_length * 0.15)
foundation_depth = int(wall_height * 0.5)

# Wall thicknesses (proportional)
ext_wall_thick = int(building_length * 0.012)  # Exterior wall
int_wall_thick = int(building_length * 0.008)  # Interior wall

# Opening dimensions (proportional)
door_width = int(wall_height * 0.3)
door_height = int(wall_height * 0.7)
window_width = int(wall_height * 0.4)
window_height = int(wall_height * 0.4)

# STEP 2: CREATE INTEGRATED BUILDING STRUCTURE
# Foundation (single continuous base)
foundation = doc.addObject("Part::Box", "Foundation")
foundation.Length.Value = building_length + 2 * ext_wall_thick
foundation.Width.Value = building_width + 2 * ext_wall_thick
foundation.Height.Value = foundation_depth
foundation.Placement.Base = FreeCAD.Vector(-ext_wall_thick, -ext_wall_thick, -foundation_depth)
foundation.ViewObject.ShapeColor = {component_colors['foundation']}

# Exterior walls (continuous perimeter)
walls = []
for i, (name, length, width, x, y) in enumerate([
    ("Front_Wall", building_length, ext_wall_thick, 0, 0),
    ("Back_Wall", building_length, ext_wall_thick, 0, building_width - ext_wall_thick),
    ("Left_Wall", ext_wall_thick, building_width, 0, 0),
    ("Right_Wall", ext_wall_thick, building_width, building_length - ext_wall_thick, 0)
]):
    wall = doc.addObject("Part::Box", name)
    wall.Length.Value = length
    wall.Width.Value = width
    wall.Height.Value = wall_height
    wall.Placement.Base = FreeCAD.Vector(x, y, 0)
    wall.ViewObject.ShapeColor = {component_colors['exterior_walls']}
    walls.append(wall)

# STEP 3: INTERIOR LAYOUT (PROPORTIONAL ROOM DIVISION)
# Calculate room positions based on proportions, not fixed coordinates
living_area = total_area * 0.25  # 25% for living room
kitchen_area = total_area * 0.15  # 15% for kitchen
# ... continue with proportional calculations

# STEP 4: ROOF AND COMPLETION
roof = doc.addObject("Part::Box", "Roof")
roof.Length.Value = building_length
roof.Width.Value = building_width
roof.Height.Value = int(building_length * 0.008)  # Proportional thickness
roof.Placement.Base = FreeCAD.Vector(0, 0, wall_height)
roof.ViewObject.ShapeColor = {component_colors['roof']}

# STEP 5: PROFESSIONAL SUMMARY
print("\\n" + "="*50)
print("PARAMETRIC MODEL GENERATED")
print("="*50)
print(f"Building Type: {{bhk_match.upper() if bhk_match else 'CUSTOM ARCHITECTURE'}}")
print(f"Total Length: {{building_length//1000}}m")
print(f"Total Width: {{building_width//1000}}m")
print(f"Wall Height: {{wall_height//1000}}m")
print(f"Foundation Depth: {{foundation_depth//1000}}m")
print(f"Total Area: {{(building_length * building_width)//1000000}} sqm")
print(f"Rooms: {{len(rooms_needed)}}")
print("Features: {', '.join(features_needed) if features_needed else 'Standard'}")
print("="*50)

# Final view setup
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()

GENERATE INTEGRATED ARCHITECTURAL MODEL WITH:
- All dimensions computed from relationships
- Proportional scaling based on building type
- Connected building structure (not separate boxes)
- Professional engineering ratios
- Context-aware room layouts
- Dynamic positioning system
- Comprehensive design summary

RESULT: Professional parametric architecture with intelligent design logic!

STRUCTURAL REQUIREMENTS:
1. FOUNDATION & BASE:
   - Concrete foundation extending proportionally below ground
   - Foundation should be wider than building on all sides
   - Slab thickness proportional to building size

2. ROOM LAYOUT (Parametric Residential):
   - Living Room: Calculated from total area * 0.25
   - Master Bedroom: Calculated from total area * 0.20
   - Bedroom: Calculated from total area * 0.15
   - Kitchen: Calculated from total area * 0.12
   - Bathroom: Calculated from total area * 0.08
   - Parking: Proportional to building size
   - Garden: Proportional open area

3. WALL SPECIFICATIONS:
   - Exterior walls: building_length * 0.012 thick
   - Interior walls: building_length * 0.008 thick
   - Wall height: building_length * 0.15
   - Foundation walls: proportional thickness

4. DOORS & WINDOWS:
   - Main door: wall_height * 0.3 x wall_height * 0.7
   - Room doors: proportional sizing
   - Windows: wall_height * 0.4 x wall_height * 0.4
   - Window sill height: wall_height * 0.3 from floor

5. PARKING & GARDEN:
   - Parking: Proportional slab thickness
   - Driveway: Proportional width
   - Garden: Landscaped area with boundary walls
   - Compound wall: Proportional height and thickness

TECHNICAL IMPLEMENTATION:
- Use FreeCAD Python API (import FreeCAD, Part)
- Create document with descriptive name
- ALL dimensions computed parametrically
- Use only plain numbers
- Position objects using computed coordinates
- Create realistic proportional relationships

MATERIAL SPECIFICATIONS:
- Foundation: Reinforced concrete with proper curing
- Walls: Brick masonry with cement mortar
- Roof: RCC slab with waterproof treatment
- Doors: Wooden frames with proper hardware
- Windows: Aluminum frames with glass panels

CONSTRUCTION SEQUENCE:
1. Create foundation and basement
2. Build exterior walls with proper thickness
3. Add interior partitions
4. Install doors and windows with proper openings
5. Create roof structure
6. Add parking area and driveway
7. Design garden and landscaping
8. Add finishing details and colors

OUTPUT REQUIREMENT:
Generate professional FreeCAD Python code that creates a structurally accurate, proportionally correct architectural model. The model should look like a real building, not just simple boxes. Each component should be properly sized and positioned according to Indian building standards."""
    
    def _create_general_engineering_prompt(self, command: str, model_type: str, quality_level: str, include_materials: bool) -> str:
        """Create prompt for non-architectural engineering models"""
        
        material_instruction = ""
        if include_materials:
            material_instruction = """
MATERIALS & APPEARANCE:
- Apply realistic colors and materials based on object type
- Use appropriate color schemes (e.g., metallic for mechanical parts)
- Add transparency where appropriate (glass, water, etc.)
- Consider real-world material properties"""

        quality_instructions = {
            "draft": "Focus on basic geometry and functionality. Simple, clean shapes.",
            "standard": "Include moderate detail level with proper proportions and basic features.",
            "professional": "Create highly detailed model with precise dimensions, fine features, and professional finish."
        }
        
        complexity_instruction = quality_instructions.get(quality_level, quality_instructions["standard"])
        
        return f"""Create a {quality_level} quality {model_type} FreeCAD model for: {command}

SPECIFICATIONS:
- Model Type: {model_type.upper()}
- Quality Level: {quality_level.title()}
- Design Approach: {complexity_instruction}

TECHNICAL REQUIREMENTS:
- Use FreeCAD Python API (import FreeCAD, Part)
- Create new document with descriptive name
- All dimensions in millimeters (use plain numbers, not quantities)
- Use realistic, functional proportions
- Include proper geometric relationships
- Add meaningful labels to all objects
- CRITICAL: Use only plain numbers in calculations, avoid mixing properties with numbers
- When accessing object dimensions, use .Value property (e.g., obj.Length.Value)
- Position objects using FreeCAD.Vector with plain number coordinates{material_instruction}

IMPLEMENTATION:
1. Start with imports and document creation
2. Define key dimensions as variables
3. Create main geometric shapes
4. Add details and features progressively
5. Apply materials and colors
6. Position and orient objects properly
7. Add informative labels
8. End with doc.recompute() and ViewFit

OUTPUT FORMAT:
- Clean, well-commented Python code
- Professional variable naming
- Logical code organization
- Error-free FreeCAD execution

Generate production-ready FreeCAD Python code that creates a professional {model_type} model."""
    
    def _get_system_prompt(self) -> str:
        """Get the enhanced system prompt for AI Design Engineer code generation"""
        from config.load_prompt import load_system_prompt
        return load_system_prompt()
    
    def _clean_generated_code(self, code: str) -> str:
        try:
            if '```python' in code:
                python_blocks = re.findall(r'```python\n?(.*?)\n?```', code, re.DOTALL)
                if python_blocks:
                    code = python_blocks[0]  # Take the first python block
            
            # Remove any remaining markdown artifacts
            code = re.sub(r'```python\n?', '', code)
            code = re.sub(r'```\n?', '', code)
            
            # Remove extra whitespace and normalize line endings
            lines = code.split('\n')
            cleaned_lines = []
            
            for line in lines:
                # Remove trailing whitespace and skip empty explanatory lines
                cleaned_line = line.rstrip()
                # Skip comment-only lines that are too long (likely explanations)
                if cleaned_line.startswith('#') and len(cleaned_line) > 100:
                    continue
                cleaned_lines.append(cleaned_line)
            
            # Join lines and normalize
            cleaned_code = '\n'.join(cleaned_lines)
            
            # Remove common problematic patterns
            cleaned_code = re.sub(r'FreeCADGui[.]showMainWindow[(][)]', '', cleaned_code)
            cleaned_code = re.sub(r'FreeCADGui[.]updateGui[(][)]', '', cleaned_code)
            
            # Remove invalid FreeCAD patterns
            cleaned_code = re.sub(r'FreeCAD[.]ActiveMaterial.*?\n', '', cleaned_code)
            cleaned_code = re.sub(r'[.]Material[ \t]*=.*?\n', '', cleaned_code)
            cleaned_code = re.sub(r'[.]DiffuseColor[ \t]*=.*?\n', '', cleaned_code)
            cleaned_code = re.sub(r'FreeCAD[.]ActiveDocument[.]ActiveMaterial.*?\n', '', cleaned_code)
            
            # Remove deprecated Units patterns
            cleaned_code = re.sub(r'Units[.]setPreferredUnitSystem[(].*?[)]', '', cleaned_code)
            cleaned_code = re.sub(r'import Units.*?\n', '', cleaned_code)
            cleaned_code = re.sub(r'from Units import.*?\n', '', cleaned_code)
            cleaned_code = re.sub(r'FreeCAD[.]Units[.]setPreferredUnitSystem[(].*?[)]', '', cleaned_code)
            cleaned_code = re.sub(r'FreeCAD[.]Units[.]setUnitSystem[(].*?[)]', '', cleaned_code)  # Fix for setUnitSystem
            cleaned_code = re.sub(r'Units[.]setUnitSystem[(].*?[)]', '', cleaned_code)  # Fix for Units.setUnitSystem
            
            # Remove import Part since we only use Draft for 2D drawings
            cleaned_code = re.sub(r'import Part\s*\n', '', cleaned_code)
            
            # Fix deprecated dimension API
            cleaned_code = self._fix_deprecated_dimension_api(cleaned_code)
            
            # Fix Part.makeBox usage that causes Label errors
            cleaned_code = self._fix_part_makebox_usage(cleaned_code)
            
            # Fix TechDraw issues
            cleaned_code = self._fix_techdraw_issues(cleaned_code)
            
            # Fix incomplete FreeCAD statements (edge case from cleaning)
            cleaned_code = re.sub(r'FreeCAD[.][ \t]*\n', '', cleaned_code)
            cleaned_code = re.sub(r'FreeCAD[.][ \t]*$', '', cleaned_code, flags=re.MULTILINE)
            
            # Remove other deprecated patterns
            cleaned_code = re.sub(r'FreeCADGui[.]showMainWindow[(][)]', '', cleaned_code)
            cleaned_code = re.sub(r'FreeCADGui[.]updateGui[(][)]', '', cleaned_code)
            cleaned_code = re.sub(r'[.]Transparency[ \t]*=.*?\n', '', cleaned_code)
            cleaned_code = re.sub(r'[.]LineColor[ \t]*=.*?\n', '', cleaned_code)
            cleaned_code = re.sub(r'[.]PointColor[ \t]*=.*?\n', '', cleaned_code)
            
            # Remove problematic App.* patterns
            cleaned_code = re.sub(r'App[.]setActiveDocument[(].*?[)]', '', cleaned_code)
            cleaned_code = re.sub(r'App[.]ActiveDocument = .*?\n', '', cleaned_code)
            
            # Fix common GUI attribute errors
            cleaned_code = re.sub(r'[.]ViewObject[.]Transparency[ \t]*=[ \t]*\d+', lambda m: m.group(0).replace('Transparency', 'ShapeColor = (0.8, 0.8, 0.8) #'), cleaned_code)
            
            # Remove orphaned comment lines from cleaning
            cleaned_code = re.sub(r'# Set the unit system to millimeters[ \t]*\n', '', cleaned_code)
            cleaned_code = re.sub(r'# Set unit system.*?\n', '', cleaned_code)
            
            # Remove duplicate imports to prevent "Empty module name" errors
            lines = cleaned_code.split('\n')
            seen_imports = set()
            deduplicated_lines = []
            imports_section = []
            code_section = []
            in_imports = True
            
            for line in lines:
                stripped = line.strip()
                
                # Handle import statements to remove duplicates
                if stripped.startswith('import ') or stripped.startswith('from '):
                    # Normalize the import statement for comparison
                    normalized_import = stripped.split('#')[0].strip()  # Remove inline comments
                    if normalized_import and normalized_import not in seen_imports and len(normalized_import) > 6:  # Valid import
                        seen_imports.add(normalized_import)
                        imports_section.append(line)
                    # Skip duplicate or empty imports
                elif stripped == '':
                    # Skip empty lines in imports section, but keep them in code section
                    if not in_imports:
                        code_section.append(line)
                else:
                    # We've moved past imports
                    in_imports = False
                    code_section.append(line)
            
            # Rebuild code with clean imports first, then code
            cleaned_code = '\n'.join(imports_section + [''] + code_section)
            
            # Remove malformed import lines that cause "Empty module name" errors
            cleaned_code = re.sub(r'^import[ \t]*$', '', cleaned_code, flags=re.MULTILINE)
            cleaned_code = re.sub(r'^from[ \t]*$', '', cleaned_code, flags=re.MULTILINE)
            cleaned_code = re.sub(r'^from[ \t]+import[ \t]*$', '', cleaned_code, flags=re.MULTILINE)
            cleaned_code = re.sub(r'^import[ \t]+$', '', cleaned_code, flags=re.MULTILINE)
            cleaned_code = re.sub(r'^from[ \t]+$', '', cleaned_code, flags=re.MULTILINE)
            
            # Remove empty lines that might be left from regex replacements
            lines = cleaned_code.split('\n')
            cleaned_lines = [line for line in lines if line.strip()]
            cleaned_code = '\n'.join(cleaned_lines)
            
            # Ensure proper imports at the beginning
            if 'import FreeCAD' not in cleaned_code:
                cleaned_code = 'import FreeCAD\nimport Part\n\n' + cleaned_code
            
            # Ensure document creation
            if 'newDocument' not in cleaned_code:
                lines = cleaned_code.split('\n')
                import_lines = []
                other_lines = []
                
                for line in lines:
                    if line.strip().startswith('import'):
                        import_lines.append(line)
                    else:
                        other_lines.append(line)
                
                doc_creation = 'doc = FreeCAD.newDocument("GeneratedModel")'
                cleaned_code = '\n'.join(import_lines) + '\n\n' + doc_creation + '\n' + '\n'.join(other_lines)
            
            # Ensure recompute at the end
            if 'doc.recompute()' not in cleaned_code:
                cleaned_code += '\n\ndoc.recompute()'
                
            # Ensure view fit at the end
            if 'ViewFit' not in cleaned_code:
                cleaned_code += '\nFreeCAD.Gui.SendMsgToActiveView("ViewFit")'
            
            # Fix FreeCAD unit mismatch issues
            # Convert property access to .Value to get plain numbers
            cleaned_code = re.sub(r'(\w+)\.Length([^a-zA-Z_])', r'\1.Length.Value\2', cleaned_code)
            cleaned_code = re.sub(r'(\w+)\.Width([^a-zA-Z_])', r'\1.Width.Value\2', cleaned_code)
            cleaned_code = re.sub(r'(\w+)\.Height([^a-zA-Z_])', r'\1.Height.Value\2', cleaned_code)
            cleaned_code = re.sub(r'(\w+)\.Radius([^a-zA-Z_])', r'\1.Radius.Value\2', cleaned_code)
            
            # Fix vector addition with mixed units
            cleaned_code = re.sub(r'FreeCAD[.]Vector[(][^)]+[)][ \t]*[+][ \t]*FreeCAD[.]Vector[(][^)]+[)]', 
                                lambda m: self._fix_vector_addition(m.group(0)), cleaned_code)
            
            # Final validation: Remove any lines that could cause "Empty module name" error
            lines = cleaned_code.split('\n')
            final_lines = []
            for line in lines:
                stripped = line.strip()
                # Skip lines that are just "import" or "from" without module names
                if stripped in ['import', 'from', 'import ', 'from ']:
                    continue
                # Skip malformed import statements
                if stripped.startswith('import ') and len(stripped.replace('import ', '').strip()) == 0:
                    continue
                if stripped.startswith('from ') and 'import' not in stripped:
                    continue
                final_lines.append(line)
            
            cleaned_code = '\n'.join(final_lines)
            
            # Fix double .Value.Value issues - this causes 'float' object has no attribute 'Value' errors
            cleaned_code = re.sub(r'\.Value\.Value', '.Value', cleaned_code)
            
            # Fix cases where .Value is applied to variables that are already numbers
            # Pattern: variable.Property.Value = number (correct)
            # But fix: number.Value = something (incorrect)
            cleaned_code = re.sub(r'(\d+)[.]Value[ \t]*=', r'\1 =', cleaned_code)
            
            # FIX INDENTATION ISSUES - CRITICAL
            cleaned_code = self._fix_indentation(cleaned_code)
            
            # ===== FINAL NUCLEAR CLEANUP - Last chance to fix ViewObject errors =====
            # This is the absolute last line of defense before returning code
            cleaned_code = self._nuclear_viewobject_fix(cleaned_code)
            
            # ===== FIX: Remove problematic LineStyle assignments =====
            # LineStyle doesn't exist on all ViewObject types, causes AttributeError
            cleaned_code = self._fix_linestyle_errors(cleaned_code)
            
            return cleaned_code
            
        except Exception as e:
            self.logger.warning(f"Code cleaning failed: {e}")
            return code
    
    def _fix_indentation(self, code: str) -> str:
        """Fix broken indentation in generated code - specifically for attribute assignments"""
        try:
            import ast
            
            # Try to parse the code - if it parses, indentation is OK
            try:
                ast.parse(code)
                return code  # Indentation is fine
            except SyntaxError as e:
                self.logger.warning(f"Indentation error detected at line {e.lineno}: {e.msg}. Attempting to fix...")
            
            lines = code.split('\n')
            fixed_lines = []
            
            # Pattern for object property assignments that should be on same indent as object creation
            # Example: wall.Length.Value = 200 (should follow wall = doc.addObject(...))
            property_pattern = r'^([a-zA-Z_]\w*)[.]\w+([.]Value)?\s*=\s*.+'
            
            i = 0
            while i < len(lines):
                line = lines[i]
                
                # Check if this line is an unindented property assignment
                if re.match(property_pattern, line.strip()) and not line.startswith((' ', '\t')):
                    # This is a property assignment at column 0 - needs indentation
                    # Look back to find the proper indent level
                    indent_to_use = ''
                    
                    # Look at previous non-empty line to get indent
                    for j in range(i - 1, -1, -1):
                        prev_line = lines[j]
                        if prev_line.strip():
                            # Get the indentation of the previous line
                            indent_match = re.match(r'^(\s*)', prev_line)
                            if indent_match:
                                prev_indent = indent_match.group(1)
                                # If previous line is object creation or assignment, use same indent
                                if '=' in prev_line or prev_line.strip().endswith(':'):
                                    if prev_line.strip().endswith(':'):
                                        # Increase indent for block
                                        indent_to_use = prev_indent + '    '
                                    else:
                                        # Same indent as previous assignment
                                        indent_to_use = prev_indent
                                else:
                                    # Use same indent as previous line
                                    indent_to_use = prev_indent
                            break
                    
                    # Apply the indentation
                    fixed_lines.append(indent_to_use + line.strip())
                else:
                    # Keep line as is
                    fixed_lines.append(line)
                
                i += 1
            
            fixed_code = '\n'.join(fixed_lines)
            
            # Try to parse the fixed code
            try:
                ast.parse(fixed_code)
                self.logger.info("Indentation fixed successfully")
                return fixed_code
            except SyntaxError as e2:
                # Still broken, try a more aggressive fix
                self.logger.warning(f"First fix attempt failed: {e2}. Trying aggressive fix...")
                return self._aggressive_indent_fix(code)
                
        except Exception as e:
            self.logger.error(f"Error fixing indentation: {e}")
            return code
    
    def _aggressive_indent_fix(self, code: str) -> str:
        """More aggressive indentation fix using heuristics"""
        try:
            lines = code.split('\n')
            fixed_lines = []
            current_indent = 0
            base_indent = '    '  # 4 spaces
            
            for i, line in enumerate(lines):
                stripped = line.strip()
                
                # Skip empty lines
                if not stripped:
                    fixed_lines.append('')
                    continue
                
                # Detect if we need to decrease indent
                if stripped.startswith(('else:', 'elif ', 'except:', 'except ', 'finally:', 'def ', 'class ')):
                    if current_indent > 0:
                        current_indent -= 1
                
                # Detect dedent patterns (closing blocks)
                if i > 0:
                    prev_stripped = lines[i-1].strip()
                    # If previous line was a single statement (return, pass, etc), we might need to dedent
                    if prev_stripped.startswith(('return ', 'break', 'continue', 'pass', 'raise ')):
                        # Check if current line is not a continuation of the block
                        if not stripped.startswith((' ', '\t')) and not stripped.startswith(('else:', 'elif ', 'except:', 'finally:')):
                            current_indent = max(0, current_indent - 1)
                
                # Apply current indentation
                fixed_line = (base_indent * current_indent) + stripped
                fixed_lines.append(fixed_line)
                
                # Detect if we need to increase indent for next line
                if stripped.endswith(':'):
                    current_indent += 1
            
            fixed_code = '\n'.join(fixed_lines)
            
            # Validate
            import ast
            try:
                ast.parse(fixed_code)
                self.logger.info("Aggressive indentation fix successful")
                return fixed_code
            except SyntaxError:
                self.logger.error("Could not fix indentation. Returning original code.")
                return code
                
        except Exception as e:
            self.logger.error(f"Aggressive indent fix failed: {e}")
            return code
    
    def _fix_deprecated_dimension_api(self, code: str) -> str:
        """Fix deprecated Draft.makeDimension() to modern Draft.make_linear_dimension()"""
        
        # Pattern to find old dimension API with 3 parameters
        # Old: Draft.makeDimension(p1, p2, p3)
        # New: Draft.make_linear_dimension(p1, p2)
        
        pattern = r'(\w+)\s*=\s*Draft\.makeDimension\(\s*FreeCAD\.Vector\(([^)]+)\),\s*FreeCAD\.Vector\(([^)]+)\),\s*FreeCAD\.Vector\(([^)]+)\)\s*\)'
        
        def replace_dimension(match):
            var_name = match.group(1)
            p1_coords = match.group(2)
            p2_coords = match.group(3)
            # p3 (text position) is ignored in new API
            
            replacement = f"{var_name} = Draft.make_linear_dimension(FreeCAD.Vector({p1_coords}), FreeCAD.Vector({p2_coords}))"
            return replacement
        
        fixed_code = re.sub(pattern, replace_dimension, code)
        
        # Also fix simpler patterns
        fixed_code = re.sub(r'Draft\.makeDimension\s*\(', 'Draft.make_linear_dimension(', fixed_code)
        
        # ====== CRITICAL: Fix ViewObject errors - MOST AGGRESSIVE APPROACH ======
        # Multiple different patterns to catch ALL variations of this bug
        
        # Pattern 1: Fix dim1.ViewObjectdim1.ViewObject.FontSize (most common)
        fixed_code = re.sub(r'(\w+)\.ViewObject\1\.ViewObject', r'\1.ViewObject', fixed_code)
        
        # Pattern 2: Fix dim1.ViewObjectdim2.ViewObject (cross-variable contamination)
        for _ in range(15):  # Very aggressive - 15 passes
            fixed_code = re.sub(r'\.ViewObject\w+\.ViewObject', '.ViewObject', fixed_code)
            fixed_code = re.sub(r'\.ViewObject[a-z0-9_]+\.ViewObject', '.ViewObject', fixed_code, flags=re.IGNORECASE)
        
        # Pattern 3: Fix missing newlines (dim1.ViewObjectdim2 = Draft...)
        fixed_code = re.sub(r'(\w+)\.ViewObject(\w+)\s*=\s*Draft', r'\1.ViewObject\n\2 = Draft', fixed_code)
        
        # Pattern 4: Fix whitespace concatenation (grid_line.ViewObject    grid_line.ViewObject.LineWidth)
        fixed_code = re.sub(r'(\w+)\.ViewObject\s+(\w+)\.ViewObject', r'\1.ViewObject\n    \2.ViewObject', fixed_code)
        
        # Pattern 5: Nuclear option - find any line with ViewObjectXXX.ViewObject and fix it
        lines = fixed_code.split('\n')
        fixed_lines = []
        for line in lines:
            # If line contains pattern like .ViewObject<something>.ViewObject, fix it
            if '.ViewObject' in line and line.count('.ViewObject') >= 2:
                # Replace any .ViewObject<word>.ViewObject with just .ViewObject
                line = re.sub(r'\.ViewObject[a-zA-Z0-9_]+\.ViewObject', '.ViewObject', line)
            fixed_lines.append(line)
        fixed_code = '\n'.join(fixed_lines)
        
        self.logger.info("Fixed deprecated dimension API calls and ViewObject errors")
        return fixed_code
    
    def _nuclear_viewobject_fix(self, code: str) -> str:
        """
        NUCLEAR OPTION - Final cleanup to eliminate ALL ViewObject errors
        This is called as the very last step before code is returned
        """
        self.logger.info("Running nuclear ViewObject cleanup...")
        
        # Count how many ViewObjectdimX patterns we find
        error_count = len(re.findall(r'\.ViewObject[a-zA-Z0-9_]+\.ViewObject', code))
        if error_count > 0:
            self.logger.warning(f"Found {error_count} ViewObject errors - fixing aggressively")
        
        # Strategy 1: Line-by-line replacement with simple string operations
        lines = code.split('\n')
        cleaned_lines = []
        for line in lines:
            original_line = line
            # If line has ViewObject appearing multiple times, it's probably broken
            if '.ViewObject' in line:
                viewobject_count = line.count('.ViewObject')
                if viewobject_count >= 2:
                    # Try multiple fix strategies
                    # Pattern: dim1.ViewObjectdim1.ViewObject.FontSize
                    line = line.replace('.ViewObjectdim1.ViewObject.', '.ViewObject.')
                    line = line.replace('.ViewObjectdim2.ViewObject.', '.ViewObject.')
                    line = line.replace('.ViewObjectdim3.ViewObject.', '.ViewObject.')
                    line = line.replace('.ViewObjectdim4.ViewObject.', '.ViewObject.')
                    line = line.replace('.ViewObjectdim5.ViewObject.', '.ViewObject.')
                    line = line.replace('.ViewObjectdim6.ViewObject.', '.ViewObject.')
                    line = line.replace('.ViewObjectgrid_line.ViewObject.', '.ViewObject.')
                    line = line.replace('.ViewObjectlabel.ViewObject.', '.ViewObject.')
                    
                    # Fix CRITICAL syntax error: grid_line.ViewObject    grid_line.ViewObject.LineWidth
                    # This pattern has whitespace instead of newline - causes invalid syntax
                    if re.search(r'(\w+)\.ViewObject\s{2,}(\w+)\.ViewObject', line):
                        # Split the line at the whitespace gap
                        match = re.search(r'^(\s*)(\w+)\.ViewObject\s{2,}(\w+)\.ViewObject', line)
                        if match:
                            indent = match.group(1)
                            var1 = match.group(2)
                            var2 = match.group(3)
                            # Split into two lines
                            remaining = line[match.end():]
                            cleaned_lines.append(f'{indent}{var1}.ViewObject')
                            line = f'{indent}{var2}.ViewObject{remaining}'
                            self.logger.info(f"Split whitespace error: {original_line.strip()[:60]}...")
                    
                    # Generic pattern with regex as backup
                    line = re.sub(r'\.ViewObject[a-zA-Z0-9_]+\.ViewObject', '.ViewObject', line)
                    
                    if original_line != line:
                        self.logger.info(f"Fixed line: {original_line.strip()[:60]}... -> {line.strip()[:60]}...")
            
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _fix_linestyle_errors(self, code: str) -> str:
        """
        Fix LineStyle attribute errors - LineStyle doesn't exist on all ViewObject types
        Wrap LineStyle assignments in try-except to prevent crashes
        """
        self.logger.info("Wrapping LineStyle assignments in try-except...")
        
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
                fixed_lines.append(f'{indent_str}    pass  # LineStyle not supported on this object')
                
                self.logger.info(f"Wrapped LineStyle: {line.strip()[:60]}")
            else:
                fixed_lines.append(line)
            i += 1
        
        return '\n'.join(fixed_lines)
    
    def _fix_part_makebox_usage(self, code: str) -> str:
        """Fix Part.makeBox usage that causes Label errors"""
        
        # Pattern to find Part.makeBox assignments
        pattern = r'(\w+)[ \t]*=[ \t]*Part[.]makeBox[(]([^)]+)[)]'
        
        def replace_makebox(match):
            var_name = match.group(1)
            dimensions = match.group(2)
            
            # Extract dimensions (length, width, height)
            dims = [d.strip() for d in dimensions.split(',')]
            if len(dims) >= 3:
                length, width, height = dims[0], dims[1], dims[2]
                
                # Convert to proper FreeCAD object creation
                replacement = f"""{var_name} = doc.addObject("Part::Box", "{var_name.title()}")
{var_name}.Length.Value = {length}
{var_name}.Width.Value = {width}
{var_name}.Height.Value = {height}"""
                
                return replacement
            return match.group(0)  # Return original if can't parse
        
        # Apply the replacement
        fixed_code = re.sub(pattern, replace_makebox, code)
        
        # Remove any remaining .Label assignments on variables that might be Part objects
        fixed_code = re.sub(r'(\w+)\.Label\s*=\s*["\']([^"\']+)["\']', '', fixed_code)
        
        # Remove lines that try to add Part objects directly to document
        fixed_code = re.sub(r'doc\.addObject\(["\']Part::Feature["\'],\s*\w+\)', '', fixed_code)
        
        return fixed_code
    
    def _fix_techdraw_issues(self, code: str) -> str:
        """Fix TechDraw related issues that cause argument type errors"""
        
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
        
        # Fix overlapping objects at same coordinates
        code = self._fix_overlapping_objects(code)
        
        return code
    
    def _fix_overlapping_objects(self, code: str) -> str:
        """Fix overlapping objects that create box-like scattered models"""
        
        # Detect patterns where multiple objects are placed at (0,0,0) or similar coordinates
        # This creates the "scattered boxes" problem
        
        # Look for multiple Placement assignments with same coordinates
        placement_pattern = r'\.Placement\s*=\s*FreeCAD\.Placement\(FreeCAD\.Vector\(([^)]+)\)'
        
        lines = code.split('\n')
        coordinate_usage = {}
        
        for i, line in enumerate(lines):
            match = re.search(placement_pattern, line)
            if match:
                coords = match.group(1)
                if coords in coordinate_usage:
                    coordinate_usage[coords].append(i)
                else:
                    coordinate_usage[coords] = [i]
        
        # Add warning comment for overlapping coordinates
        overlapping_coords = {coords: line_nums for coords, line_nums in coordinate_usage.items() if len(line_nums) > 1}
        
        if overlapping_coords:
            warning = "# WARNING: Multiple objects detected at same coordinates - this may create overlapping elements\n"
            warning += "# Consider using unique positioning for each architectural element\n"
            code = warning + code
        
        return code
    
    def _fix_vector_addition(self, vector_expression: str) -> str:
        """Fix vector addition with mixed units by ensuring all values are plain numbers"""
        try:
            # For now, return the original expression as it's complex to parse
            # The .Value fixes above should handle most cases
            return vector_expression
        except:
            return vector_expression
    
    def _contains_3d_objects(self, code: str) -> bool:
        """Check if code contains 3D objects instead of 2D drawings"""
        # Patterns that indicate 3D objects
        three_d_patterns = [
            r'Part\.makeBox',
            r'Part\.makeCylinder',
            r'Part\.makeSphere',
            r'Part\.makeCone',
            r'doc\.addObject\(["\']Part::Box',
            r'doc\.addObject\(["\']Part::Cylinder',
            r'doc\.addObject\(["\']Part::Sphere',
            r'doc\.addObject\(["\']Part::Cone',
            r'\.Length\.Value\s*=',  # 3D box properties
            r'\.Width\.Value\s*=',
            r'\.Height\.Value\s*=',
        ]
        
        for pattern in three_d_patterns:
            if re.search(pattern, code):
                self.logger.warning(f"Found 3D object pattern: {pattern}")
                return True
        
        return False
    
    def _has_sufficient_complexity(self, code: str) -> bool:
        """Check if generated code meets professional blueprint standards"""
        if not code:
            return False
            
        # Count ALL Draft line commands (must have MANY for detailed drawing)
        draft_lines = len(re.findall(r'Draft\.makeLine', code))
        draft_wires = len(re.findall(r'Draft\.makeWire', code))
        draft_rectangles = len(re.findall(r'Draft\.makeRectangle', code))
        draft_circles = len(re.findall(r'Draft\.makeCircle', code))
        total_drawing_commands = draft_lines + draft_wires + draft_rectangles + draft_circles
        
        # Count dimensions (MUST show all measurements) - check both old and new API
        dimensions_modern = len(re.findall(r'Draft\.make_linear_dimension', code))
        dimensions_old = len(re.findall(r'Draft\.makeDimension', code))
        dimensions = dimensions_modern + dimensions_old
        
        # Warn if using deprecated API
        if dimensions_old > 0:
            self.logger.warning(f"⚠️ Code uses DEPRECATED Draft.makeDimension() - should use Draft.make_linear_dimension()")
        
        # Count text labels (MUST label all components)
        labels = len(re.findall(r'Draft\.makeText', code))
        
        # Check for multiple views (MANDATORY: Front, Top, Side)
        view_keywords = ['# FRONT', '# TOP', '# SIDE', '# SECTION', '# PROJECTION', 'elevation', 'floor_plan', 'section']
        view_count = sum(1 for keyword in view_keywords if keyword.lower() in code.lower())
        
        # Check for grid system
        has_grid = 'grid' in code.lower() and ('Draft.makeLine' in code or 'grid_line' in code.lower())
        
        self.logger.info(f"Blueprint Quality Check:")
        self.logger.info(f"  - Drawing commands: {total_drawing_commands} (Lines: {draft_lines}, Wires: {draft_wires}, Rects: {draft_rectangles}, Circles: {draft_circles})")
        self.logger.info(f"  - Dimensions: {dimensions}")
        self.logger.info(f"  - Labels: {labels}")
        self.logger.info(f"  - Views detected: {view_count}")
        self.logger.info(f"  - Grid system: {has_grid}")
        
        # STRICT REQUIREMENTS for professional blueprints
        if total_drawing_commands < 30:
            self.logger.warning(f"❌ INSUFFICIENT DETAIL: Only {total_drawing_commands} drawing commands (need minimum 30 for complex drawings)")
            return False
        
        if dimensions < 8:
            self.logger.warning(f"❌ MISSING DIMENSIONS: Only {dimensions} dimensions (need minimum 8 to show all measurements)")
            return False
            
        if labels < 8:
            self.logger.warning(f"❌ MISSING LABELS: Only {labels} labels (need minimum 8 for component identification)")
            return False
        
        if view_count < 2:
            self.logger.warning(f"❌ SINGLE VIEW ONLY: Detected {view_count} views (need minimum 3: Front, Top, Side)")
            return False
        
        if not has_grid:
            self.logger.warning(f"❌ NO GRID SYSTEM: Professional blueprints require coordinate grid (A-F, 1-6)")
            return False
        
        self.logger.info("✅ Blueprint quality check PASSED - generating professional multi-view technical drawing")
        return True
    
    def _regenerate_as_2d_only(self, command: str, model_type: str = "2D") -> str:
        """Regenerate code with ABSOLUTE emphasis on professional blueprint standards"""
        try:
            # Add EXTREME 2D blueprint emphasis to the prompt
            enhanced_prompt = f"""
{command}

🎯 GENERATE PROFESSIONAL MULTI-VIEW BLUEPRINT - 2D TECHNICAL DRAWING ONLY

MANDATORY STRUCTURE (YOUR OUTPUT WILL BE REJECTED IF MISSING ANY):
=====================================================================
1. FRONT VIEW - Primary orthographic projection showing façade
2. TOP VIEW - Bird's eye floor plan showing layout from above  
3. SIDE/PROJECTION VIEW - Profile view showing depth and height
4. MINIMUM 30 Draft.makeLine() commands for detailed drawings
5. MINIMUM 8 Draft.makeDimension() calls showing ALL measurements
6. MINIMUM 8 Draft.makeText() labels identifying every component
7. Grid system with letters (A-F) and numbers (1-6)
8. Title block with drawing name, scale, date

EXAMPLE BLUEPRINT STRUCTURE YOU MUST FOLLOW:
```python
import FreeCAD
import Draft

doc = FreeCAD.newDocument("Blueprint")

# === FRONT VIEW (y_offset = 0) ===
# Perimeter outline
front_outline = Draft.makeWire([
    FreeCAD.Vector(0, 0, 0),
    FreeCAD.Vector(5000, 0, 0),
    FreeCAD.Vector(5000, 2400, 0),
    FreeCAD.Vector(0, 2400, 0),
    FreeCAD.Vector(0, 0, 0)
], closed=True)
front_outline.ViewObject.LineWidth = 3.0

# Internal details (doors, windows, compartments)
door1 = Draft.makeLine(FreeCAD.Vector(1000, 0, 0), FreeCAD.Vector(1900, 0, 0))
door1.ViewObject.LineWidth = 2.0

window1 = Draft.makeRectangle(800, 1200, placement=FreeCAD.Placement(FreeCAD.Vector(3000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
window1.ViewObject.LineWidth = 1.5

# Dimensions - MODERN API (FreeCAD 0.21+)
dim1 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, -500, 0),
    FreeCAD.Vector(5000, -500, 0)
)
dim1.ViewObject.LineColor = (0.0, 0.0, 0.0)
dim1.ViewObject.FontSize = 300

# === TOP VIEW (y_offset = 10000) ===
# Floor plan with rooms, furniture, fixtures
# ... minimum 15 lines showing plan details

# === SIDE VIEW (y_offset = 20000) ===
# Profile projection showing depth
# ... minimum 10 lines showing profile

# === GRID SYSTEM ===
# Grid lines every 1000mm with A,B,C labels

# === TITLE BLOCK ===
# Drawing name, scale, date
```

⚠️ ABSOLUTELY FORBIDDEN (INSTANT REJECTION):
- Part.makeBox() or ANY Part.* commands
- doc.addObject("Part::*")
- Simple single rectangle (too basic!)
- Missing views (need all 3: front, top, side)
- Missing dimensions (every measurement must be shown)
- Missing grid system

✅ ONLY USE THESE 2D COMMANDS:
- Draft.makeLine(start_vec, end_vec)
- Draft.makeWire(points_list, closed=True)
- Draft.makeRectangle(length, height, placement)
- Draft.makeCircle(radius, placement)
- Draft.makeDimension(p1, p2, p3)
- Draft.makeText(text_list, point)

Generate CONSTRUCTION-READY professional blueprint with ALL views, dimensions, labels!
"""
            
            self.logger.info("Regenerating with 2D-only emphasis...")
            
            # Call AI with enhanced prompt (using Groq)
            response = self.client.chat.completions.create(
                model=self.config.groq.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": enhanced_prompt}
                ],
                max_tokens=8000,
                temperature=0.3
            )
            
            generated_code = response.choices[0].message.content if response.choices else ""
            
            if generated_code:
                cleaned_code = self._clean_generated_code(generated_code)
                
                # Check again
                if self._contains_3d_objects(cleaned_code):
                    self.logger.error("AI still generated 3D objects after regeneration!")
                    # Return a minimal 2D example as fallback
                    return self._create_minimal_2d_example(command)
                
                return cleaned_code
            else:
                return self._create_minimal_2d_example(command)
                
        except Exception as e:
            self.logger.error(f"Regeneration failed: {e}")
            return self._create_minimal_2d_example(command)
    
    def _convert_3d_to_2d(self, code: str) -> str:
        """Convert 3D code to 2D technical drawings - just return None to force regeneration"""
        # Conversion is too complex and unreliable
        # Better to regenerate from scratch with proper 2D emphasis
        self.logger.warning("3D code detected - will force complete 2D regeneration")
        return None
    
    def _create_minimal_2d_example(self, command: str) -> str:
        """Create a minimal 2D drawing example - NOT USED ANYMORE"""
        return None  # Force proper generation instead
    
    def _validate_freecad_code(self, code: str) -> bool:
        """
        Validate generated FreeCAD code for common issues
        
        Args:
            code: Generated FreeCAD code
            
        Returns:
            True if code appears valid, False otherwise
        """
        try:
            # Check for required imports
            required_patterns = [
                r'import\s+FreeCAD',
                r'newDocument',
                r'recompute'
            ]
            
            for pattern in required_patterns:
                if not re.search(pattern, code, re.IGNORECASE):
                    self.logger.warning(f"Missing required pattern: {pattern}")
                    return False
            
            # Check for common syntax issues and deprecated patterns
            forbidden_patterns = [
                r'```',  # Markdown code blocks
                r'undefined',  # Common AI hallucination
                r'<[^>]+>',  # HTML tags
                r'Units\.setPreferredUnitSystem',  # Deprecated Units pattern
                r'Units\.setUnitSystem',  # Deprecated setUnitSystem pattern
                r'FreeCAD\.Units\.setUnitSystem',  # Deprecated FreeCAD.Units.setUnitSystem pattern
                r'Part\.makeBox',  # Causes Label errors - use doc.addObject instead
                r'\.Label\s*=',  # Setting Label on Part objects causes errors
                r'FreeCAD\.Units\.setPreferredUnitSystem',  # Another deprecated Units pattern
                r'\.ActiveMaterial',  # Deprecated material pattern
                r'\.DiffuseColor',  # Deprecated color pattern
                r'App\.setActiveDocument',  # Problematic App pattern
            ]
            
            for pattern in forbidden_patterns:
                if re.search(pattern, code):
                    self.logger.warning(f"Found problematic pattern: {pattern}")
                    return False
            
            # Basic Python syntax check
            try:
                compile(code, '<string>', 'exec')
            except SyntaxError as e:
                self.logger.warning(f"Syntax error in generated code: {e}")
                return False
            
            self.logger.info("Code validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Code validation failed: {e}")
            return False
    
    def _create_simple_bhk_model(self) -> str:
        """Create a structured architectural house model with proper room layout"""
        return '''import FreeCAD
import Part
import Draft

# Create new document
doc = FreeCAD.newDocument("Structured_2BHK_House")
print("Creating Structured 2BHK Architectural Model...")

# ==== ARCHITECTURAL SPECIFICATIONS ====
# All dimensions in millimeters
HOUSE_LENGTH = 12000      # 12m total length  
HOUSE_WIDTH = 9000        # 9m total width
WALL_HEIGHT = 3000        # 3m ceiling height
WALL_THICKNESS = 200      # 200mm walls
SLAB_THICKNESS = 150      # 150mm slab
DOOR_WIDTH = 900          # Standard door width
WINDOW_WIDTH = 1200       # Standard window width
WINDOW_HEIGHT = 1200      # Standard window height

# ==== STEP 1: CREATE FOUNDATION & FLOOR ====
print("Step 1: Creating Foundation System...")

# Foundation
foundation = Part.makeBox(HOUSE_LENGTH + 400, HOUSE_WIDTH + 400, 500)
foundation = foundation.translate(FreeCAD.Vector(-200, -200, -500))
foundation_obj = doc.addObject("Part::Feature", "Foundation")
foundation_obj.Shape = foundation
foundation_obj.ViewObject.ShapeColor = (0.4, 0.4, 0.4)  # Dark gray
foundation_obj.Label = "Foundation"

# Floor Slab
floor_slab = Part.makeBox(HOUSE_LENGTH, HOUSE_WIDTH, SLAB_THICKNESS)
floor_obj = doc.addObject("Part::Feature", "Floor_Slab")
floor_obj.Shape = floor_slab
floor_obj.ViewObject.ShapeColor = (0.8, 0.75, 0.7)  # Light brown
floor_obj.Label = "Floor"

# ==== STEP 2: CREATE EXTERIOR WALLS WITH OPENINGS ====
print("Step 2: Creating Exterior Wall System...")

def create_wall_with_openings(length, width, height, openings=None):
    """Create a wall with door/window openings"""
    wall = Part.makeBox(length, width, height)
    
    if openings:
        for opening in openings:
            opening_box = Part.makeBox(
                opening['width'], 
                width + 100,  # Cut through wall
                opening['height']
            )
            opening_box = opening_box.translate(FreeCAD.Vector(
                opening['x'], 
                -50, 
                opening['z']
            ))
            wall = wall.cut(opening_box)
    
    return wall

# Front Wall (South) with Main Door and Window
front_openings = [
    {'x': 5000, 'z': 0, 'width': DOOR_WIDTH, 'height': 2100},  # Main door
    {'x': 8000, 'z': 1000, 'width': WINDOW_WIDTH, 'height': WINDOW_HEIGHT}  # Window
]
front_wall = create_wall_with_openings(HOUSE_LENGTH, WALL_THICKNESS, WALL_HEIGHT, front_openings)
front_wall = front_wall.translate(FreeCAD.Vector(0, 0, SLAB_THICKNESS))
front_obj = doc.addObject("Part::Feature", "Front_Wall")
front_obj.Shape = front_wall
front_obj.ViewObject.ShapeColor = (0.9, 0.85, 0.8)  # Cream
front_obj.Label = "Front Wall (Main Entrance)"

# Back Wall (North) with Kitchen Window
back_openings = [
    {'x': 2000, 'z': 1000, 'width': WINDOW_WIDTH, 'height': WINDOW_HEIGHT},  # Kitchen window
    {'x': 9000, 'z': 1000, 'width': WINDOW_WIDTH, 'height': WINDOW_HEIGHT}   # Bedroom window
]
back_wall = create_wall_with_openings(HOUSE_LENGTH, WALL_THICKNESS, WALL_HEIGHT, back_openings)
back_wall = back_wall.translate(FreeCAD.Vector(0, HOUSE_WIDTH - WALL_THICKNESS, SLAB_THICKNESS))
back_obj = doc.addObject("Part::Feature", "Back_Wall")
back_obj.Shape = back_wall
back_obj.ViewObject.ShapeColor = (0.9, 0.85, 0.8)
back_obj.Label = "Back Wall"

# Left Wall (East) with Living Room Window
left_openings = [
    {'x': 0, 'z': 1000, 'width': WALL_THICKNESS + 100, 'height': WINDOW_HEIGHT}  # Living room window
]
# Special handling for side wall (rotate opening)
left_wall = Part.makeBox(WALL_THICKNESS, HOUSE_WIDTH, WALL_HEIGHT)
# Cut window opening
window_cut = Part.makeBox(WALL_THICKNESS + 100, WINDOW_WIDTH, WINDOW_HEIGHT)
window_cut = window_cut.translate(FreeCAD.Vector(-50, 3000, SLAB_THICKNESS + 1000))
left_wall = left_wall.cut(window_cut)
left_wall = left_wall.translate(FreeCAD.Vector(0, 0, SLAB_THICKNESS))
left_obj = doc.addObject("Part::Feature", "Left_Wall")
left_obj.Shape = left_wall
left_obj.ViewObject.ShapeColor = (0.9, 0.85, 0.8)
left_obj.Label = "Left Wall"

# Right Wall (West) with Bedroom Window
right_wall = Part.makeBox(WALL_THICKNESS, HOUSE_WIDTH, WALL_HEIGHT)
# Cut bedroom window
bedroom_window = Part.makeBox(WALL_THICKNESS + 100, WINDOW_WIDTH, WINDOW_HEIGHT)
bedroom_window = bedroom_window.translate(FreeCAD.Vector(-50, 6000, SLAB_THICKNESS + 1000))
right_wall = right_wall.cut(bedroom_window)
right_wall = right_wall.translate(FreeCAD.Vector(HOUSE_LENGTH - WALL_THICKNESS, 0, SLAB_THICKNESS))
right_obj = doc.addObject("Part::Feature", "Right_Wall")
right_obj.Shape = right_wall
right_obj.ViewObject.ShapeColor = (0.9, 0.85, 0.8)
right_obj.Label = "Right Wall"

# ==== STEP 3: CREATE INTERIOR WALLS WITH DOORS ====
print("Step 3: Creating Interior Partition Walls...")

# Horizontal Wall separating Living Room from Bedrooms (with corridor door)
main_partition = Part.makeBox(HOUSE_LENGTH - 2*WALL_THICKNESS, WALL_THICKNESS, WALL_HEIGHT)
# Cut corridor door opening
corridor_door = Part.makeBox(DOOR_WIDTH, WALL_THICKNESS + 100, 2100)
corridor_door = corridor_door.translate(FreeCAD.Vector(5000, -50, 0))
main_partition = main_partition.cut(corridor_door)
main_partition = main_partition.translate(FreeCAD.Vector(WALL_THICKNESS, 6000, SLAB_THICKNESS))
main_partition_obj = doc.addObject("Part::Feature", "Main_Partition")
main_partition_obj.Shape = main_partition
main_partition_obj.ViewObject.ShapeColor = (0.85, 0.8, 0.75)
main_partition_obj.Label = "Living-Bedroom Partition"

# Vertical Wall separating Master Bedroom from Second Bedroom (with doors)
bedroom_separator = Part.makeBox(WALL_THICKNESS, HOUSE_WIDTH - 6000 - WALL_THICKNESS, WALL_HEIGHT)
# Cut Master Bedroom door
master_door = Part.makeBox(WALL_THICKNESS + 100, DOOR_WIDTH, 2100)
master_door = master_door.translate(FreeCAD.Vector(-50, 500, 0))
bedroom_separator = bedroom_separator.cut(master_door)
# Cut Second Bedroom door  
second_door = Part.makeBox(WALL_THICKNESS + 100, DOOR_WIDTH, 2100)
second_door = second_door.translate(FreeCAD.Vector(-50, 2000, 0))
bedroom_separator = bedroom_separator.cut(second_door)
bedroom_separator = bedroom_separator.translate(FreeCAD.Vector(6000, 6000 + WALL_THICKNESS, SLAB_THICKNESS))
bedroom_separator_obj = doc.addObject("Part::Feature", "Bedroom_Separator")
bedroom_separator_obj.Shape = bedroom_separator
bedroom_separator_obj.ViewObject.ShapeColor = (0.85, 0.8, 0.75)
bedroom_separator_obj.Label = "Bedroom Separator Wall"

# Kitchen Wall (separating kitchen from living room with door)
kitchen_wall = Part.makeBox(WALL_THICKNESS, 3000, WALL_HEIGHT)
# Cut kitchen door
kitchen_door = Part.makeBox(WALL_THICKNESS + 100, DOOR_WIDTH, 2100)
kitchen_door = kitchen_door.translate(FreeCAD.Vector(-50, 1500, 0))
kitchen_wall = kitchen_wall.cut(kitchen_door)
kitchen_wall = kitchen_wall.translate(FreeCAD.Vector(3000, WALL_THICKNESS, SLAB_THICKNESS))
kitchen_obj = doc.addObject("Part::Feature", "Kitchen_Wall")
kitchen_obj.Shape = kitchen_wall
kitchen_obj.ViewObject.ShapeColor = (0.85, 0.8, 0.75)
kitchen_obj.Label = "Kitchen Wall"

# Bathroom Wall (with door)
bathroom_wall = Part.makeBox(2500, WALL_THICKNESS, WALL_HEIGHT)
# Cut bathroom door
bathroom_door = Part.makeBox(DOOR_WIDTH, WALL_THICKNESS + 100, 2100)
bathroom_door = bathroom_door.translate(FreeCAD.Vector(500, -50, 0))
bathroom_wall = bathroom_wall.cut(bathroom_door)
bathroom_wall = bathroom_wall.translate(FreeCAD.Vector(WALL_THICKNESS, 3500, SLAB_THICKNESS))
bathroom_obj = doc.addObject("Part::Feature", "Bathroom_Wall")
bathroom_obj.Shape = bathroom_wall
bathroom_obj.ViewObject.ShapeColor = (0.8, 0.85, 0.9)  # Light blue for bathroom
bathroom_obj.Label = "Bathroom Wall"

# ==== STEP 4: CREATE ROOF AND ARCHITECTURAL FEATURES ====
print("Step 4: Creating Roof Structure...")

# Main Roof Slab
roof_slab = Part.makeBox(HOUSE_LENGTH, HOUSE_WIDTH, SLAB_THICKNESS)
roof_slab = roof_slab.translate(FreeCAD.Vector(0, 0, WALL_HEIGHT + SLAB_THICKNESS))
roof_obj = doc.addObject("Part::Feature", "Roof_Slab")
roof_obj.Shape = roof_slab
roof_obj.ViewObject.ShapeColor = (0.6, 0.4, 0.3)  # Terracotta roof
roof_obj.Label = "Roof Slab"

# Create Room Labels as Text (conceptual room areas)
print("Step 5: Defining Room Areas...")

# Living Room area indicator
living_area = Part.makeBox(5500, 3500, 50)
living_area = living_area.translate(FreeCAD.Vector(500, 500, SLAB_THICKNESS + 1))
living_obj = doc.addObject("Part::Feature", "Living_Room")
living_obj.Shape = living_area
living_obj.ViewObject.ShapeColor = (0.9, 0.9, 0.7)  # Light yellow
living_obj.Label = "Living Room (19.25 sq.m)"

# Kitchen area indicator  
kitchen_area = Part.makeBox(2500, 2500, 50)
kitchen_area = kitchen_area.translate(FreeCAD.Vector(500, 4000, SLAB_THICKNESS + 1))
kitchen_obj = doc.addObject("Part::Feature", "Kitchen")
kitchen_obj.Shape = kitchen_area
kitchen_obj.ViewObject.ShapeColor = (0.7, 0.9, 0.7)  # Light green
kitchen_obj.Label = "Kitchen (6.25 sq.m)"

# Master Bedroom area indicator
master_area = Part.makeBox(5500, 2500, 50)
master_area = master_area.translate(FreeCAD.Vector(500, 6500, SLAB_THICKNESS + 1))
master_obj = doc.addObject("Part::Feature", "Master_Bedroom")
master_obj.Shape = master_area
master_obj.ViewObject.ShapeColor = (0.9, 0.7, 0.7)  # Light pink
master_obj.Label = "Master Bedroom (13.75 sq.m)"

# Second Bedroom area indicator
second_area = Part.makeBox(5500, 2000, 50)
second_area = second_area.translate(FreeCAD.Vector(6500, 6500, SLAB_THICKNESS + 1))
second_obj = doc.addObject("Part::Feature", "Second_Bedroom") 
second_obj.Shape = second_area
second_obj.ViewObject.ShapeColor = (0.7, 0.7, 0.9)  # Light blue
second_obj.Label = "Second Bedroom (11 sq.m)"

# Bathroom area indicator
bathroom_area = Part.makeBox(2000, 2000, 50)
bathroom_area = bathroom_area.translate(FreeCAD.Vector(1000, 1500, SLAB_THICKNESS + 1))
bathroom_obj = doc.addObject("Part::Feature", "Bathroom")
bathroom_obj.Shape = bathroom_area  
bathroom_obj.ViewObject.ShapeColor = (0.7, 0.9, 0.9)  # Light cyan
bathroom_obj.Label = "Bathroom (4 sq.m)"

# ==== STEP 6: ADD ARCHITECTURAL DETAILS ====
print("Step 6: Adding Architectural Features...")

# Main Entrance Canopy
canopy = Part.makeBox(2000, 800, 150)
canopy = canopy.translate(FreeCAD.Vector(4500, -800, WALL_HEIGHT + SLAB_THICKNESS + 200))
canopy_obj = doc.addObject("Part::Feature", "Entrance_Canopy")
canopy_obj.Shape = canopy
canopy_obj.ViewObject.ShapeColor = (0.5, 0.3, 0.2)  # Dark brown
canopy_obj.Label = "Entrance Canopy"

# Door Frames (as thin boxes)
# Main Door Frame
main_door_frame = Part.makeBox(DOOR_WIDTH + 200, 100, 2200)
main_door_frame = main_door_frame.translate(FreeCAD.Vector(4900, -50, SLAB_THICKNESS))
main_door_obj = doc.addObject("Part::Feature", "Main_Door_Frame")
main_door_obj.Shape = main_door_frame
main_door_obj.ViewObject.ShapeColor = (0.4, 0.2, 0.1)  # Dark wood
main_door_obj.Label = "Main Door Frame"

# Window Frames 
window_frame1 = Part.makeBox(WINDOW_WIDTH + 200, 100, WINDOW_HEIGHT + 200)
window_frame1 = window_frame1.translate(FreeCAD.Vector(7900, -50, SLAB_THICKNESS + 900))
window1_obj = doc.addObject("Part::Feature", "Front_Window_Frame")
window1_obj.Shape = window_frame1
window1_obj.ViewObject.ShapeColor = (0.3, 0.3, 0.3)  # Gray aluminum
window1_obj.Label = "Front Window Frame"

# Recompute the document to update all objects
doc.recompute()

# Set professional isometric view
try:
    if hasattr(FreeCAD, 'Gui') and FreeCAD.Gui:
        FreeCAD.Gui.SendMsgToActiveView("ViewFit")
        FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
        # Zoom to fit all objects
        FreeCAD.Gui.SendMsgToActiveView("ViewFit")
except:
    pass

# ==== ARCHITECTURAL MODEL SUMMARY ====
print("\\n" + "="*50)
print("STRUCTURED 2BHK HOUSE - ARCHITECTURAL MODEL")
print("="*50)
print("BUILDING SPECIFICATIONS:")
print(f"- Total Area: {(HOUSE_LENGTH * HOUSE_WIDTH)/1000000:.1f} sq.m")
print(f"- Overall Dimensions: {HOUSE_LENGTH/1000:.1f}m x {HOUSE_WIDTH/1000:.1f}m")
print(f"- Ceiling Height: {WALL_HEIGHT/1000:.1f}m")
print(f"- Wall Thickness: {WALL_THICKNESS}mm")
print("\\nROOM DETAILS:")
print("Living Room: 5.5m x 3.5m (19.25 sq.m)")
print("- Kitchen: 2.5m x 2.5m (6.25 sq.m)")  
print("- Master Bedroom: 5.5m x 2.5m (13.75 sq.m)")
print("- Second Bedroom: 5.5m x 2.0m (11.0 sq.m)")
print("- Bathroom: 2.0m x 2.0m (4.0 sq.m)")
print("\\nSTRUCTURAL FEATURES:")
print("- Foundation with proper depth")
print("- Load-bearing brick walls with openings")
print("- Doors: 900mm wide standard doors")
print("- Windows: 1200mm x 1200mm with frames")
print("- RCC roof slab with proper thickness")
print("- Room area indicators for clear visualization")
print("\\nARCHITECTURAL ELEMENTS:")
print("- Main entrance with canopy")
print("- Door and window frames")
print("- Proper wall openings for natural light")
print("- Color-coded room identification")
print("- Professional structural layout")
print("="*50)
print("STRUCTURED MODEL COMPLETE - Ready for Review!")
'''

    def _create_simple_cube(self) -> str:
        """Create a simple cube model"""
        return '''import FreeCAD
import Part

# Create new document
doc = FreeCAD.newDocument("Simple_Cube")

# Create a simple cube
cube = Part.makeBox(1000, 1000, 1000)  # 1m x 1m x 1m cube
cube_obj = doc.addObject("Part::Feature", "Cube")
cube_obj.Shape = cube

# Recompute the document
doc.recompute()

print("Simple cube created successfully!")
'''

    def _create_school_model(self) -> str:
        """Create a structured school building model with proper educational layout"""
        return '''import FreeCAD
import Part

# Create new document
doc = FreeCAD.newDocument("Structured_School_Building")
print("Creating Structured School Architectural Model...")

# ==== SCHOOL ARCHITECTURAL SPECIFICATIONS ====
# All dimensions in millimeters
SCHOOL_LENGTH = 50000     # 50m total length  
SCHOOL_WIDTH = 30000      # 30m total width
FLOOR_HEIGHT = 3500       # 3.5m ceiling height (school standard)
WALL_THICKNESS = 250      # 250mm walls (institutional standard)
SLAB_THICKNESS = 200      # 200mm slab
CORRIDOR_WIDTH = 3000     # 3m wide corridors
DOOR_WIDTH = 1000         # 1m doors (institutional)
WINDOW_WIDTH = 1500       # 1.5m windows
WINDOW_HEIGHT = 1500      # 1.5m windows

print("School Building Specifications:")
print(f"- Total Built-up Area: {(SCHOOL_LENGTH * SCHOOL_WIDTH) / 1000000:.1f} sq.m")
print(f"- Building Dimensions: {SCHOOL_LENGTH/1000:.1f}m x {SCHOOL_WIDTH/1000:.1f}m")
print(f"- Floor Height: {FLOOR_HEIGHT/1000:.1f}m (Educational Standard)")

# ==== STEP 1: CREATE FOUNDATION & FLOOR ====
print("Step 1: Creating Foundation System...")

# Foundation
foundation = Part.makeBox(SCHOOL_LENGTH + 1000, SCHOOL_WIDTH + 1000, 800)
foundation = foundation.translate(FreeCAD.Vector(-500, -500, -800))
foundation_obj = doc.addObject("Part::Feature", "Foundation")
foundation_obj.Shape = foundation
foundation_obj.ViewObject.ShapeColor = (0.4, 0.4, 0.4)  # Dark gray
foundation_obj.Label = "School Foundation"

# Ground Floor Slab
floor_slab = Part.makeBox(SCHOOL_LENGTH, SCHOOL_WIDTH, SLAB_THICKNESS)
floor_obj = doc.addObject("Part::Feature", "Ground_Floor")
floor_obj.Shape = floor_slab
floor_obj.ViewObject.ShapeColor = (0.8, 0.8, 0.75)  # Light concrete
floor_obj.Label = "Ground Floor"

# ==== STEP 2: CREATE EXTERIOR WALLS ====
print("Step 2: Creating Exterior Wall System...")

def create_wall_with_openings(length, width, height, openings=None):
    """Create a wall with door/window openings"""
    wall = Part.makeBox(length, width, height)
    
    if openings:
        for opening in openings:
            opening_box = Part.makeBox(
                opening['width'], 
                width + 100,  # Cut through wall
                opening['height']
            )
            opening_box = opening_box.translate(FreeCAD.Vector(
                opening['x'], 
                -50, 
                opening['z']
            ))
            wall = wall.cut(opening_box)
    
    return wall

# Front Wall with Main Entrance and Windows
front_openings = [
    {'x': 24000, 'z': 0, 'width': 2000, 'height': 2500},  # Main entrance (double door)
    {'x': 5000, 'z': 1000, 'width': WINDOW_WIDTH, 'height': WINDOW_HEIGHT},   # Window 1
    {'x': 10000, 'z': 1000, 'width': WINDOW_WIDTH, 'height': WINDOW_HEIGHT},  # Window 2
    {'x': 15000, 'z': 1000, 'width': WINDOW_WIDTH, 'height': WINDOW_HEIGHT},  # Window 3
    {'x': 35000, 'z': 1000, 'width': WINDOW_WIDTH, 'height': WINDOW_HEIGHT},  # Window 4
    {'x': 40000, 'z': 1000, 'width': WINDOW_WIDTH, 'height': WINDOW_HEIGHT},  # Window 5
]
front_wall = create_wall_with_openings(SCHOOL_LENGTH, WALL_THICKNESS, FLOOR_HEIGHT, front_openings)
front_wall = front_wall.translate(FreeCAD.Vector(0, 0, SLAB_THICKNESS))
front_obj = doc.addObject("Part::Feature", "Front_Wall")
front_obj.Shape = front_wall
front_obj.ViewObject.ShapeColor = (0.9, 0.88, 0.85)  # Light cream
front_obj.Label = "School Front Wall"

# Back Wall with Emergency Exits and Windows
back_openings = [
    {'x': 10000, 'z': 0, 'width': DOOR_WIDTH, 'height': 2100},  # Emergency exit 1
    {'x': 30000, 'z': 0, 'width': DOOR_WIDTH, 'height': 2100},  # Emergency exit 2
    {'x': 5000, 'z': 1000, 'width': WINDOW_WIDTH, 'height': WINDOW_HEIGHT},   # Window 1
    {'x': 20000, 'z': 1000, 'width': WINDOW_WIDTH, 'height': WINDOW_HEIGHT},  # Window 2
    {'x': 35000, 'z': 1000, 'width': WINDOW_WIDTH, 'height': WINDOW_HEIGHT},  # Window 3
]
back_wall = create_wall_with_openings(SCHOOL_LENGTH, WALL_THICKNESS, FLOOR_HEIGHT, back_openings)
back_wall = back_wall.translate(FreeCAD.Vector(0, SCHOOL_WIDTH - WALL_THICKNESS, SLAB_THICKNESS))
back_obj = doc.addObject("Part::Feature", "Back_Wall")
back_obj.Shape = back_wall
back_obj.ViewObject.ShapeColor = (0.9, 0.88, 0.85)
back_obj.Label = "School Back Wall"

# Left Wall with Windows
left_wall = Part.makeBox(WALL_THICKNESS, SCHOOL_WIDTH, FLOOR_HEIGHT)
# Cut multiple windows
for i, y_pos in enumerate([5000, 10000, 15000, 20000, 25000]):
    window_cut = Part.makeBox(WALL_THICKNESS + 100, WINDOW_WIDTH, WINDOW_HEIGHT)
    window_cut = window_cut.translate(FreeCAD.Vector(-50, y_pos, SLAB_THICKNESS + 1000))
    left_wall = left_wall.cut(window_cut)
left_wall = left_wall.translate(FreeCAD.Vector(0, 0, SLAB_THICKNESS))
left_obj = doc.addObject("Part::Feature", "Left_Wall")
left_obj.Shape = left_wall
left_obj.ViewObject.ShapeColor = (0.9, 0.88, 0.85)
left_obj.Label = "School Left Wall"

# Right Wall with Windows
right_wall = Part.makeBox(WALL_THICKNESS, SCHOOL_WIDTH, FLOOR_HEIGHT)
# Cut multiple windows
for i, y_pos in enumerate([5000, 10000, 15000, 20000, 25000]):
    window_cut = Part.makeBox(WALL_THICKNESS + 100, WINDOW_WIDTH, WINDOW_HEIGHT)
    window_cut = window_cut.translate(FreeCAD.Vector(-50, y_pos, SLAB_THICKNESS + 1000))
    right_wall = right_wall.cut(window_cut)
right_wall = right_wall.translate(FreeCAD.Vector(SCHOOL_LENGTH - WALL_THICKNESS, 0, SLAB_THICKNESS))
right_obj = doc.addObject("Part::Feature", "Right_Wall")
right_obj.Shape = right_wall
right_obj.ViewObject.ShapeColor = (0.9, 0.88, 0.85)
right_obj.Label = "School Right Wall"

# ==== STEP 3: CREATE INTERIOR PARTITIONS ====
print("Step 3: Creating Interior Educational Spaces...")

# Central Corridor Wall
corridor_wall = Part.makeBox(SCHOOL_LENGTH - 2*WALL_THICKNESS, WALL_THICKNESS, FLOOR_HEIGHT)
# Cut doors for classroom access
door_positions = [5000, 12000, 19000, 26000, 33000, 40000]
for pos in door_positions:
    corridor_door = Part.makeBox(DOOR_WIDTH, WALL_THICKNESS + 100, 2100)
    corridor_door = corridor_door.translate(FreeCAD.Vector(pos, -50, 0))
    corridor_wall = corridor_wall.cut(corridor_door)
corridor_wall = corridor_wall.translate(FreeCAD.Vector(WALL_THICKNESS, 15000, SLAB_THICKNESS))
corridor_obj = doc.addObject("Part::Feature", "Central_Corridor_Wall")
corridor_obj.Shape = corridor_wall
corridor_obj.ViewObject.ShapeColor = (0.85, 0.82, 0.78)
corridor_obj.Label = "Central Corridor Wall"

# Classroom Divider Walls (North Side)
classroom_positions = [8000, 15000, 22000, 29000, 36000]
for i, pos in enumerate(classroom_positions):
    divider_wall = Part.makeBox(WALL_THICKNESS, 12000, FLOOR_HEIGHT)
    divider_wall = divider_wall.translate(FreeCAD.Vector(pos, WALL_THICKNESS, SLAB_THICKNESS))
    divider_obj = doc.addObject("Part::Feature", f"Classroom_Divider_{i+1}")
    divider_obj.Shape = divider_wall
    divider_obj.ViewObject.ShapeColor = (0.88, 0.85, 0.80)
    divider_obj.Label = f"Classroom Divider {i+1}"

# Classroom Divider Walls (South Side)
for i, pos in enumerate(classroom_positions):
    divider_wall = Part.makeBox(WALL_THICKNESS, 12000, FLOOR_HEIGHT)
    divider_wall = divider_wall.translate(FreeCAD.Vector(pos, 18000, SLAB_THICKNESS))
    divider_obj = doc.addObject("Part::Feature", f"South_Classroom_Divider_{i+1}")
    divider_obj.Shape = divider_wall
    divider_obj.ViewObject.ShapeColor = (0.88, 0.85, 0.80)
    divider_obj.Label = f"South Classroom Divider {i+1}"

# ==== STEP 4: CREATE ROOF STRUCTURE ====
print("Step 4: Creating Roof Structure...")

# Main Roof Slab
roof_slab = Part.makeBox(SCHOOL_LENGTH, SCHOOL_WIDTH, SLAB_THICKNESS)
roof_slab = roof_slab.translate(FreeCAD.Vector(0, 0, FLOOR_HEIGHT + SLAB_THICKNESS))
roof_obj = doc.addObject("Part::Feature", "School_Roof")
roof_obj.Shape = roof_slab
roof_obj.ViewObject.ShapeColor = (0.6, 0.5, 0.4)  # Brown roof
roof_obj.Label = "School Roof"

# ==== STEP 5: CREATE EDUCATIONAL SPACES ====
print("Step 5: Defining Educational Areas...")

# Reception/Entrance Hall
reception_area = Part.makeBox(8000, 12000, 100)
reception_area = reception_area.translate(FreeCAD.Vector(21000, 1500, SLAB_THICKNESS + 1))
reception_obj = doc.addObject("Part::Feature", "Reception_Hall")
reception_obj.Shape = reception_area
reception_obj.ViewObject.ShapeColor = (0.9, 0.9, 0.8)  # Light yellow
reception_obj.Label = "Reception Hall (96 sq.m)"

# Principal Office
principal_office = Part.makeBox(6000, 5000, 100)
principal_office = principal_office.translate(FreeCAD.Vector(1000, 1000, SLAB_THICKNESS + 1))
principal_obj = doc.addObject("Part::Feature", "Principal_Office")
principal_obj.Shape = principal_office
principal_obj.ViewObject.ShapeColor = (0.8, 0.7, 0.9)  # Light purple
principal_obj.Label = "Principal Office (30 sq.m)"

# Staff Room
staff_room = Part.makeBox(8000, 6000, 100)
staff_room = staff_room.translate(FreeCAD.Vector(9000, 1000, SLAB_THICKNESS + 1))
staff_obj = doc.addObject("Part::Feature", "Staff_Room")
staff_obj.Shape = staff_room
staff_obj.ViewObject.ShapeColor = (0.7, 0.9, 0.7)  # Light green
staff_obj.Label = "Staff Room (48 sq.m)"

# Classrooms (North Side)
classroom_names = ["Class_1A", "Class_1B", "Class_2A", "Class_2B", "Class_3A"]
classroom_colors = [(0.9, 0.7, 0.7), (0.7, 0.9, 0.7), (0.7, 0.7, 0.9), (0.9, 0.9, 0.7), (0.9, 0.7, 0.9)]
for i, (name, color) in enumerate(zip(classroom_names, classroom_colors)):
    x_pos = 1000 + i * 8000
    classroom_area = Part.makeBox(7000, 12000, 100)
    classroom_area = classroom_area.translate(FreeCAD.Vector(x_pos, 1500, SLAB_THICKNESS + 1))
    classroom_obj = doc.addObject("Part::Feature", name)
    classroom_obj.Shape = classroom_area
    classroom_obj.ViewObject.ShapeColor = color
    classroom_obj.Label = f"{name.replace('_', ' ')} (84 sq.m)"

# Library
library_area = Part.makeBox(12000, 10000, 100)
library_area = library_area.translate(FreeCAD.Vector(30000, 18500, SLAB_THICKNESS + 1))
library_obj = doc.addObject("Part::Feature", "Library")
library_obj.Shape = library_area
library_obj.ViewObject.ShapeColor = (0.8, 0.9, 0.9)  # Light cyan
library_obj.Label = "Library (120 sq.m)"

# Computer Lab
computer_lab = Part.makeBox(10000, 8000, 100)
computer_lab = computer_lab.translate(FreeCAD.Vector(16000, 18500, SLAB_THICKNESS + 1))
computer_obj = doc.addObject("Part::Feature", "Computer_Lab")
computer_obj.Shape = computer_lab
computer_obj.ViewObject.ShapeColor = (0.9, 0.8, 0.7)  # Light orange
computer_obj.Label = "Computer Lab (80 sq.m)"

# Science Laboratory
science_lab = Part.makeBox(9000, 8000, 100)
science_lab = science_lab.translate(FreeCAD.Vector(1000, 18500, SLAB_THICKNESS + 1))
science_obj = doc.addObject("Part::Feature", "Science_Lab")
science_obj.Shape = science_lab
science_obj.ViewObject.ShapeColor = (0.7, 0.8, 0.9)  # Light blue
science_obj.Label = "Science Lab (72 sq.m)"

# ==== STEP 6: ADD ARCHITECTURAL FEATURES ====
print("Step 6: Adding School Architectural Features...")

# Main Entrance Canopy
entrance_canopy = Part.makeBox(4000, 1500, 200)
entrance_canopy = entrance_canopy.translate(FreeCAD.Vector(23000, -1500, FLOOR_HEIGHT + SLAB_THICKNESS + 300))
canopy_obj = doc.addObject("Part::Feature", "Main_Entrance_Canopy")
canopy_obj.Shape = entrance_canopy
canopy_obj.ViewObject.ShapeColor = (0.5, 0.3, 0.2)  # Dark brown
canopy_obj.Label = "Main Entrance Canopy"

# School Sign Board
sign_board = Part.makeBox(6000, 200, 1000)
sign_board = sign_board.translate(FreeCAD.Vector(22000, -300, FLOOR_HEIGHT + 500))
sign_obj = doc.addObject("Part::Feature", "School_Sign")
sign_obj.Shape = sign_board
sign_obj.ViewObject.ShapeColor = (0.2, 0.4, 0.8)  # School blue
sign_obj.Label = "School Name Board"

# Recompute the document
doc.recompute()

# Set professional isometric view
try:
    if hasattr(FreeCAD, 'Gui') and FreeCAD.Gui:
        FreeCAD.Gui.SendMsgToActiveView("ViewFit")
        FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
        FreeCAD.Gui.SendMsgToActiveView("ViewFit")
except:
    pass

# ==== SCHOOL BUILDING SUMMARY ====
print("\\n" + "="*60)
print("STRUCTURED SCHOOL BUILDING - EDUCATIONAL ARCHITECTURE")
print("="*60)
print("BUILDING SPECIFICATIONS:")
print(f"- Total Built-up Area: {(SCHOOL_LENGTH * SCHOOL_WIDTH)/1000000:.1f} sq.m")
print(f"- Building Dimensions: {SCHOOL_LENGTH/1000:.1f}m x {SCHOOL_WIDTH/1000:.1f}m")
print(f"- Floor Height: {FLOOR_HEIGHT/1000:.1f}m (Educational Standard)")
print(f"- Wall Thickness: {WALL_THICKNESS}mm (Institutional Grade)")
print("\\nEDUCATIONAL FACILITIES:")
print("- Reception Hall: 8m x 12m (96 sq.m)")
print("- Principal Office: 6m x 5m (30 sq.m)")  
print("- Staff Room: 8m x 6m (48 sq.m)")
print("- 5 Classrooms: 7m x 12m each (84 sq.m each)")
print("- Library: 12m x 10m (120 sq.m)")
print("- Computer Lab: 10m x 8m (80 sq.m)")
print("- Science Laboratory: 9m x 8m (72 sq.m)")
print("- Central Corridor: 3m wide (Accessibility compliant)")
print("\\nSTRUCTURAL FEATURES:")
print("- Reinforced foundation for institutional load")
print("- Load-bearing walls with proper openings")
print("- Large windows for natural lighting")
print("- Multiple emergency exits")
print("- Wide corridors for student movement")
print("- Professional educational layout")
print("\\nSAFETY & COMPLIANCE:")
print("- Fire safety exits and wide corridors")
print("- Accessibility compliant design")
print("- Natural lighting in all classrooms")
print("- Proper ventilation systems")
print("- Emergency exit provisions")
print("="*60)
print("EDUCATIONAL BUILDING COMPLETE - Ready for Academic Use!")
'''
    
    def get_model_suggestions(self, partial_description: str) -> List[str]:
        """
        Get AI-powered suggestions for model descriptions
        
        Args:
            partial_description: Partial model description
            
        Returns:
            List of suggested completions
        """
        if not self.client:
            return []
            
        try:
            prompt = f"""
            Based on this partial CAD model description: "{partial_description}"
            
            Provide 3-5 professional completion suggestions that would result in detailed, 
            realistic FreeCAD models. Focus on:
            - Architectural elements and buildings
            - Mechanical components and assemblies
            - Industrial designs and products
            - Technical objects with specific dimensions
            
            Return only the completed descriptions, one per line.
            """
            
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            
            if response and response.choices:
                suggestions_text = response.choices[0].message.content
                suggestions = [s.strip() for s in suggestions_text.split('\n') if s.strip()]
                return suggestions[:5]  # Limit to 5 suggestions
                
        except Exception as e:
            self.logger.error(f"Failed to get model suggestions: {e}")
            
        return []
    
    def analyze_command_complexity(self, command: str) -> Dict[str, Any]:
        """
        Analyze command complexity and provide generation estimates
        
        Args:
            command: Model description command
            
        Returns:
            Dictionary with complexity analysis
        """
        try:
            # Simple complexity analysis based on keywords and length
            architectural_keywords = ['house', 'building', 'room', 'bhk', 'apartment', 'floor']
            mechanical_keywords = ['gear', 'shaft', 'bearing', 'valve', 'pump', 'engine']
            complex_keywords = ['assembly', 'multiple', 'detailed', 'complex', 'advanced']
            
            command_lower = command.lower()
            word_count = len(command.split())
            
            # Calculate complexity score
            complexity_score = 0
            complexity_factors = []
            
            if word_count > 50:
                complexity_score += 3
                complexity_factors.append("Long description")
            elif word_count > 25:
                complexity_score += 2
                complexity_factors.append("Detailed description")
            
            if any(kw in command_lower for kw in architectural_keywords):
                complexity_score += 2
                complexity_factors.append("Architectural model")
            
            if any(kw in command_lower for kw in mechanical_keywords):
                complexity_score += 2
                complexity_factors.append("Mechanical component")
            
            if any(kw in command_lower for kw in complex_keywords):
                complexity_score += 3
                complexity_factors.append("Complex assembly")
            
            # Determine complexity level
            if complexity_score <= 2:
                complexity_level = "Simple"
                estimated_time = "1-2 minutes"
                estimated_lines = 50
            elif complexity_score <= 5:
                complexity_level = "Moderate"  
                estimated_time = "2-4 minutes"
                estimated_lines = 100
            else:
                complexity_level = "Complex"
                estimated_time = "4-8 minutes"
                estimated_lines = 200
            
            return {
                "complexity_level": complexity_level,
                "complexity_score": complexity_score,
                "factors": complexity_factors,
                "estimated_generation_time": estimated_time,
                "estimated_code_lines": estimated_lines,
                "word_count": word_count,
                "recommended_quality": "professional" if complexity_score > 3 else "standard"
            }
            
        except Exception as e:
            self.logger.error(f"Complexity analysis failed: {e}")
            return {
                "complexity_level": "Unknown",
                "error": str(e)
            }
    
    def get_service_status(self) -> Dict[str, Any]:
        """
        Get comprehensive AI service status
        
        Returns:
            Dictionary with service status information
        """
        status = {
            "groq_available": GROQ_AVAILABLE,
            "client_initialized": self.client is not None,
            "api_key_configured": bool(self.config.api_key),
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature
        }
        
        if self.client:
            try:
                # Test basic functionality
                test_response = self.client.chat.completions.create(
                    model=self.config.model,
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=5
                )
                status["connection_test"] = "success"
            except Exception as e:
                status["connection_test"] = f"failed: {e}"
        
        return status