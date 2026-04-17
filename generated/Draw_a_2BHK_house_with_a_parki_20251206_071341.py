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
door1 = Draft.makeLine(FreeCAD.Vector(1000, 0, 0), FreeCAD.Vector(1900, 0, 0))
door1.ViewObject.LineWidth = 2.0
window1 = Draft.makeRectangle(800, 1200, placement=FreeCAD.Placement(FreeCAD.Vector(3000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
window1.ViewObject.LineWidth = 1.5
window2 = Draft.makeRectangle(800, 1200, placement=FreeCAD.Placement(FreeCAD.Vector(7000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
window2.ViewObject.LineWidth = 1.5
# Parking gate
parking_gate = Draft.makeLine(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 2000, 0))
parking_gate.ViewObject.LineWidth = 2.0
# Garden boundary
garden_boundary = Draft.makeWire([
    FreeCAD.Vector(12000, 0, 0),
    FreeCAD.Vector(15000, 0, 0),
    FreeCAD.Vector(15000, 3000, 0),
    FreeCAD.Vector(12000, 3000, 0),
    FreeCAD.Vector(12000, 0, 0)
], closed=True)
garden_boundary.ViewObject.LineWidth = 1.5
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
# Labels
label1 = Draft.makeText(["Front Elevation"], point=FreeCAD.Vector(0, -1000, 0))
label1.ViewObject.FontSize = 200
label2 = Draft.makeText(["Parking"], point=FreeCAD.Vector(-500, 1000, 0))
label2.ViewObject.FontSize = 150
label3 = Draft.makeText(["Garden"], point=FreeCAD.Vector(12500, 1500, 0))
label3.ViewObject.FontSize = 150
# === TOP VIEW (y_offset = 7000) ===
# Floor plan with rooms, furniture, fixtures
top_view_y_offset = 7000
living_room = Draft.makeRectangle(4000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(1000, top_view_y_offset, 0), FreeCAD.Rotation(0, 0, 0)))
living_room.ViewObject.LineWidth = 1.5
kitchen = Draft.makeRectangle(2000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(6000, top_view_y_offset, 0), FreeCAD.Rotation(0, 0, 0)))
kitchen.ViewObject.LineWidth = 1.5
bedroom1 = Draft.makeRectangle(3000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(1000, top_view_y_offset + 3000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom1.ViewObject.LineWidth = 1.5
bedroom2 = Draft.makeRectangle(3000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(6000, top_view_y_offset + 3000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom2.ViewObject.LineWidth = 1.5
bathroom = Draft.makeRectangle(1500, 1500, placement=FreeCAD.Placement(FreeCAD.Vector(4000, top_view_y_offset + 4500, 0), FreeCAD.Rotation(0, 0, 0)))
bathroom.ViewObject.LineWidth = 1.5
# Dimensions
dim3 = Draft.make_linear_dimension(
    FreeCAD.Vector(1000, top_view_y_offset - 500, 0),
    FreeCAD.Vector(5000, top_view_y_offset - 500, 0)
)
dim3.ViewObject.FontSize = 300
dim4 = Draft.make_linear_dimension(
    FreeCAD.Vector(1000, top_view_y_offset + 3000 - 500, 0),
    FreeCAD.Vector(5000, top_view_y_offset + 3000 - 500, 0)
)
dim4.ViewObject.FontSize = 300
# Labels
label4 = Draft.makeText(["Living Room"], point=FreeCAD.Vector(1500, top_view_y_offset + 1500, 0))
label4.ViewObject.FontSize = 150
label5 = Draft.makeText(["Kitchen"], point=FreeCAD.Vector(6500, top_view_y_offset + 1000, 0))
label5.ViewObject.FontSize = 150
label6 = Draft.makeText(["Bedroom 1"], point=FreeCAD.Vector(1500, top_view_y_offset + 4500, 0))
label6.ViewObject.FontSize = 150
label7 = Draft.makeText(["Bedroom 2"], point=FreeCAD.Vector(6500, top_view_y_offset + 4500, 0))
label7.ViewObject.FontSize = 150
label8 = Draft.makeText(["Bathroom"], point=FreeCAD.Vector(4250, top_view_y_offset + 5250, 0))
label8.ViewObject.FontSize = 150
# === SIDE VIEW (y_offset = 14000) ===
# Profile projection showing depth
side_view_y_offset = 14000
side_outline = Draft.makeWire([
    FreeCAD.Vector(0, side_view_y_offset, 0),
    FreeCAD.Vector(12000, side_view_y_offset, 0),
    FreeCAD.Vector(12000, side_view_y_offset + 6000, 0),
    FreeCAD.Vector(0, side_view_y_offset + 6000, 0),
    FreeCAD.Vector(0, side_view_y_offset, 0)
], closed=True)
side_outline.ViewObject.LineWidth = 3.0
# Dimensions
dim5 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, side_view_y_offset - 500, 0),
    FreeCAD.Vector(0, side_view_y_offset + 6000 - 500, 0)
)
dim5.ViewObject.FontSize = 300
# Labels
label9 = Draft.makeText(["Side Elevation"], point=FreeCAD.Vector(0, side_view_y_offset - 1000, 0))
label9.ViewObject.FontSize = 200
# === GRID SYSTEM ===
# Grid lines every 1000mm with A,B,C labels
grid_spacing = 1000
for i in range(0, 15000, grid_spacing):
    grid_line = Draft.makeLine(FreeCAD.Vector(i, 0, 0), FreeCAD.Vector(i, 7000, 0))
    grid_line.ViewObject.LineWidth = 0.5
    grid_line.ViewObject.LineStyle = "Dashed"
    label = Draft.makeText([chr(65 + i//grid_spacing)], point=FreeCAD.Vector(i, -500, 0))
    label.ViewObject.FontSize = 150
# === TITLE BLOCK ===
# Drawing name, scale, date
title_block = Draft.makeText(["2BHK House Blueprint", "Scale: 1:100", "Date: 2024-09-16"], point=FreeCAD.Vector(0, -1500, 0))
title_block.ViewObject.FontSize = 150
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.activeDocument().activeView().viewTop()
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
