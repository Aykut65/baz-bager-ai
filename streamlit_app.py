import streamlit as st
from groq import Groq

# Sayfa Yapılandırması
st.set_page_config(page_title="BAZ BAGER: PROJE", page_icon="🦅", layout="wide")
st.title("🦅 BAZ BAGER: PROJE ORTAĞI")
st.markdown("---")

# API Anahtarı
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("🔑 API Anahtarı bulunamadı!")
    st.stop()

client = Groq(api_key=api_key)

# Hafıza Yönetimi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj Geçmişini Göster
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# PROJE GİRİŞİ
if prompt := st.chat_input("Proje detaylarını buraya yaz, analiz edelim..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            # Dünyanın en iyi mantık yürüten modeli: Llama 3.3 70B
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": "Sen BAZ BAGER'sin. Bir proje ortağısın. Resim çizmek gibi yan işlerle uğraşmazsın. Görevin, sana verilen proje detaylarını en üst seviye mantık ve bilgiyle analiz etmektir."
                    },
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                temperature=0.4 # Daha ciddi ve profesyonel cevaplar için
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Sistem Hatası: {e}")
