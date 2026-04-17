import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
import FreeCAD
import Draft
# TEMPLATE_GENERATED
doc = FreeCAD.newDocument("2BHK_Apartment_with_Parking")
# === FLOOR PLAN ===
# Exterior perimeter
exterior = Draft.makeWire([
    FreeCAD.Vector(0, 0, 0),
    FreeCAD.Vector(15000, 0, 0),
    FreeCAD.Vector(15000, 12000, 0),
    FreeCAD.Vector(0, 12000, 0),
    FreeCAD.Vector(0, 0, 0)
], closed=True)
exterior.ViewObject.LineWidth = 3.0
# Living Room
living_room_rect = Draft.makeRectangle(5000, 4000, placement=FreeCAD.Placement(FreeCAD.Vector(1000, 6000, 0), FreeCAD.Rotation(0, 0, 0)))
living_room_rect.ViewObject.LineWidth = 1.5
living_room_label = Draft.make_text(["Living Room"], placement=FreeCAD.Placement(FreeCAD.Vector(2666, 8000, 0), FreeCAD.Rotation(0, 0, 0)))
living_room_label.ViewObject.FontSize = 200
# Master Bedroom
master_bedroom_rect = Draft.makeRectangle(4000, 3500, placement=FreeCAD.Placement(FreeCAD.Vector(1000, 10500, 0), FreeCAD.Rotation(0, 0, 0)))
master_bedroom_rect.ViewObject.LineWidth = 1.5
master_bedroom_label = Draft.make_text(["Master Bedroom"], placement=FreeCAD.Placement(FreeCAD.Vector(2333, 12250, 0), FreeCAD.Rotation(0, 0, 0)))
master_bedroom_label.ViewObject.FontSize = 200
# Bedroom 2
bedroom_2_rect = Draft.makeRectangle(3500, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(6000, 10500, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom_2_rect.ViewObject.LineWidth = 1.5
bedroom_2_label = Draft.make_text(["Bedroom 2"], placement=FreeCAD.Placement(FreeCAD.Vector(7166, 12000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom_2_label.ViewObject.FontSize = 200
# Kitchen
kitchen_rect = Draft.makeRectangle(3500, 2500, placement=FreeCAD.Placement(FreeCAD.Vector(7000, 6000, 0), FreeCAD.Rotation(0, 0, 0)))
kitchen_rect.ViewObject.LineWidth = 1.5
kitchen_label = Draft.make_text(["Kitchen"], placement=FreeCAD.Placement(FreeCAD.Vector(8166, 7250, 0), FreeCAD.Rotation(0, 0, 0)))
kitchen_label.ViewObject.FontSize = 200
# Bathroom 1
bathroom_1_rect = Draft.makeRectangle(2500, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(11000, 6000, 0), FreeCAD.Rotation(0, 0, 0)))
bathroom_1_rect.ViewObject.LineWidth = 1.5
bathroom_1_label = Draft.make_text(["Bathroom 1"], placement=FreeCAD.Placement(FreeCAD.Vector(11833, 7000, 0), FreeCAD.Rotation(0, 0, 0)))
bathroom_1_label.ViewObject.FontSize = 200
# Bathroom 2
bathroom_2_rect = Draft.makeRectangle(2000, 1800, placement=FreeCAD.Placement(FreeCAD.Vector(5200, 10500, 0), FreeCAD.Rotation(0, 0, 0)))
bathroom_2_rect.ViewObject.LineWidth = 1.5
bathroom_2_label = Draft.make_text(["Bathroom 2"], placement=FreeCAD.Placement(FreeCAD.Vector(5866, 11400, 0), FreeCAD.Rotation(0, 0, 0)))
bathroom_2_label.ViewObject.FontSize = 200
# Parking
parking_rect = Draft.makeRectangle(5000, 2500, placement=FreeCAD.Placement(FreeCAD.Vector(1000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
parking_rect.ViewObject.LineWidth = 1.5
parking_label = Draft.make_text(["Parking"], placement=FreeCAD.Placement(FreeCAD.Vector(2666, 2250, 0), FreeCAD.Rotation(0, 0, 0)))
parking_label.ViewObject.FontSize = 200
# Overall dimensions
dim_h = Draft.make_linear_dimension(FreeCAD.Vector(0, -500, 0), FreeCAD.Vector(15000, -500, 0))
dim_h.ViewObject.FontSize = 300
dim_v = Draft.make_linear_dimension(FreeCAD.Vector(-500, 0, 0), FreeCAD.Vector(-500, 12000, 0))
dim_v.ViewObject.FontSize = 300
# Grid system
for i in range(0, 17000, 2000):
    grid_line = Draft.makeLine(FreeCAD.Vector(i, -1000, 0), FreeCAD.Vector(i, 13000, 0))
    grid_line.ViewObject.LineWidth = 0.3
# Title block
title = Draft.make_text(["2BHK Apartment with Parking", "Scale: 1:100"], placement=FreeCAD.Placement(FreeCAD.Vector(10000, -1500, 0), FreeCAD.Rotation(0, 0, 0)))
title.ViewObject.FontSize = 300
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.activeDocument().activeView().viewTop()
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
