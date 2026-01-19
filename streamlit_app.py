import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. ARAYÜZ AYARLARI (GEMINI STYLE) ---
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="centered")

# CSS: Ekranı temizler ve sohbet odaklı yapar
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: #FFFFFF;}
    .stChatMessage {border-radius: 15px; margin-bottom: 10px;}
</style>
""", unsafe_allow_html=True)

# --- 2. YAN MENÜ (STRATEJİK MERKEZ) ---
with st.sidebar:
    st.markdown("### 🦅 BAZ BAGER")
    st.caption("Sahibi: Aykut Kutpınar")
    st.divider()
    st.write("🎙️ **Sesli Komut:**")
    # Akıllı mikrofon: Sen susunca otomatik durur
    voice = speech_to_text(language='tr', start_prompt="Konuşmak için dokun", stop_prompt="Dinliyorum...", just_once=True, key='mic')
    st.divider()
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- 3. SİSTEM ÇEKİRDEĞİ ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Lütfen Secrets kısmına GROQ_API_KEY ekleyin.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SOHBET AKIŞI ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if "http" in str(msg["content"]) and "pollinations" in str(msg["content"]):
            st.image(msg["content"])
        else:
            st.markdown(msg["content"])

# --- 5. GİRİŞ YÖNETİMİ ---
prompt = None
if voice:
    prompt = voice
elif txt := st.chat_input("Bir şeyler yaz..."):
    prompt = txt

# --- 6. İŞLEM MERKEZİ ---
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        p_low = prompt.lower()
        res_text = ""

        # A) KİMLİK (Aykut Kutpınar)
        if any(x in p_low for x in ["kim tasarladı", "sahibin", "
