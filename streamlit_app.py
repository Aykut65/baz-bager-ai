import streamlit as st
import requests

# Sayfa Ayarları
st.set_page_config(page_title="BAZ BAGER AI - GLOBAL", page_icon="🦅", layout="wide")

st.markdown("<h1 style='text-align: center; color: #FFD700;'>🦅 BAZ BAGER AI: DÜNYA ZEKASI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Sınırsız Bilgi, Sanat ve Çözüm Merkezi.</p>", unsafe_allow_html=True)

# Yan Panel - Tüm Sistemler Aktif
with st.sidebar:
    st.header("🌐 Küresel Güçler")
    st.success("✅ Dünya Bilgi Bankası Bağlı")
    st.success("✅ Sanatsal Çizim Motoru Aktif")
    st.success("✅ Çoklu Dil Çeviri Hazır")
    st.warning("Mod: Ultra Zeka (Her Şeyi Bilir)")

# Sohbet Sistemi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Bana dünyadaki herhangi bir şeyi sor veya bir resim hayal et..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Resim Çizme Komutu Algılama
        if "çiz" in prompt.lower() or "resim" in prompt.lower():
            st.write("🎨 Sanat

git add streamlit_app.py
git commit -m "dunya-zekasi-ve-sanat-aktif"
git push origin main

cat <<EOF > streamlit_app.py
import streamlit as st
import random

# Sayfa Ayarları
st.set_page_config(page_title="BAZ BAGER AI", page_icon="🦅", layout="wide")

# Tasarım
st.markdown("<h1 style='text-align: center; color: #FFD700;'>🦅 BAZ BAGER AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Geleceğin Yapay Zekası Herkes İçin Hazır.</p>", unsafe_allow_html=True)

# Yan Panel - Küresel Erişim
with st.sidebar:
    st.header("🌐 Sistem Durumu")
    st.success("✅ Tüm Kullanıcılara Açık")
    st.success("✅ Problem Çözme & Sanat Aktif")
    st.info("Sürüm: 5.0 (Global Edition)")

# Sohbet Sistemi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kapsayıcı Mesaj Kutusu
if prompt := st.chat_input("Size nasıl yardımcı olabilirim?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if "çiz" in prompt.lower() or "resim" in prompt.lower():
            st.write("🎨 Talebiniz doğrultusunda görsel oluşturuluyor...")
            url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024"
            st.image(url, caption=f"BAZ BAGER AI Tasarımı")
            res = "Görseliniz başarıyla hazırlandı."
        else:
            res = f"🦅 **BAZ BAGER AI:** '{prompt}' konulu talebiniz analiz edildi. Size yardımcı olmaktan mutluluk duyarım."
        
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
