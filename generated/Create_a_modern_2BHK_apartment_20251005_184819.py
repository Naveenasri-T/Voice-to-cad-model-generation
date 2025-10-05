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

# Create a new group for the apartment
apartment_group = doc.addObject("App::Part", "Apartment")

# Create the living room
living_room_length = 5000  # mm
living_room_width = 4000  # mm
living_room_height = 2500  # mm
living_room = doc.addObject("Part::Box", "Living_Room")
living_room.Length = living_room_length
living_room.Width = living_room_width
living_room.Height = living_room_height
living_room.ViewObject.ShapeColor = (0.8, 0.8, 0.8)  # Light gray color
apartment_group.addObject(living_room)

# Create the kitchen
kitchen_length = 3000  # mm
kitchen_width = 3000  # mm
kitchen_height = 2500  # mm
kitchen = doc.addObject("Part::Box", "Kitchen")
kitchen.Length = kitchen_length
kitchen.Width = kitchen_width
kitchen.Height = kitchen_height
kitchen.Placement.Base = Base.Vector(living_room_length, 0, 0)  # Position the kitchen next to the living room
kitchen.ViewObject.ShapeColor = (0.7, 0.7, 0.7)  # Dark gray color
apartment_group.addObject(kitchen)

# Create the master bedroom
master_bedroom_length = 3500  # mm
master_bedroom_width = 4000  # mm
master_bedroom_height = 2500  # mm
master_bedroom = doc.addObject("Part::Box", "Master_Bedroom")
master_bedroom.Length = master_bedroom_length
master_bedroom.Width = master_bedroom_width
master_bedroom.Height = master_bedroom_height
master_bedroom.Placement.Base = Base.Vector(0, living_room_width, 0)  # Position the master bedroom above the living room
master_bedroom.ViewObject.ShapeColor = (0.9, 0.9, 0.9)  # White color
apartment_group.addObject(master_bedroom)

# Create the second bedroom
second_bedroom_length = 3000  # mm
second_bedroom_width = 3000  # mm
second_bedroom_height = 2500  # mm
second_bedroom = doc.addObject("Part::Box", "Second_Bedroom")
second_bedroom.Length = second_bedroom_length
second_bedroom.Width = second_bedroom_width
second_bedroom.Height = second_bedroom_height
second_bedroom.Placement.Base = Base.Vector(master_bedroom_length, living_room_width, 0)  # Position the second bedroom next to the master bedroom
second_bedroom.ViewObject.ShapeColor = (0.7, 0.7, 0.7)  # Dark gray color
apartment_group.addObject(second_bedroom)

# Create the bathroom
bathroom_length = 2000  # mm
bathroom_width = 2000  # mm
bathroom_height = 2500  # mm
bathroom = doc.addObject("Part::Box", "Bathroom")
bathroom.Length = bathroom_length
bathroom.Width = bathroom_width
bathroom.Height = bathroom_height
bathroom.Placement.Base = Base.Vector(living_room_length + kitchen_length, living_room_width, 0)  # Position the bathroom next to the kitchen
bathroom.ViewObject.ShapeColor = (0.6, 0.6, 0.6)  # Dark gray color
apartment_group.addObject(bathroom)

# Recompute the document and fit the view
doc.recompute()
FreeCAD.Gui.SendMsgToActiveView("ViewFit")

# Professional completion
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()

FreeCAD.Console.PrintMessage("Professional model completed successfully\n")