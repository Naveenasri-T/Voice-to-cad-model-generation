import FreeCAD, Part, Draft, FreeCADGui

# Create a new document
doc = FreeCAD.newDocument("Model")

# Create a cube with side length 10
cube = Part.makeBox(10, 10, 10)

# Add the cube to the document
cube_feature = doc.addObject("Part::Feature", "Cube")
cube_feature.Shape = cube

# Recompute the document and fit the view
doc.recompute()
FreeCADGui.activeDocument().activeView().viewAxometric()
FreeCADGui.SendMsgToActiveView('ViewFit')