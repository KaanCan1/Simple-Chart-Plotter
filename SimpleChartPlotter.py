import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "figure.dpi": 120,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})

PALETTE = sns.color_palette("muted")

AY_SIRASI = ["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran",
            "Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]


def _group(df, x, y_cols):
    """Aynı x değerlerini toplayarak tek satıra indirir."""
    grp = df.groupby(x, sort=False)[y_cols].sum().reset_index()
    if x == "Ay":
        grp["Ay"] = pd.Categorical(grp["Ay"], categories=AY_SIRASI, ordered=True)
        grp = grp.sort_values("Ay")
    return grp


class ChartPlotter:

    def __init__(self, figsize=(9, 5)):
        self.figsize = figsize

    def _new_ax(self, title, xlabel, ylabel):
        fig, ax = plt.subplots(figsize=self.figsize)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        return fig, ax

    def _finish(self, fig, save, filename):
        plt.tight_layout()
        if save:
            path = os.path.join(OUTPUT_DIR, filename)
            fig.savefig(path, bbox_inches="tight")
            print(f"Kaydedildi → {path}")
        plt.show()
        return fig

    # 1. Line chart
    def line(self, df, x, y_cols,
            title="Line chart", xlabel="", ylabel="",
            save=True, filename="line.png"):
        data = _group(df, x, y_cols)
        fig, ax = self._new_ax(title, xlabel or x, ylabel)
        for col, color in zip(y_cols, PALETTE):
            ax.plot(data[x], data[col], marker="o", label=col,
                    color=color, linewidth=2, markersize=5)
        ax.legend()
        plt.xticks(rotation=30, ha="right")
        return self._finish(fig, save, filename)

    # 2. Bar chart
    def bar(self, df, x, y_cols,
            title="Bar chart", xlabel="", ylabel="",
            save=True, filename="bar.png"):
        data = _group(df, x, y_cols)
        fig, ax = self._new_ax(title, xlabel or x, ylabel)
        x_idx = np.arange(len(data[x]))
        n = len(y_cols)
        width = 0.7 / n
        for i, (col, color) in enumerate(zip(y_cols, PALETTE)):
            offset = (i - n / 2 + 0.5) * width
            ax.bar(x_idx + offset, data[col], width,
                label=col, color=color, alpha=0.85, zorder=3)
        ax.set_xticks(x_idx)
        ax.set_xticklabels(data[x], rotation=30, ha="right")
        ax.legend()
        return self._finish(fig, save, filename)

    # 3. Scatter plot
    def scatter(self, df, x, y, hue=None,
                title="Scatter plot", xlabel="", ylabel="",
                save=True, filename="scatter.png"):
        fig, ax = self._new_ax(title, xlabel or x, ylabel or y)
        if hue and hue in df.columns:
            for grp, color in zip(df[hue].unique(), PALETTE):
                mask = df[hue] == grp
                ax.scatter(df.loc[mask, x], df.loc[mask, y],
                        label=grp, color=color, s=60, alpha=0.8, zorder=3)
            ax.legend(title=hue)
        else:
            ax.scatter(df[x], df[y], color=PALETTE[0], s=60, alpha=0.8, zorder=3)
        return self._finish(fig, save, filename)

    # 4. Pie chart
    def pie(self, labels, values,
            title="Pie chart", save=True, filename="pie.png"):
        fig, ax = plt.subplots(figsize=(7, 7))
        _, texts, autotexts = ax.pie(
            values, labels=labels, autopct="%1.1f%%",
            colors=PALETTE[:len(values)], startangle=90,
            wedgeprops={"linewidth": 0.8, "edgecolor": "white"},
        )
        for at in autotexts:
            at.set_fontsize(10)
        ax.set_title(title)
        return self._finish(fig, save, filename)

    # 5. Histogram
    def histogram(self, series, bins=10,
                title="Histogram", xlabel="Değer", ylabel="Frekans",
                kde=True, save=True, filename="histogram.png"):
        fig, ax = self._new_ax(title, xlabel, ylabel)
        sns.histplot(series, bins=bins, kde=kde,
                    color=PALETTE[1], ax=ax, zorder=3)
        return self._finish(fig, save, filename)

    # 6. Dashboard
    def dashboard(self, plots: list, title="Dashboard",
                save=True, filename="dashboard.png"):
        n = len(plots)
        cols = min(n, 3)
        rows = (n + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(7 * cols, 5 * rows))
        axes = np.array(axes).flatten()
        fig.suptitle(title, fontsize=14)

        for ax, (panel_type, data, kw) in zip(axes, plots):
            self._draw_panel(ax, panel_type, data, kw)

        for ax in axes[n:]:
            ax.set_visible(False)

        plt.tight_layout()
        if save:
            path = os.path.join(OUTPUT_DIR, filename)
            fig.savefig(path, bbox_inches="tight")
            print(f"Kaydedildi → {path}")
        plt.show()
        return fig

    def _draw_panel(self, ax, kind, data, kw):
        ax.set_title(kw.get("title", kind))

        if kind == "line":
            x = kw["x"]
            y_cols = kw["y_cols"]
            grp = _group(data, x, y_cols)
            for col, color in zip(y_cols, PALETTE):
                ax.plot(grp[x], grp[col], marker="o",
                        label=col, color=color, linewidth=1.8, markersize=4)
            ax.legend(fontsize=9)
            ax.set_xticks(range(len(grp[x])))
            ax.set_xticklabels(grp[x], rotation=30, ha="right", fontsize=8)

        elif kind == "bar":
            x = kw["x"]
            y = kw["y"]
            grp = _group(data, x, [y])
            x_idx = np.arange(len(grp[x]))
            ax.bar(x_idx, grp[y], color=PALETTE[2], alpha=0.85)
            ax.set_xticks(x_idx)
            ax.set_xticklabels(grp[x], rotation=30, ha="right", fontsize=8)

        elif kind == "hist":
            sns.histplot(data, bins=8, kde=True, color=PALETTE[1], ax=ax)

        ax.grid(True, linestyle="--", alpha=0.4)