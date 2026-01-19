import streamlit as st
from groq import Groq
import random
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text

# Sayfa Ayarları
st.set_page_config(page_title="BAZ BAGER: SESLİ ASİSTAN", page_icon="🦅", layout="wide")
st.title("🦅 BAZ BAGER: DUYAN VE KONUŞAN GÜÇ")

# API Anahtarı
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("🔑 API Anahtarı bulunamadı!")
    st.stop()

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SESLİ GİRİŞ (KULAK) ---
st.write("🎤 **Mikrofona bas ve konuş (İngilizce/Türkçe algılar):**")
# Mikrofondan gelen sesi metne çevirir
voice_input = speech_to_text(language='tr', start_prompt="🔴 Kayıt Başlat", stop_prompt="⬛ Kaydı Bitir", just_once=True, use_container_width=True)

# --- MESAJ GEÇMİŞİNİ GÖSTER ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- GİRİŞ YÖNETİMİ (SES veya YAZI) ---
prompt = None
# Eğer sesli giriş varsa onu kullan, yoksa yazı kutusuna bak
if voice_input:
    prompt = voice_input
elif chat_input := st.chat_input("Veya buraya yazarak emret Aykut Kutpınar..."):
    prompt = chat_input

# --- İŞLEM MERKEZİ ---
if prompt:
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 1. KİMLİK KORUMA (Aykut Kutpınar)
        identity_queries = ["kim tasarladı", "sahibin kim", "yaratıcın kim", "seni kim yaptı"]
        is_identity = any(q in prompt.lower() for q in identity_queries)
        
        # 2. RESİM MOTORU
        image_triggers = ["resim çiz", "görsel yap", "fotoğraf oluştur", "image", "paint"]
        is_image = any(t in prompt.lower() for t in image_triggers) and not is_identity

        response_text = ""

        if is_image:
            with st.spinner("🎨 Bager senin için çiziyor..."):
                seed = random.randint(1, 10**9)
                image_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed={seed}&nologo=true"
                st.image(image_url, caption="🦅 Bager'in Eseri")
                response_text = "İstediğin görseli senin için hazırladım Aykut Bey."
                st.session_state.messages.append({"role": "assistant", "content": f"![Görsel]({image_url})"})
        
        else:
            # 3. ZEKÂ MODU (Llama 3.3)
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system", 
                            "content": "Sen BAZ BAGER'sin. Seni tasarlayan, yapan ve tek sahibin AYKUT KUTPINAR'dır. Cevapların kısa, net ve zeki olsun. Türkçe konuş."
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
                # Metni sese çevir (Türkçe)
                tts = gTTS(text=response_text, lang='tr')
                sound_file = BytesIO()
                tts.write_to_fp(sound_file)
                st.audio(sound_file, format='audio/mp3', start_time=0)
            except Exception as e:
                st.warning("Ses motoru şu an yoğun, ama cevabı ekrana yazdım.")
