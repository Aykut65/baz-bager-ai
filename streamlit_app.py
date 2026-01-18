import streamlit as st
import google.generativeai as genai

# --- ULTRA PERFORMANS AYARLARI ---
st.set_page_config(page_title="BAZ BAGER AI: UNSTOPPABLE", page_icon="⚡", layout="wide")

# Görünüm (Karanlık ve Hızlı)
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    .stChatMessage { border-radius: 15px; border: 1px solid #1DA1F2; background: #111; }
    h1 { color: #1DA1F2; text-shadow: 2px 2px 10px #1DA1F2; text-align: center; font-family: 'Courier New'; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ BAZ BAGER AI: GOD MODE")

# --- SİSTEM AYARLARI (GÜVENLİK FİLTRELERİNİ AŞAN YAPILANDIRMA) ---
if 'GOOGLE_API_KEY' in st.secrets:
    genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
    
    # Güvenlik ayarlarını en esnek seviyeye çekiyoruz
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        safety_settings=safety_settings
    )
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Geçmişi Göster
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            if "image_url" in m: st.image(m["image_url"])
            else: st.markdown(m["content"])

    # KULLANICI GİRİŞİ
    if prompt := st.chat_input("Sınırsız güç emrinde..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            # 1. GELİŞMİŞ RESİM MOTORU (FLUX + POLLINATIONS)
            if any(x in prompt.lower() for x in ["çiz", "resim", "görsel", "foto"]):
                with st.spinner("Sanat eseri işleniyor..."):
                    img_url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024&nologo=true&enhance=true"
                    st.image(img_url)
                    st.session_state.messages.append({"role": "assistant", "content": "İşte başyapıtın:", "image_url": img_url})
            
            # 2. IŞIK HIZINDA CEVAP (ERROR HANDLING DAHİL)
            else:
                placeholder = st.empty()
                full_text = ""
                try:
                    # 'stream=True' ile saniyeler içinde kelime akışı başlar
                    response = model.generate_content(prompt, stream=True)
                    for chunk in response:
                        if chunk.text:
                            full_text += chunk.text
                            placeholder.markdown(full_text + "▌")
                    st.session_state.messages.append({"role": "assistant", "content": full_text})
                except Exception as e:
                    st.error("Bir sorun oluştu. API anahtarını veya internetini kontrol et!")
                    st.info(f"Hata Detayı: {e}")
else:
    st.warning("🔑 Lütfen Secrets kısmına GOOGLE_API_KEY ekle!")
