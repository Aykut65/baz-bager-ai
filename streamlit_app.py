import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. PREMİUM ARAYÜZ AYARLARI ---
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="centered")

# Gemini/ChatGPT tarzı modern tasarım
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: white;}
    .stChatMessage {border-radius: 15px; border: 1px solid #333; margin-bottom: 10px;}
</style>
""", unsafe_allow_html=True)

# --- 2. YAN MENÜ: DİL VE KİMLİK ---
with st.sidebar:
    st.markdown("## 🦅 BAZ BAGER")
    st.caption("Sahibi: Aykut Kutpınar")
    st.divider()
    
    # Tüm dilleri destekleyen dil seçici
    st.write("🌐 **İletişim Dili:**")
    langs = {"Türkçe": "tr", "English": "en", "Deutsch": "de", "Français": "fr", "Español": "es"}
    sel_lang = st.selectbox("Seçin:", list(langs.keys()))
    l_code = langs[sel_lang]
    
    st.divider()
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- 3. SİSTEM ÇEKİRDEĞİ ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Secrets kısmına GROQ_API_KEY ekleyin.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. ANA EKRAN: MERKEZİ KONUŞMA BUTONU ---
# Görsel 1768812304198'deki buton kaybolma sorununu çözmek için en üste sabitledik
st.markdown("<h3 style='text-align: center;'>🎙️ Bager'le Konuş</h3>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    voice = speech_to_text(
        language=l_code,
        start_prompt="🔴 DOKUN VE KONUŞ",
        stop_prompt="⏳ DİNLİYORUM...",
        just_once=True,
        key='bager_mic_main'
    )
st.divider()

# --- 5. SOHBET AKIŞI ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        msg = str(m["content"])
        if "http" in msg and "pollinations" in msg:
            st.image(msg, use_container_width=True)
        else:
            st.markdown(msg)

# --- 6. GİRİŞ YÖNETİMİ ---
query = None
if voice:
    query = voice
elif txt := st.chat_input("Buraya yazın Aykut Bey..."):
    query = txt

# --- 7. İŞLEM MERKEZİ ---
if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        q_low = query.lower()
        res = ""

        # A) KİMLİK KORUMASI (Mutlak Kural)
        ids = ["kim tasarladı", "sahibin", "seni kim", "yaratıcın", "who created you"]
        if any(x in q_low for x in ids):
            res = "Beni tasarlayan ve tek sahibim Aykut Kutpınar'dır."
            st.markdown(res)

        # B) GÖRSEL ÜRETİMİ (Hata Korumalı)
        elif any(x in q_low for x in ["resim", "çiz", "görsel", "image", "draw"]):
            try:
                seed = random.randint(1, 10**6)
                # f-string hatasını önlemek için URL'yi güvenli birleştiriyoruz
                base_url = "https://image.pollinations.ai/prompt/"
                clean_q = query.replace(' ', '%20')
                url = base_url + clean_q + "?width=1024&height=1024&seed=" + str(seed)
                st.image(url, caption="Bager Design")
                res = url
            except:
                st.error("Görsel motoru hatası.")
        
        # C) EVRENSEL ZEKA (Llama 3.3 70B)
        else:
            try:
                sys_msg = f"Sen BAZ BAGER'sin. Sahibin Aykut Kutpınar. {sel_lang} dilinde zeki ve net cevap ver."
                history = [{"role": "system", "content": sys_msg}]
                for m in st.session_state.messages:
                    if "http" not in str(m["content"]):
                        history.append(m)
                
                comp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=history)
                res = comp.choices[0].message.content
                st.markdown(res)
            except Exception as e:
                st.error(f"Zeka Hatası: {e}")

        # Kaydet ve Seslendir
        if res:
            st.session_state.messages.append({"role": "assistant", "content": res})
            if "http" not in res:
                try:
                    tts = gTTS(text=res, lang=l_code)
                    b = BytesIO()
                    tts.write_to_fp(b)
                    st.audio(b, format='audio/mp3')
                except:
                    pass
