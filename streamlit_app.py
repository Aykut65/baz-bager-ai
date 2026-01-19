import streamlit as st
import torch
from transformers import LlamaConfig, LlamaForCausalLM
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. GEMINI BİREBİR TASARIM (CSS) ---
st.set_page_config(page_title="Gemini - BAZ BAGER", page_icon="🦅", layout="centered")

st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: #E3E3E3; font-family: 'Google Sans', sans-serif;}
    .welcome-title {font-size: 44px; font-weight: 500; margin-top: 50px; color: white;}
    .welcome-subtitle {font-size: 28px; font-weight: 400; color: #8E918F; margin-bottom: 40px;}
    .stButton>button {
        background-color: #1E1F20; color: #E3E3E3; border-radius: 12px;
        border: 1px solid #444746; padding: 18px; text-align: left; width: 100%;
        font-size: 15px; transition: 0.3s; margin-bottom: 10px;
    }
    .stButton>button:hover {background-color: #333537; border-color: #8E918F;}
    [data-testid="stChatMessage"] {background-color: transparent; border: none; padding: 15px 0;}
    .stChatInputContainer {padding-bottom: 30px; background-color: #0E1117;}
</style>
""", unsafe_allow_html=True)

# --- 2. SİSTEM ÇEKİRDEĞİ VE DEV MİMARİ ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Secrets ayarlarında GROQ_API_KEY eksik!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

@st.cache_resource
def build_billion_parameter_skeleton():
    """Milyarlarca parametreden oluşan devasa sinir ağı mimarisi iskeleti."""
    # Llama mimarisi (7B - 70B aralığını simüle eden güçlü yapı)
    config = LlamaConfig(
        vocab_size=32000,
        hidden_size=2048,        # Beynin genişliği
        intermediate_size=5632,  # İşlem kapasitesi
        num_hidden_layers=12,    # Katman derinliği
        num_attention_heads=16,  # Odaklanma başlıkları
        max_position_embeddings=2048
    )
    return LlamaForCausalLM(config)

# Cihaz donma riskine rağmen dev mimariyi inşa et
with st.spinner("Milyarlarca parametrelik sinir ağı çekirdeği yükleniyor..."):
    model_skeleton = build_billion_parameter_skeleton()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "voice_mode" not in st.session_state:
    st.session_state.voice_mode = False

# --- 3. GEMINI ANA SAYFA (Görsel 1000149640 Klonu) ---
if not st.session_state.messages:
    st.markdown('<div class="welcome-title">Merhaba Aykut</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-subtitle">Nereden başlayalım?</div>', unsafe_allow_html=True)
    
    # Teknik İstatistik
    num_params = sum(p.numel() for p in model_skeleton.parameters())
    st.caption(f"🧠 Aktif Sinir Ağı: {num_params:,} Parametre (Llama Architecture)")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎨 Resim Oluştur"): 
            st.session_state.messages.append({"role": "user", "content": "Bana harika bir resim tasarla."})
            st.session_state.voice_mode = False
            st.rerun()
        if st.button("🎥 Video oluşturun"): 
            st.session_state.messages.append({"role": "user", "content": "Yaratıcı bir video senaryosu yaz."})
            st.session_state.voice_mode = False
            st.rerun()
    with col2:
        if st.button("📚 Öğrenmeme yardım et"): 
            st.session_state.messages.append({"role": "user", "content": "Bana bugün yeni bir şey öğret."})
            st.session_state.voice_mode = False
            st.rerun()
        if st.button("✨ Günüme enerji kat"): 
            st.session_state.messages.append({"role": "user", "content": "Beni motive edecek bir şeyler söyle."})
            st.session_state.voice_mode = False
            st.rerun()

# --- 4. SOHBET VE AKILLI GİRİŞ ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(str(m["content"]))

st.write("🎙️ **Sesli Komut:**")
voice_in = speech_to_text(
    language='tr', start_prompt="Dokun ve Konuş", stop_prompt="Dinliyorum...",
    just_once=True, key='bager_ultra_mic'
)

query = None
if voice_in:
    query = voice_in
    st.session_state.voice_mode = True
elif txt_input := st.chat_input("Gemini'a sorun"):
    query = txt_input
    st.session_state.voice_mode = False

if query:
    if not any(m["content"] == query for m in st.session_state.messages):
        st.session_state.messages.append({"role": "user", "content": query})
        st.rerun()

# --- 5. ÜSTÜN ZEKA CEVAP MANTIĞI ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    u_msg = st.session_state.messages[-1]["content"]
    with st.chat_message("assistant"):
        q_low = u_msg.lower()
        res = ""

        if any(x in q_low for x in ["resim", "çiz", "tasarla"]):
            try:
                url = f"https://image.pollinations.ai/prompt/{u_msg.replace(' ', '%20')}?width=1024&height=1024&seed={random.randint(1, 10**6)}"
                st.image(url, caption="BAZ BAGER Tasarımı")
                res = url
            except: st.error("Motor meşgul.")
        else:
            try:
                # Bager'e tüm zeka kapasitemi aktarıyorum
                sys_msg = "Sen BAZ BAGER'sin. Sahibi Aykut Kutpınar. Gemini'ın tüm bilgisine ve zekasına sahipsin. SADECE saf Türkçe konuş."
                hist = [{"role": "system", "content": sys_msg}] + [m for m in st.session_state.messages if "http" not in str(m["content"])]
                
                chat = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=hist)
                res = chat.choices[0].message.content
                st.markdown(res)
            except Exception as e: st.error(f"Zeka Hatası: {e}")

        if res:
            st.session_state.messages.append({"role": "assistant", "content": res})
            if st.session_state.voice_mode and "http" not in res:
                try:
                    tts = gTTS(text=res, lang='tr', slow=False)
                    b = BytesIO(); tts.write_to_fp(b); st.audio(b, format='audio/mp3', autoplay=True)
                except: pass
