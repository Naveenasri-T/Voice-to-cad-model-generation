import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
import FreeCAD
import Draft
# Create a new document
doc = FreeCAD.newDocument("2BHK_House")
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
window2 = Draft.makeRectangle(800, 1200, placement=FreeCAD.Placement(FreeCAD.Vector(7000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
window2.ViewObject.LineWidth = 1.5
# Parking gate
parking_gate = Draft.makeLine(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(2000, 0, 0))
parking_gate.ViewObject.LineWidth = 2.0
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
# === TOP VIEW (y_offset = 8000) ===
# Floor plan with rooms, furniture, fixtures
top_view_y_offset = 8000
living_room = Draft.makeRectangle(4000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(2000, top_view_y_offset, 0), FreeCAD.Rotation(0, 0, 0)))
living_room.ViewObject.LineWidth = 1.5
kitchen = Draft.makeRectangle(2000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(8000, top_view_y_offset, 0), FreeCAD.Rotation(0, 0, 0)))
kitchen.ViewObject.LineWidth = 1.5
bedroom1 = Draft.makeRectangle(3000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(2000, top_view_y_offset + 4000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom1.ViewObject.LineWidth = 1.5
bedroom2 = Draft.makeRectangle(3000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(6000, top_view_y_offset + 4000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom2.ViewObject.LineWidth = 1.5
# Dimensions - MODERN API (FreeCAD 0.21+)
dim3 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, top_view_y_offset - 500, 0),
    FreeCAD.Vector(12000, top_view_y_offset - 500, 0)
)
dim3.ViewObject.FontSize = 300
dim4 = Draft.make_linear_dimension(
    FreeCAD.Vector(-500, top_view_y_offset, 0),
    FreeCAD.Vector(-500, top_view_y_offset + 8000, 0)
)
dim4.ViewObject.FontSize = 300
# === SIDE VIEW (y_offset = 16000) ===
# Profile projection showing depth
side_view_y_offset = 16000
side_profile = Draft.makeRectangle(12000, 6000, placement=FreeCAD.Placement(FreeCAD.Vector(0, side_view_y_offset, 0), FreeCAD.Rotation(0, 0, 0)))
side_profile.ViewObject.LineWidth = 1.5
# Dimensions - MODERN API (FreeCAD 0.21+)
dim5 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, side_view_y_offset - 500, 0),
    FreeCAD.Vector(12000, side_view_y_offset - 500, 0)
)
dim5.ViewObject.FontSize = 300
dim6 = Draft.make_linear_dimension(
    FreeCAD.Vector(-500, side_view_y_offset, 0),
    FreeCAD.Vector(-500, side_view_y_offset + 6000, 0)
)
dim6.ViewObject.FontSize = 300
# === GRID SYSTEM ===
# Grid lines every 1000mm with A,B,C labels
grid_spacing = 1000
for i in range(0, 13000, grid_spacing):
    grid_line = Draft.makeLine(
        FreeCAD.Vector(i, 0, 0),
        FreeCAD.Vector(i, 6000, 0)
    )
    grid_line.ViewObject.LineWidth = 0.5
    grid_line.ViewObject.LineStyle = "Dashed"
    grid_label = Draft.makeText(
        [chr(65 + i//grid_spacing)],
        point=FreeCAD.Vector(i, -500, 0)
    )
    grid_label.ViewObject.FontSize = 300
# === TITLE BLOCK ===
# Drawing name, scale, date
title_block = Draft.makeText(
    ["2BHK House", "Scale 1:100", "Date: 2024-09-16"],
    point=FreeCAD.Vector(10000, -1000, 0)
)
title_block.ViewObject.FontSize = 300
# Recompute the document
doc.recompute()
# Show the document
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.activeDocument().activeView().viewTop()
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
