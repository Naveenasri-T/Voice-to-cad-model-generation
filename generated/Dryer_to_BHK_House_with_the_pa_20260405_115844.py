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
house = room_box(0,PLAN_Y,10500,8500,3.5)
spine_wall = wall(6000,PLAN_Y,6000,8500,2.2)
mid_wall = wall(0,4500,10500,4500,2.2)
kitchen_e = wall(3500,4500,3500,8500,2.0)
bath_div = wall(3500,6400,6000,6400,2.0)
# Doors
door1 = door_arc(0,2250,900,0,90)
wall(-100,2200,0,2200,1.5)
door2 = door_arc(6000,2250,900,0,90)
wall(6000,2200,6100,2200,1.5)
door3 = door_arc(0,7000,900,0,90)
wall(-100,7000,0,7000,1.5)
door4 = door_arc(3500,7000,900,0,90)
wall(3400,7000,3500,7000,1.5)
# Windows
wall(1000,PLAN_Y-60,1500,PLAN_Y-60,1.0)
wall(1000,PLAN_Y,1500,PLAN_Y,1.8)
wall(1000,PLAN_Y+60,1500,PLAN_Y+60,1.0)
wall(7000,PLAN_Y-60,7500,PLAN_Y-60,1.0)
wall(7000,PLAN_Y,7500,PLAN_Y,1.8)
wall(7000,PLAN_Y+60,7500,PLAN_Y+60,1.0)
wall(1000,4500-60,1500,4500-60,1.0)
wall(1000,4500,1500,4500,1.8)
wall(1000,4500+60,1500,4500+60,1.0)
wall(7000,4500-60,7500,4500-60,1.0)
wall(7000,4500,7500,4500,1.8)
wall(7000,4500+60,7500,4500+60,1.0)
# Labels
lbl("Living Room",2500,200,280)
lbl("Master Bed",8000,200,280)
lbl("Kitchen",1500,5000,280)
lbl("Bathroom",4500,5000,280)
lbl("Toilet",4500,7000,280)
lbl("Bedroom 2",8000,5000,280)
# Dimensions
dim(0,0,10500,0)
dim(0,0,0,8500)
dim(6000,0,6000,8500)
dim(0,4500,10500,4500)
dim(3500,4500,3500,8500)
dim(3500,6400,6000,6400)
dim(0,2250,0,7000)
dim(6000,2250,6000,7000)
# Front elevation
facade = room_box(0,FRONT_Y,10500,8500,3.5)
wall(0,FRONT_Y+8500,10500,FRONT_Y+8500,2.0)
wall(0,FRONT_Y+9000,10500,FRONT_Y+9000,2.0)
wall(0,FRONT_Y+9500,10500,FRONT_Y+9500,2.0)
# Side elevation
depth = room_box(0,SIDE_Y,10500,8500,3.5)
wall(0,SIDE_Y+8500,10500,SIDE_Y+8500,2.0)
wall(0,SIDE_Y+9000,10500,SIDE_Y+9000,2.0)
wall(0,SIDE_Y+9500,10500,SIDE_Y+9500,2.0)
# Coordinate grid
for i in range(1,11):
    wall(i*1200,0,i*1200,8500,0.3)
    wall(0,i*1200,10500,i*1200,0.3)
# Title block
title = room_box(0,11000,10500,1000,2.0)
lbl("Project: 2BHK House",100,11100,280)
lbl("Scale: 1:100",100,11200,280)
lbl("Sheet: 1",100,11300,280)
lbl("Date: 2024-09-16",100,11400,280)
print(f"Primitives : {drawing_commands}")
print(f"Dimensions : {dimension_count}")
print(f"Labels     : {text_count}")
doc.recompute()
if hasattr(FreeCAD,"Gui") and FreeCAD.Gui:
    try:
        FreeCAD.Gui.SendMsgToActiveView("ViewFit")
        FreeCAD.Gui.ActiveDocument.activeView().viewTop()
    except Exception: pass