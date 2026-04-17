import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

st.set_page_config(
    page_title="Voice to CAD Model Generation",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

        :root {
            --bg: #010312;
            --surface: #0f1424;
            --surface-alt: #131a2f;
            --border: #242b44;
            --primary: #8b5cf6;
            --primary-dark: #6d28d9;
            --secondary: #38bdf8;
            --text: #e2e8f0;
            --muted: #94a3b8;
            --accent-gradient: linear-gradient(135deg, #8b5cf6 0%, #38bdf8 100%);
        }

        * {
            font-family: 'Space Grotesk', sans-serif;
        }

        body, .stApp {
            background: var(--bg);
            color: var(--text);
        }

        .hero {
            background: var(--surface);
            padding: 2.5rem 3rem;
            border-radius: 20px;
            border: 1px solid var(--border);
            margin-bottom: 1.5rem;
            display: flex;
            flex-wrap: wrap;
            gap: 2rem;
            position: relative;
            overflow: hidden;
        }
        .hero::after {
            content: '';
            position: absolute;
            right: -120px;
            top: -120px;
            width: 280px;
            height: 280px;
            background: radial-gradient(circle, rgba(56,189,248,0.2), transparent 70%);
        }
        .hero h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
            color: #f8fafc;
        }
        .hero p {
            color: var(--muted);
            font-size: 1.1rem;
            max-width: 640px;
        }
        .hero-actions {
            margin-top: 1.5rem;
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }
        .primary-btn, .ghost-btn {
            padding: 0.9rem 1.6rem;
            border-radius: 999px;
            border: 1px solid transparent;
            font-weight: 600;
            text-decoration: none;
            color: inherit;
        }
        .primary-btn {
            background: var(--accent-gradient);
            color: #050510;
        }
        .ghost-btn {
            border-color: var(--border);
            color: var(--text);
        }

        .hero-panel {
            background: var(--surface-alt);
            border-radius: 16px;
            border: 1px solid var(--border);
            padding: 1.5rem;
            min-width: 260px;
            position: relative;
        }
        .hero-panel h3 {
            margin-bottom: 1rem;
            font-size: 1rem;
            color: var(--muted);
            letter-spacing: 0.08em;
        }
        .hero-panel .metric {
            display: flex;
            justify-content: space-between;
            margin-bottom: 1rem;
            font-size: 0.95rem;
            color: var(--muted);
        }
        .hero-panel .metric-value {
            font-size: 1.4rem;
            font-weight: 600;
            color: var(--text);
        }

        .card {
            background: var(--surface);
            border-radius: 18px;
            border: 1px solid var(--border);
            padding: 1.5rem 1.8rem;
            margin-bottom: 1.5rem;
        }
        .card h3 {
            margin-bottom: 1rem;
            font-size: 1.1rem;
        }
        .outline-card {
            border: 1px solid rgba(148,163,184,0.3);
            background: rgba(15,20,36,0.7);
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.8rem;
            border-bottom: none;
        }
        .stTabs [data-baseweb="tab"] {
            height: 48px;
            background: transparent;
            border: 1px solid var(--border);
            border-radius: 12px;
            color: var(--muted);
        }
        .stTabs [aria-selected="true"] {
            background: rgba(139,92,246,0.15);
            border-color: var(--primary);
            color: var(--text);
        }

        .stButton > button {
            border-radius: 12px;
            border: none;
            font-weight: 600;
            background: var(--accent-gradient);
            color: #050510;
            height: 3rem;
        }
        .stButton > button[kind="secondary"] {
            background: transparent;
            color: var(--text);
            border: 1px solid var(--border);
        }

        .stTextArea textarea,
        .stSelectbox > div,
        .stAudioRecorder > div {
            background: var(--surface-alt);
            border: 1px solid var(--border);
            color: var(--text);
            border-radius: 12px;
        }
        .stTextArea textarea {
            min-height: 160px;
        }

        .callout {
            background: rgba(56,189,248,0.12);
            border: 1px solid rgba(56,189,248,0.3);
            border-radius: 12px;
            padding: 1rem 1.2rem;
            margin-top: 1rem;
            color: var(--text);
        }

        .example-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 0.8rem;
        }
        .example-button {
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 0.75rem 1rem;
            background: rgba(19,26,47,0.8);
            text-align: left;
            cursor: pointer;
            font-size: 0.95rem;
        }
        .example-button:hover {
            border-color: var(--primary);
        }

        .divider {
            margin: 2rem 0;
            border-bottom: 1px solid var(--border);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_current_command() -> str:
    """Return the active command, preferring voice input when available."""
    voice_cmd = st.session_state.get("voice_command", "").strip()
    text_cmd = st.session_state.get("command_text", "").strip()
    return voice_cmd or text_cmd or ""


def render_hero_section() -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-text">
                <div class="ghost-btn" style="width:max-content; border-radius:999px; border:1px solid rgba(148,163,184,0.4); padding:0.45rem 1.2rem; font-size:0.85rem;">Voice to CAD Model Generation</div>
                <h1>Voice to CAD Model Generation</h1>
                <p>Describe spatial requirements, constraints, and intent. Voice to CAD AI orchestrates transcription, prompt engineering, and FreeCAD execution to deliver ready-to-edit files.</p>
                <div class="hero-actions">
                    <a class="primary-btn" href="#generate">Start generating</a>
                    <a class="ghost-btn" href="#examples">Browse examples</a>
                </div>
            </div>
            <div class="hero-panel">
                <h3>Live system status</h3>
                <div class="metric">
                    <span>Model latency</span>
                    <span class="metric-value">18s</span>
                </div>
                <div class="metric">
                    <span>Blueprints delivered</span>
                    <span class="metric-value">3,214</span>
                </div>
                <div class="metric">
                    <span>Success rate</span>
                    <span class="metric-value">98%</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_insight_row() -> None:
    cols = st.columns(3)
    insights = [
        ("Architectural + mechanical ready", "Auto-detects between 2D drawings and 3D solids with dimension guards"),
        ("Context-aware AI agents", "Voice transcription, plan synthesis, and FreeCAD execution run in sequence"),
        ("Production-grade exports", "Outputs stored with versioned metadata and FreeCAD packages"),
    ]
    for col, (title, detail) in zip(cols, insights):
        with col:
            st.markdown(
                f"<div class='card outline-card'><h3>{title}</h3><p style='color:var(--muted); margin-bottom:0;'>{detail}</p></div>",
                unsafe_allow_html=True,
            )


def render_command_summary(command: str) -> None:
    st.markdown(
        f"""
        <div class="callout">
            <strong>Command ready:</strong><br />
            {command}
        </div>
        """,
        unsafe_allow_html=True,
    )


def clear_command_state() -> None:
    st.session_state.command_text = ""
    st.session_state.voice_command = ""
    st.session_state.command_source = ""


def rerun_app() -> None:
    """Trigger a Streamlit rerun across legacy and current APIs."""
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        raise RuntimeError("No rerun API available in this Streamlit version.")


def main() -> None:
    if "timestamp" not in st.session_state:
        st.session_state.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.setdefault("command_text", "")
    st.session_state.setdefault("voice_command", "")
    st.session_state.setdefault("command_source", "")

    render_hero_section()
    render_insight_row()

    input_col, config_col = st.columns([1.8, 1])

    with input_col:
        with st.container():
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3>Input pipeline</h3>", unsafe_allow_html=True)

            voice_tab, text_tab = st.tabs(["Voice capture", "Text description"])

            with voice_tab:
                st.caption("Record a prompt describing geometry, adjacency, finishes, or constraints. Audio never leaves your workspace.")
                audio_data = st.audio_input("Record your description", label_visibility="collapsed")
                if audio_data:
                    from services.voice_service import VoiceService
                    from config.settings import config

                    voice_service = VoiceService()
                    audio_path = voice_service.audio_dir / f"voice_command_{st.session_state.timestamp}.wav"
                    with open(audio_path, "wb") as file_handle:
                        file_handle.write(audio_data.getvalue())

                    st.success("Audio captured. Transcribe below.")
                    if st.button("Transcribe voice", key="transcribe_voice", use_container_width=True):
                        from services.ai_service import AIService

                        ai_service = AIService(config.ai)
                        transcription = voice_service.transcribe_with_ai(str(audio_path), ai_service)
                        if transcription:
                            st.session_state.voice_command = transcription.strip()
                            st.session_state.command_text = transcription.strip()
                            st.session_state.command_source = "voice"
                            rerun_app()
                        else:
                            st.error("Transcription failed. Please try again with clearer audio.")

            with text_tab:
                st.caption("Type a precise requirement. Include measurements, room adjacencies, furniture placement, or mechanical specs.")
                value = st.text_area(
                    "Describe the model",
                    value=st.session_state.command_text,
                    height=180,
                    placeholder="Example: Generate a 3D model of an R&D lab with two rows of workstations, ventilation shafts, and an equipment room"
                )
                if value != st.session_state.command_text:
                    st.session_state.command_text = value.strip()
                    st.session_state.voice_command = value.strip()
                    st.session_state.command_source = "text"
                    rerun_app()

            st.markdown("</div>", unsafe_allow_html=True)

        active_command = get_current_command()
        if active_command:
            render_command_summary(active_command)
        else:
            st.markdown(
                "<div class='callout' style='border-color:rgba(248,113,113,0.5); background:rgba(248,113,113,0.1);'><strong>No command detected.</strong><br />Upload audio or type instructions to begin.</div>",
                unsafe_allow_html=True,
            )

    with config_col:
        with st.container():
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3>Generation controls</h3>", unsafe_allow_html=True)
            quality = st.selectbox("Quality level", ["professional", "standard", "draft"], index=0)
            model_type = st.selectbox("Output type", ["3d", "2d"], index=0)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card' id='examples'>", unsafe_allow_html=True)
        st.markdown("<h3>Reference prompts</h3>", unsafe_allow_html=True)
        example_commands = [
            "Design a modular 2BHK apartment with balcony access from each room",
            "Create a 3D concept for an L-shaped office desk with cable channels",
            "Generate a hospital ward layout with ten beds, storage, and nurse station",
            "Draft a compact computer lab with ventilation ducts and raised flooring"
        ]
        for idx, sample in enumerate(example_commands):
            if st.button(sample, key=f"example_{idx}"):
                st.session_state.command_text = sample
                st.session_state.voice_command = sample
                st.session_state.command_source = "example"
                rerun_app()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3>Session utilities</h3>", unsafe_allow_html=True)
        if st.button("Reset session", type="secondary", use_container_width=True):
            for key in ["timestamp", "command_text", "voice_command", "command_source"]:
                st.session_state[key] = ""
            rerun_app()
        if st.button("Clear command", use_container_width=True):
            clear_command_state()
            rerun_app()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='divider' id='generate'></div>", unsafe_allow_html=True)

    current_command = get_current_command()
    if not current_command:
        st.info("Provide a command using voice or text to start generating a blueprint.")
        return

    st.markdown("<div class='card'><h3>Generate blueprint</h3>", unsafe_allow_html=True)
    st.write("The system will orchestrate AI code generation and FreeCAD execution. This may take a minute depending on complexity.")

    if st.button("Run pipeline", use_container_width=True):
        try:
            from config.settings import config
            from services.ai_service import AIService
            from services.freecad_service import FreeCADService
            from services.file_service import FileService
            from pathlib import Path

            with st.spinner("Generating FreeCAD blueprint script..."):
                config.create_directories()
                ai_service = AIService(config.ai)
                freecad_service = FreeCADService(config.freecad)
                file_service = FileService(config.file, config.get_directories())

                generated_code = freecad_service.generate_model(
                    command=current_command,
                    model_type=model_type,
                    quality_level=quality,
                    ai_service=ai_service
                )

                if not generated_code:
                    st.error("AI could not produce valid code. Refine the command and try again.")
                    return

                filepath = file_service.save_generated_code(generated_code, current_command)

                # filepath is now a Path object; guard against save failure
                if filepath and filepath.name:
                    st.success(f"✅ Blueprint script saved: **{filepath.name}**")
                else:
                    st.warning("⚠️ Script generated but could not be saved to disk.")

                # Show generated code preview
                with st.expander("📄 View generated FreeCAD script", expanded=False):
                    st.code(generated_code, language="python")

                # Download button
                st.download_button(
                    label="⬇️ Download .py script",
                    data=generated_code,
                    file_name=filepath.name if filepath and filepath.name else "blueprint.py",
                    mime="text/plain",
                )

            with st.spinner("Launching FreeCAD..."):
                execution_result = freecad_service.execute_code_and_open_freecad(
                    generated_code, str(filepath) if filepath and filepath.name else None
                )
                if isinstance(execution_result, dict):
                    msg = execution_result.get("message", "")
                    if execution_result.get("success"):
                        st.success(f"🚀 {msg}")
                    else:
                        st.info(f"ℹ️ {msg}")
                elif execution_result:
                    st.code(execution_result)
                else:
                    st.info("FreeCAD process finished (no output).")

        except Exception as exc:
            st.error(f"Generation failed: {exc}")

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
