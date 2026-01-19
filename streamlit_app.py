import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. PREMİUM TASARIM VE SAYFA AYARI ---
st.set_page_config(page_title="BAZ BAGER: GLOBAL", page_icon="🦅", layout="centered")

# CSS: Gemini tarzı modern, temiz ve siyah ekran hatasız arayüz
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: #FFFFFF;}
    [data-testid="stChatMessage"] {border-radius: 15px; border: 1px solid #333; margin-bottom: 8px;}
</style>
""", unsafe_allow_html=True)

# --- 2. YAN MENÜ: DİL VE KONTROL MERKEZİ ---
with st.sidebar:
    st.markdown("# 🦅 BAZ BAGER")
    st.caption("Sahibi: Aykut Kutpınar")
    st.divider()
    
    # EVRENSEL DİL SEÇİCİ
    st.write("🌐 **İletişim Dili (Language):**")
    lang_opt = {
        "Türkçe": "tr",
        "English": "en",
        "Deutsch": "de",
        "Français": "fr",
        "Español": "es",
        "Русский": "ru",
        "العربية": "ar",
        "日本語": "ja",
        "中文": "zh"
    }
    selected_lang_name = st.selectbox("Bir dil seçin:", list(lang_opt.keys()))
    lang_code = lang_opt[selected_lang_name]

    st.divider()
    st.write("🎙️ **Sesli Komut:**")
    # Mikrofon: Seçilen dile göre seni dinler
    voice_input = speech_to_text(
        language=lang_code, 
        start_prompt=f"{selected_lang_name} Konuş", 
        stop_prompt="Dinliyorum...", 
        just_once=True, 
        key='bager_global_mic'
    )
    
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

# --- 4. SOHBET AKIŞI (MODERN CHAT) ---
# Boş ekran hatasını önlemek için geçmişi en başta yüklüyoruz (cite: 1768812065656.jpeg)
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        c = str(m["content"])
        if "http" in c and "pollinations" in c:
            st.image(c, use_container_width=True)
        else:
            st.markdown(c)

# --- 5. GİRİŞ YÖNETİMİ ---
query = None
if voice_input:
    query = voice_input
elif txt_in := st.chat_input("Emret Aykut Bey..."):
    query = txt_in

# --- 6. EVRENSEL İŞLEM MERKEZİ ---
if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        q_low = query.lower()
        res_text = ""

        # A) KİMLİK KORUMASI (Aykut Kutpınar)
        id_keys = ["kim tasarladı", "sahibin", "seni kim", "ismin ne", "who created you", "who is your owner"]
        if any(x in q_low for x in id_keys):
            res_text = "Beni tasarlayan ve tek sahibim Aykut Kutpınar'dır."
            st.markdown(res_text)

        # B) EVRENSEL RESİM ÜRETİMİ (Pollinations HQ)
        elif any(x in q_low for x in ["resim", "çiz", "görsel", "tasarla", "draw", "image", "paint"]):
            try:
                seed = random.randint(1, 1000000)
                url = f"https://image.pollinations.ai/prompt/{query.replace(' ', '%20')}?width=1024&height=1024&seed={seed}&nologo
