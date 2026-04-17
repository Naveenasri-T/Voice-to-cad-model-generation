import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
import Draft
doc = FreeCAD.newDocument("2BHK_House_Blueprint")
# === FRONT VIEW (y_offset = 0) ===
front_y_offset = 0
# Perimeter outline
front_outline = Draft.makeWire([
    FreeCAD.Vector(0, front_y_offset, 0),
    FreeCAD.Vector(12000, front_y_offset, 0),
    FreeCAD.Vector(12000, front_y_offset + 6000, 0),
    FreeCAD.Vector(0, front_y_offset + 6000, 0),
    FreeCAD.Vector(0, front_y_offset, 0)
], closed=True)
front_outline.ViewObject.LineWidth = 3.0
# Internal details (doors, windows, compartments)
door1 = Draft.makeLine(FreeCAD.Vector(1000, front_y_offset, 0), FreeCAD.Vector(1900, front_y_offset, 0))
door1.ViewObject.LineWidth = 2.0
window1 = Draft.makeRectangle(800, 1200, placement=FreeCAD.Placement(FreeCAD.Vector(3000, front_y_offset + 1000, 0), FreeCAD.Rotation(0, 0, 0)))
window1.ViewObject.LineWidth = 1.5
window2 = Draft.makeRectangle(800, 1200, placement=FreeCAD.Placement(FreeCAD.Vector(9000, front_y_offset + 1000, 0), FreeCAD.Rotation(0, 0, 0)))
window2.ViewObject.LineWidth = 1.5
# Dimensions - MODERN API (FreeCAD 0.21+)
dim1 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, front_y_offset - 500, 0),
    FreeCAD.Vector(12000, front_y_offset - 500, 0)
)
dim1.ViewObject.FontSize = 300
dim2 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, front_y_offset - 500, 0),
    FreeCAD.Vector(0, front_y_offset + 6000 - 500, 0)
)
dim2.ViewObject.FontSize = 300
# Labels
label_door = Draft.makeText(["Main Door"], point=FreeCAD.Vector(1450, front_y_offset - 500, 0))
label_door.ViewObject.FontSize = 200
label_window1 = Draft.makeText(["Window 1"], point=FreeCAD.Vector(3500, front_y_offset + 1300, 0))
label_window1.ViewObject.FontSize = 200
label_window2 = Draft.makeText(["Window 2"], point=FreeCAD.Vector(9500, front_y_offset + 1300, 0))
label_window2.ViewObject.FontSize = 200
# === TOP VIEW (y_offset = 10000) ===
top_y_offset = 10000
# Floor plan with rooms, furniture, fixtures
living_room = Draft.makeRectangle(4000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(2000, top_y_offset, 0), FreeCAD.Rotation(0, 0, 0)))
living_room.ViewObject.LineWidth = 2.0
kitchen = Draft.makeRectangle(2000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(8000, top_y_offset, 0), FreeCAD.Rotation(0, 0, 0)))
kitchen.ViewObject.LineWidth = 2.0
bedroom1 = Draft.makeRectangle(3000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(2000, top_y_offset + 4000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom1.ViewObject.LineWidth = 2.0
bedroom2 = Draft.makeRectangle(3000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(6000, top_y_offset + 4000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom2.ViewObject.LineWidth = 2.0
# Dimensions
dim3 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, top_y_offset - 500, 0),
    FreeCAD.Vector(12000, top_y_offset - 500, 0)
)
dim3.ViewObject.FontSize = 300
dim4 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, top_y_offset - 500, 0),
    FreeCAD.Vector(0, top_y_offset + 8000 - 500, 0)
)
dim4.ViewObject.FontSize = 300
# Labels
label_living_room = Draft.makeText(["Living Room"], point=FreeCAD.Vector(4000, top_y_offset + 1500, 0))
label_living_room.ViewObject.FontSize = 200
label_kitchen = Draft.makeText(["Kitchen"], point=FreeCAD.Vector(9000, top_y_offset + 1000, 0))
label_kitchen.ViewObject.FontSize = 200
label_bedroom1 = Draft.makeText(["Bedroom 1"], point=FreeCAD.Vector(3500, top_y_offset + 5500, 0))
label_bedroom1.ViewObject.FontSize = 200
label_bedroom2 = Draft.makeText(["Bedroom 2"], point=FreeCAD.Vector(7500, top_y_offset + 5500, 0))
label_bedroom2.ViewObject.FontSize = 200
# === SIDE VIEW (y_offset = 20000) ===
side_y_offset = 20000
# Profile projection showing depth
profile = Draft.makeRectangle(12000, 6000, placement=FreeCAD.Placement(FreeCAD.Vector(0, side_y_offset, 0), FreeCAD.Rotation(0, 0, 0)))
profile.ViewObject.LineWidth = 3.0
# Dimensions
dim5 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, side_y_offset - 500, 0),
    FreeCAD.Vector(12000, side_y_offset - 500, 0)
)
dim5.ViewObject.FontSize = 300
dim6 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, side_y_offset - 500, 0),
    FreeCAD.Vector(0, side_y_offset + 6000 - 500, 0)
)
dim6.ViewObject.FontSize = 300
# Labels
label_profile = Draft.makeText(["Side Profile"], point=FreeCAD.Vector(6000, side_y_offset + 3000, 0))
label_profile.ViewObject.FontSize = 200
# === GRID SYSTEM ===
grid_spacing = 1000
for i in range(0, 13000, grid_spacing):
    grid_line = Draft.makeLine(
        FreeCAD.Vector(i, front_y_offset - 2000, 0),
        FreeCAD.Vector(i, front_y_offset + 8000, 0)
    )
    grid_line.ViewObject
    grid_line.ViewObject.LineWidth = 0.5
    try:
        try:
            grid_line.ViewObject.LineStyle = "Dashed"
        except AttributeError:
            pass  # LineStyle not supported
    except AttributeError:
        pass  # LineStyle not supported on this object
    grid_label = Draft.makeText([chr(65 + i//grid_spacing)], point=FreeCAD.Vector(i, front_y_offset - 2500, 0))
    grid_label.ViewObject.FontSize = 200
    grid_label.ViewObject.TextColor = (1.0, 0.0, 0.0)
# === TITLE BLOCK ===
title_block = Draft.makeText(
    ["2BHK House Blueprint", "Scale: 1:100", "Date: 2024-09-16"],
    point=FreeCAD.Vector(10000, front_y_offset + 6500, 0)
)
title_block.ViewObject.FontSize = 200
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.activeDocument().activeView().viewTop()
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
