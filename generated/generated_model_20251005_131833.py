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
import Draft
from FreeCAD import Base

# Create a new document
doc = FreeCAD.newDocument()

# Create a new group for the 2BHK house
house_group = doc.addObject("App::DocumentObjectGroup", "2BHK_House")

# Define the dimensions of the house
house_length = 12000  # mm
house_width = 9000  # mm
house_height = 3000  # mm

# Define the dimensions of the parking space
parking_length = 6000  # mm
parking_width = 3000  # mm
parking_height = 2500  # mm

# Create the base of the house
base = doc.addObject("Part::Box", "Base")
base.Length = house_length
base.Width = house_width
base.Height = 100  # mm
base.Placement.Base = Base.Vector(0, 0, 0)
base.ViewObject.ShapeColor = (0.8, 0.8, 0.8, 0.0)  # Grey color
base.ViewObject.Transparency = 50

# Create the walls of the house
wall1 = doc.addObject("Part::Box", "Wall1")
wall1.Length = house_length
wall1.Width = 200  # mm
wall1.Height = house_height
wall1.Placement.Base = Base.Vector(0, -house_width / 2 + 100, 100)
wall1.ViewObject.ShapeColor = (0.5, 0.5, 0.5, 0.0)  # Dark grey color
wall1.ViewObject.Transparency = 50

wall2 = doc.addObject("Part::Box", "Wall2")
wall2.Length = house_length
wall2.Width = 200  # mm
wall2.Height = house_height
wall2.Placement.Base = Base.Vector(0, house_width / 2 - 100, 100)
wall2.ViewObject.ShapeColor = (0.5, 0.5, 0.5, 0.0)  # Dark grey color
wall2.ViewObject.Transparency = 50

wall3 = doc.addObject("Part::Box", "Wall3")
wall3.Length = 200  # mm
wall3.Width = house_width - 400  # mm
wall3.Height = house_height
wall3.Placement.Base = Base.Vector(-house_length / 2 + 100, 0, 100)
wall3.ViewObject.ShapeColor = (0.5, 0.5, 0.5, 0.0)  # Dark grey color
wall3.ViewObject.Transparency = 50

wall4 = doc.addObject("Part::Box", "Wall4")
wall4.Length = 200  # mm
wall4.Width = house_width - 400  # mm
wall4.Height = house_height
wall4.Placement.Base = Base.Vector(house_length / 2 - 100, 0, 100)
wall4.ViewObject.ShapeColor = (0.5, 0.5, 0.5, 0.0)  # Dark grey color
wall4.ViewObject.Transparency = 50

# Create the roof of the house
roof = doc.addObject("Part::Box", "Roof")
roof.Length = house_length
roof.Width = house_width
roof.Height = 500  # mm
roof.Placement.Base = Base.Vector(0, 0, house_height + 100)
roof.ViewObject.ShapeColor = (0.8, 0.8, 0.8, 0.0)  # Grey color
roof.ViewObject.Transparency = 50

# Create the parking space
parking_base = doc.addObject("Part::Box", "Parking_Base")
parking_base.Length = parking_length
parking_base.Width = parking_width
parking_base.Height = 100  # mm
parking_base.Placement.Base = Base.Vector(-house_length / 2 - parking_length / 2, 0, 0)
parking_base.ViewObject.ShapeColor = (0.8, 0.8, 0.8, 0.0)  # Grey color
parking_base.ViewObject.Transparency = 50

parking_wall1 = doc.addObject("Part::Box", "Parking_Wall1")
parking_wall1.Length = parking_length
parking_wall1.Width = 200  # mm
parking_wall1.Height = parking_height
parking_wall1.Placement.Base = Base.Vector(-house_length / 2 - parking_length / 2, -parking_width / 2 + 100, 100)
parking_wall1.ViewObject.ShapeColor = (0.5, 0.5, 0.5, 0.0)  # Dark grey color
parking_wall1.ViewObject.Transparency = 50

parking_wall2 = doc.addObject("Part::Box", "Parking_Wall2")
parking_wall2.Length = parking_length
parking_wall2.Width = 200  # mm
parking_wall2.Height = parking_height
parking_wall2.Placement.Base = Base.Vector(-house_length / 2 - parking_length / 2, parking_width / 2 - 100, 100)
parking_wall2.ViewObject.ShapeColor = (0.5, 0.5, 0.5, 0.0)  # Dark grey color
parking_wall2.ViewObject.Transparency = 50

parking_wall3 = doc.addObject("Part::Box", "Parking_Wall3")
parking_wall3.Length = 200  # mm
parking_wall3.Width = parking_width - 400  # mm
parking_wall3.Height = parking_height
parking_wall3.Placement.Base = Base.Vector(-house_length / 2 - parking_length / 2 - 100, 0, 100)
parking_wall3.ViewObject.ShapeColor = (0.5, 0.5, 0.5, 0.0)  # Dark grey color
parking_wall3.ViewObject.Transparency = 50

parking_wall4 = doc.addObject("Part::Box", "Parking_Wall4")
parking_wall4.Length = 200  # mm
parking_wall4.Width = parking_width - 400  # mm
parking_wall4.Height = parking_height
parking_wall4.Placement.Base = Base.Vector(-house_length / 2 - parking_length / 2 + parking_length - 100, 0, 100)
parking_wall4.ViewObject.ShapeColor = (0.5, 0.5, 0.5, 0.0)  # Dark grey color
parking_wall4.ViewObject.Transparency = 50

# Add all objects to the house group
house_group.addObject(base)
house_group.addObject(wall1)
house_group.addObject(wall2)
house_group.addObject(wall3)
house_group.addObject(wall4)
house_group.addObject(roof)
house_group.addObject(parking_base)
house_group.addObject(parking_wall1)
house_group.addObject(parking_wall2)
house_group.addObject(parking_wall3)
house_group.addObject(parking_wall4)

# Recompute the document
doc.recompute()

# Fit the view to the entire model
FreeCAD.Gui.SendMsgToActiveView("ViewFit")

# Professional completion
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()

FreeCAD.Console.PrintMessage("Professional model completed successfully\n")