import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
import FreeCAD
import Part

# Create new document
doc = FreeCAD.newDocument("Simple_Cube")

# Create a simple cube
cube = Part.makeBox(1000, 1000, 1000)  # 1m x 1m x 1m cube
cube_obj = doc.addObject("Part::Feature", "Cube")
cube_obj.Shape = cube

# Recompute the document
doc.recompute()

print("Simple cube created successfully!")

doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
