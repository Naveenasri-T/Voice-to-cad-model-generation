"""
PERFECT INTEGRATED ARCHITECTURAL MODEL EXAMPLE
==============================================

This example shows EXACTLY what the AI should generate:
A unified, realistic building with proper integration.
"""

import FreeCAD
import Part
import Draft

doc = FreeCAD.newDocument("Perfect_Integrated_2BHK")

print("=== ARCHITECTURAL ANALYSIS ===")
print("Building Type: 2BHK Residential House")
print("Required Spaces: Living Room, Master Bedroom, Second Bedroom, Kitchen, Bathroom")
print("Integration Strategy: Single unified structure with shared walls and logical layout")

# STEP 1: CALCULATE TOTAL BUILDING SIZE BASED ON ROOM REQUIREMENTS
print("\n=== PARAMETRIC CALCULATIONS ===")

# Room sizes based on architectural standards
living_room_size = (5000, 4000)    # 5m x 4m = 20 sq.m
master_bedroom_size = (4000, 3500) # 4m x 3.5m = 14 sq.m  
second_bedroom_size = (3500, 3000) # 3.5m x 3m = 10.5 sq.m
kitchen_size = (3000, 2500)        # 3m x 2.5m = 7.5 sq.m
bathroom_size = (2500, 2000)       # 2.5m x 2m = 5 sq.m

# Calculate total building dimensions for efficient layout
# Layout: Living room + Kitchen in front, Bedrooms + Bathroom in back
total_building_length = living_room_size[0] + kitchen_size[0]  # 8000mm = 8m
total_building_width = max(living_room_size[1] + master_bedroom_size[1], 7500)  # 7500mm = 7.5m

wall_thickness = 200  # 200mm structural walls
ceiling_height = 3000 # 3m ceiling height

print(f"Total Building: {total_building_length}mm x {total_building_width}mm")
print(f"Living Room: {living_room_size[0]}mm x {living_room_size[1]}mm")
print(f"Master Bedroom: {master_bedroom_size[0]}mm x {master_bedroom_size[1]}mm")
print(f"Kitchen: {kitchen_size[0]}mm x {kitchen_size[1]}mm")

print("\n=== BUILDING INTEGRATED STRUCTURE ===")

# STEP 2: CREATE SINGLE UNIFIED FOUNDATION
foundation = doc.addObject("Part::Box", "Foundation")
foundation.Length = total_building_length
foundation.Width = total_building_width
foundation.Height = 150  # 150mm foundation slab
foundation.Placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), FreeCAD.Rotation(0, 0, 0))
foundation.ViewObject.ShapeColor = (0.3, 0.3, 0.3)  # Dark concrete
print("✓ Unified foundation: Single slab supporting entire building")

# STEP 3: CREATE PERIMETER WALLS (BUILDING ENVELOPE)
print("✓ Creating perimeter walls...")

# Front wall (street-facing)
front_wall = doc.addObject("Part::Box", "Front_Wall")
front_wall.Length = total_building_length
front_wall.Width = wall_thickness
front_wall.Height = ceiling_height
front_wall.Placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, 150), FreeCAD.Rotation(0, 0, 0))
front_wall.ViewObject.ShapeColor = (0.9, 0.85, 0.7)  # Warm beige

# Back wall
back_wall = doc.addObject("Part::Box", "Back_Wall")
back_wall.Length = total_building_length
back_wall.Width = wall_thickness
back_wall.Height = ceiling_height
back_wall.Placement = FreeCAD.Placement(FreeCAD.Vector(0, total_building_width - wall_thickness, 150), FreeCAD.Rotation(0, 0, 0))
back_wall.ViewObject.ShapeColor = (0.9, 0.85, 0.7)

# Left wall
left_wall = doc.addObject("Part::Box", "Left_Wall")
left_wall.Length = wall_thickness
left_wall.Width = total_building_width
left_wall.Height = ceiling_height
left_wall.Placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, 150), FreeCAD.Rotation(0, 0, 0))
left_wall.ViewObject.ShapeColor = (0.9, 0.85, 0.7)

# Right wall
right_wall = doc.addObject("Part::Box", "Right_Wall")
right_wall.Length = wall_thickness
right_wall.Width = total_building_width
right_wall.Height = ceiling_height
right_wall.Placement = FreeCAD.Placement(FreeCAD.Vector(total_building_length - wall_thickness, 0, 150), FreeCAD.Rotation(0, 0, 0))
right_wall.ViewObject.ShapeColor = (0.9, 0.85, 0.7)

# STEP 4: CREATE INTERIOR PARTITION WALLS (LOGICAL ROOM DIVISION)
print("✓ Creating interior partition walls...")

# Main partition wall separating front rooms from back bedrooms
main_partition = doc.addObject("Part::Box", "Main_Partition")
main_partition.Length = total_building_length - 2 * wall_thickness
main_partition.Width = wall_thickness
main_partition.Height = ceiling_height
main_partition.Placement = FreeCAD.Placement(FreeCAD.Vector(wall_thickness, living_room_size[1], 150), FreeCAD.Rotation(0, 0, 0))
main_partition.ViewObject.ShapeColor = (0.9, 0.85, 0.7)

# Partition between living room and kitchen
living_kitchen_partition = doc.addObject("Part::Box", "Living_Kitchen_Partition")
living_kitchen_partition.Length = wall_thickness
living_kitchen_partition.Width = living_room_size[1] - 2 * wall_thickness
living_kitchen_partition.Height = ceiling_height
living_kitchen_partition.Placement = FreeCAD.Placement(FreeCAD.Vector(living_room_size[0], wall_thickness, 150), FreeCAD.Rotation(0, 0, 0))
living_kitchen_partition.ViewObject.ShapeColor = (0.9, 0.85, 0.7)

# Partition between master bedroom and second bedroom
bedroom_partition = doc.addObject("Part::Box", "Bedroom_Partition")
bedroom_partition.Length = wall_thickness
bedroom_partition.Width = total_building_width - living_room_size[1] - 2 * wall_thickness
bedroom_partition.Height = ceiling_height
bedroom_partition.Placement = FreeCAD.Placement(FreeCAD.Vector(master_bedroom_size[0] + wall_thickness, living_room_size[1] + wall_thickness, 150), FreeCAD.Rotation(0, 0, 0))
bedroom_partition.ViewObject.ShapeColor = (0.9, 0.85, 0.7)

# STEP 5: CREATE SINGLE UNIFIED ROOF
roof = doc.addObject("Part::Box", "Roof")
roof.Length = total_building_length + 400  # 200mm overhang each side
roof.Width = total_building_width + 400
roof.Height = 150  # 150mm roof slab
roof.Placement = FreeCAD.Placement(FreeCAD.Vector(-200, -200, ceiling_height + 150), FreeCAD.Rotation(0, 0, 0))
roof.ViewObject.ShapeColor = (0.8, 0.2, 0.1)  # Terracotta red
print("✓ Unified roof: Single structure covering entire building")

# STEP 6: CREATE FLOOR FINISH
floor = doc.addObject("Part::Box", "Floor_Finish")
floor.Length = total_building_length - 2 * wall_thickness
floor.Width = total_building_width - 2 * wall_thickness
floor.Height = 20  # 20mm floor finish
floor.Placement = FreeCAD.Placement(FreeCAD.Vector(wall_thickness, wall_thickness, 150), FreeCAD.Rotation(0, 0, 0))
floor.ViewObject.ShapeColor = (0.9, 0.8, 0.6)  # Light wood finish
print("✓ Floor finish: Continuous flooring throughout building")

# STEP 7: ADD DOORS AND WINDOWS AT LOGICAL POSITIONS
print("✓ Adding doors and windows...")

# Main entrance door (center of front wall in living room area)
main_door = doc.addObject("Part::Box", "Main_Door")
door_width = 900
door_height = 2100
main_door.Length = door_width
main_door.Width = 100
main_door.Height = door_height
door_x = living_room_size[0] / 2 - door_width / 2  # Center in living room
main_door.Placement = FreeCAD.Placement(FreeCAD.Vector(door_x, -50, 150), FreeCAD.Rotation(0, 0, 0))
main_door.ViewObject.ShapeColor = (0.6, 0.3, 0.1)  # Brown wood

# Living room window (front wall for natural light)
living_window = doc.addObject("Part::Box", "Living_Window")
window_width = 1500
window_height = 1200
living_window.Length = window_width
living_window.Width = 100
living_window.Height = window_height
window_x = living_room_size[0] - window_width - 500  # Leave space for furniture
living_window.Placement = FreeCAD.Placement(FreeCAD.Vector(window_x, -50, 150 + 800), FreeCAD.Rotation(0, 0, 0))
living_window.ViewObject.ShapeColor = (0.7, 0.9, 1.0)  # Light blue glass

# Master bedroom window (back wall)
master_window = doc.addObject("Part::Box", "Master_Window")
master_window.Length = 1200
master_window.Width = 100  
master_window.Height = 1200
master_window.Placement = FreeCAD.Placement(FreeCAD.Vector(wall_thickness + 1000, total_building_width - 50, 150 + 800), FreeCAD.Rotation(0, 0, 0))
master_window.ViewObject.ShapeColor = (0.7, 0.9, 1.0)

# Kitchen window (right wall)
kitchen_window = doc.addObject("Part::Box", "Kitchen_Window")
kitchen_window.Length = 100
kitchen_window.Width = 1000
kitchen_window.Height = 1000
kitchen_window.Placement = FreeCAD.Placement(FreeCAD.Vector(total_building_length - 50, wall_thickness + 1000, 150 + 1000), FreeCAD.Rotation(0, 0, 0))
kitchen_window.ViewObject.ShapeColor = (0.7, 0.9, 1.0)

# STEP 8: ADD ROOM LABELS WITH AREAS
print("✓ Adding room labels...")

# Living room label
living_label = Draft.makeText(["LIVING ROOM", "20.0 sq.m"], FreeCAD.Vector(living_room_size[0]/2, living_room_size[1]/2, ceiling_height + 200))
living_label.ViewObject.FontSize = 300
living_label.ViewObject.TextColor = (0, 0, 0)

# Master bedroom label  
master_label = Draft.makeText(["MASTER BEDROOM", "14.0 sq.m"], FreeCAD.Vector(wall_thickness + master_bedroom_size[0]/2, living_room_size[1] + wall_thickness + master_bedroom_size[1]/2, ceiling_height + 200))
master_label.ViewObject.FontSize = 300
master_label.ViewObject.TextColor = (0, 0, 0)

# Kitchen label
kitchen_label = Draft.makeText(["KITCHEN", "7.5 sq.m"], FreeCAD.Vector(living_room_size[0] + wall_thickness + kitchen_size[0]/2, kitchen_size[1]/2, ceiling_height + 200))
kitchen_label.ViewObject.FontSize = 300
kitchen_label.ViewObject.TextColor = (0, 0, 0)

# FINALIZE INTEGRATED MODEL
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()

print("\n=== ARCHITECTURAL MODEL SUMMARY ===")
print(f"✓ Total Building Area: {(total_building_length * total_building_width) / 1000000:.1f} sq.m")
print("✓ Room Areas:")
print(f"   - Living Room: {(living_room_size[0] * living_room_size[1]) / 1000000:.1f} sq.m")
print(f"   - Master Bedroom: {(master_bedroom_size[0] * master_bedroom_size[1]) / 1000000:.1f} sq.m")
print(f"   - Kitchen: {(kitchen_size[0] * kitchen_size[1]) / 1000000:.1f} sq.m")
print("✓ Structural Elements:")
print(f"   - Foundation: {total_building_length}mm x {total_building_width}mm")
print(f"   - Walls: {wall_thickness}mm thick, {ceiling_height}mm high")
print(f"   - Roof: Single structure with overhangs")
print("✓ Integration Features:")
print("   - Unified foundation supporting entire building")
print("   - Shared walls between rooms (no duplication)")
print("   - Single roof covering all spaces")
print("   - Logical room connections and circulation")
print("   - Professional materials and color scheme")

print("\n🏗️ PERFECT INTEGRATED ARCHITECTURAL MODEL COMPLETE!")
print("This is exactly what the AI should generate - a unified, realistic building!")

"""
THIS EXAMPLE SHOWS THE CORRECT OUTPUT:

✅ SINGLE UNIFIED FOUNDATION covering entire footprint
✅ PERIMETER WALLS forming building envelope
✅ INTERIOR PARTITIONS at specific coordinates (not 0,0,0)
✅ SINGLE ROOF covering everything with overhangs
✅ DOORS AND WINDOWS at logical positions
✅ ROOM LABELS with calculated areas
✅ PROFESSIONAL MATERIALS and colors
✅ REALISTIC PROPORTIONS based on human use
✅ INTEGRATED STRUCTURE - everything connects properly

This is REAL ARCHITECTURE, not scattered boxes!
"""