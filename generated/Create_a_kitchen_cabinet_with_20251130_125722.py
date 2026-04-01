import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
import FreeCAD
import Draft
# TEMPLATE_GENERATED
doc = FreeCAD.newDocument("Technical_Drawing")
# Front View
front = Draft.makeRectangle(5000, 3000)
front.ViewObject.LineWidth = 2.5
Draft.make_text(["FRONT VIEW"], placement=FreeCAD.Placement(FreeCAD.Vector(1500, -500, 0), FreeCAD.Rotation(0, 0, 0)))
# Top View
top = Draft.makeRectangle(5000, 4000, placement=FreeCAD.Placement(FreeCAD.Vector(0, 5000, 0), FreeCAD.Rotation(0, 0, 0)))
top.ViewObject.LineWidth = 2.5
Draft.make_text(["TOP VIEW"], placement=FreeCAD.Placement(FreeCAD.Vector(1500, 4500, 0), FreeCAD.Rotation(0, 0, 0)))
# Dimensions
dim1 = Draft.make_linear_dimension(FreeCAD.Vector(0, -800, 0), FreeCAD.Vector(5000, -800, 0))
dim1.ViewObject.FontSize = 250
dim2 = Draft.make_linear_dimension(FreeCAD.Vector(-800, 0, 0), FreeCAD.Vector(-800, 3000, 0))
dim2.ViewObject.FontSize = 250
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.activeDocument().activeView().viewTop()
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
