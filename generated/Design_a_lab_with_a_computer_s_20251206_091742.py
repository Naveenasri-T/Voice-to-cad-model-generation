import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
import FreeCAD
import Draft
doc = FreeCAD.newDocument("Lab_Blueprint")
# === FRONT VIEW (y_offset = 0) ===
# Perimeter outline
front_outline = Draft.makeWire([
    FreeCAD.Vector(0, 0, 0),
    FreeCAD.Vector(8000, 0, 0),
    FreeCAD.Vector(8000, 3000, 0),
    FreeCAD.Vector(0, 3000, 0),
    FreeCAD.Vector(0, 0, 0)
], closed=True)
front_outline.ViewObject.LineWidth = 3.0
# Internal details (doors, windows, compartments)
door1 = Draft.makeLine(FreeCAD.Vector(1000, 0, 0), FreeCAD.Vector(1900, 0, 0))
door1.ViewObject.LineWidth = 2.0
window1 = Draft.makeRectangle(800, 1200, placement=FreeCAD.Placement(FreeCAD.Vector(3000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
window1.ViewObject.LineWidth = 1.5
# Computer space
computer_space = Draft.makeRectangle(2000, 1500, placement=FreeCAD.Placement(FreeCAD.Vector(500, 500, 0), FreeCAD.Rotation(0, 0, 0)))
computer_space.ViewObject.LineWidth = 2.0
# Sub-tube
sub_tube = Draft.makeCircle(500, placement=FreeCAD.Placement(FreeCAD.Vector(6500, 1500, 0), FreeCAD.Rotation(0, 0, 0)))
sub_tube.ViewObject.LineWidth = 2.0
# Dimensions - MODERN API (FreeCAD 0.21+)
dim1 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, -500, 0),
    FreeCAD.Vector(8000, -500, 0)
)
dim1.ViewObject.FontSize = 300
dim2 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 0, 0),
    FreeCAD.Vector(0, 3000, 0)
)
dim2.ViewObject.FontSize = 300
# Labels
label_door = Draft.makeText(["Door"], point=FreeCAD.Vector(1450, -200, 0))
label_door.ViewObject.FontSize = 200
label_window = Draft.makeText(["Window"], point=FreeCAD.Vector(3500, 1300, 0))
label_window.ViewObject.FontSize = 200
label_computer_space = Draft.makeText(["Computer Space"], point=FreeCAD.Vector(1000, 2000, 0))
label_computer_space.ViewObject.FontSize = 200
label_sub_tube = Draft.makeText(["Sub-tube"], point=FreeCAD.Vector(7000, 2000, 0))
label_sub_tube.ViewObject.FontSize = 200
# === TOP VIEW (y_offset = 10000) ===
# Floor plan with rooms, furniture, fixtures
top_outline = Draft.makeWire([
    FreeCAD.Vector(0, 10000, 0),
    FreeCAD.Vector(8000, 10000, 0),
    FreeCAD.Vector(8000, 13000, 0),
    FreeCAD.Vector(0, 13000, 0),
    FreeCAD.Vector(0, 10000, 0)
], closed=True)
top_outline.ViewObject.LineWidth = 3.0
# Computer space
computer_space_top = Draft.makeRectangle(2000, 1500, placement=FreeCAD.Placement(FreeCAD.Vector(500, 10500, 0), FreeCAD.Rotation(0, 0, 0)))
computer_space_top.ViewObject.LineWidth = 2.0
# Sub-tube
sub_tube_top = Draft.makeCircle(500, placement=FreeCAD.Placement(FreeCAD.Vector(6500, 11500, 0), FreeCAD.Rotation(0, 0, 0)))
sub_tube_top.ViewObject.LineWidth = 2.0
# Dimensions
dim3 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 10000, 0),
    FreeCAD.Vector(8000, 10000, 0)
)
dim3.ViewObject.FontSize = 300
dim4 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 10000, 0),
    FreeCAD.Vector(0, 13000, 0)
)
dim4.ViewObject.FontSize = 300
# Labels
label_computer_space_top = Draft.makeText(["Computer Space"], point=FreeCAD.Vector(1000, 12500, 0))
label_computer_space_top.ViewObject.FontSize = 200
label_sub_tube_top = Draft.makeText(["Sub-tube"], point=FreeCAD.Vector(7000, 12500, 0))
label_sub_tube_top.ViewObject.FontSize = 200
# === SIDE VIEW (y_offset = 20000) ===
# Profile projection showing depth
side_outline = Draft.makeWire([
    FreeCAD.Vector(0, 20000, 0),
    FreeCAD.Vector(8000, 20000, 0),
    FreeCAD.Vector(8000, 23000, 0),
    FreeCAD.Vector(0, 23000, 0),
    FreeCAD.Vector(0, 20000, 0)
], closed=True)
side_outline.ViewObject.LineWidth = 3.0
# Computer space
computer_space_side = Draft.makeRectangle(2000, 1500, placement=FreeCAD.Placement(FreeCAD.Vector(500, 20500, 0), FreeCAD.Rotation(0, 0, 0)))
computer_space_side.ViewObject.LineWidth = 2.0
# Sub-tube
sub_tube_side = Draft.makeCircle(500, placement=FreeCAD.Placement(FreeCAD.Vector(6500, 21500, 0), FreeCAD.Rotation(0, 0, 0)))
sub_tube_side.ViewObject.LineWidth = 2.0
# Dimensions
dim5 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 20000, 0),
    FreeCAD.Vector(8000, 20000, 0)
)
dim5.ViewObject.FontSize = 300
dim6 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 20000, 0),
    FreeCAD.Vector(0, 23000, 0)
)
dim6.ViewObject.FontSize = 300
# Labels
label_computer_space_side = Draft.makeText(["Computer Space"], point=FreeCAD.Vector(1000, 22500, 0))
label_computer_space_side.ViewObject.FontSize = 200
label_sub_tube_side = Draft.makeText(["Sub-tube"], point=FreeCAD.Vector(7000, 22500, 0))
label_sub_tube_side.ViewObject.FontSize = 200
# === GRID SYSTEM ===
# Grid lines every 1000mm with A,B,C labels
for i in range(0, 9000, 1000):
    grid_line = Draft.makeLine(FreeCAD.Vector(i, 0, 0), FreeCAD.Vector(i, 3000, 0))
    grid_line.ViewObject.LineWidth = 0.5
    try:
        grid_line.ViewObject.LineStyle = "Dashed"
    except AttributeError:
        pass  # LineStyle not supported on this object
    label_grid = Draft.makeText([chr(65 + i//1000)], point=FreeCAD.Vector(i, -200, 0))
    label_grid.ViewObject.FontSize = 200
for i in range(0, 9000, 1000):
    grid_line = Draft.makeLine(FreeCAD.Vector(0, i, 0), FreeCAD.Vector(8000, i, 0))
    grid_line.ViewObject.LineWidth = 0.5
    try:
        grid_line.ViewObject.LineStyle = "Dashed"
    except AttributeError:
        pass  # LineStyle not supported on this object
# === TITLE BLOCK ===
# Drawing name, scale, date
title_block = Draft.makeText(["Lab Blueprint", "Scale: 1:100", "Date: 2024-09-16"], point=FreeCAD.Vector(6000, -500, 0))
title_block.ViewObject.FontSize = 200
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.activeDocument().activeView().viewTop()
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
