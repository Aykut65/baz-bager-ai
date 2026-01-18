import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="BAZ BAGER AI", layout="wide")

if 'GOOGLE_API_KEY' in st.secrets:
    genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
    
    # 404 hatasını çözen model tanımlaması
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Emret, anında yapayım..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_text = ""
            try:
                # Işık hızında yanıt (Streaming)
                response = model.generate_content(prompt, stream=True)
                for chunk in response:
                    full_text += chunk.text
                    placeholder.markdown(full_text + "▌")
                st.session_state.messages.append({"role": "assistant", "content": full_text})
            except Exception as e:
                st.error(f"Hata: {e}")
