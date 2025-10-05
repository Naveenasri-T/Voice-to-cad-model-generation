import FreeCAD, Part, Draft, Arch, FreeCADGui
import math

doc = FreeCAD.newDocument("Professional_Model")

command = "Create a 3BHK house with parking"

if "2bhk" in command.lower():
    building_length = 8000  # 8 meters
    building_width = 6000   # 6 meters
elif "3bhk" in command.lower():
    building_length = 10000  # 10 meters 
    building_width = 8000    # 8 meters
else:
    building_length = 12000  # Default large
    building_width = 10000

wall_thickness = 200
floor_height = 3000
foundation_depth = 500

foundation = doc.addObject("Part::Feature", "Foundation")
foundation.Shape = Part.makeBox(building_length, building_width, foundation_depth)
foundation.Placement.Base = FreeCAD.Vector(0, 0, 0)
foundation.ViewObject.ShapeColor = (0.4, 0.4, 0.4)

ext_wall_1 = doc.addObject("Part::Feature", "ExtWall_1")
ext_wall_1.Shape = Part.makeBox(building_length, wall_thickness, floor_height)
ext_wall_1.Placement.Base = FreeCAD.Vector(0, 0, foundation_depth)
ext_wall_1.ViewObject.ShapeColor = (0.8, 0.8, 0.7)

ext_wall_2 = doc.addObject("Part::Feature", "ExtWall_2")
ext_wall_2.Shape = Part.makeBox(wall_thickness, building_width, floor_height)
ext_wall_2.Placement.Base = FreeCAD.Vector(0, 0, foundation_depth)
ext_wall_2.ViewObject.ShapeColor = (0.8, 0.8, 0.7)

ext_wall_3 = doc.addObject("Part::Feature", "ExtWall_3")
ext_wall_3.Shape = Part.makeBox(building_length, wall_thickness, floor_height)
ext_wall_3.Placement.Base = FreeCAD.Vector(0, building_width - wall_thickness, foundation_depth)
ext_wall_3.ViewObject.ShapeColor = (0.8, 0.8, 0.7)

ext_wall_4 = doc.addObject("Part::Feature", "ExtWall_4")
ext_wall_4.Shape = Part.makeBox(wall_thickness, building_width, floor_height)
ext_wall_4.Placement.Base = FreeCAD.Vector(building_length - wall_thickness, 0, foundation_depth)
ext_wall_4.ViewObject.ShapeColor = (0.8, 0.8, 0.7)

int_wall_1 = doc.addObject("Part::Feature", "IntWall_1")
int_wall_1.Shape = Part.makeBox(100, 4000, floor_height)
int_wall_1.Placement.Base = FreeCAD.Vector(1000, 1000, foundation_depth)
int_wall_1.ViewObject.ShapeColor = (0.9, 0.9, 0.9)

int_wall_2 = doc.addObject("Part::Feature", "IntWall_2")
int_wall_2.Shape = Part.makeBox(100, 4000, floor_height)
int_wall_2.Placement.Base = FreeCAD.Vector(3000, 1000, foundation_depth)
int_wall_2.ViewObject.ShapeColor = (0.9, 0.9, 0.9)

int_wall_3 = doc.addObject("Part::Feature", "IntWall_3")
int_wall_3.Shape = Part.makeBox(4000, 100, floor_height)
int_wall_3.Placement.Base = FreeCAD.Vector(1000, 3000, foundation_depth)
int_wall_3.ViewObject.ShapeColor = (0.9, 0.9, 0.9)

window_1 = doc.addObject("Part::Feature", "Window_1")
window_1.Shape = Part.makeBox(1000, 1200, 100)
window_1.Placement.Base = FreeCAD.Vector(1500, 100, foundation_depth + floor_height - 100)
window_1.ViewObject.ShapeColor = (0.2, 0.4, 0.8, 0.7)
window_1.ViewObject.Transparency = 50

window_2 = doc.addObject("Part::Feature", "Window_2")
window_2.Shape = Part.makeBox(1000, 1200, 100)
window_2.Placement.Base = FreeCAD.Vector(3500, 100, foundation_depth + floor_height - 100)
window_2.ViewObject.ShapeColor = (0.2, 0.4, 0.8, 0.7)
window_2.ViewObject.Transparency = 50

door_1 = doc.addObject("Part::Feature", "Door_1")
door_1.Shape = Part.makeBox(900, 2100, 100)
door_1.Placement.Base = FreeCAD.Vector(100, 1500, foundation_depth + floor_height - 100)
door_1.ViewObject.ShapeColor = (0.6, 0.3, 0.1)

floor = doc.addObject("Part::Feature", "Floor")
floor.Shape = Part.makeBox(building_length, building_width, 150)
floor.Placement.Base = FreeCAD.Vector(0, 0, foundation_depth)
floor.ViewObject.ShapeColor = (0.9, 0.9, 0.8)

roof = doc.addObject("Part::Feature", "Roof")
roof.Shape = Part.makeBox(building_length, building_width, 200)
roof.Placement.Base = FreeCAD.Vector(0, 0, foundation_depth + floor_height)
roof.ViewObject.ShapeColor = (0.4, 0.4, 0.4)

doc.recompute()
FreeCADGui.activeDocument().activeView().viewAxometric()

# Professional view settings for client presentation
try:
    import FreeCADGui
    view = FreeCADGui.activeDocument().activeView()
    view.viewAxometric()
    view.fitAll()
    # Enhanced rendering for professional appearance
    FreeCADGui.runCommand("Std_DrawStyle", 4)  # Flat lines + Shaded
    FreeCADGui.runCommand("Std_ToggleClipPlane", 0)
except:
    pass