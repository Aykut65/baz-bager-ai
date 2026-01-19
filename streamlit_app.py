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
    /* Gemini Karanlık Tema ve Yazı Tipi */
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: #E3E3E3; font-family: 'Google Sans', sans-serif;}
    
    /* Öneri Butonları (Suggestion Chips) Tasarımı */
    .stButton>button {
        background-color: #1E1F20; color: #E3E3E3; border-radius: 12px;
        border: 1px solid #444746; padding: 15px; text-align: left; width: 100%;
        font-size: 14px; transition: 0.3s;
    }
    .stButton>button:hover {background-color: #333537; border-color: #8E918F;}
    
    /* Sohbet Balonları */
    [data-testid="stChatMessage"] {background-color: transparent; border: none; padding: 20px 0;}
    
    /* Sabit Alt Giriş Alanı */
    .stChatInputContainer {padding-bottom: 20px; background-color: #0E1117;}
    
    /* Hoşgeldin Mesajı Stili */
    .welcome-text {font-size: 40px; font-weight:
