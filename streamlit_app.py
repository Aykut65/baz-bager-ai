import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. GEMINI TARZI TASARIM (CSS) ---
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="centered")

st.markdown("""
<style>
    /* Gemini minimalist arka plan ve font */
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {
        background-color: #0E1117;
        color: #E3E3E3;
        font-family: 'Inter', sans-serif;
    }
    
    /* Mesaj Baloncukları */
    [data-testid="stChatMessage"] {
        background-color: transparent;
        border: none;
        padding: 20px 0px;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Giriş alanını alta sabitleme ve güzelleştirme */
    .stChatInputContainer {
        padding-bottom: 30px;
        background-color: #0E1117;
    }
    
    /* Mikrofon butonu stili */
    .mic-container {
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.markdown("### 🦅 BAZ BAGER")
    st.caption("Owner: Aykut Kutpınar")
    st.divider()
    
    # Çoklu Dil Seçeneği
    langs = {"Türkçe": "tr", "English": "en", "Deutsch": "de", "Français": "fr"}
    sel_lang = st.selectbox("Language / Dil:", list(langs.keys()))
    l_code = langs[sel_lang]
    
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- 3. SİSTEM VE HAFIZA ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Secrets ayarlarında GROQ_API_KEY bulunamadı!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SOHBET AKIŞI ---
# Mesajları Gemini tarzı temiz bir akışla gösteriyoruz
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        msg_val = str(m["content"])
        if "http" in msg_val and "pollinations" in msg_val:
            st.image(msg_val, use_container_width=True)
        else:
            st.markdown(msg_val)

# --- 5. HİBRİT GİRİŞ ALANI (SES + YAZI) ---
# Mikrofonu yazma çubuğunun hemen üzerine şıkça yerleştiriyoruz
st.markdown('<div class="mic-container">', unsafe_allow_html=True)
voice = speech_to_text(
    language=l_code,
    start_prompt="🎙️ Konuşmak için Dokun",
    stop_prompt="⏳ Dinliyorum... (Susunca Biter)",
    just_once=True,
    key='gemini_mic'
)
st.markdown('</div>', unsafe_allow_html=True)

# Gemini tarzı yazışma kutusu
query = None
if voice:
    query = voice
elif txt := st.chat_input("Bir şeyler sorun veya isteyin..."):
    query = txt

# --- 6. ZEKA VE CEVAP MANTIĞI ---
if query:
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        q_low = query.lower()
        response_text = ""

        # A) KİMLİK KONTROLÜ
        if any(x in q_low for x in ["kim tasarladı", "sahibin", "seni kim", "yaratıcın"]):
            response_text = "Beni tasarlayan ve tek sahibim Aykut Kutpınar'dır."
            st.markdown(response_text)

        # B) RESİM ÜRETİMİ (Hatasız URL Yapısı)
        elif any(x in q_low for x in ["resim", "çiz", "görsel", "tasarla", "draw", "image"]):
            try:
                seed = random.randint(1, 1000000)
                clean_q = query.replace(' ', '%20')
                # Görsel 1768831580119 hatasını önlemek için URL'yi güvenli birleştirme
                url = f"https://image.pollinations.ai/prompt/{clean_q}?width=1024&height=1024&seed={seed}"
                st.image(url, caption="Bager'in Tasarımı")
                response_text = url # Hafıza için URL
            except:
                st.error("Görsel oluşturulamadı.")
        
        # C) EVRENSEL ZEKA (Llama 3.3)
        else:
            try:
                sys_msg = f"Sen BAZ BAGER'sin. Sahibin Aykut Kutpınar. {sel_lang} dilinde, tıpkı bir dahi gibi net cevaplar ver."
                history = [{"role": "system", "content": sys_msg}]
                for m in st.session_state.messages:
                    if "http" not in str(m["content"]):
                        history.append(m)
                
                chat = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=history)
                response_text = chat.choices[0].message.content
                st.markdown(response_text)
            except Exception as e:
                st.error(f"Sistem hatası: {e}")

        # Hafızaya Kaydet ve Seslendir
        if response_text:
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            # Sadece metin ise seslendir
            if "http" not in response_text:
                try:
                    tts = gTTS(text=response_text, lang=l_code)
                    b = BytesIO()
                    tts.write_to_fp(b)
                    st.audio(b, format='audio/mp3')
                except:
                    pass
