import streamlit as st
import streamlit.components.v1 as components

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Bileşik Kesir Modelleme", layout="wide")

st.markdown("<h2 style='text-align: center; color: #2c3e50;'>🧩 Sayı Doğrusunda Tam Sayılı Kesir Modeli</h2>", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Ayarlar")
    selected_option = st.radio("Birim Kesir Seçin:", ["1/2", "1/3", "1/4", "1/5", "1/6"], index=1)
    denom = int(selected_option.split("/")[1])
    
    st.markdown("---")
    st.info("💡 **Nasıl Kullanılır?**\n1. Üst bölgeye parçaları sürükleyerek doldurun.\n2. 1 Tam dolduğunda altta pembe blok otomatik çıkacaktır.\n3. 1 Tamın yanındaki boşluğa parçaları kendiniz sürükleyip bırakın.")
    
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
        --block-height: 55px;
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
        background: white; border-radius: 20px; padding: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        display: flex; flex-direction: column; gap: 0;
    }}

    /* ÜST DROP ZONE */
    .zone-top {{
        width: 100%; height: 75px;
        display: flex; align-items: flex-end;
        border-bottom: 2px solid var(--line-color);
        position: relative;
    }}

    /* ORTA KATMAN (RAKAMLAR VE ÇİZGİLER) */
    .axis-layer {{
        width: 100%; height: 50px; position: relative;
    }}
    
    .tick {{ position: absolute; background-color: var(--line-color); transform: translateX(-50%); }}
    .tick.major {{ width: 4px; height: 18px; top: 0; }}
    .tick.minor {{ width: 2px; height: 10px; top: 0; opacity: 0.4; }}
    
    .label {{
        position: absolute; top: 22px; transform: translateX(-50%);
        font-weight: bold; font-size: 22px; color: var(--line-color);
    }}

    /* ALT DROP ZONE (OTOMATİK + MANUEL) */
    .zone-bottom {{
        width: 100%; height: 75px;
        display: flex; align-items: flex-start;
        padding-top: 5px;
        position: relative;
        border-top: 2px solid #dfe6e9;
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
        <div id="target-top" class="zone-top" ondrop="dropTop(event)" ondragover="allowDrop(event)"></div>

        <div class="axis-layer" id="axis"></div>

        <div id="target-bottom" class="zone-bottom" ondrop="dropBottom(event)" ondragover="allowDrop(event)"></div>
    </div>

    <div style="margin-top:20px; font-size:12px; color:#aaa; font-weight:bold;">PARÇA HAVUZU</div>
    <div class="pool">
        <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}" style="width: 100px;">1/{denom}</div>
        <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}" style="width: 100px;">1/{denom}</div>
        <div class="block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}" style="width: 100px;">1/{denom}</div>
    </div>

<script>
    const denom = {denom};
    let topSum = 0;
    let bottomSum = 0;
    const MAX_VAL = 2.0;

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

    function allowDrop(ev) {{ ev.preventDefault(); }}

    function drag(ev) {{
        ev.dataTransfer.setData("className", ev.target.className); 
        ev.dataTransfer.setData("content", ev.target.innerText);
        ev.dataTransfer.setData("val", ev.target.getAttribute("data-val"));
    }}

    // --- ÜST BÖLGE BIRAKMA ---
    function dropTop(ev) {{
        ev.preventDefault();
        const val = parseFloat(ev.dataTransfer.getData("val"));
        if (topSum + val > MAX_VAL + 0.01) return;

        const node = createBlock(ev);
        document.getElementById("target-top").appendChild(node);
        topSum += val;

        checkAutoWhole();
    }}

    // --- ALT BÖLGE BIRAKMA ---
    function dropBottom(ev) {{
        ev.preventDefault();
        const val = parseFloat(ev.dataTransfer.getData("val"));
        if (bottomSum + val > MAX_VAL + 0.01) return;

        const node = createBlock(ev);
        document.getElementById("target-bottom").appendChild(node);
        bottomSum += val;
    }}

    function createBlock(ev) {{
        const val = parseFloat(ev.dataTransfer.getData("val"));
        const node = document.createElement("div");
        node.className = ev.dataTransfer.getData("className");
        node.innerText = ev.dataTransfer.getData("content");
        node.style.width = (val / MAX_VAL * 100) + "%";
        node.setAttribute('data-val', val);
        return node;
    }}

    // --- OTOMATİK 1 TAM KONTROLÜ ---
    function checkAutoWhole() {{
        const bottomZone = document.getElementById("target-bottom");
        const hasWhole = document.getElementById("auto-whole");

        if (topSum >= 0.99 && !hasWhole) {{
            const full = document.createElement("div");
            full.id = "auto-whole";
            full.className = "block pink-1";
            full.innerText = "1 TAM";
            full.style.width = "50%"; // 0-2 aralığında %50 genişlik
            full.setAttribute('data-val', 1.0);
            
            // Mevcut manuel eklenenlerden önce (en sola) ekle
            bottomZone.prepend(full);
            bottomSum += 1.0;

            confetti({{ particleCount: 100, spread: 70, origin: {{ y: 0.6 }} }});
        }}
    }}
</script>
</body>
</html>
"""

components.html(html_code, height=650)
