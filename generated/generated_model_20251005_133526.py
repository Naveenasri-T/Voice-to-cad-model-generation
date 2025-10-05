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
base.Placement = Base.Placement(Base.Vector(0, 0, 0), Base.Rotation(0, 0, 0))
base.ViewObject.ShapeColor = (0.8, 0.8, 0.8, 0.0)  # Grey color
base.ViewObject.Transparency = 50

# Create the walls of the house
wall1 = doc.addObject("Part::Box", "Wall1")
wall1.Length = house_length
wall1.Width = 500  # mm
wall1.Height = house_height
wall1.Placement = Base.Placement(Base.Vector(0, house_width / 2 - 250, 500), Base.Rotation(0, 0, 0))
wall1.ViewObject.ShapeColor = (0.5, 0.5, 0.5, 0.0)  # Dark grey color
wall1.ViewObject.Transparency = 50

wall2 = doc.addObject("Part::Box", "Wall2")
wall2.Length = house_length
wall2.Width = 500  # mm
wall2.Height = house_height
wall2.Placement = Base.Placement(Base.Vector(0, -house_width / 2 + 250, 500), Base.Rotation(0, 0, 0))
wall2.ViewObject.ShapeColor = (0.5, 0.5, 0.5, 0.0)  # Dark grey color
wall2.ViewObject.Transparency = 50

wall3 = doc.addObject("Part::Box", "Wall3")
wall3.Length = 500  # mm
wall3.Width = house_width
wall3.Height = house_height
wall3.Placement = Base.Placement(Base.Vector(house_length / 2 - 250, 0, 500), Base.Rotation(0, 0, 0))
wall3.ViewObject.ShapeColor = (0.5, 0.5, 0.5, 0.0)  # Dark grey color
wall3.ViewObject.Transparency = 50

wall4 = doc.addObject("Part::Box", "Wall4")
wall4.Length = 500  # mm
wall4.Width = house_width
wall4.Height = house_height
wall4.Placement = Base.Placement(Base.Vector(-house_length / 2 + 250, 0, 500), Base.Rotation(0, 0, 0))
wall4.ViewObject.ShapeColor = (0.5, 0.5, 0.5, 0.0)  # Dark grey color
wall4.ViewObject.Transparency = 50

# Create the roof of the house
roof = doc.addObject("Part::Box", "Roof")
roof.Length = house_length
roof.Width = house_width
roof.Height = 500  # mm
roof.Placement = Base.Placement(Base.Vector(0, 0, house_height), Base.Rotation(0, 0, 0))
roof.ViewObject.ShapeColor = (0.8, 0.8, 0.8, 0.0)  # Grey color
roof.ViewObject.Transparency = 50

# Create the parking
parking = doc.addObject("Part::Box", "Parking")
parking.Length = parking_length
parking.Width = parking_width
parking.Height = parking_height
parking.Placement = Base.Placement(Base.Vector(-house_length / 2 - parking_length / 2, 0, 0), Base.Rotation(0, 0, 0))
parking.ViewObject.ShapeColor = (0.5, 0.5, 0.5, 0.0)  # Dark grey color
parking.ViewObject.Transparency = 50

# Add the objects to the house group
house_group.addObject(base)
house_group.addObject(wall1)
house_group.addObject(wall2)
house_group.addObject(wall3)
house_group.addObject(wall4)
house_group.addObject(roof)
house_group.addObject(parking)

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