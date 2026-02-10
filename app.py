import streamlit as st
import streamlit.components.v1 as components

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Kesirleri Tamamla", layout="wide")

st.title("🧩 Kesirleri Birleştir: 1 Tamı Oluştur")
st.markdown("""
Aşağıdaki birim kesirleri tutup **yukarıdaki çerçeveye** taşıyın. 
Parçalar birleştiğinde **1** bütünün nasıl oluştuğunu göreceksiniz.
""")

# --- HTML/CSS/JS KODU ---
html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; user-select: none; background-color: #f8f9fa; }
    
    /* ANA ÇERÇEVE (1 TAM) */
    .container-title {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 5px;
        color: #333;
    }

    .drop-zone {
        width: 100%;
        max-width: 800px;
        height: 100px;
        border: 4px solid #333;
        background-color: #ffffff;
        margin: 0 auto 20px auto;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        position: relative;
        overflow: hidden;
        border-radius: 8px;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* ARKA PLANDAKİ '1' YAZISI */
    .bg-label {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 60px;
        font-weight: bold;
        color: rgba(0, 0, 0, 0.05);
        z-index: 0;
    }

    /* KESİR DUVARI */
    .fraction-wall {
        display: flex;
        flex-direction: column;
        width: 100%;
        max-width: 800px;
        margin: 20px auto;
        gap: 8px;
    }

    .row {
        display: flex;
        width: 100%;
        height: 60px;
        gap: 4px;
    }

    /* BLOK STİLLERİ (Görseldeki renklerle aynı) */
    .block {
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: #333;
        border: 2px solid rgba(0,0,0,0.15);
        cursor: grab;
        border-radius: 4px;
        font-size: 1.1rem;
        z-index: 1;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .block:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    .block:active { cursor: grabbing; }

    /* RENK TANIMLARI */
    .p1 { background-color: #ff9ff3; width: 100%; }   /* 1 Tam */
    .p2 { background-color: #d980fa; width: 50%; }   /* 1/2 */
    .p3 { background-color: #a29bfe; width: 33.33%; } /* 1/3 */
    .p4 { background-color: #74b9ff; width: 25%; }   /* 1/4 */
    .p5 { background-color: #81ecec; width: 20%; }   /* 1/5 */
    .p6 { background-color: #55efc4; width: 16.66%; } /* 1/6 */

    /* HEDEF ALAN İÇİNDEKİ PARÇALAR */
    .drop-zone .block {
        height: 100%;
        border-radius: 0;
        border-top: none;
        border-bottom: none;
        cursor: default;
    }

    .controls { text-align: center; margin-top: 10px; }
    .btn {
        padding: 10px 25px;
        background-color: #2d3436;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
    }
    .btn:hover { background-color: #000; }

</style>
</head>
<body>

    <div class="container-title">1 TAM</div>
    <div id="target" class="drop-zone" ondrop="drop(event)" ondragover="allowDrop(event)">
        <div class="bg-label">1</div>
    </div>
    
    <div class="controls">
        <button class="btn" onclick="resetTarget()">Temizle ve Yeniden Başla</button>
    </div>

    <div class="fraction-wall">
        <div class="row"><div class="block p1" draggable="true" ondragstart="drag(event)" data-val="1">1</div></div>
        <div class="row">
            <div class="block p2" draggable="true" ondragstart="drag(event)" data-val="1/2">1/2</div>
            <div class="block p2" draggable="true" ondragstart="drag(event)" data-val="1/2">1/2</div>
        </div>
        <div class="row">
            <div class="block p3" draggable="true" ondragstart="drag(event)" data-val="1/3">1/3</div>
            <div class="block p3" draggable="true" ondragstart="drag(event)" data-val="1/3">1/3</div>
            <div class="block p3" draggable="true" ondragstart="drag(event)" data-val="1/3">1/3</div>
        </div>
        <div class="row">
            <div class="block p4" draggable="true" ondragstart="drag(event)" data-val="1/4">1/4</div>
            <div class="block p4" draggable="true" ondragstart="drag(event)" data-val="1/4">1/4</div>
            <div class="block p4" draggable="true" ondragstart="drag(event)" data-val="1/4">1/4</div>
            <div class="block p4" draggable="true" ondragstart="drag(event)" data-val="1/4">1/4</div>
        </div>
        <div class="row">
            <div class="block p5" draggable="true" ondragstart="drag(event)" data-val="1/5">1/5</div>
            <div class="block p5" draggable="true" ondragstart="drag(event)" data-val="1/5">1/5</div>
            <div class="block p5" draggable="true" ondragstart="drag(event)" data-val="1/5">1/5</div>
            <div class="block p5" draggable="true" ondragstart="drag(event)" data-val="1/5">1/5</div>
            <div class="block p5" draggable="true" ondragstart="drag(event)" data-val="1/5">1/5</div>
        </div>
    </div>

<script>
    function allowDrop(ev) { ev.preventDefault(); }

    function drag(ev) {
        ev.dataTransfer.setData("className", ev.target.className); 
        ev.dataTransfer.setData("content", ev.target.innerText);
    }

    function drop(ev) {
        ev.preventDefault();
        var target = document.getElementById("target");
        
        // Mevcut doluluk oranını kontrol et (Basit genişlik hesabı)
        var currentWidth = 0;
        target.querySelectorAll('.block').forEach(el => {
            currentWidth += el.getBoundingClientRect().width;
        });

        if (currentWidth >= target.offsetWidth - 5) {
            alert("1 Tam doldu!");
            return;
        }

        var className = ev.dataTransfer.getData("className");
        var content = ev.dataTransfer.getData("content");
        
        var node = document.createElement("div");
        node.className = className;
        node.innerText = content;
        node.draggable = false;
        
        target.appendChild(node);
    }

    function resetTarget() {
        const target = document.getElementById("target");
        target.innerHTML = '<div class="bg-label">1</div>';
    }
</script>

</body>
</html>
"""

# Komponenti Yükle
components.html(html_code, height=750, scrolling=False)
