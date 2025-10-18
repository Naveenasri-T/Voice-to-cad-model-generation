import streamlit as st
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

st.set_page_config(page_title="Voice to CAD Generator", page_icon="🏗️", layout="wide")

def main():
    st.title("🏗️ Voice to CAD Generator")
    st.write("AI-Powered FreeCAD Model Generation")
    

    
    # Check system status
    try:
        from config.settings import config
        config_ok = True
        ai_ok = bool(config.ai.groq.api_key)
    except:
        config_ok = False
        ai_ok = False
        
    if not config_ok:
        st.error("Configuration error. Check your setup.")
        return
    if not ai_ok:
        st.error("No API key found. Check your .env file.")
        return
    
    # Input section
    st.subheader("🎯 Create Your CAD Model")
    
    command = st.text_area(
        "Describe your model:",
        placeholder="Example: Create a 2BHK apartment, Create a school building, Create a simple cube",
        height=100
    )
    
    if not command:
        st.info("Enter a description to generate CAD model")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        quality = st.selectbox("Quality:", ["professional", "standard", "draft"])
    with col2:
        model_type = st.selectbox("Type:", ["3d", "2d"])
    
    if st.button("🚀 Generate Model", type="primary", use_container_width=True):
        
        try:
            with st.spinner("Generating FreeCAD model..."):
                from config.settings import config
                from services.ai_service import AIService
                from services.freecad_service import FreeCADService
                from services.file_service import FileService
                
                config.create_directories()
                ai_service = AIService(config.ai)
                freecad_service = FreeCADService(config.freecad)
                file_service = FileService(config.file, config.get_directories())
                
                generated_code = freecad_service.generate_model(
                    command=command, model_type=model_type, 
                    quality_level=quality, ai_service=ai_service
                )
                
                if generated_code:
                    filepath = file_service.save_generated_code(generated_code, command)
                    if not filepath:
                        st.error("Failed to save code")
                        return
                        
                    st.success(f"✅ Code saved to: {filepath}")
                    
                    execution_result = freecad_service.execute_code_and_open_freecad(generated_code, filepath)
                    
                    if execution_result.get("success"):
                        st.success("🎯 Model generated successfully!")
                        if execution_result.get("gui_opened"):
                            st.balloons()
                            st.info("🖥️ FreeCAD should open with your model!")
                    
                    st.subheader("Generated Code")
                    st.code(generated_code, language='python')
                    
                    st.download_button(
                        label="📥 Download Code",
                        data=generated_code,
                        file_name="freecad_model.py",
                        mime="text/plain"
                    )
                else:
                    st.error("❌ Failed to generate code")
                    
        except Exception as e:
            st.error(f"❌ Error: {e}")
    
    st.markdown("---")
    st.markdown("🏗️ **Voice to CAD Generator** - AI-Powered FreeCAD Model Generation")

if __name__ == "__main__":
    main()