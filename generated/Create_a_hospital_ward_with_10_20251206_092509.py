import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
import FreeCAD
import Draft
# Create new document
doc = FreeCAD.newDocument("Hospital_Ward_Blueprint")
# === FRONT VIEW (y_offset = 0) ===
# Perimeter outline
front_outline = Draft.makeWire([
    FreeCAD.Vector(0, 0, 0),
    FreeCAD.Vector(12000, 0, 0),
    FreeCAD.Vector(12000, 3000, 0),
    FreeCAD.Vector(0, 3000, 0),
    FreeCAD.Vector(0, 0, 0)
], closed=True)
front_outline.ViewObject.LineWidth = 3.0
# Internal details (doors, windows, compartments)
door1 = Draft.makeLine(FreeCAD.Vector(1000, 0, 0), FreeCAD.Vector(1900, 0, 0))
door1.ViewObject.LineWidth = 2.0
window1 = Draft.makeRectangle(800, 1200, placement=FreeCAD.Placement(FreeCAD.Vector(3000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
window1.ViewObject.LineWidth = 1.5
# Nurse station
nurse_station = Draft.makeRectangle(2000, 1000, placement=FreeCAD.Placement(FreeCAD.Vector(4000, 500, 0), FreeCAD.Rotation(0, 0, 0)))
nurse_station.ViewObject.LineWidth = 2.0
# Doctor's room
doctor_room = Draft.makeRectangle(1500, 1000, placement=FreeCAD.Placement(FreeCAD.Vector(7000, 500, 0), FreeCAD.Rotation(0, 0, 0)))
doctor_room.ViewObject.LineWidth = 2.0
# Utility space
utility_space = Draft.makeRectangle(1000, 1000, placement=FreeCAD.Placement(FreeCAD.Vector(10000, 500, 0), FreeCAD.Rotation(0, 0, 0)))
utility_space.ViewObject.LineWidth = 2.0
# Dimensions - MODERN API (FreeCAD 0.21+)
dim1 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, -500, 0),
    FreeCAD.Vector(12000, -500, 0)
)
dim1.ViewObject.FontSize = 300
dim2 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 0, 0),
    FreeCAD.Vector(0, 3000, 0)
)
dim2.ViewObject.FontSize = 300
# === TOP VIEW (y_offset = 10000) ===
# Floor plan with rooms, furniture, fixtures
top_outline = Draft.makeWire([
    FreeCAD.Vector(0, 10000, 0),
    FreeCAD.Vector(12000, 10000, 0),
    FreeCAD.Vector(12000, 13000, 0),
    FreeCAD.Vector(0, 13000, 0),
    FreeCAD.Vector(0, 10000, 0)
], closed=True)
top_outline.ViewObject.LineWidth = 3.0
# Patient beds
bed1 = Draft.makeRectangle(1000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(1000, 11000, 0), FreeCAD.Rotation(0, 0, 0)))
bed1.ViewObject.LineWidth = 1.5
bed2 = Draft.makeRectangle(1000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(3000, 11000, 0), FreeCAD.Rotation(0, 0, 0)))
bed2.ViewObject.LineWidth = 1.5
bed3 = Draft.makeRectangle(1000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(5000, 11000, 0), FreeCAD.Rotation(0, 0, 0)))
bed3.ViewObject.LineWidth = 1.5
bed4 = Draft.makeRectangle(1000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(7000, 11000, 0), FreeCAD.Rotation(0, 0, 0)))
bed4.ViewObject.LineWidth = 1.5
bed5 = Draft.makeRectangle(1000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(9000, 11000, 0), FreeCAD.Rotation(0, 0, 0)))
bed5.ViewObject.LineWidth = 1.5
bed6 = Draft.makeRectangle(1000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(1000, 12000, 0), FreeCAD.Rotation(0, 0, 0)))
bed6.ViewObject.LineWidth = 1.5
bed7 = Draft.makeRectangle(1000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(3000, 12000, 0), FreeCAD.Rotation(0, 0, 0)))
bed7.ViewObject.LineWidth = 1.5
bed8 = Draft.makeRectangle(1000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(5000, 12000, 0), FreeCAD.Rotation(0, 0, 0)))
bed8.ViewObject.LineWidth = 1.5
bed9 = Draft.makeRectangle(1000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(7000, 12000, 0), FreeCAD.Rotation(0, 0, 0)))
bed9.ViewObject.LineWidth = 1.5
bed10 = Draft.makeRectangle(1000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(9000, 12000, 0), FreeCAD.Rotation(0, 0, 0)))
bed10.ViewObject.LineWidth = 1.5
# Shared bathrooms
bathroom1 = Draft.makeRectangle(1000, 1000, placement=FreeCAD.Placement(FreeCAD.Vector(4000, 11000, 0), FreeCAD.Rotation(0, 0, 0)))
bathroom1.ViewObject.LineWidth = 2.0
bathroom2 = Draft.makeRectangle(1000, 1000, placement=FreeCAD.Placement(FreeCAD.Vector(4000, 12000, 0), FreeCAD.Rotation(0, 0, 0)))
bathroom2.ViewObject.LineWidth = 2.0
# Dimensions - MODERN API (FreeCAD 0.21+)
dim3 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 10000, 0),
    FreeCAD.Vector(12000, 10000, 0)
)
dim3.ViewObject.FontSize = 300
dim4 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 10000, 0),
    FreeCAD.Vector(0, 13000, 0)
)
dim4.ViewObject.FontSize = 300
# === SIDE VIEW (y_offset = 20000) ===
# Profile projection showing depth
side_outline = Draft.makeWire([
    FreeCAD.Vector(0, 20000, 0),
    FreeCAD.Vector(12000, 20000, 0),
    FreeCAD.Vector(12000, 23000, 0),
    FreeCAD.Vector(0, 23000, 0),
    FreeCAD.Vector(0, 20000, 0)
], closed=True)
side_outline.ViewObject.LineWidth = 3.0
# Dimensions - MODERN API (FreeCAD 0.21+)
dim5 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 20000, 0),
    FreeCAD.Vector(12000, 20000, 0)
)
dim5.ViewObject.FontSize = 300
dim6 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 20000, 0),
    FreeCAD.Vector(0, 23000, 0)
)
dim6.ViewObject.FontSize = 300
# === GRID SYSTEM ===
# Grid lines every 1000mm with A,B,C labels
grid_spacing = 1000
for i in range(0, 13000, grid_spacing):
    grid_line = Draft.makeLine(FreeCAD.Vector(0, i, 0), FreeCAD.Vector(12000, i, 0))
    grid_line.ViewObject.LineWidth = 0.5
    try:
        grid_line.ViewObject.LineStyle = "Dashed"
    except AttributeError:
        pass  # LineStyle not supported on this object
for i in range(0, 12000, grid_spacing):
    grid_line = Draft.makeLine(FreeCAD.Vector(i, 0, 0), FreeCAD.Vector(i, 13000, 0))
    grid_line.ViewObject.LineWidth = 0.5
    try:
        grid_line.ViewObject.LineStyle = "Dashed"
    except AttributeError:
        pass  # LineStyle not supported on this object
# === TITLE BLOCK ===
# Drawing name, scale, date
title_block = Draft.makeText(
    ["Hospital Ward Blueprint", "Scale: 1:100", "Date: 2024-09-16"],
    point=FreeCAD.Vector(10000, 25000, 0)
)
title_block.ViewObject.FontSize = 300
# === LABELS ===
# Labels for rooms, furniture, fixtures
label1 = Draft.makeText(
    ["Nurse Station"],
    point=FreeCAD.Vector(4500, 500, 0)
)
label1.ViewObject.FontSize = 200
label2 = Draft.makeText(
    ["Doctor's Room"],
    point=FreeCAD.Vector(8000, 500, 0)
)
label2.ViewObject.FontSize = 200
label3 = Draft.makeText(
    ["Utility Space"],
    point=FreeCAD.Vector(11000, 500, 0)
)
label3.ViewObject.FontSize = 200
label4 = Draft.makeText(
    ["Patient Bed 1"],
    point=FreeCAD.Vector(1500, 11000, 0)
)
label4.ViewObject.FontSize = 200
label5 = Draft.makeText(
    ["Patient Bed 2"],
    point=FreeCAD.Vector(3500, 11000, 0)
)
label5.ViewObject.FontSize = 200
label6 = Draft.makeText(
    ["Shared Bathroom"],
    point=FreeCAD.Vector(4500, 11000, 0)
)
label6.ViewObject.FontSize = 200
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.activeDocument().activeView().viewTop()
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
