import FreeCAD, Part, Draft, FreeCADGui

# Create a new document
doc = FreeCAD.newDocument("2BHK_House_Model")

# Create the foundation
foundation = doc.addObject("Part::Feature", "Foundation")
foundation.Shape = Part.makeBox(15, 10, 0.5)  # 15m length, 10m width, 0.5m thickness
foundation.Placement.Base = FreeCAD.Vector(0, 0, 0)

# Create the ground floor
ground_floor = doc.addObject("Part::Feature", "Ground_Floor")
ground_floor.Shape = Part.makeBox(15, 10, 3)  # 15m length, 10m width, 3m height
ground_floor.Placement.Base = FreeCAD.Vector(0, 0, 0.5)

# Create the first floor
first_floor = doc.addObject("Part::Feature", "First_Floor")
first_floor.Shape = Part.makeBox(15, 10, 3)  # 15m length, 10m width, 3m height
first_floor.Placement.Base = FreeCAD.Vector(0, 0, 3.5)

# Create the walls
wall1 = doc.addObject("Part::Feature", "Wall1")
wall1.Shape = Part.makeBox(0.2, 10, 6)  # 0.2m thickness, 10m width, 6m height
wall1.Placement.Base = FreeCAD.Vector(-7.5, 0, 0.5)

wall2 = doc.addObject("Part::Feature", "Wall2")
wall2.Shape = Part.makeBox(0.2, 10, 6)  # 0.2m thickness, 10m width, 6m height
wall2.Placement.Base = FreeCAD.Vector(7.5, 0, 0.5)

wall3 = doc.addObject("Part::Feature", "Wall3")
wall3.Shape = Part.makeBox(15, 0.2, 6)  # 15m length, 0.2m thickness, 6m height
wall3.Placement.Base = FreeCAD.Vector(0, -5, 0.5)

wall4 = doc.addObject("Part::Feature", "Wall4")
wall4.Shape = Part.makeBox(15, 0.2, 6)  # 15m length, 0.2m thickness, 6m height
wall4.Placement.Base = FreeCAD.Vector(0, 5, 0.5)

# Create the doors
door1 = doc.addObject("Part::Feature", "Door1")
door1.Shape = Part.makeBox(0.8, 2, 0.05)  # 0.8m width, 2m height, 0.05m thickness
door1.Placement.Base = FreeCAD.Vector(-7.3, -4.5, 0.5)

door2 = doc.addObject("Part::Feature", "Door2")
door2.Shape = Part.makeBox(0.8, 2, 0.05)  # 0.8m width, 2m height, 0.05m thickness
door2.Placement.Base = FreeCAD.Vector(7.3, -4.5, 0.5)

# Create the windows
window1 = doc.addObject("Part::Feature", "Window1")
window1.Shape = Part.makeBox(1.5, 1, 0.05)  # 1.5m width, 1m height, 0.05m thickness
window1.Placement.Base = FreeCAD.Vector(-6, 2, 2)

window2 = doc.addObject("Part::Feature", "Window2")
window2.Shape = Part.makeBox(1.5, 1, 0.05)  # 1.5m width, 1m height, 0.05m thickness
window2.Placement.Base = FreeCAD.Vector(6, 2, 2)

# Create the rooms
room1 = doc.addObject("Part::Feature", "Room1")
room1.Shape = Part.makeBox(5, 5, 3)  # 5m length, 5m width, 3m height
room1.Placement.Base = FreeCAD.Vector(-4, -2, 0.5)

room2 = doc.addObject("Part::Feature", "Room2")
room2.Shape = Part.makeBox(5, 5, 3)  # 5m length, 5m width, 3m height
room2.Placement.Base = FreeCAD.Vector(4, -2, 0.5)

room3 = doc.addObject("Part::Feature", "Room3")
room3.Shape = Part.makeBox(5, 5, 3)  # 5m length, 5m width, 3m height
room3.Placement.Base = FreeCAD.Vector(-4, 2, 3.5)

room4 = doc.addObject("Part::Feature", "Room4")
room4.Shape = Part.makeBox(5, 5, 3)  # 5m length, 5m width, 3m height
room4.Placement.Base = FreeCAD.Vector(4, 2, 3.5)

# Combine the objects
compound = doc.addObject("Part::Compound", "2BHK_House")
compound.Links = [foundation, ground_floor, first_floor, wall1, wall2, wall3, wall4, door1, door2, window1, window2, room1, room2, room3, room4]

# Recompute and view the model
doc.recompute()
FreeCADGui.activeDocument().activeView().viewAxometric()
FreeCADGui.SendMsgToActiveView('ViewFit')