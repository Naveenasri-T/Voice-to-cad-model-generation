import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
# Import necessary modules
import FreeCAD
import Part

# Create a new document
doc = FreeCAD.newDocument()

# Create a gear
# Define gear parameters
pitch_radius = 10
thickness = 5
teeth_number = 20
pressure_angle = 20

# Create a gear profile
gear_profile = Part.makeCircle(pitch_radius, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))

# Create a gear
gear = Part.makePrism(gear_profile, FreeCAD.Vector(0, 0, thickness))

# Create teeth
for i in range(teeth_number):
    tooth_angle = 360 / teeth_number * i
    tooth_profile = Part.makeCircle(pitch_radius + 2, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
    tooth = Part.makePrism(tooth_profile, FreeCAD.Vector(0, 0, thickness))
    tooth.translate(FreeCAD.Vector(pitch_radius * 2 * math.sin(math.radians(tooth_angle)),
                                   pitch_radius * 2 * math.cos(math.radians(tooth_angle)),
                                   0))
    gear = gear.fuse(tooth)

# Create a shaft
shaft = Part.makeCylinder(2, thickness, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))

# Combine gear and shaft
gear = gear.fuse(shaft)

# Add the gear to the document
doc.addObject("Part::Feature", "Gear").Shape = gear

# Recompute the document and fit the view
doc.recompute()
FreeCAD.Gui.SendMsgToActiveView("ViewFit")
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
