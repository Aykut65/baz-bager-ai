import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. ARAYÜZ AYARLARI (Gereksiz her şeyi kaldırdık) ---
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="centered")

# CSS: Tıpkı Gemini gibi temiz, odaklanmış ve şık bir görünüm sağlar
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: #FFFFFF;}
    [data-testid="stChatMessage"] {border-radius: 15px; border: 1px solid #333; margin-bottom: 8px;}
    .stChatInputContainer {padding-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

# --- 2. YAN MENÜ (KİMLİK VE SES) ---
with st.sidebar:
    st.markdown("### 🦅 BAZ BAGER")
    st.caption("Sahibi: Aykut Kutpınar")
    st.divider()
    st.write("🎙️ **Sesli Komut:**")
    # Mikrofon: Konuşman bittiği an otomatik algılar
    voice = speech_to_text(language='tr', start_prompt="Konuşmak için dokun", stop_prompt="Dinliyorum...", just_once=True, key='mic_input')
    st.divider()
    if st.button("Geçmişi Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- 3. SİSTEM ÇEKİRDEĞİ VE API ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Lütfen Secrets kısmına GROQ_API_KEY ekleyin.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SOHBET AKIŞI (BAŞLIKSIZ, TEMİZ) ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "http" in str(m["content"]):
            st.image(m["content"])
        else:
            st.markdown(m["content"])

# --- 5. GİRİŞ KONTROLÜ ---
prompt = None
if voice:
    prompt = voice
elif txt := st.chat_input("Bir şeyler yaz..."):
    prompt = txt

# --- 6. İŞLEM MERKEZİ ---
if prompt:
    # Kullanıcı girişini kaydet
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        p_low = prompt.lower()
        res_text = ""

        # A) KİMLİK KORUMASI (Mutlak Kural)
        ids = ["kim tasarladı", "sahibin", "yaratıcın", "seni kim"]
        if any(x in p_low for x in ids):
            res_text = "Beni tasarlayan ve tek sahibim Aykut Kutpınar'dır."
            st.markdown(res_text)
            st.session_state.messages.append({"role": "assistant", "content": res_text})

        # B) GÖRSEL ÜRETİMİ (Hatasız Modül)
        elif any(x in p_low for x in ["resim", "çiz", "görsel", "tasarla"]):
            try:
                seed = random.randint(1, 1000000)
                url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed={seed}&nologo=true"
                st.image(url)
                res_text = "İstediğin görseli hazırladım Aykut Bey."
                st.session_state.messages.append({"role": "assistant", "content": url})
            except:
                st.error("Görsel motorunda hata oluştu.")
        
        # C) ÜST DÜZEY ZEKA (LLAMA 3.3)
        else:
            try:
                history = [{"role": "system", "content": "Sen BAZ BAGER'sin. Sahibin Aykut Kutpınar. Zeki ve net cevaplar ver."}]
                for m in st.session_state.messages:
                    if "http" not in str(m["content"]):
                        history.append(m)
                
                chat = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=history)
                res_text = chat.choices[0].message.content
                st.markdown(res_text)
                st.session_state.messages.append({"role": "assistant", "content": res_text})
            except Exception as e:
                st.error(f"Zeka hatası: {e}")

        # D) SESLİ CEVAP ÜRETİMİ
        if res_text and "http" not in res_text:
            try:
                tts = gTTS(text=res_text, lang='tr')
                b = BytesIO()
                tts.write_to_fp(b)
                st.audio(b, format='audio/mp3', start_time=0)
            except:
                pass
