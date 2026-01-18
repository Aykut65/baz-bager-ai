import streamlit as st
import google.generativeai as genai

# Sayfa Yapılandırması
st.set_page_config(page_title="BAZ BAGER AI: FINAL", page_icon="⚡", layout="wide")

# API Anahtarı Kontrolü
if 'GOOGLE_API_KEY' in st.secrets:
    genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
    
    # 404 Hatasını Çözen Yeni Model Tanımlaması
    # Google'ın en güncel isimlendirme formatı kullanıldı
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mesaj Geçmişini Görüntüle
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # Kullanıcı Girişi ve Yanıt Döngüsü
    if prompt := st.chat_input("Emret, anında yapayım..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            try:
                # Işık hızında yanıt (Streaming)
                response = model.generate_content(prompt, stream=True)
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        placeholder.markdown(full_response + "▌")
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                # Hata durumunda detaylı rapor sunar
                st.error(f"Sistemsel bir sorun oluştu: {e}")
else:
    st.error("🔑 API Key eksik! Secrets kısmına GOOGLE_API_KEY ekle.")
