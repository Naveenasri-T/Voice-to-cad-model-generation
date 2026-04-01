import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
import FreeCAD
import Draft
doc = FreeCAD.newDocument("Computer_Laboratory_Blueprint")
# === FRONT VIEW (y_offset = 0) ===
# Perimeter outline
front_outline = Draft.makeWire([
    FreeCAD.Vector(0, 0, 0),
    FreeCAD.Vector(12000, 0, 0),
    FreeCAD.Vector(12000, 3600, 0),
    FreeCAD.Vector(0, 3600, 0),
    FreeCAD.Vector(0, 0, 0)
], closed=True)
front_outline.ViewObject.LineWidth = 3.0
# Internal details (doors, windows, compartments)
door1 = Draft.makeLine(FreeCAD.Vector(1000, 0, 0), FreeCAD.Vector(1900, 0, 0))
door1.ViewObject.LineWidth = 2.0
window1 = Draft.makeRectangle(800, 1200, placement=FreeCAD.Placement(FreeCAD.Vector(3000, 1000, 0), FreeCAD.Rotation(0, 0, 0)))
window1.ViewObject.LineWidth = 1.5
# Server room outline
server_room = Draft.makeWire([
    FreeCAD.Vector(9000, 0, 0),
    FreeCAD.Vector(12000, 0, 0),
    FreeCAD.Vector(12000, 1200, 0),
    FreeCAD.Vector(9000, 1200, 0),
    FreeCAD.Vector(9000, 0, 0)
], closed=True)
server_room.ViewObject.LineWidth = 2.0
# Instructor area outline
instructor_area = Draft.makeWire([
    FreeCAD.Vector(0, 2400, 0),
    FreeCAD.Vector(3000, 2400, 0),
    FreeCAD.Vector(3000, 3600, 0),
    FreeCAD.Vector(0, 3600, 0),
    FreeCAD.Vector(0, 2400, 0)
], closed=True)
instructor_area.ViewObject.LineWidth = 2.0
# Storage room outline
storage_room = Draft.makeWire([
    FreeCAD.Vector(3000, 2400, 0),
    FreeCAD.Vector(4500, 2400, 0),
    FreeCAD.Vector(4500, 3600, 0),
    FreeCAD.Vector(3000, 3600, 0),
    FreeCAD.Vector(3000, 2400, 0)
], closed=True)
storage_room.ViewObject.LineWidth = 2.0
# Dimensions - MODERN API (FreeCAD 0.21+)
dim1 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, -500, 0),
    FreeCAD.Vector(12000, -500, 0)
)
dim1.ViewObject.FontSize = 300
dim2 = Draft.make_linear_dimension(
    FreeCAD.Vector(-500, 0, 0),
    FreeCAD.Vector(-500, 3600, 0)
)
dim2.ViewObject.FontSize = 300
# Labels
label_server_room = Draft.makeText(["Server Room"], point=FreeCAD.Vector(10000, 600, 0))
label_server_room.ViewObject.FontSize = 200
label_server_room.ViewObject.TextColor = (0.0, 0.0, 0.0)
label_instructor_area = Draft.makeText(["Instructor Area"], point=FreeCAD.Vector(1500, 2700, 0))
label_instructor_area.ViewObject.FontSize = 200
label_instructor_area.ViewObject.TextColor = (0.0, 0.0, 0.0)
label_storage_room = Draft.makeText(["Storage Room"], point=FreeCAD.Vector(3750, 2700, 0))
label_storage_room.ViewObject.FontSize = 200
label_storage_room.ViewObject.TextColor = (0.0, 0.0, 0.0)
# === TOP VIEW (y_offset = 10000) ===
# Floor plan with rooms, furniture, fixtures
top_outline = Draft.makeWire([
    FreeCAD.Vector(0, 10000, 0),
    FreeCAD.Vector(12000, 10000, 0),
    FreeCAD.Vector(12000, 13600, 0),
    FreeCAD.Vector(0, 13600, 0),
    FreeCAD.Vector(0, 10000, 0)
], closed=True)
top_outline.ViewObject.LineWidth = 3.0
# Student workstations
for i in range(40):
    workstation = Draft.makeRectangle(800, 600, placement=FreeCAD.Placement(FreeCAD.Vector(200 + (i % 10) * 1000, 11000 + (i // 10) * 800, 0), FreeCAD.Rotation(0, 0, 0)))
    workstation.ViewObject.LineWidth = 1.0
# Instructor desk
instructor_desk = Draft.makeRectangle(1200, 800, placement=FreeCAD.Placement(FreeCAD.Vector(3000, 13000, 0), FreeCAD.Rotation(0, 0, 0)))
instructor_desk.ViewObject.LineWidth = 2.0
# Storage shelves
storage_shelf = Draft.makeRectangle(800, 1200, placement=FreeCAD.Placement(FreeCAD.Vector(3500, 13000, 0), FreeCAD.Rotation(0, 0, 0)))
storage_shelf.ViewObject.LineWidth = 1.5
# Dimensions
dim3 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 10000 - 500, 0),
    FreeCAD.Vector(12000, 10000 - 500, 0)
)
dim3.ViewObject.FontSize = 300
dim4 = Draft.make_linear_dimension(
    FreeCAD.Vector(-500, 10000, 0),
    FreeCAD.Vector(-500, 13600, 0)
)
dim4.ViewObject.FontSize = 300
# Labels
label_student_workstations = Draft.makeText(["Student Workstations"], point=FreeCAD.Vector(6000, 12500, 0))
label_student_workstations.ViewObject.FontSize = 200
label_student_workstations.ViewObject.TextColor = (0.0, 0.0, 0.0)
label_instructor_desk = Draft.makeText(["Instructor Desk"], point=FreeCAD.Vector(3300, 13500, 0))
label_instructor_desk.ViewObject.FontSize = 200
label_instructor_desk.ViewObject.TextColor = (0.0, 0.0, 0.0)
label_storage_shelf = Draft.makeText(["Storage Shelf"], point=FreeCAD.Vector(3800, 13500, 0))
label_storage_shelf.ViewObject.FontSize = 200
label_storage_shelf.ViewObject.TextColor = (0.0, 0.0, 0.0)
# === SIDE VIEW (y_offset = 20000) ===
# Profile projection showing depth
side_outline = Draft.makeWire([
    FreeCAD.Vector(0, 20000, 0),
    FreeCAD.Vector(12000, 20000, 0),
    FreeCAD.Vector(12000, 23600, 0),
    FreeCAD.Vector(0, 23600, 0),
    FreeCAD.Vector(0, 20000, 0)
], closed=True)
side_outline.ViewObject.LineWidth = 3.0
# Server room depth
server_room_depth = Draft.makeLine(FreeCAD.Vector(9000, 20000, 0), FreeCAD.Vector(9000, 21200, 0))
server_room_depth.ViewObject.LineWidth = 2.0
# Instructor area depth
instructor_area_depth = Draft.makeLine(FreeCAD.Vector(0, 22400, 0), FreeCAD.Vector(0, 23600, 0))
instructor_area_depth.ViewObject.LineWidth = 2.0
# Storage room depth
storage_room_depth = Draft.makeLine(FreeCAD.Vector(3000, 22400, 0), FreeCAD.Vector(3000, 23600, 0))
storage_room_depth.ViewObject.LineWidth = 2.0
# Dimensions
dim5 = Draft.make_linear_dimension(
    FreeCAD.Vector(0, 20000 - 500, 0),
    FreeCAD.Vector(12000, 20000 - 500, 0)
)
dim5.ViewObject.FontSize = 300
dim6 = Draft.make_linear_dimension(
    FreeCAD.Vector(-500, 20000, 0),
    FreeCAD.Vector(-500, 23600, 0)
)
dim6.ViewObject.FontSize = 300
# Labels
label_server_room_depth = Draft.makeText(["Server Room Depth"], point=FreeCAD.Vector(9500, 20600, 0))
label_server_room_depth.ViewObject.FontSize = 200
label_server_room_depth.ViewObject.TextColor = (0.0, 0.0, 0.0)
label_instructor_area_depth = Draft.makeText(["Instructor Area Depth"], point=FreeCAD.Vector(500, 22800, 0))
label_instructor_area_depth.ViewObject.FontSize = 200
label_instructor_area_depth.ViewObject.TextColor = (0.0, 0.0, 0.0)
label_storage_room_depth = Draft.makeText(["Storage Room Depth"], point=FreeCAD.Vector(3500, 22800, 0))
label_storage_room_depth.ViewObject.FontSize = 200
label_storage_room_depth.ViewObject.TextColor = (0.0, 0.0, 0.0)
# === GRID SYSTEM ===
# Grid lines every 1000mm with A,B,C labels
for i in range(7):
    grid_line = Draft.makeLine(FreeCAD.Vector(0, i * 1000, 0), FreeCAD.Vector(12000, i * 1000, 0))
    grid_line.ViewObject.LineWidth = 0.5
    try:
        grid_line.ViewObject.LineStyle = "Dashed"
    except AttributeError:
        pass  # LineStyle not supported on this object
    label = Draft.makeText([chr(65 + i)], point=FreeCAD.Vector(-500, i * 1000, 0))
    label.ViewObject.FontSize = 200
    label.ViewObject.TextColor = (0.0, 0.0, 0.0)
for i in range(13):
    grid_line = Draft.makeLine(FreeCAD.Vector(i * 1000, 0, 0), FreeCAD.Vector(i * 1000, 3600, 0))
    grid_line.ViewObject.LineWidth = 0.5
    try:
        grid_line.ViewObject.LineStyle = "Dashed"
    except AttributeError:
        pass  # LineStyle not supported on this object
    label = Draft.makeText([str(i)], point=FreeCAD.Vector(i * 1000, -500, 0))
    label.ViewObject.FontSize = 200
    label.ViewObject.TextColor = (0.0, 0.0, 0.0)
# === TITLE BLOCK ===
# Drawing name, scale, date
title_block = Draft.makeText(["Computer Laboratory Blueprint", "Scale: 1:100", "Date: 2024-09-16"], point=FreeCAD.Vector(10000, -1000, 0))
title_block.ViewObject.FontSize = 200
title_block.ViewObject.TextColor = (0.0, 0.0, 0.0)
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.activeDocument().activeView().viewTop()
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
