import streamlit as st
from groq import Groq
import requests

# Sayfa Ayarları
st.set_page_config(page_title="BAZ BAGER ULTRA", page_icon="🦅", layout="centered")
st.title("🦅 BAZ BAGER: AKTİF")

# API Anahtarı
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("🔑 API Anahtarı eksik!")
    st.stop()

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları Ekrana Bas
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# KULLANICI GİRİŞİ
if prompt := st.chat_input("Bir şeyler sor veya resim iste..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # KRİTİK DEĞİŞİKLİK: Resim isteğini daha hassas yakalıyoruz
        trigger_words = ["çiz", "resim", "görsel", "fotoğraf", "image", "paint"]
        if any(word in prompt.lower() for word in trigger_words):
            try:
                # Daha güvenilir bir resim motoruna geçtik
                image_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1024&height=1024&nologo=true"
                
                # Resmi önce göster, sonra hafızaya kaydet
                st.image(image_url, caption="🦅 Bager senin için çizdi.")
                st.session_state.messages.append({"role": "assistant", "content": f"![Görsel]({image_url})"})
            except Exception as e:
                st.error("Resim motoru şu an meşgul, lütfen tekrar dene.")
        
        else:
            # Zekâ Modu (Llama 3.3 70B)
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Sen BAZ BAGER'sin. Çok zeki ve her emri ikiletmeden yerine getiren bir asistansın."},
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    ],
                    temperature=0.5
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Zekâ hatası: {e}")
