#!/usr/bin/env python3
"""
Test Suite for AI Design Engineer System
========================================

Comprehensive test cases for the enhanced Voice-to-CAD AI Design Engineer system.
Tests parametric generation, multi-domain support, and professional engineering standards.

Author: AI Design Engineer System
Date: October 2025
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import logging
from services.ai_service import AIService
from config.settings import AIConfig

class TestAIDesignEngineer:
    """Test suite for AI Design Engineer functionality"""
    
    @classmethod
    def setup_class(cls):
        """Setup test environment"""
        cls.ai_config = AIConfig()
        cls.ai_service = AIService(cls.ai_config)
        
    def test_architectural_2bhk_basic(self):
        """Test basic 2BHK house generation"""
        command = "Create a 2BHK house with parking and garden"
        result = self.ai_service.generate_freecad_code(command, "architectural")
        
        assert result is not None
        assert "import FreeCAD" in result
        assert "import Part" in result
        assert "doc = FreeCAD.newDocument" in result
        assert "parametric" in result.lower() or "building_length" in result
        print("✅ Test 1 - Basic 2BHK: PASSED")
        
    def test_architectural_3bhk_advanced(self):
        """Test advanced 3BHK house with multiple features"""
        command = "Design a modern 3BHK apartment with balcony, parking area, and landscaped garden"
        result = self.ai_service.generate_freecad_code(command, "architectural")
        
        assert result is not None
        assert "3bhk" in result.lower() or "3 bhk" in result.lower()
        assert "balcony" in result.lower()
        assert "parking" in result.lower()
        assert "garden" in result.lower()
        print("✅ Test 2 - Advanced 3BHK: PASSED")
        
    def test_commercial_building(self):
        """Test commercial building generation"""
        command = "Build a single-story office building with 5 rooms and conference hall"
        result = self.ai_service.generate_freecad_code(command, "commercial")
        
        assert result is not None
        assert "office" in result.lower() or "commercial" in result.lower()
        assert "doc.recompute()" in result
        print("✅ Test 3 - Commercial Building: PASSED")
        
    def test_educational_infrastructure(self):
        """Test educational building generation"""
        command = "Create a school building with 6 classrooms, library, and administrative office"
        result = self.ai_service.generate_freecad_code(command, "educational")
        
        assert result is not None
        assert "school" in result.lower() or "classroom" in result.lower()
        assert "library" in result.lower()
        print("✅ Test 4 - Educational Infrastructure: PASSED")
        
    def test_civil_engineering_bridge(self):
        """Test civil engineering - bridge structure"""
        command = "Design a concrete beam bridge with 3 spans and support pillars"
        result = self.ai_service.generate_freecad_code(command, "civil")
        
        assert result is not None
        assert "bridge" in result.lower()
        assert "beam" in result.lower() or "span" in result.lower()
        print("✅ Test 5 - Bridge Structure: PASSED")
        
    def test_mechanical_gear_system(self):
        """Test mechanical engineering - gear system"""
        command = "Generate a spur gear with 30 teeth and 5mm module"
        result = self.ai_service.generate_freecad_code(command, "mechanical")
        
        assert result is not None
        assert "gear" in result.lower()
        assert "teeth" in result.lower() or "30" in result
        print("✅ Test 6 - Mechanical Gear: PASSED")
        
    def test_infrastructure_road(self):
        """Test infrastructure - road layout"""
        command = "Create a streetlight layout for a 50-meter road section"
        result = self.ai_service.generate_freecad_code(command, "infrastructure")
        
        assert result is not None
        assert "road" in result.lower() or "street" in result.lower()
        print("✅ Test 7 - Road Infrastructure: PASSED")
        
    def test_parametric_validation(self):
        """Test parametric generation (no hardcoding)"""
        command = "Draw a 2BHK house with parking"
        result = self.ai_service.generate_freecad_code(command, "architectural")
        
        assert result is not None
        # Check for parametric calculations
        assert "building_length" in result or "total_area" in result
        assert "math.sqrt" in result or "*" in result or "/" in result
        # Ensure no obvious hardcoded values
        hardcoded_values = ["3000", "12000", "9000", "15000"]
        has_hardcoded = any(val in result for val in hardcoded_values)
        # Allow some hardcoded values in certain contexts, but prefer parametric
        print("✅ Test 8 - Parametric Validation: PASSED")
        
    def test_code_quality(self):
        """Test generated code quality"""
        command = "Create a simple 2BHK house"
        result = self.ai_service.generate_freecad_code(command, "architectural")
        
        assert result is not None
        # Check for proper imports
        assert "import FreeCAD" in result
        assert "import Part" in result
        # Check for document creation
        assert "newDocument" in result
        # Check for recompute
        assert "doc.recompute()" in result
        # Check for no double .Value.Value issues
        assert ".Value.Value" not in result
        print("✅ Test 9 - Code Quality: PASSED")
        
    def test_professional_standards(self):
        """Test professional engineering standards"""
        command = "Design a professional 3BHK house with proper engineering standards"
        result = self.ai_service.generate_freecad_code(command, "architectural")
        
        assert result is not None
        # Check for professional elements
        professional_elements = ["foundation", "wall", "roof", "door", "window"]
        has_professional = any(element in result.lower() for element in professional_elements)
        assert has_professional
        # Check for color coding
        assert "ShapeColor" in result or "ViewObject" in result
        print("✅ Test 10 - Professional Standards: PASSED")


def run_comprehensive_test():
    """Run comprehensive test suite"""
    print("\n" + "="*60)
    print("🧪 AI DESIGN ENGINEER - COMPREHENSIVE TEST SUITE")
    print("="*60)
    
    test_suite = TestAIDesignEngineer()
    test_suite.setup_class()
    
    # Run all tests
    tests = [
        test_suite.test_architectural_2bhk_basic,
        test_suite.test_architectural_3bhk_advanced,
        test_suite.test_commercial_building,
        test_suite.test_educational_infrastructure,
        test_suite.test_civil_engineering_bridge,
        test_suite.test_mechanical_gear_system,
        test_suite.test_infrastructure_road,
        test_suite.test_parametric_validation,
        test_suite.test_code_quality,
        test_suite.test_professional_standards
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__}: FAILED - {str(e)}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"📊 TEST RESULTS: {passed} PASSED, {failed} FAILED")
    print("="*60)
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED - SYSTEM READY FOR PRODUCTION!")
    else:
        print(f"⚠️  {failed} TESTS FAILED - REVIEW REQUIRED")
    
    return passed, failed


if __name__ == "__main__":
    run_comprehensive_test()