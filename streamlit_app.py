import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. SAYFA VE MODERN TASARIM AYARLARI ---
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="wide")

# CSS: Arayüzü Gemini gibi temiz, modern ve odaklanmış yapar
st.markdown("<style>.stApp {background-color: #0E1117; color: white;} .stChatMessage {border-radius: 15px; border: 1px solid #333;} footer {visibility: hidden;} header {visibility: hidden;}</style>", unsafe_allow_html=True)

# --- 2. YAN MENÜ: KİMLİK VE SES KONTROLÜ ---
with st.sidebar:
    st.markdown("# 🦅 BAZ BAGER")
    st.markdown("---")
    st.info("👤 **Sahibi:** Aykut Kutpınar")
    st.write("🎙️ **Sesli Komut Ver:**")
    # Mikrofon: Dokun ve konuş. Sen sustuğunda otomatik algılar.
    voice_msg = speech_to_text(
        language='tr',
        start_prompt="🔴 DOKUN VE KONUŞ",
        stop_prompt="⏳ DİNLİYORUM...",
        just_once=True,
        key='bager_mic'
    )
    st.markdown("---")
    if st.button("Sohbeti Sıfırla"):
        st.session_state.messages = []
        st.rerun()

# --- 3. SİSTEM ÇEKİRDEĞİ (API KONTROLÜ) ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Lütfen Secrets kısmına GROQ_API_KEY ekleyin.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SOHBET AKIŞI (GÖRÜNÜR ALAN) ---
# Boş ekran hatasını önlemek için geçmişi en başta yüklüyoruz
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        msg_content = str(m["content"])
        if "http" in msg_content and "pollinations" in msg_content:
            st.image(msg_content, use_container_width=True)
        else:
            st.markdown(msg_content)

# --- 5. GİRİŞ MERKEZİ (SES VEYA METİN) ---
user_input = None
if voice_msg:
    user_input = voice_msg
elif text_input := st.chat_input("Emret Aykut Bey..."):
    user_input = text_input

# --- 6. İŞLEM VE CEVAP MANTIĞI ---
if user_input:
    # Kullanıcı mesajını kaydet
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        cmd = user_input.lower()
        final_response = ""

        # A) KİMLİK SORGUSU (Resim tetikleyicilerinden önce kontrol edilir)
        identity_keys = ["kim tasarladı", "sahibin", "seni kim", "ismin ne", "yaratıcın"]
        if any(x in cmd for x in identity_keys):
            final_response = "Beni tasarlayan ve tek sahibim Aykut Kutpınar'dır."
            st.markdown(final_response)
            st.session_state.messages.append({"role": "assistant", "content": final_response})

        # B) GÖRSEL TASARIM (Resim Modülü)
        elif any(x in cmd for x in ["resim", "çiz", "görsel", "tasarla", "fotoğraf"]):
            try:
                seed_val = random.randint(1, 1000000)
                safe_prompt = user_input.replace(' ', '%20')
                img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=1024&seed={seed_val}&nologo=true&enhance=true"
                st.image(img_url)
                final_response = "Görseli Aykut Kutpınar'ın vizyonuyla hazırladım."
                st.session_state.messages.append({"role": "assistant", "content": img_url})
            except:
                st.error("Görsel motoru şu an meşgul.")
        
        # C) ÜSTÜN ZEKA (LLAMA 3.3)
        else:
            try:
                # Geçmişi temizle (resim linklerini zekaya gönderme)
                clean_history = [{"role": "system", "content": "Sen BAZ BAGER'sin. Sahibin Aykut Kutpınar. Çok zeki, kısa ve net cevaplar ver."}]
                for m in st.session_state.messages:
                    if "http" not in str(m["content"]):
                        clean_history.append(m)
                
                chat_res = client.chat.completions.
