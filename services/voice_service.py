"""
Voice Input Service Module
Handles audio recording and speech-to-text conversion
"""

import streamlit as st
import tempfile
import os
from pathlib import Path
import logging
from typing import Optional

class VoiceService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.audio_dir = Path("audio")
        self.audio_dir.mkdir(exist_ok=True)
    
    def create_audio_recorder(self) -> Optional[str]:
        """Create audio recorder widget and return audio file path if recorded"""
        try:
            # Use streamlit-audio-recorder or similar for voice input
            audio_data = st.audio_input("🎤 Record your voice command")
            
            if audio_data:
                # Save audio to temporary file
                timestamp = st.session_state.get('timestamp', 'temp')
                audio_path = self.audio_dir / f"voice_command_{timestamp}.wav"
                
                with open(audio_path, "wb") as f:
                    f.write(audio_data.getvalue())
                
                st.success("✅ Audio recorded successfully!")
                return str(audio_path)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Audio recording failed: {e}")
            st.error(f"❌ Recording failed: {e}")
            return None
    
    def transcribe_with_ai(self, audio_path: str, ai_service) -> Optional[str]:
        """Transcribe audio using AI service"""
        try:
            if not ai_service:
                st.error("AI service not available for transcription")
                return None
            
            with st.spinner("🎯 Converting speech to text..."):
                transcription = ai_service.transcribe_audio(audio_path)
                
                if transcription:
                    st.success("✅ Voice successfully converted to text!")
                    return transcription
                else:
                    st.error("❌ Could not transcribe audio")
                    return None
                    
        except Exception as e:
            self.logger.error(f"Transcription failed: {e}")
            st.error(f"❌ Transcription failed: {e}")
            return None