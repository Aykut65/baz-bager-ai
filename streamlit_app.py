import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. SAYFA VE MODERN TASARIM AYARLARI ---
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="centered")

# CSS: Gereksiz her şeyi gizler ve Gemini tarzı şık bir sohbet ekranı oluşturur
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stApp {background-color: #0E1117; color: white;} .stChatMessage {border-radius: 15px; border: 1px solid #333; margin-bottom: 10px;}</style>", unsafe_allow_html=True)

# --- 2. SİSTEM ÇEKİRDEĞİ (API) ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Secrets kısmında GROQ_API_KEY eksik!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. ANA EKRAN: KONUŞMA DÜĞMESİ (MİKROFON) ---
# Mikrofonu en üste, kimsenin kaçıramayacağı şekilde koyuyoruz
st.markdown("<h2 style='text-align: center;'>🦅 BAZ BAGER</h2>", unsafe_allow_html=True)
st.write("🎙️ **Sesli Komut Vermek İçin Dokun:**")

# Görsel 1768812304198'deki görünmeme hatasını çözmek için merkezi konumlandırma
voice_msg = speech_to_text(
    language='tr',
    start_prompt="🔴 KONUŞMAYI BAŞLAT",
    stop_prompt="⏳ DİNLİYORUM... (Susunca Biter)",
    just_once=True,
    key='bager_mic_ultimate'
)

st.divider()

# --- 4. SOHBET AKIŞI (GÖRÜNÜR ALAN) ---
# Boş ekran hat
