import streamlit as st
from groq import Groq
import random
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text

# --- 1. SAYFA VE CSS AYARLARI ---
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="wide")

# CSS Bloğunu hatasız hale getirdik
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #141E30, #243B55);
    color: white;
}
.stChatMessage {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 15px;
}
h1 {
    text-align: center;
    color: #ffcc00;
    text-shadow: 2px 2px 4px #000000;
}
</style>
""", unsafe_allow_html=True)

# --- 2. YAN MENÜ (KİMLİK) ---
with st.sidebar:
    st.header("🦅 BAZ BAGER")
    st.write("---")
    st.info("👤 **Sahibi:** Aykut Kutpınar")
    st.success("🟢 Durum: Aktif")
    st.warning("🎤 Ses: Açık")

# --- 3. API BAĞLANTISI ---
try:
    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        st.error("🔑 API Key Eksik! Lütfen Secrets ayarlarını kontrol et.")
        st.stop()
    client = Groq(api_key=api_key)
except:
    st.stop()

# --- 4. HAFIZA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 5. ANA BAŞLIK VE SES BUTONU ---
st.title("🦅 BAZ BAGER: PREMIUM")
st.write("---")

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    # Ses Girişi
    voice_input = speech_to_text(
        language='tr',
        start_prompt="🔴 KONUŞMAK İÇİN DOKUN",
        stop_prompt="⏳ DİNLİYORUM...",
        just_once=True,
        key='mic_main',
        use_container_width=True
    )

# --- 6. MESAJLARI GÖSTER ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if m["content"].startswith("!["):
            st.markdown(m["content"])
        else:
            st.write(m["content"])

# --- 7. GİRİŞ YÖNETİMİ ---
prompt = None
if voice_input:
    prompt = voice_input
elif chat_input := st.chat_input("Mesaj yazın Aykut Bey..."):
    prompt = chat_input

# --- 8. CEVAP ÜRETME ---
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # Kimlik ve Resim Kontrolü
        lower_prompt = prompt.lower()
        is_identity = any(x in lower_prompt for x in ["kim tasarladı", "sahibin kim", "yaratıcın", "seni kim yaptı"])
        is_image = any(x in lower_prompt for x in ["resim", "çiz", "görsel", "tasarla"]) and not is_identity
        
        response_text = ""

        # A) Resim Modu
        if is_image:
            with st.spinner("🎨 Resim hazırlanıyor..."):
                try:
                    seed = random.randint(1, 999999)
                    url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed={seed}&nologo=true&enhance=true"
                    st.image(url, caption="🦅 Bager Tasarımı")
                    response_text = "Görseli sizin için hazırladım Aykut Bey."
                    st.session_state.messages.append({"role": "assistant", "content": f"![img]({url})"})
                except:
                    response_text = "Resim servisine ulaşılamadı."
        
        # B) Zeka Modu
        else:
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Sen BAZ BAGER'sin
