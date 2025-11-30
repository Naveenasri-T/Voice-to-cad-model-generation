"""
ARCHITECTURAL CODE TEMPLATE ENFORCER
===================================

This system forces the AI to generate proper architectural models
by providing a strict template that must be followed.
"""

ARCHITECTURAL_TEMPLATE = '''
import FreeCAD
import Part
import Draft

# CREATE DOCUMENT
doc = FreeCAD.newDocument("Integrated_Architecture")

print("=== ARCHITECTURAL ANALYSIS ===")
print("Building Type: {building_type}")
print("Required Rooms: {rooms}")
print("Total Area Strategy: {strategy}")
print("Structural Integration: All elements connected as unified building")

print("\\n=== PARAMETRIC CALCULATIONS ===")
# REALISTIC DIMENSIONS BASED ON ARCHITECTURAL STANDARDS
{parametric_calculations}

print("\\n=== BUILDING INTEGRATED STRUCTURE ===")

def create_unified_foundation():
    """Create single foundation supporting entire building"""
    foundation = doc.addObject("Part::Box", "Unified_Foundation")
    foundation.Length = total_building_length
    foundation.Width = total_building_width
    foundation.Height = 150  # 150mm foundation slab
    foundation.Placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), FreeCAD.Rotation(0, 0, 0))
    foundation.ViewObject.ShapeColor = (0.3, 0.3, 0.3)  # Dark concrete
    print("✓ Unified foundation created: Supporting entire building footprint")
    return foundation

def create_integrated_walls():
    """Create walls that form connected rooms in logical layout"""
    walls = []
    wall_thickness = 200  # 200mm structural walls
    wall_height = 3000   # 3m ceiling height
    
    {wall_creation_code}
    
    # Apply consistent wall materials
    for wall in walls:
        wall.ViewObject.ShapeColor = (0.9, 0.85, 0.7)  # Warm beige
    
    print(f"✓ Integrated wall system: {{len(walls)}} walls forming connected spaces")
    return walls

def create_unified_roof():
    """Create single roof covering entire building"""
    roof = doc.addObject("Part::Box", "Unified_Roof")
    roof.Length = total_building_length + 400  # 200mm overhang each side
    roof.Width = total_building_width + 400
    roof.Height = 150  # 150mm roof slab
    roof.Placement = FreeCAD.Placement(FreeCAD.Vector(-200, -200, 3150), FreeCAD.Rotation(0, 0, 0))
    roof.ViewObject.ShapeColor = (0.8, 0.2, 0.1)  # Terracotta red
    print("✓ Unified roof: Single structure covering entire building")
    return roof

def add_functional_openings():
    """Add doors and windows in logical positions"""
    openings = []
    
    {openings_code}
    
    print(f"✓ Functional openings: {{len(openings)}} doors and windows for access and light")
    return openings

def add_room_labels():
    """Add professional room labels with areas"""
    labels = []
    
    {labels_code}
    
    print(f"✓ Room labeling: {{len(labels)}} rooms clearly identified")
    return labels

# EXECUTE INTEGRATED CONSTRUCTION
print("\\n=== CONSTRUCTION SEQUENCE ===")
foundation = create_unified_foundation()
walls = create_integrated_walls()
roof = create_unified_roof()
openings = add_functional_openings()
labels = add_room_labels()

# FINALIZE INTEGRATED MODEL
doc.recompute()
if hasattr(FreeCAD, 'Gui'):
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.ActiveDocument.activeView().viewIsometric()

print("\\n=== ARCHITECTURAL MODEL SUMMARY ===")
{summary_code}
print("\\n🏗️ INTEGRATED ARCHITECTURAL MODEL COMPLETE!")
print("This is a unified, realistic building structure!")
'''