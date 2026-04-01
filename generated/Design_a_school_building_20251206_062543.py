import FreeCAD
import Draft
# TEMPLATE_GENERATED
doc = FreeCAD.newDocument("Primary_School_Classroom_Block")
# === FLOOR PLAN - Primary School Classroom Block ===
print("Generating: Primary School Classroom Block")
print("Total Area: 680 sqm")
# Exterior perimeter
exterior = Draft.makeWire([
    FreeCAD.Vector(0, 0, 0),
    FreeCAD.Vector(40000, 0, 0),
    FreeCAD.Vector(40000, 18000, 0),
    FreeCAD.Vector(0, 18000, 0),
    FreeCAD.Vector(0, 0, 0)
], closed=True)
exterior.ViewObject.LineWidth = 4.0
exterior.ViewObject
# Room Definitions
# Classroom 1 (52 sqm)
room_0 = Draft.makeRectangle(8000, 6500, placement=FreeCAD.Placement(FreeCAD.Vector(1000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
room_0.ViewObject.LineWidth = 1.5
room_0.ViewObject
label_0 = Draft.make_text(["Classroom 1", "52 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(3666, 4250, 0), FreeCAD.Rotation(0, 0, 0)))
label_0.ViewObject.FontSize = 180
# Classroom 2 (52 sqm)
room_1 = Draft.makeRectangle(8000, 6500, placement=FreeCAD.Placement(FreeCAD.Vector(10000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
room_1.ViewObject.LineWidth = 1.5
room_1.ViewObject
label_1 = Draft.make_text(["Classroom 2", "52 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(12666, 4250, 0), FreeCAD.Rotation(0, 0, 0)))
label_1.ViewObject.FontSize = 180
# Classroom 3 (52 sqm)
room_2 = Draft.makeRectangle(8000, 6500, placement=FreeCAD.Placement(FreeCAD.Vector(19000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
room_2.ViewObject.LineWidth = 1.5
room_2.ViewObject
label_2 = Draft.make_text(["Classroom 3", "52 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(21666, 4250, 0), FreeCAD.Rotation(0, 0, 0)))
label_2.ViewObject.FontSize = 180
# Classroom 4 (52 sqm)
room_3 = Draft.makeRectangle(8000, 6500, placement=FreeCAD.Placement(FreeCAD.Vector(28000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
room_3.ViewObject.LineWidth = 1.5
room_3.ViewObject
label_3 = Draft.make_text(["Classroom 4", "52 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(30666, 4250, 0), FreeCAD.Rotation(0, 0, 0)))
label_3.ViewObject.FontSize = 180
# Classroom 5 (52 sqm)
room_4 = Draft.makeRectangle(8000, 6500, placement=FreeCAD.Placement(FreeCAD.Vector(1000, 8500, 0), FreeCAD.Rotation(0, 0, 0)))
room_4.ViewObject.LineWidth = 1.5
room_4.ViewObject
label_4 = Draft.make_text(["Classroom 5", "52 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(3666, 11750, 0), FreeCAD.Rotation(0, 0, 0)))
label_4.ViewObject.FontSize = 180
# Classroom 6 (52 sqm)
room_5 = Draft.makeRectangle(8000, 6500, placement=FreeCAD.Placement(FreeCAD.Vector(10000, 8500, 0), FreeCAD.Rotation(0, 0, 0)))
room_5.ViewObject.LineWidth = 1.5
room_5.ViewObject
label_5 = Draft.make_text(["Classroom 6", "52 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(12666, 11750, 0), FreeCAD.Rotation(0, 0, 0)))
label_5.ViewObject.FontSize = 180
# Library (52 sqm)
room_6 = Draft.makeRectangle(8000, 6500, placement=FreeCAD.Placement(FreeCAD.Vector(19000, 8500, 0), FreeCAD.Rotation(0, 0, 0)))
room_6.ViewObject.LineWidth = 1.5
room_6.ViewObject
label_6 = Draft.make_text(["Library", "52 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(21666, 11750, 0), FreeCAD.Rotation(0, 0, 0)))
label_6.ViewObject.FontSize = 180
# Staff Room (20 sqm)
room_7 = Draft.makeRectangle(5000, 4000, placement=FreeCAD.Placement(FreeCAD.Vector(28000, 8500, 0), FreeCAD.Rotation(0, 0, 0)))
room_7.ViewObject.LineWidth = 1.5
room_7.ViewObject
label_7 = Draft.make_text(["Staff Room", "20 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(29666, 10500, 0), FreeCAD.Rotation(0, 0, 0)))
label_7.ViewObject.FontSize = 180
# Principal Office (16 sqm)
room_8 = Draft.makeRectangle(4000, 4000, placement=FreeCAD.Placement(FreeCAD.Vector(34000, 8500, 0), FreeCAD.Rotation(0, 0, 0)))
room_8.ViewObject.LineWidth = 1.5
room_8.ViewObject
label_8 = Draft.make_text(["Principal Office", "16 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(35333, 10500, 0), FreeCAD.Rotation(0, 0, 0)))
label_8.ViewObject.FontSize = 180
# Boys Restroom (12 sqm)
room_9 = Draft.makeRectangle(4000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(28000, 13500, 0), FreeCAD.Rotation(0, 0, 0)))
room_9.ViewObject.LineWidth = 1.5
room_9.ViewObject
label_9 = Draft.make_text(["Boys Restroom", "12 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(29333, 15000, 0), FreeCAD.Rotation(0, 0, 0)))
label_9.ViewObject.FontSize = 180
# Girls Restroom (12 sqm)
room_10 = Draft.makeRectangle(4000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(33000, 13500, 0), FreeCAD.Rotation(0, 0, 0)))
room_10.ViewObject.LineWidth = 1.5
room_10.ViewObject
label_10 = Draft.make_text(["Girls Restroom", "12 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(34333, 15000, 0), FreeCAD.Rotation(0, 0, 0)))
label_10.ViewObject.FontSize = 180
# Overall Dimensions
dim_h = Draft.make_linear_dimension(FreeCAD.Vector(0, -800, 0), FreeCAD.Vector(40000, -800, 0))
dim_h.ViewObject.FontSize = 350
dim_h.ViewObject
dim_v = Draft.make_linear_dimension(FreeCAD.Vector(-800, 0, 0), FreeCAD.Vector(-800, 18000, 0))
dim_v.ViewObject.FontSize = 350
dim_v.ViewObject
# Grid System
grid_idx = 0
for i in range(0, 42000, 2000):
    grid_v = Draft.makeLine(FreeCAD.Vector(i, -1500, 0), FreeCAD.Vector(i, 19500, 0))
    grid_v.ViewObject.LineWidth = 0.3
    grid_v.ViewObject
    if i <= 40000:
        exec(f"g_{grid_idx} = Draft.make_text([chr(65 + {i}//2000)], placement=FreeCAD.Placement(FreeCAD.Vector({i} - 100, -2000, 0), FreeCAD.Rotation(0, 0, 0)))")
        exec(f"g_{grid_idx}.ViewObject.FontSize = 250")
        exec(f"g_{grid_idx}.ViewObject.TextColor = (1.0, 0.0, 0.0)")
        grid_idx += 1
for j in range(0, 20000, 2000):
    grid_h = Draft.makeLine(FreeCAD.Vector(-1500, j, 0), FreeCAD.Vector(41500, j, 0))
    grid_h.ViewObject.LineWidth = 0.3
    grid_h.ViewObject
    if j <= 18000:
        exec(f"g_{grid_idx} = Draft.make_text([str({j}//2000 + 1)], placement=FreeCAD.Placement(FreeCAD.Vector(-2200, {j} - 100, 0), FreeCAD.Rotation(0, 0, 0)))")
        exec(f"g_{grid_idx}.ViewObject.FontSize = 250")
        exec(f"g_{grid_idx}.ViewObject.TextColor = (1.0, 0.0, 0.0)")
        grid_idx += 1
# Title Block
title = Draft.make_text(["Primary School Classroom Block", "Scale: 1:100", "Total Area: 680 sqm"], placement=FreeCAD.Placement(FreeCAD.Vector(34000, -2500, 0), FreeCAD.Rotation(0, 0, 0)))
title.ViewObject.FontSize = 350
title.ViewObject.TextColor = (0.0, 0.0, 0.0)
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.activeDocument().activeView().viewTop()
print("✓ Floor plan generation complete")