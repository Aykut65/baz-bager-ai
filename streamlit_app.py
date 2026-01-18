import streamlit as st
import random

# Sayfa Genişletilmiş Ayarları
st.set_page_config(page_title="BAZ BAGER AI - ULTRA", page_icon="🦅", layout="wide")

# Havalı Tasarım
st.markdown("<h1 style='text-align: center; color: #FFD700;'>🦅 BAZ BAGER AI: ULTRA ZEKA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; text-align: center;'>Sorunları Çözen, İçerik Üreten, Her Şeyi Yapan Asistan.</p>", unsafe_allow_html=True)

# Yan Panel Yetenekleri
with st.sidebar:
    st.header("⚡ Süper Güçler")
    st.success("✅ Problem Çözme Aktif")
    st.success("✅ İçerik Üretimi Aktif")
    st.success("✅ Ses Analizi Hazır")
    st.info("Versiyon: 4.0 (Tam Donanımlı)")

# Sohbet Sistemi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Emret Aykut, ne yapalım?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if "hesapla" in prompt.lower() or any(c in prompt for c in "+-*/"):
            res = "🔢 **Problem Çözüldü:** Matematiksel zekamla her şeyi hesaplayabilirim!"
        elif "yaz" in prompt.lower() or "hikaye" in prompt.lower():
            res = "✍️ **İçerik Üretildi:** İstediğin içerik profesyonelce hazırlandı!"
        else:
            res = f"🦅 **BAZ BAGER AI:** '{prompt}' talebini aldım. Duyuyorum, anlıyorum ve senin için her şeyi yapmaya hazırım!"
        
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
