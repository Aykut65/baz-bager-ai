import os
import subprocess
import sys

# SUNUCUYU GÜNCELLEMEYE ZORLA (404 HATASININ TEK ÇÖZÜMÜ)
try:
    import google.generativeai as genai
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai"])
    import google.generativeai as genai

import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="BAZ BAGER AI", layout="wide")
st.title("🦅 BAZ BAGER: SİSTEM AKTİF")

# API Anahtarı Kontrolü
if 'GOOGLE_API_KEY' in st.secrets:
    genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
    
    # DÜNYADAKİ HER SÜRÜMDE ÇALIŞAN EN GARANTİ MODEL
    model = genai.GenerativeModel('gemini-pro')
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Bager emirlerini bekliyor..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # En stabil ve en eski yöntem (Error 404'ü bypass eder)
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Sistem: {e}")
else:
    st.error("🔑 API Key bulunamadı! Lütfen Secrets kısmını kontrol et.")
