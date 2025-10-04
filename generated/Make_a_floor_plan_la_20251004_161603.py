# Import necessary modules
import FreeCAD, Part, Draft, FreeCADGui

# Create a new document
doc = FreeCAD.newDocument("Floor_Plan_Layout")

# Create walls
wall1 = doc.addObject("Part::Feature", "Wall1")
wall1.Shape = Part.makeBox(10, 0.2, 3)  # Length, Width, Height
wall1.Placement.Base = FreeCAD.Vector(0, 0, 0)

wall2 = doc.addObject("Part::Feature", "Wall2")
wall2.Shape = Part.makeBox(10, 0.2, 3)  # Length, Width, Height
wall2.Placement.Base = FreeCAD.Vector(0, 10, 0)
wall2.Placement.Rotation = FreeCAD.Rotation(0, 0, 90)

wall3 = doc.addObject("Part::Feature", "Wall3")
wall3.Shape = Part.makeBox(10, 0.2, 3)  # Length, Width, Height
wall3.Placement.Base = FreeCAD.Vector(10, 10, 0)
wall3.Placement.Rotation = FreeCAD.Rotation(0, 0, 90)

wall4 = doc.addObject("Part::Feature", "Wall4")
wall4.Shape = Part.makeBox(10, 0.2, 3)  # Length, Width, Height
wall4.Placement.Base = FreeCAD.Vector(10, 0, 0)
wall4.Placement.Rotation = FreeCAD.Rotation(0, 0, 90)

# Create doors
door1 = doc.addObject("Part::Feature", "Door1")
door1.Shape = Part.makeBox(1, 0.1, 2)  # Length, Width, Height
door1.Placement.Base = FreeCAD.Vector(5, 0, 0)

door2 = doc.addObject("Part::Feature", "Door2")
door2.Shape = Part.makeBox(1, 0.1, 2)  # Length, Width, Height
door2.Placement.Base = FreeCAD.Vector(5, 10, 0)

# Create windows
window1 = doc.addObject("Part::Feature", "Window1")
window1.Shape = Part.makeBox(1, 0.1, 1)  # Length, Width, Height
window1.Placement.Base = FreeCAD.Vector(2, 2, 1)

window2 = doc.addObject("Part::Feature", "Window2")
window2.Shape = Part.makeBox(1, 0.1, 1)  # Length, Width, Height
window2.Placement.Base = FreeCAD.Vector(8, 2, 1)

window3 = doc.addObject("Part::Feature", "Window3")
window3.Shape = Part.makeBox(1, 0.1, 1)  # Length, Width, Height
window3.Placement.Base = FreeCAD.Vector(2, 8, 1)

window4 = doc.addObject("Part::Feature", "Window4")
window4.Shape = Part.makeBox(1, 0.1, 1)  # Length, Width, Height
window4.Placement.Base = FreeCAD.Vector(8, 8, 1)

# Create rooms
room1 = doc.addObject("Part::Feature", "Room1")
room1.Shape = Part.makeBox(5, 5, 3)  # Length, Width, Height
room1.Placement.Base = FreeCAD.Vector(0, 0, 0)

room2 = doc.addObject("Part::Feature", "Room2")
room2.Shape = Part.makeBox(5, 5, 3)  # Length, Width, Height
room2.Placement.Base = FreeCAD.Vector(5, 5, 0)

# Combine objects
compound = doc.addObject("Part::Compound", "Floor_Plan")
compound.Links = [wall1, wall2, wall3, wall4, door1, door2, window1, window2, window3, window4, room1, room2]

# Recompute and view the document
doc.recompute()
FreeCADGui.activeDocument().activeView().viewAxometric()
FreeCADGui.SendMsgToActiveView('ViewFit')