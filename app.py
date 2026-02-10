import streamlit as st
import streamlit.components.v1 as components

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="İnteraktif Kesir Duvarı", layout="wide")

st.title("🧩 Kesir Duvarı: Sürükle ve Bırak")
st.markdown("""
Aşağıdaki renkli kesir bloklarını **mouse ile tutup** en üstteki **"HEDEF: 1 TAM"** kutusunun içine sürükleyin.
Parçaların bütünü nasıl oluşturduğunu gözlemleyin. (Örn: 3 tane 1/3'ü yan yana dizin)
""")

# --- HTML/CSS/JS KODU (GÖMÜLÜ ARAYÜZ) ---
# Bu blok, Streamlit'in yapamadığı "Sürükle-Bırak" işlemini tarayıcıda yapar.
html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
    body { font-family: sans-serif; user-select: none; }
    
    /* HEDEF ALAN (DROP ZONE) */
    .drop-zone {
        width: 100%;
        max-width: 800px;
        height: 80px;
        border: 3px dashed #333;
        background-color: #f0f2f6;
        margin: 20px auto;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        padding: 5px;
        box-sizing: border-box;
        border-radius: 10px;
        position: relative;
    }
    
    .drop-zone::before {
        content: "HEDEF ALAN (Buraya Bırak)";
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: #aaa;
        font-weight: bold;
        z-index: 0;
    }

    /* KESİR DUVARI (KAYNAK) */
    .fraction-wall {
        display: flex;
        flex-direction: column;
        width: 100%;
        max-width: 800px;
        margin: 0 auto;
        gap: 5px;
    }

    .row {
        display: flex;
        width: 100%;
        height: 60px;
        gap: 2px;
    }

    /* GENEL KUTU STİLİ */
    .block {
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: black;
        border: 1px solid rgba(0,0,0,0.2);
        cursor: grab;
        border-radius: 4px;
        font-size: 1.2rem;
        z-index: 1; /* Yazının üstte kalması için */
        transition: transform 0.1s;
    }

    .block:active {
        cursor: grabbing;
        transform: scale(0.98);
    }

    /* GÖRSELDEKİ RENKLER */
    .full { background-color: #ff9ff3; width: 100%; }       /* 1 Tam - Pembe */
    .half { background-color: #c8a2c8; width: 50%; }         /* 1/2 - Lila */
    .third { background-color: #a29bfe; width: 33.33%; }     /* 1/3 - Morumsu */
    .quarter { background-color: #74b9ff; width: 25%; }      /* 1/4 - Mavi */
    .fifth { background-color: #81ecec; width: 20%; }        /* 1/5 - Turkuaz */
    .sixth { background-color: #55efc4; width: 16.66%; }     /* 1/6 - Yeşil */

    /* SİLME BUTONU */
    .reset-btn {
        display: block;
        margin: 10px auto;
        padding: 10px 20px;
        background-color: #ff7675;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1rem;
    }
    .reset-btn:hover { background-color: #d63031; }

</style>
</head>
<body>

    <div id="target" class="drop-zone" ondrop="drop(event)" ondragover="allowDrop(event)"></div>
    
    <button class="reset-btn" onclick="resetTarget()">Alanı Temizle</button>

    <div class="fraction-wall">
        <div class="row">
            <div class="block half" draggable="true" ondragstart="drag(event)" data-val="1/2">1/2</div>
            <div class="block half" draggable="true" ondragstart="drag(event)" data-val="1/2">1/2</div>
        </div>
        <div class="row">
            <div class="block third" draggable="true" ondragstart="drag(event)" data-val="1/3">1/3</div>
            <div class="block third" draggable="true" ondragstart="drag(event)" data-val="1/3">1/3</div>
            <div class="block third" draggable="true" ondragstart="drag(event)" data-val="1/3">1/3</div>
        </div>
        <div class="row">
            <div class="block quarter" draggable="true" ondragstart="drag(event)" data-val="1/4">1/4</div>
            <div class="block quarter" draggable="true" ondragstart="drag(event)" data-val="1/4">1/4</div>
            <div class="block quarter" draggable="true" ondragstart="drag(event)" data-val="1/4">1/4</div>
            <div class="block quarter" draggable="true" ondragstart="drag(event)" data-val="1/4">1/4</div>
        </div>
        <div class="row">
            <div class="block fifth" draggable="true" ondragstart="drag(event)" data-val="1/5">1/5</div>
            <div class="block fifth" draggable="true" ondragstart="drag(event)" data-val="1/5">1/5</div>
            <div class="block fifth" draggable="true" ondragstart="drag(event)" data-val="1/5">1/5</div>
            <div class="block fifth" draggable="true" ondragstart="drag(event)" data-val="1/5">1/5</div>
            <div class="block fifth" draggable="true" ondragstart="drag(event)" data-val="1/5">1/5</div>
        </div>
        <div class="row">
            <div class="block sixth" draggable="true" ondragstart="drag(event)" data-val="1/6">1/6</div>
            <div class="block sixth" draggable="true" ondragstart="drag(event)" data-val="1/6">1/6</div>
            <div class="block sixth" draggable="true" ondragstart="drag(event)" data-val="1/6">1/6</div>
            <div class="block sixth" draggable="true" ondragstart="drag(event)" data-val="1/6">1/6</div>
            <div class="block sixth" draggable="true" ondragstart="drag(event)" data-val="1/6">1/6</div>
            <div class="block sixth" draggable="true" ondragstart="drag(event)" data-val="1/6">1/6</div>
        </div>
    </div>

<script>
    function allowDrop(ev) {
        ev.preventDefault();
    }

    function drag(ev) {
        // Sürüklenen elementin özelliklerini kopyalamak için veri setini alıyoruz
        // Orijinal elementi taşımıyoruz, kopyasını oluşturacağız (cloning)
        ev.dataTransfer.setData("text", ev.target.className); 
        ev.dataTransfer.setData("content", ev.target.innerText);
    }

    function drop(ev) {
        ev.preventDefault();
        
        // Sadece target alanına bırakmaya izin ver
        if (ev.target.id !== "target" && ev.target.parentNode.id !== "target") return;

        var className = ev.dataTransfer.getData("text");
        var content = ev.dataTransfer.getData("content");
        
        // Yeni bir element oluştur (Kopyalama mantığı)
        var node = document.createElement("div");
        node.className = className;
        node.innerText = content;
        
        // Kopyanın draggable özelliğini kaldırıyoruz (tekrar sürüklenmesin)
        node.draggable = false;
        node.style.cursor = "default";
        
        // Hedef alana ekle
        document.getElementById("target").appendChild(node);
    }

    function resetTarget() {
        document.getElementById("target").innerHTML = "";
    }
</script>

</body>
</html>
"""

# HTML Kodunu Streamlit içinde çalıştır
components.html(html_code, height=600, scrolling=False)

st.info("💡 **İpucu:** Örneğin 2 tane 1/4 bloğu ile 1 tane 1/2 bloğunun aynı boyutta olduğunu görmek için yan yana koymayı dene!")
