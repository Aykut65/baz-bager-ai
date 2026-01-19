import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. GEMINI TARZI ULTRA MODERN TASARIM ---
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="centered")

# Görsel 1768832132040'daki siyah ekran hatasını önlemek için güvenli CSS
st.markdown("<style>#MainMenu,footer,header{visibility:hidden;}.stApp{background-color:#0E1117;color:#E3E3E3;}[data-testid='stChatMessage']{background-color:transparent;border:none;padding:20px 0;max-width:800px;margin:0 auto;}.stChatInputContainer{padding-bottom:30px;background-color:#0E1117;}</style>", unsafe_allow_html=True)

# --- 2. SİSTEM ÇEKİRDEĞİ ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Secrets ayarlarına GROQ_API_KEY eklenmemiş!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. YAN MENÜ (SideBar) ---
with st.sidebar:
    st.markdown("### 🦅 BAZ BAGER")
    st.caption("Sahibi: Aykut Kutpınar")
    st.divider()
    langs = {"Türkçe": "tr", "English": "en", "Deutsch": "de", "Français": "fr"}
    sel_lang = st.selectbox("Dil Seçin:", list(langs.keys()))
    l_code = langs[sel_lang]
    if st.button("Sohbeti Sıfırla"):
        st.session_state.messages = []
        st.rerun()

# --- 4. SOHBET AKIŞI ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        msg_val = str(m["content"])
        if "http" in msg_val and "pollinations" in msg_val:
            st.image(msg_val, use_container_width=True)
        else:
            st.markdown(msg_val)

# --- 5. AKILLI MİKROFON (SUSUNCA OTOMATİK DURUR) ---
st.write("🎙️ **Sesli Komut:**")
voice = speech_to_text(
    language=l_code,
    start_prompt="Dokun ve Konuş",
    stop_prompt="Seni Dinliyorum...",
    just_once=True, # Sessizlik algılandığında otomatik durur
    key='bager_titanium_mic'
)

# --- 6. GİRİŞ VE CEVAP MANTIĞI ---
query = None
if voice:
    query = voice
elif txt := st.chat_input("Gemini gibi akıcı... Bir şeyler yazın Aykut Bey"):
    query = txt

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        q_low = query.lower()
        res_text = ""

        # Kimlik Koruması
        if any(x in q_low for x in ["kim tasarladı", "sahibin", "seni kim"]):
            res_text = "Beni tasarlayan ve tek sahibim Aykut Kutpınar'dır."
            st.markdown(res_text)
        
        # Resim Üretimi (Hata Korumalı URL)
        elif any(x in q_low for x in ["resim", "çiz", "görsel", "image"]):
            try:
                seed = random.randint(1, 999999)
                clean_q = query.replace(' ', '%20')
                url = f"https://image.pollinations.ai/prompt/{clean_q}?width=1024&height=1024&seed={seed}"
                st.image(url, caption="Bager Tasarımı")
                res_text = url
            except:
                st.error("Görsel motoru meşgul.")
        
        # Zeka ve Akıcı Cevap (Llama 3.3)
        else:
            try:
                sys_msg = f"Sen BAZ BAGER'sin. Sahibin Aykut Kutpınar. {sel_lang} dilinde, tıpkı Gemini gibi akıcı ve profesyonel cevap ver. Asla robot gibi tane tane konuşma."
                history = [{"role": "system", "content": sys_msg}]
                for m in st.session_state.messages:
                    if "http" not in str(m["content"]):
                        history.append(m)
                
                chat = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=history)
                res_text = chat.choices[0].message.content
                st.markdown(res_text)
            except Exception as e:
                st.error(f"Sistem Hatası: {e}")

        if res_text:
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            if "http" not in res_text:
                try:
                    # 'slow=False' ile akıcı ve hızlı konuşma
                    tts = gTTS(text=res_text, lang=l_code, slow=False)
                    b = BytesIO()
                    tts.write_to_fp(b)
                    st.audio(b, format='audio/mp3', autoplay=True)
                except:
                    pass
