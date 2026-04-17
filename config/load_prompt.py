"""Load AI system prompts from configuration files."""
from pathlib import Path


def load_system_prompt() -> str:
    """Load the main AI system prompt from the configuration file."""
    prompt_file = Path(__file__).parent / "ai_system_prompt.txt"
    try:
        with open(prompt_file, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return (
            "Generate professional FreeCAD Python 2D blueprint code using only "
            "FreeCAD and Draft modules. Create floor plan + front + side elevation. "
            "Include >= 30 Draft primitives, >= 8 dimensions, >= 8 text labels, "
            "a coordinate grid, and a title block. End with doc.recompute()."
        )


def load_regeneration_prompt(user_command: str) -> str:
    """Build the 2D-only regeneration prompt (kept short to stay within token limits)."""
    return (
        f"{user_command}\n\n"
        "GENERATE 2BHK HOUSE BLUEPRINT — 2D ONLY, NO Part module.\n\n"
        "MANDATORY:\n"
        "  - Floor plan (y=0): exterior room_box(0,0,10500,8500,3.5), interior walls\n"
        "  - Front elevation (y=16000): facade, openings, parapet\n"
        "  - Side elevation (y=32000): depth profile\n"
        "  - >= 30 Draft primitives, >= 8 dim(), >= 8 lbl()\n"
        "  - Coordinate grid + title block\n\n"
        "USE THESE HELPERS:\n"
        "  def S(o,w=2.,c=(0.,0.,0.)):\n"
        "      if hasattr(o,'ViewObject'): o.ViewObject.LineWidth=w; o.ViewObject.LineColor=c\n"
        "  def wall(x1,y1,x2,y2,w=2.):\n"
        "      global drawing_commands\n"
        "      ln=Draft.makeLine(FreeCAD.Vector(x1,y1,0),FreeCAD.Vector(x2,y2,0))\n"
        "      S(ln,w); drawing_commands+=1; return ln\n"
        "  def room_box(x,y,w,d,lw=2.):\n"
        "      global drawing_commands\n"
        "      r=Draft.makeRectangle(length=w,height=d,\n"
        "        placement=FreeCAD.Placement(FreeCAD.Vector(x,y,0),FreeCAD.Rotation(0,0,0)))\n"
        "      S(r,lw); drawing_commands+=1; return r\n"
        "  def lbl(texts,x,y,size=280,color=(0.,0.,0.)):\n"
        "      global text_count\n"
        "      t=Draft.makeText(texts,point=FreeCAD.Vector(x,y,0))\n"
        "      t.ViewObject.FontSize=size; t.ViewObject.TextColor=color\n"
        "      text_count+=1; return t\n"
        "  def dim(x1,y1,x2,y2):\n"
        "      global dimension_count\n"
        "      d=Draft.make_linear_dimension(FreeCAD.Vector(x1,y1,0),FreeCAD.Vector(x2,y2,0))\n"
        "      d.ViewObject.FontSize=260; d.ViewObject.TextColor=(1.,0.,0.)\n"
        "      d.ViewObject.LineColor=(0.,0.,0.); dimension_count+=1; return d\n"
        "  def door_arc(cx,cy,r,a1,a2):\n"
        "      global drawing_commands\n"
        "      arc=Draft.makeCircle(radius=r,\n"
        "        placement=FreeCAD.Placement(FreeCAD.Vector(cx,cy,0),FreeCAD.Rotation(0,0,0)),\n"
        "        startangle=a1,endangle=a2)\n"
        "      S(arc,0.8); drawing_commands+=1; return arc\n\n"
        "ROOM LAYOUT (mm): Living(0..6000,0..4500), MasterBed(6000..10500,0..4500),\n"
        "  Kitchen(0..3500,4500..8500), Bath(3500..6000,4500..6400),\n"
        "  Toilet(3500..6000,6400..8500), Bed2(6000..10500,4500..8500)\n"
        "DOORS: gap + door_arc(cx,cy,900,0,90)\n"
        "WINDOWS: three parallel lines (y-60 lw=1, y lw=1.8, y+60 lw=1)\n"
        "FORBIDDEN: import Part, Part.makeBox, non-zero Z, Draft.makeDimension,\n"
        "  merged ViewObject tokens, markdown fences\n"
    )
