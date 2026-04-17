import FreeCAD
import Draft
print("=== 2D BLUEPRINT ENGINEERING START ===")
print("Scope: 2BHK house with parking and garden")
doc = FreeCAD.newDocument("Professional_2D_Blueprint")
GRID_SPACING = 1000
VIEW_SPACING = 15000
plan_y  = 0
front_y = VIEW_SPACING
side_y  = 2 * VIEW_SPACING
drawing_commands = 0
dimension_count  = 0
text_count       = 0
def style(obj, width=2.0, color=(0.0, 0.0, 0.0)):
    if hasattr(obj, "ViewObject"):
        obj.ViewObject.LineWidth = width
        obj.ViewObject
# === PLAN VIEW ===
# Exterior boundary
exterior = Draft.makeWire([
    FreeCAD.Vector(0, 0, 0),
    FreeCAD.Vector(12000, 0, 0),
    FreeCAD.Vector(12000, 9000, 0),
    FreeCAD.Vector(0, 9000, 0),
    FreeCAD.Vector(0, 0, 0)
], closed=True, face=False)
style(exterior, width=3.0)
drawing_commands += 1
# Partitions
partition1 = Draft.makeLine(FreeCAD.Vector(3000, 0, 0), FreeCAD.Vector(3000, 9000, 0))
style(partition1, width=2.0)
drawing_commands += 1
partition2 = Draft.makeLine(FreeCAD.Vector(6000, 0, 0), FreeCAD.Vector(6000, 9000, 0))
style(partition2, width=2.0)
drawing_commands += 1
partition3 = Draft.makeLine(FreeCAD.Vector(9000, 0, 0), FreeCAD.Vector(9000, 9000, 0))
style(partition3, width=2.0)
drawing_commands += 1
# Furniture
furniture1 = Draft.makeRectangle(2000, 1000, placement=FreeCAD.Placement(FreeCAD.Vector(1000, 1000, 0), FreeCAD.Rotation(0, 0, 0, 1)))
style(furniture1, width=1.5, color=(0.3, 0.3, 0.3))
drawing_commands += 1
furniture2 = Draft.makeRectangle(2000, 1000, placement=FreeCAD.Placement(FreeCAD.Vector(4000, 1000, 0), FreeCAD.Rotation(0, 0, 0, 1)))
style(furniture2, width=1.5, color=(0.3, 0.3, 0.3))
drawing_commands += 1
# Doors
door1 = Draft.makeLine(FreeCAD.Vector(0, 4500, 0), FreeCAD.Vector(1000, 4500, 0))
style(door1, width=1.5)
drawing_commands += 1
door2 = Draft.makeLine(FreeCAD.Vector(6000, 4500, 0), FreeCAD.Vector(7000, 4500, 0))
style(door2, width=1.5)
drawing_commands += 1
# Windows
window1 = Draft.makeLine(FreeCAD.Vector(2000, 0, 0), FreeCAD.Vector(2000, 1000, 0))
style(window1, width=1.0)
drawing_commands += 1
window2 = Draft.makeLine(FreeCAD.Vector(8000, 0, 0), FreeCAD.Vector(8000, 1000, 0))
style(window2, width=1.0)
drawing_commands += 1
# Parking
parking = Draft.makeRectangle(3000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(10000, 7000, 0), FreeCAD.Rotation(0, 0, 0, 1)))
style(parking, width=2.0)
drawing_commands += 1
# Garden
garden = Draft.makeRectangle(2000, 2000, placement=FreeCAD.Placement(FreeCAD.Vector(11000, 5000, 0), FreeCAD.Rotation(0, 0, 0, 1)))
style(garden, width=2.0)
drawing_commands += 1
# === FRONT ELEVATION ===
# Facade outline
facade = Draft.makeLine(FreeCAD.Vector(0, front_y), FreeCAD.Vector(12000, front_y))
style(facade, width=3.0)
drawing_commands += 1
# Doors
door3 = Draft.makeLine(FreeCAD.Vector(0, front_y + 1000), FreeCAD.Vector(1000, front_y + 1000))
style(door3, width=1.5)
drawing_commands += 1
door4 = Draft.makeLine(FreeCAD.Vector(6000, front_y + 1000), FreeCAD.Vector(7000, front_y + 1000))
style(door4, width=1.5)
drawing_commands += 1
# Windows
window3 = Draft.makeLine(FreeCAD.Vector(2000, front_y), FreeCAD.Vector(2000, front_y + 1000))
style(window3, width=1.0)
drawing_commands += 1
window4 = Draft.makeLine(FreeCAD.Vector(8000, front_y), FreeCAD.Vector(8000, front_y + 1000))
style(window4, width=1.0)
drawing_commands += 1
# === SIDE ELEVATION ===
# Depth profile
depth = Draft.makeLine(FreeCAD.Vector(0, side_y), FreeCAD.Vector(12000, side_y))
style(depth, width=3.0)
drawing_commands += 1
# Roof line
roof = Draft.makeLine(FreeCAD.Vector(0, side_y + 2000), FreeCAD.Vector(12000, side_y + 2000))
style(roof, width=2.0)
drawing_commands += 1
# === DIMENSIONS ===
dim1 = Draft.make_linear_dimension(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(12000, 0, 0))
dim1.ViewObject.FontSize = 300
dim1.ViewObject.TextColor = (1.0, 0.0, 0.0)
dimension_count += 1
dim2 = Draft.make_linear_dimension(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 9000, 0))
dim2.ViewObject.FontSize = 300
dim2.ViewObject.TextColor = (1.0, 0.0, 0.0)
dimension_count += 1
dim3 = Draft.make_linear_dimension(FreeCAD.Vector(0, front_y), FreeCAD.Vector(12000, front_y))
dim3.ViewObject.FontSize = 300
dim3.ViewObject.TextColor = (1.0, 0.0, 0.0)
dimension_count += 1
dim4 = Draft.make_linear_dimension(FreeCAD.Vector(0, front_y), FreeCAD.Vector(0, front_y + 1000))
dim4.ViewObject.FontSize = 300
dim4.ViewObject.TextColor = (1.0, 0.0, 0.0)
dimension_count += 1
dim5 = Draft.make_linear_dimension(FreeCAD.Vector(0, side_y), FreeCAD.Vector(12000, side_y))
dim5.ViewObject.FontSize = 300
dim5.ViewObject.TextColor = (1.0, 0.0, 0.0)
dimension_count += 1
dim6 = Draft.make_linear_dimension(FreeCAD.Vector(0, side_y), FreeCAD.Vector(0, side_y + 2000))
dim6.ViewObject.FontSize = 300
dim6.ViewObject.TextColor = (1.0, 0.0, 0.0)
dimension_count += 1
dim7 = Draft.make_linear_dimension(FreeCAD.Vector(1000, 0, 0), FreeCAD.Vector(1000, 9000, 0))
dim7.ViewObject.FontSize = 300
dim7.ViewObject.TextColor = (1.0, 0.0, 0.0)
dimension_count += 1
dim8 = Draft.make_linear_dimension(FreeCAD.Vector(6000, 0, 0), FreeCAD.Vector(6000, 9000, 0))
dim8.ViewObject.FontSize = 300
dim8.ViewObject.TextColor = (1.0, 0.0, 0.0)
dimension_count += 1
# === GRID & TITLE BLOCK ===
for i in range(7):
    grid_line = Draft.makeLine(FreeCAD.Vector(i * GRID_SPACING, 0, 0), FreeCAD.Vector(i * GRID_SPACING, 9000, 0))
    grid_line.ViewObject
    grid_line.ViewObject.LineWidth = 0.4
    try:
        grid_line.ViewObject.LineStyle = "dashed"
    except AttributeError:
        pass  # LineStyle not supported on this object
    drawing_commands += 1
    label = Draft.makeText([chr(65 + i)], point=FreeCAD.Vector(i * GRID_SPACING, -500, 0))
    label.ViewObject.FontSize = 300
    label.ViewObject.TextColor = (1.0, 0.0, 0.0)
    text_count += 1
for i in range(7):
    grid_line = Draft.makeLine(FreeCAD.Vector(0, i * GRID_SPACING, 0), FreeCAD.Vector(12000, i * GRID_SPACING, 0))
    grid_line.ViewObject
    grid_line.ViewObject.LineWidth = 0.4
    try:
        grid_line.ViewObject.LineStyle = "dashed"
    except AttributeError:
        pass  # LineStyle not supported on this object
    drawing_commands += 1
    label = Draft.makeText([str(i + 1)], point=FreeCAD.Vector(-500, i * GRID_SPACING, 0))
    label.ViewObject.FontSize = 300
    label.ViewObject.TextColor = (1.0, 0.0, 0.0)
    text_count += 1
title_block = Draft.makeRectangle(3000, 500, placement=FreeCAD.Placement(FreeCAD.Vector(10000, -1000, 0), FreeCAD.Rotation(0, 0, 0, 1)))
style(title_block, width=2.0)
drawing_commands += 1
title_text = Draft.makeText(["Project: 2BHK House", "Scale: 1:100", "Sheet Number: 1", "Date: 2024-09-16"], point=FreeCAD.Vector(10100, -900, 0))
title_text.ViewObject.FontSize = 250
text_count += 1
print(f"Primitives: {drawing_commands}")
print(f"Dimensions: {dimension_count}")
print(f"Labels:     {text_count}")
doc.recompute()
if hasattr(FreeCAD, "Gui") and FreeCAD.Gui:
    try:
        FreeCAD.Gui.SendMsgToActiveView("ViewFit")
        FreeCAD.Gui.ActiveDocument.activeView().viewTop()
    except Exception:
        pass