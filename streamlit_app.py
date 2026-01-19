import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="BAZ BAGER AI", page_icon="🦅")
st.title("🦅 BAZ BAGER: AKTİF")

# 1. API Anahtarını Al
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("🚨 API Anahtarı bulunamadı! Lütfen 'Secrets' ayarlarını kontrol et.")
    st.stop()

# 2. Google'a Bağlan (En güncel kütüphane ile)
try:
    genai.configure(api_key=api_key)
    # En hızlı ve kararlı model
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Bağlantı Hatası: {e}")
    st.stop()

# 3. Mesaj Geçmişini Göster
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 4. Kullanıcıdan Mesaj Al ve Cevapla
if prompt := st.chat_input("Emret..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            # Doğrudan cevap üret
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Cevap Üretilemedi: {e}")
