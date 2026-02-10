import streamlit as st
import streamlit.components.v1 as components

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Kesirleri Birleştir", layout="wide")

st.markdown("<h2 style='text-align: center;'>🧩 Kesirleri Bütüne Tamamla</h2>", unsafe_allow_html=True)

# --- HTML/CSS/JS KODU ---
html_code = """
<!DOCTYPE html>
<html>
<head>
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
<style>
    body { font-family: 'Arial', sans-serif; background-color: #f0f2f6; display: flex; flex-direction: column; align-items: center; }
    
    /* HEDEF ALAN (PEMBE 1 BLOĞU) */
    #target-container {
        width: 100%;
        max-width: 800px;
        margin: 20px 0;
        text-align: center;
    }

    .drop-zone {
        width: 100%;
        height: 80px;
        border: 3px dashed #ff9ff3;
        background-color: rgba(255, 159, 243, 0.1);
        display: flex;
        align-items: center;
        justify-content: flex-start;
        position: relative;
        border-radius: 10px;
        overflow: hidden;
        transition: all 0.3s;
    }

    .drop-zone.full-border {
        border: 3px solid #ff9ff3;
        background-color: white;
    }

    .target-label {
        position: absolute;
        width: 100%;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #ff9ff3;
        z-index: 0;
        pointer-events: none;
    }

    /* KESİR DUVARI */
    .fraction-wall {
        width: 100%;
        max-width: 800px;
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-top: 30px;
    }

    .row { display: flex; width: 100%; height: 60px; gap: 4px; }

    /* PARÇA STİLLERİ */
    .block {
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: #2c3e50;
        border: 1px solid rgba(0,0,0,0.1);
        cursor: grab;
        border-radius: 6px;
        font-size: 1.1rem;
        z-index: 1;
    }

    .block:active { cursor: grabbing; }

    /* RENKLER (Görsellerle Birebir) */
    .c1 { background-color: #ff9ff3; width: 100%; }   /* 1 */
    .c2 { background-color: #d980fa; width: 50%; }   /* 1/2 */
    .c3 { background-color: #a29bfe; width: 33.33%; } /* 1/3 */
    .c4 { background-color: #74b9ff; width: 25%; }   /* 1/4 */
    .c5 { background-color: #81ecec; width: 20%; }   /* 1/5 */
    .c6 { background-color: #55efc4; width: 16.66%; } /* 1/6 */

    /* HEDEF İÇİNDEKİ PARÇALAR */
    .drop-zone .block {
        height: 100%;
        border-radius: 0;
        cursor: default;
    }

    .btn-reset {
        margin-bottom: 10px;
        padding: 10px 20px;
        background-color: #34495e;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
    }
</style>
</head>
<body>

    <button class="btn-reset" onclick="resetAll()">Temizle ve Yeniden Başla</button>

    <div id="target-container">
        <div id="target" class="drop-zone" ondrop="drop(event)" ondragover="allowDrop(event)">
            <div class="target-label">1</div>
        </div>
    </div>

    <div class="fraction-wall">
        <div class="row">
            <div class="block c2" draggable="true" ondragstart="drag(event)" data-val="0.5">1/2</div>
            <div class="block c2" draggable="true" ondragstart="drag(event)" data-val="0.5">1/2</div>
        </div>
        <div class="row">
            <div class="block c3" draggable="true" ondragstart="drag(event)" data-val="0.333">1/3</div>
            <div class="block c3" draggable="true" ondragstart="drag(event)" data-val="0.333">1/3</div>
            <div class="block c3" draggable="true" ondragstart="drag(event)" data-val="0.333">1/3</div>
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

<script>
    let currentSum = 0;

    function allowDrop(ev) { ev.preventDefault(); }

    function drag(ev) {
        ev.dataTransfer.setData("className", ev.target.className); 
        ev.dataTransfer.setData("content", ev.target.innerText);
        ev.dataTransfer.setData("val", ev.target.getAttribute("data-val"));
    }

    function drop(ev) {
        ev.preventDefault();
        const val = parseFloat(ev.dataTransfer.getData("val"));
        
        // 1 Tam'ı aşma kontrolü
        if (currentSum + val > 1.01) {
            alert("Dikkat! Bu parça bütünden fazla geliyor.");
            return;
        }

        const className = ev.dataTransfer.getData("className");
        const content = ev.dataTransfer.getData("content");
        
        const node = document.createElement("div");
        node.className = className;
        node.innerText = content;
        
        document.getElementById("target").appendChild(node);
        currentSum += val;

        // Tam dolma kontrolü
        if (currentSum >= 0.99) {
            confetti({
                particleCount: 150,
                spread: 70,
                origin: { y: 0.6 }
            });
            document.getElementById("target").classList.add("full-border");
        }
    }

    function resetAll() {
        document.getElementById("target").innerHTML = '<div class="target-label">1</div>';
        document.getElementById("target").classList.remove("full-border");
        currentSum = 0;
    }
</script>

</body>
</html>
"""

components.html(html_code, height=650)
