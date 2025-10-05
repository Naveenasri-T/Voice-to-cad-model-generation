import FreeCAD, Part, Draft, FreeCADGui
import math

doc = FreeCAD.newDocument("Professional_Model")

# Building dimensions
building_length = 10000
building_width = 8000

# Standard measurements
wall_thickness = 200
floor_height = 3000
foundation_depth = 600

# Foundation:
foundation = doc.addObject("Part::Feature", "Foundation")
foundation.Shape = Part.makeBox(building_length + 1000, building_width + 1000, foundation_depth)
foundation.Placement.Base = FreeCAD.Vector(-500, -500, -foundation_depth)
foundation.ViewObject.ShapeColor = (0.3, 0.3, 0.3)

# Create rooms
# Living Room (4m x 5m)
living_room_floor = doc.addObject("Part::Feature", "LivingRoom_Floor")
living_room_floor.Shape = Part.makeBox(4000, 5000, 150)
living_room_floor.Placement.Base = FreeCAD.Vector(0, 0, 0)
living_room_floor.ViewObject.ShapeColor = (0.9, 0.9, 0.8)

# Master Bedroom (4m x 3.5m)
master_bed_floor = doc.addObject("Part::Feature", "MasterBed_Floor")
master_bed_floor.Shape = Part.makeBox(4000, 3500, 150)
master_bed_floor.Placement.Base = FreeCAD.Vector(4200, 0, 0)
master_bed_floor.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

# Bedroom 2 (3m x 3m)
bed2_floor = doc.addObject("Part::Feature", "Bedroom2_Floor")
bed2_floor.Shape = Part.makeBox(3000, 3000, 150)
bed2_floor.Placement.Base = FreeCAD.Vector(4200, 3700, 0)
bed2_floor.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

# Bedroom 3 (3m x 3m)
bed3_floor = doc.addObject("Part::Feature", "Bedroom3_Floor")
bed3_floor.Shape = Part.makeBox(3000, 3000, 150)
bed3_floor.Placement.Base = FreeCAD.Vector(4200, 7000, 0)
bed3_floor.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

# Kitchen (3m x 2.5m)
kitchen_floor = doc.addObject("Part::Feature", "Kitchen_Floor")
kitchen_floor.Shape = Part.makeBox(3000, 2500, 150)
kitchen_floor.Placement.Base = FreeCAD.Vector(0, 5200, 0)
kitchen_floor.ViewObject.ShapeColor = (0.8, 0.9, 0.8)

# Bathroom 1 (2m x 2m)
bath1_floor = doc.addObject("Part::Feature", "Bathroom1_Floor")
bath1_floor.Shape = Part.makeBox(2000, 2000, 150)
bath1_floor.Placement.Base = FreeCAD.Vector(8400, 0, 0)
bath1_floor.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

# Bathroom 2 (2m x 1.8m)
bath2_floor = doc.addObject("Part::Feature", "Bathroom2_Floor")
bath2_floor.Shape = Part.makeBox(2000, 1800, 150)
bath2_floor.Placement.Base = FreeCAD.Vector(8400, 2200, 0)
bath2_floor.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

# Create walls
# Living room walls
living_wall_1 = doc.addObject("Part::Feature", "Living_Wall_1")
living_wall_1.Shape = Part.makeBox(4000, 200, 3000)
living_wall_1.Placement.Base = FreeCAD.Vector(0, -200, 150)
living_wall_1.ViewObject.ShapeColor = (0.8, 0.8, 0.7)

living_wall_2 = doc.addObject("Part::Feature", "Living_Wall_2")
living_wall_2.Shape = Part.makeBox(200, 5000, 3000)
living_wall_2.Placement.Base = FreeCAD.Vector(-200, 0, 150)
living_wall_2.ViewObject.ShapeColor = (0.8, 0.8, 0.7)

# Master bedroom walls
master_wall_1 = doc.addObject("Part::Feature", "Master_Wall_1")
master_wall_1.Shape = Part.makeBox(4000, 200, 3000)
master_wall_1.Placement.Base = FreeCAD.Vector(4200, -200, 150)
master_wall_1.ViewObject.ShapeColor = (0.8, 0.8, 0.7)

master_wall_2 = doc.addObject("Part::Feature", "Master_Wall_2")
master_wall_2.Shape = Part.makeBox(200, 3500, 3000)
master_wall_2.Placement.Base = FreeCAD.Vector(8000, 0, 150)
master_wall_2.ViewObject.ShapeColor = (0.8, 0.8, 0.7)

# Bedroom 2 walls
bed2_wall_1 = doc.addObject("Part::Feature", "Bedroom2_Wall_1")
bed2_wall_1.Shape = Part.makeBox(3000, 200, 3000)
bed2_wall_1.Placement.Base = FreeCAD.Vector(4200, 3700 - 200, 150)
bed2_wall_1.ViewObject.ShapeColor = (0.8, 0.8, 0.7)

bed2_wall_2 = doc.addObject("Part::Feature", "Bedroom2_Wall_2")
bed2_wall_2.Shape = Part.makeBox(200, 3000, 3000)
bed2_wall_2.Placement.Base = FreeCAD.Vector(4200 - 200, 3700, 150)
bed2_wall_2.ViewObject.ShapeColor = (0.8, 0.8, 0.7)

# Bedroom 3 walls
bed3_wall_1 = doc.addObject("Part::Feature", "Bedroom3_Wall_1")
bed3_wall_1.Shape = Part.makeBox(3000, 200, 3000)
bed3_wall_1.Placement.Base = FreeCAD.Vector(4200, 7000 - 200, 150)
bed3_wall_1.ViewObject.ShapeColor = (0.8, 0.8, 0.7)

bed3_wall_2 = doc.addObject("Part::Feature", "Bedroom3_Wall_2")
bed3_wall_2.Shape = Part.makeBox(200, 3000, 3000)
bed3_wall_2.Placement.Base = FreeCAD.Vector(4200 - 200, 7000, 150)
bed3_wall_2.ViewObject.ShapeColor = (0.8, 0.8, 0.7)

# Kitchen walls
kitchen_wall_1 = doc.addObject("Part::Feature", "Kitchen_Wall_1")
kitchen_wall_1.Shape = Part.makeBox(3000, 200, 3000)
kitchen_wall_1.Placement.Base = FreeCAD.Vector(0, 5200 - 200, 150)
kitchen_wall_1.ViewObject.ShapeColor = (0.8, 0.8, 0.7)

kitchen_wall_2 = doc.addObject("Part::Feature", "Kitchen_Wall_2")
kitchen_wall_2.Shape = Part.makeBox(200, 2500, 3000)
kitchen_wall_2.Placement.Base = FreeCAD.Vector(-200, 5200, 150)
kitchen_wall_2.ViewObject.ShapeColor = (0.8, 0.8, 0.7)

# Create windows and doors
# Living room window
living_window = doc.addObject("Part::Feature", "Living_Window")
living_window.Shape = Part.makeBox(1500, 100, 1200)
living_window.Placement.Base = FreeCAD.Vector(1250, -250, 800)
living_window.ViewObject.ShapeColor = (0.2, 0.4, 0.8)
living_window.ViewObject.Transparency = 70

# Master bedroom window
master_window = doc.addObject("Part::Feature", "Master_Window")
master_window.Shape = Part.makeBox(1200, 100, 1200)
master_window.Placement.Base = FreeCAD.Vector(5600, -250, 800)
master_window.ViewObject.ShapeColor = (0.2, 0.4, 0.8)
master_window.ViewObject.Transparency = 70

# Bedroom 2 window
bed2_window = doc.addObject("Part::Feature", "Bedroom2_Window")
bed2_window.Shape = Part.makeBox(1000, 100, 1200)
bed2_window.Placement.Base = FreeCAD.Vector(4800, 3700 - 250, 800)
bed2_window.ViewObject.ShapeColor = (0.2, 0.4, 0.8)
bed2_window.ViewObject.Transparency = 70

# Bedroom 3 window
bed3_window = doc.addObject("Part::Feature", "Bedroom3_Window")
bed3_window.Shape = Part.makeBox(1000, 100, 1200)
bed3