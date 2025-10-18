import streamlit as st
import sys
import subprocess
import os
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

st.set_page_config(
    page_title="Voice to CAD Generator", 
    page_icon="🏗️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .input-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .voice-section {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin-bottom: 1rem;
    }
    .text-section {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin-bottom: 1rem;
    }
    .stButton > button {
        width: 100%;
        height: 3rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 8px;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def get_current_command():
    """Helper function to consistently get current command from session state"""
    # Simplified logic - just return the first non-empty command found
    voice_cmd = st.session_state.get('voice_command', '').strip()
    text_cmd = st.session_state.get('command_text', '').strip()
    
    # Return whichever is non-empty, prefer voice if both exist
    if voice_cmd:
        return voice_cmd
    elif text_cmd:
        return text_cmd
    else:
        return ''

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏗️ Voice to CAD Generator</h1>
        <p style="margin: 0; font-size: 1.1rem;">AI-Powered FreeCAD Model Generation with Voice Commands</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'timestamp' not in st.session_state:
        st.session_state.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if 'command_text' not in st.session_state:
        st.session_state.command_text = ""
    if 'voice_command' not in st.session_state:
        st.session_state.voice_command = ""
    if 'command_source' not in st.session_state:
        st.session_state.command_source = ""
    
    # Debug section (can be removed later)
    with st.expander("🔧 Debug Info", expanded=False):
        st.write("**Session State:**")
        st.write(f"- command_text: '{st.session_state.command_text}'")
        st.write(f"- voice_command: '{st.session_state.voice_command}'")
        st.write(f"- command_source: '{st.session_state.command_source}'")
        st.write(f"- get_current_command(): '{get_current_command()}'")
        st.write(f"- Command validation passes: {bool(get_current_command())}")
        
        if st.button("🔄 Reset Session", key="reset_session"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
            
        if st.button("🧪 Test Command Set", key="test_cmd"):
            st.session_state.command_text = "Create a simple test cube"
            st.session_state.command_source = "test"
            st.success("Test command set!")
            st.rerun()
            
        # Quick test for voice bypass
        if st.button("🎯 Set 2BHK Command", key="test_2bhk"):
            st.session_state.command_text = "Create 2BHK House"
            st.session_state.command_source = "test"
            st.success("2BHK command set!")
            st.rerun()
            
        # Force command to appear in generation section
        if st.button("🔄 Force Refresh Command", key="force_refresh"):
            current_cmd = get_current_command()
            if current_cmd:
                st.success(f"Force refreshing with: '{current_cmd}'")
            else:
                st.session_state.command_text = "Create 2BHK House"  
                st.session_state.command_source = "test"
                st.success("Set backup command")
            st.rerun()
            
        # Emergency fix button
        if st.button("🚨 Emergency Fix - Copy Voice to Generation", key="emergency_fix"):
            voice_cmd = st.session_state.get('voice_command', '').strip()
            if voice_cmd:
                st.session_state.command_text = voice_cmd
                st.success(f"Copied voice command to generation: '{voice_cmd}'")
                st.rerun()
            else:
                st.error("No voice command found to copy")
    
    # Check system status
    try:
        from config.settings import config
        config_ok = True
        ai_ok = bool(config.ai.groq.api_key)
    except:
        config_ok = False
        ai_ok = False
        
    if not config_ok:
        st.error("⚠️ Configuration error. Check your setup.")
        return
    if not ai_ok:
        st.error("⚠️ No API key found. Check your .env file.")
        return
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Input Methods Section
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.subheader("📝 Choose Your Input Method")
        
        # Tabs for different input methods
        voice_tab, text_tab = st.tabs(["🎤 Voice Input", "⌨️ Text Input"])
        
        with voice_tab:
            st.markdown('<div class="voice-section">', unsafe_allow_html=True)
            st.markdown("**🎙️ Record your voice command**")
            st.info("Click the microphone below and describe your CAD model")
            
            try:
                from services.voice_service import VoiceService
                voice_service = VoiceService()
                
                # Audio recorder
                audio_data = st.audio_input("Record your voice command")
                
                if audio_data:
                    # Save and transcribe audio
                    audio_path = voice_service.audio_dir / f"voice_command_{st.session_state.timestamp}.wav"
                    with open(audio_path, "wb") as f:
                        f.write(audio_data.getvalue())
                    
                    st.success("✅ Audio recorded successfully!")
                    
                    # Transcribe button
                    if st.button("🎯 Convert Speech to Text", key="transcribe_btn"):
                        with st.spinner("🔄 Converting speech to text..."):
                            try:
                                from config.settings import config
                                from services.ai_service import AIService
                                
                                ai_service = AIService(config.ai)
                                transcription = voice_service.transcribe_with_ai(str(audio_path), ai_service)
                                
                                st.write(f"DEBUG: Transcription result: '{transcription}'")
                                
                                if transcription and transcription.strip():
                                    # Store in both locations for redundancy
                                    st.session_state.voice_command = transcription.strip()
                                    st.session_state.command_text = transcription.strip()
                                    st.session_state.command_source = "voice"
                                    
                                    st.write(f"DEBUG: Set voice_command to: '{st.session_state.voice_command}'")
                                    st.write(f"DEBUG: Set command_text to: '{st.session_state.command_text}'")
                                    st.success(f"✅ Transcribed: {transcription}")
                                    # Force immediate update
                                    st.rerun()
                                else:
                                    st.error("❌ Could not transcribe audio. Please try recording again.")
                            except Exception as e:
                                st.error(f"❌ Transcription failed: {e}")
                                st.write(f"DEBUG: Exception details: {str(e)}")
                    
                    # Show current transcribed text if available
                    current_voice_cmd = st.session_state.get('voice_command', '')
                    if current_voice_cmd and current_voice_cmd.strip():
                        st.success(f"🎯 **Current voice command:** {current_voice_cmd}")
                        st.info("✅ Voice command is ready for generation!")
                        
                        
            except Exception as e:
                st.error(f"❌ Voice input error: {e}")
                st.info("💡 Voice input requires proper audio permissions and AI service")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with text_tab:
            st.markdown('<div class="text-section">', unsafe_allow_html=True)
            st.markdown("**✍️ Type your model description**")
            
            # Text input area - don't auto-populate from voice to prevent conflicts
            text_area_value = st.session_state.command_text if st.session_state.get('command_source') == 'text' else ""
            
            command_input = st.text_area(
                "Describe your CAD model:",
                value=text_area_value,
                placeholder="Example: Create a 2BHK apartment with living room, kitchen, and bedrooms\nExample: Design a simple mechanical gear\nExample: Build a school building with classrooms",
                height=120,
                key="text_input"
            )
            
            # Update session state when text input changes
            if command_input and command_input.strip():
                st.session_state.command_text = command_input.strip()
                st.session_state.voice_command = command_input.strip()  # Keep both in sync
                st.session_state.command_source = "text"
                st.success(f"✅ Command updated: {command_input}")
            elif not command_input and st.session_state.get('command_source') == 'text':
                # Clear if text was cleared manually
                st.session_state.command_text = ""
                st.session_state.voice_command = ""
                st.session_state.command_source = ""
                
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Current Command Display - Move outside the tabs
        current_command_col1 = get_current_command()
        
        if current_command_col1:
            st.markdown("### 🎯 Current Command")
            st.info(f"**Command:** {current_command_col1}")
            
            # Add a clear button
            if st.button("🗑️ Clear Command", key="clear_cmd"):
                st.session_state.command_text = ""
                st.session_state.voice_command = ""
                st.session_state.command_source = ""
                st.rerun()
        else:
            st.warning("💡 Please provide a command using voice or text input above")
    
    
    with col2:
        # Settings Panel
        st.markdown("### ⚙️ Generation Settings")
        
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            quality = st.selectbox(
                "🎨 Quality Level:",
                ["professional", "standard", "draft"],
                index=0,
                help="Professional: High detail, Standard: Balanced, Draft: Quick generation"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            model_type = st.selectbox(
                "📐 Model Type:",
                ["3d", "2d"],
                index=0,
                help="3D: Full 3D model, 2D: Flat/plan view"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Examples
        st.markdown("### 💡 Quick Examples")
        example_commands = [
            "Create a 2BHK apartment",
            "Design a school building", 
            "Build a simple cube",
            "Make a mechanical gear"
        ]
        
        for cmd in example_commands:
            if st.button(f"📝 {cmd}", key=f"example_{cmd}"):
                st.session_state.command_text = cmd
                st.session_state.voice_command = cmd
                st.session_state.command_source = "example"
                st.success(f"✅ Selected: {cmd}")
                st.rerun()
    
    # Generation Section - Final validation
    current_command = get_current_command()
    
    # Debug: Show what we're checking with improved output
    st.write(f"Debug: Final command validation - '{current_command}' (length: {len(current_command)})")
    st.write(f"Debug: Raw session_state.command_text = '{st.session_state.get('command_text', 'NOT_SET')}'")
    st.write(f"Debug: Raw session_state.voice_command = '{st.session_state.get('voice_command', 'NOT_SET')}'")
    st.write(f"Debug: Command source = '{st.session_state.get('command_source', 'NOT_SET')}'")
    st.write(f"Debug: get_current_command() result = '{get_current_command()}'")
    st.write(f"Debug: Boolean validation = {bool(current_command)}")
    
    if current_command:
        st.markdown("---")
        st.markdown("### 🚀 Generate Your CAD Model")
        
        if st.button("🚀 Generate FreeCAD Model", type="primary", use_container_width=True):
            
            try:
                with st.spinner("🔄 Generating your FreeCAD model..."):
                    from config.settings import config
                    from services.ai_service import AIService
                    from services.freecad_service import FreeCADService
                    from services.file_service import FileService
                    
                    config.create_directories()
                    ai_service = AIService(config.ai)
                    freecad_service = FreeCADService(config.freecad)
                    file_service = FileService(config.file, config.get_directories())
                    
                    generated_code = freecad_service.generate_model(
                        command=current_command, model_type=model_type, 
                        quality_level=quality, ai_service=ai_service
                    )
                    
                    if generated_code:
                        filepath = file_service.save_generated_code(generated_code, current_command)
                        if not filepath:
                            st.error("❌ Failed to save code")
                            return
                            
                        st.success(f"✅ Code saved to: {filepath}")
                        
                        execution_result = freecad_service.execute_code_and_open_freecad(generated_code, filepath)

                        # Always show the returned execution message to the user
                        if execution_result:
                            if execution_result.get("success"):
                                st.success("🎯 Model generated successfully!")
                            else:
                                st.error("❌ Generation saved but opening failed")

                            # Show detailed message and any execution errors
                            st.info(execution_result.get("message", "No message returned"))
                            if execution_result.get("execution_error"):
                                st.error(f"Execution error: {execution_result.get('execution_error')}")

                            # If GUI wasn't opened, provide manual instructions and helpers
                            if not execution_result.get("gui_opened"):
                                with st.expander("Manual steps to open in FreeCAD", expanded=True):
                                    st.write("Automatic FreeCAD launch didn't succeed on this machine. You can open the saved script manually or try supplying a custom FreeCAD executable path below.")
                                    st.markdown("**1) Manual command (Windows example):**")
                                    win_cmd = f'"C:\\Program Files\\FreeCAD\\bin\\FreeCAD.exe" "{filepath}"'
                                    st.code(win_cmd, language='bash')
                                    st.markdown("**2) Manual command (Linux/macOS example):**")
                                    unix_cmd = f'freecad "{filepath}"'
                                    st.code(unix_cmd, language='bash')

                                    st.markdown("**Open using a custom FreeCAD executable**")
                                    custom_exe = st.text_input("Path to FreeCAD executable (leave blank to skip)")
                                    if st.button("� Launch with custom executable") and custom_exe:
                                        try:
                                            subprocess.Popen([custom_exe, filepath], shell=False)
                                            st.success("✅ Launched FreeCAD using the custom executable (check your desktop).")
                                        except Exception as e:
                                            st.error(f"Failed to launch with provided executable: {e}")

                                    # Allow server-side execution as last-resort (dangerous)
                                    if st.checkbox("Run generated code on this server (only if you trust it)"):
                                        if st.button("⚠️ Execute on server now"):
                                            try:
                                                exec(generated_code, {})
                                                st.success("✅ Code executed on server (check server logs).")
                                            except Exception as e:
                                                st.error(f"Server execution failed: {e}")
                        
                        # Results display in columns
                        code_col, download_col = st.columns([3, 1])
                        
                        with code_col:
                            st.subheader("📋 Generated Code")
                            with st.expander("View FreeCAD Python Code", expanded=False):
                                st.code(generated_code, language='python')
                        
                        with download_col:
                            st.subheader("💾 Download")
                            st.download_button(
                                label="📥 Download Code",
                                data=generated_code,
                                file_name=f"freecad_model_{st.session_state.timestamp}.py",
                                mime="text/plain",
                                use_container_width=True
                            )
                    else:
                        st.error("❌ Failed to generate code")
                        
            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.info("💡 Generation section: No valid command found. Please set a command first.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 8px;">
        <p style="margin: 0; color: #6c757d;">
            🏗️ <strong>Voice to CAD Generator</strong> - AI-Powered FreeCAD Model Generation
            <br>💡 Speak or type your ideas, get professional CAD models
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()