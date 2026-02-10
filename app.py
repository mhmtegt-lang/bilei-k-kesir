import streamlit as st
import streamlit.components.v1 as components

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Sayı Doğrusu: Bileşik Kesirler", layout="wide")

# --- CSS STİLLERİ ---
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .sidebar .sidebar-content { background-color: #eec9d2; }
    h1, h2, h3 { color: #2c3e50; font-family: 'Segoe UI', sans-serif; }
    .hint-text { background-color: #fff3cd; padding: 10px; border-left: 5px solid #ffc107; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (SOL PANEL) ---
with st.sidebar:
    st.header("⚙️ Ayarlar")
    st.write("Birim kesri seçin:")
    
    selected_option = st.radio(
        "Parça Boyutu:",
        options=["1/2", "1/3", "1/4", "1/5", "1/6"],
        index=2 # Varsayılan 1/4
    )
    
    denom = int(selected_option.split("/")[1])
    
    st.markdown("---")
    st.markdown("""
    <div class="hint-text">
    💡 **Yeni Hedef:** <br>
    Parçaları birleştirerek önce <b>1 Tam</b>'a ulaşın.<br>
    Sonra parça eklemeye devam ederek <b>1'i geçin</b> (Örn: 1 tam 1/4).
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    if st.button("🔄 Ekranı Temizle"):
        st.rerun()

# --- ANA SAYFA ---
col1, col2 = st.columns([1, 10]) 

with col2:
    st.title(f"📏 Sayı Doğrusunda İlerleme ({selected_option})")
    st.write("Aşağıdaki parçaları sürükleyip sayı doğrusunun üzerine bırakın. 1'e ulaştığınızda durmayın, devam edin!")

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
            --whole-color: #ff9ff3;
            --whole-border: #fd79a8;
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
        
        /* SAYI DOĞRUSU ALANI (Kapsayıcı) */
        .number-line-wrapper {{
            position: relative;
            width: 100%;
            max-width: 850px;
            height: 220px;
            margin-top: 20px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            padding: 20px;
            box-sizing: border-box;
        }}

        /* Drop Zone (Bırakma Alanı - Çizginin Üstü) */
        .drop-zone {{
            width: 100%;
            height: 60px;
            display: flex;
            align-items: flex-end;
            justify-content: flex-start;
            position: relative;
            border-bottom: 4px solid var(--line-color);
            z-index: 10;
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
            left: 20px; top: 80px; height: 40px; pointer-events: none; z-index: 5;
        }}
        .tick-mark {{ position: absolute; background-color: var(--line-color); transform: translateX(-50%); }}
        .tick-main {{ height: 20px; width: 4px; top: 0; }}
        .tick-sub {{ height: 10px; width: 2px; top: 0; opacity: 0.6; }}
        .tick-label {{ position: absolute; top: 25px; transform: translateX(-50%); font-size: 18px; font-weight: bold; color: var(--text-color); }}

        /* --- BÜTÜN KATMANI (Sayı doğrusunun ALTI) --- */
        .wholes-layer {{
            position: absolute; width: calc(100% - 40px); left: 20px; top: 140px; height: 50px; display: flex; pointer-events: none;
        }}
        .whole-indicator {{
            position: absolute; height: 100%; width: 50%; /* 0-1 ve 1-2 arası */
            background-color: var(--whole-color); border: 2px solid var(--whole-border);
            border-radius: 8px; display: flex; align-items: center; justify-content: center;
            font-size: 20px; font-weight: bold; color: #2d3436;
            opacity: 0; transition: all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275); transform: translateY(-10px);
        }}
        .whole-indicator.visible {{ opacity: 1; transform: translateY(0); }}

        /* BLOKLAR ALANI */
        .fraction-pool {{
            display: flex; flex-direction: column; gap: 15px; margin-top: 30px; width: 100%; max-width: 850px; align-items: center;
        }}
        .row {{ display: flex; width: 100%; justify-content: center; gap: 5px; }}

        /* BLOK STİLİ */
        .block {{
            display: flex; align-items: center; justify-content: center; font-weight: bold; color: #fff; 
            border: 1px solid rgba(0,0,0,0.15); cursor: grab; border-radius: 6px; font-size: 1.1rem;
            height: 50px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); transition: transform 0.1s;
        }}
        .block:active {{ cursor: grabbing; transform: scale(0.95); }}

        /* Sayı doğrusuna bırakılan blok */
        .drop-zone .block {{
            height: 56px; border-radius: 4px 4px 0 0; border-bottom: none; margin: 0; box-shadow: none; color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
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

        <div class="number-line-wrapper">
            <div id="target" class="drop-zone" ondrop="drop(event)" ondragover="allowDrop(event)"></div>
            <div class="ticks-layer" id="ticks-container"></div>
            
            <div class="wholes-layer">
                <div id="whole-1" class="whole-indicator" style="left: 0%;">1 TAM</div>
                <div id="whole-2" class="whole-indicator" style="left: 50%;">2 TAM</div>
            </div>
        </div>

        <div class="fraction-pool">
            <div style="font-size: 14px; color: #aaa; margin-bottom: 5px;">KULLANILABİLİR PARÇALAR (1/{denom})</div>
            <div class="row">
                <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}">1/{denom}</div>
                <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}">1/{denom}</div>
                <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}">1/{denom}</div>
                <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}">1/{denom}</div>
                <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}">1/{denom}</div>
                <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}">1/{denom}</div>
                <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}">1/{denom}</div>
                <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}">1/{denom}</div>
            </div>
             <div style="font-size: 12px; color: #aaa;">(Dilediğiniz kadar parça alabilirsiniz)</div>
        </div>

    <script>
        let currentSum = 0;
        const MAX_VAL = 2.0; // Sayı doğrusu 2'ye kadar gidiyor
        const denom = {denom}; 

        // --- ÇİZİM FONKSİYONLARI ---
        function drawTicks() {{
            const container = document.getElementById('ticks-container');
            container.innerHTML = '';
            const totalRange = 2;
            const totalSubTicks = denom * totalRange;

            for(let i=0; i <= totalSubTicks; i++) {{
                let pos = (i / totalSubTicks) * 100;
                let val = i / denom;
                let isMain = (i % denom === 0);

                if (isMain) {{
                    container.innerHTML += `<div class="tick-mark tick-main" style="left: ${{pos}}%"></div>`;
                    container.innerHTML += `<div class="tick-label" style="left: ${{pos}}%">${{val}}</div>`;
                }} else {{
                    container.innerHTML += `<div class="tick-mark tick-sub" style="left: ${{pos}}%"></div>`;
                }}
            }}
        }}

        drawTicks();

        // --- SÜRÜKLE BIRAK MANTIĞI ---
        function allowDrop(ev) {{ ev.preventDefault(); }}

        function drag(ev) {{
            ev.dataTransfer.setData("className", ev.target.className); 
            ev.dataTransfer.setData("content", ev.target.innerText);
            ev.dataTransfer.setData("val", ev.target.getAttribute("data-val"));
        }}

        function drop(ev) {{
            ev.preventDefault();
            const val = parseFloat(ev.dataTransfer.getData("val"));
            
            // 2'yi geçmeyi engelle (Küçük bir tolerans ile)
            if (currentSum + val > MAX_VAL + 0.001) {{
                alert("Sayı doğrusunun sonuna (2) ulaştınız!");
                return; 
            }}

            const originalClass = ev.dataTransfer.getData("className");
            const content = ev.dataTransfer.getData("content");
            
            const node = document.createElement("div");
            node.className = originalClass;
            node.innerText = content;
            // Genişliği sayı doğrusunun toplam uzunluğuna (2 birim) göre oranla
            node.style.width = (val / MAX_VAL * 100) + "%";
            
            document.getElementById("target").appendChild(node);
            currentSum += val;

            checkWholeCondition();
        }}

        // --- KONTROL MEKANİZMASI ---
        function checkWholeCondition() {{
            // 1 Tam kontrolü
            if (currentSum >= 0.99) {{
                const w1 = document.getElementById('whole-1');
                if (!w1.classList.contains('visible')) {{
                    w1.classList.add('visible');
                    confetti({{ particleCount: 80, spread: 60, origin: {{ y: 0.5 }}, colors: ['#ff9ff3', '#fd79a8'] }});
                }}
            }}
            
            // 2 Tam kontrolü (Büyük kutlama)
            if (currentSum >= 1.99) {{
                const w2 = document.getElementById('whole-2');
                if (!w2.classList.contains('visible')) {{
                    w2.classList.add('visible');
                    confetti({{ particleCount: 150, spread: 100, origin: {{ y: 0.5 }} }});
                }}
            }}
        }}
    </script>
    </body>
    </html>
    """

    components.html(html_code, height=650)
