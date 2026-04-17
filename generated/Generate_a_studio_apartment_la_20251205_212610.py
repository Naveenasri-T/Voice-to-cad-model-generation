import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
import FreeCAD
import Draft
# TEMPLATE_GENERATED
doc = FreeCAD.newDocument("2BHK_Apartment_with_Parking")
# === FLOOR PLAN - 2BHK Apartment with Parking ===
print("Generating: 2BHK Apartment with Parking")
print("Total Area: 95 sqm")
# Exterior perimeter
exterior = Draft.makeWire([
    FreeCAD.Vector(0, 0, 0),
    FreeCAD.Vector(15000, 0, 0),
    FreeCAD.Vector(15000, 12000, 0),
    FreeCAD.Vector(0, 12000, 0),
    FreeCAD.Vector(0, 0, 0)
], closed=True)
exterior.ViewObject.LineWidth = 4.0
exterior.ViewObject
# Room Definitions
# Living Room (20 sqm)
room_0 = Draft.makeRectangle(5000, 4000, placement=FreeCAD.Placement(FreeCAD.Vector(1000, 6000, 0), FreeCAD.Rotation(0, 0, 0)))
room_0.ViewObject.LineWidth = 1.5
room_0.ViewObject
label_0 = Draft.make_text(["Living Room", "20 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(2666, 8000, 0), FreeCAD.Rotation(0, 0, 0)))
label_0.ViewObject.FontSize = 180
# Master Bedroom (14 sqm)
room_1 = Draft.makeRectangle(4000, 3500, placement=FreeCAD.Placement(FreeCAD.Vector(1000, 10500, 0), FreeCAD.Rotation(0, 0, 0)))
room_1.ViewObject.LineWidth = 1.5
room_1.ViewObject
label_1 = Draft.make_text(["Master Bedroom", "14 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(2333, 12250, 0), FreeCAD.Rotation(0, 0, 0)))
label_1.ViewObject.FontSize = 180
# Bedroom 2 (10.5 sqm)
room_2 = Draft.makeRectangle(3500, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(6000, 10500, 0), FreeCAD.Rotation(0, 0, 0)))
room_2.ViewObject.LineWidth = 1.5
room_2.ViewObject
label_2 = Draft.make_text(["Bedroom 2", "10.5 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(7166, 12000, 0), FreeCAD.Rotation(0, 0, 0)))
label_2.ViewObject.FontSize = 180
# Kitchen (8.75 sqm)
room_3 = Draft.makeRectangle(3500, 2500, placement=FreeCAD.Placement(FreeCAD.Vector(7000, 6000, 0), FreeCAD.Rotation(0, 0, 0)))
room_3.ViewObject.LineWidth = 1.5
room_3.ViewObject
label_3 = Draft.make_text(["Kitchen", "8.75 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(8166, 7250, 0), FreeCAD.Rotation(0, 0, 0)))
label_3.ViewObject.FontSize = 180
# Bathroom 1 (5 sqm)
room_4 = Draft.makeRectangle(2500, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(11000, 6000, 0), FreeCAD.Rotation(0, 0, 0)))
room_4.ViewObject.LineWidth = 1.5
room_4.ViewObject
label_4 = Draft.make_text(["Bathroom 1", "5 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(11833, 7000, 0), FreeCAD.Rotation(0, 0, 0)))
label_4.ViewObject.FontSize = 180
# Bathroom 2 (3.6 sqm)
room_5 = Draft.makeRectangle(2000, 1800, placement=FreeCAD.Placement(FreeCAD.Vector(5200, 10500, 0), FreeCAD.Rotation(0, 0, 0)))
room_5.ViewObject.LineWidth = 1.5
room_5.ViewObject
label_5 = Draft.make_text(["Bathroom 2", "3.6 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(5866, 11400, 0), FreeCAD.Rotation(0, 0, 0)))
label_5.ViewObject.FontSize = 180
# Parking (12.5 sqm)
room_6 = Draft.makeRectangle(5000, 2500, placement=FreeCAD.Placement(FreeCAD.Vector(1000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
room_6.ViewObject.LineWidth = 1.5
room_6.ViewObject
label_6 = Draft.make_text(["Parking", "12.5 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(2666, 2250, 0), FreeCAD.Rotation(0, 0, 0)))
label_6.ViewObject.FontSize = 180
# Doors
door_0 = Draft.makeLine(FreeCAD.Vector(7500, 0, 0), FreeCAD.Vector(8400, 0, 0))
door_0.ViewObject.LineWidth = 2.0
door_0.ViewObject
door_1 = Draft.makeLine(FreeCAD.Vector(4800, 6000, 0), FreeCAD.Vector(5600, 6000, 0))
door_1.ViewObject.LineWidth = 2.0
door_1.ViewObject
door_2 = Draft.makeLine(FreeCAD.Vector(6000, 10700, 0), FreeCAD.Vector(6800, 10700, 0))
door_2.ViewObject.LineWidth = 2.0
door_2.ViewObject
# Windows
win_0 = Draft.makeRectangle(1200, 120, placement=FreeCAD.Placement(FreeCAD.Vector(3000, 12000, 0), FreeCAD.Rotation(0, 0, 0)))
win_0.ViewObject.LineWidth = 1.5
win_0.ViewObject
win_1 = Draft.makeRectangle(1200, 120, placement=FreeCAD.Placement(FreeCAD.Vector(8000, 12000, 0), FreeCAD.Rotation(0, 0, 0)))
win_1.ViewObject.LineWidth = 1.5
win_1.ViewObject
win_2 = Draft.makeRectangle(1000, 120, placement=FreeCAD.Placement(FreeCAD.Vector(0, 7000, 0), FreeCAD.Rotation(0, 0, 0)))
win_2.ViewObject.LineWidth = 1.5
win_2.ViewObject
# Overall Dimensions
dim_h = Draft.make_linear_dimension(FreeCAD.Vector(0, -800, 0), FreeCAD.Vector(15000, -800, 0))
dim_h.ViewObject.FontSize = 350
dim_h.ViewObject
dim_v = Draft.make_linear_dimension(FreeCAD.Vector(-800, 0, 0), FreeCAD.Vector(-800, 12000, 0))
dim_v.ViewObject.FontSize = 350
dim_v.ViewObject
# Grid System
grid_idx = 0
for i in range(0, 17000, 2000):
    grid_v = Draft.makeLine(FreeCAD.Vector(i, -1500, 0), FreeCAD.Vector(i, 13500, 0))
    grid_v.ViewObject.LineWidth = 0.3
    grid_v.ViewObject
    if i <= 15000:
        exec(f"g_{grid_idx} = Draft.make_text([chr(65 + {i}//2000)], placement=FreeCAD.Placement(FreeCAD.Vector({i} - 100, -2000, 0), FreeCAD.Rotation(0, 0, 0)))")
        exec(f"g_{grid_idx}.ViewObject.FontSize = 250")
        exec(f"g_{grid_idx}.ViewObject.TextColor = (1.0, 0.0, 0.0)")
        grid_idx += 1
for j in range(0, 14000, 2000):
    grid_h = Draft.makeLine(FreeCAD.Vector(-1500, j, 0), FreeCAD.Vector(16500, j, 0))
    grid_h.ViewObject.LineWidth = 0.3
    grid_h.ViewObject
    if j <= 12000:
        exec(f"g_{grid_idx} = Draft.make_text([str({j}//2000 + 1)], placement=FreeCAD.Placement(FreeCAD.Vector(-2200, {j} - 100, 0), FreeCAD.Rotation(0, 0, 0)))")
        exec(f"g_{grid_idx}.ViewObject.FontSize = 250")
        exec(f"g_{grid_idx}.ViewObject.TextColor = (1.0, 0.0, 0.0)")
        grid_idx += 1
# Title Block
title = Draft.make_text(["2BHK Apartment with Parking", "Scale: 1:100", "Total Area: 95 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(9000, -2500, 0), FreeCAD.Rotation(0, 0, 0)))
title.ViewObject.FontSize = 350
title.ViewObject.TextColor = (0.0, 0.0, 0.0)
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.activeDocument().activeView().viewTop()
print("✓ Floor plan generation complete")
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
