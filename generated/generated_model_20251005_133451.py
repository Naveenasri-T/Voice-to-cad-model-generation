"""
Professional FreeCAD Model - Client Ready
Generated with Enterprise AI Technology
"""

import FreeCAD
import Part

# Create professional document
doc = FreeCAD.newDocument("ProfessionalModel")
FreeCAD.Console.PrintMessage("=== Professional Model Generation ===\n")

# Import necessary modules
import FreeCAD
import Part
from FreeCAD import Base

# Create a new document
doc = FreeCAD.newDocument()

# Create a new group for the house
house_group = doc.addObject("App::DocumentObjectGroup", "House")

# Define the dimensions of the house
house_length = 15000  # mm
house_width = 10000  # mm
house_height = 6000  # mm

# Define the dimensions of the parking
parking_length = 5000  # mm
parking_width = 3000  # mm
parking_height = 2500  # mm

# Create the base of the house
base = doc.addObject("Part::Box", "Base")
base.Length = house_length
base.Width = house_width
base.Height = 500  # mm
base.Placement.Base = Base.Vector(0, 0, 0)
base.Label = "Base"

# Add the base to the house group
house_group.addObject(base)

# Create the walls of the house
wall_thickness = 200  # mm
wall_height = house_height - 500  # mm

# Create the front wall
front_wall = doc.addObject("Part::Box", "Front Wall")
front_wall.Length = house_width
front_wall.Width = wall_thickness
front_wall.Height = wall_height
front_wall.Placement.Base = Base.Vector(0, 0, 500)
front_wall.Label = "Front Wall"

# Add the front wall to the house group
house_group.addObject(front_wall)

# Create the back wall
back_wall = doc.addObject("Part::Box", "Back Wall")
back_wall.Length = house_width
back_wall.Width = wall_thickness
back_wall.Height = wall_height
back_wall.Placement.Base = Base.Vector(house_length - wall_thickness, 0, 500)
back_wall.Label = "Back Wall"

# Add the back wall to the house group
house_group.addObject(back_wall)

# Create the left wall
left_wall = doc.addObject("Part::Box", "Left Wall")
left_wall.Length = house_length - 2 * wall_thickness
left_wall.Width = wall_thickness
left_wall.Height = wall_height
left_wall.Placement.Base = Base.Vector(wall_thickness, 0, 500)
left_wall.Label = "Left Wall"

# Add the left wall to the house group
house_group.addObject(left_wall)

# Create the right wall
right_wall = doc.addObject("Part::Box", "Right Wall")
right_wall.Length = house_length - 2 * wall_thickness
right_wall.Width = wall_thickness
right_wall.Height = wall_height
right_wall.Placement.Base = Base.Vector(wall_thickness, house_width - wall_thickness, 500)
right_wall.Label = "Right Wall"

# Add the right wall to the house group
house_group.addObject(right_wall)

# Create the roof
roof = doc.addObject("Part::Box", "Roof")
roof.Length = house_length
roof.Width = house_width
roof.Height = 1000  # mm
roof.Placement.Base = Base.Vector(0, 0, house_height - 1000)
roof.Label = "Roof"

# Add the roof to the house group
house_group.addObject(roof)

# Create the parking
parking = doc.addObject("Part::Box", "Parking")
parking.Length = parking_length
parking.Width = parking_width
parking.Height = parking_height
parking.Placement.Base = Base.Vector(house_length - parking_length, -parking_width, 0)
parking.Label = "Parking"

# Add the parking to the house group
house_group.addObject(parking)

# Apply materials to the objects
base.Material = "Concrete"
front_wall.Material = "Brick"
back_wall.Material = "Brick"
left_wall.Material = "Brick"
right_wall.Material = "Brick"
roof.Material = "Asphalt"
parking.Material = "Concrete"

# Apply colors to the objects
base.ViewObject.ShapeColor = (0.5, 0.5, 0.5)  # Gray
front_wall.ViewObject.ShapeColor = (1, 0, 0)  # Red
back_wall.ViewObject.ShapeColor = (1, 0, 0)  # Red
left_wall.ViewObject.ShapeColor = (1, 0, 0)  # Red
right_wall.ViewObject.ShapeColor = (1, 0, 0)  # Red
roof.ViewObject.ShapeColor = (0, 0, 0)  # Black
parking.ViewObject.ShapeColor = (0.5, 0.5, 0.5)  # Gray

# Recompute the document
doc.recompute()

# Fit the view to the objects
FreeCAD.Gui.SendMsgToActiveView("ViewFit")

# Professional completion
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()

FreeCAD.Console.PrintMessage("Professional model completed successfully\n")