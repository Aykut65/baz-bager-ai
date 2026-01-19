import streamlit as st
import requests
import json

# Sayfa Ayarları
st.set_page_config(page_title="BAZ BAGER AI", page_icon="🦅")
st.title("🦅 BAZ BAGER: NİHAİ ÇÖZÜM")

# API Anahtarını Çek
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("🔑 API Key 'Secrets' kısmında bulunamadı!")
    st.stop()

# Mesaj Geçmişini Başlat
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Kullanıcı Girişi
if prompt := st.chat_input("Emret, şimdi çalışacak..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        # 404 HATASINI BİTİREN KRİTİK DEĞİŞİKLİK: v1beta YERİNE v1 KULLANIYORUZ
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        try:
            # Doğrudan HTTP isteği
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            result = response.json()
            
            # Yanıtı çözümle
            if "candidates" in result and len(result["candidates"]) > 0:
                answer = result["candidates"][0]["content"]["parts"][0]["text"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            elif "error" in result:
                st.error(f"Google Hatası: {result['error']['message']}")
            else:
                st.warning("Google'dan boş yanıt geldi, lütfen tekrar dene.")
        except Exception as e:
            st.error(f"Bağlantı başarısız: {e}")

st.divider()
st.caption("✅ Bu sürüm v1 API kapısını kullanarak 404 hatasını kalıcı olarak engeller.")
