# Import necessary modules
import FreeCAD
import Part
from FreeCAD import Base

# Create a new document
doc = FreeCAD.newDocument()

# Create a new object for the house
house = doc.addObject("Part::Feature", "House")

# Define the dimensions of the house
house_length = 12000  # mm
house_width = 9000  # mm
house_height = 3000  # mm

# Create the base of the house
base = Part.makeBox(house_length, house_width, 100)  # 100 mm thick base
base.translate(Base.Vector(0, 0, 0))  # Position the base at the origin

# Create the walls of the house
wall_thickness = 200  # mm
wall_height = house_height - 100  # Subtract the base thickness
wall1 = Part.makeBox(house_length, wall_thickness, wall_height)
wall1.translate(Base.Vector(0, -house_width / 2 + wall_thickness / 2, 100))  # Position the wall
wall2 = Part.makeBox(house_length, wall_thickness, wall_height)
wall2.translate(Base.Vector(0, house_width / 2 - wall_thickness / 2, 100))  # Position the wall
wall3 = Part.makeBox(wall_thickness, house_width, wall_height)
wall3.translate(Base.Vector(-house_length / 2 + wall_thickness / 2, 0, 100))  # Position the wall
wall4 = Part.makeBox(wall_thickness, house_width, wall_height)
wall4.translate(Base.Vector(house_length / 2 - wall_thickness / 2, 0, 100))  # Position the wall

# Create the roof of the house
roof_thickness = 100  # mm
roof = Part.makeBox(house_length, house_width, roof_thickness)
roof.translate(Base.Vector(0, 0, house_height - roof_thickness))  # Position the roof

# Create the rooms
# Living room
living_room_length = 6000  # mm
living_room_width = 4000  # mm
living_room_height = 2500  # mm
living_room = Part.makeBox(living_room_length, living_room_width, living_room_height)
living_room.translate(Base.Vector(-house_length / 2 + living_room_length / 2, -house_width / 2 + living_room_width / 2, 100))  # Position the living room

# Kitchen
kitchen_length = 3000  # mm
kitchen_width = 3000  # mm
kitchen_height = 2500  # mm
kitchen = Part.makeBox(kitchen_length, kitchen_width, kitchen_height)
kitchen.translate(Base.Vector(house_length / 2 - kitchen_length / 2, -house_width / 2 + kitchen_width / 2, 100))  # Position the kitchen

# Bedroom 1
bedroom1_length = 4000  # mm
bedroom1_width = 4000  # mm
bedroom1_height = 2500  # mm
bedroom1 = Part.makeBox(bedroom1_length, bedroom1_width, bedroom1_height)
bedroom1.translate(Base.Vector(-house_length / 2 + bedroom1_length / 2, house_width / 2 - bedroom1_width / 2, 100))  # Position the bedroom

# Bedroom 2
bedroom2_length = 4000  # mm
bedroom2_width = 4000  # mm
bedroom2_height = 2500  # mm
bedroom2 = Part.makeBox(bedroom2_length, bedroom2_width, bedroom2_height)
bedroom2.translate(Base.Vector(house_length / 2 - bedroom2_length / 2, house_width / 2 - bedroom2_width / 2, 100))  # Position the bedroom

# Create a compound of all the objects
compound = Part.makeCompound([base, wall1, wall2, wall3, wall4, roof, living_room, kitchen, bedroom1, bedroom2])

# Add the compound to the document
doc.addObject("Part::Feature", "Compound").Shape = compound

# Apply materials
# Walls
wall_material = doc.addObject("App::MaterialObject")
wall_material.Label = "Wall Material"
wall_material.Material = "Brick"
wall1_material = doc.addObject("App::MaterialObject")
wall1_material.Label = "Wall1 Material"
wall1_material.Material = "Brick"
wall1_material.Parent = wall1
wall2_material = doc.addObject("App::MaterialObject")
wall2_material.Label = "Wall2 Material"
wall2_material.Material = "Brick"
wall2_material.Parent = wall2
wall3_material = doc.addObject("App::MaterialObject")
wall3_material.Label = "Wall3 Material"
wall3_material.Material = "Brick"
wall3_material.Parent = wall3
wall4_material = doc.addObject("App::MaterialObject")
wall4_material.Label = "Wall4 Material"
wall4_material.Material = "Brick"
wall4_material.Parent = wall4

# Roof
roof_material = doc.addObject("App::MaterialObject")
roof_material.Label = "Roof Material"
roof_material.Material = "Asphalt"

# Rooms
living_room_material = doc.addObject("App::MaterialObject")
living_room_material.Label = "Living Room Material"
living_room_material.Material = "Wood"
kitchen_material = doc.addObject("App::MaterialObject")
kitchen_material.Label = "Kitchen Material"
kitchen_material.Material = "Tile"
bedroom1_material = doc.addObject("App::MaterialObject")
bedroom1_material.Label = "Bedroom1 Material"
bedroom1_material.Material = "Carpet"
bedroom2_material = doc.addObject("App::MaterialObject")
bedroom2_material.Label = "Bedroom2 Material"
bedroom2_material.Material = "Carpet"

# Recompute the document
doc.recompute()

# Fit the view to the document
FreeCAD.Gui.SendMsgToActiveView("ViewFit")