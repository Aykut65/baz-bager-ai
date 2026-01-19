import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. GEMINI KLON ARAYÜZÜ (CSS) ---
st.set_page_config(page_title="Gemini - BAZ BAGER", page_icon="🦅", layout="centered")

st.markdown("""
<style>
    /* Gemini minimalist ve karanlık tema */
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: #E3E3E3; font-family: 'Inter', sans-serif;}
    
    /* Öneri Butonları (Suggestion Chips) */
    .stButton>button {
        background-color: #1E1F20; color: #E3E3E3; border-radius: 20px;
        border: 1px solid #444746; padding: 10px 20px; text-align: left; width: 100%;
    }
    .stButton>button:hover {background-color: #333537; border-color: #8E918F;}
    
    /* Mesaj Balonları */
    [data-testid="stChatMessage"] {background-color: transparent; border: none; padding: 15px 0;}
    
    /* Giriş Çubuğu */
    .stChatInputContainer {padding-bottom: 30px; background-color: #0E1117;}
</style>
""", unsafe_allow_html=True)

# --- 2. SİSTEM ÇEKİRDEĞİ ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Secrets ayarlarında GROQ_API_KEY bulunamadı!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. ANA GİRİŞ EKRANI (Görsel 1000149640 Benzeri) ---
if not st.session_state.messages:
    st.markdown("<h1 style='font-size: 3rem;'>Merhaba Aykut</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #8E918F;'>Nereden başlayalım?</h2>", unsafe_allow_html=True)
    
    # Öneri Butonları (Görsel 1000149640'taki butonlar)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎨 Resim Oluştur"): st.session_state.messages.append({"role": "user", "content": "Bana güzel bir resim tasarla."}); st.rerun()
        if st.button("🎥 Video fikirleri üret"): st.session_state.messages.append({"role": "user", "content": "YouTube için video fikirleri ver."}); st.rerun()
    with col2:
        if st.button("📚 Öğrenmeme yardım et"): st.session_state.messages.append({"role": "user", "content": "Bana yeni bir şeyler öğret."}); st.rerun()
        if st.button("✨ Günüme enerji kat"): st.session_state.messages.append({"role": "user", "content": "Bana ilham verici bir şeyler söyle."}); st.rerun()

# --- 4. SOHBET AKIŞI ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        c = str(m["content"])
        if "http" in c and "pollinations" in c:
            st.image(c, use_container_width=True)
        else:
            st.markdown(c)

# --- 5. AKILLI GİRİŞ (AUTO-STOP MİKROFON) ---
st.write("🎙️ **Sesli Komut:**")
voice_in = speech_to_text(
    language='tr', start_prompt="Dokun ve Konuş", stop_prompt="Dinliyorum...",
    just_once=True, key='bager_gemini_engine'
)

query = None
if voice_in:
    query = voice_in
elif txt := st.chat_input("Gemini'a sorun"):
    query = txt

# --- 6. ZEKA VE CEVAP MANTIĞI ---
if query:
    if not any(m["content"] == query for m in st.session_state.messages):
        st.session_state.messages.append({"role": "user", "content": query})
        st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    user_msg = st.session_state.messages[-1]["content"]
    with st.chat_message("assistant"):
        q_low = user_msg.lower()
        res = ""

        # Kimlik
        if any(x in q_low for x in ["kim tasarladı", "sahibin", "seni kim"]):
            res = "Beni tasarlayan ve tek sahibim Aykut Kutpınar'dır."
            st.markdown(res)
        # Resim
        elif any(x in q_low for x in ["resim", "çiz", "tasarla"]):
            try:
                url = f"https://image.pollinations.ai/prompt/{user_msg.replace(' ', '%20')}?width=1024&height=1024&seed={random.randint(1, 10**6)}"
                st.image(url, caption="Bager Tasarımı")
                res = url
            except: st.error("Motor meşgul.")
        # Üstün Zeka (Gemini Modellemesi)
        else:
            try:
                sys_msg = "Sen BAZ BAGER'sin. Sahibi Aykut Kutpınar. Gemini'ın tüm bilgi birikimine ve zekasına sahipsin. Onun gibi derinlikli, samimi ve zeki ol. SADECE düzgün Türkçe konuş. Cevapların akıcı ve profesyonel olsun."
                hist = [{"role": "system", "content": sys_msg}] + [m for m in st.session_state.messages if "http" not in str(m["content"])]
                chat = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=hist)
                res = chat.choices[0].message.content
                st.markdown(res)
            except Exception as e: st.error(f"Hata: {e}")

        if res:
            st.session_state.messages.append({"role": "assistant", "content": res})
            if "http" not in res:
                try:
                    tts = gTTS(text=res, lang='tr', slow=False)
                    b = BytesIO(); tts.write_to_fp(b)
                    st.audio(b, format='audio/mp3', autoplay=True)
                except: pass
