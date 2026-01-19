import streamlit as st
import requests
import json

# Sayfa Yapılandırması
st.set_page_config(page_title="BAZ BAGER AI", page_icon="🦅")
st.title("🦅 BAZ BAGER: AKTİF")

# API Anahtarı
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("🔑 API Key bulunamadı!")
    st.stop()

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Kullanıcı Girişi
if prompt := st.chat_input("Emret, şimdi cevap verecek..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        # 404 HATASINI BİTİREN GARANTİ ADRES (TAM YOL)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        headers = {'Content-Type': 'application/json'}
        # Google'ın beklediği en sade veri yapısı
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            }
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            result = response.json()
            
            # Yanıtı ekrana bas
            if "candidates" in result:
                answer = result["candidates"][0]["content"]["parts"][0]["text"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            elif "error" in result:
                # Hata gelirse 'gemini-pro'ya otomatik geçiş (A Planı tutmazsa B Planı)
                st.info("Sistem güncelleniyor, yedek hat devreye giriyor...")
                alt_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
                alt_response = requests.post(alt_url, headers=headers, data=json.dumps(payload))
                alt_result = alt_response.json()
                
                if "candidates" in alt_result:
                    alt_answer = alt_result["candidates"][0]["content"]["parts"][0]["text"]
                    st.markdown(alt_answer)
                    st.session_state.messages.append({"role": "assistant", "content": alt_answer})
                else:
                    st.error(f"Google yanıt vermiyor. Hata kodu: {result['error']['code']}")
        except Exception as e:
            st.error(f"Bağlantı kesildi: {e}")
