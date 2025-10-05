"""
UI Components Module
Professional Streamlit UI components
"""

import streamlit as st
from typing import Dict, Any


class UIComponents:
    """Professional UI Components for Streamlit"""
    
    def __init__(self):
        pass
    
    def render_metric_card(self, title: str, value: str, help_text: str = ""):
        """Render a professional metric card"""
        st.metric(
            label=title,
            value=value,
            help=help_text
        )
    
    def render_status_indicator(self, status: str, message: str):
        """Render status indicator"""
        if status == "success":
            st.success(f"✅ {message}")
        elif status == "warning":
            st.warning(f"⚠️ {message}")
        elif status == "error":
            st.error(f"❌ {message}")
        else:
            st.info(f"ℹ️ {message}")
    
    def render_progress_bar(self, progress: float, text: str = ""):
        """Render progress bar with text"""
        progress_bar = st.progress(progress)
        if text:
            st.text(text)
        return progress_bar