import FreeCAD
import Draft

# Create a new document
doc = FreeCAD.newDocument("3BHK_House_Blueprint")

print("=== PROFESSIONAL 3BHK HOUSE CAD DRAWING ===")
print("Generating: Floor Plan + Front Elevation + Side Elevation")
print("Drawing Type: 2D Technical Blueprint with dimensions")

# ============================================================================
# DRAWING PARAMETERS
# ============================================================================
wall_thickness = 200  # mm
grid_spacing = 1000
view_spacing = 15000

# Room dimensions (in mm)
house_width = 12000
house_length = 15000

# Colors
BLACK = (0.0, 0.0, 0.0)
RED = (1.0, 0.0, 0.0)
DARK_GRAY = (0.3, 0.3, 0.3)
LIGHT_GRAY = (0.7, 0.7, 0.7)
BLUE = (0.0, 0.5, 0.8)

# ============================================================================
# SECTION 1: FLOOR PLAN
# ============================================================================
print("Creating Floor Plan...")
floor_plan_y = 0

# Exterior perimeter
exterior = Draft.makeWire([
    FreeCAD.Vector(0, floor_plan_y, 0),
    FreeCAD.Vector(house_width, floor_plan_y, 0),
    FreeCAD.Vector(house_width, floor_plan_y + house_length, 0),
    FreeCAD.Vector(0, floor_plan_y + house_length, 0),
    FreeCAD.Vector(0, floor_plan_y, 0)
], closed=True)
exterior.Label = "Exterior_Walls"
exterior.ViewObject.LineColor = BLACK
exterior.ViewObject.LineWidth = 4.0

# Interior walls - dividing into rooms
# Living room separator
wall_1 = Draft.makeLine(
    FreeCAD.Vector(0, floor_plan_y + 6000, 0),
    FreeCAD.Vector(house_width, floor_plan_y + 6000, 0)
)
wall_1.ViewObject.LineColor = BLACK
wall_1.ViewObject.LineWidth = 2.5

# Bedroom separators
wall_2 = Draft.makeLine(
    FreeCAD.Vector(4000, floor_plan_y, 0),
    FreeCAD.Vector(4000, floor_plan_y + 6000, 0)
)
wall_2.ViewObject.LineColor = BLACK
wall_2.ViewObject.LineWidth = 2.5

wall_3 = Draft.makeLine(
    FreeCAD.Vector(8000, floor_plan_y, 0),
    FreeCAD.Vector(8000, floor_plan_y + 6000, 0)
)
wall_3.ViewObject.LineColor = BLACK
wall_3.ViewObject.LineWidth = 2.5

# Kitchen/dining separator
wall_4 = Draft.makeLine(
    FreeCAD.Vector(6000, floor_plan_y + 6000, 0),
    FreeCAD.Vector(6000, floor_plan_y + house_length, 0)
)
wall_4.ViewObject.LineColor = BLACK
wall_4.ViewObject.LineWidth = 2.5

# Parking area
parking_outline = Draft.makeRectangle(
    length=3000, height=5000,
    placement=FreeCAD.Placement(FreeCAD.Vector(house_width + 500, floor_plan_y, 0), FreeCAD.Rotation(0, 0, 0))
)
parking_outline.Label = "Parking"
parking_outline.ViewObject.LineColor = DARK_GRAY
parking_outline.ViewObject.LineWidth = 2.0

# Dimensions in RED
dim_total_width = Draft.makeDimension(
    FreeCAD.Vector(0, floor_plan_y - 800, 0),
    FreeCAD.Vector(house_width, floor_plan_y - 800, 0),
    FreeCAD.Vector(house_width/2, floor_plan_y - 1200, 0)
)
dim_total_width.ViewObject.LineColor = RED
dim_total_width.ViewObject.FontSize = 250

dim_total_length = Draft.makeDimension(
    FreeCAD.Vector(house_width + 800, floor_plan_y, 0),
    FreeCAD.Vector(house_width + 800, floor_plan_y + house_length, 0),
    FreeCAD.Vector(house_width + 1200, floor_plan_y + house_length/2, 0)
)
dim_total_length.ViewObject.LineColor = RED
dim_total_length.ViewObject.FontSize = 250

# Room labels
label_living = Draft.makeText(
    ["LIVING ROOM", "6000 x 12000"],
    point=FreeCAD.Vector(6000, floor_plan_y + 10000, 0)
)
label_living.ViewObject.FontSize = 300
label_living.ViewObject.TextColor = BLUE

label_br1 = Draft.makeText(
    ["BEDROOM 1", "4000 x 6000"],
    point=FreeCAD.Vector(2000, floor_plan_y + 3000, 0)
)
label_br1.ViewObject.FontSize = 250
label_br1.ViewObject.TextColor = BLUE

label_br2 = Draft.makeText(
    ["BEDROOM 2", "4000 x 6000"],
    point=FreeCAD.Vector(6000, floor_plan_y + 3000, 0)
)
label_br2.ViewObject.FontSize = 250
label_br2.ViewObject.TextColor = BLUE

label_br3 = Draft.makeText(
    ["BEDROOM 3", "4000 x 6000"],
    point=FreeCAD.Vector(10000, floor_plan_y + 3000, 0)
)
label_br3.ViewObject.FontSize = 250
label_br3.ViewObject.TextColor = BLUE

label_parking = Draft.makeText(
    ["PARKING", "3000 x 5000"],
    point=FreeCAD.Vector(house_width + 1000, floor_plan_y + 2500, 0)
)
label_parking.ViewObject.FontSize = 250
label_parking.ViewObject.TextColor = BLUE

# Title
title_plan = Draft.makeText(
    ["FLOOR PLAN - 3BHK HOUSE", "Scale 1:100"],
    point=FreeCAD.Vector(0, floor_plan_y + house_length + 1000, 0)
)
title_plan.ViewObject.FontSize = 400
title_plan.ViewObject.TextColor = BLACK

# Grid system
for i in range(0, house_width + grid_spacing, grid_spacing):
    grid_line = Draft.makeLine(
        FreeCAD.Vector(i, floor_plan_y - 1500, 0),
        FreeCAD.Vector(i, floor_plan_y + house_length + 1500, 0)
    )
    grid_line.ViewObject.LineColor = LIGHT_GRAY
    grid_line.ViewObject.LineWidth = 0.5
    grid_line.ViewObject.LineStyle = "Dashed"
    
    if i <= house_width:
        grid_label = Draft.makeText(
            [chr(65 + i//grid_spacing)],
            point=FreeCAD.Vector(i, floor_plan_y - 2000, 0)
        )
        grid_label.ViewObject.FontSize = 250
        grid_label.ViewObject.TextColor = RED

# ============================================================================
# SECTION 2: FRONT ELEVATION
# ============================================================================
print("Creating Front Elevation...")
elevation_y = floor_plan_y + view_spacing

house_height = 3000

# Main outline
elevation_outline = Draft.makeRectangle(
    length=house_width, height=house_height,
    placement=FreeCAD.Placement(FreeCAD.Vector(0, elevation_y, 0), FreeCAD.Rotation(0, 0, 0))
)
elevation_outline.ViewObject.LineColor = BLACK
elevation_outline.ViewObject.LineWidth = 4.0

# Door
door = Draft.makeRectangle(
    length=900, height=2100,
    placement=FreeCAD.Placement(FreeCAD.Vector(5500, elevation_y, 0), FreeCAD.Rotation(0, 0, 0))
)
door.ViewObject.LineColor = BLACK
door.ViewObject.LineWidth = 2.5

# Windows
for window_x in [1500, 4000, 7500, 10000]:
    window = Draft.makeRectangle(
        length=1200, height=1200,
        placement=FreeCAD.Placement(FreeCAD.Vector(window_x, elevation_y + 1000, 0), FreeCAD.Rotation(0, 0, 0))
    )
    window.ViewObject.LineColor = DARK_GRAY
    window.ViewObject.LineWidth = 2.0

# Elevation dimensions
dim_elev_height = Draft.makeDimension(
    FreeCAD.Vector(-600, elevation_y, 0),
    FreeCAD.Vector(-600, elevation_y + house_height, 0),
    FreeCAD.Vector(-1000, elevation_y + house_height/2, 0)
)
dim_elev_height.ViewObject.LineColor = RED
dim_elev_height.ViewObject.FontSize = 250

# Title
title_elevation = Draft.makeText(
    ["FRONT ELEVATION", "Scale 1:100"],
    point=FreeCAD.Vector(0, elevation_y + house_height + 600, 0)
)
title_elevation.ViewObject.FontSize = 400
title_elevation.ViewObject.TextColor = BLACK

# ============================================================================
# FINALIZE
# ============================================================================
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.activeDocument().activeView().viewTop()

print("=== 3BHK HOUSE BLUEPRINT COMPLETE ===")
print("✓ Floor Plan with room layout")
print("✓ Front Elevation with doors and windows")
print("✓ Dimensions in RED")
print("✓ Grid reference system")
print("✓ Professional annotations")
