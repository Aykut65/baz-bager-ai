import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. GEMINI BİREBİR TASARIM (CSS) ---
st.set_page_config(page_title="Gemini - BAZ BAGER", page_icon="🦅", layout="centered")

st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: #E3E3E3; font-family: 'Google Sans', sans-serif;}
    .welcome-title {font-size: 42px; font-weight: 500; margin-top: 50px; color: white;}
    .welcome-subtitle {font-size: 26px; font-weight: 400; color: #8E918F; margin-bottom: 40px;}
    .stButton>button {
        background-color: #1E1F20; color: #E3E3E3; border-radius: 12px;
        border: 1px solid #444746; padding: 18px; text-align: left; width: 100%;
        font-size: 15px; transition: 0.3s; margin-bottom: 10px;
    }
    .stButton>button:hover {background-color: #333537; border-color: #8E918F;}
    [data-testid="stChatMessage"] {background-color: transparent; border: none; padding: 15px 0;}
    .stChatInputContainer {padding-bottom: 30px; background-color: #0E1117;}
</style>
""", unsafe_allow_html=True)

# --- 2. SİSTEM ÇEKİRDE
