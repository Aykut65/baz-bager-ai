import streamlit as st
from groq import Groq

# Sayfa Yapılandırması
st.set_page_config(page_title="BAZ BAGER AI", page_icon="🦅")
st.title("🦅 BAZ BAGER: LLAMA 3 GÜCÜ")

# Anahtar Kontrolü
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("🔑 Groq API Key bulunamadı! Secrets kısmını kontrol edin.")
    st.stop()

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Llama 3 motoru hazır, emret..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            # Meta Llama 3 modeliyle bağlantı
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Sistem Hatası: {e}")
