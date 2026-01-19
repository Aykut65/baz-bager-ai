import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="BAZ BAGER AI", page_icon="🦅")
st.title("🦅 BAZ BAGER: AKTİF")

# API Kurulumu
if 'GOOGLE_API_KEY' in st.secrets:
    genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
    
    # AKILLI MODEL SEÇİCİ (Hata Vermeyi İmkansız Kılar)
    def get_model():
        # Sırayla en iyi modelleri dener, hangisi çalışırsa onu seçer
        models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        for m in models_to_try:
            try:
                model = genai.GenerativeModel(m)
                # Test atışı
                model.generate_content("test")
                return model
            except:
                continue
        return None

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Emret Bager..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # Modeli dinamik olarak seç
                active_model = get_model()
                if active_model:
                    response = active_model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.error("Bağlantı kurulamadı. Lütfen 'Reboot App' yapın.")
            except Exception as e:
                st.error(f"Beklenmeyen bir durum: {e}")
else:
    st.error("🔑 API Anahtarı bulunamadı!")
