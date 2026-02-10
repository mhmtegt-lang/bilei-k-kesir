import streamlit as st
import streamlit.components.v1 as components

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Kesir Duvarı Eğitimi", layout="centered")

st.markdown("<h3 style='text-align: center; color: #2c3e50;'>🧩 Kesirleri Bütüne Tamamla</h3>", unsafe_allow_html=True)

# --- HTML/CSS/JS KODU ---
html_code = """
<!DOCTYPE html>
<html>
<head>
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
<style>
    :root {
        --row-height: 65px;
        --max-width: 700px;
        --border-radius: 10px;
    }

    body { 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        background-color: transparent; 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        margin: 0;
        padding: 10px;
    }
    
    /* ANA KONTEYNER (DİKEY SIRALAMA) */
    .main-container {
        width: 100%;
        max-width: var(--max-width);
        display: flex;
        flex-direction: column;
        gap: 15px; /* Bloklar arası boşluk */
    }

    /* HEDEF ALAN (1 BLOĞU İLE AYNI BOYUTTA) */
    .drop-zone {
        width: 100%;
        height: var(--row-height);
        border: 3px dashed #ff9ff3;
        background-color: rgba(255, 159, 243, 0.05);
        display: flex;
        align-items: center;
        justify-content: flex-start;
        position: relative;
        border-radius: var(--border-radius);
        overflow: hidden;
        box-sizing: border-box;
    }

    .drop-zone.completed {
        border: 3px solid #ff9ff3;
        background-color: white;
    }

    .target-label {
        position: absolute;
        width: 100%;
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        color: #ff9ff3;
        z-index: 0;
        pointer-events: none;
    }

    /* KESİR DUVARI SIRALARI */
    .fraction-wall {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .row { 
        display: flex; 
        width: 100%; 
        height: var(--row-height); 
        gap: 4px; 
    }

    /* BLOK STİLLERİ */
    .block {
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: #2c3e50;
        border: 1px solid rgba(0,0,0,0.1);
        cursor: grab;
        border-radius: var(--border-radius);
        font-size: 1.2rem;
        z-index: 1;
        box-sizing: border-box;
        transition: transform 0.2s;
    }

    .block:active { cursor: grabbing; transform: scale(0.98); }

    /* HEDEF İÇİNDEKİ PARÇALAR */
    .drop-zone .block {
        height: 100%;
        border-radius: 0; /* İçeridekiler birleşsin diye */
        border-top: none;
        border-bottom: none;
        cursor: default;
    }

    /* RENK PALETİ (Yüklediğin görsellere göre) */
    .c1 { background-color: #ff9ff3; width: 100%; }   /* 1 */
    .c2 { background-color: #d980fa; width: 50%; }   /* 1/2 */
    .c3 { background-color: #a29bfe; width: 33.33%; } /* 1/3 */
    .c4 { background-color: #74b9ff; width: 25%; }   /* 1/4 */
    .c5 { background-color: #81ecec; width: 20%; }   /* 1/5 */

    /* TEMİZLE BUTONU */
    .reset-area {
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
    }
    .btn-reset {
        padding: 8px 20px;
        background-color: #34495e;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
        transition: background 0.3s;
    }
    .btn-reset:hover { background-color: #2c3e50; }
</style>
</head>
<body>

    <div class="main-container">
        
        <div class="reset-area">
            <button class="btn-reset" onclick="resetAll()">Temizle ve Yeniden Başla</button>
        </div>

        <div id="target" class="drop-zone" ondrop="drop(event)" ondragover="allowDrop(event)">
            <div class="target-label">1</div>
        </div>

        <div class="fraction-wall">
            <div class="row">
                <div class="block c1" draggable="true" ondragstart="drag(event)" data-val="1">1</div>
            </div>
            <div class="row">
                <div class="block c2" draggable="true" ondragstart="drag(event)" data-val="0.5">1/2</div>
                <div class="block c2" draggable="true" ondragstart="drag(event)" data-val="0.5">1/2</div>
            </div>
            <div class="row">
                <div class="block c3" draggable="true" ondragstart="drag(event)" data-val="0.3333">1/3</div>
                <div class="block c3" draggable="true" ondragstart="drag(event)" data-val="0.3333">1/3</div>
                <div class="block c3" draggable="true" ondragstart="drag(event)" data-val="0.3333">1/3</div>
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

    function allowDrop(ev) { ev.preventDefault(); }

    function drag(ev) {
        ev.dataTransfer.setData("className", ev.target.className); 
        ev.dataTransfer.setData("content", ev.target.innerText);
        ev.dataTransfer.setData("val", ev.target.getAttribute("data-val"));
    }

    function drop(ev) {
        ev.preventDefault();
        const val = parseFloat(ev.dataTransfer.getData("val"));
        
        // Hassas matematiksel kontrol (floating point hatasını engellemek için)
        if (currentSum + val > 1.001) {
            return; // 1'i aşarsa ekleme
        }

        const className = ev.dataTransfer.getData("className");
        const content = ev.dataTransfer.getData("content");
        
        const node = document.createElement("div");
        node.className = className;
        node.innerText = content;
        
        document.getElementById("target").appendChild(node);
        currentSum += val;

        if (currentSum >= 0.99) {
            confetti({
                particleCount: 100,
                spread: 70,
                origin: { y: 0.6 }
            });
            document.getElementById("target").classList.add("completed");
        }
    }

    function resetAll() {
        document.getElementById("target").innerHTML = '<div class="target-label">1</div>';
        document.getElementById("target").classList.remove("completed");
        currentSum = 0;
    }
</script>

</body>
</html>
"""

# HTML bileşenini yükle
components.html(html_code, height=650, scrolling=False)
