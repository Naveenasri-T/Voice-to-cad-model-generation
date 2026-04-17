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
    d.ViewObject    dimension_count+=1;  return d
def door_arc(cx,cy,r,a1,a2):
    global drawing_commands
    arc=Draft.makeCircle(radius=r,
        placement=FreeCAD.Placement(FreeCAD.Vector(cx,cy,0),FreeCAD.Rotation(0,0,0)),
        startangle=a1,endangle=a2)
    S(arc,0.8);  drawing_commands+=1;  return arc
# Floor plan
room_box(0,PLAN_Y,10500,8500,3.5)
wall(6000,PLAN_Y,6000,8500,2.2)
wall(0,4500,10500,4500,2.2)
wall(3500,4500,3500,8500,2.0)
wall(3500,6400,6000,6400,2.0)
# Doors
wall(6000-900,2250,6000,2250,1.5)
door_arc(6000,2250,900,0,90)
wall(0+900,3750,0,3750,1.5)
door_arc(0,3750,900,0,90)
wall(3500-900,5500,3500,5500,1.5)
door_arc(3500,5500,900,0,90)
wall(6000+900,6250,6000,6250,1.5)
door_arc(6000,6250,900,0,90)
# Windows
wall(0+100,200,0+100+2000,200,1.0)
wall(0+100,200+60,0+100+2000,200+60,1.0)
wall(0+100,200+120,0+100+2000,200+120,1.8)
wall(6000-100,200,6000-100-2000,200,1.0)
wall(6000-100,200+60,6000-100-2000,200+60,1.0)
wall(6000-100,200+120,6000-100-2000,200+120,1.8)
wall(0+100,4500+200,0+100+2000,4500+200,1.0)
wall(0+100,4500+200+60,0+100+2000,4500+200+60,1.0)
wall(0+100,4500+200+120,0+100+2000,4500+200+120,1.8)
# Labels
lbl("Living Room",200,200)
lbl("Master Bed",6500,200)
lbl("Kitchen",200,5000)
lbl("Bath",4000,5000)
lbl("Toilet",4000,7000)
lbl("Bed 2",6500,5000)
# Front elevation
room_box(0,FRONT_Y,10500,8500,3.5)
wall(6000,FRONT_Y,6000,FRONT_Y+8500,2.2)
wall(0,FRONT_Y+4500,10500,FRONT_Y+4500,2.2)
wall(3500,FRONT_Y+4500,3500,FRONT_Y+8500,2.0)
wall(3500,FRONT_Y+6400,6000,FRONT_Y+6400,2.0)
# Side elevation
room_box(0,SIDE_Y,10500,8500,3.5)
wall(6000,SIDE_Y,6000,SIDE_Y+8500,2.2)
wall(0,SIDE_Y+4500,10500,SIDE_Y+4500,2.2)
wall(3500,SIDE_Y+4500,3500,SIDE_Y+8500,2.0)
wall(3500,SIDE_Y+6400,6000,SIDE_Y+6400,2.0)
# Coordinate grid
for i in range(11):
    wall(0+i*1200,0,0+i*1200,8500,0.3)
    wall(0,0+i*1200,10500,0+i*1200,0.3)
    S(wall(0+i*1200,0,0+i*1200,8500,0.3),(0.75,0.75,0.75))
    S(wall(0,0+i*1200,10500,0+i*1200,0.3),(0.75,0.75,0.75))
# Title block
room_box(0,VIEW_GAP*3,10500,1000,2.0)
lbl("Project: 2BHK House",200,VIEW_GAP*3+200)
lbl("Scale: 1:100",200,VIEW_GAP*3+400)
lbl("Sheet: 1",200,VIEW_GAP*3+600)
lbl("Date: 2024-02-20",200,VIEW_GAP*3+800)
# Dimensions
dim(0,0,10500,0)
dim(0,0,0,8500)
dim(6000,0,6000,8500)
dim(0,4500,10500,4500)
dim(3500,4500,3500,8500)
dim(3500,6400,6000,6400)
dim(0,FRONT_Y,10500,FRONT_Y)
dim(0,FRONT_Y,0,FRONT_Y+8500)
dim(6000,FRONT_Y,6000,FRONT_Y+8500)
dim(0,FRONT_Y+4500,10500,FRONT_Y+4500)
dim(3500,FRONT_Y+4500,3500,FRONT_Y+8500)
dim(3500,FRONT_Y+6400,6000,FRONT_Y+6400)
print(f"Primitives : {drawing_commands}")
print(f"Dimensions : {dimension_count}")
print(f"Labels     : {text_count}")
doc.recompute()
if hasattr(FreeCAD,"Gui") and FreeCAD.Gui:
    try:
        FreeCAD.Gui.SendMsgToActiveView("ViewFit")
        FreeCAD.Gui.ActiveDocument.activeView().viewTop()
    except Exception: pass