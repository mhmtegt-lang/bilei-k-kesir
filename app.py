import streamlit as st
import streamlit.components.v1 as components

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Otomatik Kesir Modelleme", layout="wide")

st.markdown("<h2 style='text-align: center; color: #2c3e50;'>📏 Otomatik Sayı Doğrusu Modeli</h2>", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Ayarlar")
    selected_option = st.radio("Birim Kesir Seçin:", ["1/2", "1/3", "1/4", "1/5", "1/6"], index=1)
    denom = int(selected_option.split("/")[1])
    
    st.markdown("---")
    st.info("💡 **Nasıl Çalışır?**\nÜstteki mavi alana parçaları sürükledikçe, alt tarafta '1 TAM' ve kalan parçalar otomatik olarak hizalanır.")
    
    if st.button("🔄 Ekranı Sıfırla"):
        st.rerun()

# --- HTML/CSS/JS KODU ---
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
<style>
    :root {{
        --line-color: #0984e3;
        --block-height: 50px;
        --max-width: 850px;
    }}

    body {{ 
        font-family: 'Segoe UI', sans-serif; 
        background-color: #f8f9fa; 
        display: flex; flex-direction: column; align-items: center; 
        padding: 10px; user-select: none;
    }}
    
    .workspace {{
        width: 100%; max-width: var(--max-width);
        background: white; border-radius: 20px; padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        display: flex; flex-direction: column; gap: 0;
    }}

    /* ÜST DROP ZONE */
    .zone-top {{
        width: 100%; height: 70px;
        display: flex; align-items: flex-end;
        border-bottom: 2px solid var(--line-color);
        position: relative;
    }}

    /* SAYI VE ÇİZGİ KATMANI */
    .axis-layer {{
        width: 100%; height: 50px; position: relative;
    }}
    
    .tick {{ position: absolute; background-color: var(--line-color); transform: translateX(-50%); }}
    .tick.major {{ width: 4px; height: 15px; top: 0; }}
    .tick.minor {{ width: 2px; height: 8px; top: 0; opacity: 0.4; }}
    
    .label {{
        position: absolute; top: 18px; transform: translateX(-50%);
        font-weight: bold; font-size: 20px; color: var(--line-color);
    }}

    /* ALT OTOMATİK ZONE */
    .zone-bottom {{
        width: 100%; height: 70px;
        display: flex; align-items: flex-start;
        padding-top: 5px;
    }}

    /* BLOK STİLLERİ */
    .block {{
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; color: white; border: 1px solid rgba(0,0,0,0.1);
        cursor: grab; border-radius: 4px; font-size: 1rem;
        box-sizing: border-box; height: var(--block-height);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }}

    /* Üsttekiler */
    .zone-top .block {{ border-bottom: none; border-radius: 6px 6px 0 0; }}
    
    /* Alttakiler */
    .zone-bottom .block {{ border-top: none; border-radius: 0 0 6px 6px; }}

    /* RENKLER */
    .pink-1 {{ background-color: #ff9ff3; color: #2d3436; }}
    .c2 {{ background-color: #cd84f1; }}
    .c3 {{ background-color: #7d5fff; }}
    .c4 {{ background-color: #74b9ff; }}
    .c5 {{ background-color: #81ecec; color: #2d3436; }}
    .c6 {{ background-color: #55efc4; color: #2d3436; }}

    /* HAVUZ */
    .pool {{
        display: flex; gap: 15px; justify-content: center;
        padding: 20px; margin-top: 20px; background: #f1f2f6; border-radius: 12px;
    }}
</style>
</head>
<body>

    <div class="workspace">
        <div id="target-top" class="zone-top" ondrop="drop(event)" ondragover="allowDrop(event)"></div>

        <div class="axis-layer" id="axis"></div>

        <div id="target-bottom" class="zone-bottom"></div>
    </div>

    <div style="margin-top:20px; font-size:12px; color:#aaa;">PARÇA HAVUZU</div>
    <div class="pool">
        <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}" style="width: 100px;">1/{denom}</div>
        <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}" style="width: 100px;">1/{denom}</div>
        <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}" style="width: 100px;">1/{denom}</div>
    </div>

<script>
    const denom = {denom};
    let currentSum = 0;

    // --- EKSEN ÇİZİMİ ---
    function drawAxis() {{
        const axis = document.getElementById('axis');
        const totalSubTicks = denom * 2;
        for(let i=0; i<=totalSubTicks; i++) {{
            let pos = (i / totalSubTicks) * 100;
            let isMajor = (i % denom === 0);
            if(isMajor) {{
                axis.innerHTML += `<div class="tick major" style="left: ${{pos}}%"></div>`;
                axis.innerHTML += `<div class="label" style="left: ${{pos}}%">${{i/denom}}</div>`;
            }} else {{
                axis.innerHTML += `<div class="tick minor" style="left: ${{pos}}%"></div>`;
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

    function drop(ev) {{
        ev.preventDefault();
        const val = parseFloat(ev.dataTransfer.getData("val"));
        if (currentSum + val > 2.01) return;

        // ÜST BÖLGEYE EKLE
        const node = document.createElement("div");
        node.className = ev.dataTransfer.getData("className");
        node.innerText = ev.dataTransfer.getData("content");
        node.style.width = (val / 2 * 100) + "%";
        document.getElementById("target-top").appendChild(node);
        
        currentSum += val;
        updateBottomModel();

        if (Math.abs(currentSum - 1.0) < 0.01) {{
            confetti({{ particleCount: 100, spread: 70, origin: {{ y: 0.6 }} }});
        }}
    }}

    // --- OTOMATİK ALT MODELLEME ---
    function updateBottomModel() {{
        const bottom = document.getElementById("target-bottom");
        bottom.innerHTML = ""; // Temizle

        if (currentSum >= 0.99) {{
            // 1 TAM BLOĞU EKLE
            const full = document.createElement("div");
            full.className = "block pink-1";
            full.innerText = "1 TAM";
            full.style.width = "50%"; // 0-2 aralığında yarısı
            bottom.appendChild(full);

            // KALAN PARÇAYI EKLE
            let remainder = currentSum - 1.0;
            if (remainder > 0.01) {{
                const remNode = document.createElement("div");
                remNode.className = "block c" + denom;
                // Örn: 1/3
                remNode.innerText = "1/" + denom;
                remNode.style.width = (remainder / 2 * 100) + "%";
                bottom.appendChild(remNode);
            }}
        }}
    }}
</script>
</body>
</html>
"""

components.html(html_code, height=600)
