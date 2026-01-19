import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. GEMINI TARZI ULTRA MODERN TASARIM ---
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="centered")

# Siyah ekran ve yazım hatalarını önlemek için en güvenli CSS yapısı (cite: 1768832132040.jpeg)
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: #E3E3E3;}
    [data-testid="stChatMessage"] {background-color: transparent; border: none; padding: 20px 0; max-width: 800px; margin: 0 auto;}
    .stChatInputContainer {padding-bottom: 30px; background-color: #0E1117;}
</style>
""", unsafe_allow_html=True)

# --- 2. SİSTEM ÇEKİRDEĞİ ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Secrets ayarlarında GROQ_API_KEY eksik!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.markdown("### 🦅 BAZ BAGER")
    st.caption("Yaratıcı & Sahibi: Aykut Kutpınar")
    st.divider()
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

# --- 5. AKILLI MİKROFON (SUSUNCA OTOMATİK İŞLER) ---
# Sessizliği algıladığı an kaydı bitirip cevaba geçer (cite: 1768831809607.jpeg)
st.write("🎙️ **Sesli Komut:**")
voice_input = speech_to_text(
    language='tr',
    start_prompt="Konuşmak için Dokun",
    stop_prompt="Dinliyorum Aykut Bey...",
    just_once=True, 
    key='bager_final_engine'
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

        # A) KİMLİK KORUMASI
        if any(x in q_low for x in ["kim tasarladı", "sahibin", "seni kim"]):
            res_text = "Beni tasarlayan ve tek sahibim Aykut Kutpınar'dır. Ben onun vizyonuyla çalışan BAZ BAGER'im."
            st.markdown(res_text)

        # B) GÖRSEL TASARIM (Hatasız URL Yapısı)
        elif any(x in q_low for x in ["resim", "çiz", "görsel", "tasarla"]):
            try:
                seed = random.randint(1, 1000000)
                clean_q = query.replace(' ', '%20')
                # Görsel 1768831580119 hatasını önlemek için URL'yi güvenli birleştirme
                url = f"https://image.pollinations.ai/prompt/{clean_q}?width=1024&height=1024&seed={seed}"
                st.image(url, caption="BAZ BAGER Tasarımı")
                res_text = url
            except:
                st.error("Görsel motoru meşgul.")
        
        # C) ÜSTÜN ZEKA (GEMINI MODELLEMESİ)
        else:
            try:
                # Gemini talimatlarını Bager'e aktarıyoruz
                sys_inst = "Sen BAZ BAGER'sin. Sahibi Aykut Kutpınar. Gemini gibi zeki, empatik ve profesyonel ol. SADECE saf ve düzgün bir Türkçe konuş. Cevapların akıcı olsun."
                history = [{"role": "system", "content": sys_inst}]
                for m in st.session_state.messages:
                    if "http" not in str(m["content
