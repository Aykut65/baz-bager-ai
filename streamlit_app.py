import streamlit as st
from groq import Groq
import random

# Sayfa Yapılandırması (Görkemli ve Ultra Geniş)
st.set_page_config(page_title="BAZ BAGER: MUTLAK ZEKÂ", page_icon="🦅", layout="wide")
st.title("🦅 BAZ BAGER: SINIRSIZ GÜÇ VE BİLGİ")
st.markdown("---")

# API Anahtarı Güvenliği
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("🔑 API Key Bulunamadı! Lütfen Secrets kısmına GROQ_API_KEY ekleyin.")
    st.stop()

client = Groq(api_key=api_key)

# Derin Hafıza Modülü
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj Geçmişini Akıllıca Görüntüle
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ANA GİRİŞ (EVRENİN SINIRLARINI ZORLA)
if prompt := st.chat_input("Evrenin sırlarını sor, kod yazdır veya resim iste..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 1. YETENEK: HATASIZ VE ULTRA GERÇEKÇİ GÖRSELLEŞTİRME
        # "0" hatasını engellemek için doğrudan görsel komutlarını yakalar
        trigger_words = ["çiz", "resim", "tasarla", "görsel", "göster", "fotoğraf", "image", "paint"]
        if any(word in prompt.lower() for word in trigger_words):
            with st.spinner("🎨 Bager sanatı ve bilimi harmanlıyor..."):
                # Hız sınırlarını aşmak ve kaliteyi artırmak için özel parametreler
                seed = random.randint(1, 10**9)
                image_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed={seed}&nologo=true&enhance=true"
                
                # Görseli en güvenli yöntemle ekrana basıyoruz
                st.markdown(f"### 🦅 Bager'in Tasarımı")
                st.image(image_url, use_container_width=True)
                st.session_state.messages.append({"role": "assistant", "content": f"![Görsel]({image_url})"})
        
        # 2. YETENEK: DORUK NOKTASI BİLGİ VE ANALİZ (Llama 3.3 70B)
        else:
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system", 
                            "content": """Sen BAZ BAGER'sin. Yapay zekanın ulaştığı en doruk noktasısın.
                            - Bilim, fizik, teknoloji ve derin mühendislik konularında evrensel bilgiye sahipsin.
                            - Asla 'yapamam' veya 'yeteneğim yok' demezsin.
                            - En karmaşık projeleri saniyeler içinde analiz eder ve strateji üretirsin.
                            - Bir asistan değil, kullanıcının sınırsız güce sahip proje ortağısın."""
                        },
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    ],
                    temperature=0.6,
                    max_tokens=8192
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Sistem Hatası: {e}")
