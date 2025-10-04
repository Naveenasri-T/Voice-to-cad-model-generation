# Import necessary modules
import FreeCAD, Part, Draft, FreeCADGui

# Create a new document
doc = FreeCAD.newDocument("Car_Model")

# Create the body of the car
body = doc.addObject("Part::Feature", "Car_Body")
body.Shape = Part.makeBox(4000, 1800, 1200)  # Length, Width, Height
body.Placement.Base = FreeCAD.Vector(0, 0, 600)  # Position the body

# Create the front wheels
front_wheel1 = doc.addObject("Part::Feature", "Front_Wheel1")
front_wheel1.Shape = Part.makeCylinder(400, 600)  # Radius, Height
front_wheel1.Placement.Base = FreeCAD.Vector(-1500, 900, 0)  # Position the wheel

front_wheel2 = doc.addObject("Part::Feature", "Front_Wheel2")
front_wheel2.Shape = Part.makeCylinder(400, 600)  # Radius, Height
front_wheel2.Placement.Base = FreeCAD.Vector(-1500, -900, 0)  # Position the wheel

# Create the rear wheels
rear_wheel1 = doc.addObject("Part::Feature", "Rear_Wheel1")
rear_wheel1.Shape = Part.makeCylinder(400, 600)  # Radius, Height
rear_wheel1.Placement.Base = FreeCAD.Vector(1500, 900, 0)  # Position the wheel

rear_wheel2 = doc.addObject("Part::Feature", "Rear_Wheel2")
rear_wheel2.Shape = Part.makeCylinder(400, 600)  # Radius, Height
rear_wheel2.Placement.Base = FreeCAD.Vector(1500, -900, 0)  # Position the wheel

# Create the windshield
windshield = doc.addObject("Part::Feature", "Windshield")
windshield.Shape = Part.makeBox(2000, 1000, 500)  # Length, Width, Height
windshield.Placement.Base = FreeCAD.Vector(0, 0, 1700)  # Position the windshield

# Create the headlights
headlight1 = doc.addObject("Part::Feature", "Headlight1")
headlight1.Shape = Part.makeSphere(100)  # Radius
headlight1.Placement.Base = FreeCAD.Vector(-1200, 1000, 1200)  # Position the headlight

headlight2 = doc.addObject("Part::Feature", "Headlight2")
headlight2.Shape = Part.makeSphere(100)  # Radius
headlight2.Placement.Base = FreeCAD.Vector(-1200, -1000, 1200)  # Position the headlight

# Create the exhaust pipe
exhaust_pipe = doc.addObject("Part::Feature", "Exhaust_Pipe")
exhaust_pipe.Shape = Part.makeCylinder(50, 500)  # Radius, Height
exhaust_pipe.Placement.Base = FreeCAD.Vector(1500, 0, 0)  # Position the exhaust pipe
exhaust_pipe.Placement.Rotation = FreeCAD.Rotation(90, 0, 0)  # Rotate the exhaust pipe

# Combine all the objects into a single compound
compound = doc.addObject("Part::Compound", "Car")
compound.Links = [body, front_wheel1, front_wheel2, rear_wheel1, rear_wheel2, windshield, headlight1, headlight2, exhaust_pipe]

# Recompute the document and fit the view
doc.recompute()
FreeCADGui.activeDocument().activeView().viewAxometric()
FreeCADGui.SendMsgToActiveView('ViewFit')