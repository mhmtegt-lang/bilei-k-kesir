import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="İnteraktif Kesir Duvarı",
    layout="centered"
)

# --- SESSION STATE (DURUM YÖNETİMİ) ---
# Kullanıcının eklediği parça sayısını hafızada tutuyoruz.
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'denominator' not in st.session_state:
    st.session_state.denominator = 3  # Varsayılan 1/3

# --- FONKSİYONLAR ---

def reset_game():
    """Oyunu sıfırlar."""
    st.session_state.count = 0

def add_piece():
    """Bir parça ekler."""
    st.session_state.count += 1

def remove_piece():
    """Bir parça çıkarır."""
    if st.session_state.count > 0:
        st.session_state.count -= 1

def draw_interactive_wall(numerator, denominator):
    """
    Matplotlib ile dinamik çizim yapar.
    Üstte: Doldurulacak '1 Tam' kutusu (Outline).
    İçinde: Eklenen parçalar.
    """
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Koordinat sistemi ayarları
    ax.set_xlim(0, 1.2)
    ax.set_ylim(0, 1.5)
    ax.axis('off') # Eksenleri gizle

    # --- 1. HEDEF KUTUSU (1 TAM) ---
    # Bu kutu şeffaf ve kenarlıklı olacak, dolmayı bekleyen kap gibi.
    rect_whole = patches.Rectangle(
        (0.1, 0.5), 1.0, 0.6, 
        linewidth=3, edgecolor='#2c3e50', facecolor='none', linestyle='--'
    )
    ax.add_patch(rect_whole)
    ax.text(0.6, 1.2, "1 TAM (Bütün)", ha='center', fontsize=14, fontweight='bold', color='#2c3e50')

    # --- 2. PARÇALARI ÇİZME (ANIMASYON HİSSİ) ---
    # Kullanıcının eklediği sayı kadar parça çizeriz.
    colors = {2: '#e056fd', 3: '#9b59b6', 4: '#3498db', 5: '#1abc9c', 6: '#2ecc71'}
    piece_color = colors.get(denominator, '#95a5a6')
    
    width = 1.0 / denominator
    
    for i in range(numerator):
        # Eğer parça sayısı paydayı geçerse (Bileşik kesir), kutudan taşar.
        # Görsel olarak 1 tam kutusunun (x=0.1) içine yerleştiriyoruz.
        x_pos = 0.1 + (i * width)
        
        rect_part = patches.Rectangle(
            (x_pos, 0.5), width, 0.6,
            linewidth=1, edgecolor='white', facecolor=piece_color
        )
        ax.add_patch(rect_part)
        
        # Parçanın içine yazıyı ortala
        ax.text(x_pos + width/2, 0.8, f"1/{denominator}", 
                ha='center', va='center', color='white', fontsize=12, fontweight='bold')

    return fig

# --- ARAYÜZ (UI) ---
def main():
    st.title("🧩 Kesirleri Birleştirme Oyunu")
    st.markdown("Aşağıdaki butonları kullanarak **Birim Kesirleri (1/n)** yukarıdaki **1 TAM** kutusuna taşıyın.")

    # 1. Ayarlar (Sidebar yerine yukarı alalım, daha kolay görünsün)
    col_set1, col_set2 = st.columns([1, 3])
    with col_set1:
        new_denom = st.selectbox(
            "Kesir Takımı Seç:", 
            options=[2, 3, 4, 5, 6], 
            index=1, # Varsayılan 3 (1/3)
            format_func=lambda x: f"1/{x}'lik Parçalar"
        )
        
        # Eğer payda değişirse sayacı sıfırla
        if new_denom != st.session_state.denominator:
            st.session_state.denominator = new_denom
            st.session_state.count = 0
            st.rerun()

    # 2. Görsel Alanı
    fig = draw_interactive_wall(st.session_state.count, st.session_state.denominator)
    st.pyplot(fig)

    # 3. Kontrol Butonları (Oyunun Kalbi)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button(f"➕ 1/{st.session_state.denominator} Ekle", type="primary"):
            add_piece()
            st.rerun()

    with col2:
        if st.button("➖ Çıkar"):
            remove_piece()
            st.rerun()
            
    with col3:
        if st.button("🔄 Sıfırla"):
            reset_game()
            st.rerun()

    # 4. Geri Bildirim Mesajları
    current_val = st.session_state.count
    denom = st.session_state.denominator
    
    st.markdown("---")
    if current_val == 0:
        st.info("👆 Başlamak için **Ekle** butonuna basın.")
    elif current_val < denom:
        st.warning(f"Şu an elimizde **{current_val} tane 1/{denom}** var. 1 Tam olması için **{denom - current_val}** tane daha lazım.")
    elif current_val == denom:
        st.balloons()
        st.success(f"🎉 TEBRİKLER! **{denom} tane 1/{denom}** birleşerek **1 TAM** oluşturdu!")
    else:
        st.error(f"Dikkat! 1 Tam'ı geçtin. Şu an elinde **{current_val}/{denom}** (Bileşik Kesir) var.")

if __name__ == "__main__":
    main()
