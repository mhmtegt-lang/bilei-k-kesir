import streamlit as st
import streamlit.components.v1 as components

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Sayı Doğrusu Modeli", layout="wide")

# --- CSS STİLLERİ (STREAMLIT ARAYÜZÜ İÇİN) ---
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .sidebar .sidebar-content { background-color: #eec9d2; }
    h1, h2, h3 { color: #2c3e50; font-family: 'Segoe UI', sans-serif; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (SOL PANEL) ---
with st.sidebar:
    st.header("⚙️ Ayarlar")
    st.write("Çalışmak istediğiniz birim kesri seçin:")
    
    # Seçim Kutusu (Radio Button daha kullanışlı)
    selected_option = st.radio(
        "Birim Kesir:",
        options=["1/2", "1/3", "1/4", "1/5", "1/6"],
        index=1 # Varsayılan 1/3
    )
    
    # Seçimi sayıya çevir (Örn: "1/4" -> 4)
    denom = int(selected_option.split("/")[1])
    
    st.markdown("---")
    st.info(f"💡 **Bilgi:** Şu an sayı doğrusu **{denom}** eşit parçaya bölündü.")
    st.markdown("---")
    
    # Sıfırlama Butonu (Session State kullanmadığımız için sayfayı yeniler gibi davranacak JS tarafında)
    if st.button("🔄 Ekranı Temizle"):
        st.rerun()

# --- ANA SAYFA ---
col1, col2 = st.columns([1, 10]) # Ortalamak için boşluk

with col2:
    st.title(f"📏 Sayı Doğrusunda {selected_option}'leri Göster")
    st.markdown("Soldaki menüden seçtiğiniz parçaları sürükleyip sayı doğrusu üzerine bırakın.")

    # --- HTML/CSS/JS KODU ---
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <style>
        :root {{
            --line-color: #0984e3;
            --bg-color: #ffffff;
            --text-color: #2d3436;
        }}

        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background-color: transparent; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            margin: 0;
            padding: 10px;
            user-select: none;
        }}
        
        /* SAYI DOĞRUSU ALANI */
        .number-line-wrapper {{
            position: relative;
            width: 100%;
            max-width: 850px;
            height: 160px;
            margin-top: 20px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            padding: 20px;
            box-sizing: border-box;
        }}

        /* Drop Zone (Bırakma Alanı) */
        .drop-zone {{
            width: 100%;
            height: 60px;
            display: flex;
            align-items: flex-end;
            justify-content: flex-start;
            position: relative;
            border-bottom: 4px solid var(--line-color);
            z-index: 2;
        }}

        /* Ok Uçları */
        .drop-zone::before {{ 
            content: ''; position: absolute; bottom: -10px; left: -10px; 
            border-width: 10px 15px 10px 0; border-color: transparent var(--line-color) transparent transparent; border-style: solid;
        }}
        .drop-zone::after {{ 
            content: ''; position: absolute; bottom: -10px; right: -10px; 
            border-width: 10px 0 10px 15px; border-color: transparent transparent transparent var(--line-color); border-style: solid;
        }}

        /* Çentikler (Ticks) */
        .ticks-layer {{
            position: absolute;
            width: calc(100% - 40px); /* Padding payı */
            left: 20px;
            top: 80px; /* Drop zone altı */
            height: 50px;
            pointer-events: none;
        }}

        .tick-mark {{
            position: absolute;
            background-color: var(--line-color);
            transform: translateX(-50%);
        }}

        .tick-main {{
            height: 20px; width: 4px; top: 0;
        }}
        
        .tick-sub {{
            height: 10px; width: 2px; top: 0; opacity: 0.6;
        }}

        .tick-label {{
            position: absolute;
            top: 25px;
            transform: translateX(-50%);
            font-size: 18px;
            font-weight: bold;
            color: var(--text-color);
        }}

        /* BLOKLAR ALANI */
        .fraction-pool {{
            display: flex;
            flex-direction: column;
            gap: 15px;
            margin-top: 30px;
            width: 100%;
            max-width: 850px;
            align-items: center;
        }}

        .pool-label {{
            font-size: 14px; color: #636e72; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px;
        }}

        .row {{ display: flex; width: 100%; justify-content: center; gap: 5px; }}

        /* BLOK STİLİ */
        .block {{
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: #333; /* Daha okunabilir olması için koyu renk yazı */
            border: 1px solid rgba(0,0,0,0.15);
            cursor: grab;
            border-radius: 6px;
            font-size: 1.1rem;
            height: 50px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: transform 0.1s;
        }}

        .block:active {{ cursor: grabbing; transform: scale(0.95); }}

        /* Sayı doğrusuna bırakılan blok */
        .drop-zone .block {{
            height: 56px; /* Çizgiye tam otursun */
            border-radius: 4px 4px 0 0;
            border-bottom: none;
            margin: 0;
            box-shadow: none;
            color: white; /* Sayı doğrusunda beyaz yazı şık durur */
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }}

        /* RENKLER (Resimden alındı) */
        .c1 {{ background-color: #ff9ff3; width: 100%; color: #333; }}       /* 1 Tam */
        .c2 {{ background-color: #cd84f1; width: 150px; color: white; }}   /* 1/2 Mor */
        .c3 {{ background-color: #7d5fff; width: 100px; color: white; }}   /* 1/3 Koyu Mor/Mavi */
        .c4 {{ background-color: #74b9ff; width: 80px; color: white; }}    /* 1/4 Mavi */
        .c5 {{ background-color: #81ecec; width: 70px; color: #333; }}     /* 1/5 Turkuaz */
        .c6 {{ background-color: #55efc4; width: 60px; color: #333; }}     /* 1/6 Yeşil */

    </style>
    </head>
    <body>

        <div class="number-line-wrapper">
            <div id="target" class="drop-zone" ondrop="drop(event)" ondragover="allowDrop(event)"></div>
            <div class="ticks-layer" id="ticks-container"></div>
        </div>

        <div class="fraction-pool">
            
            <div class="pool-label">Referans Blok</div>
            <div class="row" style="width: 100%;">
                 <div class="block c1" draggable="true" ondragstart="drag(event)" data-val="1">1 TAM</div>
            </div>

            <div class="pool-label" style="margin-top: 15px;">Kullanılabilir Parçalar (1/{denom})</div>
            <div class="row">
                <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}">1/{denom}</div>
                <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}">1/{denom}</div>
                <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}">1/{denom}</div>
                <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}">1/{denom}</div>
                <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}">1/{denom}</div>
                <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}">1/{denom}</div>
            </div>
             <div style="font-size: 12px; color: #aaa; margin-top: 5px;">(İhtiyaç duydukça sürükleyebilirsiniz, sınırsızdır)</div>
        </div>

    <script>
        let currentSum = 0;
        const MAX_VAL = 2.0;
        const denom = {denom}; 

        // --- SAYI DOĞRUSU ÇİZİMİ ---
        function drawTicks() {{
            const container = document.getElementById('ticks-container');
            container.innerHTML = '';
            
            // Toplam uzunluk (0-2 arası)
            const totalRange = 2;
            
            // Kaç tane küçük aralık olacak? (Payda * 2) -> Örn: 1/3 ise 0-2 arasında 6 parça olur.
            const totalSubTicks = denom * totalRange;

            for(let i=0; i <= totalSubTicks; i++) {{
                // Konum hesapla (Yüzde olarak)
                let pos = (i / totalSubTicks) * 100;
                
                // Değer hesapla
                let val = i / denom;
                
                // Ana sayı mı (Tam sayı)?
                let isMain = (i % denom === 0);

                if (isMain) {{
                    container.innerHTML += `<div class="tick-mark tick-main" style="left: ${{pos}}%"></div>`;
                    container.innerHTML += `<div class="tick-label" style="left: ${{pos}}%">${{val}}</div>`;
                }} else {{
                    container.innerHTML += `<div class="tick-mark tick-sub" style="left: ${{pos}}%"></div>`;
                }}
            }}
        }}

        // Başlangıçta çiz
        drawTicks();

        // --- SÜRÜKLE BIRAK MANTIĞI ---
        function allowDrop(ev) {{ ev.preventDefault(); }}

        function drag(ev) {{
            // CSS sınıfını taşı (renk için)
            ev.dataTransfer.setData("className", ev.target.className); 
            ev.dataTransfer.setData("content", ev.target.innerText);
            ev.dataTransfer.setData("val", ev.target.getAttribute("data-val"));
        }}

        function drop(ev) {{
            ev.preventDefault();
            const val = parseFloat(ev.dataTransfer.getData("val"));
            
            // 2'yi geçmesin
            if (currentSum + val > MAX_VAL + 0.001) {{
                return; 
            }}

            const originalClass = ev.dataTransfer.getData("className");
            const content = ev.dataTransfer.getData("content");
            
            const node = document.createElement("div");
            node.className = originalClass;
            node.innerText = content;
            
            // Genişliği sayı doğrusuna oranla hesapla
            // val (kesir değeri) / MAX_VAL (2) * 100
            node.style.width = (val / MAX_VAL * 100) + "%";
            
            document.getElementById("target").appendChild(node);
            currentSum += val;

            // Efektler
            checkWinCondition();
        }}

        function checkWinCondition() {{
            // Tam sayılara (1 veya 2) çok yaklaştı mı?
            if (Math.abs(currentSum - 1.0) < 0.01 || Math.abs(currentSum - 2.0) < 0.01) {{
                confetti({{ particleCount: 100, spread: 70, origin: {{ y: 0.4 }} }});
            }}
        }}
    </script>
    </body>
    </html>
    """

    components.html(html_code, height=600)
