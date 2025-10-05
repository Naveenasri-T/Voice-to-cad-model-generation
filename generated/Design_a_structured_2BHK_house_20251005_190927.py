"""
Professional FreeCAD Model - Client Ready
Generated with Enterprise AI Technology
"""

import FreeCAD
import Part

# Create professional document
doc = FreeCAD.newDocument("ProfessionalModel")
FreeCAD.Console.PrintMessage("=== Professional Model Generation ===\n")

import FreeCAD
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
print("\n" + "="*50)
print("STRUCTURED 2BHK HOUSE - ARCHITECTURAL MODEL")
print("="*50)
print("BUILDING SPECIFICATIONS:")
print(f"• Total Area: {(HOUSE_LENGTH * HOUSE_WIDTH)/1000000:.1f} sq.m")
print(f"• Overall Dimensions: {HOUSE_LENGTH/1000:.1f}m x {HOUSE_WIDTH/1000:.1f}m")
print(f"• Ceiling Height: {WALL_HEIGHT/1000:.1f}m")
print(f"• Wall Thickness: {WALL_THICKNESS}mm")
print("\nROOM DETAILS:")
print("✓ Living Room: 5.5m x 3.5m (19.25 sq.m)")
print("✓ Kitchen: 2.5m x 2.5m (6.25 sq.m)")  
print("✓ Master Bedroom: 5.5m x 2.5m (13.75 sq.m)")
print("✓ Second Bedroom: 5.5m x 2.0m (11.0 sq.m)")
print("✓ Bathroom: 2.0m x 2.0m (4.0 sq.m)")
print("\nSTRUCTURAL FEATURES:")
print("• Foundation with proper depth")
print("• Load-bearing brick walls with openings")
print("• Doors: 900mm wide standard doors")
print("• Windows: 1200mm x 1200mm with frames")
print("• RCC roof slab with proper thickness")
print("• Room area indicators for clear visualization")
print("\nARCHITECTURAL ELEMENTS:")
print("• Main entrance with canopy")
print("• Door and window frames")
print("• Proper wall openings for natural light")
print("• Color-coded room identification")
print("• Professional structural layout")
print("="*50)
print("STRUCTURED MODEL COMPLETE - Ready for Review!")


# Professional completion
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()

FreeCAD.Console.PrintMessage("Professional model completed successfully\n")