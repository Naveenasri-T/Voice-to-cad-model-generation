import FreeCAD, Part, Draft, FreeCADGui
import math

doc = FreeCAD.newDocument("3BHK_House_With_Parking")

# STEP 1: Foundation
foundation = doc.addObject("Part::Feature", "Foundation")
foundation.Shape = Part.makeBox(14000, 12000, 600)
foundation.Placement.Base = FreeCAD.Vector(-1000, -1000, -600)
foundation.ViewObject.ShapeColor = (0.3, 0.3, 0.3)

# STEP 2: INDIVIDUAL ROOM FLOORS (MANDATORY)
# Living Room Floor (4m x 5m)
living_room_floor = doc.addObject("Part::Feature", "LivingRoom_Floor")
living_room_floor.Shape = Part.makeBox(4000, 5000, 150)
living_room_floor.Placement.Base = FreeCAD.Vector(0, 0, 0)
living_room_floor.ViewObject.ShapeColor = (0.9, 0.9, 0.8)

# Master Bedroom Floor (4m x 3.5m)
master_bed_floor = doc.addObject("Part::Feature", "MasterBed_Floor")
master_bed_floor.Shape = Part.makeBox(4000, 3500, 150)
master_bed_floor.Placement.Base = FreeCAD.Vector(4200, 0, 0)
master_bed_floor.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

# Bedroom 2 Floor (3m x 3m)
bed2_floor = doc.addObject("Part::Feature", "Bedroom2_Floor")
bed2_floor.Shape = Part.makeBox(3000, 3000, 150)
bed2_floor.Placement.Base = FreeCAD.Vector(4200, 3700, 0)
bed2_floor.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

# Bedroom 3 Floor (3m x 3m)
bed3_floor = doc.addObject("Part::Feature", "Bedroom3_Floor")
bed3_floor.Shape = Part.makeBox(3000, 3000, 150)
bed3_floor.Placement.Base = FreeCAD.Vector(4200, 7000, 0)
bed3_floor.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

# Kitchen Floor (3m x 2.5m)
kitchen_floor = doc.addObject("Part::Feature", "Kitchen_Floor")
kitchen_floor.Shape = Part.makeBox(3000, 2500, 150)
kitchen_floor.Placement.Base = FreeCAD.Vector(0, 5200, 0)
kitchen_floor.ViewObject.ShapeColor = (0.8, 0.9, 0.8)

# Bathroom 1 Floor (2m x 2m)
bath1_floor = doc.addObject("Part::Feature", "Bathroom1_Floor")
bath1_floor.Shape = Part.makeBox(2000, 2000, 150)
bath1_floor.Placement.Base = FreeCAD.Vector(8400, 0, 0)
bath1_floor.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

# Bathroom 2 Floor (2m x 2m)
bath2_floor = doc.addObject("Part::Feature", "Bathroom2_Floor")
bath2_floor.Shape = Part.makeBox(2000, 2000, 150)
bath2_floor.Placement.Base = FreeCAD.Vector(8400, 2200, 0)
bath2_floor.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

# Bathroom 3 Floor (2m x 2m)
bath3_floor = doc.addObject("Part::Feature", "Bathroom3_Floor")
bath3_floor.Shape = Part.makeBox(2000, 2000, 150)
bath3_floor.Placement.Base = FreeCAD.Vector(8400, 4400, 0)
bath3_floor.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

# Parking Area Floor (5m x 3m)
parking_floor = doc.addObject("Part::Feature", "Parking_Floor")
parking_floor.Shape = Part.makeBox(5000, 3000, 100)
parking_floor.Placement.Base = FreeCAD.Vector(10500, 0, -100)
parking_floor.ViewObject.ShapeColor = (0.7, 0.7, 0.7)

# STEP 3: ROOM-SPECIFIC WALLS
# Living Room Walls
living_room_wall1 = doc.addObject("Part::Feature", "LivingRoom_Wall1")
living_room_wall1.Shape = Part.makeBox(150, 5000, 3000)
living_room_wall1.Placement.Base = FreeCAD.Vector(0, 0, 150)
living_room_wall1.ViewObject.ShapeColor = (0.9, 0.9, 0.8)

living_room_wall2 = doc.addObject("Part::Feature", "LivingRoom_Wall2")
living_room_wall2.Shape = Part.makeBox(4000, 150, 3000)
living_room_wall2.Placement.Base = FreeCAD.Vector(0, 5000, 150)
living_room_wall2.ViewObject.ShapeColor = (0.9, 0.9, 0.8)

living_room_wall3 = doc.addObject("Part::Feature", "LivingRoom_Wall3")
living_room_wall3.Shape = Part.makeBox(150, 5000, 3000)
living_room_wall3.Placement.Base = FreeCAD.Vector(4000, 0, 150)
living_room_wall3.ViewObject.ShapeColor = (0.9, 0.9, 0.8)

living_room_wall4 = doc.addObject("Part::Feature", "LivingRoom_Wall4")
living_room_wall4.Shape = Part.makeBox(4000, 150, 3000)
living_room_wall4.Placement.Base = FreeCAD.Vector(0, 0, 150)
living_room_wall4.ViewObject.ShapeColor = (0.9, 0.9, 0.8)

# Master Bedroom Walls
master_bed_wall1 = doc.addObject("Part::Feature", "MasterBed_Wall1")
master_bed_wall1.Shape = Part.makeBox(150, 3500, 3000)
master_bed_wall1.Placement.Base = FreeCAD.Vector(4200, 0, 150)
master_bed_wall1.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

master_bed_wall2 = doc.addObject("Part::Feature", "MasterBed_Wall2")
master_bed_wall2.Shape = Part.makeBox(4000, 150, 3000)
master_bed_wall2.Placement.Base = FreeCAD.Vector(4200, 3500, 150)
master_bed_wall2.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

master_bed_wall3 = doc.addObject("Part::Feature", "MasterBed_Wall3")
master_bed_wall3.Shape = Part.makeBox(150, 3500, 3000)
master_bed_wall3.Placement.Base = FreeCAD.Vector(8200, 0, 150)
master_bed_wall3.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

master_bed_wall4 = doc.addObject("Part::Feature", "MasterBed_Wall4")
master_bed_wall4.Shape = Part.makeBox(4000, 150, 3000)
master_bed_wall4.Placement.Base = FreeCAD.Vector(4200, 0, 150)
master_bed_wall4.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

# Bedroom 2 Walls
bed2_wall1 = doc.addObject("Part::Feature", "Bedroom2_Wall1")
bed2_wall1.Shape = Part.makeBox(150, 3000, 3000)
bed2_wall1.Placement.Base = FreeCAD.Vector(4200, 3700, 150)
bed2_wall1.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

bed2_wall2 = doc.addObject("Part::Feature", "Bedroom2_Wall2")
bed2_wall2.Shape = Part.makeBox(3000, 150, 3000)
bed2_wall2.Placement.Base = FreeCAD.Vector(4200, 6700, 150)
bed2_wall2.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

bed2_wall3 = doc.addObject("Part::Feature", "Bedroom2_Wall3")
bed2_wall3.Shape = Part.makeBox(150, 3000, 3000)
bed2_wall3.Placement.Base = FreeCAD.Vector(7500, 3700, 150)
bed2_wall3.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

bed2_wall4 = doc.addObject("Part::Feature", "Bedroom2_Wall4")
bed2_wall4.Shape = Part.makeBox(3000, 150, 3000)
bed2_wall4.Placement.Base = FreeCAD.Vector(4200, 3700, 150)
bed2_wall4.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

# Bedroom 3 Walls
bed3_wall1 = doc.addObject("Part::Feature", "Bedroom3_Wall1")
bed3_wall1.Shape = Part.makeBox(150, 3000, 3000)
bed3_wall1.Placement.Base = FreeCAD.Vector(4200, 7000, 150)
bed3_wall1.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

bed3_wall2 = doc.addObject("Part::Feature", "Bedroom3_Wall2")
bed3_wall2.Shape = Part.makeBox(3000, 150, 3000)
bed3_wall2.Placement.Base = FreeCAD.Vector(4200, 10000, 150)
bed3_wall2.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

bed3_wall3 = doc.addObject("Part::Feature", "Bedroom3_Wall3")
bed3_wall3.Shape = Part.makeBox(150, 3000, 3000)
bed3_wall3.Placement.Base = FreeCAD.Vector(7500, 7000, 150)
bed3_wall3.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

bed3_wall4 = doc.addObject("Part::Feature", "Bedroom3_Wall4")
bed3_wall4.Shape = Part.makeBox(3000, 150, 3000)
bed3_wall4.Placement.Base = FreeCAD.Vector(4200, 7000, 150)
bed3_wall4.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

# Kitchen Walls
kitchen_wall1 = doc.addObject("Part::Feature", "Kitchen_Wall1")
kitchen_wall1.Shape = Part.makeBox(150, 2500, 3000)
kitchen_wall1.Placement.Base = FreeCAD.Vector(0, 5200, 150)
kitchen_wall1.ViewObject.ShapeColor = (0.8, 0.9, 0.8)

kitchen_wall2 = doc.addObject("Part::Feature", "Kitchen_Wall2")
kitchen_wall2.Shape = Part.makeBox(3000, 150, 3000)
kitchen_wall2.Placement.Base = FreeCAD.Vector(0, 7700, 150)
kitchen_wall2.ViewObject.ShapeColor = (0.8, 0.9, 0.8)

kitchen_wall3 = doc.addObject("Part::Feature", "Kitchen_Wall3")
kitchen_wall3.Shape = Part.makeBox(150, 2500, 3000)
kitchen_wall3.Placement.Base = FreeCAD.Vector(3000, 5200, 150)
kitchen_wall3.ViewObject.ShapeColor = (0.8, 0.9, 0.8)

kitchen_wall4 = doc.addObject("Part::Feature", "Kitchen_Wall4")
kitchen_wall4.Shape = Part.makeBox(3000, 150, 3000)
kitchen_wall4.Placement.Base = FreeCAD.Vector(0, 5200, 150)
kitchen_wall4.ViewObject.ShapeColor = (0.8, 0.9, 0.8)

# Bathroom 1 Walls
bath1_wall1 = doc.addObject("Part::Feature", "Bathroom1_Wall1")
bath1_wall1.Shape = Part.makeBox(150, 2000, 3000)
bath1_wall1.Placement.Base = FreeCAD.Vector(8400, 0, 150)
bath1_wall1.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

bath1_wall2 = doc.addObject("Part::Feature", "Bathroom1_Wall2")
bath1_wall2.Shape = Part.makeBox(2000, 150, 3000)
bath1_wall2.Placement.Base = FreeCAD.Vector(8400, 2000, 150)
bath1_wall2.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

bath1_wall3 = doc.addObject("Part::Feature", "Bathroom1_Wall3")
bath1_wall3.Shape = Part.makeBox(150, 2000, 3000)
bath1_wall3.Placement.Base = FreeCAD.Vector(10600, 0, 150)
bath1_wall3.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

bath1_wall4 = doc.addObject("Part::Feature", "Bathroom1_Wall4")
bath1_wall4.Shape = Part.makeBox(2000, 150, 3000)
bath1_wall4.Placement.Base = FreeCAD.Vector(8400, 0, 150)
bath1_wall4.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

# Bathroom 2 Walls
bath2_wall1 = doc.addObject("Part::Feature", "Bathroom2_Wall1")
bath2_wall1.Shape = Part.makeBox(150, 2000, 3000)
bath2_wall1.Placement.Base = FreeCAD.Vector(8400, 2200, 150)
bath2_wall1.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

bath2_wall2 = doc.addObject("Part::Feature", "Bathroom2_Wall2")
bath2_wall2.Shape = Part.makeBox(2000, 150, 3000)
bath2_wall2.Placement.Base = FreeCAD.Vector(8400, 4200, 150)
bath2_wall2.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

bath2_wall3 = doc.addObject("Part::Feature", "Bathroom2_Wall3")
bath2_wall3.Shape = Part.makeBox(150, 2000, 3000)
bath2_wall3.Placement.Base = FreeCAD.Vector(10600, 2200, 150)
bath2_wall3.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

bath2_wall4 = doc.addObject("Part::Feature", "Bathroom2_Wall4")
bath2_wall4.Shape = Part.makeBox(2000, 150, 3000)
bath2_wall4.Placement.Base = FreeCAD.Vector(8400, 2200, 150)
bath2_wall4.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

# Bathroom 3 Walls
bath3_wall1 = doc.addObject("Part::Feature", "Bathroom3_Wall1")
bath3_wall1.Shape = Part.makeBox(150, 2000, 3000)
bath3_wall1.Placement.Base = FreeCAD.Vector(8400, 4400, 150)
bath3_wall1.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

bath3_wall2 = doc.addObject("Part::Feature", "Bathroom3_Wall2")
bath3_wall2.Shape = Part.makeBox(2000, 150, 3000)
bath3_wall2.Placement.Base = FreeCAD.Vector(8400, 6400, 150)
bath3_wall2.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

bath3_wall3 = doc.addObject("Part::Feature", "Bathroom3_Wall3")
bath3_wall3.Shape = Part.makeBox(150, 2000, 3000)
bath3_wall3.Placement.Base = FreeCAD.Vector(10600, 4400, 150)
bath3_wall3.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

bath3_wall4 = doc.addObject("Part::Feature", "Bathroom3_Wall4")
bath3_wall4.Shape = Part.makeBox(2000, 150, 3000)
bath3_wall4.Placement.Base = FreeCAD.Vector(8400, 4400, 150)
bath3_wall4.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

# Parking Area Walls
parking_wall1 = doc.addObject("Part::Feature", "Parking_Wall1")
parking_wall1.Shape = Part.makeBox(150, 3000, 100)
parking_wall1.Placement.Base = FreeCAD.Vector(10500, 0, -100)
parking_wall1.ViewObject.ShapeColor = (0.7, 0.7, 0.7)

parking_wall2 = doc.addObject("Part::Feature", "Parking_Wall2")
parking_wall2.Shape = Part.makeBox(5000, 150, 100)
parking_wall2.Placement.Base = FreeCAD.Vector(10500, 3000, -100)
parking_wall2.ViewObject.ShapeColor = (0.7, 0.7, 0.7)

parking_wall3 = doc.addObject("Part::Feature", "Parking_Wall3")
parking_wall3.Shape = Part.makeBox(150, 3000, 100)
parking_wall3.Placement.Base = FreeCAD.Vector(15500, 0, -100)
parking_wall3.ViewObject.ShapeColor = (0.7, 0.7, 0.7)

parking_wall4 = doc.addObject("Part::Feature", "Parking_Wall4")
parking_wall4.Shape = Part.makeBox(5000, 150, 100)
parking_wall4.Placement.Base = FreeCAD.Vector(10500, 0, -100)
parking_wall4.ViewObject.ShapeColor = (0.7, 0.7, 0.7)

# STEP 4: WINDOWS FOR EACH ROOM
# Living Room Windows
living_room_window1 = doc.addObject("Part::Feature", "LivingRoom_Window1")
living_room_window1.Shape = Part.makeBox(1000, 1500, 100)
living_room_window1.Placement.Base = FreeCAD.Vector(1000, 2000, 2800)
living_room_window1.ViewObject.ShapeColor = (0.9, 0.9, 0.8)

living_room_window2 = doc.addObject("Part::Feature", "LivingRoom_Window2")
living_room_window2.Shape = Part.makeBox(1000, 1500, 100)
living_room_window2.Placement.Base = FreeCAD.Vector(3000, 2000, 2800)
living_room_window2.ViewObject.ShapeColor = (0.9, 0.9, 0.8)

# Master Bedroom Windows
master_bed_window1 = doc.addObject("Part::Feature", "MasterBed_Window1")
master_bed_window1.Shape = Part.makeBox(1000, 1500, 100)
master_bed_window1.Placement.Base = FreeCAD.Vector(5200, 1000, 2800)
master_bed_window1.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

master_bed_window2 = doc.addObject("Part::Feature", "MasterBed_Window2")
master_bed_window2.Shape = Part.makeBox(1000, 1500, 100)
master_bed_window2.Placement.Base = FreeCAD.Vector(7200, 1000, 2800)
master_bed_window2.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

# Bedroom 2 Windows
bed2_window1 = doc.addObject("Part::Feature", "Bedroom2_Window1")
bed2_window1.Shape = Part.makeBox(1000, 1500, 100)
bed2_window1.Placement.Base = FreeCAD.Vector(5200, 4700, 2800)
bed2_window1.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

bed2_window2 = doc.addObject("Part::Feature", "Bedroom2_Window2")
bed2_window2.Shape = Part.makeBox(1000, 1500, 100)
bed2_window2.Placement.Base = FreeCAD.Vector(7200, 4700, 2800)
bed2_window2.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

# Bedroom 3 Windows
bed3_window1 = doc.addObject("Part::Feature", "Bedroom3_Window1")
bed3_window1.Shape = Part.makeBox(1000, 1500, 100)
bed3_window1.Placement.Base = FreeCAD.Vector(5200, 8000, 2800)
bed3_window1.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

bed3_window2 = doc.addObject("Part::Feature", "Bedroom3_Window2")
bed3_window2.Shape = Part.makeBox(1000, 1500, 100)
bed3_window2.Placement.Base = FreeCAD.Vector(7200, 8000, 2800)
bed3_window2.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

# Kitchen Windows
kitchen_window1 = doc.addObject("Part::Feature", "Kitchen_Window1")
kitchen_window1.Shape = Part.makeBox(1000, 1500, 100)
kitchen_window1.Placement.Base = FreeCAD.Vector(100, 6200, 2800)
kitchen_window1.ViewObject.ShapeColor = (0.8, 0.9, 0.8)

# Bathroom 1 Windows
bath1_window1 = doc.addObject("Part::Feature", "Bathroom1_Window1")
bath1_window1.Shape = Part.makeBox(500, 1000, 100)
bath1_window1.Placement.Base = FreeCAD.Vector(8700, 500, 2800)
bath1_window1.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

# Bathroom 2 Windows
bath2_window1 = doc.addObject("Part::Feature", "Bathroom2_Window1")
bath2_window1.Shape = Part.makeBox(500, 1000, 100)
bath2_window1.Placement.Base = FreeCAD.Vector(8700, 2700, 2800)
bath2_window1.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

# Bathroom 3 Windows
bath3_window1 = doc.addObject("Part::Feature", "Bathroom3_Window1")
bath3_window1.Shape = Part.makeBox(500, 1000, 100)
bath3_window1.Placement.Base = FreeCAD.Vector(8700, 4900, 2800)
bath3_window1.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

# STEP 5: DOORS BETWEEN ROOMS
# Living Room Door
living_room_door = doc.addObject("Part::Feature", "LivingRoom_Door")
living_room_door.Shape = Part.makeBox(1000, 200, 3000)
living_room_door.Placement.Base = FreeCAD.Vector(2000, 0, 150)
living_room_door.ViewObject.ShapeColor = (0.9, 0.9, 0.8)

# Master Bedroom Door
master_bed_door = doc.addObject("Part::Feature", "MasterBed_Door")
master_bed_door.Shape = Part.makeBox(1000, 200, 3000)
master_bed_door.Placement.Base = FreeCAD.Vector(4200, 0, 150)
master_bed_door.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

# Bedroom 2 Door
bed2_door = doc.addObject("Part::Feature", "Bedroom2_Door")
bed2_door.Shape = Part.makeBox(1000, 200, 3000)
bed2_door.Placement.Base = FreeCAD.Vector(4200, 3700, 150)
bed2_door.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

# Bedroom 3 Door
bed3_door = doc.addObject("Part::Feature", "Bedroom3_Door")
bed3_door.Shape = Part.makeBox(1000, 200, 3000)
bed3_door.Placement.Base = FreeCAD.Vector(4200, 7000, 150)
bed3_door.ViewObject.ShapeColor = (0.95, 0.9, 0.85)

# Kitchen Door
kitchen_door = doc.addObject("Part::Feature", "Kitchen_Door")
kitchen_door.Shape = Part.makeBox(1000, 200, 3000)
kitchen_door.Placement.Base = FreeCAD.Vector(0, 5200, 150)
kitchen_door.ViewObject.ShapeColor = (0.8, 0.9, 0.8)

# Bathroom 1 Door
bath1_door = doc.addObject("Part::Feature", "Bathroom1_Door")
bath1_door.Shape = Part.makeBox(500, 200, 3000)
bath1_door.Placement.Base = FreeCAD.Vector(8400, 0, 150)
bath1_door.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

# Bathroom 2 Door
bath2_door = doc.addObject("Part::Feature", "Bathroom2_Door")
bath2_door.Shape = Part.makeBox(500, 200, 3000)
bath2_door.Placement.Base = FreeCAD.Vector(8400, 2200, 150)
bath2_door.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

# Bathroom 3 Door
bath3_door = doc.addObject("Part::Feature", "Bathroom3_Door")
bath3_door.Shape = Part.makeBox(500, 200, 3000)
bath3_door.Placement.Base = FreeCAD.Vector(8400, 4400, 150)
bath3_door.ViewObject.ShapeColor = (0.8, 0.8, 0.9)

# Parking Area Door
parking_door = doc.addObject("Part::Feature", "Parking_Door")
parking_door.Shape = Part.makeBox(2000, 200, 100)
parking_door.Placement.Base = FreeCAD.Vector(10500, 0, -100)
parking_door.ViewObject.ShapeColor = (0.7, 0.7, 0.7)

# STEP 6: ROOF STRUCTURE
# Roof
roof = doc.addObject("Part::Feature", "Roof")
roof.Shape = Part.makeBox(14000, 12000, 500)
roof.Placement.Base = FreeCAD.Vector(-1000, -1000, 3500)
roof.ViewObject.ShapeColor = (0.5, 0.5, 0.5)