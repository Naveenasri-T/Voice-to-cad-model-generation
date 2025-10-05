
import FreeCAD, Part, FreeCADGui
doc = FreeCAD.newDocument("Model")
box = doc.addObject("Part::Feature", "Box")
box.Shape = Part.makeBox(1000, 1000, 1000)
doc.recompute()
