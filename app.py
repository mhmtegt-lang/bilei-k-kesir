import streamlit as st
import streamlit.components.v1 as components

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Sayı Doğrusunda Kesirler", layout="centered")

st.markdown("<h3 style='text-align: center; color: #2c3e50;'>📏 Sayı Doğrusunda Kesirleri İlerlet</h3>", unsafe_allow_html=True)

# --- HTML/CSS/JS KODU ---
html_code = """
<!DOCTYPE html>
<html>
<head>
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
<style>
    :root {
        --line-height: 80px;
        --max-width: 800px;
        --line-color: #3498db;
    }

    body { 
        font-family: 'Segoe UI', sans-serif; 
        background-color: transparent; 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        padding: 20px;
    }
    
    .main-container {
        width: 100%;
        max-width: var(--max-width);
        display: flex;
        flex-direction: column;
        gap: 40px;
    }

    /* SAYI DOĞRUSU ALANI */
    .number-line-container {
        position: relative;
        width: 100%;
        height: 120px;
        margin-bottom: 20px;
    }

    /* Kesirlerin bırakılacağı drop zone (Sayı doğrusunun hemen üstü) */
    .drop-zone {
        width: 100%;
        height: 50px;
        display: flex;
        align-items: flex-end;
        justify-content: flex-start;
        position: relative;
        border-bottom: 3px solid var(--line-color);
        box-sizing: border-box;
    }

    /* Sayı doğrusu üzerindeki ana çizgiler ve sayılar */
    .ticks {
        position: absolute;
        width: 100%;
        display: flex;
        justify-content: space-between;
        top: 50px;
        z-index: 0;
    }

    .tick {
        position: absolute;
        height: 15px;
        width: 3px;
        background-color: var(--line-color);
        transform: translateX(-50%);
    }

    .tick-label {
        position: absolute;
        top: 20px;
        font-weight: bold;
        transform: translateX(-50%);
        color: #2c3e50;
        font-size: 18px;
    }

    /* KESİR DUVARI SIRALARI */
    .fraction-wall {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .row { display: flex; width: 100%; height: 50px; gap: 4px; }

    /* BLOK STİLLERİ */
    .block {
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: #fff;
        border: 1px solid rgba(0,0,0,0.1);
        cursor: grab;
        border-radius: 6px;
        font-size: 1rem;
        box-sizing: border-box;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }

    /* SAYI DOĞRUSUNA BIRAKILAN PARÇALARIN ÖZEL STİLİ */
    .drop-zone .block {
        height: 40px;
        border-radius: 4px 4px 0 0;
        position: relative;
        margin-bottom: 0;
    }

    /* RENKLER */
    .c2 { background-color: #d980fa; width: 50%; }   /* 1/2 */
    .c3 { background-color: #a29bfe; width: 33.333%; } /* 1/3 */
    .c4 { background-color: #74b9ff; width: 25%; }   /* 1/4 */
    .c5 { background-color: #81ecec; width: 20%; }   /* 1/5 */

    .btn-reset {
        padding: 10px 20px;
        background-color: #34495e;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
        margin-bottom: 10px;
    }
</style>
</head>
<body>

    <div class="main-container">
        
        <div style="text-align:center;">
            <button class="btn-reset" onclick="resetAll()">Sıfırla</button>
        </div>

        <div class="number-line-container">
            <div id="target" class="drop-zone" ondrop="drop(event)" ondragover="allowDrop(event)">
                </div>
            <div class="ticks">
                <div style="left: 0%;">
                    <div class="tick"></div>
                    <div class="tick-label">0</div>
                </div>
                <div style="left: 50%;">
                    <div class="tick"></div>
                    <div class="tick-label">1</div>
                </div>
                <div style="left: 100%;">
                    <div class="tick"></div>
                    <div class="tick-label">2</div>
                </div>
            </div>
        </div>

        <div class="fraction-wall">
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
            <div class="row">
                <div class="block c5" draggable="true" ondragstart="drag(event)" data-val="0.2">1/5</div>
                <div class="block c5" draggable="true" ondragstart="drag(event)" data-val="0.2">1/5</div>
                <div class="block c5" draggable="true" ondragstart="drag(event)" data-val="0.2">1/5</div>
                <div class="block c5" draggable="true" ondragstart="drag(event)" data-val="0.2">1/5</div>
                <div class="block c5" draggable="true" ondragstart="drag(event)" data-val="0.2">1/5</div>
            </div>
        </div>

    </div>

<script>
    let currentSum = 0;
    const MAX_VAL = 2.0; // Sayı doğrusu 0-2 arası

    function allowDrop(ev) { ev.preventDefault(); }

    function drag(ev) {
        ev.dataTransfer.setData("className", ev.target.className); 
        ev.dataTransfer.setData("content", ev.target.innerText);
        ev.dataTransfer.setData("val", ev.target.getAttribute("data-val"));
    }

    function drop(ev) {
        ev.preventDefault();
        const val = parseFloat(ev.dataTransfer.getData("val"));
        
        if (currentSum + val > MAX_VAL + 0.01) {
            alert("Sayı doğrusunun dışına çıktınız (2'yi geçtiniz)!");
            return;
        }

        const className = ev.dataTransfer.getData("className");
        const content = ev.dataTransfer.getData("content");
        
        const node = document.createElement("div");
        node.className = className;
        node.innerText = content;
        
        // Sayı doğrusu 0-2 arası olduğu için genişliği yarıya bölüyoruz.
        // %100 genişlik = 2 birim. Dolayısıyla 1/2 (0.5) genişliği %25 olmalı.
        node.style.width = (val / MAX_VAL * 100) + "%";
        
        document.getElementById("target").appendChild(node);
        currentSum += val;

        // Tam sayılara (1 veya 2) ulaşıldığında kutlama
        if (Math.abs(currentSum - 1.0) < 0.02 || Math.abs(currentSum - 2.0) < 0.02) {
            confetti({
                particleCount: 150,
                spread: 70,
                origin: { y: 0.3 }
            });
        }
    }

    function resetAll() {
        document.getElementById("target").innerHTML = '';
        currentSum = 0;
    }
</script>

</body>
</html>
"""

components.html(html_code, height=700, scrolling=False)
