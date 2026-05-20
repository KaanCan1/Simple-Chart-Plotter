import os

import streamlit as st
from PIL import Image

from main import generate_charts

st.set_page_config(
    page_title="TGSS 2024 — Grafik Paneli",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Stil ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;600;700&family=IBM+Plex+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: #0F1117;
    color: #E8EAF0;
}

/* Başlık alanı */
.hero {
    background: linear-gradient(135deg, #12151F 0%, #1A2035 60%, #0F1117 100%);
    border: 1px solid #2A2D3A;
    border-radius: 12px;
    padding: 2rem 2.4rem 1.6rem;
    margin-bottom: 1.6rem;
}
.hero h1 {
    font-size: 1.9rem;
    font-weight: 700;
    color: #E8EAF0;
    margin: 0 0 0.35rem;
    letter-spacing: -0.5px;
}
.hero p {
    font-size: 0.88rem;
    color: #6B7280;
    margin: 0;
    line-height: 1.5;
}
.hero .accent { color: #4F8EF7; }

/* İstatistik kartları */
.stat-row { display: flex; gap: 0.9rem; margin-bottom: 1.4rem; flex-wrap: wrap; }
.stat-card {
    flex: 1; min-width: 130px;
    background: #1A1D27;
    border: 1px solid #2A2D3A;
    border-radius: 10px;
    padding: 1rem 1.2rem;
}
.stat-card .val {
    font-size: 1.55rem;
    font-weight: 700;
    color: #4F8EF7;
    font-family: 'IBM Plex Mono', monospace;
    line-height: 1;
}
.stat-card .lbl {
    font-size: 0.75rem;
    color: #6B7280;
    margin-top: 0.3rem;
    font-weight: 400;
}

/* Grafik kartı */
.chart-card {
    background: #1A1D27;
    border: 1px solid #2A2D3A;
    border-radius: 10px;
    padding: 0;
    overflow: hidden;
    margin-bottom: 1rem;
}
.chart-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #6B7280;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 0.75rem 1rem 0;
}

/* Bölüm başlıkları */
.section-title {
    font-size: 0.7rem;
    font-weight: 700;
    color: #4F8EF7;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 1.6rem 0 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #2A2D3A;
}

/* Buton */
.stButton > button {
    background: #4F8EF7 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.55rem 1.8rem !important;
    transition: background 0.2s !important;
}
.stButton > button:hover { background: #3A78E8 !important; }

/* Info/success kutuları */
.stAlert { border-radius: 8px !important; }

/* Divider */
hr { border-color: #2A2D3A !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>TGSS 2024 <span class="accent">·</span> Grafik Paneli</h1>
  <p>Türkiye Genel Sosyal Saha Araştırması &nbsp;|&nbsp; n = 2.615 katılımcı
  &nbsp;|&nbsp; Saha dönemi: 17 Mayıs – 2 Haziran 2024</p>
</div>
""", unsafe_allow_html=True)

# ── Özet istatistikler ────────────────────────────────────────────────────────
st.markdown("""
<div class="stat-row">
  <div class="stat-card"><div class="val">2.615</div><div class="lbl">Katılımcı</div></div>
  <div class="stat-card"><div class="val">3.52</div><div class="lbl">Ort. Mutluluk (1–5)</div></div>
  <div class="stat-card"><div class="val">3.40</div><div class="lbl">Yaşam Memnuniyeti</div></div>
  <div class="stat-card"><div class="val">9.20</div><div class="lbl">Enflasyon Tehdit Skoru</div></div>
  <div class="stat-card"><div class="val">9.17</div><div class="lbl">Kadına Şiddet Skoru</div></div>
  <div class="stat-card"><div class="val">%59</div><div class="lbl">Evli Katılımcı</div></div>
</div>
""", unsafe_allow_html=True)

# ── Grafik üretme butonu ──────────────────────────────────────────────────────
OUTPUT_DIR = "outputs"

col_btn, col_info = st.columns([1, 3])
with col_btn:
    run = st.button("⟳  Grafikleri Oluştur", type="primary", use_container_width=True)
with col_info:
    st.info(
        "Butona basınca 6 grafik `outputs/` klasörüne kaydedilir (birkaç saniye sürer).",
        icon="ℹ️"
    )

if run:
    try:
        with st.spinner("Grafikler oluşturuluyor…"):
            msg = generate_charts()
        st.success(msg)
        st.rerun()
    except Exception as e:
        st.error("Grafik oluşturulurken hata oluştu.")
        st.exception(e)

st.divider()

# ── Grafik tanımları ──────────────────────────────────────────────────────────
CHARTS = {
    "line.png":      ("Yaş & Refah Trendi",       "Yaş grubuna göre mutluluk, yaşam memnuniyeti ve sağlık ortalamaları (1–5)"),
    "bar.png":       ("Tehdit Algısı",             "Katılımcıların 7 farklı toplumsal konuyu tehdit olarak değerlendirme ortalaması (0–10)"),
    "scatter.png":   ("Güven — Memnuniyet İlişkisi","Sosyal güven düzeyi ile yaşam memnuniyeti arasındaki ilişki, cinsiyete göre"),
    "pie.png":       ("Medeni Durum Dağılımı",     "Örneklemin medeni durum kompozisyonu"),
    "histogram.png": ("Yaş Dağılımı",              "Katılımcıların yaşa göre frekans dağılımı ve yoğunluk tahmini"),
    "dashboard.png": ("Genel Bakış Paneli",        "Yaş-refah trendi, eğitim dağılımı ve gelir grubu × ekonomik algı"),
}

existing = [(f, *v) for f, v in CHARTS.items()
            if os.path.exists(os.path.join(OUTPUT_DIR, f))]

if not existing:
    st.info("Henüz grafik yok. Yukarıdaki butona basarak grafikleri oluşturun.")
else:
    dashboard = [(f, t, d) for f, t, d in existing if f == "dashboard.png"]
    others    = [(f, t, d) for f, t, d in existing if f != "dashboard.png"]

    # ── 5 grafik: 2+2+1 düzeni ────────────────────────────────────────────────
    # Kategori grupları
    groups = [
        ("📈  Refah & Eğilimler",  [x for x in others if x[0] in ("line.png", "bar.png")]),
        ("🔍  İlişkiler & Dağılım", [x for x in others if x[0] in ("scatter.png", "histogram.png")]),
        ("🥧  Demografik Yapı",    [x for x in others if x[0] in ("pie.png",)]),
    ]

    for group_title, items in groups:
        if not items:
            continue
        st.markdown(f'<div class="section-title">{group_title}</div>', unsafe_allow_html=True)
        cols = st.columns(len(items))
        for col, (fname, title, desc) in zip(cols, items):
            path = os.path.join(OUTPUT_DIR, fname)
            with col:
                st.markdown(f'<div class="chart-label">{title}</div>', unsafe_allow_html=True)
                st.image(Image.open(path), use_container_width=True)
                st.caption(desc)

    # ── Dashboard — tam genişlik ───────────────────────────────────────────────
    if dashboard:
        fname, title, desc = dashboard[0]
        st.markdown('<div class="section-title">📊  Dashboard</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chart-label">{title}</div>', unsafe_allow_html=True)
        st.image(Image.open(os.path.join(OUTPUT_DIR, fname)), use_container_width=True)
        st.caption(desc)