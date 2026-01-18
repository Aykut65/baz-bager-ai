import streamlit as st
import google.generativeai as genai

# Başlık ve Logo
st.set_page_config(page_title="BAZ BAGER AI", page_icon="🦅")
st.title("🦅 BAZ BAGER: AKTİF")

# API Kurulumu
if 'GOOGLE_API_KEY' in st.secrets:
    genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Emret Bager..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Sistem: API Anahtarı geçersiz veya kota doldu. Hata: {e}")
else:
    st.error("🔑 API Key 'Secrets' kısmına eklenmemiş!")
