import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. GEMINI TARZI ULTRA MINIMAL TASARIM ---
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="centered")

st.markdown("""
<style>
    /* Gemini minimalist görünümü */
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: #E3E3E3;}
    
    /* Sohbet Balonları */
    [data-testid="stChatMessage"] {
        background-color: transparent;
        border: none;
        padding: 20px 0px;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Giriş Alanı Tasarımı */
    .stChatInputContainer {
        padding-bottom: 30px;
        background-color: #0E1117;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SİSTEM ÇEKİRDEĞİ ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Lütfen Secrets ayarlarına GROQ_API_KEY ekleyin!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.markdown("### 🦅 BAZ BAGER")
    st.caption("Yaratıcı: Aykut Kutpınar")
    st.divider()
    
    # Çoklu Dil Desteği
    langs = {"Türkçe": "tr", "English": "en", "Deutsch": "de", "Français": "fr", "Español": "es"}
    sel_lang = st.selectbox("İletişim Dili:", list(langs.keys()))
    l_code = langs[sel_lang]
