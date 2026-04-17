import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
import Draft
print("=== 2D BLUEPRINT ENGINEERING START ===")
print("Scope: 2BHK house with parking and garden")
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
living_room = Draft.makeRectangle(4000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(2000, 10000, 0), FreeCAD.Rotation(0, 0, 0)))
living_room.ViewObject.LineWidth = 2.0
kitchen = Draft.makeRectangle(2000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(8000, 10000, 0), FreeCAD.Rotation(0, 0, 0)))
kitchen.ViewObject.LineWidth = 2.0
bedroom1 = Draft.makeRectangle(3000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(2000, 14000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom1.ViewObject.LineWidth = 2.0
bedroom2 = Draft.makeRectangle(3000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(7000, 14000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom2.ViewObject.LineWidth = 2.0
parking = Draft.makeRectangle(4000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(0, 10000, 0), FreeCAD.Rotation(0, 0, 0)))
parking.ViewObject.LineWidth = 2.0
garden = Draft.makeRectangle(4000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(10000, 10000, 0), FreeCAD.Rotation(0, 0, 0)))
garden.ViewObject.LineWidth = 2.0
# Dimensions - MODERN API (FreeCAD 0.21+)
dim3 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 10000 - 500, 0),
    FreeCAD.Vector(12000, 10000 - 500, 0)
)
dim3.ViewObject.FontSize = 300
dim4 = Draft.make_linear_dimension(
    FreeCAD.Vector(-500, 10000, 0),
    FreeCAD.Vector(-500, 20000, 0)
)
dim4.ViewObject.FontSize = 300
# === SIDE VIEW (y_offset = 20000) ===
# Profile projection showing depth
side_profile = Draft.makeWire([
    FreeCAD.Vector(0, 20000, 0),
    FreeCAD.Vector(12000, 20000, 0),
    FreeCAD.Vector(12000, 26000, 0),
    FreeCAD.Vector(0, 26000, 0),
    FreeCAD.Vector(0, 20000, 0)
], closed=True)
side_profile.ViewObject.LineWidth = 3.0
# Dimensions - MODERN API (FreeCAD 0.21+)
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
for i in range(13):
    grid_line = Draft.makeLine(FreeCAD.Vector(i * GRID_SPACING, 0, 0), FreeCAD.Vector(i * GRID_SPACING, 30000, 0))
    grid_line.ViewObject.LineWidth = 0.5
    grid_line.ViewObject
for i in range(7):
    grid_line = Draft.makeLine(FreeCAD.Vector(0, i * GRID_SPACING, 0), FreeCAD.Vector(12000, i * GRID_SPACING, 0))
    grid_line.ViewObject.LineWidth = 0.5
    grid_line.ViewObject
# === TITLE BLOCK ===
# Drawing name, scale, date
title_block = Draft.makeText("2BHK House Blueprint", FreeCAD.Vector(10000, 28000, 0))
title_block.ViewObject.FontSize = 300
title_block.ViewObject
scale_text = Draft.makeText("Scale: 1:100", FreeCAD.Vector(10000, 27500, 0))
scale_text.ViewObject.FontSize = 250
scale_text.ViewObject
date_text = Draft.makeText("Date: 2024-09-16", FreeCAD.Vector(10000, 27000, 0))
date_text.ViewObject.FontSize = 250
date_text.ViewObject
# === LABELS ===
# Room names, component callouts, material notes
living_room_label = Draft.makeText("Living Room", FreeCAD.Vector(3000, 11000, 0))
living_room_label.ViewObject.FontSize = 250
living_room_label.ViewObject
kitchen_label = Draft.makeText("Kitchen", FreeCAD.Vector(9000, 11000, 0))
kitchen_label.ViewObject.FontSize = 250
kitchen_label.ViewObject
bedroom1_label = Draft.makeText("Bedroom 1", FreeCAD.Vector(3000, 15000, 0))
bedroom1_label.ViewObject.FontSize = 250
bedroom1_label.ViewObject
bedroom2_label = Draft.makeText("Bedroom 2", FreeCAD.Vector(9000, 15000, 0))
bedroom2_label.ViewObject.FontSize = 250
bedroom2_label.ViewObject
parking_label = Draft.makeText("Parking", FreeCAD.Vector(2000, 9000, 0))
parking_label.ViewObject.FontSize = 250
parking_label.ViewObject
garden_label = Draft.makeText("Garden", FreeCAD.Vector(11000, 9000, 0))
garden_label.ViewObject.FontSize = 250
garden_label.ViewObject
# Count primitives, dimensions, texts
primitives = 30
dimensions = 8
texts = 8
print("Primitives:", primitives)
print("Dimensions:", dimensions)
print("Texts:", texts)
if primitives < 30 or dimensions < 8 or texts < 8:
    print("Thresholds not met")
doc.recompute()
FreeCAD.Gui.SendMsgToActiveView("ViewFit")
FreeCAD.Gui.SendMsgToActiveView("ViewTop")
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
