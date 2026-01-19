import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. GEMINI BİREBİR TASARIM AYARLARI ---
st.set_page_config(page_title="Gemini - BAZ BAGER", page_icon="🦅", layout="centered")

# Gemini minimalist arayüzü ve buton tasarımları
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: #E3E3E3; font-family: 'Google Sans', sans-serif;}
    
    /* Hoşgeldin Başlıkları */
    .welcome-title {font-size: 44px; font-weight: 500; margin-bottom: 5px; color: white;}
    .welcome-subtitle {font-size: 28px; font-weight: 400; color: #8E918F; margin-bottom: 35px;}
    
    /* Gemini Tarzı Öneri Butonları */
    .stButton>button {
        background-color: #1E1F20; color: #E3E3E3; border-radius: 12px;
        border: 1px solid #444746; padding: 18px; text-align: left; width: 100%;
        font-size: 15px; transition: 0.3s;
    }
    .stButton>button:hover {background-color: #333537; border-color: #8E918F;}
    
    /* Giriş Çubuğu ve Mesajlar */
    [data-testid="stChatMessage"] {background-color: transparent; border: none; padding: 15px 0;}
    .stChatInputContainer {padding-bottom: 30px; background-color: #0E1117;}
</style>
""", unsafe_allow_html=True)

# --- 2. SİSTEM ÇEKİRDEĞİ ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Secrets ayarlarında GROQ_API_KEY eksik!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. GEMINI ANA SAYFA EKRANI (Görsel 1000149640 Birebir) ---
if not st.session_state.messages:
    st.markdown('<div class="welcome-title">Merhaba Aykut</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-subtitle">Nereden başlayalım?</div>', unsafe_allow_html=True)
    
    # Öneri Butonları
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎨 Resim Oluştur"): 
            st.session_state.messages.append({"role": "user", "content": "Bana harika bir resim tasarla."})
            st.rerun()
        if st.button("🎥 Video oluşturun"): 
            st.session_state.messages.append({"role": "user", "content": "Yaratıcı bir video senaryosu yaz."})
            st.rerun()
    with col2:
        if st.button("📚 Öğrenmeme yardım et"): 
            st.session_state.messages.append({"role": "user", "content": "Bana bugün yeni ve ilginç bir bilgi öğret."})
            st.rerun()
        if st.button("✨ Günüme enerji kat"): 
            st.session_state.messages.append({"role": "user", "content": "Bana ilham verecek, enerjik bir şeyler söyle."})
            st.rerun()

# --- 4. SOHBET AKIŞI ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        m_cont = str(m["content"])
        if "http" in m_cont and "pollinations" in m_cont:
            st.image(m_cont, use_container_width=True)
        else:
            st.markdown(m_cont)

# --- 5. AKILLI GİRİŞ (AUTO-STOP MİKROFON) ---
st.write("🎙️ **Sesli Komut:**")
voice_in = speech_to_text(
    language='tr', start_prompt="Konuşmak için Dokun", stop_prompt="Dinliyorum...",
    just_once=True, key='bager_gemini_engine_final'
)

query = None
if voice_in:
    query = voice_in
elif txt_input := st.chat_input("Gemini'a sorun"):
    query = txt_input

# --- 6. ZEKA VE CEVAP MANTIĞI ---
if query:
    if not any(m["content"] == query for m in st.session_state.messages):
        st.session_state.messages.append({"role": "user", "content": query})
        st.rerun()

if st.session_state.messages and st.session_state.messages[-
