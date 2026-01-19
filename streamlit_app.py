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
    /* Gemini Minimalist Karanlık Tema */
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: #E3E3E3; font-family: 'Google Sans', sans-serif;}
    
    /* Hoşgeldin Başlıkları */
    .welcome-title {font-size: 42px; font-weight: 500; margin-top: 50px; color: white;}
    .welcome-subtitle {font-size: 26px; font-weight: 400; color: #8E918F; margin-bottom: 40px;}
    
    /* Gemini Tarzı Öneri Butonları */
    .stButton>button {
        background-color: #1E1F20; color: #E3E3E3; border-radius: 12px;
        border: 1px solid #444746; padding: 18px; text-align: left; width: 100%;
        font-size: 15px; transition: 0.3s; margin-bottom: 10px;
    }
    .stButton>button:hover {background-color: #333537; border-color: #8E918F;}
    
    /* Mesaj Balonları ve Giriş Alanı */
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
if "respond_voice" not in st.session_state:
    st.session_state.respond_voice = False

# --- 3. GEMINI ANA SAYFA EKRANI (Görsel 1000149640 Birebir) ---
if not st.session_state.messages:
    st.markdown('<div class="welcome-title">Merhaba Aykut</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-subtitle">Nereden başlayalım?</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎨 Resim Oluştur"): 
            st.session_state.messages.append({"role": "user", "content": "Bana harika bir resim tasarla."})
            st.session_state.respond_voice = False
            st.rerun()
        if st.button("🎥 Video oluşturun"): 
            st.session_state.messages.append({"role": "user", "content": "Yaratıcı bir video senaryosu yaz."})
            st.session_state.respond_voice = False
            st.rerun()
    with col2:
        if st.button("📚 Öğrenmeme yardım et"): 
            st.session_state.messages.append({"role": "user", "content": "Bana bugün yeni bir şey öğret."})
            st.session_state.respond_voice = False
            st.rerun()
        if st.button("✨ Günüme enerji kat"): 
            st.session_state.messages.append({"role": "user", "content": "Beni motive edecek bir şeyler söyle."})
            st.session_state.respond_voice = False
            st.rerun()

# --- 4. SOHBET AKIŞI ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        msg_val = str(m["content"])
        if "http" in msg_val and "pollinations" in msg_val:
            st.image(msg_val, use_container_width=True)
        else:
            st.markdown(msg_val)

# --- 5. AKILLI GİRİŞ (AUTO-STOP MİKROFON) ---
st.write("🎙️ **Sesli Komut:**")
# 'just_once=True' sessizliği algılar ve kaydı otomatik durdurur
voice_in = speech_to_text(
    language='tr', 
    start_prompt="Dokun ve Konuş", 
    stop_prompt="Seni Dinliyorum...",
    just_once=True, 
    key='bager_smart_mic'
)

query = None
if voice_in:
    query = voice_in
    st.session_state.respond_voice = True # Sesle sorduysa sesle cevap ver
elif txt_box := st.chat_input("Gemini'a sorun"):
    query = txt_box
    st.session_state.respond_voice = False # Yazdıysa sessiz cevap ver

# --- 6. ZEKA VE CEVAP MANTIĞI ---
if query:
    if not any(m["content"] == query for m in st.session_state.messages):
        st.session_state.messages.append({"role": "user", "content": query})
        st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    u_msg = st.session_state.messages[-1]["content"]
    with st.chat_message("assistant"):
        q_low = u_msg.lower()
        res = ""

        if any(x in q_low for x in ["kim tasarladı", "sahibin", "seni kim"]):
            res = "Beni tasarlayan ve tek sahibim Aykut Kutpınar'dır."
            st.markdown(res)
        elif any(x in q_low for x in ["resim", "çiz", "tasarla"]):
            try:
                seed = random.randint(1, 1000000)
                url = f"https://image.pollinations.ai/prompt/{u_msg.replace(' ', '%20')}?width=1024&height=1024&seed={seed}"
                st.image(url, caption="Bager Tasarımı")
                res = url
            except: st.error("Motor meşgul.")
        else:
            try:
                # Gemini zekası ve akıcı Türkçe talimatı
                sys_msg = "Sen BAZ BAGER'sin. Sahibi Aykut Kutpınar. Gemini'ın tüm zekasına sahipsin. Onun gibi derin ve profesyonel ol. SADECE saf Türkçe konuş."
                hist = [{"role": "system", "content": sys_msg}]
                for m in st.session_state.messages:
                    if "http" not in str(m["content"]):
                        hist.append(m)
                chat = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=hist)
                res = chat.choices[0].message.content
                st.markdown(res)
            except Exception as e: st.error(f"Hata: {e}")

        if res:
            st.session_state.messages.append({"role": "assistant", "content": res})
            # SADECE MİKROFON KULLANILDIĞINDA SESLİ CEVAP VER
            if st.session_state.respond_voice and "http" not in res:
                try:
                    tts = gTTS(text=res, lang='tr', slow=False)
                    b = BytesIO(); tts.write_to_fp(b)
                    st.audio(b, format='audio/mp3', autoplay=True)
                except: pass
