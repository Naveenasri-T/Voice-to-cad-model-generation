"""
Test Input Commands for AI Design Engineer System
==============================================

Copy and paste these commands into the Streamlit application for testing.
Each section tests different engineering domains and capabilities.
"""

# =============================================================================
# 🏠 ARCHITECTURAL TEST INPUTS
# =============================================================================

# Test 1: Basic Residential
test_1_basic_2bhk = "Create a 2BHK house with parking and garden"

# Test 2: Advanced Residential  
test_2_advanced_3bhk = "Design a modern 3BHK apartment with balcony, parking area, and landscaped garden"

# Test 3: Luxury Villa
test_3_luxury_villa = "Build a luxury 4BHK villa with swimming pool, double garage, and compound wall"

# Test 4: Compact Apartment
test_4_compact_1bhk = "Design a compact 1BHK apartment for urban living with efficient space utilization"

# =============================================================================
# 🏢 COMMERCIAL & INSTITUTIONAL TEST INPUTS  
# =============================================================================

# Test 5: Office Building
test_5_office = "Build a single-story office building with 5 rooms and conference hall"

# Test 6: School Building
test_6_school = "Create a school building with 6 classrooms, library, and administrative office"

# Test 7: Hospital Layout
test_7_hospital = "Design a small clinic with reception, consultation rooms, and pharmacy"

# Test 8: Shopping Complex
test_8_shopping = "Create a shopping complex with multiple retail units and central corridor"

# =============================================================================
# 🌉 CIVIL ENGINEERING TEST INPUTS
# =============================================================================

# Test 9: Bridge Structure
test_9_bridge = "Design a concrete beam bridge with 3 spans and support pillars"

# Test 10: Structural Elements
test_10_structure = "Create a reinforced concrete column with foundation and beam connection"

# Test 11: Retaining Wall
test_11_retaining = "Build a retaining wall structure with proper drainage and reinforcement"

# =============================================================================
# ⚙️ MECHANICAL ENGINEERING TEST INPUTS
# =============================================================================

# Test 12: Gear System
test_12_gear = "Generate a spur gear with 30 teeth and 5mm module"

# Test 13: Mechanical Press
test_13_press = "Design a simple mechanical press with frame and operating mechanism"

# Test 14: Shaft Assembly
test_14_shaft = "Create a shaft assembly with bearings and coupling mechanism"

# =============================================================================
# 🛣️ INFRASTRUCTURE TEST INPUTS
# =============================================================================

# Test 15: Road Layout
test_15_road = "Create a streetlight layout for a 50-meter road section"

# Test 16: Parking Layout
test_16_parking = "Design a parking layout with 10 car spaces and access road"

# Test 17: Drainage System
test_17_drainage = "Build a simple drainage channel with manholes and covers"

# =============================================================================
# 🧪 PARAMETRIC & QUALITY TEST INPUTS
# =============================================================================

# Test 18: Parametric Validation
test_18_parametric = "Draw a house that automatically calculates all dimensions based on room requirements"

# Test 19: Complex Integration
test_19_complex = "Create a modern 3BHK villa with master bedroom, two bedrooms, living room, kitchen, dining area, two bathrooms, balcony, parking for two cars, and landscaped garden with compound wall"

# Test 20: Engineering Standards
test_20_standards = "Design a professional residential building following Indian construction standards"

# =============================================================================
# 📋 QUICK START TESTS (Start with these)
# =============================================================================

quick_test_1 = "Draw a 2BHK house with parking"
quick_test_2 = "Create a simple office building" 
quick_test_3 = "Design a mechanical gear"
quick_test_4 = "Build a concrete bridge"

# =============================================================================
# 🚀 USAGE INSTRUCTIONS
# =============================================================================

"""
HOW TO USE THESE TESTS:

1. Open the Streamlit application at http://localhost:8513
2. Copy any test command from above
3. Paste it into the text input field
4. Click "Generate CAD Model"
5. Observe the generated FreeCAD Python code
6. Verify:
   ✅ Parametric calculations (no hardcoded values)
   ✅ Professional engineering standards
   ✅ Proper color coding and labeling
   ✅ Clean, error-free FreeCAD code
   ✅ Integrated building design (not separate boxes)

EXPECTED RESULTS:
- All dimensions calculated from relationships
- Professional engineering ratios applied
- Color-coded components for easy identification
- Comprehensive model summaries
- Clean, executable FreeCAD Python code

START WITH: quick_test_1 for basic validation
ADVANCED: test_19_complex for comprehensive testing
"""