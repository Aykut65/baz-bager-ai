import streamlit as st
import google.generativeai as genai

# --- PROFESYONEL TASARIM ---
st.set_page_config(page_title="Baz Bager AI", page_icon="🦅")
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🦅 BAZ BAGER AI PRO</h1>", unsafe_allow_html=True)

# --- ZEKA VE GÖRSEL KURULUMU ---
if 'GOOGLE_API_KEY' in st.secrets:
    genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            if m["content"].startswith("http"): st.image(m["content"])
            else: st.markdown(m["content"])

    if prompt := st.chat_input("Dostum, emret..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            if any(x in prompt.lower() for x in ["çiz", "resim", "görsel"]):
                # Görsel oluşturma
                url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1024&height=1024&nologo=true"
                st.image(url)
                st.session_state.messages.append({"role": "assistant", "content": url})
            else:
                # Zeki cevap üretme
                res = model.generate_content(prompt)
                st.markdown(res.text)
                st.session_state.messages.append({"role": "assistant", "content": res.text})
else:
    st.error("🔑 API Anahtarı eksik! Lütfen Streamlit panelinden Secrets kısmına ekle.")
