# Import necessary modules
import FreeCAD
import Part
import Draft
import FreeCADGui

# Create a new document
doc = FreeCAD.newDocument()

# Create the base of the house (parking area)
base_length = 15000  # mm
base_width = 8000  # mm
base_height = 200  # mm
base = Part.makeBox(base_length, base_width, base_height)
base.translate(FreeCAD.Base.Vector(-base_length/2, -base_width/2, 0))
doc.addObject("Part::Feature", "Base").Shape = base

# Create the walls of the house
wall_length = 12000  # mm
wall_width = 200  # mm
wall_height = 3000  # mm
wall1 = Part.makeBox(wall_length, wall_width, wall_height)
wall1.translate(FreeCAD.Base.Vector(-wall_length/2, -base_width/2 + wall_width/2, base_height))
doc.addObject("Part::Feature", "Wall1").Shape = wall1

wall2 = Part.makeBox(wall_length, wall_width, wall_height)
wall2.translate(FreeCAD.Base.Vector(-wall_length/2, base_width/2 - wall_width/2, base_height))
doc.addObject("Part::Feature", "Wall2").Shape = wall2

wall3 = Part.makeBox(wall_width, base_width, wall_height)
wall3.translate(FreeCAD.Base.Vector(-wall_length/2 + wall_length - wall_width/2, 0, base_height))
doc.addObject("Part::Feature", "Wall3").Shape = wall3

wall4 = Part.makeBox(wall_width, base_width, wall_height)
wall4.translate(FreeCAD.Base.Vector(-wall_length/2 + wall_width/2, 0, base_height))
doc.addObject("Part::Feature", "Wall4").Shape = wall4

# Create the roof of the house
roof_length = 12000  # mm
roof_width = 8000  # mm
roof_height = 200  # mm
roof = Part.makeBox(roof_length, roof_width, roof_height)
roof.translate(FreeCAD.Base.Vector(-roof_length/2, -roof_width/2, base_height + wall_height))
doc.addObject("Part::Feature", "Roof").Shape = roof

# Create the pillars for the parking area
pillar_radius = 200  # mm
pillar_height = 2000  # mm
pillar1 = Part.makeCylinder(pillar_radius, pillar_height)
pillar1.translate(FreeCAD.Base.Vector(-base_length/2 + 2000, -base_width/2 + 2000, 0))
doc.addObject("Part::Feature", "Pillar1").Shape = pillar1

pillar2 = Part.makeCylinder(pillar_radius, pillar_height)
pillar2.translate(FreeCAD.Base.Vector(base_length/2 - 2000, -base_width/2 + 2000, 0))
doc.addObject("Part::Feature", "Pillar2").Shape = pillar2

pillar3 = Part.makeCylinder(pillar_radius, pillar_height)
pillar3.translate(FreeCAD.Base.Vector(-base_length/2 + 2000, base_width/2 - 2000, 0))
doc.addObject("Part::Feature", "Pillar3").Shape = pillar3

pillar4 = Part.makeCylinder(pillar_radius, pillar_height)
pillar4.translate(FreeCAD.Base.Vector(base_length/2 - 2000, base_width/2 - 2000, 0))
doc.addObject("Part::Feature", "Pillar4").Shape = pillar4

# Recompute the document
doc.recompute()

# View the document in axometric view
FreeCADGui.ActiveDocument.ActiveView.viewAxometric()

# Fit the view to the document
FreeCADGui.ActiveDocument.ActiveView.viewFit()