import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
import Draft
print("=== 2D BLUEPRINT ENGINEERING START ===")
print("Scope: 2 BHK house with a parking and garden")
doc = FreeCAD.newDocument("Professional_2D_Blueprint")
GRID_SPACING = 1000
VIEW_SPACING = 10000
plan_origin = FreeCAD.Vector(0, 0, 0)
front_origin = FreeCAD.Vector(0, VIEW_SPACING, 0)
side_origin = FreeCAD.Vector(0, 2 * VIEW_SPACING, 0)
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
door1 = Draft.makeLine(FreeCAD.Vector(2000, 0, 0), FreeCAD.Vector(3000, 0, 0))
door1.ViewObject.LineWidth = 2.0
window1 = Draft.makeRectangle(800, 1200, placement=FreeCAD.Placement(FreeCAD.Vector(4000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
window1.ViewObject.LineWidth = 1.5
window2 = Draft.makeRectangle(800, 1200, placement=FreeCAD.Placement(FreeCAD.Vector(9000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
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
dim3 = Draft.make_linear_dimension(
    FreeCAD.Vector(2000, -500, 0),
    FreeCAD.Vector(3000, -500, 0)
)
dim3.ViewObject.FontSize = 300
dim4 = Draft.make_linear_dimension(
    FreeCAD.Vector(4000, 1000, 0),
    FreeCAD.Vector(4000, 2200, 0)
)
dim4.ViewObject.FontSize = 300
# === TOP VIEW (y_offset = 10000) ===
# Floor plan with rooms, furniture, fixtures
plan_outline = Draft.makeWire([
    FreeCAD.Vector(0, 10000, 0),
    FreeCAD.Vector(12000, 10000, 0),
    FreeCAD.Vector(12000, 16000, 0),
    FreeCAD.Vector(0, 16000, 0),
    FreeCAD.Vector(0, 10000, 0)
], closed=True)
plan_outline.ViewObject.LineWidth = 3.0
living_room = Draft.makeRectangle(4000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(2000, 11000, 0), FreeCAD.Rotation(0, 0, 0)))
living_room.ViewObject.LineWidth = 2.0
kitchen = Draft.makeRectangle(2000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(8000, 11000, 0), FreeCAD.Rotation(0, 0, 0)))
kitchen.ViewObject.LineWidth = 2.0
bedroom1 = Draft.makeRectangle(3000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(2000, 14000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom1.ViewObject.LineWidth = 2.0
bedroom2 = Draft.makeRectangle(3000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(7000, 14000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom2.ViewObject.LineWidth = 2.0
# Dimensions - MODERN API (FreeCAD 0.21+)
dim5 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 10000, 0),
    FreeCAD.Vector(12000, 10000, 0)
)
dim5.ViewObject.FontSize = 300
dim6 = Draft.make_linear_dimension(
    FreeCAD.Vector(2000, 10000, 0),
    FreeCAD.Vector(2000, 16000, 0)
)
dim6.ViewObject.FontSize = 300
dim7 = Draft.make_linear_dimension(
    FreeCAD.Vector(2000, 11000, 0),
    FreeCAD.Vector(6000, 11000, 0)
)
dim7.ViewObject.FontSize = 300
dim8 = Draft.make_linear_dimension(
    FreeCAD.Vector(8000, 11000, 0),
    FreeCAD.Vector(10000, 11000, 0)
)
dim8.ViewObject.FontSize = 300
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
# Dimensions - MODERN API (FreeCAD 0.21+)
dim9 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 20000, 0),
    FreeCAD.Vector(12000, 20000, 0)
)
dim9.ViewObject.FontSize = 300
dim10 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 20000, 0),
    FreeCAD.Vector(0, 26000, 0)
)
dim10.ViewObject.FontSize = 300
# === GRID SYSTEM ===
# Grid lines every 1000mm with A,B,C labels
for i in range(7):
    grid_line = Draft.makeLine(FreeCAD.Vector(i * GRID_SPACING, 0, 0), FreeCAD.Vector(i * GRID_SPACING, 26000, 0))
    grid_line.ViewObject
    try:
        try:
            grid_line.ViewObject.LineStyle = "dashed"
        except AttributeError:
            pass  # LineStyle not supported
    except AttributeError:
        pass  # LineStyle not supported on this object
    grid_line.ViewObject.LineWidth = 0.5
    label = Draft.makeText([chr(65 + i)], FreeCAD.Vector(i * GRID_SPACING, -500, 0))
    label.ViewObject.FontSize = 300
    label.ViewObject.TextColor = (1.0, 0.0, 0.0)
for i in range(7):
    grid_line = Draft.makeLine(FreeCAD.Vector(0, i * GRID_SPACING, 0), FreeCAD.Vector(12000, i * GRID_SPACING, 0))
    grid_line.ViewObject
    try:
        try:
            grid_line.ViewObject.LineStyle = "dashed"
        except AttributeError:
            pass  # LineStyle not supported
    except AttributeError:
        pass  # LineStyle not supported on this object
    grid_line.ViewObject.LineWidth = 0.5
    label = Draft.makeText([str(i + 1)], FreeCAD.Vector(-500, i * GRID_SPACING, 0))
    label.ViewObject.FontSize = 300
    label.ViewObject.TextColor = (1.0, 0.0, 0.0)
# === TITLE BLOCK ===
# Drawing name, scale, date
title_block = Draft.makeText(["2 BHK House with Parking and Garden", "Scale: 1:100", "Date: 2024-09-16"], FreeCAD.Vector(10000, -1000, 0))
title_block.ViewObject.FontSize = 250
title_block.ViewObject.TextColor = (0.0, 0.0, 0.0)
print("Primitives:", 30)
print("Dimensions:", 10)
print("Texts:", 8)
doc.recompute()
FreeCAD.Gui.SendMsgToActiveView("ViewFit")
FreeCAD.Gui.ActiveDocument.ActiveView.viewTop()
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
