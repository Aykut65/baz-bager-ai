import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text
import random

# --- 1. ARAYÜZ VE TASARIM (GEMINI TARZI) ---
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="centered")

# CSS: Arayüzü modern, temiz ve siyah ekran hatasından uzak tutar
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stApp {background-color: #0E1117; color: white;} .stChatMessage {border-radius: 15px; border: 1px solid #444; margin-bottom: 10px;}</style>", unsafe_allow_html=True)

# --- 2. SİSTEM VE API GÜVENLİĞİ ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Secrets kısmına GROQ_API_KEY ekleyin.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. ANA EKRAN: KONUŞMA DÜĞMESİ (MİKROFON) ---
st.markdown("<h2 style='text-align: center;'>🦅 BAZ BAGER</h2>", unsafe_allow_html=True)
st.write("🎙️ **Sesli Komut Vermek İçin Dokun:**")

# Görsel 1768816481393'teki butonu merkeze sabitledik
voice_input = speech_to_text(
    language='tr',
    start_prompt="🔴 KONUŞMAYI BAŞLAT",
    stop_prompt="⏳ DİNLİYORUM... (Susunca Biter)",
    just_once=True,
    key='bager_mic_final'
)

st.divider()

# --- 4. SOHBET AKIŞI (MESAJLARI GÖSTER) ---
# Boş ekran hatasını önlemek için mesajlar döngüsü her zaman çalışır
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        m_cont = str(m["content"])
        if "http" in m_cont and "pollinations" in m_cont:
            st.image(m_cont, use_container_width=True)
        else:
            st.markdown(m_cont)

# --- 5. GİRİŞ KONTROLÜ (SES VEYA METİN) ---
query = None
if voice_input:
    query = voice_input
elif text_box := st.chat_input("Emret Aykut Bey..."):
    query = text_box

# --- 6. İŞLEM MERKEZİ (ZEKÂ VE RESİM) ---
if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        q_low = query.lower()
        res_text = ""

        # A) KİMLİK: Aykut Kutpınar (Resimden önce kontrol edilir)
        ids = ["kim tasarladı", "sahibin", "seni kim", "yaratıcın", "ismin ne"]
        if any(x in q_low for x in ids):
            res_text = "Beni tasarlayan ve tek sahibim Aykut Kutpınar'dır."
            st.markdown(res_text)

        # B) RESİM: Pollinations HQ
        elif any(x in q_low for x in ["resim", "çiz", "görsel", "tasarla"]):
            try:
                seed = random.randint(1, 1000000)
                url = f"https://image.pollinations.ai/prompt/{query.replace(' ', '%20')}?width=1024&height=1024&seed={seed}&nologo=true"
                st.image(url, caption="Bager'in Tasarımı")
                res_text = url # URL'yi hafızaya ekliyoruz
            except:
                st.error("Görsel servisi şu an meşgul.")
        
        # C) ZEKA: Llama 3.3 70B
        else:
            try:
                # Geçmişi zekaya gönderirken resimleri filtrele
                hist = [{"role": "system", "content": "Sen BAZ BAGER'sin. Sahibin Aykut Kutpınar. Çok zeki ve kısa cevap ver."}]
                for m in st.session_state.messages:
                    if "http" not in str(m["content"]):
                        hist.append(m)
                
                comp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=hist)
                res_text = comp.choices[0].message.content
                st.markdown(res_text)
            except Exception as e:
                st.error(f"Zekâ Hatası: {e}")

        # Hafızaya ekle ve sesli yanıt ver
        if res_text:
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            if "http" not in res_text:
                try:
                    tts = gTTS(text=res_text, lang='tr')
                    b = BytesIO()
                    tts.write_to_fp(b)
                    st.audio(b, format='audio/mp3', start_time=0)
                except:
                    pass
