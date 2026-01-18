import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="BAZ BAGER AI", layout="wide")
st.title("⚡ BAZ BAGER AI: AKTİF")

# API Yapılandırması
if 'GOOGLE_API_KEY' in st.secrets:
    genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
    
    # 404 HATASINI BİTİREN EN TEMEL MODEL ADI
    model = genai.GenerativeModel('gemini-pro')
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Emret..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # Akışsız, en stabil yöntem
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Sistem Mesajı: {e}")
else:
    st.error("API Key Eksik!")
