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
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: #E3E3E3;}
    [data-testid="stChatMessage"] {
        background-color: transparent;
        padding: 20px 0px;
        max-width: 800px;
        margin: 0 auto;
    }
    .stChatInputContainer {padding-bottom: 30px; background-color: #0E1117;}
</style>
""", unsafe_allow_html=True)

# --- 2. SİSTEM ÇEKİRDEĞİ ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Secrets ayarlarına GROQ_API_KEY eklenmemiş!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. YAN MENÜ ---
with st.sidebar:
    st.markdown("### 🦅 BAZ BAGER")
    st.caption("Sahibi: Aykut Kutpınar")
    st.divider()
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- 4. SOHBET AKIŞI ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        content = str(m["content"])
        if "http" in content and "pollinations" in content:
            st.image(content, use_container_width=True)
        else:
            st.markdown(content)

# --- 5. AKILLI MİKROFON (SUSUNCA OTOMATİK CEVAP VERİR) ---
st.write("🎙️ **Sesli Komut:**")
# 'just_once=True' parametresi siz sustuğunuzda kaydı bitirip hemen işleme alır.
voice_input = speech_to_text(
    language='tr
