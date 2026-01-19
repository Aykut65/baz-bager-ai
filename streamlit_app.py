import streamlit as st
from groq import Groq
import random
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text

# Sayfa Yapılandırması
st.set_page_config(page_title="BAZ BAGER: JARVIS MODU", page_icon="🦅", layout="wide")

# Kenar Çubuğu (Sidebar) Tasarımı - Bager Logosu ve Durum
with st.sidebar:
    st.title("🦅 BAZ BAGER")
    st.markdown("**Sahibi:** Aykut Kutpınar")
    st.markdown("---")
    st.success("Sistem: Çevrimiçi")
    st.info("Mod: Hibrit (Ses & Metin)")

st.title("🦅 BAZ BAGER: HİBRİT ZEKÂ")

# API Anahtarı Kontrolü
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("🔑 API Anahtarı bulunamadı! Lütfen Secrets ayarlarını kontrol et.")
    st.stop()

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AKILLI SES GİRİŞİ (AUTO-STOP) ---
# Bunu ana ekranın üst kısmına veya sütunlara koyabiliriz.
# "just_once=True" ve tarayıcı tabanlı API sayesinde sen susunca otomatik durur.
c1, c2 = st.columns([1, 4])
with c1:
    st.write("🎙️ **Sesli Komut:**")
    # Butona basınca "Dinleniyor..." yazar, susunca otomatik gönderir.
    voice_text = speech_to_text(
        language='tr',
        start_prompt="🔴 Dokun ve Konuş",
        stop_prompt="⏳ Dinliyorum... (Susunca Otomatik Biter)",
        just_once=True,
        key='STT'
    )

# --- MESAJ GEÇMİŞİ ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- GİRİŞ MANTIĞI (Ses mi? Yazı mı?) ---
prompt = None

# Öncelik Seste: Eğer sesli metin geldiyse onu al
if voice_text:
    prompt = voice_text
# Ses yoksa, alttaki chat kutusuna bak
elif chat_input := st.chat_input("Mesaj yaz veya yukarıdan konuş..."):
    prompt = chat_input

# --- İŞLEM MERKEZİ ---
if prompt:
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 1. KİMLİK KORUMA (Aykut Kutpınar)
        identity_queries = ["kim tasarladı", "sahibin kim", "yaratıcın kim", "seni kim yaptı", "sen kimsin"]
        is_identity = any(q in prompt.lower() for q in identity_queries)
        
        # 2. RESİM MOTORU
        image_triggers = ["resim çiz", "görsel yap", "fotoğraf oluştur", "image", "paint", "tasarla"]
        is_image = any(t in prompt.lower() for t in image_triggers) and not is_identity

        response_text = ""

        if is_image:
            with st.spinner("🎨 Bager sanatını icra ediyor..."):
                try:
                    seed = random.randint(1, 10**9)
                    image_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed={seed}&nologo=true&enhance=true"
                    st.image(image_url, caption="🦅 Bager'in Tasarımı")
                    response_text = "İstediğin görseli senin için hazırladım Aykut Bey."
                    st.session_state.messages.append({"role": "assistant", "content": f"![Görsel]({image_url})"})
                except:
                    response_text = "Görsel sunucularında yoğunluk var, ama senin için tekrar deneyebilirim."

        else:
            # 3. ZEKÂ MODU (Llama 3.3)
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system", 
                            "content": "Sen BAZ BAGER'sin. Seni tasarlayan, yapan ve tek sahibin AYKUT KUTPINAR'dır. Cevapların kısa, net, zeki ve çözüm odaklı olsun. Türkçe konuş."
                        },
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    ],
                    temperature=0.6
                )
                response_text = completion.choices[0].message.content
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Hata: {e}")

        # --- SESLİ CEVAP (AĞIZ) ---
        if response_text:
            try:
                tts = gTTS(text=response_text, lang='tr')
                sound_file = BytesIO()
                tts.write_to_fp(sound_file)
                st.audio(sound_file, format='audio/mp3', start_time=0)
            except:
                pass # Ses hatası olursa sadece metin göster, akışı bozma
