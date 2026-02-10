import streamlit as st
import streamlit.components.v1 as components

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Sayı Doğrusu Atölyesi", layout="centered")

st.markdown("<h2 style='text-align: center; color: #2c3e50;'>📏 Sayı Doğrusu ve Kesir Modelleri</h2>", unsafe_allow_html=True)

# Streamlit üzerinden bölme sayısını seçelim
st.write("### 1. Sayı Doğrusu Bölmelerini Ayarla")
div_denom = st.selectbox("Sayı doğrusu kaça bölünsün? (0-1 arası)", [2, 3, 4, 5, 6], index=1)

# --- HTML/CSS/JS KODU ---
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
<style>
    :root {{
        --line-color: #00a8ff;
        --bg-color: #fcfcfc;
    }}

    body {{ 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        background-color: var(--bg-color); 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        margin: 0;
        padding: 20px;
        overflow-x: hidden;
    }}
    
    .main-container {{
        width: 100%;
        max-width: 800px;
        display: flex;
        flex-direction: column;
        gap: 30px;
    }}

    /* SAYI DOĞRUSU ALANI */
    .number-line-container {{
        position: relative;
        width: 100%;
        height: 140px;
        margin-top: 40px;
    }}

    /* Drop Zone (Sayı doğrusunun tam üstü) */
    .drop-zone {{
        width: 100%;
        height: 50px;
        display: flex;
        align-items: flex-end;
        justify-content: flex-start;
        position: relative;
        border-bottom: 3px solid var(--line-color);
        box-sizing: border-box;
        z-index: 2;
    }}

    /* Ana Sayı Doğrusu Çizgisi ve Oklar */
    .drop-zone::before, .drop-zone::after {{
        content: '';
        position: absolute;
        bottom: -8px;
        width: 15px;
        height: 3px;
        background-color: var(--line-color);
    }}
    .drop-zone::before {{ left: -5px; transform: rotate(-45deg); origin: right; }}
    .drop-zone::after {{ right: -5px; transform: rotate(45deg); origin: left; }}

    /* Sayı doğrusu üzerindeki ana noktalar ve sayılar */
    .ticks {{
        position: absolute;
        width: 100%;
        top: 50px;
        z-index: 1;
    }}

    .main-tick {{
        position: absolute;
        height: 16px;
        width: 16px;
        background-color: var(--line-color);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        top: 0;
    }}

    .sub-tick {{
        position: absolute;
        height: 8px;
        width: 8px;
        background-color: var(--line-color);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        top: 0;
        opacity: 0.6;
    }}

    .tick-label {{
        position: absolute;
        top: 15px;
        font-weight: bold;
        transform: translateX(-50%);
        color: #2c3e50;
        font-size: 20px;
    }}

    /* KESİR TAKIMI (ALTTAKİ BLOKLAR) */
    .fraction-wall {{
        display: flex;
        flex-direction: column;
        gap: 10px;
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}

    .row {{ display: flex; width: 100%; height: 55px; gap: 6px; }}

    .block {{
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: #2c3e50;
        border: 1px solid rgba(0,0,0,0.1);
        cursor: grab;
        border-radius: 8px;
        font-size: 1.1rem;
        box-sizing: border-box;
        transition: all 0.2s;
    }}

    .block:hover {{ transform: scale(1.02); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}

    /* BIRAKILAN PARÇALARIN STİLİ */
    .drop-zone .block {{
        height: 45px;
        border-radius: 4px 4px 0 0;
        border-bottom: none;
    }}

    /* RENK PALETİ (Görsellerle birebir) */
    .c1 {{ background-color: #ff9ff3; width: 100%; }}   /* 1 Tam */
    .c2 {{ background-color: #d980fa; width: 50%; }}   /* 1/2 */
    .c3 {{ background-color: #a29bfe; width: 33.33%; }} /* 1/3 */
    .c4 {{ background-color: #74b9ff; width: 25%; }}   /* 1/4 */
    .c5 {{ background-color: #81ecec; width: 20%; }}   /* 1/5 */

    .btn-reset {{
        padding: 10px 25px;
        background-color: #2d3436;
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-weight: bold;
        margin-bottom: 20px;
    }}
</style>
</head>
<body>

    <button class="btn-reset" onclick="resetAll()">Sıfırla ve Temizle</button>

    <div class="main-container">
        
        <div class="number-line-container">
            <div id="target" class="drop-zone" ondrop="drop(event)" ondragover="allowDrop(event)"></div>
            <div class="ticks" id="ticks-container">
                </div>
        </div>

        <div style="text-align: center; color: #636e72;">👇 Parçaları sayı doğrusuna taşıyın</div>

        <div class="fraction-wall">
            <div class="row">
                <div class="block c1" draggable="true" ondragstart="drag(event)" data-val="1">1</div>
            </div>
            <div class="row">
                <div class="block c2" draggable="true" ondragstart="drag(event)" data-val="0.5">1/2</div>
                <div class="block c2" draggable="true" ondragstart="drag(event)" data-val="0.5">1/2</div>
            </div>
            <div class="row">
                <div class="block c3" draggable="true" ondragstart="drag(event)" data-val="0.33333">1/3</div>
                <div class="block c3" draggable="true" ondragstart="drag(event)" data-val="0.33333">1/3</div>
                <div class="block c3" draggable="true" ondragstart="drag(event)" data-val="0.33333">1/3</div>
            </div>
            <div class="row">
                <div class="block c4" draggable="true" ondragstart="drag(event)" data-val="0.25">1/4</div>
                <div class="block c4" draggable="true" ondragstart="drag(event)" data-val="0.25">1/4</div>
                <div class="block c4" draggable="true" ondragstart="drag(event)" data-val="0.25">1/4</div>
                <div class="block c4" draggable="true" ondragstart="drag(event)" data-val="0.25">1/4</div>
            </div>
        </div>
    </div>

<script>
    let currentSum = 0;
    const MAX_VAL = 2.0;
    const denom = {div_denom}; // Streamlit'ten gelen payda

    // Sayı doğrusu çentiklerini çiz
    function drawTicks() {{
        const container = document.getElementById('ticks-container');
        container.innerHTML = '';
        
        // 0, 1, 2 ana noktaları
        for(let i=0; i<=2; i++) {{
            let pos = (i / 2) * 100;
            container.innerHTML += `<div class="main-tick" style="left: ${{pos}}%"></div>`;
            container.innerHTML += `<div class="tick-label" style="left: ${{pos}}%">${{i}}</div>`;
        }

        // Ara çentikler (Streamlit'ten seçilen paydaya göre)
        for(let i=1; i < denom * 2; i++) {{
            if (i % denom === 0) continue; // Ana noktalarla çakışmasın
            let pos = (i / (denom * 2)) * 100;
            container.innerHTML += `<div class="sub-tick" style="left: ${{pos}}%"></div>`;
        }
    }

    drawTicks();

    function allowDrop(ev) {{ ev.preventDefault(); }}

    function drag(ev) {{
        ev.dataTransfer.setData("className", ev.target.className); 
        ev.dataTransfer.setData("content", ev.target.innerText);
        ev.dataTransfer.setData("val", ev.target.getAttribute("data-val"));
    }}

    function drop(ev) {{
        ev.preventDefault();
        const val = parseFloat(ev.dataTransfer.getData("val"));
        
        if (currentSum + val > MAX_VAL + 0.001) return;

        const node = document.createElement("div");
        node.className = ev.dataTransfer.getData("className");
        node.innerText = ev.dataTransfer.getData("content");
        node.style.width = (val / MAX_VAL * 100) + "%";
        
        document.getElementById("target").appendChild(node);
        currentSum += val;

        if (Math.abs(currentSum - 1.0) < 0.02 || Math.abs(currentSum - 2.0) < 0.02) {{
            confetti({{ particleCount: 100, spread: 70, origin: {{ y: 0.3 }} }});
        }
    }}

    function resetAll() {{
        document.getElementById("target").innerHTML = '';
        currentSum = 0;
    }}
</script>
</body>
</html>
"""

# Komponenti görüntüle
components.html(html_code, height=850, scrolling=False)
