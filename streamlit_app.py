import streamlit as st
from groq import Groq
import random
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text

# --- 1. AYARLAR ---
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="wide")

# CSS Kodunu tek satırda birleştirerek hata riskini sıfırladık
css_code = """
<style>
.stApp {background: linear-gradient(to right, #141E30, #243B55); color: white;}
.stChatMessage {background-color: rgba(255, 255, 255, 0.1); border-radius: 15px;}
h1 {text-align: center; color: #ffcc00; text-shadow: 2px 2px 4px #000000;}
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# --- 2. YAN MENÜ ---
with st.sidebar:
    st.header("🦅 BAZ BAGER")
    st.write("---")
    st.info("Sahibi: Aykut Kutpınar")
    st.success("Sistem: Aktif")

# --- 3. API BAĞLANTISI ---
try:
    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        st.error("API Key Eksik!")
        st.stop()
    client = Groq(api_key=api_key)
except:
    st.stop()

# --- 4. HAFIZA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 5. ARAYÜZ ---
st.title("🦅 BAZ BAGER: PREMIUM")
st.write("---")

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    # Ses Girişi
    voice_input = speech_to_text(
        language='tr',
        start_prompt="🔴 KONUŞ",
        stop_prompt="⏳ DİNLİYORUM...",
        just_once=True,
        key='mic_main',
        use_container_width=True
    )

# --- 6. GEÇMİŞİ GÖSTER ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if str(m["content"]).startswith("!["):
            st.markdown(m["content"])
        else:
            st.write(m["content"])

# --- 7. GİRİŞ KONTROLÜ ---
prompt = None
if voice_input:
    prompt = voice_input
elif chat_input := st.chat_input("Mesaj yazın..."):
    prompt = chat_input

# --- 8. CEVAP MEKANİZMASI ---
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # Kelime analizi (Hata riskini azaltmak için basitleştirildi)
        p_low = prompt.lower()
        # Kimlik soruları
        ids = ["kim tasarladı", "sahibin kim", "yaratıcın", "seni kim yaptı"]
        is_id = False
        for x in ids:
            if x in p_low:
                is_id = True
                break
        
        # Resim soruları
        imgs = ["resim", "çiz", "görsel", "tasarla"]
        is_img = False
        if not is_id:
            for x in imgs:
                if x in p_low:
                    is_img = True
                    break
        
        response_text = ""

        # A) Resim Modu
        if is_img:
            with st.spinner("Hazırlanıyor..."):
                try:
                    seed = random.randint(1, 999999)
                    safe_prompt = prompt.replace(" ", "%20")
                    url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=1024&seed={seed}&nologo=true&enhance=true"
                    st.image(url, caption="Bager Tasarımı")
                    response_text = "Görseli hazırladım Aykut Bey."
                    st.session_state.messages.append({"role": "assistant", "content": f"![img]({url})"})
                except:
                    response_text = "Resim servisi yoğun."

        # B) Zeka Modu
        else:
            try:
                # Sistem mesajını tek parça string yaptık, hata yapmaz.
                sys_msg = "Sen BAZ BAGER'sin. Sahibin ve yaratıcın AYKUT KUTPINAR. Türkçe konuş. Kısa ve net ol."
                
                # Mesaj listesini güvenli oluştur
                api_messages = [{"role": "system", "content": sys_msg}]
                for m in st.session_state.messages:
                    if not str(m["content"]).startswith("!["):
                        api_messages.append({"role": m["role"], "content": m["content"]})

                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=api_messages,
                    temperature=0.6
                )
                response_text = completion.choices[0].message.content
                st
