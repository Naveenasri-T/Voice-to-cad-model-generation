import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
import FreeCAD
import Draft
doc = FreeCAD.newDocument("BeachHouseBlueprint")
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
# Labels
label_door = Draft.makeText(["Door"], point=FreeCAD.Vector(2500, -500, 0))
label_door.ViewObject.FontSize = 200
label_window = Draft.makeText(["Window"], point=FreeCAD.Vector(4500, 1500, 0))
label_window.ViewObject.FontSize = 200
# === TOP VIEW (y_offset = 10000) ===
# Floor plan with rooms, furniture, fixtures
top_outline = Draft.makeWire([
    FreeCAD.Vector(0, 10000, 0),
    FreeCAD.Vector(12000, 10000, 0),
    FreeCAD.Vector(12000, 16000, 0),
    FreeCAD.Vector(0, 16000, 0),
    FreeCAD.Vector(0, 10000, 0)
], closed=True)
top_outline.ViewObject.LineWidth = 3.0
room1 = Draft.makeRectangle(4000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(2000, 11000, 0), FreeCAD.Rotation(0, 0, 0)))
room1.ViewObject.LineWidth = 2.0
room2 = Draft.makeRectangle(4000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(6000, 11000, 0), FreeCAD.Rotation(0, 0, 0)))
room2.ViewObject.LineWidth = 2.0
parking = Draft.makeRectangle(4000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(0, 13000, 0), FreeCAD.Rotation(0, 0, 0)))
parking.ViewObject.LineWidth = 2.0
garden = Draft.makeRectangle(8000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(2000, 14000, 0), FreeCAD.Rotation(0, 0, 0)))
garden.ViewObject.LineWidth = 2.0
# Dimensions
dim3 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 10000, 0),
    FreeCAD.Vector(12000, 10000, 0)
)
dim3.ViewObject.FontSize = 300
dim4 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 10000, 0),
    FreeCAD.Vector(0, 16000, 0)
)
dim4.ViewObject.FontSize = 300
# Labels
label_room1 = Draft.makeText(["Room 1"], point=FreeCAD.Vector(3000, 10500, 0))
label_room1.ViewObject.FontSize = 200
label_room2 = Draft.makeText(["Room 2"], point=FreeCAD.Vector(7000, 10500, 0))
label_room2.ViewObject.FontSize = 200
label_parking = Draft.makeText(["Parking"], point=FreeCAD.Vector(2000, 13500, 0))
label_parking.ViewObject.FontSize = 200
label_garden = Draft.makeText(["Garden"], point=FreeCAD.Vector(6000, 14500, 0))
label_garden.ViewObject.FontSize = 200
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
# Dimensions
dim5 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 20000, 0),
    FreeCAD.Vector(12000, 20000, 0)
)
dim5.ViewObject.FontSize = 300
dim6 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 20000, 0),
    FreeCAD.Vector(0, 26000, 0)
)
dim6.ViewObject.FontSize = 300
# === GRID SYSTEM ===
# Grid lines every 1000mm with A,B,C labels
for i in range(0, 13000, 1000):
    grid_line = Draft.makeLine(FreeCAD.Vector(i, 0, 0), FreeCAD.Vector(i, 26000, 0))
    grid_line.ViewObject.LineWidth = 0.5
    try:
        grid_line.ViewObject.LineStyle = "Dashed"
    except AttributeError:
        pass  # LineStyle not supported on this object
    label = Draft.makeText([chr(65 + i//1000)], point=FreeCAD.Vector(i, -500, 0))
    label.ViewObject.FontSize = 200
for i in range(0, 26000, 1000):
    grid_line = Draft.makeLine(FreeCAD.Vector(0, i, 0), FreeCAD.Vector(12000, i, 0))
    grid_line.ViewObject.LineWidth = 0.5
    try:
        grid_line.ViewObject.LineStyle = "Dashed"
    except AttributeError:
        pass  # LineStyle not supported on this object
    label = Draft.makeText([str(i//1000)], point=FreeCAD.Vector(-500, i, 0))
    label.ViewObject.FontSize = 200
# === TITLE BLOCK ===
# Drawing name, scale, date
title_block = Draft.makeText(["Beach House Blueprint", "Scale: 1:100", "Date: 2024-09-16"], point=FreeCAD.Vector(10000, 27000, 0))
title_block.ViewObject.FontSize = 200
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.activeDocument().activeView().viewTop()
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
