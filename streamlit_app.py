import streamlit as st
import sys
import subprocess
import time

st.set_page_config(page_title="BAZ BAGER: KURTARMA", page_icon="🦅")
st.title("🦅 BAZ BAGER: ACİL DURUM MODU")

# 1. TEŞHİS VE ZORLA GÜNCELLEME (Bunu yapmak zorundayız)
try:
    import google.generativeai as genai
    # Sürümü ekrana yazdıralım ki ne olduğunu görelim
    mevcut_surum = genai.__version__
except ImportError:
    mevcut_surum = "Yok"

# Eğer sürüm eskiyse veya Flash modelini desteklemiyorsa ZORLA GÜNCELLE
if mevcut_surum == "Yok" or mevcut_surum < "0.8.3":
    st.warning(f"⚠️ Eski sürüm tespit edildi: {mevcut_surum}. Sistem kendini güncelliyor...")
    try:
        # Arka planda terminal komutu çalıştırarak günceliyoruz
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "google-generativeai"])
        import google.generativeai as genai
        import importlib
        importlib.reload(genai) # Kütüphaneyi yeniden yükle
        st.success(f"✅ Güncelleme Başarılı! Yeni Sürüm: {genai.__version__}")
        st.experimental_rerun() # Sayfayı yenile
    except Exception as e:
        st.error(f"Güncelleme yapılamadı: {e}")

# 2. BAĞLANTIYI KUR (Hata verirse durma, alternatif modele geç)
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("🚨 API Anahtarı bulunamadı! Lütfen Secrets ayarlarını kontrol et.")
    st.stop()

genai.configure(api_key=api_key)

# 3. MODEL SEÇİMİ (Asla hata vermeyecek sıralama)
# Önce Flash'ı dener, olmazsa Pro'yu dener.
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    st.success("🟢 Sistem: Gemini 1.5 Flash (En Hızlı)")
except:
    try:
        model = genai.GenerativeModel('gemini-pro')
        st.warning("🟠 Sistem: Gemini Pro (Yedek Hat)")
    except:
        st.error("🔴 Hiçbir model çalıştırılamadı. API Anahtarında sorun olabilir.")
        st.stop()

# 4. SOHBET EKRANI
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Lütfen bir test mesajı yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Beklenmeyen bir hata oluştu: {e}")
