import streamlit as st
import streamlit.components.v1 as components

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Kesir Laboratuvarı", layout="wide")

st.markdown("<h3 style='text-align: center; color: #2c3e50;'>📏 Sayı Doğrusu: Çift Taraflı Modelleme</h3>", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Ayarlar")
    selected_option = st.radio("Birim Parça Seçin:", ["1/2", "1/3", "1/4", "1/5", "1/6"], index=1)
    denom = int(selected_option.split("/")[1])
    
    st.markdown("---")
    st.info("💡 **Nasıl Kullanılır?**\n'1 TAM' bloğunu veya parçaları çizginin **hem üstüne hem de altına** sürükleyebilirsiniz. Bütünün sağ tarafına parça ekleyerek bileşik kesirleri modelleyebilirsiniz.")
    
    if st.button("🔄 Ekranı Sıfırla"):
        st.rerun()

# --- HTML/CSS/JS KODU (Hata Düzeltilmiş Versiyon) ---
# F-string içindeki tüm CSS ve JS parantezleri {{ }} şeklinde çiftlenmiştir.
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
<style>
    :root {{
        --line-color: #0984e3;
        --zone-height: 80px;
        --max-width: 900px;
    }}

    body {{ 
        font-family: 'Segoe UI', sans-serif; 
        background-color: #f8f9fa; 
        display: flex; flex-direction: column; align-items: center; 
        padding: 20px; user-select: none;
    }}
    
    .main-wrapper {{
        width: 100%; max-width: var(--max-width);
        display: flex; flex-direction: column; gap: 10px;
    }}

    .number-line-system {{
        background: white; border-radius: 15px; padding: 40px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        position: relative; display: flex; flex-direction: column;
    }}

    /* ÜST VE ALT DROP ZONE'LAR */
    .drop-zone {{
        width: 100%; height: var(--zone-height);
        display: flex; position: relative;
        box-sizing: border-box; transition: background 0.2s;
        border: 2px dashed transparent;
    }}
    .drop-zone:hover {{ background-color: rgba(9, 132, 227, 0.03); border-color: rgba(9, 132, 227, 0.2); }}

    .axis-container {{
        width: 100%; height: 2px; position: relative;
        background-color: var(--line-color);
        margin: 10px 0;
    }}

    .tick {{ position: absolute; background-color: var(--line-color); transform: translateX(-50%); }}
    .tick.major {{ width: 4px; height: 20px; top: -10px; }}
    .tick.minor {{ width: 2px; height: 10px; top: -5px; opacity: 0.5; }}
    .label {{ position: absolute; top: 15px; transform: translateX(-50%); font-weight: bold; font-size: 20px; color: #2d3436; }}

    /* OK UÇLARI */
    .axis-container::before {{ content: ''; position: absolute; top: -9px; left: -10px; border-width: 10px 15px 10px 0; border-color: transparent var(--line-color) transparent transparent; border-style: solid; }}
    .axis-container::after {{ content: ''; position: absolute; top: -9px; right: -10px; border-width: 10px 0 10px 15px; border-color: transparent transparent transparent var(--line-color); border-style: solid; }}

    /* BLOKLAR */
    .block {{
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; border: 1px solid rgba(0,0,0,0.1);
        cursor: grab; border-radius: 6px; font-size: 1.1rem;
        box-sizing: border-box; height: 60px;
    }}

    .drop-zone-top {{ align-items: flex-end; }}
    .drop-zone-top .block {{ border-radius: 6px 6px 0 0; border-bottom: none; }}

    .drop-zone-bottom {{ align-items: flex-start; }}
    .drop-zone-bottom .block {{ border-radius: 0 0 6px 6px; border-top: none; }}

    /* RENKLER */
    .pink-1 {{ background-color: #ff9ff3; color: #333; }}
    .frac-block {{ color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.3); }}
    .c2 {{ background-color: #cd84f1; }}
    .c3 {{ background-color: #7d5fff; }}
    .c4 {{ background-color: #74b9ff; }}
    .c5 {{ background-color: #81ecec; color: #333; }}
    .c6 {{ background-color: #55efc4; color: #333; }}

    .pool {{
        display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;
        background: white; padding: 20px; border-radius: 15px; margin-top: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }}
    .pool-section {{ display: flex; flex-direction: column; align-items: center; gap: 10px; }}
    .pool-title {{ font-size: 12px; color: #aaa; font-weight: bold; text-transform: uppercase; }}

</style>
</head>
<body>

<div class="main-wrapper">
    <div class="number-line-system">
        <div id="target-top" class="drop-zone drop-zone-top" ondrop="handleDrop(event)" ondragover="allowDrop(event)"></div>
        <div class="axis-container" id="axis"></div>
        <div id="target-bottom" class="drop-zone drop-zone-bottom" ondrop="handleDrop(event)" ondragover="allowDrop(event)"></div>
    </div>

    <div class="pool">
        <div class="pool-section">
            <div class="pool-title">Referans Blok</div>
            <div class="block pink-1" draggable="true" ondragstart="drag(event)" data-val="1" style="width: 200px;">1 TAM</div>
        </div>
        <div class="pool-section">
            <div class="pool-title">Parçalar (1/{denom})</div>
            <div style="display:flex; gap:8px;">
                <div class="block frac-block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}" style="width: 80px;">1/{denom}</div>
                <div class="block frac-block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}" style="width: 80px;">1/{denom}</div>
                <div class="block frac-block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}" style="width: 80px;">1/{denom}</div>
            </div>
        </div>
    </div>
</div>

<script>
    const denom = {denom};
    const MAX_VAL = 2.0;

    function initAxis() {{
        const axis = document.getElementById('axis');
        const subTicks = denom * 2;
        for(let i=0; i<=subTicks; i++) {{
            let pos = (i / subTicks) * 100;
            let isMajor = (i % denom === 0);
            if(isMajor) {{
                axis.innerHTML += `<div class="tick major" style="left: ${{pos}}%"></div>`;
                axis.innerHTML += `<div class="label" style="left: ${{pos}}%">${{i/denom}}</div>`;
            }} else {{
                axis.innerHTML += `<div class="tick minor" style="left: ${{pos}}%"></div>`;
            }}
        }}
    }}
    initAxis();

    function allowDrop(ev) {{ ev.preventDefault(); }}

    function drag(ev) {{
        ev.dataTransfer.setData("className", ev.target.className); 
        ev.dataTransfer.setData("content", ev.target.innerText);
        ev.dataTransfer.setData("val", ev.target.getAttribute("data-val"));
    }}

    function handleDrop(ev) {{
        ev.preventDefault();
        const zone = ev.currentTarget;
        
        const val = parseFloat(ev.dataTransfer.getData("val"));
        const className = ev.dataTransfer.getData("className");
        const content = ev.dataTransfer.getData("content");

        let sum = 0;
        zone.querySelectorAll('.block').forEach(b => {{
            sum += parseFloat(b.getAttribute('data-val'));
        }});
        
        if (sum + val > MAX_VAL + 0.01) {{
            return;
        }}

        const node = document.createElement("div");
        node.className = className;
        node.innerText = content;
        node.setAttribute('data-val', val);
        node.style.width = (val / MAX_VAL * 100) + "%";
        
        zone.appendChild(node);

        if (Math.abs((sum + val) - 1.0) < 0.01) {{
            confetti({{ particleCount: 100, spread: 70, origin: {{ y: 0.6 }} }});
        }}
    }}
</script>
</body>
</html>
"""

components.html(html_code, height=650)
