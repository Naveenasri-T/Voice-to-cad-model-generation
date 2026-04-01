import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
import FreeCAD
import Draft
# TEMPLATE_GENERATED
doc = FreeCAD.newDocument("Medical_Clinic_Layout")
# === FLOOR PLAN - Medical Clinic Layout ===
print("Generating: Medical Clinic Layout")
print("Total Area: 280 sqm")
# Exterior perimeter
exterior = Draft.makeWire([
    FreeCAD.Vector(0, 0, 0),
    FreeCAD.Vector(22000, 0, 0),
    FreeCAD.Vector(22000, 14000, 0),
    FreeCAD.Vector(0, 14000, 0),
    FreeCAD.Vector(0, 0, 0)
], closed=True)
exterior.ViewObject.LineWidth = 4.0
exterior.ViewObject
# Room Definitions
# Reception (12 sqm)
room_0 = Draft.makeRectangle(4000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(1000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
room_0.ViewObject.LineWidth = 1.5
room_0.ViewObject
label_0 = Draft.make_text(["Reception", "12 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(2333, 2500, 0), FreeCAD.Rotation(0, 0, 0)))
label_0.ViewObject.FontSize = 180
# Waiting Area (40 sqm)
room_1 = Draft.makeRectangle(8000, 5000, placement=FreeCAD.Placement(FreeCAD.Vector(6000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
room_1.ViewObject.LineWidth = 1.5
room_1.ViewObject
label_1 = Draft.make_text(["Waiting Area", "40 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(8666, 3500, 0), FreeCAD.Rotation(0, 0, 0)))
label_1.ViewObject.FontSize = 180
# Consultation Room 1 (18 sqm)
room_2 = Draft.makeRectangle(4500, 4000, placement=FreeCAD.Placement(FreeCAD.Vector(1000, 5000, 0), FreeCAD.Rotation(0, 0, 0)))
room_2.ViewObject.LineWidth = 1.5
room_2.ViewObject
label_2 = Draft.make_text(["Consultation Room 1", "18 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(2500, 7000, 0), FreeCAD.Rotation(0, 0, 0)))
label_2.ViewObject.FontSize = 180
# Consultation Room 2 (18 sqm)
room_3 = Draft.makeRectangle(4500, 4000, placement=FreeCAD.Placement(FreeCAD.Vector(6500, 5000, 0), FreeCAD.Rotation(0, 0, 0)))
room_3.ViewObject.LineWidth = 1.5
room_3.ViewObject
label_3 = Draft.make_text(["Consultation Room 2", "18 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(8000, 7000, 0), FreeCAD.Rotation(0, 0, 0)))
label_3.ViewObject.FontSize = 180
# Consultation Room 3 (18 sqm)
room_4 = Draft.makeRectangle(4500, 4000, placement=FreeCAD.Placement(FreeCAD.Vector(12000, 5000, 0), FreeCAD.Rotation(0, 0, 0)))
room_4.ViewObject.LineWidth = 1.5
room_4.ViewObject
label_4 = Draft.make_text(["Consultation Room 3", "18 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(13500, 7000, 0), FreeCAD.Rotation(0, 0, 0)))
label_4.ViewObject.FontSize = 180
# Pharmacy (20 sqm)
room_5 = Draft.makeRectangle(5000, 4000, placement=FreeCAD.Placement(FreeCAD.Vector(17000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
room_5.ViewObject.LineWidth = 1.5
room_5.ViewObject
label_5 = Draft.make_text(["Pharmacy", "20 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(18666, 3000, 0), FreeCAD.Rotation(0, 0, 0)))
label_5.ViewObject.FontSize = 180
# Laboratory (30 sqm)
room_6 = Draft.makeRectangle(6000, 5000, placement=FreeCAD.Placement(FreeCAD.Vector(1000, 10000, 0), FreeCAD.Rotation(0, 0, 0)))
room_6.ViewObject.LineWidth = 1.5
room_6.ViewObject
label_6 = Draft.make_text(["Laboratory", "30 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(3000, 12500, 0), FreeCAD.Rotation(0, 0, 0)))
label_6.ViewObject.FontSize = 180
# Sample Collection (7.5 sqm)
room_7 = Draft.makeRectangle(3000, 2500, placement=FreeCAD.Placement(FreeCAD.Vector(8000, 10000, 0), FreeCAD.Rotation(0, 0, 0)))
room_7.ViewObject.LineWidth = 1.5
room_7.ViewObject
label_7 = Draft.make_text(["Sample Collection", "7.5 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(9000, 11250, 0), FreeCAD.Rotation(0, 0, 0)))
label_7.ViewObject.FontSize = 180
# Staff Room (7.5 sqm)
room_8 = Draft.makeRectangle(3000, 2500, placement=FreeCAD.Placement(FreeCAD.Vector(12000, 10000, 0), FreeCAD.Rotation(0, 0, 0)))
room_8.ViewObject.LineWidth = 1.5
room_8.ViewObject
label_8 = Draft.make_text(["Staff Room", "7.5 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(13000, 11250, 0), FreeCAD.Rotation(0, 0, 0)))
label_8.ViewObject.FontSize = 180
# Restrooms (12 sqm)
room_9 = Draft.makeRectangle(4000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(16000, 10000, 0), FreeCAD.Rotation(0, 0, 0)))
room_9.ViewObject.LineWidth = 1.5
room_9.ViewObject
label_9 = Draft.make_text(["Restrooms", "12 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(17333, 11500, 0), FreeCAD.Rotation(0, 0, 0)))
label_9.ViewObject.FontSize = 180
# Overall Dimensions
dim_h = Draft.make_linear_dimension(FreeCAD.Vector(0, -800, 0), FreeCAD.Vector(22000, -800, 0))
dim_h.ViewObject.FontSize = 350
dim_h.ViewObject
dim_v = Draft.make_linear_dimension(FreeCAD.Vector(-800, 0, 0), FreeCAD.Vector(-800, 14000, 0))
dim_v.ViewObject.FontSize = 350
dim_v.ViewObject
# Grid System
grid_idx = 0
for i in range(0, 24000, 2000):
    grid_v = Draft.makeLine(FreeCAD.Vector(i, -1500, 0), FreeCAD.Vector(i, 15500, 0))
    grid_v.ViewObject.LineWidth = 0.3
    grid_v.ViewObject
    if i <= 22000:
        exec(f"g_{grid_idx} = Draft.make_text([chr(65 + {i}//2000)], placement=FreeCAD.Placement(FreeCAD.Vector({i} - 100, -2000, 0), FreeCAD.Rotation(0, 0, 0)))")
        exec(f"g_{grid_idx}.ViewObject.FontSize = 250")
        exec(f"g_{grid_idx}.ViewObject.TextColor = (1.0, 0.0, 0.0)")
        grid_idx += 1
for j in range(0, 16000, 2000):
    grid_h = Draft.makeLine(FreeCAD.Vector(-1500, j, 0), FreeCAD.Vector(23500, j, 0))
    grid_h.ViewObject.LineWidth = 0.3
    grid_h.ViewObject
    if j <= 14000:
        exec(f"g_{grid_idx} = Draft.make_text([str({j}//2000 + 1)], placement=FreeCAD.Placement(FreeCAD.Vector(-2200, {j} - 100, 0), FreeCAD.Rotation(0, 0, 0)))")
        exec(f"g_{grid_idx}.ViewObject.FontSize = 250")
        exec(f"g_{grid_idx}.ViewObject.TextColor = (1.0, 0.0, 0.0)")
        grid_idx += 1
# Title Block
title = Draft.make_text(["Medical Clinic Layout", "Scale: 1:100", "Total Area: 280 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(16000, -2500, 0), FreeCAD.Rotation(0, 0, 0)))
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
