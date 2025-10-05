import FreeCAD, Part, Draft, FreeCADGui

# Create a new document
doc = FreeCAD.newDocument("Two_BHK_Houses")

# Create the base for the first house
base1 = doc.addObject("Part::Feature", "Base1")
base1.Shape = Part.makeBox(10, 10, 0.5)  # 10m x 10m x 0.5m
base1.Placement.Base = FreeCAD.Vector(0, 0, 0)

# Create the walls for the first house
wall1_1 = doc.addObject("Part::Feature", "Wall1_1")
wall1_1.Shape = Part.makeBox(0.2, 10, 3)  # 0.2m x 10m x 3m
wall1_1.Placement.Base = FreeCAD.Vector(0, 0, 0.5)

wall1_2 = doc.addObject("Part::Feature", "Wall1_2")
wall1_2.Shape = Part.makeBox(10, 0.2, 3)  # 10m x 0.2m x 3m
wall1_2.Placement.Base = FreeCAD.Vector(0, 0, 0.5)

wall1_3 = doc.addObject("Part::Feature", "Wall1_3")
wall1_3.Shape = Part.makeBox(0.2, 10, 3)  # 0.2m x 10m x 3m
wall1_3.Placement.Base = FreeCAD.Vector(9.8, 0, 0.5)

wall1_4 = doc.addObject("Part::Feature", "Wall1_4")
wall1_4.Shape = Part.makeBox(10, 0.2, 3)  # 10m x 0.2m x 3m
wall1_4.Placement.Base = FreeCAD.Vector(0, 9.8, 0.5)

# Create the doors and windows for the first house
door1_1 = doc.addObject("Part::Feature", "Door1_1")
door1_1.Shape = Part.makeBox(0.8, 2, 0.1)  # 0.8m x 2m x 0.1m
door1_1.Placement.Base = FreeCAD.Vector(4.6, 0.1, 0.5)

window1_1 = doc.addObject("Part::Feature", "Window1_1")
window1_1.Shape = Part.makeBox(1.5, 1, 0.1)  # 1.5m x 1m x 0.1m
window1_1.Placement.Base = FreeCAD.Vector(2, 2, 1.5)

window1_2 = doc.addObject("Part::Feature", "Window1_2")
window1_2.Shape = Part.makeBox(1.5, 1, 0.1)  # 1.5m x 1m x 0.1m
window1_2.Placement.Base = FreeCAD.Vector(7, 2, 1.5)

# Create the base for the second house
base2 = doc.addObject("Part::Feature", "Base2")
base2.Shape = Part.makeBox(10, 10, 0.5)  # 10m x 10m x 0.5m
base2.Placement.Base = FreeCAD.Vector(15, 0, 0)

# Create the walls for the second house
wall2_1 = doc.addObject("Part::Feature", "Wall2_1")
wall2_1.Shape = Part.makeBox(0.2, 10, 3)  # 0.2m x 10m x 3m
wall2_1.Placement.Base = FreeCAD.Vector(15, 0, 0.5)

wall2_2 = doc.addObject("Part::Feature", "Wall2_2")
wall2_2.Shape = Part.makeBox(10, 0.2, 3)  # 10m x 0.2m x 3m
wall2_2.Placement.Base = FreeCAD.Vector(15, 0, 0.5)

wall2_3 = doc.addObject("Part::Feature", "Wall2_3")
wall2_3.Shape = Part.makeBox(0.2, 10, 3)  # 0.2m x 10m x 3m
wall2_3.Placement.Base = FreeCAD.Vector(24.8, 0, 0.5)

wall2_4 = doc.addObject("Part::Feature", "Wall2_4")
wall2_4.Shape = Part.makeBox(10, 0.2, 3)  # 10m x 0.2m x 3m
wall2_4.Placement.Base = FreeCAD.Vector(15, 9.8, 0.5)

# Create the doors and windows for the second house
door2_1 = doc.addObject("Part::Feature", "Door2_1")
door2_1.Shape = Part.makeBox(0.8, 2, 0.1)  # 0.8m x 2m x 0.1m
door2_1.Placement.Base = FreeCAD.Vector(19.6, 0.1, 0.5)

window2_1 = doc.addObject("Part::Feature", "Window2_1")
window2_1.Shape = Part.makeBox(1.5, 1, 0.1)  # 1.5m x 1m x 0.1m
window2_1.Placement.Base = FreeCAD.Vector(17, 2, 1.5)

window2_2 = doc.addObject("Part::Feature", "Window2_2")
window2_2.Shape = Part.makeBox(1.5, 1, 0.1)  # 1.5m x 1m x 0.1m
window2_2.Placement.Base = FreeCAD.Vector(22, 2, 1.5)

# Create the parking space
parking_base = doc.addObject("Part::Feature", "Parking_Base")
parking_base.Shape = Part.makeBox(5, 10, 0.5)  # 5m x 10m x 0.5m
parking_base.Placement.Base = FreeCAD.Vector(5, -10, 0)

parking_wall1 = doc.addObject("Part::Feature", "Parking_Wall1")
parking_wall1.Shape = Part.makeBox(0.2, 10, 1)  # 0.2m x 10m x 1m
parking_wall1.Placement.Base = FreeCAD.Vector(5, -10, 0.5)

parking_wall2 = doc.addObject("Part::Feature", "Parking_Wall2")
parking_wall2.Shape = Part.makeBox(5, 0.2, 1)  # 5m x 0.2m x 1m
parking_wall2.Placement.Base = FreeCAD.Vector(5, -10, 0.5)

parking_wall3 = doc.addObject("Part::Feature", "Parking_Wall3")
parking_wall3.Shape = Part.makeBox(0.2, 10, 1)  # 0.2m x 10m x 1m
parking_wall3.Placement.Base = FreeCAD.Vector(9.8, -10, 0.5)

parking_wall4 = doc.addObject("Part::Feature", "Parking_Wall4")
parking_wall4.Shape = Part.makeBox(5, 0.2, 1)  # 5m x 0.2m x 1m
parking_wall4.Placement.Base = FreeCAD.Vector(5, -9.8, 0.5)

# Combine all the objects into a single compound
compound = doc.addObject("Part::Compound", "Compound")
compound.Links = [base1, wall1_1, wall1_2, wall1_3, wall1_4, door1_1, window1_1, window1_2,
                  base2, wall2_1, wall2_2, wall2_3, wall2_4, door2_1, window2_1, window2_2,
                  parking_base, parking_wall1, parking_wall2, parking_wall3, parking_wall4]

# Recompute the document and view the result
doc.recompute()
FreeCADGui.activeDocument().activeView().viewAxometric()
FreeCADGui.SendMsgToActiveView('ViewFit')