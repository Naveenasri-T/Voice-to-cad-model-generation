import FreeCAD, Draft
doc = FreeCAD.newDocument("Blueprint")
VIEW_GAP = 16000;  PLAN_Y = 0;  FRONT_Y = VIEW_GAP;  SIDE_Y = VIEW_GAP*2
drawing_commands = 0;  dimension_count = 0;  text_count = 0
def S(obj, w=2.0, c=(0.,0.,0.)):
    if hasattr(obj,"ViewObject"):
        obj.ViewObject.LineWidth = w
        obj.ViewObject
def wall(x1,y1,x2,y2,w=2.0):
    global drawing_commands
    ln=Draft.makeLine(FreeCAD.Vector(x1,y1,0),FreeCAD.Vector(x2,y2,0))
    S(ln,w);  drawing_commands+=1;  return ln
def room_box(x,y,w,d,lw=2.0):
    global drawing_commands
    r=Draft.makeRectangle(length=w,height=d,
        placement=FreeCAD.Placement(FreeCAD.Vector(x,y,0),FreeCAD.Rotation(0,0,0)))
    S(r,lw);  drawing_commands+=1;  return r
def lbl(texts,x,y,size=280,color=(0.,0.,0.)):
    global text_count
    t=Draft.makeText(texts,point=FreeCAD.Vector(x,y,0))
    t.ViewObject.FontSize=size
    t.ViewObject.TextColor=color
    text_count+=1;  return t
def dim(x1,y1,x2,y2):
    global dimension_count
    d=Draft.make_linear_dimension(FreeCAD.Vector(x1,y1,0),FreeCAD.Vector(x2,y2,0))
    d.ViewObject.FontSize=260
    d.ViewObject.TextColor=(1.,0.,0.)
    d.ViewObject
def door_arc(cx,cy,r,a1,a2):
    global drawing_commands
    arc=Draft.makeCircle(radius=r,
        placement=FreeCAD.Placement(FreeCAD.Vector(cx,cy,0),FreeCAD.Rotation(0,0,0)),
        startangle=a1,endangle=a2)
    S(arc,0.8);  drawing_commands+=1;  return arc
# Floor plan
room_box(0,PLAN_Y,10500,8500,3.5)
wall(6000,PLAN_Y,6000,8500+PLAN_Y,2.2)
wall(0,4500,10500,4500,2.2)
wall(3500,4500,3500,8500,2.0)
wall(3500,6400,6000,6400,2.0)
# Doors
wall(6000-900,2250,6000,2250,1.5)
door_arc(6000,2250,900,0,90)
wall(0+900,3750,0,3750,1.5)
door_arc(0,3750,900,0,90)
wall(3500-900,5250,3500,5250,1.5)
door_arc(3500,5250,900,0,90)
wall(6000-900,6750,6000,6750,1.5)
door_arc(6000,6750,900,0,90)
# Windows
wall(0+1500,0+150,0+1500+1200,0+150,1.0)
wall(0+1500,0,0+1500+1200,0,1.8)
wall(0+1500,0-150,0+1500+1200,0-150,1.0)
wall(6000+1500,0+150,6000+1500+1200,0+150,1.0)
wall(6000+1500,0,6000+1500+1200,0,1.8)
wall(6000+1500,0-150,6000+1500+1200,0-150,1.0)
wall(0+1500,4500+150,0+1500+1200,4500+150,1.0)
wall(0+1500,4500,0+1500+1200,4500,1.8)
wall(0+1500,4500-150,0+1500+1200,4500-150,1.0)
# Labels
lbl("Living", 3000, 2250)
lbl("Master Bed", 8250, 2250)
lbl("Kitchen", 1750, 6750)
lbl("Bath", 4250, 5750)
lbl("Toilet", 4250, 7750)
lbl("Bed 2", 8250, 6750)
# Front elevation
room_box(0,FRONT_Y,10500,8500,3.5)
wall(6000,FRONT_Y,6000,8500+FRONT_Y,2.2)
wall(0,4500+FRONT_Y,10500,4500+FRONT_Y,2.2)
wall(3500,4500+FRONT_Y,3500,8500+FRONT_Y,2.0)
wall(3500,6400+FRONT_Y,6000,6400+FRONT_Y,2.0)
# Side elevation
room_box(0,SIDE_Y,10500,8500,3.5)
wall(6000,SIDE_Y,6000,8500+SIDE_Y,2.2)
wall(0,4500+SIDE_Y,10500,4500+SIDE_Y,2.2)
wall(3500,4500+SIDE_Y,3500,8500+SIDE_Y,2.0)
wall(3500,6400+SIDE_Y,6000,6400+SIDE_Y,2.0)
# Dimensions
dim(0,0,10500,0)
dim(0,0,0,8500)
dim(6000,0,6000,8500)
dim(0,4500,10500,4500)
dim(3500,4500,3500,8500)
dim(3500,6400,6000,6400)
# Coordinate grid
for i in range(1,11):
    wall(0+i*1200,0,0+i*1200,8500,0.3)
    wall(0,0+i*1200,10500,0+i*1200,0.3)
    S(wall(0,0+i*1200,10500,0+i*1200,0.3),(0.75,0.75,0.75))
# Title block
room_box(0,-2000,10500,1000,2.0)
lbl("Project: 2BHK House", 100, -1500)
lbl("Scale: 1:100", 100, -1700)
lbl("Sheet: 1", 100, -1900)
lbl("Date: 2024-09-16", 100, -2100)
print(f"Primitives : {drawing_commands}")
print(f"Dimensions : {dimension_count}")
print(f"Labels     : {text_count}")
doc.recompute()
if hasattr(FreeCAD,"Gui") and FreeCAD.Gui:
    try:
        FreeCAD.Gui.SendMsgToActiveView("ViewFit")
        FreeCAD.Gui.ActiveDocument.activeView().viewTop()
    except Exception: pass