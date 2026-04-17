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
window2 = Draft.makeRectangle(800, 1200, placement=FreeCAD.Placement(FreeCAD.Vector(9000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
window2.ViewObject.LineWidth = 1.5
# Parking gate
parking_gate = Draft.makeLine(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 2000, 0))
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
# === TOP VIEW (y_offset = 10000) ===
# Floor plan with rooms, furniture, fixtures
living_room = Draft.makeRectangle(4000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(2000, 10000, 0), FreeCAD.Rotation(0, 0, 0)))
living_room.ViewObject.LineWidth = 1.5
kitchen = Draft.makeRectangle(2000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(8000, 10000, 0), FreeCAD.Rotation(0, 0, 0)))
kitchen.ViewObject.LineWidth = 1.5
bedroom1 = Draft.makeRectangle(3000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(2000, 14000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom1.ViewObject.LineWidth = 1.5
bedroom2 = Draft.makeRectangle(3000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(8000, 14000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom2.ViewObject.LineWidth = 1.5
# Bathroom
bathroom = Draft.makeRectangle(1500, 1500, placement=FreeCAD.Placement(FreeCAD.Vector(5000, 16000, 0), FreeCAD.Rotation(0, 0, 0)))
bathroom.ViewObject.LineWidth = 1.5
# Garden
garden = Draft.makeRectangle(4000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(6000, 10000, 0), FreeCAD.Rotation(0, 0, 0)))
garden.ViewObject.LineWidth = 1.5
# Dimensions
dim3 = Draft.make_linear_dimension(
    FreeCAD.Vector(2000, 9500, 0),
    FreeCAD.Vector(6000, 9500, 0)
)
dim3.ViewObject.FontSize = 300
dim4 = Draft.make_linear_dimension(
    FreeCAD.Vector(2000, 13950, 0),
    FreeCAD.Vector(5000, 13950, 0)
)
dim4.ViewObject.FontSize = 300
# === SIDE VIEW (y_offset = 20000) ===
# Profile projection showing depth
side_profile = Draft.makeRectangle(12000, 6000, placement=FreeCAD.Placement(FreeCAD.Vector(0, 20000, 0), FreeCAD.Rotation(0, 0, 0)))
side_profile.ViewObject.LineWidth = 3.0
# Roof
roof = Draft.makeLine(FreeCAD.Vector(0, 26000, 0), FreeCAD.Vector(12000, 26000, 0))
roof.ViewObject.LineWidth = 2.0
# Dimensions
dim5 = Draft.make_linear_dimension(
    FreeCAD.Vector(-500, 20000, 0),
    FreeCAD.Vector(-500, 26000, 0)
)
dim5.ViewObject.FontSize = 300
# === GRID SYSTEM ===
# Grid lines every 1000mm with A,B,C labels
grid_spacing = 1000
for i in range(0, 13000, grid_spacing):
    grid_line = Draft.makeLine(
        FreeCAD.Vector(i, 0, 0),
        FreeCAD.Vector(i, 6000, 0)
    )
    grid_line.ViewObject
    grid_line.ViewObject.LineWidth = 0.5
    try:
        grid_line.ViewObject.LineStyle = "Dashed"
    except AttributeError:
        pass  # LineStyle not supported on this object
    label = Draft.makeText(
        [chr(65 + i//grid_spacing)],
        point=FreeCAD.Vector(i, -500, 0)
    )
    label.ViewObject.FontSize = 300
# === TITLE BLOCK ===
# Drawing name, scale, date
title_block = Draft.makeText(
    ["2BHK House Blueprint", "Scale 1:100", "Date: 2024-09-16"],
    point=FreeCAD.Vector(10000, -1000, 0)
)
title_block.ViewObject.FontSize = 300
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.activeDocument().activeView().viewTop()
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
