import streamlit as st
from groq import Groq
import random
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text

# 1. TEMEL AYARLAR
st.set_page_config(page_title="BAZ BAGER", layout="wide")

# Hata riskini sıfıra indirmek için CSS'i tek satır yapıyoruz
st.markdown("<style>.stApp {background-color: #0e1117; color: white;} h1 {text-align: center; color: #FF4B4B;}</style>", unsafe_allow_html=True)

# 2. YAN MENÜ
with st.sidebar:
    st.title("🦅 BAZ BAGER")
    st.write("Sahibi: Aykut Kutpınar")
    st.success("Sistem Aktif")

# 3. API BAĞLANTISI (Hata korumalı blok)
try:
    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        st.warning("API Key Eksik")
        st.stop()
    client = Groq(api_key=api_key)
except:
    st.error("Bağlantı Hatası")
    st.stop()

# 4. HAFIZA
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. EKRAN DÜZENİ
st.title("🦅 BAZ BAGER: ULTRA")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    voice = speech_to_text(language='tr', start_prompt="🔴 KONUŞ", stop_prompt="⏳ DUR", just_once=True, key='mic')

# 6. GEÇMİŞ
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        content = str(m["content"])
        if content.startswith("http"):
            st.image(content)
        else:
            st.write(content)

# 7. GİRİŞ KONTROLÜ
prompt = None
if voice:
    prompt = voice
elif txt := st.chat_input("Mesaj yaz..."):
    prompt = txt

# 8. CEVAP ÜRETİMİ
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # Basit Kontrol
        p = prompt.lower()
        is_id = "kim" in p and ("tasarla" in p or "sahib" in p or "yarat" in p)
        is_img = ("resim" in p or "çiz" in p) and not is_id
        
        reply = ""
        
        if is_img:
            try:
                seed = random.randint(1, 9999)
                safe_p = prompt.replace(" ", "%20")
                url = f"https://image.pollinations.ai/prompt/{safe_p}?width=1024&height=1024&seed={seed}&nologo=true"
                st.image(url)
                reply = "Resmi çizdim Aykut Bey."
                st.session_state.messages.append({"role": "assistant", "content": url})
            except:
                reply = "Resim servisi hatası."
        
        else:
            try:
                # Sistem mesajı tek satırda
                sys = "Sen BAZ BAGER'sin. Sahibin AYKUT KUTPINAR. Türkçe ve kısa cevap ver."
                msgs = [{"role": "system", "content": sys}]
                for m in st.session_state.messages:
                    if not str(m["content"]).startswith
