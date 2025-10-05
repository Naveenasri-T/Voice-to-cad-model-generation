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

# Create a new object for the apartment
apartment = doc.addObject("App::Part", "Apartment")

# Create the living room
living_room = doc.addObject("Part::Box", "Living_Room")
living_room.Length = 5000  # 5m
living_room.Width = 4000  # 4m
living_room.Height = 100  # height
living_room.Placement.Base = Base.Vector(0, 0, 0)
living_room.ViewObject.ShapeColor = (0.8, 0.8, 0.8)  # Light gray color

# Create the kitchen
kitchen = doc.addObject("Part::Box", "Kitchen")
kitchen.Length = 3000  # 3m
kitchen.Width = 3000  # 3m
kitchen.Height = 100  # height
kitchen.Placement.Base = Base.Vector(5000, 0, 0)  # Position next to living room
kitchen.ViewObject.ShapeColor = (0.7, 0.7, 0.7)  # Dark gray color

# Create the master bedroom
master_bedroom = doc.addObject("Part::Box", "Master_Bedroom")
master_bedroom.Length = 3500  # 3.5m
master_bedroom.Width = 4000  # 4m
master_bedroom.Height = 100  # height
master_bedroom.Placement.Base = Base.Vector(0, 4000, 0)  # Position above living room
master_bedroom.ViewObject.ShapeColor = (0.9, 0.9, 0.9)  # White color

# Create the second bedroom
second_bedroom = doc.addObject("Part::Box", "Second_Bedroom")
second_bedroom.Length = 3000  # 3m
second_bedroom.Width = 3000  # 3m
second_bedroom.Height = 100  # height
second_bedroom.Placement.Base = Base.Vector(5000, 4000, 0)  # Position next to master bedroom
second_bedroom.ViewObject.ShapeColor = (0.9, 0.9, 0.9)  # White color

# Create the bathroom
bathroom = doc.addObject("Part::Box", "Bathroom")
bathroom.Length = 2000  # 2m
bathroom.Width = 2000  # 2m
bathroom.Height = 100  # height
bathroom.Placement.Base = Base.Vector(8000, 2000, 0)  # Position next to second bedroom
bathroom.ViewObject.ShapeColor = (0.6, 0.6, 0.6)  # Gray color

# Add all objects to the apartment
apartment.addObject(living_room)
apartment.addObject(kitchen)
apartment.addObject(master_bedroom)
apartment.addObject(second_bedroom)
apartment.addObject(bathroom)

# Recompute the document
doc.recompute()

# Fit the view to the apartment
FreeCAD.Gui.SendMsgToActiveView("ViewFit")

# Professional completion
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()

FreeCAD.Console.PrintMessage("Professional model completed successfully\n")