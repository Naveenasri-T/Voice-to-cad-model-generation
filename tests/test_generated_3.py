# Import necessary modules
import FreeCAD
import Part
import Draft
import FreeCADGui

# Create a new document
doc = FreeCAD.newDocument()

# Create a cylinder with radius 5 and height 10
cylinder = Part.makeCylinder(5, 10)

# Add the cylinder to the document
doc.addObject("Part::Feature", "Cylinder").Shape = cylinder

# Recompute the document
doc.recompute()

# Get the active 3D view
view = FreeCADGui.ActiveDocument.ActiveView

# Set the view to axometric
view.setAxisCross(True)

# Fit the view to the object
view.fitToScreen()

# Alternatively, you can use the following functions
# viewAxometric = FreeCADGui.runCommand("Std_ViewAxometric", 0)
# viewFit = FreeCADGui.runCommand("Std_ViewFitAll", 0)
However, note that `viewAxometric()` and `ViewFit()` are not standard FreeCAD functions. Instead, you should use `view.setAxisCross(True)` and `view.fitToScreen()` as shown above.

If you want to use the `Std_ViewAxometric` and `Std_ViewFitAll` commands, you can use the following code:

FreeCADGui.runCommand("Std_ViewAxometric", 0)
FreeCADGui.runCommand("Std_ViewFitAll", 0)