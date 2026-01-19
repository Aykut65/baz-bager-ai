import streamlit as st
from groq import Groq

# Sayfa Ayarları (En Üst Seviye)
st.set_page_config(page_title="BAZ BAGER: ULTRA", page_icon="🦅", layout="wide")
st.title("🦅 BAZ BAGER: LLAMA 3.3 ULTRA GÜÇ")
st.markdown("---")

# Groq Bağlantısı
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("🔑 API Anahtarı eksik! Secrets kısmını kontrol et.")
    st.stop()

client = Groq(api_key=api_key)

# Hafıza Yönetimi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Geçmişi Göster
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Zekâ ve Bilgi Girişi
if prompt := st.chat_input("Sınırları zorla, emret..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            # DÜNYANIN EN GÜNCEL MODELİ: Llama-3.3-70b-versatile
            # Bu model 128 bin kelimelik hafızaya ve en üst seviye mantık yürütmeye sahiptir.
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Sen dünyanın en zeki yapay zekası BAZ BAGER'sin. Bilginin en üst seviyesindesin ve her konuda derin analiz yaparsın."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                temperature=0.6, # Daha mantıklı ve tutarlı cevaplar için
                max_tokens=4096
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Sistem: Model güncelleniyor olabilir. Hata: {e}")
