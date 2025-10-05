import streamlit as st
import sys
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Page config
st.set_page_config(
    page_title="Professional Voice to CAD Generator",
    page_icon="🏗️",
    layout="wide"
)

def main():
    # Header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1f77b4 0%, #2ca02c 100%); 
                padding: 2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;">
        <h1>🏗️ Professional Voice to CAD Generator</h1>
        <p>AI-Powered FreeCAD Model Generation</p>
    </div>
    """, unsafe_allow_html=True)
    

    
    # System Status
    st.markdown("### 📊 System Status")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        try:
            from config.settings import config
            st.success("⚙️ Configuration")
            config_ok = True
        except ImportError as e:
            st.error("⚙️ Configuration")
            st.error(f"Error: {e}")
            config_ok = False
    
    with col2:
        try:
            from services.ai_service import AIService
            from config.settings import config
            # Check if API key is available from config
            if config.ai.groq.api_key:
                st.success("🤖 AI Service")
                ai_ok = True
            else:
                st.warning("🤖 AI Service - No API Key")
                ai_ok = False
        except ImportError as e:
            st.error("🤖 AI Service")
            st.error(f"Error: {e}")
            ai_ok = False
    
    with col3:
        try:
            from services.freecad_service import FreeCADService
            from config.settings import config
            # Try to initialize FreeCAD service to check if it works
            freecad_service = FreeCADService(config.freecad)
            if freecad_service.freecad_available:
                st.success("🏗️ FreeCAD Service (Available)")
            else:
                st.warning("🏗️ FreeCAD Service (Code Generation Only)")
            freecad_ok = True
        except Exception as e:
            st.error("🏗️ FreeCAD Service")
            st.error(f"Error: {e}")
            freecad_ok = False
    
    with col4:
        try:
            import sounddevice
            st.success("🎤 Audio")
        except ImportError:
            st.warning("🎤 Audio")
    
    # Input section
    st.markdown("## 🎯 Create Your CAD Model")
    
    # Voice input section
    col_input1, col_input2 = st.columns([3, 1])
    
    with col_input1:
        command = st.text_area(
            "Describe your CAD model:",
            placeholder="Example: Create a modern 2BHK apartment with living room (4m x 5m), kitchen (3m x 3m), master bedroom (3.5m x 4m), second bedroom (3m x 3m), and bathroom",
            height=100,
            key="text_input"
        )
    
    with col_input2:
        st.markdown("### 🎤 Voice Input")
        
        if st.button("🎙️ Start Recording", use_container_width=True):
            try:
                import sounddevice as sd
                import numpy as np
                from scipy.io.wavfile import write
                import tempfile
                import os
                
                # Recording parameters
                duration = 30  # seconds
                sample_rate = 44100
                
                with st.spinner(f"🎤 Recording for {duration} seconds..."):
                    # Record audio
                    audio_data = sd.rec(int(duration * sample_rate), 
                                      samplerate=sample_rate, 
                                      channels=1, 
                                      dtype='float64')
                    sd.wait()  # Wait until recording is finished
                
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                    write(tmp_file.name, sample_rate, (audio_data * 32767).astype(np.int16))
                    
                    # Transcribe audio (placeholder for now)
                    st.success("✅ Recording completed!")
                    st.info("🔄 Voice-to-text feature coming soon! Please use text input for now.")
                    
                    # Clean up
                    os.unlink(tmp_file.name)
                    
            except ImportError:
                st.error("❌ Voice recording requires additional packages. Using text input only.")
            except Exception as e:
                st.error(f"❌ Recording failed: {e}")
        
        st.markdown("---")
        st.markdown("**Quick Examples:**")
        
        example_commands = [
            "2BHK apartment",
            "Modern house", 
            "Simple cube",
            "Office building"
        ]
        
        for cmd in example_commands:
            if st.button(f"📝 {cmd}", use_container_width=True):
                st.session_state.text_input = f"Create a {cmd}"
                st.rerun()
    
    if not command:
        st.info("Please enter a description of the CAD model you want to create.")
        return
    
    # Generation section
    st.markdown("## 🚀 Generate Model")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        quality = st.selectbox("Quality Level:", ["professional", "standard", "draft"])
    with col2:
        model_type = st.selectbox("Model Type:", ["3d", "2d"])
    with col3:
        # API Test Button
        if st.button("🧪 Test API", help="Test if your Groq API key is working"):
            try:
                from config.settings import config
                from services.ai_service import AIService
                
                if not config.ai.groq.api_key:
                    st.error("No API key found!")
                else:
                    ai_service = AIService(config.ai)
                    # Simple test request
                    test_result = ai_service.generate_freecad_code("create a simple cube", "3d", "draft")
                    if test_result:
                        st.success("✅ API is working!")
                    else:
                        st.error("❌ API test failed - check rate limits")
            except Exception as e:
                st.error(f"❌ API test error: {e}")
    
    if st.button("🚀 Generate FreeCAD Code", type="primary", use_container_width=True):
        if not config_ok:
            st.error("Cannot generate - configuration error")
            return
        if not ai_ok:
            st.error("Cannot generate - AI service not available. Please configure your Groq API key.")
            return
        if not freecad_ok:
            st.error("Cannot generate - FreeCAD service error")
            return
        
        try:
            with st.spinner("Generating professional FreeCAD code..."):
                # Import services
                from config.settings import config
                from services.ai_service import AIService
                from services.freecad_service import FreeCADService
                from services.file_service import FileService
                
                # Initialize
                config.create_directories()
                ai_service = AIService(config.ai)
                freecad_service = FreeCADService(config.freecad)
                file_service = FileService(config.file, config.get_directories())
                
                # Generate
                generated_code = freecad_service.generate_model(
                    command=command,
                    model_type=model_type,
                    quality_level=quality,
                    ai_service=ai_service
                )
                
                # Check if we got any response from AI (even if validation failed)
                raw_response = None
                try:
                    # Try to get raw response for debugging
                    ai_service = AIService(config.ai)
                    prompt = f"Create FreeCAD Python code for: {command}"
                    if ai_service.client:
                        response = ai_service.client.chat.completions.create(
                            model=config.ai.groq.model,
                            messages=[{"role": "user", "content": prompt}],
                            max_tokens=2000,
                            temperature=0.1
                        )
                        if response and response.choices:
                            raw_response = response.choices[0].message.content
                except:
                    pass
                
                if generated_code:
                    # Save to generated folder
                    filepath = file_service.save_generated_code(generated_code, command)
                    
                    if not filepath:
                        st.error("Failed to save generated code")
                        return
                        
                    st.info(f"📁 Code saved to: `{filepath}`")
                    
                    # Execute and try to open FreeCAD
                    execution_result = freecad_service.execute_code_and_open_freecad(
                        generated_code, 
                        filepath
                    )
                    
                    if execution_result["success"]:
                        st.success(f"✅ {execution_result['message']}")
                        
                        if execution_result.get("executed") and execution_result.get("gui_opened"):
                            st.balloons()  # Celebration animation!
                            st.success("🎯 **SUCCESS!** FreeCAD launched automatically with your 3D model!")
                            st.info("🖥️ **Check your desktop** - FreeCAD should be opening with your model loaded!")
                            st.markdown("### 🎉 **Your 2BHK Model is Ready!**")
                            st.markdown("""
                            **What happened:**
                            - ✅ AI generated your FreeCAD code
                            - ✅ Code saved to file  
                            - ✅ FreeCAD launched automatically
                            - ✅ Your 3D model is loading in FreeCAD
                            
                            **No manual steps needed!** 🚀
                            """)
                        elif execution_result.get("executed"):
                            st.success("🎯 Model created successfully!")
                            st.info("� FreeCAD may be running in the background")
                        else:
                            st.info("📁 Code ready - you can run it manually in FreeCAD if needed")
                    else:
                        st.warning(f"⚠️ Code generated but: {execution_result.get('message', 'Unknown error')}")
                    
                    # Display
                    st.markdown("### 📄 Generated Code")
                    st.code(generated_code, language='python')
                    
                    # Download
                    st.download_button(
                        label="📥 Download Python File",
                        data=generated_code,
                        file_name="freecad_model.py",
                        mime="text/plain"
                    )
                    
                    # Instructions
                    st.markdown("""
                    ### � **Automatic Execution:**
                    The application automatically:
                    1. ✅ **Generates** professional FreeCAD code
                    2. ✅ **Saves** the code to a file
                    3. ✅ **Launches** FreeCAD automatically  
                    4. ✅ **Loads** your 3D model in the viewport
                    
                    ### 📖 **Manual Option** (if needed):
                    If FreeCAD doesn't auto-launch:
                    1. Open FreeCAD manually
                    2. Go to **Macro → Macros...**
                    3. Load and execute the downloaded file
                    """)
                    
                    # Analysis
                    analysis = freecad_service.analyze_generated_code(generated_code)
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown("**📊 Code Statistics:**")
                        stats = analysis.get('statistics', {})
                        for key, value in stats.items():
                            st.text(f"• {key.replace('_', ' ').title()}: {value}")
                    
                    with col_b:
                        st.markdown("**✅ Quality Checks:**")
                        quality_checks = analysis.get('quality', {})
                        for key, value in quality_checks.items():
                            status = "✅" if value else "❌"
                            st.text(f"{status} {key.replace('_', ' ').title()}")
                elif raw_response:
                    st.warning("⚠️ AI generated code but validation failed")
                    st.markdown("### 🔍 Raw AI Response (Debug)")
                    st.code(raw_response, language='python')
                    st.info("The AI is working but generated code has syntax issues. This might help debug the problem.")
                    
                else:
                    st.error("❌ Failed to generate code")
                    
                    # Show potential reasons  
                    st.markdown("### 🔍 Possible Issues:")
                    st.markdown("""
                    **Common causes for generation failure:**
                    - 🚫 **API Rate Limit**: Your Groq API key may have hit the rate limit
                    - 🔑 **API Key Issues**: Check if your API key in .env file is valid
                    - 🌐 **Network Issues**: Connection to Groq API may be slow/failed
                    - 📝 **Description Issues**: Try a simpler or more specific description
                    - 💡 **Model Issues**: The AI model may be temporarily unavailable
                    """)
                    
                    # Show current API key status
                    if config.ai.groq.api_key:
                        api_key_preview = config.ai.groq.api_key[:10] + "..." + config.ai.groq.api_key[-5:]
                        st.info(f"🔑 Using API Key: {api_key_preview}")
                    else:
                        st.error("🔑 No API key found in configuration!")
                    
                    # Suggestions
                    st.markdown("### 💡 Try These Solutions:")
                    st.markdown("""
                    1. **Wait a few minutes** and try again (rate limit reset)
                    2. **Simplify your description** (e.g., "Create a simple cube")
                    3. **Check your .env file** has a valid GROQ_API_KEY
                    4. **Test with a basic request** first
                    """)
                    
        except Exception as e:
            st.error(f"❌ Generation failed: {e}")
            
            # Show detailed error information
            error_str = str(e).lower()
            if "rate_limit" in error_str or "quota" in error_str:
                st.warning("🚫 **API Rate Limit Exceeded** - Please wait and try again later")
            elif "api_key" in error_str or "unauthorized" in error_str:
                st.error("🔑 **API Key Error** - Check your Groq API key in .env file")
            elif "timeout" in error_str:
                st.warning("⏱️ **Request Timeout** - API is slow, try again")
            elif "connection" in error_str:
                st.warning("🌐 **Connection Error** - Check internet connection")
            else:
                st.error(f"🔧 **Technical Error**: {e}")
                st.info("Please check the logs for more details")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <strong>🏗️ Professional Voice to CAD Generator</strong> | 
        Client-Ready AI Solution | Version 2.0
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()