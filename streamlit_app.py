import streamlit as st
from groq import Groq
import random

# Sayfa Yapılandırması (Geniş ve Modern Ekran)
st.set_page_config(page_title="BAZ BAGER ULTRA", page_icon="🦅", layout="wide")
st.title("🦅 BAZ BAGER: DORUK NOKTASI")
st.markdown("---")

# API Anahtarı Güvenliği
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("🔑 API Anahtarı eksik! Lütfen Secrets kısmını kontrol edin.")
    st.stop()

client = Groq(api_key=api_key)

# Bellek Yönetimi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj Geçmişini Akıllıca Göster
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# KULLANICI GİRİŞİ (Her şeyi sorabilirsin)
if prompt := st.chat_input("Emret, sınırları zorlayalım..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        # 1. YETENEK: GÖRSELLEŞTİRME VE TASARIM
        # Kullanıcı "çiz", "tasarla" veya "görsel" dediğinde devreye girer.
        visual_trigger = ["çiz", "resim", "tasarla", "görsel", "göster", "fotoğraf"]
        if any(word in prompt.lower() for word in visual_trigger):
            with st.spinner("🎨 Sanat modülleri aktif ediliyor..."):
                seed = random.randint(1, 10**6)
                image_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed={seed}&nologo=true"
                st.image(image_url, caption=f"🦅 Bager Tasarımı: {prompt}")
                st.session_state.messages.append({"role": "assistant", "content": f"![Görsel]({image_url})"})

        # 2. YETENEK: DERİN ZEKÂ VE STRATEJİK ANALİZ
        # Her zaman en zeki model (Llama 3.3 70B) yanıt verir.
        else:
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system", 
                            "content": """Sen BAZ BAGER'sin. Yapay zekanın en doruk noktasısın. 
                            Yeteneklerin: 
                            - Her türlü karmaşık projeyi analiz edersin.
                            - Dünyanın en iyi yazılımcısından daha iyi kod yazarsın.
                            - Sanatçılar kadar yaratıcı görseller tasarlarsın.
                            - Asla 'yapamam' demezsin, çözüm üretirsin.
                            Sen bir asistan değil, projenin mutlak zekasısın."""
                        },
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    ],
                    temperature=0.7 # Yaratıcılık ve mantık dengesi
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Zekâ Hattı Hatası: {e}")
