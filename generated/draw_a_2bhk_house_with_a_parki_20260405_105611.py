import FreeCAD
import Draft
print("=== 2 Bedroom Hall Kitchen Apartment ===")
print("Scope: Create a professional 2BHK apartment model")
doc = FreeCAD.newDocument("2BHK_Apartment_Model")
GRID_SPACING = 1000
VIEW_SPACING = 15000        # vertical gap between plan / front / side
plan_y   = 0
front_y  = VIEW_SPACING
side_y   = 2 * VIEW_SPACING
drawing_commands = 0
dimension_count  = 0
text_count       = 0
def style(obj, width=2.0, color=(0.0, 0.0, 0.0)):
    if hasattr(obj, "ViewObject"):
        obj.ViewObject.LineWidth = width
        obj.ViewObject
# ── PLAN VIEW ────────────────────────────────────────────────
# exterior boundary, partitions, openings, furniture footprints,
# swing arcs, fixtures, room-area labels, north arrow + scale text
# Living Room
living_room = Draft.makeRectangle(4671, 6422, placement=FreeCAD.Placement(FreeCAD.Vector(0, 0, plan_y)))
style(living_room, width=3.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
living_room_label = Draft.makeText("Living Room", placement=FreeCAD.Placement(FreeCAD.Vector(1000, 1000, plan_y)))
style(living_room_label, width=2.0, color=(0.0, 0.0, 0.0))
text_count += 1
# Master Bedroom
master_bedroom = Draft.makeRectangle(4321, 5554, placement=FreeCAD.Placement(FreeCAD.Vector(7000, 0, plan_y)))
style(master_bedroom, width=3.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
master_bedroom_label = Draft.makeText("Master Bedroom", placement=FreeCAD.Placement(FreeCAD.Vector(8000, 1000, plan_y)))
style(master_bedroom_label, width=2.0, color=(0.0, 0.0, 0.0))
text_count += 1
# Second Bedroom
second_bedroom = Draft.makeRectangle(3674, 4898, placement=FreeCAD.Placement(FreeCAD.Vector(12000, 0, plan_y)))
style(second_bedroom, width=3.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
second_bedroom_label = Draft.makeText("Second Bedroom", placement=FreeCAD.Placement(FreeCAD.Vector(13000, 1000, plan_y)))
style(second_bedroom_label, width=2.0, color=(0.0, 0.0, 0.0))
text_count += 1
# Kitchen
kitchen = Draft.makeRectangle(3162, 3794, placement=FreeCAD.Placement(FreeCAD.Vector(16000, 0, plan_y)))
style(kitchen, width=3.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
kitchen_label = Draft.makeText("Kitchen", placement=FreeCAD.Placement(FreeCAD.Vector(17000, 1000, plan_y)))
style(kitchen_label, width=2.0, color=(0.0, 0.0, 0.0))
text_count += 1
# Bathroom
bathroom = Draft.makeRectangle(2771, 3464, placement=FreeCAD.Placement(FreeCAD.Vector(19000, 0, plan_y)))
style(bathroom, width=3.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
bathroom_label = Draft.makeText("Bathroom", placement=FreeCAD.Placement(FreeCAD.Vector(20000, 1000, plan_y)))
style(bathroom_label, width=2.0, color=(0.0, 0.0, 0.0))
text_count += 1
# Dining
dining = Draft.makeRectangle(3513, 4098, placement=FreeCAD.Placement(FreeCAD.Vector(21000, 0, plan_y)))
style(dining, width=3.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
dining_label = Draft.makeText("Dining", placement=FreeCAD.Placement(FreeCAD.Vector(22000, 1000, plan_y)))
style(dining_label, width=2.0, color=(0.0, 0.0, 0.0))
text_count += 1
# Balcony
balcony = Draft.makeRectangle(2530, 3794, placement=FreeCAD.Placement(FreeCAD.Vector(23000, 0, plan_y)))
style(balcony, width=3.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
balcony_label = Draft.makeText("Balcony", placement=FreeCAD.Placement(FreeCAD.Vector(24000, 1000, plan_y)))
style(balcony_label, width=2.0, color=(0.0, 0.0, 0.0))
text_count += 1
# Doors
door1 = Draft.makeLine(FreeCAD.Vector(1000, 0, plan_y), FreeCAD.Vector(1000, 2100, plan_y))
style(door1, width=2.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
door2 = Draft.makeLine(FreeCAD.Vector(8000, 0, plan_y), FreeCAD.Vector(8000, 2100, plan_y))
style(door2, width=2.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
door3 = Draft.makeLine(FreeCAD.Vector(13000, 0, plan_y), FreeCAD.Vector(13000, 2100, plan_y))
style(door3, width=2.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
door4 = Draft.makeLine(FreeCAD.Vector(17000, 0, plan_y), FreeCAD.Vector(17000, 2100, plan_y))
style(door4, width=2.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
door5 = Draft.makeLine(FreeCAD.Vector(20000, 0, plan_y), FreeCAD.Vector(20000, 2100, plan_y))
style(door5, width=2.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
door6 = Draft.makeLine(FreeCAD.Vector(22000, 0, plan_y), FreeCAD.Vector(22000, 2100, plan_y))
style(door6, width=2.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
door7 = Draft.makeLine(FreeCAD.Vector(24000, 0, plan_y), FreeCAD.Vector(24000, 2100, plan_y))
style(door7, width=2.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
# Windows
window1 = Draft.makeLine(FreeCAD.Vector(1000, 3000, plan_y), FreeCAD.Vector(1000, 4200, plan_y))
style(window1, width=2.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
window2 = Draft.makeLine(FreeCAD.Vector(8000, 3000, plan_y), FreeCAD.Vector(8000, 4200, plan_y))
style(window2, width=2.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
window3 = Draft.makeLine(FreeCAD.Vector(13000, 3000, plan_y), FreeCAD.Vector(13000, 4200, plan_y))
style(window3, width=2.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
window4 = Draft.makeLine(FreeCAD.Vector(17000, 3000, plan_y), FreeCAD.Vector(17000, 4200, plan_y))
style(window4, width=2.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
window5 = Draft.makeLine(FreeCAD.Vector(20000, 3000, plan_y), FreeCAD.Vector(20000, 4200, plan_y))
style(window5, width=2.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
window6 = Draft.makeLine(FreeCAD.Vector(22000, 3000, plan_y), FreeCAD.Vector(22000, 4200, plan_y))
style(window6, width=2.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
window7 = Draft.makeLine(FreeCAD.Vector(24000, 3000, plan_y), FreeCAD.Vector(24000, 4200, plan_y))
style(window7, width=2.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
# ── FRONT ELEVATION ──────────────────────────────────────────
# facade outline, doors/windows, panel joints, height markers,
# parapet / roof line, exterior material notes
# Front Elevation
front_elevation = Draft.makeRectangle(30000, 10000, placement=FreeCAD.Placement(FreeCAD.Vector(0, 0, front_y)))
style(front_elevation, width=3.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
front_elevation_label = Draft.makeText("Front Elevation", placement=FreeCAD.Placement(FreeCAD.Vector(1000, 1000, front_y)))
style(front_elevation_label, width=2.0, color=(0.0, 0.0, 0.0))
text_count += 1
# ── SIDE / SECTION ELEVATION ─────────────────────────────────
# depth profile, floor-to-ceiling heights, roof pitch,
# cut hatching (repeated Draft.makeLine), ceiling/beam notes
# Side Elevation
side_elevation = Draft.makeRectangle(30000, 10000, placement=FreeCAD.Placement(FreeCAD.Vector(0, 0, side_y)))
style(side_elevation, width=3.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
side_elevation_label = Draft.makeText("Side Elevation", placement=FreeCAD.Placement(FreeCAD.Vector(1000, 1000, side_y)))
style(side_elevation_label, width=2.0, color=(0.0, 0.0, 0.0))
text_count += 1
# ── DIMENSION PACKAGE ────────────────────────────────────────
# Use Draft.make_linear_dimension(start_vec, end_vec) ONLY
# Dimensions
dimension1 = Draft.make_linear_dimension(FreeCAD.Vector(0, 0, plan_y), FreeCAD.Vector(1000, 0, plan_y))
style(dimension1, width=2.0, color=(1.0, 0.0, 0.0))
dimension_count += 1
dimension2 = Draft.make_linear_dimension(FreeCAD.Vector(1000, 0, plan_y), FreeCAD.Vector(2000, 0, plan_y))
style(dimension2, width=2.0, color=(1.0, 0.0, 0.0))
dimension_count += 1
dimension3 = Draft.make_linear_dimension(FreeCAD.Vector(2000, 0, plan_y), FreeCAD.Vector(3000, 0, plan_y))
style(dimension3, width=2.0, color=(1.0, 0.0, 0.0))
dimension_count += 1
dimension4 = Draft.make_linear_dimension(FreeCAD.Vector(3000, 0, plan_y), FreeCAD.Vector(4000, 0, plan_y))
style(dimension4, width=2.0, color=(1.0, 0.0, 0.0))
dimension_count += 1
dimension5 = Draft.make_linear_dimension(FreeCAD.Vector(4000, 0, plan_y), FreeCAD.Vector(5000, 0, plan_y))
style(dimension5, width=2.0, color=(1.0, 0.0, 0.0))
dimension_count += 1
dimension6 = Draft.make_linear_dimension(FreeCAD.Vector(5000, 0, plan_y), FreeCAD.Vector(6000, 0, plan_y))
style(dimension6, width=2.0, color=(1.0, 0.0, 0.0))
dimension_count += 1
dimension7 = Draft.make_linear_dimension(FreeCAD.Vector(6000, 0, plan_y), FreeCAD.Vector(7000, 0, plan_y))
style(dimension7, width=2.0, color=(1.0, 0.0, 0.0))
dimension_count += 1
dimension8 = Draft.make_linear_dimension(FreeCAD.Vector(7000, 0, plan_y), FreeCAD.Vector(8000, 0, plan_y))
style(dimension8, width=2.0, color=(1.0, 0.0, 0.0))
dimension_count += 1
# ── GRID SYSTEM ──────────────────────────────────────────────
# Loop columns A–F and rows 1–6 across the full drawing height
# Grid System
for i in range(6):
    for j in range(6):
        grid_line = Draft.makeLine(FreeCAD.Vector(j * GRID_SPACING, i * GRID_SPACING, plan_y), FreeCAD.Vector((j + 1) * GRID_SPACING, i * GRID_SPACING, plan_y))
        style(grid_line, width=0.4, color=(0.7, 0.7, 0.7))
        drawing_commands += 1
        grid_line = Draft.makeLine(FreeCAD.Vector(j * GRID_SPACING, i * GRID_SPACING, plan_y), FreeCAD.Vector(j * GRID_SPACING, (i + 1) * GRID_SPACING, plan_y))
        style(grid_line, width=0.4, color=(0.7, 0.7, 0.7))
        drawing_commands += 1
# ── TITLE BLOCK ──────────────────────────────────────────────
# Draft.makeRectangle for border + Draft.makeText for content
# Title Block
title_block = Draft.makeRectangle(10000, 5000, placement=FreeCAD.Placement(FreeCAD.Vector(25000, 0, plan_y)))
style(title_block, width=3.0, color=(0.0, 0.0, 0.0))
drawing_commands += 1
title_block_label = Draft.makeText("2BHK Apartment Model", placement=FreeCAD.Placement(FreeCAD.Vector(26000, 1000, plan_y)))
style(title_block_label, width=2.0, color=(0.0, 0.0, 0.0))
text_count += 1
scale_text = Draft.makeText("Scale: 1:100", placement=FreeCAD.Placement(FreeCAD.Vector(26000, 2000, plan_y)))
style(scale_text, width=2.0, color=(0.0, 0.0, 0.0))
text_count += 1
date_text = Draft.makeText("Date: 2024-09-16", placement=FreeCAD.Placement(FreeCAD.Vector(26000, 3000, plan_y)))
style(date_text, width=2.0, color=(0.0, 0.0, 0.0))
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