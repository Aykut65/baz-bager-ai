import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="BAZ BAGER AI PRO", page_icon="⚡", layout="centered")

# Görünüm
st.markdown("<style>h1 {text-align: center; color: #00ffcc;}</style>", unsafe_allow_html=True)
st.title("⚡ BAZ BAGER AI PRO")

if 'GOOGLE_API_KEY' in st.secrets:
    genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
    
    # Daha stabil bir yapılandırma
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            if "image_url" in m: st.image(m["image_url"])
            else: st.markdown(m["content"])

    if prompt := st.chat_input("Bager emrinde..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            if any(word in prompt.lower() for word in ["çiz", "resim", "görsel"]):
                img_url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024&seed=42"
                st.image(img_url)
                st.session_state.messages.append({"role": "assistant", "content": "Görsel hazır.", "image_url": img_url})
            else:
                # En hızlı yanıt yöntemi
                response_placeholder = st.empty()
                full_res = ""
                # Hata ihtimaline karşı try-except bloğu
                try:
                    result = model.generate_content(prompt, stream=True)
                    for chunk in result:
                        full_res += chunk.text
                        response_placeholder.markdown(full_res + "▌")
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                except Exception as e:
                    st.error(f"Bir hata oluştu: {e}")
else:
    st.error("API Anahtarı bulunamadı!")
