import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
import FreeCAD
import Draft
doc = FreeCAD.newDocument("Mechanical_Gear_Blueprint")
# === FRONT VIEW (y_offset = 0) ===
# Perimeter outline
front_outline = Draft.makeWire([
    FreeCAD.Vector(0, 0, 0),
    FreeCAD.Vector(5000, 0, 0),
    FreeCAD.Vector(5000, 5000, 0),
    FreeCAD.Vector(0, 5000, 0),
    FreeCAD.Vector(0, 0, 0)
], closed=True)
front_outline.ViewObject.LineWidth = 3.0
# Internal details (gear teeth)
gear_tooth1 = Draft.makeLine(FreeCAD.Vector(1000, 0, 0), FreeCAD.Vector(1000, 500, 0))
gear_tooth1.ViewObject.LineWidth = 2.0
gear_tooth2 = Draft.makeLine(FreeCAD.Vector(2000, 0, 0), FreeCAD.Vector(2000, 500, 0))
gear_tooth2.ViewObject.LineWidth = 2.0
gear_tooth3 = Draft.makeLine(FreeCAD.Vector(3000, 0, 0), FreeCAD.Vector(3000, 500, 0))
gear_tooth3.ViewObject.LineWidth = 2.0
gear_tooth4 = Draft.makeLine(FreeCAD.Vector(4000, 0, 0), FreeCAD.Vector(4000, 500, 0))
gear_tooth4.ViewObject.LineWidth = 2.0
# Center hole
center_hole = Draft.makeCircle(500, placement=FreeCAD.Placement(FreeCAD.Vector(2500, 2500, 0), FreeCAD.Rotation(0, 0, 0)))
center_hole.ViewObject.LineWidth = 1.5
# Dimensions - MODERN API (FreeCAD 0.21+)
dim1 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, -500, 0),
    FreeCAD.Vector(5000, -500, 0)
)
dim1.ViewObjectdim1.ViewObject.FontSize = 300
dim2 = Draft.make_linear_dimension(
    FreeCAD.Vector(-500, 0, 0),
    FreeCAD.Vector(-500, 5000, 0)
)
dim2.ViewObjectdim2.ViewObject.FontSize = 300
# Labels
label_gear = Draft.makeText(["Mechanical Gear"], point=FreeCAD.Vector(0, 5500, 0))
label_gear.ViewObject.FontSize = 400
label_tooth = Draft.makeText(["Gear Tooth"], point=FreeCAD.Vector(1000, 600, 0))
label_tooth.ViewObject.FontSize = 200
label_center = Draft.makeText(["Center Hole"], point=FreeCAD.Vector(2500, 3000, 0))
label_center.ViewObject.FontSize = 200
# === TOP VIEW (y_offset = 10000) ===
# Floor plan with rooms, furniture, fixtures
top_outline = Draft.makeWire([
    FreeCAD.Vector(0, 10000, 0),
    FreeCAD.Vector(5000, 10000, 0),
    FreeCAD.Vector(5000, 15000, 0),
    FreeCAD.Vector(0, 15000, 0),
    FreeCAD.Vector(0, 10000, 0)
], closed=True)
top_outline.ViewObject.LineWidth = 3.0
gear_tooth5 = Draft.makeLine(FreeCAD.Vector(1000, 10000, 0), FreeCAD.Vector(1000, 10500, 0))
gear_tooth5.ViewObject.LineWidth = 2.0
gear_tooth6 = Draft.makeLine(FreeCAD.Vector(2000, 10000, 0), FreeCAD.Vector(2000, 10500, 0))
gear_tooth6.ViewObject.LineWidth = 2.0
gear_tooth7 = Draft.makeLine(FreeCAD.Vector(3000, 10000, 0), FreeCAD.Vector(3000, 10500, 0))
gear_tooth7.ViewObject.LineWidth = 2.0
gear_tooth8 = Draft.makeLine(FreeCAD.Vector(4000, 10000, 0), FreeCAD.Vector(4000, 10500, 0))
gear_tooth8.ViewObject.LineWidth = 2.0
center_hole2 = Draft.makeCircle(500, placement=FreeCAD.Placement(FreeCAD.Vector(2500, 12500, 0), FreeCAD.Rotation(0, 0, 0)))
center_hole2.ViewObject.LineWidth = 1.5
dim3 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 9500, 0),
    FreeCAD.Vector(5000, 9500, 0)
)
dim3.ViewObjectdim3.ViewObject.FontSize = 300
dim4 = Draft.make_linear_dimension(
    FreeCAD.Vector(-500, 10000, 0),
    FreeCAD.Vector(-500, 15000, 0)
)
dim4.ViewObjectdim4.ViewObject.FontSize = 300
label_gear2 = Draft.makeText(["Mechanical Gear"], point=FreeCAD.Vector(0, 15500, 0))
label_gear2.ViewObject.FontSize = 400
label_tooth2 = Draft.makeText(["Gear Tooth"], point=FreeCAD.Vector(1000, 10600, 0))
label_tooth2.ViewObject.FontSize = 200
label_center2 = Draft.makeText(["Center Hole"], point=FreeCAD.Vector(2500, 13000, 0))
label_center2.ViewObject.FontSize = 200
# === SIDE VIEW (y_offset = 20000) ===
# Profile projection showing depth
side_outline = Draft.makeWire([
    FreeCAD.Vector(0, 20000, 0),
    FreeCAD.Vector(5000, 20000, 0),
    FreeCAD.Vector(5000, 25000, 0),
    FreeCAD.Vector(0, 25000, 0),
    FreeCAD.Vector(0, 20000, 0)
], closed=True)
side_outline.ViewObject.LineWidth = 3.0
gear_tooth9 = Draft.makeLine(FreeCAD.Vector(1000, 20000, 0), FreeCAD.Vector(1000, 20500, 0))
gear_tooth9.ViewObject.LineWidth = 2.0
gear_tooth10 = Draft.makeLine(FreeCAD.Vector(2000, 20000, 0), FreeCAD.Vector(2000, 20500, 0))
gear_tooth10.ViewObject.LineWidth = 2.0
gear_tooth11 = Draft.makeLine(FreeCAD.Vector(3000, 20000, 0), FreeCAD.Vector(3000, 20500, 0))
gear_tooth11.ViewObject.LineWidth = 2.0
gear_tooth12 = Draft.makeLine(FreeCAD.Vector(4000, 20000, 0), FreeCAD.Vector(4000, 20500, 0))
gear_tooth12.ViewObject.LineWidth = 2.0
center_hole3 = Draft.makeCircle(500, placement=FreeCAD.Placement(FreeCAD.Vector(2500, 22500, 0), FreeCAD.Rotation(0, 0, 0)))
center_hole3.ViewObject.LineWidth = 1.5
dim5 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 19500, 0),
    FreeCAD.Vector(5000, 19500, 0)
)
dim5.ViewObjectdim5.ViewObject.FontSize = 300
dim6 = Draft.make_linear_dimension(
    FreeCAD.Vector(-500, 20000, 0),
    FreeCAD.Vector(-500, 25000, 0)
)
dim6.ViewObjectdim6.ViewObject.FontSize = 300
label_gear3 = Draft.makeText(["Mechanical Gear"], point=FreeCAD.Vector(0, 25500, 0))
label_gear3.ViewObject.FontSize = 400
label_tooth3 = Draft.makeText(["Gear Tooth"], point=FreeCAD.Vector(1000, 20600, 0))
label_tooth3.ViewObject.FontSize = 200
label_center3 = Draft.makeText(["Center Hole"], point=FreeCAD.Vector(2500, 23000, 0))
label_center3.ViewObject.FontSize = 200
# === GRID SYSTEM ===
# Grid lines every 1000mm with A,B,C labels
grid_spacing = 1000
for i in range(0, 6000, grid_spacing):
    grid_line = Draft.makeLine(
        FreeCAD.Vector(i, -500, 0),
        FreeCAD.Vector(i, 26000, 0)
    )
    grid_line.ViewObject    grid_line.ViewObject.LineWidth = 0.5
    grid_line.ViewObject.LineStyle = "Dashed"
    label = Draft.makeText(
        [chr(65 + i//grid_spacing)],  # A, B, C...
        point=FreeCAD.Vector(i, -1000, 0)
    )
    label.ViewObject.FontSize = 300
# === TITLE BLOCK ===
# Drawing name, scale, date
title_block = Draft.makeText(
    ["Mechanical Gear Blueprint", "Scale: 1:2", "Date: 2024-09-16"],
    point=FreeCAD.Vector(0, 26500, 0)
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
