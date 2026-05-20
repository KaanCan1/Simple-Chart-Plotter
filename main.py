"""
main.py  —  TGSS 2024 grafik üretici
Türkiye Genel Sosyal Saha Araştırması 2024 (n=2615)
"""

import pandas as pd
import numpy as np
from SimpleChartPlotter import ChartPlotter

# ── Etiket sözlükleri ─────────────────────────────────────────────────────────
AGEGROUP_LABELS = {
    1: "18-24", 2: "25-34", 3: "35-44",
    4: "45-54", 5: "55-64", 6: "65+"
}
DEGREE_LABELS = {
    1: "Okur-Yazar\nDeğil", 2: "İlkokul", 3: "Ortaokul",
    4: "Lise", 5: "Ön Lisans", 6: "Lisans",
    7: "Y.Lisans", 8: "Doktora"
}
GENDER_LABELS   = {1: "Erkek", 2: "Kadın"}
INCOME_LABELS   = {
    1: "Çok Düşük", 2: "Düşük", 3: "Altı Orta",
    4: "Orta", 5: "Üstü Orta", 6: "Yüksek",
    7: "Çok Yüksek", 8: "En Yüksek"
}
MARITAL_LABELS = {
    1: "Hiç Evlenmedi",
    2: "Evli",
    3: "Dini Nikah",
    4: "Birlikte Yaşıyor",
    5: "Boşandı",
    6: "Eşi Vefat Etti",
}
THREAT_COLS = {
    "Enflasyon":         "thinflat",
    "Kadına Şiddet":     "thfemicide",
    "Yolsuzluk":         "thcorrupt",
    "Terör":             "thterror",
    "Göç":               "thimmig",
    "İşsizlik":          "thunemp",
    "İklim Değişikliği": "thclimate",
}


def generate_charts(data_path: str = "data/TGSS2024.csv") -> str:
    """Tüm grafikleri outputs/ klasörüne yazar. Başarı mesajını döndürür."""
    df = pd.read_csv(data_path)
    plotter = ChartPlotter()

    # 1. Çizgi — Yaş grubuna göre Mutluluk, Yaşam Memnuniyeti, Sağlık
    age_filt = df[
        (df["agegroup"] > 0) &
        (df["happy"] > 0) &
        (df["lifesat"] > 0) &
        (df["health"] > 0)
    ].copy()

    agg_line = (
        age_filt.groupby("agegroup")[["happy", "lifesat", "health"]]
        .mean().reset_index().sort_values("agegroup")
    )
    agg_line["Yaş Grubu"] = agg_line["agegroup"].map(AGEGROUP_LABELS)
    agg_line = agg_line.rename(columns={
        "happy": "Mutluluk",
        "lifesat": "Yaşam Memnuniyeti",
        "health": "Sağlık"
    })

    plotter.line(
        agg_line,
        x="Yaş Grubu",
        y_cols=["Mutluluk", "Yaşam Memnuniyeti", "Sağlık"],
        title="Yaş Grubuna Göre Ortalama Mutluluk, Memnuniyet ve Sağlık",
        xlabel="Yaş Grubu",
        ylabel="Ortalama Puan (1–5)",
        filename="line.png"
    )

    # 2. Yatay çubuk — Tehdit algısı
    threat_rows = [
        {"Tehdit": label, "Ortalama Skor": round(df[df[col] >= 0][col].mean(), 2)}
        for label, col in THREAT_COLS.items()
    ]
    agg_threat = pd.DataFrame(threat_rows).sort_values("Ortalama Skor", ascending=True)

    plotter.barh(
        agg_threat,
        x="Tehdit",
        y_col="Ortalama Skor",
        title="Toplumsal Tehdit Algısı Ortalamaları (0–10)",
        xlabel="Ortalama Puan",
        filename="bar.png"
    )

    # 3. Saçılım — Sosyal güven × Yaşam memnuniyeti
    scatter_df = df[
        (df["trustpeople"] >= 0) &
        (df["lifesat"] > 0) &
        (df["gender"] > 0)
    ].copy()
    scatter_df["Cinsiyet"] = scatter_df["gender"].map(GENDER_LABELS)

    rng = np.random.default_rng(42)
    scatter_df["trust_j"] = scatter_df["trustpeople"] + rng.uniform(-0.25, 0.25, len(scatter_df))
    scatter_df["lifesat_j"] = scatter_df["lifesat"] + rng.uniform(-0.15, 0.15, len(scatter_df))

    plotter.scatter(
        scatter_df,
        x="trust_j",
        y="lifesat_j",
        hue="Cinsiyet",
        title="Sosyal Güven ile Yaşam Memnuniyeti İlişkisi",
        xlabel="Sosyal Güven (0–10)",
        ylabel="Yaşam Memnuniyeti (1–5)",
        filename="scatter.png"
    )

    # 4. Pasta — Medeni durum
    marital_counts = (
        df[df["marital"] > 0]["marital"]
        .map(MARITAL_LABELS)
        .value_counts()
    )

    threshold = len(df) * 0.02
    small_mask = marital_counts < threshold
    if small_mask.any():
        other_val = marital_counts[small_mask].sum()
        marital_counts = marital_counts[~small_mask]
        marital_counts["Diğer"] = other_val

    plotter.pie(
        labels=marital_counts.index.tolist(),
        values=marital_counts.values.tolist(),
        title="Medeni Durum Dağılımı (TGSS 2024, n=2615)",
        filename="pie.png"
    )

    # 5. Histogram — Yaş dağılımı
    age_series = df[df["age"] > 0]["age"]
    plotter.histogram(
        age_series,
        bins=15,
        title="Katılımcı Yaş Dağılımı",
        xlabel="Yaş",
        ylabel="Kişi Sayısı",
        filename="histogram.png"
    )

    # 6. Dashboard
    dash_line_df = agg_line[["Yaş Grubu", "Mutluluk", "Yaşam Memnuniyeti"]].copy()

    degree_filt = df[df["degree"] > 0].copy()
    degree_filt["Eğitim Seviyesi"] = degree_filt["degree"].map(DEGREE_LABELS)
    degree_counts = (
        degree_filt.groupby("degree")
        .agg(Eğitim=("Eğitim Seviyesi", "first"),
             Kişi=("degree", "count"))
        .reset_index()
        .sort_values("degree")
        .rename(columns={"Eğitim": "Eğitim Seviyesi", "Kişi": "Kişi Sayısı"})
    )

    income_filt = df[(df["income"] > 0) & (df["econpast"] > 0) & (df["econfut"] > 0)].copy()
    agg_econ = (
        income_filt.groupby("income")[["econpast", "econfut"]]
        .mean().reset_index().sort_values("income")
    )
    agg_econ["Gelir Grubu"] = agg_econ["income"].map(INCOME_LABELS)
    agg_econ = agg_econ.rename(columns={
        "econpast": "Geçmiş Değerlendirme",
        "econfut": "Gelecek Beklentisi"
    })

    plotter.dashboard(
        plots=[
            ("line", dash_line_df, {
                "x": "Yaş Grubu",
                "y_cols": ["Mutluluk", "Yaşam Memnuniyeti"],
                "title": "Yaş Grubu × Mutluluk & Memnuniyet"
            }),
            ("barh", degree_counts, {
                "x": "Eğitim Seviyesi",
                "y": "Kişi Sayısı",
                "title": "Eğitim Seviyesine Göre Katılımcı Sayısı"
            }),
            ("line", agg_econ, {
                "x": "Gelir Grubu",
                "y_cols": ["Geçmiş Değerlendirme", "Gelecek Beklentisi"],
                "title": "Gelir Grubu × Ekonomik Algı"
            }),
        ],
        title="TGSS 2024 — Genel Bakış Paneli",
        filename="dashboard.png"
    )

    return "Tüm grafikler outputs/ klasörüne kaydedildi."


if __name__ == "__main__":
    print(generate_charts())
