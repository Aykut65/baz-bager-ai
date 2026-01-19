import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. GEMINI TARZI ULTRA PREMİUM TASARIM ---
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="centered")

st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: #E3E3E3; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
    
    /* Sohbet Akışı */
    [data-testid="stChatMessage"] {
        background-color: transparent;
        padding: 15px 0px;
        max-width: 850px;
        margin: 0 auto;
    }
    
    /* Yazma Alanı Sabitleme */
    .stChatInputContainer {padding-bottom: 20px; background-color: #0E1117;}
    
    /* Ses Oynatıcıyı Gizle (Arka planda çalsın diye) */
    audio {display: none;}
</style>
""", unsafe_allow_html=True)

# --- 2. SİSTEM VE HAFIZA ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Lütfen Secrets kısmına API anahtarını ekleyin.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. YAN MENÜ (KONTROL) ---
with st.sidebar:
    st.markdown("### 🦅 BAZ BAGER")
    st.caption("Owner: Aykut Kutpınar")
    st.divider()
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- 4. SOHBET AKIŞI ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        c = str(m["content"])
        if "http" in c and "pollinations" in c:
            st.image(c, use_container_width=True)
        else:
            st.markdown(c)

# --- 5. AKILLI GİRİŞ (AUTO-STOP MİKROFON) ---
# Mikrofonu yazışma alanının hemen üzerine, şık bir şekilde koyuyoruz
st.write("🎙️ **Sesli Komut:**")
voice = speech_to_text(
    language='tr',
    start_prompt="Dokun ve Konuş",
    stop_prompt="Seni dinliyorum...",
    just_once=True, # Sen sustuğunda otomatik gönderir
    key='bager_smart_mic'
)

query = None
if voice:
    query = voice
elif txt := st.chat_input("Emret Aykut Bey..."):
    query = txt

# --- 6. ZEKA VE AKICI CEVAP ---
if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        q_low = query.lower()
        res = ""

        # A) KİMLİK DOĞRULAMA
        if any(x in q_low for x in ["kim tasarladı", "sahibin", "seni kim"]):
            res = "Beni tasarlayan ve tek sahibim Aykut Kutpınar'dır."
            st.markdown(res)

        # B) GÖRSEL TASARIM
        elif any(x in q_low for x in ["resim", "çiz", "görsel", "tasarla"]):
            try:
                seed = random.randint(1, 1000000)
                url = f"https://image.pollinations.ai/prompt/{query.replace(' ', '%20')}?width=1024&height=1024&seed={seed}&nologo=true"
                st.image(url, caption="Bager Özel Tasarım")
                res = url
            except:
                st.error("Görsel servisi yoğun.")
        
        # C) SÜPER ZEKA (AKICI KONUŞMA TALİMATI)
        else:
            try:
                hist = [{"role": "system", "content": "Sen BAZ BAGER'sin. Sahibin Aykut Kutpınar. Benim (Gemini) gibi akıcı, zeki ve profesyonel cevap ver. Kesinlikle robot gibi tane tane konuşma."}]
                for m in st.session_state.messages:
                    if "http" not in str(m["content"]):
                        hist.append(m)
                
                chat = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=hist)
                res = chat.choices[0].message.content
                st.
