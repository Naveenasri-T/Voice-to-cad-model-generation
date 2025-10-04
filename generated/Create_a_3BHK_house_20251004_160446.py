import FreeCAD, Part, Draft, FreeCADGui

# Create a new document
doc = FreeCAD.newDocument("3BHK_House")

# Create the foundation
foundation = doc.addObject("Part::Feature", "Foundation")
foundation.Shape = Part.makeBox(20, 15, 0.5)
foundation.Placement.Base = FreeCAD.Vector(0, 0, 0)

# Create the ground floor walls
wall1 = doc.addObject("Part::Feature", "Wall1")
wall1.Shape = Part.makeBox(20, 0.3, 3)
wall1.Placement.Base = FreeCAD.Vector(0, 0, 0.5)

wall2 = doc.addObject("Part::Feature", "Wall2")
wall2.Shape = Part.makeBox(0.3, 15, 3)
wall2.Placement.Base = FreeCAD.Vector(0, 0, 0.5)

wall3 = doc.addObject("Part::Feature", "Wall3")
wall3.Shape = Part.makeBox(20, 0.3, 3)
wall3.Placement.Base = FreeCAD.Vector(0, 14.7, 0.5)

wall4 = doc.addObject("Part::Feature", "Wall4")
wall4.Shape = Part.makeBox(0.3, 15, 3)
wall4.Placement.Base = FreeCAD.Vector(19.7, 0, 0.5)

# Create the first floor walls
wall5 = doc.addObject("Part::Feature", "Wall5")
wall5.Shape = Part.makeBox(20, 0.3, 3)
wall5.Placement.Base = FreeCAD.Vector(0, 0, 3.5)

wall6 = doc.addObject("Part::Feature", "Wall6")
wall6.Shape = Part.makeBox(0.3, 15, 3)
wall6.Placement.Base = FreeCAD.Vector(0, 0, 3.5)

wall7 = doc.addObject("Part::Feature", "Wall7")
wall7.Shape = Part.makeBox(20, 0.3, 3)
wall7.Placement.Base = FreeCAD.Vector(0, 14.7, 3.5)

wall8 = doc.addObject("Part::Feature", "Wall8")
wall8.Shape = Part.makeBox(0.3, 15, 3)
wall8.Placement.Base = FreeCAD.Vector(19.7, 0, 3.5)

# Create the second floor walls
wall9 = doc.addObject("Part::Feature", "Wall9")
wall9.Shape = Part.makeBox(20, 0.3, 3)
wall9.Placement.Base = FreeCAD.Vector(0, 0, 6.5)

wall10 = doc.addObject("Part::Feature", "Wall10")
wall10.Shape = Part.makeBox(0.3, 15, 3)
wall10.Placement.Base = FreeCAD.Vector(0, 0, 6.5)

wall11 = doc.addObject("Part::Feature", "Wall11")
wall11.Shape = Part.makeBox(20, 0.3, 3)
wall11.Placement.Base = FreeCAD.Vector(0, 14.7, 6.5)

wall12 = doc.addObject("Part::Feature", "Wall12")
wall12.Shape = Part.makeBox(0.3, 15, 3)
wall12.Placement.Base = FreeCAD.Vector(19.7, 0, 6.5)

# Create the roof
roof = doc.addObject("Part::Feature", "Roof")
roof.Shape = Part.makeBox(20, 15, 1)
roof.Placement.Base = FreeCAD.Vector(0, 0, 9.5)

# Create the doors
door1 = doc.addObject("Part::Feature", "Door1")
door1.Shape = Part.makeBox(0.8, 0.3, 2)
door1.Placement.Base = FreeCAD.Vector(9, 0, 0.5)

door2 = doc.addObject("Part::Feature", "Door2")
door2.Shape = Part.makeBox(0.8, 0.3, 2)
door2.Placement.Base = FreeCAD.Vector(9, 0, 3.5)

door3 = doc.addObject("Part::Feature", "Door3")
door3.Shape = Part.makeBox(0.8, 0.3, 2)
door3.Placement.Base = FreeCAD.Vector(9, 0, 6.5)

# Create the windows
window1 = doc.addObject("Part::Feature", "Window1")
window1.Shape = Part.makeBox(1.5, 0.3, 1)
window1.Placement.Base = FreeCAD.Vector(2, 4, 1)

window2 = doc.addObject("Part::Feature", "Window2")
window2.Shape = Part.makeBox(1.5, 0.3, 1)
window2.Placement.Base = FreeCAD.Vector(2, 10, 1)

window3 = doc.addObject("Part::Feature", "Window3")
window3.Shape = Part.makeBox(1.5, 0.3, 1)
window3.Placement.Base = FreeCAD.Vector(2, 4, 4)

window4 = doc.addObject("Part::Feature", "Window4")
window4.Shape = Part.makeBox(1.5, 0.3, 1)
window4.Placement.Base = FreeCAD.Vector(2, 10, 4)

window5 = doc.addObject("Part::Feature", "Window5")
window5.Shape = Part.makeBox(1.5, 0.3, 1)
window5.Placement.Base = FreeCAD.Vector(2, 4, 7)

window6 = doc.addObject("Part::Feature", "Window6")
window6.Shape = Part.makeBox(1.5, 0.3, 1)
window6.Placement.Base = FreeCAD.Vector(2, 10, 7)

# Create the parking
parking = doc.addObject("Part::Feature", "Parking")
parking.Shape = Part.makeBox(5, 10, 0.5)
parking.Placement.Base = FreeCAD.Vector(-5, 0, 0)

# Combine all the objects
compound = doc.addObject("Part::Compound", "House")
compound.Links = [foundation, wall1, wall2, wall3, wall4, wall5, wall6, wall7, wall8, wall9, wall10, wall11, wall12, roof, door1, door2, door3, window1, window2, window3, window4, window5, window6, parking]

# Recompute the document and fit the view
doc.recompute()
FreeCADGui.activeDocument().activeView().viewAxometric()
FreeCADGui.SendMsgToActiveView('ViewFit')