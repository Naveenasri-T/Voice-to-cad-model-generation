import streamlit as st
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os
import subprocess
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

FREECAD_PATH = r"C:\Program Files\FreeCAD 1.0\bin\FreeCAD.exe"

def record_audio(filename="command.wav", duration=5, fs=44100):
    st.info("🎙 Recording... Speak now!")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
    sd.wait()
    wav.write(filename, fs, audio)
    st.success(f"✅ Recording complete: {filename}")

def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3"
        )
    return transcription.text.lower()

def _clean_ai_code(raw_code: str) -> str:
    if not raw_code:
        return ""
    cleaned = re.sub(r"^```(?:python)?\s*", "", raw_code, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.replace("```", "")
    return cleaned.strip()

def generate_script_with_ai(command_text: str) -> str:
    prompt = f"""
    You are a FreeCAD Python generator.
    Convert the following description into FreeCAD Python code that creates the 3D object.

    Rules:
    - Always import: import FreeCAD, Part, Draft, FreeCADGui
    - Always create a new document: doc = FreeCAD.newDocument("Model")
    - Allowed geometry functions:
        Part.makeBox(length, width, height)
        Part.makeCylinder(radius, height)
        Part.makeSphere(radius)
        Draft.makeRectangle(length, width)
        Draft.makeCircle(radius)
        Part.makeCompound([obj1, obj2, ...])
    - Use Placement for positioning objects:
        obj_feature.Placement.Base = FreeCAD.Vector(x, y, z)
    - NEVER use .move(), .translate(), or similar methods on solids.
    - Assign each object to a variable, then add it with:
        obj_feature = doc.addObject("Part::Feature", "Name")
        obj_feature.Shape = obj
    - Always end with:
        doc.recompute()
        FreeCADGui.activeDocument().activeView().viewAxometric()
        FreeCADGui.SendMsgToActiveView('ViewFit')

    Description: "{command_text}"
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_completion_tokens=2048
        )
    except Exception as e:
        st.error(f"LLM request failed: {e}")
        return ""
    raw_code = ""
    try:
        raw_code = response.choices[0].message.content
    except Exception:
        raw_code = str(response)
    return _clean_ai_code(raw_code)

def run_freecad(script_path: str):
    try:
        subprocess.Popen([FREECAD_PATH, script_path], shell=False)
    except Exception as e:
        st.error(f"Could not launch FreeCAD: {e}")

st.title("🎙 Voice/Text → FreeCAD 3D Model")

if st.button("🎙 Start Recording"):
    record_audio("command.wav", duration=5)
    try:
        command_text = transcribe_audio("command.wav")
        st.success(f"🗣 You said: *{command_text}*")
        st.session_state["voice_command"] = command_text
    except Exception as e:
        st.error(f"Error: {str(e)}")

text_command = st.text_input("Or type your command:", placeholder="e.g., Draw a water bottle")

if st.button("🏗 Build Shape"):
    command_text = text_command.lower() if text_command else st.session_state.get("voice_command", "")
    if not command_text:
        st.error("❌ Please provide a command (voice or text).")
    else:
        script = generate_script_with_ai(command_text)
        if script:
            with open("draw_dynamic.py", "w", encoding="utf-8") as f:
                f.write(script + "\n")
            run_freecad(os.path.abspath("draw_dynamic.py"))
            st.success("✅ 3D model launched in FreeCAD.")
        else:
            st.error("❌ Could not generate FreeCAD script.")
