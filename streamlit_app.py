import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. SAYFA YAPILANDIRMASI VE TASARIM ---
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="wide")

# CSS: Arayüzü Gemini gibi temiz ve modern yapar
st.markdown("<style>.stApp {background-color: #0E1117; color: white;} .stChatMessage {border-radius: 15px; border: 1px solid #333;} footer {visibility: hidden;} header {visibility: hidden;}</style>", unsafe_allow_html=True)

# --- 2. YAN MENÜ (SOL PANEL) ---
with st.sidebar:
    st.markdown("# 🦅 BAZ BAGER")
    st.markdown("---")
    st.info("👤 **Sahibi:** Aykut Kutpınar")
    st.write("🎙️ **Sesli Komut:**")
    # Akıllı mikrofon: Dokun ve konuş. Sen sustuğunda otomatik algılar.
    voice_msg = speech_to_text(
        language='tr',
        start_prompt="🔴 DOKUN VE KONUŞ",
        stop_prompt="⏳ DİNLİYORUM...",
        just_once=True,
        key='bager_mic_final'
    )
    st.markdown("---")
    if st.button("Sohbeti Sıfırla"):
        st.session_state.messages = []
        st.rerun()

# --- 3. API BAĞLANTISI ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Secrets kısmında GROQ_API_KEY eksik!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SOHBET AKIŞI (EKRAN YÜKLEMESİ) ---
# Boş ekran hatasını önlemek için geçmiş mesajları hemen yüklüyoruz
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        msg_val = str(m["content"])
        if "http" in msg_val and "pollinations" in msg_val:
            st.image(msg_val, use_container_width=True)
        else:
            st.markdown(msg_val)

# --- 5. GİRİŞ KONTROLÜ (SES VEYA YAZI) ---
user_query = None
if voice_msg:
    user_query = voice_msg
elif text_box := st.chat_input("Emret Aykut Bey..."):
    user_query = text_box

# --- 6. İŞLEM MERKEZİ ---
if user_query:
    # Kullanıcı mesajını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        q_low = user_query.lower()
        final_text = ""

        # A) KİMLİK SORGUSU (Resimden önce kontrol edilir)
        ids = ["kim tasarladı", "sahibin", "seni kim", "yaratıcın", "ismin ne"]
        if any(x in q_low for x in ids):
            final_text = "Beni tasarlayan ve tek sahibim Aykut Kutpınar'dır."
            st.markdown(final_text)
            st.session_state.messages.append({"role": "assistant", "content": final_text})

        # B) RESİM ÜRETİMİ (Görsel Modülü)
        elif any(x in q_low for x in ["resim", "çiz", "görsel", "tasarla", "fotoğraf"]):
            try:
                seed_val = random.randint(1, 1000000)
                url = f"https://image.pollinations.ai/prompt/{user_query.replace(' ', '%20')}?width=1024&height=1024&seed={seed_val}&nologo=true&enhance=true"
                st.image(url, caption="Bager Tasarımı")
                final_text = "Görseli Aykut Kutpınar'ın vizyonuyla hazırladım."
                st.session_state.messages.append({"role": "assistant", "content": url})
            except:
                st.error("Görsel servisi şu an meşgul.")
        
        # C) ÜSTÜN ZEKA (Sohbet Modülü)
        else:
            try:
                # Geçmişi temizle (resimleri zekaya gönderme)
                history = [{"role": "system", "content": "Sen BAZ BAGER'sin. Sahibin Aykut Kutpınar. Zeki ve net cevap ver."}]
                for m in st.session_state.messages:
                    if "http" not in str(m["content"]):
                        history.append(m)
                
                # Groq API çağrısı
                comp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=history)
                final_text = comp.choices[0].message.content
                st.markdown(final_text)
                st.session_state.messages.append({"role": "assistant", "content": final_text})
            except Exception as e:
                st.error(f"Sistem Hatası: {e}")

        # --- D) SESLİ CEVAP (AUTO-PLAY)
