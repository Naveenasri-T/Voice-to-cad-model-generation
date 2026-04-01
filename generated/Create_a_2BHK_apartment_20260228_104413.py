import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
import FreeCAD
import Draft
doc = FreeCAD.newDocument("2BHK_Apartment_Blueprint")
# === FRONT VIEW (y_offset = 0) ===
# Perimeter outline
front_outline = Draft.makeWire([
    FreeCAD.Vector(0, 0, 0),
    FreeCAD.Vector(8000, 0, 0),
    FreeCAD.Vector(8000, 6000, 0),
    FreeCAD.Vector(0, 6000, 0),
    FreeCAD.Vector(0, 0, 0)
], closed=True)
front_outline.ViewObject.LineWidth = 3.0
# Internal details (doors, windows, compartments)
door1 = Draft.makeLine(FreeCAD.Vector(1000, 0, 0), FreeCAD.Vector(1900, 0, 0))
door1.ViewObject.LineWidth = 2.0
window1 = Draft.makeRectangle(800, 1200, placement=FreeCAD.Placement(FreeCAD.Vector(3000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
window1.ViewObject.LineWidth = 1.5
window2 = Draft.makeRectangle(800, 1200, placement=FreeCAD.Placement(FreeCAD.Vector(5000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
window2.ViewObject.LineWidth = 1.5
# Dimensions - MODERN API (FreeCAD 0.21+)
dim1 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, -500, 0),
    FreeCAD.Vector(8000, -500, 0)
)
dim1.ViewObject.FontSize = 300
dim2 = Draft.make_linear_dimension(
    FreeCAD.Vector(-500, 0, 0),
    FreeCAD.Vector(-500, 6000, 0)
)
dim2.ViewObject.FontSize = 300
# Labels
label_door1 = Draft.makeText(["Main Door"], point=FreeCAD.Vector(1450, -200, 0))
label_door1.ViewObject.FontSize = 200
label_door1.ViewObject.TextColor = (0.0, 0.0, 0.0)
label_window1 = Draft.makeText(["Window 1"], point=FreeCAD.Vector(3200, 1400, 0))
label_window1.ViewObject.FontSize = 200
label_window1.ViewObject.TextColor = (0.0, 0.0, 0.0)
label_window2 = Draft.makeText(["Window 2"], point=FreeCAD.Vector(5200, 1400, 0))
label_window2.ViewObject.FontSize = 200
label_window2.ViewObject.TextColor = (0.0, 0.0, 0.0)
# === TOP VIEW (y_offset = 7000) ===
# Floor plan with rooms, furniture, fixtures
top_outline = Draft.makeWire([
    FreeCAD.Vector(0, 7000, 0),
    FreeCAD.Vector(8000, 7000, 0),
    FreeCAD.Vector(8000, 13000, 0),
    FreeCAD.Vector(0, 13000, 0),
    FreeCAD.Vector(0, 7000, 0)
], closed=True)
top_outline.ViewObject.LineWidth = 3.0
living_room = Draft.makeRectangle(4000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(1000, 8000, 0), FreeCAD.Rotation(0, 0, 0)))
living_room.ViewObject.LineWidth = 2.0
kitchen = Draft.makeRectangle(2000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(5000, 8000, 0), FreeCAD.Rotation(0, 0, 0)))
kitchen.ViewObject.LineWidth = 2.0
bedroom1 = Draft.makeRectangle(3000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(1000, 11000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom1.ViewObject.LineWidth = 2.0
bedroom2 = Draft.makeRectangle(3000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(5000, 11000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom2.ViewObject.LineWidth = 2.0
# Dimensions - MODERN API (FreeCAD 0.21+)
dim3 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 6500, 0),
    FreeCAD.Vector(8000, 6500, 0)
)
dim3.ViewObject.FontSize = 300
dim4 = Draft.make_linear_dimension(
    FreeCAD.Vector(-500, 7000, 0),
    FreeCAD.Vector(-500, 13000, 0)
)
dim4.ViewObject.FontSize = 300
# Labels
label_living_room = Draft.makeText(["Living Room"], point=FreeCAD.Vector(2000, 7500, 0))
label_living_room.ViewObject.FontSize = 200
label_living_room.ViewObject.TextColor = (0.0, 0.0, 0.0)
label_kitchen = Draft.makeText(["Kitchen"], point=FreeCAD.Vector(5500, 7500, 0))
label_kitchen.ViewObject.FontSize = 200
label_kitchen.ViewObject.TextColor = (0.0, 0.0, 0.0)
label_bedroom1 = Draft.makeText(["Bedroom 1"], point=FreeCAD.Vector(2000, 11500, 0))
label_bedroom1.ViewObject.FontSize = 200
label_bedroom1.ViewObject.TextColor = (0.0, 0.0, 0.0)
label_bedroom2 = Draft.makeText(["Bedroom 2"], point=FreeCAD.Vector(5500, 11500, 0))
label_bedroom2.ViewObject.FontSize = 200
label_bedroom2.ViewObject.TextColor = (0.0, 0.0, 0.0)
# === SIDE VIEW (y_offset = 14000) ===
# Profile projection showing depth
side_outline = Draft.makeWire([
    FreeCAD.Vector(0, 14000, 0),
    FreeCAD.Vector(8000, 14000, 0),
    FreeCAD.Vector(8000, 17000, 0),
    FreeCAD.Vector(0, 17000, 0),
    FreeCAD.Vector(0, 14000, 0)
], closed=True)
side_outline.ViewObject.LineWidth = 3.0
# Dimensions - MODERN API (FreeCAD 0.21+)
dim5 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 13500, 0),
    FreeCAD.Vector(8000, 13500, 0)
)
dim5.ViewObject.FontSize = 300
dim6 = Draft.make_linear_dimension(
    FreeCAD.Vector(-500, 14000, 0),
    FreeCAD.Vector(-500, 17000, 0)
)
dim6.ViewObject.FontSize = 300
# === GRID SYSTEM ===
# Grid lines every 1000mm with A,B,C labels
for i in range(0, 9000, 1000):
    grid_line = Draft.makeLine(FreeCAD.Vector(i, 0, 0), FreeCAD.Vector(i, 17000, 0))
    grid_line.ViewObject.LineWidth = 0.5
    try:
        grid_line.ViewObject.LineStyle = "Dashed"
    except AttributeError:
        pass  # LineStyle not supported on this object
    label = Draft.makeText([chr(65 + i//1000)], point=FreeCAD.Vector(i, -200, 0))
    label.ViewObject.FontSize = 200
    label.ViewObject.TextColor = (0.0, 0.0, 0.0)
# === TITLE BLOCK ===
# Drawing name, scale, date
title_block = Draft.makeText(["2BHK Apartment Blueprint", "Scale: 1:100", "Date: 2024-09-16"], point=FreeCAD.Vector(6000, -500, 0))
title_block.ViewObject.FontSize = 200
title_block.ViewObject.TextColor = (0.0, 0.0, 0.0)
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.activeDocument().activeView().viewTop()
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
