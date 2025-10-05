import FreeCAD, Part, Draft, FreeCADGui

# Create a new document
doc = FreeCAD.newDocument("2BHK_House")

# Create the foundation
foundation = doc.addObject("Part::Feature", "Foundation")
foundation.Shape = Part.makeBox(15, 10, 0.5)  # Length, Width, Height
foundation.Placement.Base = FreeCAD.Vector(0, 0, 0)

# Create the ground floor walls
wall1 = doc.addObject("Part::Feature", "Wall1")
wall1.Shape = Part.makeBox(0.2, 10, 3)  # Thickness, Length, Height
wall1.Placement.Base = FreeCAD.Vector(0, 0, 0.5)

wall2 = doc.addObject("Part::Feature", "Wall2")
wall2.Shape = Part.makeBox(0.2, 15, 3)  # Thickness, Length, Height
wall2.Placement.Base = FreeCAD.Vector(0, 0, 0.5)

wall3 = doc.addObject("Part::Feature", "Wall3")
wall3.Shape = Part.makeBox(0.2, 10, 3)  # Thickness, Length, Height
wall3.Placement.Base = FreeCAD.Vector(14.8, 0, 0.5)

wall4 = doc.addObject("Part::Feature", "Wall4")
wall4.Shape = Part.makeBox(0.2, 15, 3)  # Thickness, Length, Height
wall4.Placement.Base = FreeCAD.Vector(0, 9.8, 0.5)

# Create the first floor walls
wall5 = doc.addObject("Part::Feature", "Wall5")
wall5.Shape = Part.makeBox(0.2, 10, 3)  # Thickness, Length, Height
wall5.Placement.Base = FreeCAD.Vector(0, 0, 3.5)

wall6 = doc.addObject("Part::Feature", "Wall6")
wall6.Shape = Part.makeBox(0.2, 15, 3)  # Thickness, Length, Height
wall6.Placement.Base = FreeCAD.Vector(0, 0, 3.5)

wall7 = doc.addObject("Part::Feature", "Wall7")
wall7.Shape = Part.makeBox(0.2, 10, 3)  # Thickness, Length, Height
wall7.Placement.Base = FreeCAD.Vector(14.8, 0, 3.5)

wall8 = doc.addObject("Part::Feature", "Wall8")
wall8.Shape = Part.makeBox(0.2, 15, 3)  # Thickness, Length, Height
wall8.Placement.Base = FreeCAD.Vector(0, 9.8, 3.5)

# Create the doors
door1 = doc.addObject("Part::Feature", "Door1")
door1.Shape = Part.makeBox(0.8, 0.05, 2)  # Width, Thickness, Height
door1.Placement.Base = FreeCAD.Vector(7.4, 0.1, 0.5)

door2 = doc.addObject("Part::Feature", "Door2")
door2.Shape = Part.makeBox(0.8, 0.05, 2)  # Width, Thickness, Height
door2.Placement.Base = FreeCAD.Vector(7.4, 9.7, 0.5)

door3 = doc.addObject("Part::Feature", "Door3")
door3.Shape = Part.makeBox(0.8, 0.05, 2)  # Width, Thickness, Height
door3.Placement.Base = FreeCAD.Vector(7.4, 0.1, 3.5)

door4 = doc.addObject("Part::Feature", "Door4")
door4.Shape = Part.makeBox(0.8, 0.05, 2)  # Width, Thickness, Height
door4.Placement.Base = FreeCAD.Vector(7.4, 9.7, 3.5)

# Create the windows
window1 = doc.addObject("Part::Feature", "Window1")
window1.Shape = Part.makeBox(1.5, 0.05, 1)  # Width, Thickness, Height
window1.Placement.Base = FreeCAD.Vector(2, 4.5, 1)

window2 = doc.addObject("Part::Feature", "Window2")
window2.Shape = Part.makeBox(1.5, 0.05, 1)  # Width, Thickness, Height
window2.Placement.Base = FreeCAD.Vector(12, 4.5, 1)

window3 = doc.addObject("Part::Feature", "Window3")
window3.Shape = Part.makeBox(1.5, 0.05, 1)  # Width, Thickness, Height
window3.Placement.Base = FreeCAD.Vector(2, 4.5, 4)

window4 = doc.addObject("Part::Feature", "Window4")
window4.Shape = Part.makeBox(1.5, 0.05, 1)  # Width, Thickness, Height
window4.Placement.Base = FreeCAD.Vector(12, 4.5, 4)

# Create the compound object
compound = doc.addObject("Part::Compound", "2BHK_House")
compound.Links = [foundation, wall1, wall2, wall3, wall4, wall5, wall6, wall7, wall8, door1, door2, door3, door4, window1, window2, window3, window4]

# Recompute the document and fit the view
doc.recompute()
FreeCADGui.activeDocument().activeView().viewAxometric()
FreeCADGui.SendMsgToActiveView('ViewFit')