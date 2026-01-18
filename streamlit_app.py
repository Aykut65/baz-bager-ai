import streamlit as st
import google.generativeai as genai

# Sayfa Yapılandırması (Görsel 75'teki başlığı korur)
st.set_page_config(page_title="BAZ BAGER AI", layout="wide")
st.title("⚡ BAZ BAGER AI: AKTİF")

# API Anahtarı Kontrolü
if 'GOOGLE_API_KEY' in st.secrets:
    genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
    
    # EN GÜNCEL VE HATASIZ MODEL TANIMLAMASI
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        model = genai.GenerativeModel('gemini-pro')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mesaj Geçmişini Görüntüle
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # Kullanıcı Girişi
    if prompt := st.chat_input("Emret Bager..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # En hızlı ve kararlı yanıt yöntemi
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Sistemsel Hata: {e}")
else:
    st.error("🔑 API Key bulunamadı! Lütfen Settings > Secrets kısmını kontrol et.")
