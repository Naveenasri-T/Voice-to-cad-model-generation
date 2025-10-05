import FreeCAD, Part, Draft, FreeCADGui

# Create a new document
doc = FreeCAD.newDocument("2BHK_House")

# Create the foundation
foundation = doc.addObject("Part::Feature", "Foundation")
foundation.Shape = Part.makeBox(15, 10, 0.5)  # 15m length, 10m width, 0.5m height
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
wall1.Placement.Base = FreeCAD.Vector(0, 0, 0.5)

wall2 = doc.addObject("Part::Feature", "Wall2")
wall2.Shape = Part.makeBox(15, 0.2, 6)  # 15m length, 0.2m thickness, 6m height
wall2.Placement.Base = FreeCAD.Vector(0, 0, 0.5)

wall3 = doc.addObject("Part::Feature", "Wall3")
wall3.Shape = Part.makeBox(0.2, 10, 6)  # 0.2m thickness, 10m width, 6m height
wall3.Placement.Base = FreeCAD.Vector(14.8, 0, 0.5)

wall4 = doc.addObject("Part::Feature", "Wall4")
wall4.Shape = Part.makeBox(15, 0.2, 6)  # 15m length, 0.2m thickness, 6m height
wall4.Placement.Base = FreeCAD.Vector(0, 9.8, 0.5)

# Create the doors
door1 = doc.addObject("Part::Feature", "Door1")
door1.Shape = Part.makeBox(0.8, 2, 0.05)  # 0.8m width, 2m height, 0.05m thickness
door1.Placement.Base = FreeCAD.Vector(7, -0.1, 0.5)

door2 = doc.addObject("Part::Feature", "Door2")
door2.Shape = Part.makeBox(0.8, 2, 0.05)  # 0.8m width, 2m height, 0.05m thickness
door2.Placement.Base = FreeCAD.Vector(7, 10.1, 3.5)

# Create the windows
window1 = doc.addObject("Part::Feature", "Window1")
window1.Shape = Part.makeBox(1.5, 1, 0.05)  # 1.5m width, 1m height, 0.05m thickness
window1.Placement.Base = FreeCAD.Vector(2, 4, 2)

window2 = doc.addObject("Part::Feature", "Window2")
window2.Shape = Part.makeBox(1.5, 1, 0.05)  # 1.5m width, 1m height, 0.05m thickness
window2.Placement.Base = FreeCAD.Vector(12, 4, 2)

window3 = doc.addObject("Part::Feature", "Window3")
window3.Shape = Part.makeBox(1.5, 1, 0.05)  # 1.5m width, 1m height, 0.05m thickness
window3.Placement.Base = FreeCAD.Vector(2, 4, 5.5)

window4 = doc.addObject("Part::Feature", "Window4")
window4.Shape = Part.makeBox(1.5, 1, 0.05)  # 1.5m width, 1m height, 0.05m thickness
window4.Placement.Base = FreeCAD.Vector(12, 4, 5.5)

# Create the rooms
living_room = doc.addObject("Part::Feature", "Living_Room")
living_room.Shape = Part.makeBox(5, 4, 3)  # 5m length, 4m width, 3m height
living_room.Placement.Base = FreeCAD.Vector(0, 0, 0.5)

kitchen = doc.addObject("Part::Feature", "Kitchen")
kitchen.Shape = Part.makeBox(3, 3, 3)  # 3m length, 3m width, 3m height
kitchen.Placement.Base = FreeCAD.Vector(10, 0, 0.5)

bedroom1 = doc.addObject("Part::Feature", "Bedroom1")
bedroom1.Shape = Part.makeBox(4, 4, 3)  # 4m length, 4m width, 3m height
bedroom1.Placement.Base = FreeCAD.Vector(0, 5, 0.5)

bedroom2 = doc.addObject("Part::Feature", "Bedroom2")
bedroom2.Shape = Part.makeBox(4, 4, 3)  # 4m length, 4m width, 3m height
bedroom2.Placement.Base = FreeCAD.Vector(0, 5, 3.5)

# Recompute the document and fit the view
doc.recompute()
FreeCADGui.activeDocument().activeView().viewAxometric()
FreeCADGui.SendMsgToActiveView('ViewFit')
#This script generates a simple 2BHK house model with a foundation, ground floor, first floor, walls, doors, windows, and rooms. The dimensions and positions of the objects are chosen to create a realistic and logical architectural layout. The `recompute()` function is called to update the document, and the `viewAxometric()` and `SendMsgToActiveView('ViewFit')` functions are called to fit the view to the model.