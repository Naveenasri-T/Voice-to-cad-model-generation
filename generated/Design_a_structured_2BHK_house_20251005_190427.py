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

# Create a new object for the house
house = doc.addObject("Part::Feature", "House")

# Define the dimensions of the rooms
living_room_length = 5.5
living_room_width = 3.5
kitchen_length = 2.5
kitchen_width = 2.5
master_bedroom_length = 5.5
master_bedroom_width = 2.5
second_bedroom_length = 5.5
second_bedroom_width = 2.0
bathroom_length = 2.0
bathroom_width = 2.0

# Define the height of the house
house_height = 3.0

# Create the living room
living_room = doc.addObject("Part::Box", "Living Room")
living_room.Length = living_room_length
living_room.Width = living_room_width
living_room.Height = house_height
living_room.ViewObject.ShapeColor = (0.8, 0.8, 0.8)  # Light gray color
living_room.ViewObject.Transparency = 0.0

# Create the kitchen
kitchen = doc.addObject("Part::Box", "Kitchen")
kitchen.Length = kitchen_length
kitchen.Width = kitchen_width
kitchen.Height = house_height
kitchen.Placement.Base = Base.Vector(living_room_length, 0, 0)
kitchen.ViewObject.ShapeColor = (0.5, 0.5, 0.5)  # Dark gray color
kitchen.ViewObject.Transparency = 0.0

# Create the master bedroom
master_bedroom = doc.addObject("Part::Box", "Master Bedroom")
master_bedroom.Length = master_bedroom_length
master_bedroom.Width = master_bedroom_width
master_bedroom.Height = house_height
master_bedroom.Placement.Base = Base.Vector(0, living_room_width, 0)
master_bedroom.ViewObject.ShapeColor = (0.7, 0.7, 0.7)  # Medium gray color
master_bedroom.ViewObject.Transparency = 0.0

# Create the second bedroom
second_bedroom = doc.addObject("Part::Box", "Second Bedroom")
second_bedroom.Length = second_bedroom_length
second_bedroom.Width = second_bedroom_width
second_bedroom.Height = house_height
second_bedroom.Placement.Base = Base.Vector(0, living_room_width + master_bedroom_width, 0)
second_bedroom.ViewObject.ShapeColor = (0.6, 0.6, 0.6)  # Dark gray color
second_bedroom.ViewObject.Transparency = 0.0

# Create the bathroom
bathroom = doc.addObject("Part::Box", "Bathroom")
bathroom.Length = bathroom_length
bathroom.Width = bathroom_width
bathroom.Height = house_height
bathroom.Placement.Base = Base.Vector(living_room_length + kitchen_length, living_room_width + master_bedroom_width, 0)
bathroom.ViewObject.ShapeColor = (0.4, 0.4, 0.4)  # Dark gray color
bathroom.ViewObject.Transparency = 0.0

# Create a compound of all the rooms
compound = doc.addObject("Part::Compound", "House Compound")
compound.Links = [living_room, kitchen, master_bedroom, second_bedroom, bathroom]

# Create a floor for the house
floor = doc.addObject("Part::Box", "Floor")
floor.Length = living_room_length + kitchen_length + 1.0
floor.Width = living_room_width + master_bedroom_width + second_bedroom_width + 1.0
floor.Height = 0.1
floor.Placement.Base = Base.Vector(-0.5, -0.5, 0)
floor.ViewObject.ShapeColor = (0.9, 0.9, 0.9)  # Light gray color
floor.ViewObject.Transparency = 0.0

# Create walls for the house
wall1 = doc.addObject("Part::Box", "Wall 1")
wall1.Length = living_room_length + kitchen_length + 1.0
wall1.Width = 0.2
wall1.Height = house_height
wall1.Placement.Base = Base.Vector(-0.5, -0.5, 0.1)
wall1.ViewObject.ShapeColor = (0.3, 0.3, 0.3)  # Dark gray color
wall1.ViewObject.Transparency = 0.0

wall2 = doc.addObject("Part::Box", "Wall 2")
wall2.Length = 0.2
wall2.Width = living_room_width + master_bedroom_width + second_bedroom_width + 1.0
wall2.Height = house_height
wall2.Placement.Base = Base.Vector(-0.5, -0.5, 0.1)
wall2.ViewObject.ShapeColor = (0.3, 0.3, 0.3)  # Dark gray color
wall2.ViewObject.Transparency = 0.0

wall3 = doc.addObject("Part::Box", "Wall 3")
wall3.Length = living_room_length + kitchen_length + 1.0
wall3.Width = 0.2
wall3.Height = house_height
wall3.Placement.Base = Base.Vector(-0.5, living_room_width + master_bedroom_width + second_bedroom_width + 0.5, 0.1)
wall3.ViewObject.ShapeColor = (0.3, 0.3, 0.3)  # Dark gray color
wall3.ViewObject.Transparency = 0.0

wall4 = doc.addObject("Part::Box", "Wall 4")
wall4.Length = 0.2
wall4.Width = living_room_width + master_bedroom_width + second_bedroom_width + 1.0
wall4.Height = house_height
wall4.Placement.Base = Base.Vector(living_room_length + kitchen_length + 0.5, -0.5, 0.1)
wall4.ViewObject.ShapeColor = (0.3, 0.3, 0.3)  # Dark gray color
wall4.ViewObject.Transparency = 0.0

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