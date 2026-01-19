import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. ARAYÜZ TASARIMI (MODERN & ŞIK) ---
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="centered")

# CSS: Gereksiz her şeyi gizler ve Gemini tarzı bir odaklanma sağlar
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: #FFFFFF;}
    [data-testid="stChatMessage"] {border-radius: 15px; border: 1px solid #333; margin-bottom: 8px;}
</style>
""", unsafe_allow_html=True)

# --- 2. YAN MENÜ (KONTROL MERKEZİ) ---
with st.sidebar:
    st.markdown("# 🦅 BAZ BAGER")
    st.caption("Sahibi: Aykut Kutpınar")
    st.divider()
    st.write("🎙️ **Sesli Komut:**")
    # Mikrofon: Konuşma bittiğinde otomatik algılar
    voice_input = speech_to_text(
        language='tr', 
        start_prompt="Dokun ve Konuş", 
        stop_prompt="Dinliyorum...", 
        just_once=True, 
        key='bager_mic_fixed'
    )
    st.divider()
    if st.button("Sohbeti Sıfırla"):
        st.session_state.messages = []
        st.rerun()

# --- 3. SİSTEM ÇEKİRDEĞİ ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Secrets kısmına GROQ_API_KEY ekleyin.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SOHBET AKIŞI ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        m_cont = str(m["content"])
        if "http" in m_cont and "pollinations" in m_cont:
            st.image(m_cont, use_container_width=True)
        else:
            st.markdown(m_cont)

# --- 5. GİRİŞ YÖNETİMİ ---
query = None
if voice_input:
    query = voice_input
elif txt_input := st.chat_input("Emret Aykut Bey..."):
    query = txt_input

# --- 6. İŞLEM MERKEZİ ---
if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        q_low = query.lower()
        res_text = ""

        # A) KİMLİK: Aykut Kutpınar (Resim motorundan önce çalışır, Görsel 1768810020603 hatasını önler)
        id_keys = ["kim tasarladı", "sahibin", "seni kim", "yaratıcın", "ismin ne"]
        if any(x in q_low for x in id_keys):
            res_text = "Beni tasarlayan ve tek sahibim Aykut Kutpınar'dır."
            st.markdown(res_text)

        # B) RESİM: Pollinations HQ (Görsel 1768809545608 hatasını önler)
        elif any(x in q_low for x in ["resim", "çiz", "görsel", "tasarla"]):
            try:
                seed = random.randint(1, 1000000)
                url = f"https://image.pollinations.ai/prompt/{query.replace(' ', '%20')}?width=1024&height=1024&seed={seed}&nologo=true"
                st.image(url, caption="Bager Tasarımı")
                res_text = url 
            except:
                st.error("Görsel motoru şu an meşgul.")
        
        # C) ZEKA: Llama 3.3 70B
        else:
            try:
                hist = [{"role": "system", "content": "Sen BAZ BAGER'sin. Sahibin Aykut Kutpınar. Çok zeki ve kısa cevap ver."}]
                for m in st.session_state.messages:
                    if "http" not in str(m["content"]):
                        hist.append(m)
                
                comp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=hist)
                res_text = comp.choices[0].message.content
                st.markdown(res_text)
            except Exception as e:
                st.error(f"Sistem Hatası: {e}")

        # Hafızaya ekle ve sesli yanıt (Görsel 1768816646779 tarzı)
        if res_text:
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            if "http" not in res_text:
                try:
                    tts = gTTS(text=res_text, lang='tr')
                    b = BytesIO()
                    tts.write_to_fp(b)
                    st.audio(b, format='audio/mp3', start_time=0)
                except:
                    pass
