import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. SAYFA VE MODERN TASARIM AYARLARI ---
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="wide")

# CSS: Arayüzü Gemini gibi temiz ve şık yapar (Hata riskini önlemek için en sade hali)
st.markdown("""
<style>
    .stApp {background-color: #0E1117; color: white;}
    .stChatMessage {border-radius: 15px; margin-bottom: 10px; border: 1px solid #333;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 2. YAN MENÜ: KİMLİK VE SES KONTROLÜ ---
with st.sidebar:
    st.markdown("# 🦅 BAZ BAGER")
    st.markdown("---")
    st.info("👤 **Sahibi:** Aykut Kutpınar")
    st.write("🎤 **Sesli Komut Ver:**")
    # Mikrofon: Dokun, konuş ve sus. Otomatik olarak algılar.
    voice_msg = speech_to_text(
        language='tr',
        start_prompt="🔴 DOKUN VE KONUŞ",
        stop_prompt="⏳ DİNLİYORUM...",
        just_once=True,
        key='bager_mic'
    )
    st.markdown("---")
    if st.button("Sohbeti Sıfırla"):
        st.session_state.messages = []
        st.rerun()

# --- 3. SİSTEM ÇEKİRDEĞİ ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Lütfen Secrets kısmına GROQ_API_KEY ekleyin.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SOHBET AKIŞI (GÖRÜNÜR ALAN) ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        msg_content = str(m["content"])
        if "http" in msg_content and "pollinations" in msg_content:
            st.image(msg_content, use_container_width=True)
        else:
            st.markdown(msg_content)

# --- 5. GİRİŞ MERKEZİ (SES VEYA METİN) ---
user_input = None
if voice_msg:
    user_input = voice_msg
elif text_input := st.chat_input("Emret Aykut Bey..."):
    user_input = text_input

# --- 6. İŞLEM VE CEVAP MANTIĞI ---
if user_input:
    # Kullanıcı mesajını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Asistanın cevabını üret
    with st.chat_message("assistant"):
        cmd = user_input.lower()
        final_response = ""

        # A) KİMLİK SORGUSU (Aykut Kutpınar Önceliği)
        if any(x in cmd for x in ["kim tasarladı", "sahibin", "seni kim"]):
            final_
