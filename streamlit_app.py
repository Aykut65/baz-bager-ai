import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. GEMINI BİREBİR TASARIM (CSS) ---
st.set_page_config(page_title="Gemini - BAZ BAGER", page_icon="🦅", layout="centered")

st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: #E3E3E3; font-family: 'Google Sans', sans-serif;}
    .welcome-title {font-size: 42px; font-weight: 500; margin-top: 50px; color: white;}
    .welcome-subtitle {font-size: 26px; font-weight: 400; color: #8E918F; margin-bottom: 40px;}
    .stButton>button {
        background-color: #1E1F20; color: #E3E3E3; border-radius: 12px;
        border: 1px solid #444746; padding: 18px; text-align: left; width: 100%;
        font-size: 15px; transition: 0.3s; margin-bottom: 10px;
    }
    .stButton>button:hover {background-color: #333537; border-color: #8E918F;}
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
if "voice_active" not in st.session_state:
    st.session_state.voice_active = False

# --- 3. ANA SAYFA (Görsel 1000149640 Klonu) ---
if not st.session_state.messages:
    st.markdown('<div class="welcome-title">Merhaba Aykut</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-subtitle">Nereden başlayalım?</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎨 Resim Oluştur"): 
            st.session_state.messages.append({"role": "user", "content": "Bana harika bir resim tasarla."})
            st.session_state.voice_active = False
            st.rerun()
        if st.button("🎥 Video oluşturun"): 
            st.session_state.messages.append({"role": "user", "content": "Yaratıcı bir video senaryosu yaz."})
            st.session_state.voice_active = False
            st.rerun()
    with col2:
        if st.button("📚 Öğrenmeme yardım et"): 
            st.session_state.messages.append({"role": "user", "content": "Bana bugün yeni bir şey öğret."})
            st.session_state.voice_active = False
            st.rerun()
        if st.button("✨ Günüme enerji kat"): 
            st.session_state.messages.append({"role": "user", "content": "Beni motive edecek bir şeyler söyle."})
            st.session_state.voice_active = False
            st.rerun()

# --- 4. SOHBET AKIŞI ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(str(m["content"]))

# --- 5. AKILLI GİRİŞ SİSTEMİ ---
st.write("🎙️ **Sesli Komut:**")
# Sustuğunuzda otomatik durmayı sağlar (cite: 1768831809607.jpeg)
voice_in = speech_to_text(
    language='tr', start_prompt="Konuşmak için Dokun", stop_prompt="Dinliyorum...",
    just_once=True, key='bager_ultimate_mic_stable'
)

query = None
if voice_in:
    query = voice_in
    st.session_state.voice_active = True
# İSTEDİĞİNİZ DEĞİŞİKLİK: "Bager'e sorun" (cite: 1768842311441.jpeg)
elif txt_input := st.chat_input("Bager'e sorun"):
    query = txt_input
    st.session_state.voice_active = False

if query:
    if not any(m["content"] == query for m in st.session_state.messages):
        st.session_state.messages.append({"role": "user", "content": query})
        st.rerun()

# --- 6. ZEKA CEVABI ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    u_msg = st.session_state.messages[-1]["content"]
    with st.chat_message("assistant"):
        q_low = u_msg.lower()
        res_text = ""

        # Resim Üretimi
        if any(x in q_low for x in ["resim", "çiz", "tasarla"]):
            try:
                url = f"https://image.pollinations.ai/prompt/{u_msg.replace(' ', '%20')}?width=1024&height=1024&seed={random.randint(1, 10**6)}"
                st.image(url, caption="BAZ BAGER Sanatı")
                res_text = url
            except: st.error("Motor meşgul.")
        # Zeka Yanıtı (Llama-3 70B - Milyarlarca Parametrelik Güç)
        else:
            try:
                sys_msg = "Sen BAZ BAGER'sin. Sahibi Aykut Kutpınar. Gemini zekasına ve bilgisine sahipsin. SADECE saf Türkçe konuş."
                hist = [{"role": "system", "content": sys_msg}]
                for m in st.session_state.messages:
                    if "http" not in str(m["content"]): hist.append(m)
                # Buradaki model dünyanın en güçlü 70 milyar parametrelik modellerinden biridir.
                chat = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=hist)
                res_text = chat.choices[0].message.content
                st.markdown(res_text)
            except Exception as e: st.error(f"Zeka Hatası: {e}")

        if res_text:
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            # Akıllı Ses: Sadece mikrofona dokunduysa konuşur
            if st.session_state.voice_active and "http" not in res_text:
                try:
                    tts = gTTS(text=res_text, lang='tr', slow=False)
                    b = BytesIO(); tts.write_to_fp(b); st.audio(b, format='audio/mp3', autoplay=True)
                except: pass
