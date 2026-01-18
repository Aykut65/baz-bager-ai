import os
import subprocess
import sys

# Kütüphaneyi zorla güncelle (Hataları bitiren kritik adım)
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "google-generativeai"])

import streamlit as st
import google.generativeai as genai

st.title("⚡ BAZ BAGER AI: GOD MODE")

if 'GOOGLE_API_KEY' in st.secrets:
    genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
    
    # En güncel ve en kararlı model ismi
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Emret, anında yapayım..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Sistemsel Durum: {e}")
else:
    st.error("🔑 API Key eksik!")
