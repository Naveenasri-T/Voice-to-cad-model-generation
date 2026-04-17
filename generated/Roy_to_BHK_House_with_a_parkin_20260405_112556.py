
import FreeCAD
import Draft

doc = FreeCAD.newDocument("Roy_to_BHK_House_with_a_parking_and_wate")
REQUEST_SUMMARY = "Roy to BHK House with a parking and water."

print("=== 2BHK HOUSE BLUEPRINT ===")
print(f"Request: {REQUEST_SUMMARY}")

# ─── DIMENSIONS (mm) ──────────────────────────────────────────
HOUSE_W  = 10500
HOUSE_D  = 8500
VIEW_GAP = 16000
PLAN_Y   = 0
FRONT_Y  = VIEW_GAP
SIDE_Y   = VIEW_GAP * 2
drawing_commands = 0
dimension_count  = 0
text_count       = 0

# ─── HELPERS ──────────────────────────────────────────────────
def S(obj, w=2.0, c=(0.0, 0.0, 0.0)):
    if hasattr(obj, "ViewObject"):
        obj.ViewObject.LineWidth = w
        obj.ViewObject.LineColor = c

def wall(x1, y1, x2, y2, w=2.0):
    global drawing_commands
    ln = Draft.makeLine(FreeCAD.Vector(x1, y1, 0), FreeCAD.Vector(x2, y2, 0))
    S(ln, w)
    drawing_commands += 1
    return ln

def room_box(x, y, w, d, lw=2.0):
    global drawing_commands
    r = Draft.makeRectangle(
        length=w, height=d,
        placement=FreeCAD.Placement(FreeCAD.Vector(x, y, 0), FreeCAD.Rotation(0, 0, 0))
    )
    S(r, lw)
    drawing_commands += 1
    return r

def lbl(texts, x, y, size=280, color=(0.0, 0.0, 0.0)):
    global text_count
    t = Draft.makeText(texts, point=FreeCAD.Vector(x, y, 0))
    t.ViewObject.FontSize = size
    t.ViewObject.TextColor = color
    text_count += 1
    return t

def dim(x1, y1, x2, y2):
    global dimension_count
    d = Draft.make_linear_dimension(FreeCAD.Vector(x1, y1, 0), FreeCAD.Vector(x2, y2, 0))
    d.ViewObject.FontSize = 260
    d.ViewObject.TextColor = (1.0, 0.0, 0.0)
    d.ViewObject.LineColor = (0.0, 0.0, 0.0)
    dimension_count += 1
    return d

def door_arc(cx, cy, r, a1, a2):
    global drawing_commands
    arc = Draft.makeCircle(radius=r,
        placement=FreeCAD.Placement(FreeCAD.Vector(cx, cy, 0), FreeCAD.Rotation(0, 0, 0)),
        startangle=a1, endangle=a2)
    S(arc, 0.8)
    drawing_commands += 1
    return arc

def win(x, y, length, horiz=True):
    global drawing_commands
    if horiz:
        wall(x, y-60, x+length, y-60, 1.0)
        wall(x, y,    x+length, y,    1.8)
        wall(x, y+60, x+length, y+60, 1.0)
    else:
        wall(x-60, y, x-60, y+length, 1.0)
        wall(x,    y, x,    y+length, 1.8)
        wall(x+60, y, x+60, y+length, 1.0)

# ═════════════════════════════════════════════════════════════
#  FLOOR PLAN  (Plan View – top-down)
# ═════════════════════════════════════════════════════════════
print("Drawing Floor Plan...")

# Outer boundary
ext = room_box(0, PLAN_Y, HOUSE_W, HOUSE_D, 3.5)
ext.Label = "Exterior_Boundary"

# ─── Interior wall lines ──────────────────────────────────────
# Vertical spine (separates living zone from bedroom zone)
wall(6000, PLAN_Y, 6000, PLAN_Y + HOUSE_D, 2.2).Label = "Spine_Wall"
# Horizontal band (front half vs rear half)
wall(0, PLAN_Y + 4500, HOUSE_W, PLAN_Y + 4500, 2.2).Label = "Mid_Wall"
# Kitchen east wall
wall(3500, PLAN_Y + 4500, 3500, PLAN_Y + HOUSE_D, 2.0).Label = "Kitchen_E_Wall"
# Bathroom divider (splits bath from toilet)
wall(3500, PLAN_Y + 6400, 6000, PLAN_Y + 6400, 2.0).Label = "Bath_Divider"
# Corridor wall (service area)
wall(9000, PLAN_Y + 4500, 9000, PLAN_Y + HOUSE_D, 2.0).Label = "Corridor_Wall"

# ─── WINDOWS ─────────────────────────────────────────────────
# South face (front)
win(700,  PLAN_Y, 1400, True)
win(2500, PLAN_Y, 1200, True)
win(7000, PLAN_Y, 1600, True)
# North face (rear)
win(400,  PLAN_Y + HOUSE_D, 1200, True)
win(2200, PLAN_Y + HOUSE_D, 1000, True)
win(6500, PLAN_Y + HOUSE_D, 1200, True)
win(9200, PLAN_Y + HOUSE_D, 900,  True)
# East face (side)
win(HOUSE_W, PLAN_Y + 1500, 1200, False)
win(HOUSE_W, PLAN_Y + 5500, 1200, False)

# ─── DOORS ───────────────────────────────────────────────────
# Main entrance (front wall, x=4700)
wall(4700, PLAN_Y, 5600, PLAN_Y, 0.4)  # opening gap
door_arc(4700, PLAN_Y, 900, 0, 90)
lbl(["D1"], 4700, PLAN_Y - 400, size=200)

# Living to corridor (spine wall, y=1500-2300)
wall(6000, PLAN_Y + 1500, 6000, PLAN_Y + 2300, 0.4)
door_arc(6000, PLAN_Y + 2300, 800, 180, 270)
lbl(["D2"], 6200, PLAN_Y + 1800, size=200)

# Kitchen door (mid wall, x=2000-2700)
wall(2000, PLAN_Y + 4500, 2700, PLAN_Y + 4500, 0.4)
door_arc(2000, PLAN_Y + 4500, 700, 270, 360)
lbl(["D3"], 2100, PLAN_Y + 4700, size=200)

# Bed2 door (kitchen east wall, y=5200-5900)
wall(3500, PLAN_Y + 5200, 3500, PLAN_Y + 5900, 0.4)
door_arc(3500, PLAN_Y + 5200, 700, 0, 90)
lbl(["D4"], 3700, PLAN_Y + 5400, size=200)

# Bathroom door
wall(3500, PLAN_Y + 6600, 3500, PLAN_Y + 7200, 0.4)
door_arc(3500, PLAN_Y + 6600, 600, 0, 90)
lbl(["D5"], 3700, PLAN_Y + 6800, size=200)

# Toilet door
wall(4400, PLAN_Y + 6400, 5000, PLAN_Y + 6400, 0.4)
door_arc(4400, PLAN_Y + 6400, 600, 270, 360)
lbl(["D6"], 4500, PLAN_Y + 6600, size=200)

# ─── FURNITURE ───────────────────────────────────────────────
room_box(350,  PLAN_Y + 2800, 2800, 800, 1.0).Label = "Sofa"
room_box(350,  PLAN_Y + 200,  1200, 700, 1.0).Label = "TV_Unit"
room_box(3200, PLAN_Y + 1800, 1800, 1200, 1.0).Label = "Dining_Table"
room_box(6300, PLAN_Y + 600,  2200, 1800, 1.0).Label = "Master_Bed"
room_box(8800, PLAN_Y + 300,  600,  2000, 1.0).Label = "Wardrobe"
room_box(6400, PLAN_Y + 5200, 2000, 1600, 1.0).Label = "Bed2"
room_box(200,  PLAN_Y + 4700, 3100, 600, 1.0).Label = "Kitchen_Counter"
room_box(200,  PLAN_Y + 5300, 600,  2900, 1.0).Label = "Pantry"

# ─── ROOM LABELS ─────────────────────────────────────────────
lbl(["LIVING ROOM",   "6.0 x 4.5 m"],   1000, PLAN_Y + 2200, size=300)
lbl(["DINING AREA",   "3.5 x 2.5 m"],   3300, PLAN_Y + 3200, size=280)
lbl(["MASTER BED",    "4.5 x 4.5 m"],   6500, PLAN_Y + 2000, size=300)
lbl(["BEDROOM 2",     "5.5 x 4.0 m"],   6400, PLAN_Y + 6000, size=300)
lbl(["KITCHEN",       "3.5 x 4.0 m"],    500, PLAN_Y + 5800, size=280)
lbl(["BATHROOM"],                        3700, PLAN_Y + 5300, size=260)
lbl(["TOILET"],                          3700, PLAN_Y + 7000, size=260)
lbl(["STORE"],                           9100, PLAN_Y + 5500, size=260)
lbl(["FLOOR PLAN", "Scale 1:100"],       0,    PLAN_Y + HOUSE_D + 700, size=340)
lbl(["N ↑"],  HOUSE_W + 900, PLAN_Y + HOUSE_D / 2, size=450, color=(0.0, 0.4, 0.8))

# ─── PLAN DIMENSIONS ─────────────────────────────────────────
dim(0,         PLAN_Y - 1500, HOUSE_W, PLAN_Y - 1500)   # total width
dim(-1500,     PLAN_Y,        -1500,   PLAN_Y + HOUSE_D) # total depth
dim(0,         PLAN_Y - 700,  6000,   PLAN_Y - 700)      # living zone W
dim(6000,      PLAN_Y - 700,  HOUSE_W,PLAN_Y - 700)      # bed zone W
dim(HOUSE_W+700, PLAN_Y, HOUSE_W+700, PLAN_Y+4500)       # front depth
dim(HOUSE_W+700, PLAN_Y+4500, HOUSE_W+700, PLAN_Y+HOUSE_D) # rear depth
dim(0,         PLAN_Y + HOUSE_D + 300, 3500, PLAN_Y + HOUSE_D + 300) # kitchen W
dim(3500,      PLAN_Y + HOUSE_D + 300, 6000, PLAN_Y + HOUSE_D + 300) # bath zone W

# ═════════════════════════════════════════════════════════════
#  FRONT ELEVATION
# ═════════════════════════════════════════════════════════════
print("Drawing Front Elevation...")

room_box(0, FRONT_Y, HOUSE_W, 3000, 3.0).Label = "Front_Elev"
wall(0, FRONT_Y - 250, HOUSE_W, FRONT_Y - 250, 3.0)   # ground line
wall(0, FRONT_Y + 450, HOUSE_W, FRONT_Y + 450, 1.5)   # plinth band
wall(0, FRONT_Y + 2200, HOUSE_W, FRONT_Y + 2200, 1.5) # lintel band
room_box(0, FRONT_Y + 3000, HOUSE_W, 400, 1.5).Label = "Parapet"

# Doors & windows on front face
room_box(4700, FRONT_Y + 450, 900, 1850, 1.5).Label = "Main_Door"
wall(5150, FRONT_Y + 450, 5150, FRONT_Y + 2300, 0.8)

for wx, ww in [(700, 1400), (2400, 1200), (6800, 1600), (9100, 900)]:
    room_box(wx, FRONT_Y + 900, ww, 1200, 1.5)

# Column marks (structural)
for cx in [0, 3500, 6000, 9000, HOUSE_W]:
    wall(cx - 75, FRONT_Y, cx + 75, FRONT_Y, 2.5)
    wall(cx, FRONT_Y, cx, FRONT_Y + 3000, 0.8)

lbl(["FRONT ELEVATION", "Scale 1:100"], 0, FRONT_Y + 3600, size=340)
dim(0,    FRONT_Y - 900, HOUSE_W, FRONT_Y - 900)
dim(-1200, FRONT_Y, -1200, FRONT_Y + 450)
dim(-1200, FRONT_Y + 450, -1200, FRONT_Y + 2200)
dim(-1200, FRONT_Y + 2200, -1200, FRONT_Y + 3400)

# ═════════════════════════════════════════════════════════════
#  SIDE ELEVATION  (East face)
# ═════════════════════════════════════════════════════════════
print("Drawing Side Elevation...")

room_box(0, SIDE_Y, HOUSE_D, 3000, 3.0).Label = "Side_Elev"
wall(0, SIDE_Y - 250, HOUSE_D, SIDE_Y - 250, 3.0)
wall(0, SIDE_Y + 450, HOUSE_D, SIDE_Y + 450, 1.5)
wall(0, SIDE_Y + 2200, HOUSE_D, SIDE_Y + 2200, 1.5)
room_box(0, SIDE_Y + 3000, HOUSE_D, 400, 1.5).Label = "Side_Parapet"

# Section hatching (cut surface)
for hx in range(0, 900, 200):
    wall(hx, SIDE_Y, hx + 100, SIDE_Y + 150, 0.4)
    wall(hx, SIDE_Y + 3000 - 150, hx + 100, SIDE_Y + 3000, 0.4)

for wx, ww in [(800, 1200), (3600, 1200), (5400, 1200), (7000, 900)]:
    room_box(wx, SIDE_Y + 900, ww, 1100, 1.5)

# Floor slabs (horizontal line markers)
wall(0, SIDE_Y + 450, HOUSE_D, SIDE_Y + 450, 1.0)

lbl(["SIDE / SECTION ELEVATION", "Scale 1:100"], 0, SIDE_Y + 3700, size=340)
dim(0,       SIDE_Y - 900, HOUSE_D, SIDE_Y - 900)
dim(-1200,   SIDE_Y, -1200, SIDE_Y + 3400)
dim(-700,    SIDE_Y, -700,  SIDE_Y + 450)

# ═════════════════════════════════════════════════════════════
#  COORDINATE GRID
# ═════════════════════════════════════════════════════════════
GRID_BOT = PLAN_Y - 2800
GRID_TOP = SIDE_Y + 4800
GRID_LEFT  = -2500
GRID_RIGHT = HOUSE_W + 2500

for ci, letter in enumerate("ABCDEFGHIJ"):
    gx = ci * 1200
    if gx > HOUSE_W + 500:
        break
    gl = Draft.makeLine(FreeCAD.Vector(gx, GRID_BOT, 0), FreeCAD.Vector(gx, GRID_TOP, 0))
    S(gl, 0.3, (0.75, 0.75, 0.75))
    drawing_commands += 1
    t = Draft.makeText([letter], point=FreeCAD.Vector(gx - 100, GRID_BOT - 700, 0))
    t.ViewObject.FontSize = 240
    t.ViewObject.TextColor = (0.8, 0.0, 0.0)
    text_count += 1

for ri in range(15):
    gy = PLAN_Y + ri * 1200
    if gy > GRID_TOP:
        break
    gh = Draft.makeLine(FreeCAD.Vector(GRID_LEFT, gy, 0), FreeCAD.Vector(GRID_RIGHT, gy, 0))
    S(gh, 0.3, (0.75, 0.75, 0.75))
    drawing_commands += 1
    t = Draft.makeText([str(ri + 1)], point=FreeCAD.Vector(GRID_LEFT - 700, gy - 100, 0))
    t.ViewObject.FontSize = 240
    t.ViewObject.TextColor = (0.8, 0.0, 0.0)
    text_count += 1

# ═════════════════════════════════════════════════════════════
#  TITLE BLOCK
# ═════════════════════════════════════════════════════════════
TB_Y = SIDE_Y + 5000
TB_W = HOUSE_W
TB_H = 2500

room_box(0, TB_Y, TB_W, TB_H, 1.5).Label = "Title_Block_Outer"
wall(TB_W * 0.5, TB_Y, TB_W * 0.5, TB_Y + TB_H, 1.0)
wall(0, TB_Y + TB_H * 0.5, TB_W, TB_Y + TB_H * 0.5, 0.8)
wall(0, TB_Y + TB_H * 0.65, TB_W * 0.5, TB_Y + TB_H * 0.65, 0.8)

lbl(
    [f"PROJECT: {REQUEST_SUMMARY}", "CLIENT:", "SITE:"],
    150, TB_Y + 1500, size=220
)
lbl(
    ["DRAWN BY: AI Blueprint Engine", "CHECKED BY:", f"DATE: 2025", "SCALE: 1:100", "SHEET: A-101"],
    TB_W * 0.5 + 150, TB_Y + 1500, size=220
)
lbl(["ARCHITECTURAL DRAWINGS"], TB_W * 0.5 - 1800, TB_Y + 200, size=300)
lbl(["FLOOR PLAN + ELEVATIONS",  "DRAWING No: A-101"],
    150, TB_Y + 100, size=260)

# ═════════════════════════════════════════════════════════════
doc.recompute()

if hasattr(FreeCAD, "Gui") and FreeCAD.Gui:
    try:
        FreeCAD.Gui.SendMsgToActiveView("ViewFit")
        FreeCAD.Gui.ActiveDocument.activeView().viewTop()
    except Exception:
        pass

print(f"Primitives : {drawing_commands}")
print(f"Dimensions : {dimension_count}")
print(f"Labels     : {text_count}")
print("=== BLUEPRINT COMPLETE ===")
