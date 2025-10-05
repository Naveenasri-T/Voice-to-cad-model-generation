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

# Create a new group for the house
house_group = doc.addObject("App::DocumentObjectGroup", "House")

# Create the base of the house
# Define the dimensions of the base
base_length = 15000  # mm
base_width = 10000  # mm
base_height = 100  # mm

# Create the base
base = doc.addObject("Part::Box", "Base")
base.Length = base_length
base.Width = base_width
base.Height = base_height
base.Placement = Base.Placement(Base.Vector(0, 0, 0), Base.Rotation(0, 0, 0))
house_group.addObject(base)

# Apply material to the base
base.Material = FreeCAD.ActiveMaterial
base.Material.Name = "Concrete"
base.Material.DiffuseColor = (0.5, 0.5, 0.5, 1.0)

# Create the walls of the house
# Define the dimensions of the walls
wall_thickness = 200  # mm
wall_height = 3000  # mm

# Create the front wall
front_wall = doc.addObject("Part::Box", "Front Wall")
front_wall.Length = base_length
front_wall.Width = wall_thickness
front_wall.Height = wall_height
front_wall.Placement = Base.Placement(Base.Vector(0, -base_width / 2 + wall_thickness / 2, base_height), Base.Rotation(0, 0, 0))
house_group.addObject(front_wall)

# Apply material to the front wall
front_wall.Material = FreeCAD.ActiveMaterial
front_wall.Material.Name = "Brick"
front_wall.Material.DiffuseColor = (0.8, 0.5, 0.2, 1.0)

# Create the back wall
back_wall = doc.addObject("Part::Box", "Back Wall")
back_wall.Length = base_length
back_wall.Width = wall_thickness
back_wall.Height = wall_height
back_wall.Placement = Base.Placement(Base.Vector(0, base_width / 2 - wall_thickness / 2, base_height), Base.Rotation(0, 0, 0))
house_group.addObject(back_wall)

# Apply material to the back wall
back_wall.Material = FreeCAD.ActiveMaterial
back_wall.Material.Name = "Brick"
back_wall.Material.DiffuseColor = (0.8, 0.5, 0.2, 1.0)

# Create the left wall
left_wall = doc.addObject("Part::Box", "Left Wall")
left_wall.Length = base_width - 2 * wall_thickness
left_wall.Width = wall_thickness
left_wall.Height = wall_height
left_wall.Placement = Base.Placement(Base.Vector(-base_length / 2 + wall_thickness / 2, 0, base_height), Base.Rotation(0, 0, 0))
house_group.addObject(left_wall)

# Apply material to the left wall
left_wall.Material = FreeCAD.ActiveMaterial
left_wall.Material.Name = "Brick"
left_wall.Material.DiffuseColor = (0.8, 0.5, 0.2, 1.0)

# Create the right wall
right_wall = doc.addObject("Part::Box", "Right Wall")
right_wall.Length = base_width - 2 * wall_thickness
right_wall.Width = wall_thickness
right_wall.Height = wall_height
right_wall.Placement = Base.Placement(Base.Vector(base_length / 2 - wall_thickness / 2, 0, base_height), Base.Rotation(0, 0, 0))
house_group.addObject(right_wall)

# Apply material to the right wall
right_wall.Material = FreeCAD.ActiveMaterial
right_wall.Material.Name = "Brick"
right_wall.Material.DiffuseColor = (0.8, 0.5, 0.2, 1.0)

# Create the roof of the house
# Define the dimensions of the roof
roof_length = base_length
roof_width = base_width
roof_height = 500  # mm

# Create the roof
roof = doc.addObject("Part::Box", "Roof")
roof.Length = roof_length
roof.Width = roof_width
roof.Height = roof_height
roof.Placement = Base.Placement(Base.Vector(0, 0, base_height + wall_height), Base.Rotation(0, 0, 0))
house_group.addObject(roof)

# Apply material to the roof
roof.Material = FreeCAD.ActiveMaterial
roof.Material.Name = "Tile"
roof.Material.DiffuseColor = (0.5, 0.2, 0.1, 1.0)

# Create the garden area
# Define the dimensions of the garden area
garden_length = 5000  # mm
garden_width = 5000  # mm
garden_height = 100  # mm

# Create the garden area
garden = doc.addObject("Part::Box", "Garden")
garden.Length = garden_length
garden.Width = garden_width
garden.Height = garden_height
garden.Placement = Base.Placement(Base.Vector(-base_length / 2 + garden_length / 2, -base_width / 2 + garden_width / 2, 0), Base.Rotation(0, 0, 0))
house_group.addObject(garden)

# Apply material to the garden area
garden.Material = FreeCAD.ActiveMaterial
garden.Material.Name = "Grass"
garden.Material.DiffuseColor = (0.2, 0.5, 0.2, 1.0)

# Create the playing area
# Define the dimensions of the playing area
playing_length = 3000  # mm
playing_width = 3000  # mm
playing_height = 100  # mm

# Create the playing area
playing = doc.addObject("Part::Box", "Playing Area")
playing.Length = playing_length
playing.Width = playing_width
playing.Height = playing_height
playing.Placement = Base.Placement(Base.Vector(base_length / 2 - playing_length / 2, -base_width / 2 + playing_width / 2, 0), Base.Rotation(0, 0, 0))
house_group.addObject(playing)

# Apply material to the playing area
playing.Material = FreeCAD.ActiveMaterial
playing.Material.Name = "Concrete"
playing.Material.DiffuseColor = (0.5, 0.5, 0.5, 1.0)

# Recompute the document
doc.recompute()

# Fit the view to the model
FreeCAD.Gui.SendMsgToActiveView("ViewFit")

# Professional completion
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()

FreeCAD.Console.PrintMessage("Professional model completed successfully\n")