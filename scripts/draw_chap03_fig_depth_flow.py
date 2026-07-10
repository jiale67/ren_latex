# -*- coding: utf-8 -*-
"""绘制第三章：深度图像到三维点云的转换处理流程图。"""

import matplotlib.pyplot as plt

from chap06_figure_utils import COLORS, add_box, add_text, add_polyline_arrow, save_figure


def main():
    fig, ax = plt.subplots(figsize=(9.4, 3.2))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    blue = COLORS["blue"]
    green = COLORS["green"]
    orange = COLORS["orange"]
    ink = COLORS["ink"]

    bw, bh = 3.0, 1.7
    y = 2.6
    gap = 0.55
    xs = [0.4 + i * (bw + gap) for i in range(5)]

    boxes = [
        ("深度图输入\n(16UC1, 640$\\times$480)", COLORS["blue_light"], blue),
        ("有效深度过滤\n(0.3\\,m $\\sim$ 5\\,m)", COLORS["green_light"], green),
        ("针孔反投影\n(内参 $f_x,f_y,c_x,c_y$)", COLORS["orange_light"], orange),
        ("光学系→机体系\n旋转 + 降采样", COLORS["green_light"], green),
        ("TF 变换 + 发布\n(base\\_link 点云)", COLORS["blue_light"], blue),
    ]

    centers = []
    for x, (label, fc, ec) in zip(xs, boxes):
        add_box(ax, x, y - bh / 2, bw, bh, label, fc=fc, ec=ec, size=10)
        centers.append((x + bw, y))
        # 起点用于连接
    # 箭头
    for i in range(len(xs) - 1):
        start = (xs[i] + bw, y)
        end = (xs[i + 1], y)
        add_polyline_arrow(ax, [start, end], color=ink, lw=1.5)

    save_figure(fig, "深度图转点云流程")


if __name__ == "__main__":
    main()
