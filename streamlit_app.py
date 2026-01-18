import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları (Başlığı geri getirir)
st.set_page_config(page_title="BAZ BAGER AI: GOD MODE", page_icon="⚡", layout="wide")
st.markdown("<h1 style='text-align: center;'>⚡ BAZ BAGER AI: GOD MODE</h1>", unsafe_allow_config=True)

# API Anahtarı Yapılandırması
if 'GOOGLE_API_KEY' in st.secrets:
    genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
    
    # 404 HATASINI ÇÖZEN KESİN FORMAT
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Sınırsız güç emrinde..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_text = ""
            try:
                # Yanıt Akışı
                response = model.generate_content(prompt, stream=True)
                for chunk in response:
                    if chunk.text:
                        full_text += chunk.text
                        placeholder.markdown(full_text + "▌")
                st.session_state.messages.append({"role": "assistant", "content": full_text})
            except Exception as e:
                st.error(f"Sistemsel Hata: {e}")
else:
    st.error("🔑 API Key bulunamadı! Lütfen Settings > Secrets kısmını kontrol et.")
