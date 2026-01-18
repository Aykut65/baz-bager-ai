import streamlit as st
import random

st.set_page_config(page_title="BAZ BAGER AI", page_icon="🦅")
st.title("🦅 BAZ BAGER AI: GLOBAL")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if p := st.chat_input("Mesajınızı buraya yazın..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.markdown(p)

    with st.chat_message("assistant"):
        if "çiz" in p.lower() or "resim" in p.lower():
            url = f"https://pollinations.ai/p/{p.replace(' ', '_')}?width=1024&height=1024&seed={random.randint(1, 999)}"
            st.image(url, caption="BAZ BAGER AI")
            res = "Görseliniz başarıyla oluşturuldu."
        else:
            res = "🦅 Talebiniz işlendi."
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
