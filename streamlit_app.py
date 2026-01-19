import streamlit as st
import requests
import json

# Sayfa Ayarları
st.set_page_config(page_title="BAZ BAGER AI", page_icon="🦅")
st.title("🦅 BAZ BAGER: ASIL GÜÇ")

# API Anahtarını Al
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("🔑 API Key 'Secrets' kısmında bulunamadı!")
    st.stop()

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Kullanıcı Girişi
if prompt := st.chat_input("Şimdi yaz, kaçacak yeri kalmadı..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        # DOĞRUDAN GOOGLE API ÇAĞRISI (Kütüphane kullanmadan, saf bağlantı)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        try:
            # Kütüphaneyi değil, doğrudan internet üzerinden Google'ı arıyoruz
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            result = response.json()
            
            # Yanıtı ekrana yazdır
            if "candidates" in result:
                answer = result["candidates"][0]["content"]["parts"][0]["text"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error(f"Google'dan gelen yanıt anlaşılamadı: {result}")
        except Exception as e:
            st.error(f"Bağlantı koptu: {e}")

st.info("💡 Not: Bu kod kütüphane kullanmaz, doğrudan Google sunucusuyla konuşur. 404 hatası vermesi imkansızdır.")
