"""
Technical Drawing Test Inputs for Voice-to-CAD System
===================================================

These inputs are specifically designed to generate detailed technical drawings
similar to the professional architectural drawings you provided.
"""

# =============================================================================
# 🏗️ TECHNICAL DRAWING TEST INPUTS (Like your examples)
# =============================================================================

# Based on your first image (Kitchen/Living area layout):
test_kitchen_living = """
Create a detailed floor plan for a kitchen and living area with precise dimensions and annotations. 
Include a kitchen with countertop, stove, and workspace, plus an adjacent living area. 
Generate technical drawings with all dimensions, room labels, and material specifications.
Add dimension lines, area calculations, and professional annotations.
"""

# Based on your second image (Multi-room residential layout):
test_detailed_house = """
Design a complete residential floor plan with multiple rooms, technical drawings, and professional dimensioning.
Include bedrooms, living room, kitchen, bathroom, and circulation areas.
Generate plan view, section view, and elevation drawings with all dimensions clearly marked.
Add room labels, areas, material specifications, and construction details.
Include door and window schedules with technical annotations.
"""

# Advanced technical drawing requests:
test_architectural_plan = """
Create a professional architectural drawing package for a 2BHK apartment including:
- Detailed floor plan with all dimensions and annotations
- Section drawings showing ceiling heights and structural details  
- Elevation drawings of all facades
- Door and window schedule with specifications
- Room areas and total built-up area calculations
- Material specifications and construction notes
- Technical drawing with proper line weights and dimension styles
"""

test_commercial_technical = """
Design a small office building with complete technical documentation including:
- Floor plan with room layouts and dimensions
- Structural plan showing columns and beams
- Electrical and plumbing layouts indicated
- Section drawings showing floor-to-floor heights
- Detailed construction drawings with specifications
- Professional dimensioning and annotation standards
- Title block with project information
"""

test_civil_engineering = """
Create detailed engineering drawings for a concrete beam bridge including:
- Structural plan view with all member dimensions
- Cross-section drawings showing reinforcement details
- Elevation view with support details and levels
- Foundation details with specifications
- Material list and construction notes
- Professional engineering drawing standards
- Complete dimensioning and technical annotations
"""

# =============================================================================
# 🎯 SPECIFIC FEATURES TO TEST
# =============================================================================

# Test 1: Detailed Dimensioning
dimension_test = """
Draw a simple rectangular room with complete dimensioning including:
- Overall dimensions (length x width)
- Wall thickness dimensions
- Door and window opening dimensions
- Height dimensions and level indicators
- Area calculations and room labels
- Professional dimension line formatting
"""

# Test 2: Multi-View Technical Drawings
multiview_test = """
Create a small house with multiple technical drawing views:
- Plan view showing room layout and dimensions
- Front and side elevation drawings
- Cross-section showing interior heights
- Detail drawings of key connections
- All views properly dimensioned and annotated
"""

# Test 3: Professional Annotations
annotation_test = """
Design a kitchen layout with comprehensive annotations including:
- Equipment labels and specifications
- Material callouts and finishes
- Dimension strings and measurements  
- Area calculations and room data
- Construction notes and details
- Professional drawing standards
"""

# =============================================================================
# 📐 COPY-PASTE READY INPUTS
# =============================================================================

# Quick professional drawing test:
quick_technical = "Create a 2BHK house floor plan with complete dimensions, room labels, and technical annotations"

# Detailed architectural package:
detailed_technical = "Generate professional architectural drawings for a 3BHK apartment including floor plan, sections, elevations, and all technical specifications with proper dimensioning"

# Engineering drawing test:
engineering_technical = "Design a concrete column with foundation showing all structural details, dimensions, reinforcement specifications, and professional engineering drawing standards"

# =============================================================================
# 🚀 USAGE INSTRUCTIONS FOR TECHNICAL DRAWINGS
# =============================================================================

"""
TO GET TECHNICAL DRAWINGS LIKE YOUR EXAMPLES:

1. COPY any of the above test inputs
2. PASTE into your app at http://localhost:8513  
3. The enhanced system will generate:
   ✅ 3D FreeCAD model
   ✅ Technical drawings with dimensions
   ✅ Professional annotations
   ✅ Room labels and specifications
   ✅ Multiple views (plan, section, elevation)
   ✅ Construction details and notes

RECOMMENDED START:
Copy this → "Create a 2BHK house floor plan with complete dimensions, room labels, and technical annotations"

ADVANCED TEST:
Copy this → detailed_technical (from above)

The system will generate FreeCAD code that creates both the 3D model 
AND technical drawings similar to your provided examples!
"""