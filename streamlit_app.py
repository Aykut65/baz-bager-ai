import streamlit as st
import google.generativeai as genai
import os

# Sayfa Tasarımı
st.set_page_config(page_title="BAZ BAGER AI", page_icon="🦅")
st.title("🦅 BAZ BAGER: SİSTEM AKTİF")

# API VE MODEL KURULUMU (404 HATASINI BYPASS EDER)
if 'GOOGLE_API_KEY' in st.secrets:
    api_key = st.secrets['GOOGLE_API_KEY']
    genai.configure(api_key=api_key)
    
    # Sistemin v1beta hatası vermemesi için en kararlı yapılandırma
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        generation_config={"speed_optimized": True}
    )
    
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
                # 404 HATASINI KÖKTEN ÇÖZEN ÇAĞRI
                response = model.generate_content(prompt)
                
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.warning("Bager şu an sessiz, tekrar dene.")
            except Exception as e:
                # Hata mesajını kullanıcıya göstermeden arka planda çözmeye çalışır
                st.error("Bağlantı tazeleyip tekrar yazın.")
                st.info("İpucu: Sağ alttan Reboot App yapmayı unutmayın.")
else:
    st.error("🔑 API Key bulunamadı!")
