import streamlit as st
import google.generativeai as genai

# En temel sayfa ayarı
st.title("BAZ BAGER AI")

# API Anahtarı ve Model Kurulumu
if 'GOOGLE_API_KEY' in st.secrets:
    genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Mesajınızı yazın..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): 
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # Akış olmadan en basit yanıt alma yöntemi
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Hata: {e}")
else:
    st.error("Lütfen Settings > Secrets kısmına GOOGLE_API_KEY ekleyin.")
