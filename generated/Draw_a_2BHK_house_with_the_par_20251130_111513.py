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
# Parking gate
parking_gate = Draft.makeLine(FreeCAD.Vector(0, -1000, 0), FreeCAD.Vector(4000, -1000, 0))
parking_gate.ViewObject.LineWidth = 2.0
# Garden boundary
garden_boundary = Draft.makeWire([
    FreeCAD.Vector(4000, -1000, 0),
    FreeCAD.Vector(12000, -1000, 0),
    FreeCAD.Vector(12000, 0, 0),
    FreeCAD.Vector(4000, 0, 0),
    FreeCAD.Vector(4000, -1000, 0)
], closed=True)
garden_boundary.ViewObject.LineWidth = 1.5
# Dimensions - MODERN API (FreeCAD 0.21+)
dim1 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, -1500, 0),
    FreeCAD.Vector(12000, -1500, 0)
)
dim1.ViewObject.FontSize = 300
dim2 = Draft.make_linear_dimension(
    FreeCAD.Vector(-500, 0, 0),
    FreeCAD.Vector(-500, 6000, 0)
)
dim2.ViewObject.FontSize = 300
# === TOP VIEW (y_offset = 10000) ===
# Floor plan with rooms, furniture, fixtures
top_view_y_offset = 10000
# Living room
living_room = Draft.makeRectangle(4000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(2000, top_view_y_offset, 0), FreeCAD.Rotation(0, 0, 0)))
living_room.ViewObject.LineWidth = 1.5
# Kitchen
kitchen = Draft.makeRectangle(2000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(8000, top_view_y_offset, 0), FreeCAD.Rotation(0, 0, 0)))
kitchen.ViewObject.LineWidth = 1.5
# Bedroom 1
bedroom1 = Draft.makeRectangle(3000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(2000, top_view_y_offset + 4000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom1.ViewObject.LineWidth = 1.5
# Bedroom 2
bedroom2 = Draft.makeRectangle(3000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(6000, top_view_y_offset + 4000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom2.ViewObject.LineWidth = 1.5
# Bathroom
bathroom = Draft.makeRectangle(1500, 1500, placement=FreeCAD.Placement(FreeCAD.Vector(10000, top_view_y_offset + 5000, 0), FreeCAD.Rotation(0, 0, 0)))
bathroom.ViewObject.LineWidth = 1.5
# === SIDE VIEW (y_offset = 20000) ===
# Profile projection showing depth
side_view_y_offset = 20000
# Building profile
building_profile = Draft.makeWire([
    FreeCAD.Vector(0, side_view_y_offset, 0),
    FreeCAD.Vector(12000, side_view_y_offset, 0),
    FreeCAD.Vector(12000, side_view_y_offset + 6000, 0),
    FreeCAD.Vector(0, side_view_y_offset + 6000, 0),
    FreeCAD.Vector(0, side_view_y_offset, 0)
], closed=True)
building_profile.ViewObject.LineWidth = 1.5
# === GRID SYSTEM ===
# Grid lines every 1000mm with A,B,C labels
grid_spacing = 1000
# Vertical grid lines
for i in range(0, 14000, grid_spacing):
    grid_line = Draft.makeLine(
        FreeCAD.Vector(i, 0, 0),
        FreeCAD.Vector(i, 20000, 0)
    )
    grid_line.ViewObject.LineWidth = 0.5
    grid_line.ViewObject.LineStyle = "Dashed"
    # Grid label
    label = Draft.makeText(
        [chr(65 + i//grid_spacing)],  # A, B, C...
        point=FreeCAD.Vector(i, -500, 0)
    )
    label.ViewObject.TextColor = (1.0, 0.0, 0.0)
    label.ViewObject.FontSize = 300
# Horizontal grid lines
for i in range(0, 20000, grid_spacing):
    grid_line = Draft.makeLine(
        FreeCAD.Vector(0, i, 0),
        FreeCAD.Vector(14000, i, 0)
    )
    grid_line.ViewObject.LineWidth = 0.5
    grid_line.ViewObject.LineStyle = "Dashed"
    # Grid label
    label = Draft.makeText(
        [str(1 + i//grid_spacing)],  # 1, 2, 3...
        point=FreeCAD.Vector(-500, i, 0)
    )
    label.ViewObject.TextColor = (1.0, 0.0, 0.0)
    label.ViewObject.FontSize = 300
# === TITLE BLOCK ===
# Drawing name, scale, date
title_block = Draft.makeText(
    ["2BHK House Blueprint", "Scale: 1:100", "Date: 2024-09-16"],
    point=FreeCAD.Vector(10000, -1500, 0)
)
title_block.ViewObject.FontSize = 300
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.activeDocument().activeView().viewTop()
