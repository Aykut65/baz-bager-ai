import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. PREMIUM ARAYÜZ TASARIMI ---
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="centered")

# CSS: Gemini/ChatGPT tarzı modern bir görünüm sağlar
st.markdown("""
<style>
    /* Streamlit standartlarını gizle */
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: #E0E0E0;}
    
    /* Sohbet Balonları Tasarımı */
    [data-testid="stChatMessage"] {
        border-radius: 15px; 
        margin-bottom: 12px; 
        padding: 15px;
        border: 1px solid #30363d;
    }
    
    /* Başlık ve Buton Renkleri */
    h1, h2, h3 {color: #FF4B4B; text-align: center;}
    .stButton>button {width: 100%; border-radius: 20px;}
</style>
""", unsafe_allow_html=True)

# --- 2. YAN MENÜ (KONTROL PANELİ) ---
with st.sidebar:
    st.markdown("## 🦅 BAZ BAGER")
    st.markdown("---")
    st.markdown("👤 **Yaratıcı:** Aykut Kutpınar")
    st.markdown("⚡ **Motor:** Llama 3.3 70B")
    st.divider()
    st.write("🎙️ **Sesli Kontrol:**")
    # Akıllı Mikrofon: Yan panelde her an hazır
    voice_command = speech_to_text(
        language='tr', 
        start_prompt="🔴 Dokun ve Konuş", 
        stop_prompt="⏳ Dinliyorum...", 
        just_once=True, 
        key='bager_mic_platinum'
    )
    st.divider()
    if st.button("Sohbeti Sıfırla"):
        st.session_state.messages = []
        st.rerun()

# --- 3. SİSTEM ÇEKİRDEĞİ ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Lütfen Secrets kısmına GROQ_API_KEY ekleyin.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SOHBET AKIŞI ---
# Mesajları Gemini tarzı, baştan sona akıcı şekilde yükler
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        content = str(m["content"])
        if "http" in content and "pollinations" in content:
            st.image(content, use_container_width=True)
        else:
            st.markdown(content)

# --- 5. GİRİŞ KONTROLÜ (HİBRİT) ---
user_query = None
if voice_command:
    user_query = voice_command
elif chat_txt := st.chat_input("Emret Aykut Bey..."):
    user_query = chat_txt

# --- 6. ZEKA VE CEVAP MANTIĞI ---
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        q_low = user_query.lower()
        response = ""

        # A) KİMLİK KORUMASI (Görsel 1768810020603 hatası çözümü)
        # "Tasarla" kelimesi geçse bile önce kimlik kontrolü yapar
        id_keys = ["kim tasarladı", "sahibin", "seni kim", "yaratıcın", "ismin ne"]
        if any(x in q_low for x in id_keys):
            response = "Beni tasarlayan ve tek sahibim Aykut Kutpınar'dır."
            st.markdown(response)

        # B) GÖRSEL MODÜLÜ (Görsel 1768809545608 hatası çözümü)
        elif any(x in q_low for x in ["resim", "çiz", "görsel", "tasarla"]):
            try:
                seed_val = random.randint(1, 10**7)
                img_url = f"https://image.pollinations.ai/prompt/{user_query.replace(' ', '%20')}?width=1024&height=1024&seed={seed_val}&nologo=true&enhance=true"
                st.image(img_url, caption="Bager'in Tasarımı")
                response = img_url # URL hafızaya kaydedilir
            except:
                st.error("Görsel motoru şu an yoğun.")
        
        # C) ÜSTÜN ZEKA (LLAMA 3.3 70B)
        else:
            try:
                history = [{"role": "system", "content": "Sen BAZ BAGER'sin. Sahibin Aykut Kutpınar. Çok zeki, özgüvenli ve net cevaplar ver."}]
                for m in st.session_state.messages:
                    if "http" not in str(m["content"]):
                        history.append(m)
                
                chat = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=history)
                response = chat.choices[0].message.content
                st.markdown(response)
            except Exception as e:
                st.error(f"Zeka Hatası: {e}")

        # Hafızaya ekle ve sesli yanıt ver
        if response:
            st.session_state.messages.append({"role": "assistant", "content": response})
            # Sadece metin ise seslendir (Görsel 1768816646779 tarzı oynatıcı)
            if "http" not in response:
                try:
                    tts = gTTS(text=response, lang='tr')
                    audio_io = BytesIO()
                    tts.write_to_fp(audio_io)
                    st.audio(audio_io, format='audio/mp3', start_time=0)
                except:
                    pass
