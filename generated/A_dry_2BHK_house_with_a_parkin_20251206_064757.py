import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
import FreeCAD
import Draft
# Create a new document
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
main_door = Draft.makeLine(FreeCAD.Vector(2000, 0, 0), FreeCAD.Vector(3000, 0, 0))
main_door.ViewObject.LineWidth = 2.0
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
    FreeCAD.Vector(0, 0, 0),
    FreeCAD.Vector(0, 6000, 0)
)
dim2.ViewObject.FontSize = 300
# === TOP VIEW (y_offset = 8000) ===
# Floor plan with rooms, furniture, fixtures
top_view_y = 8000
living_room = Draft.makeRectangle(4000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(2000, top_view_y, 0), FreeCAD.Rotation(0, 0, 0)))
living_room.ViewObject.LineWidth = 2.0
kitchen = Draft.makeRectangle(2000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(7000, top_view_y, 0), FreeCAD.Rotation(0, 0, 0)))
kitchen.ViewObject.LineWidth = 2.0
bedroom1 = Draft.makeRectangle(3000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(2000, top_view_y + 4000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom1.ViewObject.LineWidth = 2.0
bedroom2 = Draft.makeRectangle(3000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(7000, top_view_y + 4000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom2.ViewObject.LineWidth = 2.0
# Dimensions - MODERN API (FreeCAD 0.21+)
dim3 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, top_view_y - 500, 0),
    FreeCAD.Vector(12000, top_view_y - 500, 0)
)
dim3.ViewObject.FontSize = 300
dim4 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, top_view_y, 0),
    FreeCAD.Vector(0, top_view_y + 8000, 0)
)
dim4.ViewObject.FontSize = 300
# === SIDE VIEW (y_offset = 16000) ===
# Profile projection showing depth
side_view_y = 16000
profile = Draft.makeRectangle(12000, 6000, placement=FreeCAD.Placement(FreeCAD.Vector(0, side_view_y, 0), FreeCAD.Rotation(0, 0, 0)))
profile.ViewObject.LineWidth = 2.0
# Dimensions - MODERN API (FreeCAD 0.21+)
dim5 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, side_view_y - 500, 0),
    FreeCAD.Vector(12000, side_view_y - 500, 0)
)
dim5.ViewObject.FontSize = 300
dim6 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, side_view_y, 0),
    FreeCAD.Vector(0, side_view_y + 6000, 0)
)
dim6.ViewObject.FontSize = 300
# === GRID SYSTEM ===
grid_spacing = 1000
for i in range(0, 13000, grid_spacing):
    grid_line = Draft.makeLine(FreeCAD.Vector(i, 0, 0), FreeCAD.Vector(i, 8000, 0))
    grid_line.ViewObject.LineWidth = 0.5
    grid_line.ViewObject.LineStyle = "Dashed"
    grid_label = Draft.makeText([chr(65 + i//grid_spacing)], point=FreeCAD.Vector(i, -500, 0))
    grid_label.ViewObject.FontSize = 300
    grid_label.ViewObject.TextColor = (0.0, 0.0, 0.0)
for i in range(0, 9000, grid_spacing):
    grid_line = Draft.makeLine(FreeCAD.Vector(0, i, 0), FreeCAD.Vector(12000, i, 0))
    grid_line.ViewObject.LineWidth = 0.5
    grid_line.ViewObject.LineStyle = "Dashed"
    grid_label = Draft.makeText([str(1 + i//grid_spacing)], point=FreeCAD.Vector(-500, i, 0))
    grid_label.ViewObject.FontSize = 300
    grid_label.ViewObject.TextColor = (0.0, 0.0, 0.0)
# === TITLE BLOCK ===
title_block = Draft.makeText(["2BHK House Blueprint", "Scale: 1:100", "Date: 2024-09-16"], point=FreeCAD.Vector(10000, 7000, 0))
title_block.ViewObject.FontSize = 300
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.activeDocument().activeView().viewTop()
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
