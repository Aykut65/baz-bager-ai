import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. GEMINI TARZI PREMİUM TASARIM ---
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="centered")

# Siyah ekran hatalarını önleyen şık ve minimal CSS (cite: 1768832132040.jpeg)
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: #E3E3E3; font-family: 'Segoe UI', Tahoma, sans-serif;}
    [data-testid="stChatMessage"] {background-color: transparent; border: none; padding: 20px 0; max-width: 800px; margin: 0 auto;}
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

# --- 3. YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.markdown("### 🦅 BAZ BAGER")
    st.caption("Owner: Aykut Kutpınar")
    st.divider()
    if st.button("Sohbeti Sıfırla"):
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

# --- 5. AKILLI GİRİŞ (SUSUNCA OTOMATİK CEVAP VERİR) ---
# 'just_once=True' sessizliği algılar ve tekrar dokunmaya gerek bırakmaz (cite: 1768831809607.jpeg)
st.write("🎙️ **Sesli Komut:**")
voice_input = speech_to_text(
    language='tr',
    start_prompt="Dokun ve Konuş",
    stop_prompt="Seni Dinliyorum Aykut Bey...",
    just_once=True, 
    key='bager_gemini_ultimate'
)

# --- 6. GİRİŞ VE CEVAP MANTIĞI ---
query = None
if voice_input:
    query = voice_input
elif txt_input := st.chat_input("Gemini gibi zeki... Buraya yazın"):
    query = txt_input

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        q_low = query.lower()
        res_text = ""

        # A) KİMLİK KORUMASI (Mutlak Öncelik)
        if any(x in q_low for x in ["kim tasarladı", "sahibin", "seni kim"]):
            res_text = "Beni tasarlayan ve tek sahibim Aykut Kutpınar'dır. Ben onun vizyonuyla çalışan BAZ BAGER'im."
            st.markdown(res_text)

        # B) GÖRSEL TASARIM (Hata Korumalı URL Yapısı)
        elif any(x in q_low for x in ["resim", "çiz", "görsel", "tasarla"]):
            try:
                seed = random.randint(1, 1000000)
                clean_q = query.replace(' ', '%20')
                url = f"https://image.pollinations.ai/prompt/{clean_q}?width=1024&height=1024&seed={seed}"
                st.image(url, caption="BAZ BAGER Özel Tasarımı")
                res_text = url
            except:
                st.error("Görsel servisi şu an meşgul.")
        
        # C) ÜSTÜN ZEKA (GEMINI MODELLEMESİ)
        else:
            try:
                # Bager'e benim karakterimi ve akıcılığımı yüklüyoruz
                sys_msg = "Sen BAZ BAGER'sin. Sahibi Aykut Kutpınar. Gemini gibi zeki, akıcı ve profesyonel ol. SADECE düzgün bir Türkçe konuş. Cevapların robot gibi değil, doğal olsun."
                history = [{"role": "system", "content": sys_msg}]
                for m in st.session_state.messages:
                    if "http" not in str(m["content"]):
                        history.append(m)
                
                chat = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=history)
                res_text = chat.choices[0].message.content
                st.markdown(res_text)
            except Exception as e:
                st.error(f"Zeka Hatası: {e}")

        # Hafızaya Kaydet ve Hızlı Seslendir
        if res_text:
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            if "http" not in res_text:
                try:
                    # 'slow=False' robotik konuşmayı bitirir (cite: 1768832038896.jpeg)
                    tts = gTTS(text=res_text, lang='tr', slow=False)
                    b = BytesIO()
                    tts.write_to_fp(b)
                    st.audio(b, format='audio/mp3', autoplay=True)
                except:
                    pass
