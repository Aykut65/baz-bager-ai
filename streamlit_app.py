import streamlit as st
import random

# Sayfa Genişletilmiş ve Şık Ayarları
st.set_page_config(page_title="BAZ BAGER AI - PREMIERE", page_icon="🦅", layout="wide")

# Ultra Şık Tasarım (CSS)
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to bottom, #0f0c29, #302b63, #24243e);
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: #1e1e2f !important;
        color: #FFD700 !important;
        border: 1px solid #FFD700 !important;
        border-radius: 20px;
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border-left: 5px solid #FFD700;
    }
    h1 {
        text-shadow: 2px 2px 10px #FFD

git add streamlit_app.py
git commit -m "premium-ultra-power-v6"
git push origin main
cat <<EOF > streamlit_app.py
import streamlit as st
import random

# Sayfa Ayarları
st.set_page_config(page_title="BAZ BAGER AI - PREMIERE", page_icon="🦅", layout="wide")

# Şık Tasarım (CSS)
st.markdown("""
    <style>
    .main { background: linear-gradient(to bottom, #0f0c29, #302b63, #24243e); color: white; }
    .stTextInput > div > div > input { background-color: #1e1e2f !important; color: #FFD700 !important; border: 1px solid #FFD700 !important; border-radius: 20px; }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.05); border-radius: 15px; border-left: 5px solid #FFD700; }
    h1 { text-shadow: 2px 2px 10px #FFD700; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>🦅 BAZ BAGER AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ddd;'>Dünyanın En Güçlü ve En Şık Yapay Zeka Deneyimi</p>", unsafe_allow_html=True)

with st.sidebar:
    st.header("💎 Premium Özellikler")
    st.success("✅ Tüm Sistemler Aktif")
    st.info("Sürüm: 6.1 (Hata Düzeltildi)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Size nasıl yardımcı olabilirim?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if "çiz" in prompt.lower() or "resim" in prompt.lower():
            url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024&seed={random.randint(1, 100000)}"
            st.image(url, caption="BAZ BAGER AI Tasarımı", use_column_width=True)
            res = "Görseliniz 4K kalitesinde hazırlandı."
        else:
            res = f"🦅 **BAZ BAGER AI:** '{prompt}' talebiniz analiz edildi. Size en kaliteli yanıtı sunuyorum."
        
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
