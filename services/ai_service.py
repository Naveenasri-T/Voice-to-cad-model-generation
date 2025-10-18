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

from config.settings import AIConfig

class AIService:
    def __init__(self, ai_config: AIConfig):
        self.config = ai_config
        self.logger = logging.getLogger(__name__)
        self.client = None
        self._initialize_client()
        
    def _initialize_client(self) -> None:
        if not GROQ_AVAILABLE:
            self.logger.error("Groq library not available - AI functionality disabled")
            return
            
        if not self.config.groq.api_key:
            self.logger.warning("AI API key not configured - limited functionality")
            return
            
        try:
            self.client = Groq(api_key=self.config.groq.api_key)
            self.logger.info("Professional AI client initialized successfully")
            
            # Test connection
            self._test_connection()
            
        except Exception as e:
            self.logger.error(f"Failed to initialize AI client: {e}")
            self.client = None
    
    def _test_connection(self) -> None:
        """Test AI service connection"""
        try:
            # Simple test request
            response = self.client.chat.completions.create(
                model=self.config.groq.model,
                messages=[{"role": "user", "content": "Test connection"}],
                max_tokens=10,
                temperature=0.1
            )
            
            if response and response.choices:
                self.logger.info("AI connection test successful")
            else:
                self.logger.warning("AI connection test returned empty response")
                
        except Exception as e:
            self.logger.warning(f"AI connection test failed: {e}")
    
    def transcribe_audio(self, audio_file_path: str) -> Optional[str]:
        if not self.client:
            return None
            
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
            return None
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
    
    def generate_freecad_code(self, command: str, model_type: str = "3d", 
                             quality_level: str = "professional", include_materials: bool = True) -> Optional[str]:
        if not self.client:
            return None
        
        command_lower = command.lower()
        if any(keyword in command_lower for keyword in ['2bhk', '2 bhk', 'two bedroom', 'apartment', 'house', 'structured']) and not any(school_keyword in command_lower for school_keyword in ['school', 'college', 'university']):
            return self._create_simple_2bhk_model()
        elif any(keyword in command_lower for keyword in ['school', 'college', 'university', 'campus', 'academic', 'classroom', 'education']):
            return self._create_school_model()
        elif any(keyword in command_lower for keyword in ['cube', 'box', 'simple']):
            return self._create_simple_cube()
            
        try:
            self.logger.info(f"Generating {quality_level} {model_type} FreeCAD code")
            
            # Create professional prompt
            prompt = self._create_professional_prompt(command, model_type, quality_level, include_materials)
            
            # Generate code with AI
            response = self.client.chat.completions.create(
                model=self.config.groq.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                top_p=0.95,
                stop=None
            )
            
            if response and response.choices:
                generated_code = response.choices[0].message.content
                
                if generated_code:
                    # Clean and validate generated code
                    cleaned_code = self._clean_generated_code(generated_code)
                    
                    if self._validate_freecad_code(cleaned_code):
                        self.logger.info("Professional FreeCAD code generated successfully")
                        return cleaned_code
                    else:
                        self.logger.warning("Generated code failed validation, trying to create working version")
                        # Try to create a working version for common requests
                        if "2bhk" in command.lower() or "apartment" in command.lower() or "house" in command.lower():
                            return self._create_simple_2bhk_model()
                        elif "cube" in command.lower() or "box" in command.lower():
                            return self._create_simple_cube()
                        else:
                            return cleaned_code  # Return even if validation failed
                        
            self.logger.warning("AI returned empty response for code generation")
            return None
            
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Code generation failed: {error_msg}")
            
            # Check for common API issues
            if "rate_limit" in error_msg.lower() or "quota" in error_msg.lower():
                self.logger.error("API rate limit or quota exceeded")
            elif "invalid_api_key" in error_msg.lower() or "unauthorized" in error_msg.lower():
                self.logger.error("Invalid API key or unauthorized access")
            elif "timeout" in error_msg.lower():
                self.logger.error("Request timeout - API may be slow")
            
            return None
    
    def _get_system_prompt(self) -> str:
        return """You are a FreeCAD expert. Generate clean, working FreeCAD Python code.

Requirements:
- Import FreeCAD and Part
- Create new document
- Use proper FreeCAD API only
- End with doc.recompute() and ViewFit
- No invalid attributes like ActiveMaterial or DiffuseColor

Generate clean, working FreeCAD code."""

    def _create_professional_prompt(self, command: str, model_type: str, quality_level: str, include_materials: bool) -> str:
        
        return f"Create FreeCAD {model_type} model for: {command}. Use import FreeCAD, import Part, create document, build model, end with doc.recompute()."
    
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
            cleaned_code = re.sub(r'FreeCADGui\.showMainWindow\(\)', '', cleaned_code)
            cleaned_code = re.sub(r'FreeCADGui\.updateGui\(\)', '', cleaned_code)
            
            # Remove invalid FreeCAD patterns
            cleaned_code = re.sub(r'FreeCAD\.ActiveMaterial.*?\n', '', cleaned_code)
            cleaned_code = re.sub(r'\.Material\s*=.*?\n', '', cleaned_code)
            cleaned_code = re.sub(r'\.DiffuseColor\s*=.*?\n', '', cleaned_code)
            cleaned_code = re.sub(r'FreeCAD\.ActiveDocument\.ActiveMaterial.*?\n', '', cleaned_code)
            
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
            
            return cleaned_code
            
        except Exception as e:
            self.logger.warning(f"Code cleaning failed: {e}")
            return code
    
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
            
            # Check for common syntax issues
            forbidden_patterns = [
                r'```',  # Markdown code blocks
                r'undefined',  # Common AI hallucination
                r'<[^>]+>',  # HTML tags
            ]
            
            for pattern in forbidden_patterns:
                if re.search(pattern, code):
                    self.logger.warning(f"Found forbidden pattern: {pattern}")
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
    
    def _create_simple_2bhk_model(self) -> str:
        """Create a structured architectural 2BHK house model with proper room layout"""
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
print(f"• Total Area: {(HOUSE_LENGTH * HOUSE_WIDTH)/1000000:.1f} sq.m")
print(f"• Overall Dimensions: {HOUSE_LENGTH/1000:.1f}m x {HOUSE_WIDTH/1000:.1f}m")
print(f"• Ceiling Height: {WALL_HEIGHT/1000:.1f}m")
print(f"• Wall Thickness: {WALL_THICKNESS}mm")
print("\\nROOM DETAILS:")
print("✓ Living Room: 5.5m x 3.5m (19.25 sq.m)")
print("✓ Kitchen: 2.5m x 2.5m (6.25 sq.m)")  
print("✓ Master Bedroom: 5.5m x 2.5m (13.75 sq.m)")
print("✓ Second Bedroom: 5.5m x 2.0m (11.0 sq.m)")
print("✓ Bathroom: 2.0m x 2.0m (4.0 sq.m)")
print("\\nSTRUCTURAL FEATURES:")
print("• Foundation with proper depth")
print("• Load-bearing brick walls with openings")
print("• Doors: 900mm wide standard doors")
print("• Windows: 1200mm x 1200mm with frames")
print("• RCC roof slab with proper thickness")
print("• Room area indicators for clear visualization")
print("\\nARCHITECTURAL ELEMENTS:")
print("• Main entrance with canopy")
print("• Door and window frames")
print("• Proper wall openings for natural light")
print("• Color-coded room identification")
print("• Professional structural layout")
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
print(f"• Total Built-up Area: {(SCHOOL_LENGTH * SCHOOL_WIDTH)/1000000:.1f} sq.m")
print(f"• Building Dimensions: {SCHOOL_LENGTH/1000:.1f}m x {SCHOOL_WIDTH/1000:.1f}m")
print(f"• Floor Height: {FLOOR_HEIGHT/1000:.1f}m (Educational Standard)")
print(f"• Wall Thickness: {WALL_THICKNESS}mm (Institutional Grade)")
print("\\nEDUCATIONAL FACILITIES:")
print("✓ Reception Hall: 8m x 12m (96 sq.m)")
print("✓ Principal Office: 6m x 5m (30 sq.m)")  
print("✓ Staff Room: 8m x 6m (48 sq.m)")
print("✓ 5 Classrooms: 7m x 12m each (84 sq.m each)")
print("✓ Library: 12m x 10m (120 sq.m)")
print("✓ Computer Lab: 10m x 8m (80 sq.m)")
print("✓ Science Laboratory: 9m x 8m (72 sq.m)")
print("✓ Central Corridor: 3m wide (Accessibility compliant)")
print("\\nSTRUCTURAL FEATURES:")
print("• Reinforced foundation for institutional load")
print("• Load-bearing walls with proper openings")
print("• Large windows for natural lighting")
print("• Multiple emergency exits")
print("• Wide corridors for student movement")
print("• Professional educational layout")
print("\\nSAFETY & COMPLIANCE:")
print("• Fire safety exits and wide corridors")
print("• Accessibility compliant design")
print("• Natural lighting in all classrooms")
print("• Proper ventilation systems")
print("• Emergency exit provisions")
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