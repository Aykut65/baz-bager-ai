import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. AYARLAR VE "GEMINI" TARZI ARAYÜZ ---
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="centered")

# CSS: Gereksiz boşlukları siler, mesajları güzelleştirir
st.markdown("""
<style>
    /* Ana başlık ve menü gizleme */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Arka planı koyu ve modern yap */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Mesaj Baloncukları */
    .stChatMessage {
        background-color: #262730;
        border-radius: 20px;
        padding: 10px;
        margin-bottom: 5px;
    }
    
    /* Kullanıcı mesajını farklı renklendir (Opsiyonel, Streamlit otomatik halleder ama garanti olsun) */
    div[data-testid="stChatMessage"] {
        border: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. YAN MENÜ (KİMLİK KARTI) ---
with st.sidebar:
    st.title("🦅 BAZ BAGER")
    st.caption("Sahibi: Aykut Kutpınar")
    st.divider()
    # Mikrofonu yan menüye alarak ana ekranı temiz tutuyoruz (Tıpkı profesyonel appler gibi)
    st.write("🎙️ **Sesli Komut:**")
    voice = speech_to_text(language='tr', start_prompt="🔴 Dokun ve Konuş", stop_prompt="Dur", just_once=True, key='mic_sidebar')
    st.info("Sistem: Hazır")

# --- 3. API BAĞLANTISI ---
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Lütfen API anahtarını ekleyin.")
    st.stop()

# --- 4. HAFIZA ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # İlk karşılama mesajı
    st.session_state.messages.append({"role": "assistant", "content": "Merhaba Aykut Bey. Ben
