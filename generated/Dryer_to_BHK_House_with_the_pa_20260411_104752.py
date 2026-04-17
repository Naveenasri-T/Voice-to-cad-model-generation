
import FreeCAD
import Draft

doc = FreeCAD.newDocument("Dryer_to_BHK_House_with_the_parking_and")
REQUEST_SUMMARY = "Dryer to BHK House with the parking and garden."

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

# ─── SAFE COLOUR HELPER ───────────────────────────────────────
def _set_color(vo, attr, val):
    """Safely set a ViewObject colour property."""
    try:
        setattr(vo, attr, val)
    except Exception:
        pass   # Some FreeCAD builds reject certain colour formats

# ─── HELPERS ──────────────────────────────────────────────────
def S(obj, w=2.0, c=(0.0, 0.0, 0.0)):
    if hasattr(obj, "ViewObject"):
        try:
            obj.ViewObject.LineWidth = w
        except Exception:
            pass
        _set_color(obj.ViewObject, "LineColor", c)

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
    # Draft.make_text is the current API (makeText is deprecated)
    try:
        t = Draft.make_text(texts, placement=FreeCAD.Vector(x, y, 0))
    except Exception:
        t = Draft.makeText(texts, point=FreeCAD.Vector(x, y, 0))
    if hasattr(t, "ViewObject"):
        try:
            t.ViewObject.FontSize = size
        except Exception:
            pass
        _set_color(t.ViewObject, "TextColor", color)
    text_count += 1
    return t

def dim(x1, y1, x2, y2):
    global dimension_count
    try:
        d = Draft.make_linear_dimension(
            FreeCAD.Vector(x1, y1, 0),
            FreeCAD.Vector(x2, y2, 0)
        )
        if hasattr(d, "ViewObject"):
            try:
                d.ViewObject.FontSize = 260
            except Exception:
                pass
            _set_color(d.ViewObject, "TextColor", (1.0, 0.0, 0.0))
            _set_color(d.ViewObject, "LineColor",  (0.0, 0.0, 0.0))
        dimension_count += 1
        return d
    except Exception:
        return None

def door_arc(cx, cy, r, a1, a2):
    global drawing_commands
    try:
        arc = Draft.makeCircle(
            radius=r,
            placement=FreeCAD.Placement(FreeCAD.Vector(cx, cy, 0), FreeCAD.Rotation(0, 0, 0)),
            startangle=a1, endangle=a2
        )
        S(arc, 0.8)
        drawing_commands += 1
        return arc
    except Exception:
        return None

def win(x, y, length, horiz=True):
    """Three-line window symbol."""
    if horiz:
        wall(x, y - 60, x + length, y - 60, 1.0)
        wall(x, y,      x + length, y,      1.8)
        wall(x, y + 60, x + length, y + 60, 1.0)
    else:
        wall(x - 60, y, x - 60, y + length, 1.0)
        wall(x,      y, x,      y + length, 1.8)
        wall(x + 60, y, x + 60, y + length, 1.0)

# ═════════════════════════════════════════════════════════════
#  FLOOR PLAN  (Plan View – looking down)
# ═════════════════════════════════════════════════════════════
print("Drawing Floor Plan...")

# ── Outer house boundary (thick) ──────────────────────────────
ext = room_box(0, PLAN_Y, HOUSE_W, HOUSE_D, 3.5)
ext.Label = "Exterior_Boundary"

# ── Interior walls ─────────────────────────────────────────────
wall(6000, PLAN_Y, 6000, PLAN_Y + HOUSE_D, 2.2).Label = "Spine_Wall"
wall(0, PLAN_Y + 4500, HOUSE_W, PLAN_Y + 4500, 2.2).Label = "Mid_Wall"
wall(3500, PLAN_Y + 4500, 3500, PLAN_Y + HOUSE_D, 2.0).Label = "Kitchen_E_Wall"
wall(3500, PLAN_Y + 6400, 6000, PLAN_Y + 6400, 2.0).Label = "Bath_Divider"
wall(9000, PLAN_Y + 4500, 9000, PLAN_Y + HOUSE_D, 2.0).Label = "Store_Wall"

# ── Windows ────────────────────────────────────────────────────
# South face (front wall y=PLAN_Y)
win(700,  PLAN_Y, 1400, True)
win(2500, PLAN_Y, 1200, True)
win(7000, PLAN_Y, 1600, True)
# North face (rear wall y=PLAN_Y+HOUSE_D)
win(400,  PLAN_Y + HOUSE_D, 1200, True)
win(2200, PLAN_Y + HOUSE_D, 1000, True)
win(6500, PLAN_Y + HOUSE_D, 1200, True)
# East face (side wall x=HOUSE_W)
win(HOUSE_W, PLAN_Y + 1200, 1200, False)
win(HOUSE_W, PLAN_Y + 5500, 1200, False)

# ── Door openings + swing arcs ─────────────────────────────────
# Main entrance (south, x=4700)
wall(4700, PLAN_Y, 5600, PLAN_Y, 0.4)
door_arc(4700, PLAN_Y, 900, 0, 90)
lbl(["D1"], 4700, PLAN_Y - 350, size=200)

# Master bed door (spine, y=1500-2300)
wall(6000, PLAN_Y + 1500, 6000, PLAN_Y + 2300, 0.4)
door_arc(6000, PLAN_Y + 2300, 800, 180, 270)
lbl(["D2"], 6150, PLAN_Y + 1800, size=200)

# Kitchen door (mid wall, x=2000-2700)
wall(2000, PLAN_Y + 4500, 2700, PLAN_Y + 4500, 0.4)
door_arc(2000, PLAN_Y + 4500, 700, 270, 360)
lbl(["D3"], 2100, PLAN_Y + 4650, size=200)

# Bed2 door (kitchen east wall, y=5200-5900)
wall(3500, PLAN_Y + 5200, 3500, PLAN_Y + 5900, 0.4)
door_arc(3500, PLAN_Y + 5200, 700, 0, 90)
lbl(["D4"], 3650, PLAN_Y + 5300, size=200)

# Bathroom door
wall(3500, PLAN_Y + 6600, 3500, PLAN_Y + 7200, 0.4)
door_arc(3500, PLAN_Y + 6600, 600, 0, 90)
lbl(["D5"], 3650, PLAN_Y + 6700, size=200)

# Toilet door
wall(4400, PLAN_Y + 6400, 5000, PLAN_Y + 6400, 0.4)
door_arc(4400, PLAN_Y + 6400, 600, 270, 360)
lbl(["D6"], 4450, PLAN_Y + 6580, size=200)

# ── Furniture ──────────────────────────────────────────────────
room_box(300,  PLAN_Y + 2800, 2800, 800,  1.0).Label = "Sofa"
room_box(300,  PLAN_Y + 200,  1200, 700,  1.0).Label = "TV_Unit"
room_box(3200, PLAN_Y + 1800, 1800, 1200, 1.0).Label = "Dining_Table"
room_box(6300, PLAN_Y + 600,  2200, 1800, 1.0).Label = "Master_Bed"
room_box(8800, PLAN_Y + 300,  600,  2000, 1.0).Label = "Wardrobe"
room_box(6400, PLAN_Y + 5200, 2000, 1600, 1.0).Label = "Bed2"
room_box(200,  PLAN_Y + 4700, 3100, 600,  1.0).Label = "Kitchen_Counter"

# ── Room labels ────────────────────────────────────────────────
lbl(["LIVING ROOM",   "6.0 x 4.5 m"],   1000, PLAN_Y + 2000, size=300)
lbl(["DINING",        "3.5 x 2.5 m"],   3200, PLAN_Y + 3000, size=260)
lbl(["MASTER BEDROOM","4.5 x 4.5 m"],   6500, PLAN_Y + 1800, size=300)
lbl(["BEDROOM 2",     "4.5 x 4.0 m"],   6400, PLAN_Y + 5900, size=300)
lbl(["KITCHEN",       "3.5 x 4.0 m"],    400, PLAN_Y + 5600, size=280)
lbl(["BATHROOM"],                        3700, PLAN_Y + 5100, size=260)
lbl(["TOILET"],                          3700, PLAN_Y + 7100, size=260)
lbl(["STORE"],                           9100, PLAN_Y + 5900, size=240)

lbl(["FLOOR PLAN", "Scale 1:100"],     0, PLAN_Y + HOUSE_D + 600, size=340)
lbl(["N", chr(8593)],  HOUSE_W + 950, PLAN_Y + HOUSE_D / 2, size=500, color=(0.0, 0.4, 0.8))

# ── Plan dimensions ────────────────────────────────────────────
dim(0,          PLAN_Y - 1400, HOUSE_W, PLAN_Y - 1400)        # total width
dim(-1400,      PLAN_Y,       -1400,    PLAN_Y + HOUSE_D)     # total depth
dim(0,          PLAN_Y - 700,  6000,    PLAN_Y - 700)         # living zone W
dim(6000,       PLAN_Y - 700,  HOUSE_W, PLAN_Y - 700)         # bed zone W
dim(HOUSE_W+700, PLAN_Y,      HOUSE_W+700, PLAN_Y+4500)       # front depth
dim(HOUSE_W+700, PLAN_Y+4500, HOUSE_W+700, PLAN_Y+HOUSE_D)   # rear depth
dim(0,          PLAN_Y + HOUSE_D + 300, 3500, PLAN_Y + HOUSE_D + 300)
dim(3500,       PLAN_Y + HOUSE_D + 300, 6000, PLAN_Y + HOUSE_D + 300)

# ═════════════════════════════════════════════════════════════
#  FRONT ELEVATION  (y = FRONT_Y)
# ═════════════════════════════════════════════════════════════
print("Drawing Front Elevation...")

room_box(0, FRONT_Y, HOUSE_W, 3000, 3.0).Label = "Front_Elev"
wall(0, FRONT_Y - 250, HOUSE_W, FRONT_Y - 250, 3.0)          # ground
wall(0, FRONT_Y + 450, HOUSE_W, FRONT_Y + 450, 1.5)          # plinth
wall(0, FRONT_Y + 2200, HOUSE_W, FRONT_Y + 2200, 1.5)        # lintel
room_box(0, FRONT_Y + 3000, HOUSE_W, 400, 1.5).Label = "Parapet"

# Door & windows
room_box(4700, FRONT_Y + 450,  900, 1850, 1.5).Label = "Main_Door"
wall(5150, FRONT_Y + 450, 5150, FRONT_Y + 2300, 0.8)         # door mullion
room_box(700,  FRONT_Y + 900, 1400, 1200, 1.5).Label = "Win_F1"
room_box(2400, FRONT_Y + 900, 1200, 1200, 1.5).Label = "Win_F2"
room_box(6800, FRONT_Y + 900, 1600, 1200, 1.5).Label = "Win_F3"
room_box(9100, FRONT_Y + 900,  900, 1000, 1.5).Label = "Win_F4"

# Column marks
for cx in [0, 3500, 6000, 9000, HOUSE_W]:
    wall(cx, FRONT_Y, cx, FRONT_Y + 3000, 0.8)

lbl(["FRONT ELEVATION", "Scale 1:100"], 0, FRONT_Y + 3650, size=340)

dim(0,     FRONT_Y - 850, HOUSE_W, FRONT_Y - 850)            # width
dim(-1200, FRONT_Y,       -1200,   FRONT_Y + 450)            # plinth
dim(-1200, FRONT_Y + 450, -1200,   FRONT_Y + 2200)           # wall to lintel
dim(-1200, FRONT_Y + 2200,-1200,   FRONT_Y + 3400)           # lintel to slab

# ═════════════════════════════════════════════════════════════
#  SIDE ELEVATION  (y = SIDE_Y)
# ═════════════════════════════════════════════════════════════
print("Drawing Side Elevation...")

room_box(0, SIDE_Y, HOUSE_D, 3000, 3.0).Label = "Side_Elev"
wall(0, SIDE_Y - 250, HOUSE_D, SIDE_Y - 250, 3.0)            # ground
wall(0, SIDE_Y + 450, HOUSE_D, SIDE_Y + 450, 1.5)            # plinth
wall(0, SIDE_Y + 2200, HOUSE_D, SIDE_Y + 2200, 1.5)          # lintel
room_box(0, SIDE_Y + 3000, HOUSE_D, 400, 1.5).Label = "Side_Parapet"

# Side windows
room_box(800,  SIDE_Y + 900, 1200, 1100, 1.5).Label = "Side_Win1"
room_box(3600, SIDE_Y + 900, 1200, 1100, 1.5).Label = "Side_Win2"
room_box(5400, SIDE_Y + 900, 1200, 1100, 1.5).Label = "Side_Win3"

# Section cut marks at wall faces (just 4 short diagonal marks, not a dense hatch)
for hx in [0, 200, 400, 600]:
    wall(hx, SIDE_Y, hx + 200, SIDE_Y + 200, 0.5)

lbl(["SIDE / SECTION ELEVATION", "Scale 1:100"], 0, SIDE_Y + 3700, size=340)

dim(0,      SIDE_Y - 850, HOUSE_D, SIDE_Y - 850)             # depth
dim(-1200,  SIDE_Y,      -1200,    SIDE_Y + 3400)            # total height
dim(-700,   SIDE_Y,      -700,     SIDE_Y + 450)             # plinth

# ═════════════════════════════════════════════════════════════
#  COORDINATE GRID  (spaced 2400mm — half as dense)
# ═════════════════════════════════════════════════════════════
GRID_SPACING = 2400
GRID_BOT = PLAN_Y - 2600
GRID_TOP = SIDE_Y + 4400
GRID_L   = -2200
GRID_R   = HOUSE_W + 2200

for ci, letter in enumerate("ABCDE"):
    gx = ci * GRID_SPACING
    if gx > HOUSE_W + 500:
        break
    gl = Draft.makeLine(FreeCAD.Vector(gx, GRID_BOT, 0), FreeCAD.Vector(gx, GRID_TOP, 0))
    S(gl, 0.3, (0.78, 0.78, 0.78))
    drawing_commands += 1
    try:
        t = Draft.make_text([letter], placement=FreeCAD.Vector(gx - 100, GRID_BOT - 600, 0))
    except Exception:
        t = Draft.makeText([letter], point=FreeCAD.Vector(gx - 100, GRID_BOT - 600, 0))
    if hasattr(t, "ViewObject"):
        try:
            t.ViewObject.FontSize = 240
        except Exception:
            pass
        _set_color(t.ViewObject, "TextColor", (0.8, 0.0, 0.0))
    text_count += 1

for ri, num in enumerate(["1", "2", "3", "4", "5", "6", "7"]):
    gy = PLAN_Y + ri * GRID_SPACING
    if gy > GRID_TOP:
        break
    gh = Draft.makeLine(FreeCAD.Vector(GRID_L, gy, 0), FreeCAD.Vector(GRID_R, gy, 0))
    S(gh, 0.3, (0.78, 0.78, 0.78))
    drawing_commands += 1
    try:
        t = Draft.make_text([num], placement=FreeCAD.Vector(GRID_L - 600, gy - 100, 0))
    except Exception:
        t = Draft.makeText([num], point=FreeCAD.Vector(GRID_L - 600, gy - 100, 0))
    if hasattr(t, "ViewObject"):
        try:
            t.ViewObject.FontSize = 240
        except Exception:
            pass
        _set_color(t.ViewObject, "TextColor", (0.8, 0.0, 0.0))
    text_count += 1

# ═════════════════════════════════════════════════════════════
#  TITLE BLOCK
# ═════════════════════════════════════════════════════════════
TB_Y = SIDE_Y + 4600
room_box(0, TB_Y, HOUSE_W, 2500, 1.5).Label = "Title_Block"
wall(HOUSE_W * 0.5, TB_Y, HOUSE_W * 0.5, TB_Y + 2500, 1.0)
wall(0, TB_Y + 1250, HOUSE_W, TB_Y + 1250, 0.8)
lbl([f"PROJECT: {REQUEST_SUMMARY}", "CLIENT:", "SCALE: 1:100"], 150, TB_Y + 1450, size=220)
lbl(["DRAWN BY: AI Blueprint", "DATE: 2025", "SHEET: A-101"], HOUSE_W * 0.5 + 150, TB_Y + 1450, size=220)
lbl(["VOICE TO CAD MODEL GENERATION"], HOUSE_W * 0.5 - 2500, TB_Y + 200, size=300)

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
