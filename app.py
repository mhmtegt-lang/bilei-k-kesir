import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

# --- AYARLAR ---
st.set_page_config(page_title="Kesir Modelleme", layout="wide")

# --- MANTIK KATMANI (Logic) ---
class FractionModel:
    def __init__(self, numerator, denominator):
        if denominator == 0:
            raise ValueError("Payda 0 olamaz.")
        self.numerator = int(numerator)
        self.denominator = int(denominator)

    @property
    def value(self):
        return self.numerator / self.denominator

    @property
    def mixed_parts(self):
        # Tam sayılı kesre çevirir: (Tam, Kalan Pay)
        return self.numerator // self.denominator, self.numerator % self.denominator

# --- GÖRSELLEŞTİRME KATMANI (Visualization) ---
def draw_fraction_visuals(model):
    # Grafik alanını oluştur
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), gridspec_kw={'height_ratios': [2, 1]})
    
    # --- 1. KUTU MODELİ (Üst Kısım) ---
    ax1.set_xlim(-0.5, max(model.value, 1) + 1.5)
    ax1.set_ylim(0, 3.5)
    ax1.axis('off')
    ax1.set_title("Kesir Modelleri", fontsize=14)

    # Renkler
    color_block = '#9b59b6' # Mor (Bileşik)
    color_whole = '#e056fd' # Pembe (Tam)

    # A) Bileşik Kesir Gösterimi (Yan yana kutular) - Üst Sıra
    ax1.text(-0.5, 2.5, "Bileşik:", fontsize=12, fontweight='bold')
    for i in range(model.numerator):
        rect = patches.Rectangle(
            (i * (1/model.denominator), 2.1), 
            1/model.denominator, 0.8, 
            linewidth=1, edgecolor='white', facecolor=color_block
        )
        ax1.add_patch(rect)
        ax1.text((i + 0.5) * (1/model.denominator), 2.5, f"1/{model.denominator}", 
                 ha='center', va='center', color='white', fontsize=9)

    # B) Tam Sayılı Kesir Gösterimi (Tam Bloklar + Kalan) - Alt Sıra
    ax1.text(-0.5, 0.9, "Tam Sayılı:", fontsize=12, fontweight='bold')
    whole, remainder = model.mixed_parts
    current_x = 0
    
    # Tam kısımlar
    for w in range(whole):
        rect = patches.Rectangle((current_x, 0.5), 1, 0.8, linewidth=1, edgecolor='white', facecolor=color_whole)
        ax1.add_patch(rect)
        ax1.text(current_x + 0.5, 0.9, "1 TAM", ha='center', va='center', color='white', fontsize=10)
        current_x += 1
        
    # Kalan kısımlar
    for r in range(remainder):
        rect = patches.Rectangle(
            (current_x + r * (1/model.denominator), 0.5), 
            1/model.denominator, 0.8, 
            linewidth=1, edgecolor='white', facecolor=color_block
        )
        ax1.add_patch(rect)
        ax1.text(current_x + (r + 0.5) * (1/model.denominator), 0.9, f"1/{model.denominator}", 
                 ha='center', va='center', color='white', fontsize=9)

    # --- 2. SAYI DOĞRUSU (Alt Kısım) ---
    limit = math.ceil(max(model.value, 2)) + 1
    ax2.set_xlim(-0.5, limit)
    ax2.set_ylim(-1, 1)
    ax2.axis('off')
    
    # Ana çizgi
    ax2.axhline(y=0, color='#2980b9', linewidth=2)
    
    # İşaretler
    for i in range(limit + 1):
        ax2.plot(i, 0, 'o', color='#2980b9') # Tam sayılar
        ax2.text(i, -0.4, str(i), ha='center', fontsize=12)
        
        # Ara parçalar
        if i < limit:
            for j in range(1, model.denominator):
                ax2.plot(i + j/model.denominator, 0, '|', color='gray', markersize=5)

    # Konum İşaretleme
    ax2.plot(model.value, 0, 'o', color='#e74c3c', markersize=12) # Kırmızı nokta
    ax2.annotate(f"{model.numerator}/{model.denominator}", 
                 xy=(model.value, 0.1), xytext=(model.value, 0.7),
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 ha='center', fontsize=12, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", fc="#e056fd", alpha=0.3))

    plt.tight_layout()
    return fig

# --- ARAYÜZ (UI) ---
def main():
    st.title("🧩 Matematik Atölyesi: Kesirler")
    
    with st.sidebar:
        st.header("Ayarlar")
        pay = st.number_input("Pay", min_value=1, value=4, step=1)
        payda = st.number_input("Payda", min_value=1, value=3, step=1)

    try:
        model = FractionModel(pay, payda)
        
        # Grafik Çizimi
        fig = draw_fraction_visuals(model)
        st.pyplot(fig)
        
        # Alt Bilgi ve Soru
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Gösterilen Kesir:** {pay}/{payda}")
            
        with col2:
            tam, kalan = model.mixed_parts
            st.success(f"**Tam Sayılı Hali:** {tam} Tam {kalan}/{payda}")

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    main()
