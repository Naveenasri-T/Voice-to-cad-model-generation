# Import necessary modules
import FreeCAD
import Part
import Draft
import FreeCADGui

# Create a new document
doc = FreeCAD.newDocument()

# Create a simple cube
cube = Part.makeBox(10, 10, 10)

# Add the cube to the document
doc.addObject("Part::Feature", "Cube").Shape = cube

# Recompute the document
doc.recompute()

# Get the active 3D view
view = FreeCADGui.ActiveDocument.ActiveView

# Set the view to axometric
view.setAxisCrosshair(0)
view.setOrthographic(0)
view.setPerspective(0)
view.setCameraType("Perspective")

# Zoom the view to fit the object
view.fitAll()

# Alternatively, you can use the following functions
# viewAxometric = FreeCADGui.runCommand("Std_ViewAxometric", 0)
# viewFit = FreeCADGui.runCommand("Std_ViewFitAll", 0)
However, the `viewAxometric()` and `ViewFit()` functions are not built-in FreeCAD functions. They are custom functions that can be created to simplify the process of setting the view to axometric and zooming to fit the object.

Here's an updated version of the code that includes these custom functions:

# Import necessary modules
import FreeCAD
import Part
import Draft
import FreeCADGui

# Function to set the view to axometric
def viewAxometric():
    view = FreeCADGui.ActiveDocument.ActiveView
    view.setAxisCrosshair(0)
    view.setOrthographic(0)
    view.setPerspective(0)
    view.setCameraType("Perspective")

# Function to zoom the view to fit the object
def viewFit():
    view = FreeCADGui.ActiveDocument.ActiveView
    view.fitAll()

# Create a new document
doc = FreeCAD.newDocument()

# Create a simple cube
cube = Part.makeBox(10, 10, 10)

# Add the cube to the document
doc.addObject("Part::Feature", "Cube").Shape = cube

# Recompute the document
doc.recompute()