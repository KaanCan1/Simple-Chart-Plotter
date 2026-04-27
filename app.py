import streamlit as st
import subprocess
import os
from PIL import Image

st.set_page_config(page_title="Simple Chart Plotter", layout="wide")
st.title("Simple Chart Plotter")

OUTPUT_DIR = "outputs"
CHARTS = ["line.png", "bar.png", "scatter.png", "pie.png", "histogram.png", "dashboard.png"]

if st.button("Grafikleri Oluştur"):
    with st.spinner("main.py çalışıyor..."):
        result = subprocess.run(["python3", "main.py"], capture_output=True, text=True)
    if result.returncode == 0:
        st.success("Tüm grafikler oluşturuldu.")
    else:
        st.error(result.stderr)

st.divider()

existing = [f for f in CHARTS if os.path.exists(os.path.join(OUTPUT_DIR, f))]

if not existing:
    st.info("Henüz grafik yok. Yukarıdaki butona bas.")
else:
    for i in range(0, len(existing), 2):
        cols = st.columns(2)
        for col, fname in zip(cols, existing[i:i+2]):
            path = os.path.join(OUTPUT_DIR, fname)
            col.image(Image.open(path), caption=fname, use_container_width=True)