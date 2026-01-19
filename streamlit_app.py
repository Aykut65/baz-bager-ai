import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. AYARLAR ---
st.set_page_config(page_title="BAZ BAGER", layout="wide")

# CSS (Hata riskini sıfırlamak için tek satır yazdım)
st.markdown("<style>.stApp {background-color: #121212; color: white;} .stChatMessage {background-color: #262730;}</style>", unsafe_allow_html=True)

# --- 2. YAN MENÜ ---
with st.sidebar:
    st.title("🦅 BAZ BAGER")
    st.info("Sahibi: Aykut Kutpınar")
    st.success("Sistem: Aktif")

# --- 3. API BAĞLANTISI ---
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("API Key bulunamadı.")
    st.stop()

# --- 4. HAFIZA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 5. BAŞLIK VE MİKROFON ---
st.title("🦅 BAZ BAGER: FİNAL")

# Mikrofon Butonu
c1, c2 = st.columns([1, 4])
with c1:
    voice = speech_to_text(language='tr', start_prompt="🎙️ KONUŞ", stop_prompt="DUR", just_once=True, key='mic')

# --- 6. GEÇMİŞİ GÖSTERME ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        # Mesaj bir resim linki mi? Kontrolü
        content = str(msg["content"])
        if "http" in content and "pollinations" in content:
            st.image(content)
        else:
            st.write(content)
