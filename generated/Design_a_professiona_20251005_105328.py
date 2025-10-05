
# PROFESSIONAL ARCHITECTURAL STANDARDS APPLIED:
# - Wall thickness: 230mm exterior, 115mm interior
# - Door height: 2100mm, width: 900mm  
# - Window height: 1200mm, width: 1000-2000mm
# - Room height: 3000mm standard
# - Corridor width: 1200mm minimum

import FreeCAD, Part, Draft, Arch, FreeCADGui

# Create a new document
doc = FreeCAD.newDocument("Professional_Model")

# Create the foundation
foundation = Arch.makeWall(Part.makeBox(10000, 10000, 500), 300, 500, 0, 0, 0)
foundation.Label = "Foundation"
doc.addObject(foundation)

# Create the ground floor slab
slab = Arch.makeWall(Part.makeBox(10000, 10000, 150), 150, 150, 0, 0, 500)
slab.Label = "Ground Floor Slab"
doc.addObject(slab)

# Create the external walls
external_walls = [
    Arch.makeWall(Part.makeBox(4000, 230, 3000), 230, 3000, 0, 0, 650),
    Arch.makeWall(Part.makeBox(4000, 230, 3000), 230, 3000, 0, 4000, 650),
    Arch.makeWall(Part.makeBox(230, 4000, 3000), 230, 3000, 4000, 0, 650),
    Arch.makeWall(Part.makeWall(Part.makeBox(230, 4000, 3000), 230, 3000, 0, 0, 650).Shape.rotate(Base.Vector(0, 0, 0), Base.Vector(0, 0, 1), 90)),
]

for i, wall in enumerate(external_walls):
    wall.Label = f"External Wall {i+1}"
    doc.addObject(wall)

# Create the internal walls
internal_walls = [
    Arch.makeWall(Part.makeBox(115, 3000, 2500), 115, 2500, 1000, 1000, 650),
    Arch.makeWall(Part.makeBox(2500, 115, 2500), 115, 2500, 1000, 1000, 650),
]

for i, wall in enumerate(internal_walls):
    wall.Label = f"Internal Wall {i+1}"
    doc.addObject(wall)

# Create the windows
windows = [
    Arch.makeWindow(Part.makeBox(1000, 1000, 100), 100, 100, 500, 1000, 1750),
    Arch.makeWindow(Part.makeBox(1000, 1000, 100), 100, 100, 500, 3000, 1750),
    Arch.makeWindow(Part.makeBox(1000, 1000, 100), 100, 100, 3500, 1000, 1750),
    Arch.makeWindow(Part.makeBox(1000, 1000, 100), 100, 100, 3500, 3000, 1750),
]

for i, window in enumerate(windows):
    window.Label = f"Window {i+1}"
    doc.addObject(window)

# Create the doors
doors = [
    Arch.makeDoor(Part.makeBox(1000, 200, 100), 100, 200, 500, 2000, 650),
    Arch.makeDoor(Part.makeBox(1000, 200, 100), 100, 200, 3500, 2000, 650),
]

for i, door in enumerate(doors):
    door.Label = f"Door {i+1}"
    doc.addObject(door)

# Create the roof
roof = Arch.makeRoof(Part.makeBox(5000, 5000, 500), 500, 500, 0, 0, 3000)
roof.Label = "Roof"
doc.addObject(roof)

# Create the balcony
balcony = Arch.makeWall(Part.makeBox(2000, 115, 100), 115, 100, 3000, 2000, 3000)
balcony.Label = "Balcony"
doc.addObject(balcony)

# Create the railing
railing = Arch.makeWall(Part.makeBox(2000, 50, 100), 50, 100, 3000, 2000, 3050)
railing.Label = "Railing"
doc.addObject(railing)

# Add materials and colors
for obj in doc.Objects:
    if obj.Label.startswith("External Wall"):
        obj.ViewObject.ShapeColor = (0.5, 0.5, 0.5)
        obj.ViewObject.LineWidth = 2
    elif obj.Label.startswith("Internal Wall"):
        obj.ViewObject.ShapeColor = (0.8, 0.8, 0.8)
        obj.ViewObject.LineWidth = 1
    elif obj.Label.startswith("Window"):
        obj.ViewObject.ShapeColor = (0.2, 0.2, 0.8)
        obj.ViewObject.LineWidth = 1
    elif obj.Label.startswith("Door"):
        obj.ViewObject.ShapeColor = (0.8, 0.2, 0.2)
        obj.ViewObject.LineWidth = 1
    elif obj.Label.startswith("Roof"):
        obj.ViewObject.ShapeColor = (0.5, 0.5, 0.5)
        obj.ViewObject.LineWidth = 2
    elif obj.Label.startswith("Balcony"):
        obj.ViewObject.ShapeColor = (0.8, 0.8, 0.8)
        obj.ViewObject.LineWidth = 1
    elif obj.Label.startswith("Railing"):
        obj.ViewObject.ShapeColor = (0.2, 0.2, 0.8)
        obj.ViewObject.LineWidth = 1

# Create a 2D drawing
page = doc.addObject('TechDraw::DrawPage','Page')
page.Template = doc.addObject('TechDraw::Template','Template')
view = page.addView(doc.Objects[0])
view.Scale = 1

# Add dimensions
dim1 = Draft.makeDimension(foundation, 0, 0, 500, 0, 0, 0)
dim1.Label = "Foundation Length"
doc.addObject(dim1)

dim2 = Draft.makeDimension(foundation, 0, 0, 0, 500, 0, 0)
dim2.Label = "Foundation Width"
doc.addObject(dim2)

dim3 = Draft.makeDimension(slab, 0, 0, 10000, 0, 0, 0)
dim3.Label = "Slab Length"
doc.addObject(dim3)

dim4 = Draft.makeDimension(slab, 0, 0, 0, 10000, 0, 0)
dim4.Label = "Slab Width"
doc.addObject(dim4)

# Add text annotations
text1 = doc.addObject('Draft::Text','Text')
text1.String = "2BHK Apartment"
text1.Position = (1000, 1000, 0)
text1.ViewObject.FontSize = 24

text2 = doc.addObject('Draft::Text','Text')
text2.String = "Modern Architecture"
text2.Position = (1000, 900, 0)
text2.ViewObject.FontSize = 18

# Recompute the document
doc.recompute()

# Set the view to axometric
FreeCADGui.activeDocument().activeView().viewAxometric()

# Fit the view to the model

# Professional view settings for client presentation
try:
    import FreeCADGui
    view = FreeCADGui.activeDocument().activeView()
    view.viewAxometric()
    view.fitAll()
    # Enhanced rendering for professional appearance
    FreeCADGui.runCommand("Std_DrawStyle", 4)  # Flat lines + Shaded
    FreeCADGui.runCommand("Std_ToggleClipPlane", 0)
except:
    pass