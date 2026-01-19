import torch
from transformers import LlamaConfig, LlamaForCausalLM

# --- 1. DEVASA MİMARİNİN PLANLARI (Konfigürasyon) ---
# Buradaki sayılar, modelin "milyarlarca parametreye" ulaşmasını sağlayan ayarlardır.
# Bu konfigürasyon yaklaşık 7 Milyar (7B) parametreli bir modele denktir.
# 70B gibi daha büyükleri için bu sayıları 10 kat artırmak gerekir.

config = LlamaConfig(
    vocab_size=32000,     # Kelime dağarcığı boyutu (Bildiği kelime sayısı)
    hidden_size=4096,     # Nöron katmanlarının genişliği (Düşünce kapasitesi)
    intermediate_size=11008, # Ara katman genişliği (Karmaşık işlem kapasitesi)
    num_hidden_layers=32, # Derinlik (Kaç katmanlı bir beyin olduğu)
    num_attention_heads=32, # Dikkat mekanizması (Aynı anda kaç yere odaklanabildiği)
    max_position_embeddings=4096, # Bir seferde okuyabildiği maksimum metin uzunluğu
    rms_norm_eps=1e-6,    # Stabilizasyon ayarı
    initializer_range=0.02, # Başlangıç ağırlıkları
    use_cache=True,       # Hızlandırma önbelleği
    pad_token_id=0,
    bos_token_id=1,
    eos_token_id=2,
    tie_word_embeddings=False,
)

# --- 2. SİNİR AĞINI İNŞA ETME (Mimariyi Ayağa Kaldırma) ---
print("Devasa sinir ağı mimarisi inşa ediliyor... (Bu işlem RAM'i dolduracak)")

# Bu satır, yukarıdaki plana göre milyarlarca rastgele parametreyi (nöronu) oluşturur.
# Henüz eğitilmemiştir, yani şu anki haliyle sadece rastgele saçmalar.
model = LlamaForCausalLM(config)

# --- 3. MİMARİNİN BOYUTUNU HESAPLAMA ---
# Kaç milyar parametre olduğunu sayalım.
num_parameters = sum(p.numel() for p in model.parameters())
print(f"✅ MİMARİ TAMAMLANDI!")
print(f"🧠 Toplam Parametre Sayısı: {num_parameters:,} (Yaklaşık {num_parameters / 1e9:.2f} Milyar)")
print("-" * 50)
print("UYARI: Bu model şu an sadece rastgele sayılardan oluşuyor.")
print("Gemini gibi konuşabilmesi için trilyonlarca kelimelik veriyle aylarca eğitilmesi gerekiyor.")

# --- ÖRNEK BİR GİRİŞ (Eğer bilgisayar çökmezse çalışır) ---
# device = "cuda" if torch.cuda.is_available() else "cpu"
# model.to(device) # <- BU SATIR STANDART BİLGİSAYARI ÇÖKERTİR
# inputs = torch.randint(0, 32000, (1, 10)).to(device) # Rastgele bir giriş
# outputs = model(inputs)
# print("Model çıktısı (henüz eğitilmediği için anlamsız sayılar):", outputs.logits.shape)
