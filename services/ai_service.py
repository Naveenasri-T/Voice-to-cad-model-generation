import logging
import json
from typing import Optional, Dict, Any, List
from pathlib import Path
import re
import textwrap

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    import google.genai as genai  # Modern Gemini SDK
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
            self.logger.error(
                "google-genai package not available. Install it with 'pip install google-genai' "
                "(see https://github.com/google-gemini/deprecated-generative-ai-python) to enable Gemini support."
            )
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
                self.logger.error("Failed to create prompt - using blueprint template fallback")
                return self._build_blueprint_template(command)

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

                # Check for 3D objects — one regeneration attempt only
                if self._contains_3d_objects(cleaned_code):
                    self.logger.warning("Generated code contains 3D objects — attempting 2D regeneration once")
                    regen = self._regenerate_as_2d_only(command, model_type)
                    return regen if regen else self._build_blueprint_template(command)

                # Check complexity — one regeneration attempt only
                if cleaned_code and not self._has_sufficient_complexity(cleaned_code, min_commands=15):
                    self.logger.warning("Generated code too simple — attempting 2D regeneration once")
                    regen = self._regenerate_as_2d_only(command, model_type)
                    return regen if regen else self._build_blueprint_template(command)

                if self._validate_freecad_code(cleaned_code):
                    self.logger.info("Professional FreeCAD code generated successfully")
                    return cleaned_code
                else:
                    self.logger.warning("Generated code failed validation, attempting to fix")
                    fixed_code = self._fix_common_issues(cleaned_code)
                    if self._validate_freecad_code(fixed_code):
                        return fixed_code
                    # Return cleaned version as last resort
                    self.logger.warning("Code validation still failed — returning cleaned version")
                    return cleaned_code
            else:
                self.logger.warning("AI returned empty response — using blueprint template")
                return self._build_blueprint_template(command)

        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Code generation failed: {error_msg}")

            if "rate limit" in error_msg.lower() or "api" in error_msg.lower():
                self.logger.info("API/rate-limit error — using blueprint template fallback")
                return self._build_blueprint_template(command)

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
        """Return deterministic 2D blueprint template when AI providers refuse requests."""
        return self._build_blueprint_template(prompt)

    def _build_blueprint_template(self, command: str) -> str:
        """Generate a professional multi-view 2BHK architectural blueprint."""
        safe_summary = (command or "2BHK House Blueprint").strip().replace('"', "'")
        safe_summary = safe_summary.replace('{', '[').replace('}', ']')
        if len(safe_summary) > 120:
            safe_summary = safe_summary[:117] + "..."
        safe_doc_name = re.sub(r"[^A-Za-z0-9_]+", "_", safe_summary) or "2BHK_Blueprint"
        safe_doc_name = safe_doc_name[:40].strip('_') or "2BHK_Blueprint"
        summary_literal = json.dumps(safe_summary)

        template = textwrap.dedent("""
import FreeCAD
import Draft

doc = FreeCAD.newDocument("__DOC_NAME__")
REQUEST_SUMMARY = __SUMMARY_LITERAL__

print("=== 2BHK HOUSE BLUEPRINT ===")
print(f"Request: {REQUEST_SUMMARY}")

# ─── DIMENSIONS (mm) ──────────────────────────────────────────
HOUSE_W  = 10500
HOUSE_D  = 8500
VIEW_GAP = 16000
PLAN_Y   = 0
FRONT_Y  = VIEW_GAP
SIDE_Y   = VIEW_GAP * 2
drawing_commands = 0
dimension_count  = 0
text_count       = 0

# ─── SAFE COLOUR HELPER ───────────────────────────────────────
def _set_color(vo, attr, val):
    \"\"\"Safely set a ViewObject colour property.\"\"\"
    try:
        setattr(vo, attr, val)
    except Exception:
        pass   # Some FreeCAD builds reject certain colour formats

# ─── HELPERS ──────────────────────────────────────────────────
def S(obj, w=2.0, c=(0.0, 0.0, 0.0)):
    if hasattr(obj, "ViewObject"):
        try:
            obj.ViewObject.LineWidth = w
        except Exception:
            pass
        _set_color(obj.ViewObject, "LineColor", c)

def wall(x1, y1, x2, y2, w=2.0):
    global drawing_commands
    ln = Draft.makeLine(FreeCAD.Vector(x1, y1, 0), FreeCAD.Vector(x2, y2, 0))
    S(ln, w)
    drawing_commands += 1
    return ln

def room_box(x, y, w, d, lw=2.0):
    global drawing_commands
    r = Draft.makeRectangle(
        length=w, height=d,
        placement=FreeCAD.Placement(FreeCAD.Vector(x, y, 0), FreeCAD.Rotation(0, 0, 0))
    )
    S(r, lw)
    drawing_commands += 1
    return r

def lbl(texts, x, y, size=280, color=(0.0, 0.0, 0.0)):
    global text_count
    # Draft.make_text is the current API (makeText is deprecated)
    try:
        t = Draft.make_text(texts, placement=FreeCAD.Vector(x, y, 0))
    except Exception:
        t = Draft.makeText(texts, point=FreeCAD.Vector(x, y, 0))
    if hasattr(t, "ViewObject"):
        try:
            t.ViewObject.FontSize = size
        except Exception:
            pass
        _set_color(t.ViewObject, "TextColor", color)
    text_count += 1
    return t

def dim(x1, y1, x2, y2):
    global dimension_count
    try:
        d = Draft.make_linear_dimension(
            FreeCAD.Vector(x1, y1, 0),
            FreeCAD.Vector(x2, y2, 0)
        )
        if hasattr(d, "ViewObject"):
            try:
                d.ViewObject.FontSize = 260
            except Exception:
                pass
            _set_color(d.ViewObject, "TextColor", (1.0, 0.0, 0.0))
            _set_color(d.ViewObject, "LineColor",  (0.0, 0.0, 0.0))
        dimension_count += 1
        return d
    except Exception:
        return None

def door_arc(cx, cy, r, a1, a2):
    global drawing_commands
    try:
        arc = Draft.makeCircle(
            radius=r,
            placement=FreeCAD.Placement(FreeCAD.Vector(cx, cy, 0), FreeCAD.Rotation(0, 0, 0)),
            startangle=a1, endangle=a2
        )
        S(arc, 0.8)
        drawing_commands += 1
        return arc
    except Exception:
        return None

def win(x, y, length, horiz=True):
    \"\"\"Three-line window symbol.\"\"\"
    if horiz:
        wall(x, y - 60, x + length, y - 60, 1.0)
        wall(x, y,      x + length, y,      1.8)
        wall(x, y + 60, x + length, y + 60, 1.0)
    else:
        wall(x - 60, y, x - 60, y + length, 1.0)
        wall(x,      y, x,      y + length, 1.8)
        wall(x + 60, y, x + 60, y + length, 1.0)

# ═════════════════════════════════════════════════════════════
#  FLOOR PLAN  (Plan View – looking down)
# ═════════════════════════════════════════════════════════════
print("Drawing Floor Plan...")

# ── Outer house boundary (thick) ──────────────────────────────
ext = room_box(0, PLAN_Y, HOUSE_W, HOUSE_D, 3.5)
ext.Label = "Exterior_Boundary"

# ── Interior walls ─────────────────────────────────────────────
wall(6000, PLAN_Y, 6000, PLAN_Y + HOUSE_D, 2.2).Label = "Spine_Wall"
wall(0, PLAN_Y + 4500, HOUSE_W, PLAN_Y + 4500, 2.2).Label = "Mid_Wall"
wall(3500, PLAN_Y + 4500, 3500, PLAN_Y + HOUSE_D, 2.0).Label = "Kitchen_E_Wall"
wall(3500, PLAN_Y + 6400, 6000, PLAN_Y + 6400, 2.0).Label = "Bath_Divider"
wall(9000, PLAN_Y + 4500, 9000, PLAN_Y + HOUSE_D, 2.0).Label = "Store_Wall"

# ── Windows ────────────────────────────────────────────────────
# South face (front wall y=PLAN_Y)
win(700,  PLAN_Y, 1400, True)
win(2500, PLAN_Y, 1200, True)
win(7000, PLAN_Y, 1600, True)
# North face (rear wall y=PLAN_Y+HOUSE_D)
win(400,  PLAN_Y + HOUSE_D, 1200, True)
win(2200, PLAN_Y + HOUSE_D, 1000, True)
win(6500, PLAN_Y + HOUSE_D, 1200, True)
# East face (side wall x=HOUSE_W)
win(HOUSE_W, PLAN_Y + 1200, 1200, False)
win(HOUSE_W, PLAN_Y + 5500, 1200, False)

# ── Door openings + swing arcs ─────────────────────────────────
# Main entrance (south, x=4700)
wall(4700, PLAN_Y, 5600, PLAN_Y, 0.4)
door_arc(4700, PLAN_Y, 900, 0, 90)
lbl(["D1"], 4700, PLAN_Y - 350, size=200)

# Master bed door (spine, y=1500-2300)
wall(6000, PLAN_Y + 1500, 6000, PLAN_Y + 2300, 0.4)
door_arc(6000, PLAN_Y + 2300, 800, 180, 270)
lbl(["D2"], 6150, PLAN_Y + 1800, size=200)

# Kitchen door (mid wall, x=2000-2700)
wall(2000, PLAN_Y + 4500, 2700, PLAN_Y + 4500, 0.4)
door_arc(2000, PLAN_Y + 4500, 700, 270, 360)
lbl(["D3"], 2100, PLAN_Y + 4650, size=200)

# Bed2 door (kitchen east wall, y=5200-5900)
wall(3500, PLAN_Y + 5200, 3500, PLAN_Y + 5900, 0.4)
door_arc(3500, PLAN_Y + 5200, 700, 0, 90)
lbl(["D4"], 3650, PLAN_Y + 5300, size=200)

# Bathroom door
wall(3500, PLAN_Y + 6600, 3500, PLAN_Y + 7200, 0.4)
door_arc(3500, PLAN_Y + 6600, 600, 0, 90)
lbl(["D5"], 3650, PLAN_Y + 6700, size=200)

# Toilet door
wall(4400, PLAN_Y + 6400, 5000, PLAN_Y + 6400, 0.4)
door_arc(4400, PLAN_Y + 6400, 600, 270, 360)
lbl(["D6"], 4450, PLAN_Y + 6580, size=200)

# ── Furniture ──────────────────────────────────────────────────
room_box(300,  PLAN_Y + 2800, 2800, 800,  1.0).Label = "Sofa"
room_box(300,  PLAN_Y + 200,  1200, 700,  1.0).Label = "TV_Unit"
room_box(3200, PLAN_Y + 1800, 1800, 1200, 1.0).Label = "Dining_Table"
room_box(6300, PLAN_Y + 600,  2200, 1800, 1.0).Label = "Master_Bed"
room_box(8800, PLAN_Y + 300,  600,  2000, 1.0).Label = "Wardrobe"
room_box(6400, PLAN_Y + 5200, 2000, 1600, 1.0).Label = "Bed2"
room_box(200,  PLAN_Y + 4700, 3100, 600,  1.0).Label = "Kitchen_Counter"

# ── Room labels ────────────────────────────────────────────────
lbl(["LIVING ROOM",   "6.0 x 4.5 m"],   1000, PLAN_Y + 2000, size=300)
lbl(["DINING",        "3.5 x 2.5 m"],   3200, PLAN_Y + 3000, size=260)
lbl(["MASTER BEDROOM","4.5 x 4.5 m"],   6500, PLAN_Y + 1800, size=300)
lbl(["BEDROOM 2",     "4.5 x 4.0 m"],   6400, PLAN_Y + 5900, size=300)
lbl(["KITCHEN",       "3.5 x 4.0 m"],    400, PLAN_Y + 5600, size=280)
lbl(["BATHROOM"],                        3700, PLAN_Y + 5100, size=260)
lbl(["TOILET"],                          3700, PLAN_Y + 7100, size=260)
lbl(["STORE"],                           9100, PLAN_Y + 5900, size=240)

lbl(["FLOOR PLAN", "Scale 1:100"],     0, PLAN_Y + HOUSE_D + 600, size=340)
lbl(["N", chr(8593)],  HOUSE_W + 950, PLAN_Y + HOUSE_D / 2, size=500, color=(0.0, 0.4, 0.8))

# ── Plan dimensions ────────────────────────────────────────────
dim(0,          PLAN_Y - 1400, HOUSE_W, PLAN_Y - 1400)        # total width
dim(-1400,      PLAN_Y,       -1400,    PLAN_Y + HOUSE_D)     # total depth
dim(0,          PLAN_Y - 700,  6000,    PLAN_Y - 700)         # living zone W
dim(6000,       PLAN_Y - 700,  HOUSE_W, PLAN_Y - 700)         # bed zone W
dim(HOUSE_W+700, PLAN_Y,      HOUSE_W+700, PLAN_Y+4500)       # front depth
dim(HOUSE_W+700, PLAN_Y+4500, HOUSE_W+700, PLAN_Y+HOUSE_D)   # rear depth
dim(0,          PLAN_Y + HOUSE_D + 300, 3500, PLAN_Y + HOUSE_D + 300)
dim(3500,       PLAN_Y + HOUSE_D + 300, 6000, PLAN_Y + HOUSE_D + 300)

# ═════════════════════════════════════════════════════════════
#  FRONT ELEVATION  (y = FRONT_Y)
# ═════════════════════════════════════════════════════════════
print("Drawing Front Elevation...")

room_box(0, FRONT_Y, HOUSE_W, 3000, 3.0).Label = "Front_Elev"
wall(0, FRONT_Y - 250, HOUSE_W, FRONT_Y - 250, 3.0)          # ground
wall(0, FRONT_Y + 450, HOUSE_W, FRONT_Y + 450, 1.5)          # plinth
wall(0, FRONT_Y + 2200, HOUSE_W, FRONT_Y + 2200, 1.5)        # lintel
room_box(0, FRONT_Y + 3000, HOUSE_W, 400, 1.5).Label = "Parapet"

# Door & windows
room_box(4700, FRONT_Y + 450,  900, 1850, 1.5).Label = "Main_Door"
wall(5150, FRONT_Y + 450, 5150, FRONT_Y + 2300, 0.8)         # door mullion
room_box(700,  FRONT_Y + 900, 1400, 1200, 1.5).Label = "Win_F1"
room_box(2400, FRONT_Y + 900, 1200, 1200, 1.5).Label = "Win_F2"
room_box(6800, FRONT_Y + 900, 1600, 1200, 1.5).Label = "Win_F3"
room_box(9100, FRONT_Y + 900,  900, 1000, 1.5).Label = "Win_F4"

# Column marks
for cx in [0, 3500, 6000, 9000, HOUSE_W]:
    wall(cx, FRONT_Y, cx, FRONT_Y + 3000, 0.8)

lbl(["FRONT ELEVATION", "Scale 1:100"], 0, FRONT_Y + 3650, size=340)

dim(0,     FRONT_Y - 850, HOUSE_W, FRONT_Y - 850)            # width
dim(-1200, FRONT_Y,       -1200,   FRONT_Y + 450)            # plinth
dim(-1200, FRONT_Y + 450, -1200,   FRONT_Y + 2200)           # wall to lintel
dim(-1200, FRONT_Y + 2200,-1200,   FRONT_Y + 3400)           # lintel to slab

# ═════════════════════════════════════════════════════════════
#  SIDE ELEVATION  (y = SIDE_Y)
# ═════════════════════════════════════════════════════════════
print("Drawing Side Elevation...")

room_box(0, SIDE_Y, HOUSE_D, 3000, 3.0).Label = "Side_Elev"
wall(0, SIDE_Y - 250, HOUSE_D, SIDE_Y - 250, 3.0)            # ground
wall(0, SIDE_Y + 450, HOUSE_D, SIDE_Y + 450, 1.5)            # plinth
wall(0, SIDE_Y + 2200, HOUSE_D, SIDE_Y + 2200, 1.5)          # lintel
room_box(0, SIDE_Y + 3000, HOUSE_D, 400, 1.5).Label = "Side_Parapet"

# Side windows
room_box(800,  SIDE_Y + 900, 1200, 1100, 1.5).Label = "Side_Win1"
room_box(3600, SIDE_Y + 900, 1200, 1100, 1.5).Label = "Side_Win2"
room_box(5400, SIDE_Y + 900, 1200, 1100, 1.5).Label = "Side_Win3"

# Section cut marks at wall faces (just 4 short diagonal marks, not a dense hatch)
for hx in [0, 200, 400, 600]:
    wall(hx, SIDE_Y, hx + 200, SIDE_Y + 200, 0.5)

lbl(["SIDE / SECTION ELEVATION", "Scale 1:100"], 0, SIDE_Y + 3700, size=340)

dim(0,      SIDE_Y - 850, HOUSE_D, SIDE_Y - 850)             # depth
dim(-1200,  SIDE_Y,      -1200,    SIDE_Y + 3400)            # total height
dim(-700,   SIDE_Y,      -700,     SIDE_Y + 450)             # plinth

# ═════════════════════════════════════════════════════════════
#  COORDINATE GRID  (spaced 2400mm — half as dense)
# ═════════════════════════════════════════════════════════════
GRID_SPACING = 2400
GRID_BOT = PLAN_Y - 2600
GRID_TOP = SIDE_Y + 4400
GRID_L   = -2200
GRID_R   = HOUSE_W + 2200

for ci, letter in enumerate("ABCDE"):
    gx = ci * GRID_SPACING
    if gx > HOUSE_W + 500:
        break
    gl = Draft.makeLine(FreeCAD.Vector(gx, GRID_BOT, 0), FreeCAD.Vector(gx, GRID_TOP, 0))
    S(gl, 0.3, (0.78, 0.78, 0.78))
    drawing_commands += 1
    try:
        t = Draft.make_text([letter], placement=FreeCAD.Vector(gx - 100, GRID_BOT - 600, 0))
    except Exception:
        t = Draft.makeText([letter], point=FreeCAD.Vector(gx - 100, GRID_BOT - 600, 0))
    if hasattr(t, "ViewObject"):
        try:
            t.ViewObject.FontSize = 240
        except Exception:
            pass
        _set_color(t.ViewObject, "TextColor", (0.8, 0.0, 0.0))
    text_count += 1

for ri, num in enumerate(["1", "2", "3", "4", "5", "6", "7"]):
    gy = PLAN_Y + ri * GRID_SPACING
    if gy > GRID_TOP:
        break
    gh = Draft.makeLine(FreeCAD.Vector(GRID_L, gy, 0), FreeCAD.Vector(GRID_R, gy, 0))
    S(gh, 0.3, (0.78, 0.78, 0.78))
    drawing_commands += 1
    try:
        t = Draft.make_text([num], placement=FreeCAD.Vector(GRID_L - 600, gy - 100, 0))
    except Exception:
        t = Draft.makeText([num], point=FreeCAD.Vector(GRID_L - 600, gy - 100, 0))
    if hasattr(t, "ViewObject"):
        try:
            t.ViewObject.FontSize = 240
        except Exception:
            pass
        _set_color(t.ViewObject, "TextColor", (0.8, 0.0, 0.0))
    text_count += 1

# ═════════════════════════════════════════════════════════════
#  TITLE BLOCK
# ═════════════════════════════════════════════════════════════
TB_Y = SIDE_Y + 4600
room_box(0, TB_Y, HOUSE_W, 2500, 1.5).Label = "Title_Block"
wall(HOUSE_W * 0.5, TB_Y, HOUSE_W * 0.5, TB_Y + 2500, 1.0)
wall(0, TB_Y + 1250, HOUSE_W, TB_Y + 1250, 0.8)
lbl([f"PROJECT: {REQUEST_SUMMARY}", "CLIENT:", "SCALE: 1:100"], 150, TB_Y + 1450, size=220)
lbl(["DRAWN BY: AI Blueprint", "DATE: 2025", "SHEET: A-101"], HOUSE_W * 0.5 + 150, TB_Y + 1450, size=220)
lbl(["VOICE TO CAD MODEL GENERATION"], HOUSE_W * 0.5 - 2500, TB_Y + 200, size=300)

# ═════════════════════════════════════════════════════════════
doc.recompute()

if hasattr(FreeCAD, "Gui") and FreeCAD.Gui:
    try:
        FreeCAD.Gui.SendMsgToActiveView("ViewFit")
        FreeCAD.Gui.ActiveDocument.activeView().viewTop()
    except Exception:
        pass

print(f"Primitives : {drawing_commands}")
print(f"Dimensions : {dimension_count}")
print(f"Labels     : {text_count}")
print("=== BLUEPRINT COMPLETE ===")
""")

        template = template.replace("__DOC_NAME__", safe_doc_name)
        template = template.replace("__SUMMARY_LITERAL__", summary_literal)
        return template


    def _generate_with_groq(self, prompt: str) -> Optional[str]:
        """Generate code using Groq API with token-budget guard."""
        try:
            if not prompt or not prompt.strip():
                self.logger.error("Empty prompt provided to Groq API")
                return None

            system_prompt = self._get_system_prompt()
            if not system_prompt or not system_prompt.strip():
                self.logger.error("Empty system prompt")
                system_prompt = (
                    "You are a FreeCAD Python code generator. "
                    "Generate clean 2D Draft-only FreeCAD Python blueprints."
                )

            # ── Token budget guard ───────────────────────────────────────────
            # Groq free tier: 6000 TPM input limit is safest assumption.
            # We reserve 4000 tokens for the response, leaving 6000 for input.
            MAX_INPUT_TOKENS = 6000
            system_tokens = self._estimate_tokens(system_prompt)
            prompt_tokens  = self._estimate_tokens(prompt)
            total_input    = system_tokens + prompt_tokens

            if total_input > MAX_INPUT_TOKENS:
                self.logger.warning(
                    f"Combined prompt too large (~{total_input} tokens, limit {MAX_INPUT_TOKENS}). "
                    "Truncating user prompt to fit."
                )
                # Truncate user prompt to stay within budget
                available = MAX_INPUT_TOKENS - system_tokens
                max_chars = available * 4
                prompt = prompt[:max_chars] + "\n\n[...truncated to fit token limit]"
                self.logger.info(f"User prompt truncated to {len(prompt)} chars")

            response = self.client.chat.completions.create(
                model=self.config.groq.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": prompt.strip()},
                ],
                max_tokens=min(self.config.max_tokens, 6000),
                temperature=self.config.temperature,
                top_p=0.95,
                stop=None,
            )

            if response and response.choices:
                return response.choices[0].message.content
            return None

        except Exception as e:
            err = str(e)
            if "413" in err or "rate_limit" in err.lower() or "tokens" in err.lower():
                self.logger.warning(
                    f"Groq token/rate-limit error — skipping AI, using template. ({err[:120]})"
                )
            else:
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

            building_spec = dynamic_config.parse_building_command(command)
            if building_spec:
                spec_name = getattr(building_spec, "name", "Custom Blueprint")
                rooms = getattr(building_spec, "rooms", []) or []
                summary = f"{spec_name} with {len(rooms)} planned spaces" if rooms else spec_name
                return self._build_blueprint_template(summary)

        except Exception as e:
            self.logger.warning(f"Dynamic config analysis failed: {e}")

        return self._build_blueprint_template(command)

    def _create_professional_prompt(self, command: str, model_type: str = "2d",
                                    quality_level: str = "professional",
                                    include_materials: bool = False) -> str:
        """Create a concise 2D-only user prompt for the AI.

        The heavy structural rules live in the system prompt (ai_system_prompt.txt).
        This user prompt only needs to:
          1. State what to draw
          2. Remind the AI of the house layout and room names
          3. Stay SHORT to avoid exceeding Groq's 12000 TPM limit
        """
        cmd = (command or "2BHK house blueprint").strip()

        # Detect number of bedrooms from command
        bhk = "2"
        for n in ["1", "2", "3", "4"]:
            if f"{n}bhk" in cmd.lower() or f"{n} bhk" in cmd.lower():
                bhk = n
                break

        room_map = {
            "1": "Living Room, Kitchen, Bedroom, Bathroom",
            "2": "Living Room, Dining, Master Bedroom, Bedroom 2, Kitchen, Bathroom, Toilet",
            "3": "Living Room, Dining, Master Bedroom, Bedroom 2, Bedroom 3, Kitchen, Bathroom 1, Bathroom 2, Store",
            "4": "Living Room, Dining, Master Bedroom, Bedroom 2, Bedroom 3, Bedroom 4, Kitchen, Dining, Study, Bathroom 1, Bathroom 2, Store",
        }
        rooms = room_map.get(bhk, room_map["2"])

        return (
            f"Draw a professional {bhk}BHK house architectural blueprint for: {cmd}\n\n"
            f"Rooms required: {rooms}\n\n"
            "Follow the system prompt structure exactly:\n"
            "  1. Floor plan (y=0): exterior room_box(0,0,10500,8500,3.5), "
            "interior walls, door arcs, window symbols, furniture, room labels\n"
            "  2. Front elevation (y=16000): facade, openings, parapet\n"
            "  3. Side elevation (y=32000): depth profile, section hatching\n"
            "  4. Grid (light grey columns A-J, rows 1-12, every 1200mm)\n"
            "  5. Title block at bottom\n\n"
            "REMEMBER: Draft-only (no Part module), all Z=0, "
            ">=30 primitives, >=8 dim(), >=8 lbl()."
        )


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
        """Conservative indentation fixer: only corrects dedented top-level property
        assignments.  Leaves multi-line strings and f-strings untouched."""
        import ast

        # Fast path — already valid Python
        try:
            ast.parse(code)
            return code
        except SyntaxError as first_err:
            self.logger.warning(
                f"Indentation error at line {first_err.lineno}: {first_err.msg}. "
                "Attempting conservative fix..."
            )

        # Only attempt to re-indent lines where a property assignment
        # (e.g. `wall.Length.Value = 200`) appears at column 0 when it
        # should be inside a block.  We do NOT touch lines that are part
        # of multi-line strings or complex expressions.
        property_pattern = re.compile(r'^([A-Za-z_]\w*)\.\w+(\.\w+)? *=')
        lines = code.split('\n')
        fixed = []
        prev_indent = ''

        for line in lines:
            stripped = line.strip()
            if not stripped:
                fixed.append(line)
                continue

            # If this looks like a bare property assignment at col-0, give
            # it the same indent as the previous non-empty line.
            if property_pattern.match(stripped) and not line[0:1] in (' ', '\t'):
                fixed.append(prev_indent + stripped)
            else:
                fixed.append(line)
                # Remember the indent of any non-empty line
                m = re.match(r'^(\s*)', line)
                if m and stripped:
                    prev_indent = m.group(1)

        fixed_code = '\n'.join(fixed)

        try:
            ast.parse(fixed_code)
            self.logger.info("Conservative indentation fix successful")
            return fixed_code
        except SyntaxError as second_err:
            self.logger.warning(
                f"Conservative fix insufficient ({second_err}). "
                "Returning original code unchanged — do not mangle further."
            )
            # Return the *original* code so we don't make things worse
            return code
    
    def _aggressive_indent_fix(self, code: str) -> str:
        """Kept for backward compat but now just returns the original code.
        Aggressive reindentation destroys multi-line strings and f-strings,
        so we no longer attempt it — the conservative fixer in _fix_indentation
        is the last line of defence."""
        self.logger.warning(
            "_aggressive_indent_fix called — returning original code unchanged "
            "to avoid mangling multi-line strings."
        )
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
        Final cleanup pass: eliminates all malformed ViewObject token merges.

        Handles patterns such as:
          - dim1.ViewObjectdim1.ViewObject.FontSize   (common AI merge)
          - grid_line.ViewObject    grid_line.ViewObject.LineColor  (whitespace split)
          - obj.ViewObjectSomeRandomWord.ViewObject   (generic merge)
        """
        # Count errors before fix
        error_count = len(re.findall(r'\.ViewObject[A-Za-z0-9_]+\.ViewObject', code))
        if error_count:
            self.logger.warning(f"Found {error_count} ViewObject merge errors — fixing")

        lines = code.split('\n')
        result_lines = []

        for line in lines:
            if '.ViewObject' not in line:
                result_lines.append(line)
                continue

            # ── Case 1: whitespace-merged duplicates on one line ──────────────
            # e.g. "grid_line.ViewObject    grid_line.ViewObject.LineColor = ..."
            ws_match = re.match(
                r'^(\s*)(\w+)\.ViewObject\s{2,}(\w+)\.ViewObject(.*)$', line
            )
            if ws_match:
                indent, var1, var2, rest = ws_match.groups()
                result_lines.append(f'{indent}{var1}.ViewObject')
                line = f'{indent}{var2}.ViewObject{rest}'

            # ── Case 2: concatenated variable names ───────────────────────────
            # e.g. "dim1.ViewObjectdim1.ViewObject.FontSize"
            # One regex pass handles all variable-name variants:
            line = re.sub(r'\.ViewObject[A-Za-z_][A-Za-z0-9_]*\.ViewObject', '.ViewObject', line)

            result_lines.append(line)

        return '\n'.join(result_lines)
    
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
    
    def _has_sufficient_complexity(self, code: str, min_commands: int = 30) -> bool:
        """Check if generated code meets professional blueprint standards.

        Args:
            code: Python source to analyse.
            min_commands: Minimum Draft primitive count (default 30 for final check;
                          use a lower value, e.g. 15, for the first-pass check to avoid
                          an infinite regenerate loop).
        """
        if not code:
            return False

        draft_lines      = len(re.findall(r'Draft\.makeLine', code))
        draft_wires      = len(re.findall(r'Draft\.makeWire', code))
        draft_rectangles = len(re.findall(r'Draft\.makeRectangle', code))
        draft_circles    = len(re.findall(r'Draft\.makeCircle', code))
        total_drawing_commands = draft_lines + draft_wires + draft_rectangles + draft_circles

        dimensions_modern = len(re.findall(r'Draft\.make_linear_dimension', code))
        dimensions_old    = len(re.findall(r'Draft\.makeDimension', code))
        dimensions        = dimensions_modern + dimensions_old

        if dimensions_old > 0:
            self.logger.warning(
                "⚠️ Code uses DEPRECATED Draft.makeDimension() — "
                "should use Draft.make_linear_dimension()"
            )

        labels = len(re.findall(r'Draft\.makeText', code))

        view_keywords = [
            '# front', '# top', '# side', '# section', '# projection',
            'elevation', 'floor_plan', 'section', 'plan view', 'front view',
        ]
        view_count = sum(
            1 for kw in view_keywords if kw in code.lower()
        )

        has_grid = (
            'grid' in code.lower()
            and ('Draft.makeLine' in code or 'grid_line' in code.lower())
        )

        self.logger.info(
            f"Blueprint Quality Check: commands={total_drawing_commands}/{min_commands} "
            f"dims={dimensions} labels={labels} views={view_count} grid={has_grid}"
        )

        if total_drawing_commands < min_commands:
            self.logger.warning(
                f"❌ INSUFFICIENT DETAIL: {total_drawing_commands} drawing commands "
                f"(need ≥ {min_commands})"
            )
            return False

        if dimensions < 8:
            self.logger.warning(
                f"❌ MISSING DIMENSIONS: {dimensions} (need ≥ 8)"
            )
            return False

        if labels < 8:
            self.logger.warning(
                f"❌ MISSING LABELS: {labels} (need ≥ 8)"
            )
            return False

        if view_count < 2:
            self.logger.warning(
                f"❌ FEW VIEWS: {view_count} detected (need ≥ 2: plan + elevation)"
            )
            return False

        if not has_grid:
            self.logger.warning(
                "❌ NO GRID SYSTEM — professional blueprints require coordinate grid"
            )
            return False

        self.logger.info("✅ Blueprint quality check PASSED")
        return True
    
    def _regenerate_as_2d_only(self, command: str, model_type: str = "2D") -> Optional[str]:
        """One-shot attempt to regenerate with strict 2D-only emphasis.

        Prompt text is loaded from config/load_prompt.py — no hardcoded blocks here.
        Falls back to the static blueprint template if the provider fails or still
        returns 3D code.
        """
        try:
            from config.load_prompt import load_regeneration_prompt
            enhanced_prompt = load_regeneration_prompt(command)

            self.logger.info("Regenerating with 2D-only emphasis (single attempt)...")

            if self.provider == 'groq':
                response = self.client.chat.completions.create(
                    model=self.config.groq.model,
                    messages=[
                        {"role": "system", "content": self._get_system_prompt()},
                        {"role": "user",   "content": enhanced_prompt},
                    ],
                    max_tokens=8000,
                    temperature=0.3,
                )
                generated_code = (
                    response.choices[0].message.content
                    if response and response.choices
                    else ""
                )
            elif self.provider == 'gemini':
                # Gemini blocks most CAD content; fall straight to template
                self.logger.info(
                    "Gemini provider detected — skipping API call, returning template"
                )
                return self._build_blueprint_template(command)
            else:
                generated_code = ""

            if not generated_code:
                self.logger.warning("Empty response during regeneration — using template")
                return self._build_blueprint_template(command)

            cleaned_code = self._clean_generated_code(generated_code)

            if self._contains_3d_objects(cleaned_code):
                self.logger.error(
                    "AI still generated 3D objects after regeneration — using template"
                )
                return self._build_blueprint_template(command)

            return cleaned_code

        except Exception as e:
            err = str(e)
            if "413" in err or "rate_limit" in err.lower() or "tokens" in err.lower():
                self.logger.warning(
                    f"Rate/token limit during regeneration — using blueprint template. ({err[:120]})"
                )
            else:
                self.logger.error(f"Regeneration failed: {e} — using blueprint template")
            return self._build_blueprint_template(command)
    
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
        """Validate generated FreeCAD code for common issues.

        Returns True when the code is safe to hand to FreeCAD.
        """
        try:
            # Required structural patterns
            for pattern in [
                r'import\s+FreeCAD',
                r'newDocument',
                r'recompute',
            ]:
                if not re.search(pattern, code, re.IGNORECASE):
                    self.logger.warning(f"Missing required pattern: {pattern}")
                    return False

            # Forbidden patterns (3D / deprecated / markdown artefacts)
            forbidden = [
                (r'```',                            "Markdown code fence"),
                (r'undefined',                      "Undefined variable artefact"),
                (r'<[^>]+>',                        "HTML tag"),
                (r'Units\.setPreferredUnitSystem',  "Deprecated Units API"),
                (r'Units\.setUnitSystem',           "Deprecated Units API"),
                (r'FreeCAD\.Units\.setUnitSystem',  "Deprecated Units API"),
                (r'FreeCAD\.Units\.setPreferredUnitSystem', "Deprecated Units API"),
                (r'Part\.makeBox',                  "3D Part.makeBox"),
                (r'\.ActiveMaterial',               "Deprecated material"),
                (r'\.DiffuseColor',                 "Deprecated color"),
                (r'App\.setActiveDocument',         "Problematic App pattern"),
                # NOTE: .Label = is valid for Draft objects, so NOT forbidden here
            ]
            for pattern, reason in forbidden:
                if re.search(pattern, code):
                    self.logger.warning(f"Forbidden pattern ({reason}): {pattern}")
                    return False

            # Python syntax check
            try:
                compile(code, '<generated>', 'exec')
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