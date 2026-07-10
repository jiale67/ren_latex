# -*- coding: utf-8 -*-
"""绘制第三章：针孔相机成像模型示意图。"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

from chap06_figure_utils import COLORS, FONT, add_text, save_figure


def _arrow(ax, start, end, color, lw=1.3, ms=12, style="-|>"):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=ms,
                                 linewidth=lw, color=color, shrinkA=0, shrinkB=0))


def main():
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    ax.set_xlim(-0.6, 9.2)
    ax.set_ylim(-2.4, 2.8)
    ax.axis("off")

    ink = COLORS["ink"]
    blue = COLORS["blue"]
    orange = COLORS["orange"]
    green = COLORS["green"]
    muted = COLORS["muted"]

    # 光心 O_c
    oc = (1.0, 0.0)
    ax.plot(*oc, "o", color=ink, ms=7, zorder=5)
    add_text(ax, oc[0] - 0.15, oc[1] - 0.35, r"$O_c$", size=13, color=ink)

    # 相机坐标轴
    _arrow(ax, oc, (oc[0] + 1.2, oc[1] + 0.0), muted, lw=1.0, ms=10)   # Zc 光轴方向(水平)
    _arrow(ax, oc, (oc[0] + 0.0, oc[1] + 1.1), muted, lw=1.0, ms=10)   # Yc
    add_text(ax, oc[0] + 0.15, oc[1] + 1.2, r"$Y_c$", size=11, color=muted)

    # 光轴
    ax.plot([oc[0], 8.8], [0, 0], "--", color=muted, lw=1.0)
    add_text(ax, 8.7, -0.28, r"$Z_c$ (光轴)", size=11, color=muted, ha="right")

    # 成像平面 (image plane) at focal length f
    f_x = 3.4
    ax.plot([f_x, f_x], [-1.7, 1.7], "-", color=blue, lw=2.2)
    add_text(ax, f_x, 2.0, "成像平面", size=11, color=blue)
    add_text(ax, f_x + 0.02, -2.0, "(焦距 $f$)", size=10, color=blue)
    # 主点 principal point
    ax.plot(f_x, 0, "s", color=blue, ms=6, zorder=5)
    add_text(ax, f_x + 0.42, 0.02, r"$(c_x,c_y)$", size=10, color=blue, ha="left")

    # f 标注
    ax.annotate("", xy=(f_x, -1.35), xytext=(oc[0], -1.35),
                arrowprops=dict(arrowstyle="<->", color=ink, lw=1.0))
    add_text(ax, (oc[0] + f_x) / 2, -1.6, r"$f$", size=12, color=ink)

    # 三维空间点 P
    P = (7.8, 1.9)
    ax.plot(*P, "o", color=orange, ms=8, zorder=5)
    add_text(ax, P[0] + 0.1, P[1] + 0.28, r"$P=(X_c,Y_c,Z_c)$", size=12, color=orange, ha="left")

    # 投影线 P -> Oc
    ax.plot([oc[0], P[0]], [oc[1], P[1]], "-", color=orange, lw=1.4, alpha=0.9)

    # 像点 p (交点在成像平面上)
    t = (f_x - oc[0]) / (P[0] - oc[0])
    p_img = (f_x, oc[1] + t * (P[1] - oc[1]))
    ax.plot(*p_img, "o", color=orange, ms=7, zorder=6)
    add_text(ax, p_img[0] - 0.15, p_img[1] + 0.02, r"$p=(u,v)$", size=11, color=orange, ha="right")

    # 像素坐标系示意 (右下角)
    ox, oy = 4.2, -1.9
    _arrow(ax, (ox, oy), (ox + 1.0, oy), ink, lw=1.0, ms=10)
    _arrow(ax, (ox, oy), (ox, oy + 0.8), ink, lw=1.0, ms=10)
    add_text(ax, ox + 1.1, oy, r"$u$", size=11, color=ink, ha="left")
    add_text(ax, ox - 0.05, oy + 0.95, r"$v$", size=11, color=ink, ha="right")
    add_text(ax, ox - 0.15, oy - 0.05, "$o$", size=10, color=ink, ha="right", va="top")

    save_figure(fig, "针孔相机成像模型")


if __name__ == "__main__":
    main()
