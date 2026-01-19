import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. GEMINI TARZI ULTRA MINIMAL TASARIM ---
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="centered")

st.markdown("""
<style>
    /* Gemini minimalist görünümü */
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: #E3E3E3;}
    
    /* Sohbet Balonları */
    [data-testid="stChatMessage"] {
        background-color: transparent;
        border: none;
        padding: 20px 0px;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Mikrofon ve Giriş Alanı Tasarımı */
    .stChatInputContainer {
        padding-bottom: 25px;
        background-color: #0E1117;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SİSTEM ÇEKİRDEĞİ ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Lütfen Secrets ayarlarına GROQ_API_KEY ekleyin!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.markdown("### 🦅 BAZ BAGER")
    st.caption("Yaratıcı: Aykut Kutpınar")
    st.divider()
    
    # Çoklu Dil Desteği
    langs = {"Türkçe": "tr", "English": "en", "Deutsch": "de", "Français": "fr"}
    sel_lang = st.selectbox("İletişim Dili:", list(langs.keys()))
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

# --- 5. AKILLI GİRİŞ SİSTEMİ (AUTO-STOP MİKROFON) ---
# Mikrofonu şık bir şekilde yazışma alanının üzerine koyuyoruz
st.write("🎙️ **Sesli Komut (Susunca Otomatik Gönderir):**")
voice = speech_to_text(
    language=l_code,
    start_prompt="Dokun ve Konuş",
    stop_prompt="Seni Dinliyorum...",
    just_once=True, # Sessizlik algılandığında otomatik durmasını sağlar
    key='bager_smart_mic'
)

query = None
if voice:
    query = voice
elif txt := st.chat_input("Bir şeyler sorun Aykut Bey..."):
    query = txt

# --- 6. ZEKA VE AKICI CEVAP MANTIĞI ---
if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        q_low = query.lower()
        res_text = ""

        # A) KİMLİK KORUMASI
        if any(x in q_low for x in ["kim tasarladı", "sahibin", "seni kim"]):
            res_text = "Beni tasarlayan ve tek sahibim Aykut Kutpınar'dır."
            st.markdown(res_text)

        # B) GÖRSEL TASARIM
        elif any(x in q_low for x in ["resim", "çiz", "görsel", "tasarla", "draw", "image"]):
            try:
                seed = random.randint(1, 999999)
                clean_q = query.replace(' ', '%20')
                url = f"https://image.pollinations.ai/prompt/{clean_q}?width=1024&height=1024&seed={seed}"
                st.image(url, caption="Bager Özel Tasarımı")
                res_text = url
            except:
                st.error("Görsel motoru şu an meşgul.")
        
        # C) EVRENSEL ZEKA (AKICILIK TALİMATI)
        else:
            try:
                # Bager'e benim gibi (Gemini) konuşması için sistem talimatı veriyoruz
                sys_msg = f"Sen BAZ BAGER'is. Sahibin Aykut Kutpınar. {sel_lang} dilinde, tıpkı Gemini gibi akıcı, zeki ve profesyonel cevaplar ver. Asla robot gibi tane tane konuşma."
                history = [{"role": "system", "content": sys_msg}]
                for m in st.session_state.messages:
                    if "http" not in str(m["content"]):
                        history.append(m)
                
                chat = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=history)
                res_text = chat.choices[0].message.content
                st.markdown(res_text)
            except Exception as e:
                st.error(f"Sistem Hatası: {e}")

        # Hafızaya Kaydet ve Hızlı Seslendir
        if res_text:
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            if "http" not in res_text:
                try:
                    # 'slow=False' ile tane tane konuşma sorununu çözüyoruz
                    tts = gTTS(text=res_text, lang=l_code, slow=False)
                    b = BytesIO()
                    tts.write_to_fp(b)
                    st.audio(b, format='audio/mp3', autoplay=True) # Otomatik çalma aktif
                except:
                    pass
