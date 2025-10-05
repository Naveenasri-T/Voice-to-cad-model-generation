# �️ Voice-to-CAD Model Generator

An intelligent voice-controlled CAD application that converts voice commands or text descriptions into 2D and 3D models using AI and FreeCAD.

## ✨ Features

- **🗣️ Voice Input**: Record voice commands to generate CAD models
- **📝 Text Input**: Type descriptions for precise model generation  
- **🤖 AI-Powered**: Uses Groq AI (Llama-3.3-70b) for intelligent code generation
- **🎯 Universal Models**: Automatically detects and generates both 2D sketches and 3D models
## 📋 Prerequisites

Before starting, ensure you have:

1. **Python 3.8+** installed
2. **FreeCAD** installed and accessible from system PATH
3. **Microphone** for voice input (optional)
4. **Groq API Key** (free at [console.groq.com](https://console.groq.com))

## ⚡ Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/Voice-to-cad-model-generation.git
cd Voice-to-cad-model-generation
```

### 2. Setup Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Key
Create a `.env` file in the project root:
```bash
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

### 4. Run the Application
```bash
streamlit run main.py
```
The application will open in your browser at `http://localhost:8501`

## 🎯 How to Use

### Voice Input Method:
1. Click **🎙️ Start Recording** button
2. Speak your model description clearly
3. Click **⏹️ Stop Recording** when finished
4. Click **🚀 Generate Model** to create your CAD model

### Text Input Method:
1. Type your model description in the text area
2. Click **🚀 Generate Model** to create your CAD model

### Example Commands:
- **"Create a 2BHK house with modern layout"**
- **"Generate a simple cube with 10x10x10 dimensions"** 
- **"Make a cylinder with radius 5 and height 15"**
- **"Design a rectangular building with windows and doors"**
- **"Create a mechanical part with holes and fillets"**

## �️ Troubleshooting

### Common Issues:

**1. GROQ_API_KEY Error**
```
Error: GROQ_API_KEY not found in environment variables
```
**Solution**: Create a `.env` file with your API key:
```bash
echo "GROQ_API_KEY=your_api_key_here" > .env
```

**2. FreeCAD Not Opening**
```
Error: Could not launch FreeCAD
```
**Solution**: Ensure FreeCAD is installed and in your system PATH, or update the FreeCAD path in the application.

**3. Audio Recording Issues**
```
Error: Audio recording failed
```
**Solution**: Check microphone permissions and ensure your system has audio input capabilities.

**4. Module Import Errors**
```
Error: No module named 'streamlit'
```
**Solution**: Activate your virtual environment and install requirements:
```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```
Voice-to-cad-model-generation/
├── main.py                  # Main Streamlit application
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create this)
├── .gitignore              # Git ignore rules
├── config/
│   └── settings.py         # Configuration management
├── utils/
│   ├── logging_config.py   # Logging system
│   ├── exceptions.py       # Custom exceptions
│   └── code_cleaning.py    # AI code cleaning
├── tests/                  # Test suite
│   └── test_*.py          # Various test files
└── generated/              # Generated FreeCAD scripts
```

## 🚀 Advanced Usage

### Custom Model Generation:
1. Use detailed descriptions for better results
2. Specify dimensions and materials when needed
3. Include architectural terms for building models
4. The AI automatically detects if you want 2D sketches or 3D models

### Batch Processing:
You can generate multiple models by running different commands sequentially in the web interface.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Groq AI** for powerful language model API
- **FreeCAD** for excellent open-source CAD capabilities
- **Streamlit** for simple web application framework
- **OpenAI Whisper** for speech-to-text conversion

## 📞 Support

If you encounter any issues:

1. Check the **Troubleshooting** section above
2. Review the logs in the `../voice-to-cad-logs/` directory
3. Create an issue in the GitHub repository
4. Ensure all dependencies are properly installed

---

**Happy CAD Modeling! 🎉**

## 🔑 Requirements

- Python 3.8+
- FreeCAD installed
- Groq API key (in .env file)
- Required packages: streamlit, sounddevice, numpy, groq, python-dotenv

## 🎉 Success!

Your Voice-to-CAD application now generates **exact 2BHK house models** instead of basic geometric shapes!