import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. PREMİUM GEMINI ARAYÜZ TASARIMI ---
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="centered")

# Siyah ekran hatasını önlemek için optimize edilmiş CSS (cite: 1768812065656.jpeg)
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: #E3E3E3; font-family: 'Inter', sans-serif;}
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
    st.caption("Sahibi: Aykut Kutpınar")
    st.divider()
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- 4. SOHBET AKIŞI (BAŞLIKSIZ VE TEMİZ) ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        msg_val = str(m["content"])
        if "http" in msg_val and "pollinations" in msg_val:
            st.image(msg_val, use_container_width=True)
        else:
            st.markdown(msg_val)

# --- 5. AKILLI MİKROFON (SUSUNCA OTOMATİK CEVAP VERİR) ---
# 'just_once=True' sessizliği algılar ve tekrar dokunmaya gerek bırakmaz (cite: 1768831809607.jpeg)
st.write("🎙️ **Sesli Komut:**")
voice_input = speech_to_text(
    language='tr',
    start_prompt="Konuşmak için Dokun",
    stop_prompt="Seni Dinliyorum Aykut Bey...",
    just_once=True, 
    key='bager_gemini_core'
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

        # A) KİMLİK KORUMASI (Aykut Kutpınar Önceliği)
        if any(x in q_low for x in ["kim tasarladı", "sahibin", "seni kim"]):
            res_text = "Beni tasarlayan ve tek sahibim Aykut Kutpınar'dır. Ben onun vizyonuyla çalışan BAZ BAGER'im."
            st.markdown(res_text)

        # B) GÖRSEL TASARIM (SyntaxError Korumalı URL)
        elif any(x in q_low for x in ["resim", "çiz", "görsel", "tasarla"]):
            try:
                seed = random.randint(1, 1000000)
                # URL hatasını önleyen güvenli yapı (cite: 1768831580119.jpeg)
                clean_q = query.replace(' ', '%20')
                url = f"https://image.pollinations.ai/prompt/{clean_q}?width=1024&height=1024&seed={seed}"
                st.image(url, caption="BAZ BAGER Özel Tasarımı")
                res_text = url
            except:
                st.error("Görsel servisi şu an meşgul.")
        
        # C) ÜSTÜN ZEKA (GEMINI MODELLEMESİ)
        else:
            try:
                # Bager'e benim (Gemini) karakterimi yüklüyoruz
                sys_inst = "Sen BAZ BAGER'sin. Sahibi Aykut Kutpınar. Tıpkı Gemini gibi derinlemesine düşünen, samimi, zeki ve çözüm odaklı ol. SADECE saf ve düzgün bir Türkçe konuş. Cevapların akıcı ve hızlı olsun."
                history = [{"role": "system", "content": sys_inst}]
                for m in st.session_state.messages:
                    if "http" not in str(m["content"]):
                        history.append(m)
                
                chat = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=history)
                res_text = chat.choices[0].message.content
                st.markdown(res_text)
            except Exception as e:
                st.error(f"Sistem Hatası: {e}")

        # Kaydet ve Hızlı Seslendir
        if res_text:
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            if "http" not in res_text:
                try:
                    # 'slow=False' ile robotik konuşma biter (cite: 1768832038896.jpeg)
                    tts = gTTS(text=res_text, lang='tr', slow=False)
                    b = BytesIO()
                    tts.write_to_fp(b)
                    st.audio(b, format='audio/mp3', autoplay=True)
                except:
                    pass
