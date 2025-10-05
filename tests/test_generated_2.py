# Import necessary modules
import FreeCAD
import Part
import Draft
import FreeCADGui

# Create a new document
doc = FreeCAD.newDocument()

# Define the dimensions of the house
house_length = 12000  # mm
house_width = 9000  # mm
house_height = 3000  # mm

# Define the dimensions of the rooms
bedroom1_length = 4000  # mm
bedroom1_width = 3000  # mm
bedroom2_length = 3500  # mm
bedroom2_width = 3000  # mm
living_room_length = 6000  # mm
living_room_width = 4000  # mm
kitchen_length = 3000  # mm
kitchen_width = 2500  # mm
bathroom_length = 2000  # mm
bathroom_width = 1500  # mm

# Create the base of the house
base = Part.makeBox(house_length, house_width, 100)  # 100 mm thick base
base.translate(FreeCAD.Base.Vector(-house_length/2, -house_width/2, 0))

# Create the walls of the house
wall1 = Part.makeBox(house_length, 200, house_height)  # 200 mm thick wall
wall1.translate(FreeCAD.Base.Vector(-house_length/2, -house_width/2 + house_width - 200, 100))
wall2 = Part.makeBox(house_length, 200, house_height)  # 200 mm thick wall
wall2.translate(FreeCAD.Base.Vector(-house_length/2, -house_width/2, 100))
wall3 = Part.makeBox(200, house_width, house_height)  # 200 mm thick wall
wall3.translate(FreeCAD.Base.Vector(-house_length/2 + house_length - 200, -house_width/2, 100))
wall4 = Part.makeBox(200, house_width, house_height)  # 200 mm thick wall
wall4.translate(FreeCAD.Base.Vector(-house_length/2, -house_width/2, 100))

# Create the rooms
bedroom1 = Part.makeBox(bedroom1_length, bedroom1_width, house_height)
bedroom1.translate(FreeCAD.Base.Vector(-house_length/2 + 500, -house_width/2 + 500, 100))
bedroom2 = Part.makeBox(bedroom2_length, bedroom2_width, house_height)
bedroom2.translate(FreeCAD.Base.Vector(-house_length/2 + 500, -house_width/2 + bedroom1_width + 500, 100))
living_room = Part.makeBox(living_room_length, living_room_width, house_height)
living_room.translate(FreeCAD.Base.Vector(-house_length/2 + bedroom1_length + 500, -house_width/2 + 500, 100))
kitchen = Part.makeBox(kitchen_length, kitchen_width, house_height)
kitchen.translate(FreeCAD.Base.Vector(-house_length/2 + bedroom1_length + living_room_length + 500, -house_width/2 + 500, 100))
bathroom = Part.makeBox(bathroom_length, bathroom_width, house_height)
bathroom.translate(FreeCAD.Base.Vector(-house_length/2 + bedroom1_length + living_room_length + kitchen_length + 500, -house_width/2 + 500, 100))

# Create the roof
roof = Part.makeBox(house_length, house_width, 500)  # 500 mm thick roof
roof.translate(FreeCAD.Base.Vector(-house_length/2, -house_width/2, house_height + 100))

# Add the objects to the document
doc.addObject("Part::Feature", "Base").Shape = base
doc.addObject("Part::Feature", "Wall1").Shape = wall1
doc.addObject("Part::Feature", "Wall2").Shape = wall2
doc.addObject("Part::Feature", "Wall3").Shape = wall3
doc.addObject("Part::Feature", "Wall4").Shape = wall4
doc.addObject("Part::Feature", "Bedroom1").Shape = bedroom1
doc.addObject("Part::Feature", "Bedroom2").Shape = bedroom2
doc.addObject("Part::Feature", "LivingRoom").Shape = living_room
doc.addObject("Part::Feature", "Kitchen").Shape = kitchen
doc.addObject("Part::Feature", "Bathroom").Shape = bathroom
doc.addObject("Part::Feature", "Roof").Shape = roof

# Recompute the document and fit the view
doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.viewAxometric()
FreeCADGui.ActiveView.fitAll()