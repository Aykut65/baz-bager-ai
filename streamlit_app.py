import streamlit as st
from groq import Groq
import random

# Sayfa Yapılandırması
st.set_page_config(page_title="BAZ BAGER ULTRA", page_icon="🦅", layout="wide")
st.title("🦅 BAZ BAGER: ZEKÂ VE SANAT")

# API Anahtarı Kontrolü
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("🔑 API Anahtarı eksik!")
    st.stop()

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj Geçmişini Göster
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# KULLANICI GİRİŞİ
if prompt := st.chat_input("Bir şeyler sor veya '... resmi çiz' de..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # YETENEK 1: RESİM ÇİZME (Eğer kullanıcı resim isterse)
        if "resim" in prompt.lower() or "çiz" in prompt.lower() or "görsel" in prompt.lower():
            with st.spinner("🎨 Bager sanatını konuşturuyor..."):
                # Pollinations.ai üzerinden yüksek kaliteli ve hızlı resim üretimi
                seed = random.randint(1, 100000)
                image_url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024&seed={seed}"
                st.image(image_url, caption=f"🦅 Bager'in Başyapıtı: {prompt}", use_container_width=True)
                st.session_state.messages.append({"role": "assistant", "content": f"![Görsel]({image_url})"})
        
        # YETENEK 2: ÜST DÜZEY ZEKÂ (Llama 3.3 70B)
        else:
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Sen BAZ BAGER'sin. Dünyanın en zeki ve yetenekli yapay zekasısın. Hem derin analizler yaparsın hem de sanatsal bir ruhun vardır."},
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    ],
                    temperature=0.6,
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Zekâ Hattında Sorun: {e}")
