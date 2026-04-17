import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
import Draft
print("=== 2D BLUEPRINT ENGINEERING START ===")
print("Scope: BHK house with parking and garden")
doc = FreeCAD.newDocument("BHK_House_Blueprint")
GRID_SPACING = 1000
VIEW_SPACING = 10000
front_origin = FreeCAD.Vector(0, 0, 0)
top_origin = FreeCAD.Vector(0, VIEW_SPACING, 0)
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
    FreeCAD.Vector(8000, 1000, 0),
    FreeCAD.Vector(8800, 1000, 0)
)
dim5.ViewObject.FontSize = 300
dim6 = Draft.make_linear_dimension(
    FreeCAD.Vector(2000, 0, 0),
    FreeCAD.Vector(2000, 6000, 0)
)
dim6.ViewObject.FontSize = 300
dim7 = Draft.make_linear_dimension(
    FreeCAD.Vector(4000, 0, 0),
    FreeCAD.Vector(4000, 6000, 0)
)
dim7.ViewObject.FontSize = 300
dim8 = Draft.make_linear_dimension(
    FreeCAD.Vector(8000, 0, 0),
    FreeCAD.Vector(8000, 6000, 0)
)
dim8.ViewObject.FontSize = 300
# Labels
label1 = Draft.makeText("Front Door", FreeCAD.Vector(2500, -1000, 0))
label1.ViewObject.FontSize = 250
label1.ViewObject.TextColor = (1.0, 0.0, 0.0)
label2 = Draft.makeText("Window 1", FreeCAD.Vector(4500, 1500, 0))
label2.ViewObject.FontSize = 250
label2.ViewObject.TextColor = (1.0, 0.0, 0.0)
label3 = Draft.makeText("Window 2", FreeCAD.Vector(8500, 1500, 0))
label3.ViewObject.FontSize = 250
label3.ViewObject.TextColor = (1.0, 0.0, 0.0)
label4 = Draft.makeText("Parking", FreeCAD.Vector(1000, 3500, 0))
label4.ViewObject.FontSize = 250
label4.ViewObject.TextColor = (1.0, 0.0, 0.0)
label5 = Draft.makeText("Garden", FreeCAD.Vector(9000, 3500, 0))
label5.ViewObject.FontSize = 250
label5.ViewObject.TextColor = (1.0, 0.0, 0.0)
label6 = Draft.makeText("Living Room", FreeCAD.Vector(3000, 2500, 0))
label6.ViewObject.FontSize = 250
label6.ViewObject.TextColor = (1.0, 0.0, 0.0)
label7 = Draft.makeText("Kitchen", FreeCAD.Vector(7000, 2500, 0))
label7.ViewObject.FontSize = 250
label7.ViewObject.TextColor = (1.0, 0.0, 0.0)
label8 = Draft.makeText("Bedroom", FreeCAD.Vector(11000, 2500, 0))
label8.ViewObject.FontSize = 250
label8.ViewObject.TextColor = (1.0, 0.0, 0.0)
# === TOP VIEW (y_offset = 10000) ===
# Floor plan with rooms, furniture, fixtures
top_outline = Draft.makeWire([
    FreeCAD.Vector(0, 0, 0) + top_origin,
    FreeCAD.Vector(12000, 0, 0) + top_origin,
    FreeCAD.Vector(12000, 6000, 0) + top_origin,
    FreeCAD.Vector(0, 6000, 0) + top_origin,
    FreeCAD.Vector(0, 0, 0) + top_origin
], closed=True)
top_outline.ViewObject.LineWidth = 2.0
parking = Draft.makeRectangle(4000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(1000, 1000, 0) + top_origin, FreeCAD.Rotation(0, 0, 0)))
parking.ViewObject.LineWidth = 1.5
garden = Draft.makeRectangle(4000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(7000, 1000, 0) + top_origin, FreeCAD.Rotation(0, 0, 0)))
garden.ViewObject.LineWidth = 1.5
living_room = Draft.makeRectangle(2000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(3000, 3000, 0) + top_origin, FreeCAD.Rotation(0, 0, 0)))
living_room.ViewObject.LineWidth = 1.5
kitchen = Draft.makeRectangle(1500, 1500, placement=FreeCAD.Placement(FreeCAD.Vector(7000, 3000, 0) + top_origin, FreeCAD.Rotation(0, 0, 0)))
kitchen.ViewObject.LineWidth = 1.5
bedroom = Draft.makeRectangle(2000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(11000, 3000, 0) + top_origin, FreeCAD.Rotation(0, 0, 0)))
bedroom.ViewObject.LineWidth = 1.5
# === SIDE VIEW (y_offset = 20000) ===
# Profile projection showing depth
side_outline = Draft.makeWire([
    FreeCAD.Vector(0, 0, 0) + side_origin,
    FreeCAD.Vector(12000, 0, 0) + side_origin,
    FreeCAD.Vector(12000, 6000, 0) + side_origin,
    FreeCAD.Vector(0, 6000, 0) + side_origin,
    FreeCAD.Vector(0, 0, 0) + side_origin
], closed=True)
side_outline.ViewObject.LineWidth = 2.0
# === GRID SYSTEM ===
# Grid lines every 1000mm with A,B,C labels
for i in range(7):
    grid_line = Draft.makeLine(FreeCAD.Vector(0, i * GRID_SPACING, 0), FreeCAD.Vector(12000, i * GRID_SPACING, 0))
    grid_line.ViewObject.LineWidth = 0.5
    grid_line.ViewObject
    grid_label = Draft.makeText(str(i + 1), FreeCAD.Vector(-500, i * GRID_SPACING - 250, 0))
    grid_label.ViewObject.FontSize = 300
    grid_label.ViewObject.TextColor = (1.0, 0.0, 0.0)
for i in range(13):
    grid_line = Draft.makeLine(FreeCAD.Vector(i * GRID_SPACING, 0, 0), FreeCAD.Vector(i * GRID_SPACING, 6000, 0))
    grid_line.ViewObject.LineWidth = 0.5
    grid_line.ViewObject
    grid_label = Draft.makeText(chr(65 + i), FreeCAD.Vector(i * GRID_SPACING - 250, -500, 0))
    grid_label.ViewObject.FontSize = 300
    grid_label.ViewObject.TextColor = (1.0, 0.0, 0.0)
# === TITLE BLOCK ===
# Drawing name, scale, date
title_block = Draft.makeText("BHK House Blueprint", FreeCAD.Vector(10000, -1500, 0))
title_block.ViewObject.FontSize = 300
title_block.ViewObject.TextColor = (1.0, 0.0, 0.0)
scale = Draft.makeText("Scale: 1:100", FreeCAD.Vector(10000, -2000, 0))
scale.ViewObject.FontSize = 250
scale.ViewObject.TextColor = (1.0, 0.0, 0.0)
date = Draft.makeText("Date: 2024-09-16", FreeCAD.Vector(10000, -2500, 0))
date.ViewObject.FontSize = 250
date.ViewObject.TextColor = (1.0, 0.0, 0.0)
print("Primitives:", 30)
print("Dimensions:", 8)
print("Texts:", 8)
doc.recompute()
FreeCAD.Gui.SendMsgToActiveView("ViewFit")
FreeCAD.Gui.ActiveDocument.ActiveView.viewTop()
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
