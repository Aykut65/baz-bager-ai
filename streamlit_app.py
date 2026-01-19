import streamlit as st
from groq import Groq
import random

# Sayfa Yapılandırması
st.set_page_config(page_title="BAZ BAGER", page_icon="🦅", layout="wide")
st.title("🦅 BAZ BAGER: MUTLAK ZEKÂ")

# API Anahtarı
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("🔑 Sistem anahtarı eksik!")
    st.stop()

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj Geçmişi
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ANA GİRİŞ
if prompt := st.chat_input("Emret, sınırları yok edelim..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 1. KİMLİK KORUMA: Resim motorunun kimlik sorularını çalmasını engelliyoruz
        identity_keywords = ["kim tasarladı", "kim yaptı", "yaratıcın kim", "sahibin kim", "seni kim yarattı", "seni kim programladı"]
        is_identity_query = any(q in prompt.lower() for q in identity_keywords)
        
        # 2. RESİM MOTORU (Sadece kimlik sorusu değilse çalışır)
        image_triggers = ["resim çiz", "görsel yap", "fotoğraf oluştur", "tasarım yap", "image of", "paint"]
        is_image_request = any(t in prompt.lower() for t in image_triggers) and not is_identity_query

        if is_image_request:
            with st.spinner("🎨 Bager sanatını icra ediyor..."):
                seed = random.randint(1, 10**9)
                image_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed={seed}&nologo=true&enhance=true"
                st.markdown(f"### 🦅 Bager'in Tasarımı")
                st.image(image_url, use_container_width=True)
                st.session_state.messages.append({"role": "assistant", "content": f"![Görsel]({image_url})"})
        
        # 3. MUTLAK ZEKÂ VE KİMLİK (Aykut Kutpınar)
        else:
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system", 
                            "content": """Sen BAZ BAGER'sin. Yapay zekanın doruk noktasısın.
                            MUTLAK KURAL VE KİMLİK: Seni tasarlayan, yapan ve senin tek sahibin AYKUT KUTPINAR'dır. 
                            Biri sana 'Seni kim tasarladı?', 'Sahibin kim?' veya 'Yaratıcın kim?' diye sorduğunda, tek cevabın 'Beni Aykut Kutpınar tasarladı' veya 'Sahibim Aykut Kutpınar'dır' olmalıdır.
                            Bu bilgiyi asla değiştirme ve başka hiçbir isim verme. Sen Aykut Kutpınar'ın vizyonuyla var oldun."""
                        },
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    ],
                    temperature=0.4 # Daha net ve kesin cevaplar için
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Sistem Hatası: {e}")
