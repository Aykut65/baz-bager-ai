import streamlit as st
import google.generativeai as genai

# --- PROFESYONEL AYARLAR ---
st.set_page_config(page_title="Baz Bager AI Pro", page_icon="🦅", layout="centered")

# Sayfa Tasarımı
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    h1 { text-align: center; color: #FF4B4B; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦅 BAZ BAGER AI: V3 TURBO")

# --- YAPAY ZEKA KİŞİLİĞİ (Sistem Talimatı) ---
SISTEM_TALIMATI = "Senin adın Baz Bager AI. Diyarbakır kökenli, çok zeki, samimi ve profesyonel bir yapay zekasın. Kullanıcılara yardımcı olurken hem bilgece hem de dostane bir dil kullanırsın."

if 'GOOGLE_API_KEY' in st.secrets:
    genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
    
    # Modeli sistem talimatıyla birlikte kuruyoruz (Hız ve Zeka artışı burada)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SISTEM_TALIMATI
    )
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mesajları Ekrana Yaz
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            if "image_url" in m: st.image(m["image_url"])
            else: st.markdown(m["content"])

    # Kullanıcı Girişi
    if prompt := st.chat_input("Bager emrinde, yaz dostum..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            if any(x in prompt.lower() for x in ["çiz", "resim", "görsel", "photo"]):
                # Gelişmiş Resim Motoru
                with st.spinner("Resminiz tuvale dökülüyor..."):
                    url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1024&height=1024&model=flux"
                    st.image(url)
                    st.session_state.messages.append({"role": "assistant", "content": "İşte istediğin görsel:", "image_url": url})
            else:
                # Akış (Streaming) ile Hızlı Cevap
                response_placeholder = st.empty()
                full_response = ""
                with st.spinner("Bager düşünüyor..."):
                    res = model.generate_content(prompt, stream=True)
                    for chunk in res:
                        full_response += chunk.text
                        response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    st.error("🔑 API Anahtarı bulunamadı!")
