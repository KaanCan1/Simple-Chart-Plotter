import os

# Yazılabilir önbellek: her subprocess'te font cache yeniden kurulmasını önler
_mpl_cache = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".mpl_cache")
os.makedirs(_mpl_cache, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", _mpl_cache)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import pandas as pd

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Estetik Tema ───────────────────────────────────────────────────────────────
BG_COLOR     = "#0F1117"
CARD_COLOR   = "#1A1D27"
TEXT_COLOR   = "#E8EAF0"
MUTED_COLOR  = "#6B7280"
ACCENT_1     = "#4F8EF7"   # mavi
ACCENT_2     = "#F7934F"   # turuncu
ACCENT_3     = "#4FF7A0"   # yeşil
ACCENT_4     = "#F74F8E"   # pembe
ACCENT_5     = "#C44FF7"   # mor
ACCENT_6     = "#F7E44F"   # sarı

PALETTE = [ACCENT_1, ACCENT_2, ACCENT_3, ACCENT_4, ACCENT_5, ACCENT_6]

GRID_STYLE = dict(color="#2A2D3A", linewidth=0.6, linestyle="--", alpha=0.7)

plt.rcParams.update({
    "figure.dpi": 130,
    "figure.facecolor": BG_COLOR,
    "axes.facecolor": CARD_COLOR,
    "axes.edgecolor": "#2A2D3A",
    "axes.titlesize": 13,
    "axes.titlecolor": TEXT_COLOR,
    "axes.titlepad": 14,
    "axes.titleweight": "bold",
    "axes.labelsize": 10,
    "axes.labelcolor": MUTED_COLOR,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "xtick.color": MUTED_COLOR,
    "ytick.color": MUTED_COLOR,
    "legend.facecolor": "#1E2130",
    "legend.edgecolor": "#2A2D3A",
    "legend.labelcolor": TEXT_COLOR,
    "legend.fontsize": 9,
    "text.color": TEXT_COLOR,
    "font.family": "DejaVu Sans",
    "grid.color": "#2A2D3A",
    "grid.linestyle": "--",
    "grid.linewidth": 0.6,
    "grid.alpha": 0.7,
})

AY_SIRASI = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
             "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]


def _group(df, x, y_cols):
    grp = df.groupby(x, sort=False)[y_cols].sum().reset_index()
    if x == "Ay":
        grp["Ay"] = pd.Categorical(grp["Ay"], categories=AY_SIRASI, ordered=True)
        grp = grp.sort_values("Ay")
    return grp


def _style_ax(ax):
    ax.set_facecolor(CARD_COLOR)
    ax.grid(True, **GRID_STYLE)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#2A2D3A")
    ax.spines["bottom"].set_color("#2A2D3A")


class ChartPlotter:

    def __init__(self, figsize=(10, 5.5)):
        self.figsize = figsize

    def _new_ax(self, title, xlabel, ylabel):
        fig, ax = plt.subplots(figsize=self.figsize, facecolor=BG_COLOR)
        ax.set_facecolor(CARD_COLOR)
        ax.set_title(title, color=TEXT_COLOR, fontsize=13, fontweight="bold", pad=14)
        ax.set_xlabel(xlabel, color=MUTED_COLOR, fontsize=10)
        ax.set_ylabel(ylabel, color=MUTED_COLOR, fontsize=10)
        _style_ax(ax)
        return fig, ax

    def _finish(self, fig, save, filename):
        fig.patch.set_facecolor(BG_COLOR)
        plt.tight_layout(pad=1.8)
        if save:
            path = os.path.join(OUTPUT_DIR, filename)
            fig.savefig(path, bbox_inches="tight", facecolor=BG_COLOR)
            print(f"Kaydedildi → {path}")
        plt.close(fig)
        return fig

    # 1. Çizgi grafik
    def line(self, df, x, y_cols,
             title="Line chart", xlabel="", ylabel="",
             save=True, filename="line.png"):
        data = _group(df, x, y_cols)
        fig, ax = self._new_ax(title, xlabel or x, ylabel)
        for col, color in zip(y_cols, PALETTE):
            ax.plot(data[x], data[col], marker="o", label=col,
                    color=color, linewidth=2.2, markersize=6,
                    markerfacecolor=BG_COLOR, markeredgecolor=color, markeredgewidth=2)
            # Son nokta etiketi
            last_val = data[col].iloc[-1]
            ax.annotate(f"{last_val:.2f}",
                        xy=(len(data[x])-1, last_val),
                        xytext=(6, 0), textcoords="offset points",
                        color=color, fontsize=8, va="center")
        ax.legend(framealpha=0.85, loc="best")
        ax.set_xticks(range(len(data[x])))
        ax.set_xticklabels(data[x], rotation=30, ha="right", color=MUTED_COLOR)
        return self._finish(fig, save, filename)

    # 2. Çubuk grafik
    def bar(self, df, x, y_cols,
            title="Bar chart", xlabel="", ylabel="",
            save=True, filename="bar.png"):
        data = _group(df, x, y_cols)
        fig, ax = self._new_ax(title, xlabel or x, ylabel)
        x_idx = np.arange(len(data[x]))
        n = len(y_cols)
        width = 0.65 / n
        for i, (col, color) in enumerate(zip(y_cols, PALETTE)):
            offset = (i - n / 2 + 0.5) * width
            bars = ax.bar(x_idx + offset, data[col], width,
                          label=col, color=color, alpha=0.88,
                          zorder=3, edgecolor="none",
                          linewidth=0)
            # Değer etiketi
            for bar in bars:
                h = bar.get_height()
                lbl = f"{h:.2f}" if isinstance(h, float) else str(h)
                ax.annotate(lbl,
                            xy=(bar.get_x() + bar.get_width() / 2, h),
                            xytext=(0, 4), textcoords="offset points",
                            ha="center", va="bottom", fontsize=8,
                            color=TEXT_COLOR, fontweight="bold")
        ax.set_xticks(x_idx)
        ax.set_xticklabels(data[x], rotation=30, ha="right", color=MUTED_COLOR)
        if n > 1:
            ax.legend(framealpha=0.85)
        return self._finish(fig, save, filename)

    # 3. Yatay çubuk grafik (tehdit algısı gibi uzun etiketler için)
    def barh(self, df, x, y_col,
             title="Bar chart", xlabel="", ylabel="",
             save=True, filename="barh.png"):
        fig, ax = plt.subplots(figsize=(10, 5.5), facecolor=BG_COLOR)
        ax.set_facecolor(CARD_COLOR)
        _style_ax(ax)
        ax.set_title(title, color=TEXT_COLOR, fontsize=13, fontweight="bold", pad=14)

        vals = df[y_col].values
        labels = df[x].values
        colors = [PALETTE[i % len(PALETTE)] for i in range(len(vals))]

        bars = ax.barh(np.arange(len(labels)), vals, color=colors, alpha=0.88,
                       edgecolor="none", height=0.62, zorder=3)
        ax.set_yticks(np.arange(len(labels)))
        ax.set_yticklabels(labels, color=TEXT_COLOR, fontsize=10)
        ax.set_xlabel(xlabel or y_col, color=MUTED_COLOR)
        ax.invert_yaxis()

        for bar, val in zip(bars, vals):
            ax.text(val + 0.05, bar.get_y() + bar.get_height()/2,
                    f" {val:.2f}", va="center", ha="left",
                    color=TEXT_COLOR, fontsize=9, fontweight="bold")
        ax.set_xlim(0, max(vals) * 1.12)
        ax.grid(True, axis="x", **GRID_STYLE)
        ax.grid(False, axis="y")
        return self._finish(fig, save, filename)

    # 4. Saçılım grafiği
    def scatter(self, df, x, y, hue=None,
                title="Scatter plot", xlabel="", ylabel="",
                save=True, filename="scatter.png"):
        fig, ax = self._new_ax(title, xlabel or x, ylabel or y)
        if hue and hue in df.columns:
            for grp, color in zip(df[hue].unique(), PALETTE):
                mask = df[hue] == grp
                ax.scatter(df.loc[mask, x], df.loc[mask, y],
                           label=grp, color=color, s=22, alpha=0.45, zorder=3,
                           edgecolors="none")
            ax.legend(title=hue, framealpha=0.85)
        else:
            ax.scatter(df[x], df[y], color=PALETTE[0], s=22, alpha=0.45,
                       zorder=3, edgecolors="none")
        return self._finish(fig, save, filename)

    # 5. Pasta grafik
    def pie(self, labels, values,
            title="Pie chart", save=True, filename="pie.png"):
        fig, ax = plt.subplots(figsize=(8, 7), facecolor=BG_COLOR)
        ax.set_facecolor(BG_COLOR)
        colors = PALETTE[:len(values)]
        wedges, texts, autotexts = ax.pie(
            values, labels=None, autopct="%1.1f%%",
            colors=colors, startangle=90,
            wedgeprops={"linewidth": 2, "edgecolor": BG_COLOR},
            pctdistance=0.78,
        )
        for at in autotexts:
            at.set_fontsize(9)
            at.set_color(BG_COLOR)
            at.set_fontweight("bold")
        # Özel legend
        patches = [mpatches.Patch(color=c, label=l) for c, l in zip(colors, labels)]
        ax.legend(handles=patches, loc="lower center", ncol=2,
                  bbox_to_anchor=(0.5, -0.08), framealpha=0.6,
                  fontsize=9)
        ax.set_title(title, color=TEXT_COLOR, fontsize=13, fontweight="bold", pad=12)
        return self._finish(fig, save, filename)

    # 6. Histogram
    def histogram(self, series, bins=15,
                  title="Histogram", xlabel="Değer", ylabel="Frekans",
                  kde=True, save=True, filename="histogram.png"):
        fig, ax = self._new_ax(title, xlabel, ylabel)
        ax.hist(series, bins=bins, color=ACCENT_1, alpha=0.75,
                edgecolor=BG_COLOR, linewidth=0.5, zorder=3)
        if kde:
            try:
                from scipy.stats import gaussian_kde
                xs = np.linspace(series.min(), series.max(), 300)
                kde_vals = gaussian_kde(series)(xs)
                ax2 = ax.twinx()
                ax2.plot(xs, kde_vals, color=ACCENT_2, linewidth=2.2, alpha=0.9)
                ax2.set_ylabel("Yoğunluk", color=MUTED_COLOR, fontsize=9)
                ax2.tick_params(colors=MUTED_COLOR)
                ax2.set_facecolor(CARD_COLOR)
                ax2.spines["top"].set_visible(False)
                ax2.spines["right"].set_color("#2A2D3A")
            except ImportError:
                pass
        return self._finish(fig, save, filename)

    # 7. Dashboard
    def dashboard(self, plots: list, title="Dashboard",
                  save=True, filename="dashboard.png"):
        n = len(plots)
        cols = min(n, 3)
        rows = (n + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols,
                                 figsize=(7.5 * cols, 5 * rows),
                                 facecolor=BG_COLOR)
        axes = np.array(axes).flatten()
        fig.suptitle(title, fontsize=15, fontweight="bold",
                     color=TEXT_COLOR, y=1.01)

        for ax, (panel_type, data, kw) in zip(axes, plots):
            _style_ax(ax)
            self._draw_panel(ax, panel_type, data, kw)

        for ax in axes[n:]:
            ax.set_visible(False)

        plt.tight_layout(pad=2.0)
        if save:
            path = os.path.join(OUTPUT_DIR, filename)
            fig.savefig(path, bbox_inches="tight", facecolor=BG_COLOR)
            print(f"Kaydedildi → {path}")
        plt.close(fig)
        return fig

    def _draw_panel(self, ax, kind, data, kw):
        ax.set_facecolor(CARD_COLOR)
        ax.set_title(kw.get("title", kind), color=TEXT_COLOR,
                     fontsize=11, fontweight="bold", pad=10)

        if kind == "line":
            x = kw["x"]
            y_cols = kw["y_cols"]
            grp = _group(data, x, y_cols)
            for col, color in zip(y_cols, PALETTE):
                ax.plot(grp[x], grp[col], marker="o",
                        label=col, color=color, linewidth=1.8, markersize=4,
                        markerfacecolor=BG_COLOR, markeredgecolor=color,
                        markeredgewidth=1.8)
            ax.legend(fontsize=8, framealpha=0.7)
            ax.set_xticks(range(len(grp[x])))
            ax.set_xticklabels(grp[x], rotation=30, ha="right",
                               fontsize=8, color=MUTED_COLOR)

        elif kind == "bar":
            x = kw["x"]
            y = kw["y"]
            grp = _group(data, x, [y])
            x_idx = np.arange(len(grp[x]))
            colors = [PALETTE[i % len(PALETTE)] for i in range(len(x_idx))]
            ax.bar(x_idx, grp[y], color=colors, alpha=0.85,
                   edgecolor="none", zorder=3)
            ax.set_xticks(x_idx)
            ax.set_xticklabels(grp[x], rotation=30, ha="right",
                               fontsize=8, color=MUTED_COLOR)

        elif kind == "hist":
            ax.hist(data, bins=10, color=ACCENT_1, alpha=0.75,
                    edgecolor=BG_COLOR, linewidth=0.4, zorder=3)

        elif kind == "barh":
            x_col = kw["x"]
            y_col = kw["y"]
            vals = data[y_col].values
            labels = data[x_col].values
            colors = [PALETTE[i % len(PALETTE)] for i in range(len(vals))]
            ax.barh(np.arange(len(labels)), vals, color=colors,
                    alpha=0.85, edgecolor="none", height=0.6, zorder=3)
            ax.set_yticks(np.arange(len(labels)))
            ax.set_yticklabels(labels, color=TEXT_COLOR, fontsize=8)
            ax.invert_yaxis()
            ax.grid(True, axis="x", **GRID_STYLE)
            ax.grid(False, axis="y")

        ax.tick_params(colors=MUTED_COLOR)
        ax.yaxis.label.set_color(MUTED_COLOR)
        ax.xaxis.label.set_color(MUTED_COLOR)