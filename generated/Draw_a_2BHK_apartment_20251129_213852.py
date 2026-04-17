import FreeCAD
import Part

doc = FreeCAD.newDocument("Model")
import FreeCAD
import Draft
# Create a new document
doc = FreeCAD.newDocument("2BHK_Apartment")
# === FRONT VIEW (y_offset = 0) ===
# Perimeter outline
front_outline = Draft.makeWire([
    FreeCAD.Vector(0, 0, 0),
    FreeCAD.Vector(8000, 0, 0),
    FreeCAD.Vector(8000, 6000, 0),
    FreeCAD.Vector(0, 6000, 0),
    FreeCAD.Vector(0, 0, 0)
], closed=True)
front_outline.ViewObject.LineWidth = 3.0
# Internal details (doors, windows, compartments)
door1 = Draft.makeLine(FreeCAD.Vector(1000, 0, 0), FreeCAD.Vector(1000, 2000, 0))
door1.ViewObject.LineWidth = 2.0
window1 = Draft.makeLine(FreeCAD.Vector(3000, 0, 0), FreeCAD.Vector(3000, 1500, 0))
window1.ViewObject.LineWidth = 1.5
compartment1 = Draft.makeLine(FreeCAD.Vector(5000, 0, 0), FreeCAD.Vector(5000, 1000, 0))
compartment1.ViewObject.LineWidth = 1.5
# Dimensions
dim1 = Draft.makeDimension(
    FreeCAD.Vector(0, -500, 0),
    FreeCAD.Vector(8000, -500, 0),
    FreeCAD.Vector(4000, -1000, 0)
)
dim1.ViewObjectdim2 = Draft.makeDimension(
    FreeCAD.Vector(0, 6000, 0),
    FreeCAD.Vector(0, 0, 0),
    FreeCAD.Vector(-1000, 3000, 0)
)
dim2.ViewObject
# Labels
label1 = Draft.makeText(["Front Elevation"], point=FreeCAD.Vector(0, 6500, 0))
label1.ViewObject.FontSize = 300
label2 = Draft.makeText(["Door"], point=FreeCAD.Vector(1000, 2000, 0))
label2.ViewObject.FontSize = 200
label3 = Draft.makeText(["Window"], point=FreeCAD.Vector(3000, 1500, 0))
label3.ViewObject.FontSize = 200
# === TOP VIEW (y_offset = 10000) ===
# Floor plan with rooms, furniture, fixtures
top_outline = Draft.makeWire([
    FreeCAD.Vector(0, 10000, 0),
    FreeCAD.Vector(8000, 10000, 0),
    FreeCAD.Vector(8000, 16000, 0),
    FreeCAD.Vector(0, 16000, 0),
    FreeCAD.Vector(0, 10000, 0)
], closed=True)
top_outline.ViewObject.LineWidth = 3.0
# Internal details (rooms, furniture, fixtures)
room1 = Draft.makeLine(FreeCAD.Vector(1000, 10000, 0), FreeCAD.Vector(1000, 14000, 0))
room1.ViewObject.LineWidth = 2.0
furniture1 = Draft.makeLine(FreeCAD.Vector(3000, 10000, 0), FreeCAD.Vector(3000, 12000, 0))
furniture1.ViewObject.LineWidth = 1.5
fixture1 = Draft.makeLine(FreeCAD.Vector(5000, 10000, 0), FreeCAD.Vector(5000, 11000, 0))
fixture1.ViewObject.LineWidth = 1.5
# Dimensions
dim3 = Draft.makeDimension(
    FreeCAD.Vector(0, 10000, 0),
    FreeCAD.Vector(8000, 10000, 0),
    FreeCAD.Vector(4000, 9000, 0)
)
dim3.ViewObjectdim4 = Draft.makeDimension(
    FreeCAD.Vector(0, 16000, 0),
    FreeCAD.Vector(0, 10000, 0),
    FreeCAD.Vector(-1000, 13000, 0)
)
dim4.ViewObject
# Labels
label4 = Draft.makeText(["Floor Plan"], point=FreeCAD.Vector(0, 17000, 0))
label4.ViewObject.FontSize = 300
label5 = Draft.makeText(["Room"], point=FreeCAD.Vector(1000, 14000, 0))
label5.ViewObject.FontSize = 200
label6 = Draft.makeText(["Furniture"], point=FreeCAD.Vector(3000, 12000, 0))
label6.ViewObject.FontSize = 200
# === SIDE VIEW (y_offset = 20000) ===
# Profile projection showing depth
side_outline = Draft.makeWire([
    FreeCAD.Vector(0, 20000, 0),
    FreeCAD.Vector(8000, 20000, 0),
    FreeCAD.Vector(8000, 26000, 0),
    FreeCAD.Vector(0, 26000, 0),
    FreeCAD.Vector(0, 20000, 0)
], closed=True)
side_outline.ViewObject.LineWidth = 3.0
# Internal details (depth, height)
depth1 = Draft.makeLine(FreeCAD.Vector(0, 20000, 0), FreeCAD.Vector(0, 22000, 0))
depth1.ViewObject.LineWidth = 2.0
height1 = Draft.makeLine(FreeCAD.Vector(8000, 20000, 0), FreeCAD.Vector(8000, 24000, 0))
height1.ViewObject.LineWidth = 2.0
# Dimensions
dim5 = Draft.makeDimension(
    FreeCAD.Vector(0, 20000, 0),
    FreeCAD.Vector(8000, 20000, 0),
    FreeCAD.Vector(4000, 19000, 0)
)
dim5.ViewObjectdim6 = Draft.makeDimension(
    FreeCAD.Vector(0, 26000, 0),
    FreeCAD.Vector(0, 20000, 0),
    FreeCAD.Vector(-1000, 23000, 0)
)
dim6.ViewObject
# Labels
label7 = Draft.makeText(["Side Elevation"], point=FreeCAD.Vector(0, 27000, 0))
label7.ViewObject.FontSize = 300
label8 = Draft.makeText(["Depth"], point=FreeCAD.Vector(0, 22000, 0))
label8.ViewObject.FontSize = 200
label9 = Draft.makeText(["Height"], point=FreeCAD.Vector(8000, 24000, 0))
label9.ViewObject.FontSize = 200
# === GRID SYSTEM ===
# Grid lines every 1000mm with A,B,C labels
for i in range(0, 9000, 1000):
    grid_line = Draft.makeLine(FreeCAD.Vector(i, 0, 0), FreeCAD.Vector(i, 6000, 0))
    grid_line.ViewObject.LineWidth = 0.5
    grid_label = Draft.makeText([chr(65 + i // 1000)], point=FreeCAD.Vector(i, -500, 0))
    grid_label.ViewObject.FontSize = 200
# === TITLE BLOCK ===
# Drawing name, scale, date
title_block = Draft.makeText(["2BHK Apartment", "Scale: 1:100", "Date: 2024-09-16"], point=FreeCAD.Vector(0, -1000, 0))
title_block.ViewObject.FontSize = 200
# Recompute and view
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.activeDocument().activeView().viewTop()
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()
