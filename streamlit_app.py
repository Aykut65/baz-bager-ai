import streamlit as st
import google.generativeai as genai

# Sayfa Başlığı
st.title("⚡ BAZ BAGER AI: GOD MODE")

# API Ayarları
if 'GOOGLE_API_KEY' in st.secrets:
    genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
    
    # 404 HATASINI BİTİREN SATIR
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Emret, anında yapayım..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # En kararlı yanıt alma yöntemi
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Sistemsel Durum: {e}")
else:
    st.error("🔑 API Key eksik! Settings > Secrets kısmını kontrol et.")
