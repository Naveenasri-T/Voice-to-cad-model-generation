import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
import FreeCAD
import Draft

doc = FreeCAD.newDocument("2BHK_House_Blueprint")

# === FRONT VIEW (y_offset = 0) ===
front_outline = Draft.makeWire([
    FreeCAD.Vector(0, 0, 0),
    FreeCAD.Vector(12000, 0, 0),
    FreeCAD.Vector(12000, 3000, 0),
    FreeCAD.Vector(0, 3000, 0),
    FreeCAD.Vector(0, 0, 0)
], closed=True)
front_outline.ViewObject.LineWidth = 3.0

# Doors and windows
door1 = Draft.makeLine(FreeCAD.Vector(1000, 0, 0), FreeCAD.Vector(1900, 0, 0))
door1.ViewObject.LineWidth = 2.0
window1 = Draft.makeRectangle(800, 1200, placement=FreeCAD.Placement(FreeCAD.Vector(3000, 800, 0), FreeCAD.Rotation(0, 0, 0)))
window1.ViewObject.LineWidth = 1.5
window2 = Draft.makeRectangle(800, 1200, placement=FreeCAD.Placement(FreeCAD.Vector(8000, 800, 0), FreeCAD.Rotation(0, 0, 0)))
window2.ViewObject.LineWidth = 1.5

# Dimensions
dim1 = Draft.make_linear_dimension(FreeCAD.Vector(0, -500, 0), FreeCAD.Vector(12000, -500, 0))
dim1.ViewObject.FontSize = 300
dim2 = Draft.make_linear_dimension(FreeCAD.Vector(-500, 0, 0), FreeCAD.Vector(-500, 3000, 0))
dim2.ViewObject.FontSize = 300

# === TOP VIEW (y_offset = 5000) ===
top_outline = Draft.makeWire([
    FreeCAD.Vector(0, 5000, 0),
    FreeCAD.Vector(12000, 5000, 0),
    FreeCAD.Vector(12000, 13000, 0),
    FreeCAD.Vector(0, 13000, 0),
    FreeCAD.Vector(0, 5000, 0)
], closed=True)
top_outline.ViewObject.LineWidth = 3.0

# Rooms
living_room = Draft.makeRectangle(5000, 4000, placement=FreeCAD.Placement(FreeCAD.Vector(1000, 6000, 0), FreeCAD.Rotation(0, 0, 0)))
living_room.ViewObject.LineWidth = 1.5
living_label = Draft.make_text(["Living Room"], point=FreeCAD.Vector(2500, 7500, 0))
living_label.ViewObject.FontSize = 200

kitchen = Draft.makeRectangle(3000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(7000, 6000, 0), FreeCAD.Rotation(0, 0, 0)))
kitchen.ViewObject.LineWidth = 1.5
kitchen_label = Draft.make_text(["Kitchen"], point=FreeCAD.Vector(7800, 7200, 0))
kitchen_label.ViewObject.FontSize = 200

bedroom1 = Draft.makeRectangle(4000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(1000, 10000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom1.ViewObject.LineWidth = 1.5
bed1_label = Draft.make_text(["Bedroom 1"], point=FreeCAD.Vector(2200, 11000, 0))
bed1_label.ViewObject.FontSize = 200

bedroom2 = Draft.makeRectangle(4000, 3000, placement=FreeCAD.Placement(FreeCAD.Vector(6000, 10000, 0), FreeCAD.Rotation(0, 0, 0)))
bedroom2.ViewObject.LineWidth = 1.5
bed2_label = Draft.make_text(["Bedroom 2"], point=FreeCAD.Vector(7200, 11000, 0))
bed2_label.ViewObject.FontSize = 200

# Dimensions
dim3 = Draft.make_linear_dimension(FreeCAD.Vector(0, 4500, 0), FreeCAD.Vector(12000, 4500, 0))
dim3.ViewObject.FontSize = 300
dim4 = Draft.make_linear_dimension(FreeCAD.Vector(-500, 5000, 0), FreeCAD.Vector(-500, 13000, 0))
dim4.ViewObject.FontSize = 300

# === SIDE VIEW (y_offset = 15000) ===
side_outline = Draft.makeWire([
    FreeCAD.Vector(0, 15000, 0),
    FreeCAD.Vector(8000, 15000, 0),
    FreeCAD.Vector(8000, 18000, 0),
    FreeCAD.Vector(0, 18000, 0),
    FreeCAD.Vector(0, 15000, 0)
], closed=True)
side_outline.ViewObject.LineWidth = 3.0

# Dimensions
dim5 = Draft.make_linear_dimension(FreeCAD.Vector(0, 14500, 0), FreeCAD.Vector(8000, 14500, 0))
dim5.ViewObject.FontSize = 300
dim6 = Draft.make_linear_dimension(FreeCAD.Vector(-500, 15000, 0), FreeCAD.Vector(-500, 18000, 0))
dim6.ViewObject.FontSize = 300

# === GRID SYSTEM ===
for i in range(0, 13000, 2000):
    grid_h = Draft.makeLine(FreeCAD.Vector(i, 0, 0), FreeCAD.Vector(i, 18000, 0))
    grid_h.ViewObject.LineWidth = 0.3
    # LineStyle "Dotted" not supported, using thin line instead
    label = Draft.make_text([chr(65 + i//2000)], point=FreeCAD.Vector(i, -700, 0))
    label.ViewObject.FontSize = 200

for i in range(0, 18000, 2000):
    grid_v = Draft.makeLine(FreeCAD.Vector(0, i, 0), FreeCAD.Vector(12000, i, 0))
    grid_v.ViewObject.LineWidth = 0.3
    # LineStyle "Dotted" not supported, using thin line instead

# === TITLE BLOCK ===
title = Draft.make_text(["2BHK House Blueprint", "Scale: 1:100", "Date: 2025-11-30"], point=FreeCAD.Vector(9000, -1200, 0))
title.ViewObject.FontSize = 250

doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.activeDocument().activeView().viewTop()

doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
