# Import necessary modules
import FreeCAD, Part, Draft, FreeCADGui

# Create a new document
doc = FreeCAD.newDocument("Mechanical_Gear")

# Create the gear body
gear_body = doc.addObject("Part::Feature", "Gear_Body")
gear_body.Shape = Part.makeCylinder(50, 20, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))

# Create the gear teeth
gear_teeth = []
for i in range(10):
    tooth = doc.addObject("Part::Feature", "Tooth_" + str(i))
    tooth.Shape = Part.makeBox(10, 5, 5)
    tooth.Placement.Base = FreeCAD.Vector(60 * i, 0, 0)
    gear_teeth.append(tooth)

# Create the gear shaft
gear_shaft = doc.addObject("Part::Feature", "Gear_Shaft")
gear_shaft.Shape = Part.makeCylinder(10, 50, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))

# Create the gear compound
gear_compound = doc.addObject("Part::Compound", "Gear_Compound")
gear_compound.Links = [gear_body, gear_shaft] + gear_teeth

# Position the gear compound
gear_compound.Placement.Base = FreeCAD.Vector(0, 0, 0)

# Recompute the document and fit the view
doc.recompute()
FreeCADGui.activeDocument().activeView().viewAxometric()
FreeCADGui.SendMsgToActiveView('ViewFit')