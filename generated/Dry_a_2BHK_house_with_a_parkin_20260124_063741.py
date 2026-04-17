import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
import FreeCAD
import Draft
doc = FreeCAD.newDocument("2BHK_House_Blueprint")
# === FRONT VIEW (y_offset = 0) ===
# Perimeter outline
front_outline = Draft.makeWire([
    FreeCAD.Vector(0, 0, 0),
    FreeCAD.Vector(12000, 0, 0),
    FreeCAD.Vector(12000, 6000, 0),
    FreeCAD.Vector(0, 6000, 0),
    FreeCAD.Vector(0, 0, 0)
], closed=True)
front_outline.ViewObject.LineWidth = 3.0
# Internal details (doors, windows, compartments)
door1 = Draft.makeLine(FreeCAD.Vector(1000, 0, 0), FreeCAD.Vector(1900, 0, 0))
door1.ViewObject.LineWidth = 2.0
window1 = Draft.makeRectangle(800, 1200, placement=FreeCAD.Placement(FreeCAD.Vector(3000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
window1.ViewObject.LineWidth = 1.5
window2 = Draft.makeRectangle(800, 1200, placement=FreeCAD.Placement(FreeCAD.Vector(8000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
window2.ViewObject.LineWidth = 1.5
# Dimensions - MODERN API (FreeCAD 0.21+)
dim1 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, -500, 0),
    FreeCAD.Vector(12000, -500, 0)
)
dim1.ViewObject.FontSize = 300
dim2 = Draft.make_linear_dimension(
    FreeCAD.Vector(-500, 0, 0),
    FreeCAD.Vector(-500, 6000, 0)
)
dim2.ViewObject.FontSize = 300
# === TOP VIEW (y_offset = 10000) ===
# Floor plan with rooms, furniture, fixtures
top_outline = Draft.makeWire([
    FreeCAD.Vector(0, 10000, 0),
    FreeCAD.Vector(12000, 10000, 0),
    FreeCAD.Vector(12000, 16000, 0),
    FreeCAD.Vector(0, 16000, 0),
    FreeCAD.Vector(0, 10000, 0)
], closed=True)
top_outline.ViewObject.LineWidth = 3.0
# Internal walls
internal_wall1 = Draft.makeLine(FreeCAD.Vector(4000, 10000, 0), FreeCAD.Vector(4000, 16000, 0))
internal_wall1.ViewObject.LineWidth = 2.0
internal_wall2 = Draft.makeLine(FreeCAD.Vector(8000, 10000, 0), FreeCAD.Vector(8000, 16000, 0))
internal_wall2.ViewObject.LineWidth = 2.0
# Furniture
bed = Draft.makeRectangle(2000, 1500, placement=FreeCAD.Placement(FreeCAD.Vector(500, 11000, 0), FreeCAD.Rotation(0, 0, 0)))
bed.ViewObject.LineWidth = 1.5
sofa = Draft.makeRectangle(2000, 1000, placement=FreeCAD.Placement(FreeCAD.Vector(9000, 11000, 0), FreeCAD.Rotation(0, 0, 0)))
sofa.ViewObject.LineWidth = 1.5
# Dimensions
dim3 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 10000 - 500, 0),
    FreeCAD.Vector(12000, 10000 - 500, 0)
)
dim3.ViewObject.FontSize = 300
dim4 = Draft.make_linear_dimension(
    FreeCAD.Vector(-500, 10000, 0),
    FreeCAD.Vector(-500, 16000, 0)
)
dim4.ViewObject.FontSize = 300
# === SIDE VIEW (y_offset = 20000) ===
# Profile projection showing depth
side_outline = Draft.makeWire([
    FreeCAD.Vector(0, 20000, 0),
    FreeCAD.Vector(12000, 20000, 0),
    FreeCAD.Vector(12000, 26000, 0),
    FreeCAD.Vector(0, 26000, 0),
    FreeCAD.Vector(0, 20000, 0)
], closed=True)
side_outline.ViewObject.LineWidth = 3.0
# Profile details
profile_line1 = Draft.makeLine(FreeCAD.Vector(0, 22000, 0), FreeCAD.Vector(12000, 22000, 0))
profile_line1.ViewObject.LineWidth = 2.0
profile_line2 = Draft.makeLine(FreeCAD.Vector(0, 24000, 0), FreeCAD.Vector(12000, 24000, 0))
profile_line2.ViewObject.LineWidth = 2.0
# Dimensions
dim5 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 20000 - 500, 0),
    FreeCAD.Vector(12000, 20000 - 500, 0)
)
dim5.ViewObject.FontSize = 300
dim6 = Draft.make_linear_dimension(
    FreeCAD.Vector(-500, 20000, 0),
    FreeCAD.Vector(-500, 26000, 0)
)
dim6.ViewObject.FontSize = 300
# === GRID SYSTEM ===
# Grid lines every 1000mm with A,B,C labels
for i in range(0, 13000, 1000):
    grid_line = Draft.makeLine(FreeCAD.Vector(i, 0, 0), FreeCAD.Vector(i, 6000, 0))
    grid_line.ViewObject.LineWidth = 0.5
    try:
        grid_line.ViewObject.LineStyle = "Dashed"
    except AttributeError:
        pass  # LineStyle not supported on this object
    label = Draft.makeText([chr(65 + i // 1000)], point=FreeCAD.Vector(i, -500, 0))
    label.ViewObject.FontSize = 200
for i in range(0, 13000, 1000):
    grid_line = Draft.makeLine(FreeCAD.Vector(i, 10000, 0), FreeCAD.Vector(i, 16000, 0))
    grid_line.ViewObject.LineWidth = 0.5
    try:
        grid_line.ViewObject.LineStyle = "Dashed"
    except AttributeError:
        pass  # LineStyle not supported on this object
    label = Draft.makeText([chr(65 + i // 1000)], point=FreeCAD.Vector(i, 10000 - 500, 0))
    label.ViewObject.FontSize = 200
for i in range(0, 13000, 1000):
    grid_line = Draft.makeLine(FreeCAD.Vector(i, 20000, 0), FreeCAD.Vector(i, 26000, 0))
    grid_line.ViewObject.LineWidth = 0.5
    try:
        grid_line.ViewObject.LineStyle = "Dashed"
    except AttributeError:
        pass  # LineStyle not supported on this object
    label = Draft.makeText([chr(65 + i // 1000)], point=FreeCAD.Vector(i, 20000 - 500, 0))
    label.ViewObject.FontSize = 200
# === TITLE BLOCK ===
# Drawing name, scale, date
title_block = Draft.makeText(["2BHK House Blueprint", "Scale: 1:100", "Date: 2024-09-16"], point=FreeCAD.Vector(10000, 0, 0))
title_block.ViewObject.FontSize = 200
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.activeDocument().activeView().viewTop()
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
