import streamlit as st
import streamlit.components.v1 as components

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Çift Yönlü Sayı Doğrusu", layout="wide")

# --- CSS STİLLERİ ---
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    h1, h2, h3 { color: #2c3e50; font-family: 'Segoe UI', sans-serif; }
    .info-box { background-color: #e3f2fd; padding: 15px; border-radius: 10px; border-left: 5px solid #2196f3; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Kesir Seçimi")
    selected_option = st.radio("Parça Boyutu:", ["1/2", "1/3", "1/4", "1/5", "1/6"], index=2)
    denom = int(selected_option.split("/")[1])
    
    st.markdown("---")
    st.write("🗑️ **Temizlemek için:** Sayfayı yenileyin veya aşağıdaki butona basın.")
    if st.button("🔄 Sıfırla"):
        st.rerun()

# --- ANA SAYFA ---
st.title("📏 Çift Yönlü Sayı Doğrusu")
st.markdown("""
<div class="info-box">
    <b>Nasıl Kullanılır?</b><br>
    🔵 Parçaları sürükleyip <b>çizginin üstüne</b> bırakabilirsiniz.<br>
    🟣 Aynı zamanda <b>çizginin altına</b> da parça bırakarak karşılaştırma yapabilirsiniz.
</div>
""", unsafe_allow_html=True)

# --- HTML/CSS/JS KODU ---
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
<style>
    :root {{
        --line-color: #2c3e50;
        --axis-height: 4px;
        --zone-height: 70px;
    }}

    body {{ 
        font-family: 'Segoe UI', sans-serif; 
        display: flex; flex-direction: column; align-items: center; 
        background-color: transparent; margin: 0; padding: 10px; user-select: none;
    }}

    /* --- ANA KONTEYNER --- */
    .workspace {{
        width: 100%; max-width: 900px;
        background: white; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        padding: 20px; margin-top: 10px;
        display: flex; flex-direction: column; align-items: center;
    }}

    /* --- SAYI DOĞRUSU ALANI (SANDVİÇ) --- */
    .number-line-system {{
        position: relative; width: 100%; height: 200px; /* Toplam yükseklik */
        display: flex; flex-direction: column; justify-content: center;
        margin-bottom: 20px;
    }}

    /* 1. ÜST BÖLGE (TOP ZONE) */
    .drop-zone-top {{
        width: 100%; height: var(--zone-height);
        display: flex; align-items: flex-end; /* Tabana yasla */
        border-bottom: 2px dashed rgba(0,0,0,0.1); /* Rehber çizgi */
        position: relative; z-index: 2;
    }}

    /* 2. ORTA EKSEN (AXIS) */
    .axis-layer {{
        width: 100%; height: 40px; position: relative; z-index: 1;
    }}
    
    .main-line {{
        width: 100%; height: var(--axis-height);
        background-color: var(--line-color);
        position: absolute; top: 0;
    }}

    /* Çentikler ve Rakamlar */
    .tick {{ position: absolute; background-color: var(--line-color); transform: translateX(-50%); }}
    .tick.major {{ width: 4px; height: 15px; top: 0; }}
    .tick.minor {{ width: 2px; height: 8px; top: 0; opacity: 0.5; }}
    
    .label {{
        position: absolute; top: 20px; transform: translateX(-50%);
        font-weight: bold; font-size: 18px; color: var(--line-color);
    }}

    /* 3. ALT BÖLGE (BOTTOM ZONE) */
    .drop-zone-bottom {{
        width: 100%; height: var(--zone-height);
        display: flex; align-items: flex-start; /* Tavana yasla */
        border-top: 2px dashed rgba(0,0,0,0.1);
        position: relative; z-index: 2;
    }}

    /* --- BLOKLAR --- */
    .pool {{
        display: flex; gap: 10px; justify-content: center;
        padding: 15px; background: #f1f2f6; border-radius: 10px; width: 100%;
    }}

    .block {{
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; color: white; border: 1px solid rgba(0,0,0,0.1);
        cursor: grab; border-radius: 6px; font-size: 1rem; height: 50px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1); transition: transform 0.1s;
    }}
    .block:active {{ transform: scale(0.95); cursor: grabbing; }}

    /* Sayı doğrusuna bırakılan blokların özel stilleri */
    /* ÜSTTEKİLER */
    .drop-zone-top .block {{
        height: 60px; border-radius: 6px 6px 0 0; margin: 0;
        border-bottom: none; box-shadow: none;
    }}
    
    /* ALTTAKİLER (Ters duruş) */
    .drop-zone-bottom .block {{
        height: 60px; border-radius: 0 0 6px 6px; margin: 0;
        border-top: none; box-shadow: none; align-items: flex-start; padding-top: 15px;
    }}

    /* RENKLER */
    .c2 {{ background-color: #cd84f1; width: 150px; }}
    .c3 {{ background-color: #7d5fff; width: 100px; }}
    .c4 {{ background-color: #74b9ff; width: 80px; }}
    .c5 {{ background-color: #81ecec; width: 70px; color: #333; }}
    .c6 {{ background-color: #55efc4; width: 60px; color: #333; }}

</style>
</head>
<body>

<div class="workspace">
    
    <div class="number-line-system">
        <div id="zone-top" class="drop-zone-top" ondrop="drop(event, 'top')" ondragover="allowDrop(event)">
            </div>

        <div class="axis-layer" id="axis"></div>

        <div id="zone-bottom" class="drop-zone-bottom" ondrop="drop(event, 'bottom')" ondragover="allowDrop(event)">
            </div>
    </div>

    <div style="margin-bottom:5px; color:#aaa; font-size:14px;">PARÇA HAVUZU</div>
    <div class="pool">
        <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}">1/{denom}</div>
        <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}">1/{denom}</div>
        <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}">1/{denom}</div>
        <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}">1/{denom}</div>
        <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}">1/{denom}</div>
        <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}">1/{denom}</div>
    </div>

</div>

<script>
    const MAX_VAL = 2.0;
    const denom = {denom};

    // --- EKSENİ ÇİZ ---
    function drawAxis() {{
        const container = document.getElementById('axis');
        container.innerHTML = '<div class="main-line"></div>'; // Ana çizgi
        
        const totalSubTicks = denom * 2; // 0-2 arası toplam parça

        for(let i=0; i<=totalSubTicks; i++) {{
            let pos = (i / totalSubTicks) * 100;
            let isMajor = (i % denom === 0);
            let val = i / denom;

            if (isMajor) {{
                // Büyük Çentik ve Rakam (0, 1, 2)
                container.innerHTML += `<div class="tick major" style="left: ${{pos}}%"></div>`;
                container.innerHTML += `<div class="label" style="left: ${{pos}}%">${{val}}</div>`;
            }} else {{
                // Küçük Çentik (Ara değerler)
                container.innerHTML += `<div class="tick minor" style="left: ${{pos}}%"></div>`;
            }}
        }}
    }}
    drawAxis();

    // --- SÜRÜKLE BIRAK ---
    function allowDrop(ev) {{ ev.preventDefault(); }}

    function drag(ev) {{
        ev.dataTransfer.setData("className", ev.target.className); 
        ev.dataTransfer.setData("content", ev.target.innerText);
        ev.dataTransfer.setData("val", ev.target.getAttribute("data-val"));
    }}

    function drop(ev, zoneType) {{
        ev.preventDefault();
        
        // Hedef bölgeyi belirle (top veya bottom)
        let targetZone = document.getElementById('zone-' + zoneType);
        
        // Eğer kullanıcı bloğu başka bir bloğun üzerine bırakırsa, 
        // JavaScript hatasını önlemek için "closest" ile ana bölgeyi bul.
        if (!ev.target.id.startsWith('zone-')) {{
            // Hedef yanlışlıkla bir blok olduysa, ana container'a yönlendir
             // Ancak bu basit versiyonda direkt targetZone değişkenini kullanıyoruz, güvenli.
        }}

        const val = parseFloat(ev.dataTransfer.getData("val"));
        
        // O bölgedeki mevcut genişliği hesapla (Basit toplama)
        let currentWidth = 0;
        // Not: Burada gerçek DOM genişliğine bakmıyoruz, mantıksal toplama daha sağlıklı olurdu
        // ama görsel olarak basit ekleme yapıyoruz.
        
        const node = document.createElement("div");
        node.className = ev.dataTransfer.getData("className");
        node.innerText = ev.dataTransfer.getData("content");
        
        // Genişlik hesabı: (Değer / 2) * 100%
        node.style.width = (val / MAX_VAL * 100) + "%";
        
        targetZone.appendChild(node);
        
        // Basit bir kutlama kontrolü (Görsel efekt)
        // Eğer o bölgedeki çocukların toplam genişliği yaklaşık %50 (1 Tam) ise
        checkWin(targetZone);
    }}

    function checkWin(zone) {{
        // Bölgedeki elemanların data-val'larını toplayıp kontrol edebiliriz
        // Şimdilik sadece görsel ve serbest bırakma odaklı.
        // Ama kullanıcıya bir 'tık' sesi veya efekt güzel olurdu.
    }}

</script>
</body>
</html>
"""

components.html(html_code, height=450)
