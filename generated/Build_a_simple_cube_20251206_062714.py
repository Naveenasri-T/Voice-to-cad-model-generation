import FreeCAD
import Draft
# TEMPLATE_GENERATED
doc = FreeCAD.newDocument("College_Computer_Lab")
# === FLOOR PLAN - College Computer Lab ===
print("Generating: College Computer Lab")
print("Total Area: 180 sqm")
# Exterior perimeter
exterior = Draft.makeWire([
    FreeCAD.Vector(0, 0, 0),
    FreeCAD.Vector(18000, 0, 0),
    FreeCAD.Vector(18000, 12000, 0),
    FreeCAD.Vector(0, 12000, 0),
    FreeCAD.Vector(0, 0, 0)
], closed=True)
exterior.ViewObject.LineWidth = 4.0
exterior.ViewObject
# Room Definitions
# Main Lab Area (140 sqm)
room_0 = Draft.makeRectangle(14000, 10000, placement=FreeCAD.Placement(FreeCAD.Vector(1000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
room_0.ViewObject.LineWidth = 1.5
room_0.ViewObject
label_0 = Draft.make_text(["Main Lab Area", "140 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(5666, 6000, 0), FreeCAD.Rotation(0, 0, 0)))
label_0.ViewObject.FontSize = 180
# Server Room (9 sqm)
room_1 = Draft.makeRectangle(3000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(15500, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
room_1.ViewObject.LineWidth = 1.5
room_1.ViewObject
label_1 = Draft.make_text(["Server Room", "9 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(16500, 2500, 0), FreeCAD.Rotation(0, 0, 0)))
label_1.ViewObject.FontSize = 180
# Instructor Area (8 sqm)
room_2 = Draft.makeRectangle(4000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(1000, 11500, 0), FreeCAD.Rotation(0, 0, 0)))
room_2.ViewObject.LineWidth = 1.5
room_2.ViewObject
label_2 = Draft.make_text(["Instructor Area", "8 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(2333, 12500, 0), FreeCAD.Rotation(0, 0, 0)))
label_2.ViewObject.FontSize = 180
# Storage (6 sqm)
room_3 = Draft.makeRectangle(3000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(6000, 11500, 0), FreeCAD.Rotation(0, 0, 0)))
room_3.ViewObject.LineWidth = 1.5
room_3.ViewObject
label_3 = Draft.make_text(["Storage", "6 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(7000, 12500, 0), FreeCAD.Rotation(0, 0, 0)))
label_3.ViewObject.FontSize = 180
# Restroom (4 sqm)
room_4 = Draft.makeRectangle(2000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(15500, 5000, 0), FreeCAD.Rotation(0, 0, 0)))
room_4.ViewObject.LineWidth = 1.5
room_4.ViewObject
label_4 = Draft.make_text(["Restroom", "4 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(16166, 6000, 0), FreeCAD.Rotation(0, 0, 0)))
label_4.ViewObject.FontSize = 180
# Overall Dimensions
dim_h = Draft.make_linear_dimension(FreeCAD.Vector(0, -800, 0), FreeCAD.Vector(18000, -800, 0))
dim_h.ViewObject.FontSize = 350
dim_h.ViewObject
dim_v = Draft.make_linear_dimension(FreeCAD.Vector(-800, 0, 0), FreeCAD.Vector(-800, 12000, 0))
dim_v.ViewObject.FontSize = 350
dim_v.ViewObject
# Grid System
grid_idx = 0
for i in range(0, 20000, 2000):
    grid_v = Draft.makeLine(FreeCAD.Vector(i, -1500, 0), FreeCAD.Vector(i, 13500, 0))
    grid_v.ViewObject.LineWidth = 0.3
    grid_v.ViewObject
    if i <= 18000:
        exec(f"g_{grid_idx} = Draft.make_text([chr(65 + {i}//2000)], placement=FreeCAD.Placement(FreeCAD.Vector({i} - 100, -2000, 0), FreeCAD.Rotation(0, 0, 0)))")
        exec(f"g_{grid_idx}.ViewObject.FontSize = 250")
        exec(f"g_{grid_idx}.ViewObject.TextColor = (1.0, 0.0, 0.0)")
        grid_idx += 1
for j in range(0, 14000, 2000):
    grid_h = Draft.makeLine(FreeCAD.Vector(-1500, j, 0), FreeCAD.Vector(19500, j, 0))
    grid_h.ViewObject.LineWidth = 0.3
    grid_h.ViewObject
    if j <= 12000:
        exec(f"g_{grid_idx} = Draft.make_text([str({j}//2000 + 1)], placement=FreeCAD.Placement(FreeCAD.Vector(-2200, {j} - 100, 0), FreeCAD.Rotation(0, 0, 0)))")
        exec(f"g_{grid_idx}.ViewObject.FontSize = 250")
        exec(f"g_{grid_idx}.ViewObject.TextColor = (1.0, 0.0, 0.0)")
        grid_idx += 1
# Title Block
title = Draft.make_text(["College Computer Lab", "Scale: 1:100", "Total Area: 180 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(12000, -2500, 0), FreeCAD.Rotation(0, 0, 0)))
title.ViewObject.FontSize = 350
title.ViewObject.TextColor = (0.0, 0.0, 0.0)
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.activeDocument().activeView().viewTop()
print("✓ Floor plan generation complete")