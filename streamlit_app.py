import streamlit as st
import requests
import json

st.set_page_config(page_title="BAZ BAGER", page_icon="🦅")
st.title("🦅 BAZ BAGER: SON DENEME")

api_key = st.secrets.get("GOOGLE_API_KEY")

if prompt := st.chat_input("Buraya bir kelime yaz..."):
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        # MODEL İSMİNİ EN ESKİ VE EN KARARLI HALİNE ÇEKTİM (v1beta/models/gemini-pro)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            response = requests.post(url, json=payload)
            result = response.json()
            # Yanıtı doğrudan yazdır, hata yakalamayı bile en aza indir
            answer = result["candidates"][0]["content"]["parts"][0]["text"]
            st.markdown(answer)
        except Exception as e:
            st.error(f"Google yanıt vermiyor: {result if 'result' in locals() else e}")
