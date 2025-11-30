# Testing Suite for Enhanced AI Design Engineer System

This directory contains comprehensive tests for the Voice-to-CAD model generation system with enhanced AI Design Engineer capabilities.

## 🚀 Quick Start

### Option 1: Guided Manual Testing (Recommended)
```bash
cd Voice-to-cad-model-generation
python tests/testing_guide.py
```

### Option 2: Automated Test Suite
```bash
cd Voice-to-cad-model-generation
python tests/test_master.py
```

### Option 3: Individual Tests
```bash
cd Voice-to-cad-model-generation
python tests/test_ai_design_engineer.py
```

## 📁 Test Files Overview

### Core Test Files
- **`test_master.py`** - Master test runner with comprehensive reporting
- **`test_ai_design_engineer.py`** - Main tests for enhanced AI capabilities
- **`testing_guide.py`** - Interactive guided testing session
- **`test_inputs.py`** - Collection of test input commands

### Specific Domain Tests
- **`test_2bhk.py`** - 2BHK house generation tests
- **`test_functionality.py`** - Core functionality validation
- **`test_main.py`** - Main application tests
- **`test_code_cleaning.py`** - Code quality and cleaning tests
- **`test_syntax_validation.py`** - Generated code syntax validation

### Advanced Tests
- **`test_enhanced_architecture.py`** - Architectural domain tests
- **`test_freecad_compatibility.py`** - FreeCAD compatibility tests
- **`test_transcription.py`** - Voice transcription tests
- **`test_voice_flow.py`** - End-to-end voice workflow tests
- **`test_unit_handling.py`** - Unit conversion and handling tests

## 🎯 Testing Categories

### 1. Quick Validation Tests
- Basic 2BHK house generation
- Simple office building
- Mechanical gear design
- Basic bridge structure

### 2. Architectural Domain Tests
- Modern 3BHK apartments
- Luxury villas with amenities
- Commercial office complexes
- Educational institutions

### 3. Engineering Domain Tests
- Civil engineering structures (bridges, columns)
- Mechanical components (gears, assemblies)
- Infrastructure layouts (roads, parking)

### 4. Advanced Integration Tests
- Parametric design validation
- Complex multi-domain projects
- Professional engineering standards
- Code quality and optimization

## 🧪 Test Input Examples

### Architectural
```
"Create a modern 3BHK apartment with balcony, parking area, and landscaped garden"
"Build a luxury 4BHK villa with swimming pool, double garage, and compound wall"
"Design a school building with 6 classrooms, library, and administrative office"
```

### Civil Engineering
```
"Design a concrete beam bridge with 3 spans and support pillars"
"Create a reinforced concrete column with foundation and beam connection"
"Build a retaining wall structure with proper drainage and reinforcement"
```

### Mechanical Engineering
```
"Generate a spur gear with 30 teeth and 5mm module"
"Design a simple mechanical press with frame and operating mechanism"
"Create a shaft assembly with bearings and coupling mechanism"
```

### Infrastructure
```
"Create a streetlight layout for a 50-meter road section"
"Design a parking layout with 10 car spaces and access road"
"Build a simple drainage channel with manholes and covers"
```

## ✅ Expected Test Results

All tests should verify:

1. **Parametric Design**: No hardcoded dimensions, all calculated from relationships
2. **Professional Standards**: Engineering best practices and standards applied
3. **Color Coding**: Components properly color-coded for identification
4. **Code Quality**: Clean, executable FreeCAD Python code
5. **Integration**: Unified designs, not separate disconnected boxes
6. **Documentation**: Comprehensive model summaries and descriptions

## 🔧 Prerequisites

Before running tests, ensure:

1. **Streamlit App Running**: `streamlit run main.py` (should be accessible at http://localhost:8513)
2. **Dependencies Installed**: `pip install -r requirements.txt`
3. **Enhanced AI System**: AI Design Engineer system prompt is active
4. **Python Environment**: Python 3.8+ with required packages

## 📊 Test Execution Modes

### Interactive Mode (Recommended for First-Time)
```bash
python tests/testing_guide.py
# Choose option 1 for guided testing
```

### Automated Suite
```bash
python tests/test_master.py
# Choose option 1 for full automation
```

### Individual Test
```bash
python tests/test_ai_design_engineer.py
# Runs specific test category
```

## 📋 Test Results

Test results are logged to:
- `logs/test_session.log` - Guided testing logs
- `logs/test_master_YYYYMMDD_HHMMSS.log` - Automated test logs
- `logs/ai_generation.log` - AI generation logs
- `logs/app.log` - General application logs

## 🐛 Troubleshooting

### Common Issues:

1. **Import Errors**
   ```bash
   # Ensure you're in the project root directory
   cd Voice-to-cad-model-generation
   python -m tests.test_master
   ```

2. **Streamlit Not Running**
   ```bash
   # Start the application first
   streamlit run main.py
   # Then run tests in another terminal
   ```

3. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Permission Issues**
   ```bash
   # On Windows, run as administrator or check file permissions
   ```

## 🌟 Best Practices

1. **Start with Quick Tests**: Use guided testing for initial validation
2. **Progressive Complexity**: Begin with simple tests, advance to complex
3. **Document Issues**: Note any failures in test logs for debugging
4. **Regular Testing**: Run tests after any system modifications
5. **Environment Consistency**: Use same Python environment for development and testing

## 📞 Support

For test-related issues:
1. Check logs in the `logs/` directory
2. Run individual tests for specific debugging
3. Verify all prerequisites are met
4. Ensure Enhanced AI Design Engineer system is active

## 🎉 Success Criteria

A successful test session should show:
- ✅ High success rate (>90%) for basic tests
- ✅ Generated code is syntactically correct
- ✅ Models follow parametric design principles
- ✅ Professional engineering standards applied
- ✅ Comprehensive documentation generated