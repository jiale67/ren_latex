# -*- coding: utf-8 -*-
"""绘制第三章：机器人传感器安装位置示意图（俯视图）。"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle

from chap06_figure_utils import COLORS, FONT, add_text, save_figure


def _arrow(ax, start, end, color, lw=1.4, ms=13):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=ms,
                                 linewidth=lw, color=color, shrinkA=0, shrinkB=0))


def _frame(ax, origin, color, label, label_dx=0.0, label_dy=0.0, ax_len=0.12):
    """在 origin 处画一个二维坐标系（+X 前, +Y 左）并标注名称。"""
    ox, oy = origin
    _arrow(ax, (ox, oy), (ox + ax_len, oy), color, lw=1.2, ms=10)   # X 前
    _arrow(ax, (ox, oy), (ox, oy + ax_len), color, lw=1.2, ms=10)   # Y 左
    ax.add_patch(Circle((ox, oy), 0.012, facecolor=color, edgecolor="none", zorder=6))
    add_text(ax, ox + label_dx, oy + label_dy, label, size=10.5, color=color)


def main():
    fig, ax = plt.subplots(figsize=(6.6, 5.6))
    ax.set_xlim(-0.45, 0.6)
    ax.set_ylim(-0.5, 0.55)
    ax.set_aspect("equal")
    ax.axis("off")

    ink = COLORS["ink"]
    blue = COLORS["blue"]
    green = COLORS["green"]
    orange = COLORS["orange"]
    muted = COLORS["muted"]

    # 机器人底盘轮廓 (俯视, 以 base_link 为中心的方形)
    half = 0.30
    ax.add_patch(Rectangle((-half, -half), 2 * half, 2 * half,
                           facecolor=COLORS["gray"], edgecolor=ink,
                           linewidth=1.4, alpha=0.35, zorder=0))
    add_text(ax, -half + 0.02, half - 0.03, "机器人底盘（俯视）", size=10,
             color=muted, ha="left")

    # base_link 坐标系 (中心)
    _frame(ax, (0.0, 0.0), ink, "base\\_link", label_dx=-0.02, label_dy=-0.045)
    add_text(ax, 0.135, -0.012, "$X$", size=9.5, color=ink, ha="left")
    add_text(ax, -0.01, 0.135, "$Y$", size=9.5, color=ink, ha="right")

    # realsense_link: 前方 (0.275, 0, 0)
    rs = (0.275, 0.0)
    _frame(ax, rs, orange, "realsense\\_link", label_dx=0.0, label_dy=0.055)
    ax.add_patch(Rectangle((rs[0] - 0.015, rs[1] - 0.04), 0.03, 0.08,
                           facecolor=COLORS["orange_light"], edgecolor=orange,
                           linewidth=1.2, zorder=5))

    # livox_frame: 前右 (0.22, -0.22, 0)
    lv = (0.22, -0.22)
    _frame(ax, lv, green, "livox\\_frame", label_dx=0.02, label_dy=-0.05)
    ax.add_patch(Circle(lv, 0.028, facecolor=COLORS["green_light"],
                        edgecolor=green, linewidth=1.2, zorder=5))

    # 平移标注 (虚线 + 数值)
    ax.plot([0, rs[0]], [0, 0], "--", color=orange, lw=1.0, alpha=0.7)
    add_text(ax, 0.14, 0.018, "0.275\\,m", size=9, color=orange)

    ax.plot([0, lv[0]], [0, 0], ":", color=green, lw=1.0, alpha=0.6)
    ax.plot([lv[0], lv[0]], [0, lv[1]], ":", color=green, lw=1.0, alpha=0.6)
    add_text(ax, 0.11, -0.02, "0.22", size=8.5, color=green, ha="center")
    add_text(ax, lv[0] + 0.035, -0.11, "0.22", size=8.5, color=green, ha="left")

    # 前方向指示
    add_text(ax, 0.0, -0.42, "$+X$：机器人前进方向", size=10, color=muted)

    save_figure(fig, "传感器安装位置示意图")


if __name__ == "__main__":
    main()
