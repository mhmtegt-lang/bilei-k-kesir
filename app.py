import streamlit as st
import streamlit.components.v1 as components

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Kesir Laboratuvarı", layout="wide")

st.markdown("<h3 style='text-align: center; color: #2c3e50;'>📏 Sayı Doğrusu Laboratuvarı: Bileşik ve Tam Sayılı Kesirler</h3>", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Ayarlar")
    selected_option = st.radio("Birim Parça Seçin:", ["1/2", "1/3", "1/4", "1/5", "1/6"], index=1)
    denom = int(selected_option.split("/")[1])
    
    st.markdown("---")
    st.warning("💡 **İpucu:** '1 TAM' bloğunu sayı doğrusunun altına koyup, yanına 1/{denom} ekleyerek denklik modelini oluşturabilirsiniz.")
    
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

    /* --- SAYI DOĞRUSU SİSTEMİ --- */
    .number-line-system {{
        background: white; border-radius: 15px; padding: 30px;
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
    .drop-zone:hover {{ background-color: rgba(9, 132, 227, 0.05); border-color: #0984e3; }}

    /* Sayı doğrusu çizgisinin olduğu orta alan */
    .axis-container {{
        width: 100%; height: 60px; position: relative;
        border-top: 4px solid var(--line-color);
        margin: 5px 0;
    }}

    /* Çentikler ve Rakamlar */
    .tick {{ position: absolute; background-color: var(--line-color); transform: translateX(-50%); }}
    .tick.major {{ width: 4px; height: 20px; top: -12px; }}
    .tick.minor {{ width: 2px; height: 10px; top: -7px; opacity: 0.5; }}
    .label {{ position: absolute; top: 15px; transform: translateX(-50%); font-weight: bold; font-size: 20px; color: #2d3436; }}

    /* OK UÇLARI */
    .axis-container::before {{ content: ''; position: absolute; top: -11px; left: -10px; border-width: 8px 12px 8px 0; border-color: transparent var(--line-color) transparent transparent; border-style: solid; }}
    .axis-container::after {{ content: ''; position: absolute; top: -11px; right: -10px; border-width: 8px 0 8px 12px; border-color: transparent transparent transparent var(--line-color); border-style: solid; }}

    /* --- BLOKLARIN GÖRÜNÜMÜ --- */
    .block {{
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; border: 1px solid rgba(0,0,0,0.1);
        cursor: grab; border-radius: 6px; font-size: 1.1rem;
        box-sizing: border-box; transition: transform 0.1s;
    }}
    .block:active {{ transform: scale(0.95); cursor: grabbing; }}

    /* Üsttekiler çizgiye yaslansın */
    .drop-zone-top {{ align-items: flex-end; }}
    .drop-zone-top .block {{ border-radius: 6px 6px 0 0; border-bottom: none; height: 60px; }}

    /* Alttakiler çizgiye asılsın */
    .drop-zone-bottom {{ align-items: flex-start; }}
    .drop-zone-bottom .block {{ border-radius: 0 0 6px 6px; border-top: none; height: 60px; }}

    /* RENKLER */
    .pink-1 {{ background-color: #ff9ff3; width: 50%; color: #333; }} /* 1 Tam (0-2 aralığında %50 genişlik) */
    .frac-block {{ color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.3); }}
    .c2 {{ background-color: #cd84f1; }}
    .c3 {{ background-color: #7d5fff; }}
    .c4 {{ background-color: #74b9ff; }}
    .c5 {{ background-color: #81ecec; color: #333; }}
    .c6 {{ background-color: #55efc4; color: #333; }}

    /* HAVUZ ALANI */
    .pool {{
        display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;
        background: white; padding: 20px; border-radius: 15px; margin-top: 20px;
    }}
    .pool-section {{ display: flex; flex-direction: column; align-items: center; gap: 5px; }}
    .pool-title {{ font-size: 12px; color: #aaa; font-weight: bold; }}

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
            <div class="pool-title">REFERANS</div>
            <div class="block pink-1" draggable="true" ondragstart="drag(event)" data-val="1">1 TAM</div>
        </div>
        <div class="pool-section">
            <div class="pool-title">KESİR PARÇALARI (1/{denom})</div>
            <div style="display:flex; gap:5px;">
                <div class="block frac-block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}" style="width: calc(100% / {denom} / 2)">1/{denom}</div>
                <div class="block frac-block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}" style="width: calc(100% / {denom} / 2)">1/{denom}</div>
                <div class="block frac-block c{denom}" draggable="true" ondragstart="drag(event)" data-val="{1/denom:.5f}" style="width: calc(100% / {denom} / 2)">1/{denom}</div>
            </div>
        </div>
    </div>
    <div style="text-align: center; color: #aaa; font-size: 12px; margin-top: 10px;">
        * Parçaları istediğiniz bölgeye (çizginin üstü veya altı) sürükleyebilirsiniz. Sınırsız sayıda parça mevcuttur.
    </div>
</div>

<script>
    const denom = {denom};
    const MAX_VAL = 2.0;

    // --- EKSEN ÇİZİMİ ---
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

    // --- SÜRÜKLE BIRAK ---
    function allowDrop(ev) {{ ev.preventDefault(); }}

    function drag(ev) {{
        ev.dataTransfer.setData("className", ev.target.className); 
        ev.dataTransfer.setData("content", ev.target.innerText);
        ev.dataTransfer.setData("val", ev.target.getAttribute("data-val"));
    }}

    function handleDrop(ev) {{
        ev.preventDefault();
        // Hangi bölgeye bırakıldığını 'currentTarget' ile kesinleştiriyoruz
        const zone = ev.currentTarget;
        
        const val = parseFloat(ev.dataTransfer.getData("val"));
        const className = ev.dataTransfer.getData("className");
        const content = ev.dataTransfer.getData("content");

        // Bölgedeki mevcut doluluğu kontrol et (Görsel taşmayı önlemek için basit kontrol)
        let sum = 0;
        zone.querySelectorAll('.block').forEach(b => {{
            sum += parseFloat(b.getAttribute('data-val'));
        }});
        
        if (sum + val > MAX_VAL + 0.01) {{
            alert("Bu bölge doldu (Maksimum 2 tam)!");
            return;
        }

        // Yeni bloğu oluştur ve ekle
        const node = document.createElement("div");
        node.className = className;
        node.innerText = content;
        node.setAttribute('data-val', val);
        
        // Genişlik hesabı: 0-2 aralığı olduğu için değeri 2'ye bölüp yüzdeye çeviriyoruz
        node.style.width = (val / MAX_VAL * 100) + "%";
        
        zone.appendChild(node);

        // Tam sayıya ulaşınca kutlama
        if (Math.abs((sum + val) - 1.0) < 0.01 || Math.abs((sum + val) - 2.0) < 0.01) {{
            confetti({{ particleCount: 100, spread: 70, origin: {{ y: 0.6 }} }});
        }}
    }}
</script>
</body>
</html>
"""

components.html(html_code, height=650)
