# -*- coding: utf-8 -*-
"""绘制第三章：镜头畸变示意图（径向畸变 + 切向畸变）。"""

import numpy as np
import matplotlib.pyplot as plt

from chap06_figure_utils import COLORS, add_text, save_figure


def _grid(n=9):
    xs = np.linspace(-1, 1, n)
    lines = []
    for x in xs:
        lines.append((np.full(50, x), np.linspace(-1, 1, 50)))
    for y in xs:
        lines.append((np.linspace(-1, 1, 50), np.full(50, y)))
    return lines


def _radial(x, y, k):
    r2 = x**2 + y**2
    factor = 1 + k * r2
    return x * factor, y * factor


def _tangential(x, y, p1, p2):
    r2 = x**2 + y**2
    xd = x + (2 * p1 * x * y + p2 * (r2 + 2 * x**2))
    yd = y + (p1 * (r2 + 2 * y**2) + 2 * p2 * x * y)
    return xd, yd


def _panel(ax, title, transform):
    for gx, gy in _grid():
        tx, ty = transform(gx, gy)
        ax.plot(tx, ty, color=COLORS["blue"], lw=0.9)
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.5, 1.35)
    ax.set_aspect("equal")
    ax.axis("off")
    add_text(ax, 0, -1.42, title, size=12, color=COLORS["ink"])


def main():
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 3.4))

    _panel(axes[0], "(a) 理想无畸变", lambda x, y: (x, y))
    _panel(axes[1], "(b) 径向畸变（桶形 $k_1<0$）", lambda x, y: _radial(x, y, -0.28))
    _panel(axes[2], "(c) 切向畸变", lambda x, y: _tangential(x, y, 0.05, 0.10))

    fig.subplots_adjust(wspace=0.08)
    save_figure(fig, "镜头畸变示意图")


if __name__ == "__main__":
    main()
