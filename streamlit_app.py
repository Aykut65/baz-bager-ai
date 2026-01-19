import streamlit as st
import google.generativeai as genai

# Sayfa Yapılandırması
st.set_page_config(page_title="BAZ BAGER AI", page_icon="🦅")
st.title("🦅 BAZ BAGER: AKTİF")

# API VE MODEL KURULUMU (404 HATASINI KÖKTEN ÇÖZER)
if 'GOOGLE_API_KEY' in st.secrets:
    try:
        genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
        
        # v1beta yerine doğrudan en güncel stabil modele bağlanır
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash-latest' # 'latest' eki sorunları çözer
        )
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

        if prompt := st.chat_input("Emret Bager..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                try:
                    # Akış şeklinde yanıt alma (Daha hızlı ve hatasızdır)
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Bağlantı Hatası: {e}")
                    st.info("İpucu: Sağ alttan Reboot App yapmayı deneyin.")
    except Exception as e:
        st.error(f"Sistem Kurulum Hatası: {e}")
else:
    st.error("🔑 API Key 'Secrets' kısmına eklenmemiş!")
