import streamlit as st
from groq import Groq
import random
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text

# --- 1. SAYFA VE TASARIM AYARLARI (GÖZ ALICI ARAYÜZ) ---
st.set_page_config(page_title="BAZ BAGER: X", page_icon="🦅", layout="wide")

# Özel CSS ile arayüzü modernleştiriyoruz (Başlıkları ortala, butonları güzelleştir)
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    h1 {
        text-align: center;
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FF914D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em !important;
        font-weight: bold;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. YAN MENÜ (KİMLİK KARTI) ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/eagle.png", width=80)
    st.title("BAZ BAGER")
    st.markdown("---")
    st.markdown("👤 **Sahibi:** Aykut Kutpınar")
    st.markdown("🧠 **Zekâ:** Llama 3.3 (70B)")
    st.markdown("🎨 **Görsel:** Pollinations HQ")
    st.markdown("🎤 **Ses:** Neural TTS")
    st.success("🟢 Sistem Aktif")

# --- 3. BAŞLIK VE SES GİRİŞ ALANI ---
st.title("🦅 BAZ BAGER: PREMIUM")
st.markdown("<p style='text-align: center; color: gray;'>Sınırsız güç ve estetik bir arada.</p>", unsafe_allow_html=True)

# Ses girişini merkeze alıyoruz
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    # Bu buton sen sustuğunda otomatik durur
    voice_input = speech_to_text(
        language='tr',
        start_prompt="🎙️ KONUŞMAK İÇİN DOKUN",
        stop_prompt="⏳ DİNLİYORUM... (Sessizlikte Biter)",
        just_once=True,
        key='mic_input',
        use_container_width=True
    )

# --- 4. HAFINZA VE GEÇMİŞ ---
api_key = st.secrets.get("GROQ_
