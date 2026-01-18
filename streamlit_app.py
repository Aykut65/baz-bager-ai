import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="BAZ BAGER AI", page_icon="🦅", layout="centered")

# Tasarım ve Başlık
st.markdown("<h1 style='text-align: center; color: #FFD700;'>🦅 BAZ BAGER AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Her şeyi yapabilen kişisel asistanın emrinde.</p>", unsafe_allow_html=True)

# Sohbet Geçmişi Başlatma
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski Mesajları Göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan Girdi Al
if prompt := st.chat_input("Emret Aykut, ne yapmamı istersin?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yapay Zeka Cevabı (Buraya zeka eklendi)
    with st.chat_message("assistant"):
        response = f"BAZ BAGER AI Emrinde! '{prompt}' dedin. Şimdilik seni duyabiliyorum, yakında tüm dünyayı senin için tarayacağım!"
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Yan Panel (Özellikler)
with st.sidebar:
    st.header("🦅 Asistan Menüsü")
    st.button("Hafızayı Temizle")
    st.write("Versiyon: 2.0 (Ultra Zeka)")
