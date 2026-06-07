from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
PIC_DIR = ROOT / "pic"

FONT_PATH = Path(r"C:\Windows\Fonts\msyh.ttc")
BOLD_FONT_PATH = Path(r"C:\Windows\Fonts\msyhbd.ttc")
FONT = font_manager.FontProperties(fname=str(FONT_PATH))
BOLD_FONT = font_manager.FontProperties(fname=str(BOLD_FONT_PATH if BOLD_FONT_PATH.exists() else FONT_PATH))

font_manager.fontManager.addfont(str(FONT_PATH))
if BOLD_FONT_PATH.exists():
    font_manager.fontManager.addfont(str(BOLD_FONT_PATH))

plt.rcParams["font.family"] = FONT.get_name()
plt.rcParams["font.sans-serif"] = [FONT.get_name(), "SimHei", "SimSun", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42


COLORS = {
    "ink": "#263238",
    "muted": "#5f6b73",
    "blue": "#2f6f9f",
    "blue_light": "#e7f0f8",
    "green": "#2e8b57",
    "green_light": "#e8f4ec",
    "orange": "#c56b2d",
    "orange_light": "#fff0df",
    "red": "#b94a48",
    "red_light": "#fde9e7",
    "gray": "#d7dde2",
    "gray_dark": "#8b98a5",
    "purple": "#6c5ce7",
    "purple_light": "#eeeafe",
}


def add_text(ax, x, y, text, size=10, color=None, bold=False, ha="center", va="center", **kwargs):
    ax.text(
        x,
        y,
        text,
        fontsize=size,
        color=color or COLORS["ink"],
        fontproperties=BOLD_FONT if bold else FONT,
        ha=ha,
        va=va,
        linespacing=1.25,
        **kwargs,
    )


def add_box(ax, x, y, w, h, label, fc, ec=None, lw=1.2, size=10, bold=False):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.018,rounding_size=0.035",
        linewidth=lw,
        edgecolor=ec or COLORS["ink"],
        facecolor=fc,
    )
    ax.add_patch(patch)
    add_text(ax, x + w / 2, y + h / 2, label, size=size, bold=bold)
    return patch


def add_arrow(ax, start, end, color=None, lw=1.5, rad=0.0, ms=13, style="-|>"):
    patch = FancyArrowPatch(
        start,
        end,
        arrowstyle=style,
        mutation_scale=ms,
        linewidth=lw,
        color=color or COLORS["ink"],
        connectionstyle=f"arc3,rad={rad}",
        shrinkA=2,
        shrinkB=2,
    )
    ax.add_patch(patch)
    return patch


def add_polyline_arrow(ax, points, color=None, lw=1.5, ms=13, style="-|>"):
    """Draw an orthogonal/polyline connector with the arrow head on the last segment."""
    if len(points) < 2:
        raise ValueError("A polyline arrow needs at least two points.")

    color = color or COLORS["ink"]
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.plot(xs, ys, color=color, linewidth=lw, solid_capstyle="round")

    start = points[-2]
    end = points[-1]
    patch = FancyArrowPatch(
        start,
        end,
        arrowstyle=style,
        mutation_scale=ms,
        linewidth=lw,
        color=color,
        shrinkA=0,
        shrinkB=0,
    )
    ax.add_patch(patch)
    return patch


def sample_polyline(points, n_per_edge=12):
    samples = []
    for p, q in zip(points, points[1:] + points[:1]):
        p = np.array(p, dtype=float)
        q = np.array(q, dtype=float)
        for t in np.linspace(0, 1, n_per_edge, endpoint=False):
            samples.append(p * (1 - t) + q * t)
    return np.array(samples)


def draw_robot(ax, x, y, color=COLORS["blue"]):
    ax.add_patch(Circle((x, y), 0.12, facecolor="#ffffff", edgecolor=color, linewidth=1.4))
    add_arrow(ax, (x - 0.06, y), (x + 0.16, y), color=color, lw=1.2, ms=10)


def save_figure(fig, stem):
    PIC_DIR.mkdir(parents=True, exist_ok=True)
    pdf = PIC_DIR / f"{stem}.pdf"
    png = PIC_DIR / f"{stem}.png"
    fig.savefig(pdf, bbox_inches="tight")
    fig.savefig(png, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(pdf)
    print(png)
