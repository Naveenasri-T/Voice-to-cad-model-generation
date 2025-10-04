# Import necessary modules
import FreeCAD, Part, Draft, FreeCADGui

# Create a new document
doc = FreeCAD.newDocument("2BHK_House_Model")

# Create the foundation/floor base
foundation = Draft.makeRectangle(10, 8, center=(0, 0, 0), face=True)
foundation.Label = "Foundation"
foundation.ViewObject.ShapeColor = (0.5, 0.5, 0.5)  # Grey color

# Create the living room
living_room = Draft.makeRectangle(4, 3, center=(1, 1, 0), face=True)
living_room.Label = "Living Room"
living_room.ViewObject.ShapeColor = (1, 1, 1)  # White color

# Create the kitchen
kitchen = Draft.makeRectangle(2, 2, center=(5, 1, 0), face=True)
kitchen.Label = "Kitchen"
kitchen.ViewObject.ShapeColor = (1, 0, 0)  # Red color

# Create the bedroom 1
bedroom1 = Draft.makeRectangle(3, 3, center=(1, -2, 0), face=True)
bedroom1.Label = "Bedroom 1"
bedroom1.ViewObject.ShapeColor = (0, 1, 0)  # Green color

# Create the bedroom 2
bedroom2 = Draft.makeRectangle(3, 3, center=(5, -2, 0), face=True)
bedroom2.Label = "Bedroom 2"
bedroom2.ViewObject.ShapeColor = (0, 0, 1)  # Blue color

# Create the bathroom
bathroom = Draft.makeRectangle(1, 1, center=(3, -4, 0), face=True)
bathroom.Label = "Bathroom"
bathroom.ViewObject.ShapeColor = (1, 1, 0)  # Yellow color

# Create walls
wall1 = Draft.makeLine((0, 0, 0), (10, 0, 0))
wall1.Label = "Wall 1"
wall1.ViewObject.LineWidth = 2
wall1.ViewObject.LineColor = (0, 0, 0)  # Black color

wall2 = Draft.makeLine((10, 0, 0), (10, -5, 0))
wall2.Label = "Wall 2"
wall2.ViewObject.LineWidth = 2
wall2.ViewObject.LineColor = (0, 0, 0)  # Black color

wall3 = Draft.makeLine((10, -5, 0), (0, -5, 0))
wall3.Label = "Wall 3"
wall3.ViewObject.LineWidth = 2
wall3.ViewObject.LineColor = (0, 0, 0)  # Black color

wall4 = Draft.makeLine((0, -5, 0), (0, 0, 0))
wall4.Label = "Wall 4"
wall4.ViewObject.LineWidth = 2
wall4.ViewObject.LineColor = (0, 0, 0)  # Black color

# Create doors
door1 = Draft.makeRectangle(0.8, 2, center=(2, -0.1, 0), face=True)
door1.Label = "Door 1"
door1.ViewObject.ShapeColor = (0.5, 0.5, 0.5)  # Grey color

door2 = Draft.makeRectangle(0.8, 2, center=(6, -0.1, 0), face=True)
door2.Label = "Door 2"
door2.ViewObject.ShapeColor = (0.5, 0.5, 0.5)  # Grey color

# Create windows
window1 = Draft.makeRectangle(1.5, 1, center=(3, 1.5, 0), face=True)
window1.Label = "Window 1"
window1.ViewObject.ShapeColor = (0.5, 0.5, 0.5)  # Grey color

window2 = Draft.makeRectangle(1.5, 1, center=(7, 1.5, 0), face=True)
window2.Label = "Window 2"
window2.ViewObject.ShapeColor = (0.5, 0.5, 0.5)  # Grey color

# Add labels
label1 = Draft.makeText("Living Room", point=(2, 1.5, 0))
label1.Label = "Label 1"
label1.ViewObject.FontSize = 12

label2 = Draft.makeText("Kitchen", point=(5.5, 1.5, 0))
label2.Label = "Label 2"
label2.ViewObject.FontSize = 12

label3 = Draft.makeText("Bedroom 1", point=(2, -1.5, 0))
label3.Label = "Label 3"
label3.ViewObject.FontSize = 12

label4 = Draft.makeText("Bedroom 2", point=(5.5, -1.5, 0))
label4.Label = "Label 4"
label4.ViewObject.FontSize = 12

label5 = Draft.makeText("Bathroom", point=(3, -4.5, 0))
label5.Label = "Label 5"
label5.ViewObject.FontSize = 12

# Recompute and fit the view
doc.recompute()
FreeCADGui.activeDocument().activeView().viewAxometric()
FreeCADGui.SendMsgToActiveView('ViewFit')