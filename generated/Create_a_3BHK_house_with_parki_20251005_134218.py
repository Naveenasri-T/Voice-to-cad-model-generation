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

# Create the walls of the house
wall1 = doc.addObject("Part::Box", "Wall1")
wall1.Length = house_length
wall1.Width = 500  # mm
wall1.Height = house_height
wall1.Placement.Base = Base.Vector(0, house_width / 2 - 250, 500)
wall1.Label = "Wall1"

wall2 = doc.addObject("Part::Box", "Wall2")
wall2.Length = house_length
wall2.Width = 500  # mm
wall2.Height = house_height
wall2.Placement.Base = Base.Vector(0, -house_width / 2 + 250, 500)
wall2.Label = "Wall2"

wall3 = doc.addObject("Part::Box", "Wall3")
wall3.Length = 500  # mm
wall3.Width = house_width
wall3.Height = house_height
wall3.Placement.Base = Base.Vector(house_length / 2 - 250, 0, 500)
wall3.Label = "Wall3"

wall4 = doc.addObject("Part::Box", "Wall4")
wall4.Length = 500  # mm
wall4.Width = house_width
wall4.Height = house_height
wall4.Placement.Base = Base.Vector(-house_length / 2 + 250, 0, 500)
wall4.Label = "Wall4"

# Create the roof of the house
roof = doc.addObject("Part::Box", "Roof")
roof.Length = house_length
roof.Width = house_width
roof.Height = 500  # mm
roof.Placement.Base = Base.Vector(0, 0, house_height)
roof.Label = "Roof"

# Create the parking
parking = doc.addObject("Part::Box", "Parking")
parking.Length = parking_length
parking.Width = parking_width
parking.Height = parking_height
parking.Placement.Base = Base.Vector(-house_length / 2 - parking_length / 2, 0, 0)
parking.Label = "Parking"

# Create the doors and windows
door1 = doc.addObject("Part::Box", "Door1")
door1.Length = 1500  # mm
door1.Width = 500  # mm
door1.Height = 2000  # mm
door1.Placement.Base = Base.Vector(house_length / 2 - 750, 0, 1000)
door1.Label = "Door1"

window1 = doc.addObject("Part::Box", "Window1")
window1.Length = 1000  # mm
window1.Width = 500  # mm
window1.Height = 1000  # mm
window1.Placement.Base = Base.Vector(house_length / 2 - 500, house_width / 2 - 250, 1500)
window1.Label = "Window1"

# Add the objects to the house group
house_group.addObject(base)
house_group.addObject(wall1)
house_group.addObject(wall2)
house_group.addObject(wall3)
house_group.addObject(wall4)
house_group.addObject(roof)
house_group.addObject(parking)
house_group.addObject(door1)
house_group.addObject(window1)

# Apply materials and colors
base.Material = "Concrete"
wall1.Material = "Brick"
wall2.Material = "Brick"
wall3.Material = "Brick"
wall4.Material = "Brick"
roof.Material = "Asphalt"
parking.Material = "Concrete"
door1.Material = "Wood"
window1.Material = "Glass"

# Set the colors
base.ViewObject.ShapeColor = (0.5, 0.5, 0.5)
wall1.ViewObject.ShapeColor = (1, 0, 0)
wall2.ViewObject.ShapeColor = (1, 0, 0)
wall3.ViewObject.ShapeColor = (1, 0, 0)
wall4.ViewObject.ShapeColor = (1, 0, 0)
roof.ViewObject.ShapeColor = (0, 0, 0)
parking.ViewObject.ShapeColor = (0.5, 0.5, 0.5)
door1.ViewObject.ShapeColor = (0.5, 0.2, 0)
window1.ViewObject.ShapeColor = (0, 1, 1)

# Recompute the document
doc.recompute()

# Fit the view to the house
FreeCAD.Gui.SendMsgToActiveView("ViewFit")

# Professional completion
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()

FreeCAD.Console.PrintMessage("Professional model completed successfully\n")