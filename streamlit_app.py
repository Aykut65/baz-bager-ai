import streamlit as st
from groq import Groq
import random
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text

# --- 1. SAYFA YAPILANDIRMASI ---
st.set_page_config(
    page_title="BAZ BAGER: GOLD",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. PREMIUM CSS TASARIMI (Görsel Düzenleme) ---
st.markdown("""
    <style>
    /* Ana arka plan ve yazı renkleri */
    .stApp {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: #ffffff;
    }
    /* Başlık stili */
    h1 {
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        background: -webkit-linear-gradient(#eee, #333);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 10px rgba(255,255,255,0.3);
    }
    /* Mesaj balonları */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    /* Alt bilgi */
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        font-size: 12px;
        color: gray;
    }
    </style>
