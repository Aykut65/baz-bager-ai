import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="BAZ BAGER AI", page_icon="🦅")
st.title("🦅 BAZ BAGER: AKTİF")

# API Anahtarı ve Model Ayarı
if 'GOOGLE_API_KEY' in st.secrets:
    api_key = st.secrets['GOOGLE_API_KEY']
    genai.configure(api_key=api_key)
    
    # 404 hatasını bitiren temel yapılandırma
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("Emret Bager..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # En stabil yanıt alma yöntemi
                response = model.generate_content(prompt)
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("Sistem yoğun, lütfen 10 saniye sonra tekrar deneyin.")
                # Hatanın detayını sadece yönetici görecek şekilde konsola basar
                print(f"Hata Detayı: {e}") 
else:
    st.error("🔑 API Key 'Secrets' kısmına eklenmemiş!")
