import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
import FreeCAD
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

# Create interior partitions for 3 bedrooms
for i in range(3):
    partition = doc.addObject("Part::Box", f"Partition_{i+1}")
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

doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
