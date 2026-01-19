import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. ARAYÜZ VE MODERN TASARIM ---
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="centered")

# Gemini tarzı temiz arayüz için CSS
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: white;}
    .stChatMessage {border-radius: 15px; border: 1px solid #333; margin-bottom: 10px;}
    .stChatInputContainer {padding-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

# --- 2. SİSTEM ÇEKİRDEĞİ ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Secrets kısmında GROQ_API_KEY eksik!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. ANA EKRAN: KONUŞMA DÜĞMESİ (MİKROFON) ---
# Mikrofonu en üste, çok belirgin bir şekilde koyuyoruz
st.markdown("<h3 style='text-align: center;'>🎙️ Sesli Komut</h3>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    voice_msg = speech_to_text(
        language='tr',
        start_prompt="🔴 KONUŞMAK İÇİN DOKUN",
        stop_prompt="⏳ DİNLİYORUM... (Susunca Biter)",
        just_once=True,
        key='bager_mic_fixed'
    )

st.divider()

# --- 4. SOHBET AKIŞI ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        msg_val = str(m["content"])
        if "http" in msg_val and "pollinations" in msg_val:
            st.image(msg_val, use_container_width=True)
        else:
            st.markdown(msg_val)

# --- 5. GİRİŞ KONTROLÜ (SES VEYA METİN) ---
user_query = None
if
