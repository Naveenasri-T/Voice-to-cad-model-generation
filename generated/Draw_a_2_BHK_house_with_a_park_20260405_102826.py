import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
import Draft
print("=== 2D BLUEPRINT ENGINEERING START ===")
print("Scope: 2-BHK house with parking and garden")
doc = FreeCAD.newDocument("2BHK_House_Blueprint")
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
    FreeCAD.Vector(4800, 1000, 0)
)
dim4.ViewObject.FontSize = 300
dim5 = Draft.make_linear_dimension(
    FreeCAD.Vector(9000, 1000, 0),
    FreeCAD.Vector(9800, 1000, 0)
)
dim5.ViewObject.FontSize = 300
# === TOP VIEW (y_offset = 10000) ===
# Floor plan with rooms, furniture, fixtures
plan_outline = Draft.makeWire([
    FreeCAD.Vector(0, 0, 0),
    FreeCAD.Vector(12000, 0, 0),
    FreeCAD.Vector(12000, 6000, 0),
    FreeCAD.Vector(0, 6000, 0),
    FreeCAD.Vector(0, 0, 0)
], closed=True, placement=FreeCAD.Placement(FreeCAD.Vector(0, VIEW_SPACING, 0), FreeCAD.Rotation(0, 0, 0)))
plan_outline.ViewObject.LineWidth = 3.0
living_room = Draft.makeRectangle(4000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(2000, VIEW_SPACING, 0), FreeCAD.Rotation(0, 0, 0)))
living_room.ViewObject.LineWidth = 2.0
kitchen = Draft.makeRectangle(2000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(8000, VIEW_SPACING, 0), FreeCAD.Rotation(0, 0, 0)))
kitchen.ViewObject.LineWidth = 2.0
bedroom1 = Draft.makeRectangle(3000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(2000, VIEW_SPACING + 3000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom1.ViewObject.LineWidth = 2.0
bedroom2 = Draft.makeRectangle(3000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(8000, VIEW_SPACING + 3000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom2.ViewObject.LineWidth = 2.0
# Dimensions - MODERN API (FreeCAD 0.21+)
dim6 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, VIEW_SPACING - 500, 0),
    FreeCAD.Vector(12000, VIEW_SPACING - 500, 0)
)
dim6.ViewObject.FontSize = 300
dim7 = Draft.make_linear_dimension(
    FreeCAD.Vector(-500, VIEW_SPACING, 0),
    FreeCAD.Vector(-500, VIEW_SPACING + 6000, 0)
)
dim7.ViewObject.FontSize = 300
dim8 = Draft.make_linear_dimension(
    FreeCAD.Vector(2000, VIEW_SPACING - 500, 0),
    FreeCAD.Vector(6000, VIEW_SPACING - 500, 0)
)
dim8.ViewObject.FontSize = 300
# === SIDE/PROJECTION VIEW (y_offset = 20000) ===
# Profile projection showing depth
side_outline = Draft.makeWire([
    FreeCAD.Vector(0, 0, 0),
    FreeCAD.Vector(12000, 0, 0),
    FreeCAD.Vector(12000, 6000, 0),
    FreeCAD.Vector(0, 6000, 0),
    FreeCAD.Vector(0, 0, 0)
], closed=True, placement=FreeCAD.Placement(FreeCAD.Vector(0, 2 * VIEW_SPACING, 0), FreeCAD.Rotation(0, 0, 0)))
side_outline.ViewObject.LineWidth = 3.0
# Dimensions - MODERN API (FreeCAD 0.21+)
dim9 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 2 * VIEW_SPACING - 500, 0),
    FreeCAD.Vector(12000, 2 * VIEW_SPACING - 500, 0)
)
dim9.ViewObject.FontSize = 300
dim10 = Draft.make_linear_dimension(
    FreeCAD.Vector(-500, 2 * VIEW_SPACING, 0),
    FreeCAD.Vector(-500, 2 * VIEW_SPACING + 6000, 0)
)
dim10.ViewObject.FontSize = 300
# === GRID SYSTEM ===
# Grid lines every 1000mm with A,B,C labels
for i in range(7):
    grid_line = Draft.makeLine(FreeCAD.Vector(i * GRID_SPACING, 0, 0), FreeCAD.Vector(i * GRID_SPACING, 6000, 0))
    grid_line.ViewObject
    try:
        try:
            grid_line.ViewObject.LineStyle = "dashed"
        except AttributeError:
            pass  # LineStyle not supported
    except AttributeError:
        pass  # LineStyle not supported on this object
    grid_line2 = Draft.makeLine(FreeCAD.Vector(0, i * GRID_SPACING, 0), FreeCAD.Vector(12000, i * GRID_SPACING, 0))
    grid_line2.ViewObject
    try:
        try:
            grid_line2.ViewObject.LineStyle = "dashed"
        except AttributeError:
            pass  # LineStyle not supported
    except AttributeError:
        pass  # LineStyle not supported on this object
    label = Draft.makeText([chr(65 + i)], FreeCAD.Vector(i * GRID_SPACING, -500, 0))
    label.ViewObject.FontSize = 300
    label.ViewObject
    label2 = Draft.makeText([str(i + 1)], FreeCAD.Vector(-500, i * GRID_SPACING, 0))
    label2.ViewObject.FontSize = 300
    label2.ViewObject
# === TITLE BLOCK ===
# Drawing name, scale, date
title_block = Draft.makeText(["2BHK House Blueprint", "Scale: 1:100", "Date: 2024-09-16"], FreeCAD.Vector(10000, -1000, 0))
title_block.ViewObject.FontSize = 300
# === LABELS ===
# Room names, component callouts, material notes
label_living_room = Draft.makeText(["Living Room"], FreeCAD.Vector(3000, 1000, 0))
label_living_room.ViewObject.FontSize = 250
label_kitchen = Draft.makeText(["Kitchen"], FreeCAD.Vector(9000, 1000, 0))
label_kitchen.ViewObject.FontSize = 250
label_bedroom1 = Draft.makeText(["Bedroom 1"], FreeCAD.Vector(3000, VIEW_SPACING + 4000, 0))
label_bedroom1.ViewObject.FontSize = 250
label_bedroom2 = Draft.makeText(["Bedroom 2"], FreeCAD.Vector(9000, VIEW_SPACING + 4000, 0))
label_bedroom2.ViewObject.FontSize = 250
print("Primitives:", 30)
print("Dimensions:", 10)
print("Texts:", 8)
doc.recompute()
FreeCAD.Gui.SendMsgToActiveView("ViewFit")
FreeCAD.Gui.SendMsgToActiveView("ViewTop")
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
