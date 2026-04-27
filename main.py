import pandas as pd
from SimpleChartPlotter import ChartPlotter

df = pd.read_csv("data/ornek.csv")
plotter = ChartPlotter()

# 1 — Çizgi grafik: Satış, Gider ve Kâr trendi
plotter.line(
    df, x="Ay", y_cols=["Satış", "Gider", "Kâr"],
    title="Aylık Finansal Trend", ylabel="₺",
    filename="line.png"
)

# 2 — Çubuk grafik: Satış ve Gider karşılaştırması
plotter.bar(
    df, x="Ay", y_cols=["Satış", "Gider"],
    title="Aylık Satış & Gider Karşılaştırması", ylabel="₺",
    filename="bar.png"
)

# 3 — Scatter: Müşteri sayısı ile Kâr ilişkisi, bölgeye göre renkli
plotter.scatter(
    df, x="Müşteri", y="Kâr", hue="Bölge",
    title="Müşteri Sayısı — Kâr İlişkisi",
    xlabel="Müşteri Sayısı", ylabel="Kâr (TL)",
    filename="scatter.png"
)

# 4 — Pasta: Bölge bazında toplam satış
bolge = df.groupby("Bölge")["Satış"].sum()
plotter.pie(
    labels=bolge.index.tolist(),
    values=bolge.values.tolist(),
    title="Bölge Bazında Toplam Satış",
    filename="pie.png"
)

# 5 — Histogram: Kâr dağılımı
plotter.histogram(
    df["Kâr"], bins=6,
    title="Kâr Dağılımı", xlabel="Kâr (TL)",
    filename="histogram.png"
)

# 6 — Dashboard: Hepsini tek dosyada göster
plotter.dashboard([
    ("line", df, {"x": "Ay", "y_cols": ["Satış", "Gider"], "title": "Satış & Gider"}),
    ("bar",  df, {"x": "Ay", "y": "Kâr", "title": "Aylık Kâr"}),
    ("hist", df["Müşteri"], {"title": "Müşteri Dağılımı"}),
], title="Genel Bakış Paneli", filename="dashboard.png")

print("\nTüm grafikler outputs/ klasörüne kaydedildi.")