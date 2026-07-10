# -*- coding: utf-8 -*-
"""绘制第三章：机器人 TF 坐标变换树结构图。"""

import matplotlib.pyplot as plt

from chap06_figure_utils import COLORS, add_box, add_text, add_polyline_arrow, save_figure


def main():
    fig, ax = plt.subplots(figsize=(7.6, 5.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8.4)
    ax.axis("off")

    bw, bh = 2.6, 0.82

    def box(cx, cy, label, fc, ec):
        add_box(ax, cx - bw / 2, cy - bh / 2, bw, bh, label, fc=fc, ec=ec, size=11)
        return (cx, cy)

    blue = COLORS["blue"]
    green = COLORS["green"]
    orange = COLORS["orange"]
    ink = COLORS["ink"]

    # 层级：map -> odom -> base_link -> {livox_frame, realsense_link}
    p_map = box(5.0, 7.7, "map（全局地图坐标系）", COLORS["blue_light"], blue)
    p_odom = box(5.0, 6.1, "odom（里程计坐标系）", COLORS["blue_light"], blue)
    p_base = box(5.0, 4.5, "base\\_link（机器人本体）", COLORS["gray"], ink)
    p_livox = box(2.7, 2.4, "livox\\_frame（激光雷达）", COLORS["green_light"], green)
    p_rs = box(7.3, 2.4, "realsense\\_link（深度相机）", COLORS["orange_light"], orange)

    # 连接线
    def down(a, b, color, label, dyn=False):
        add_polyline_arrow(ax, [(a[0], a[1] - bh / 2), (b[0], b[1] + bh / 2)],
                           color=color, lw=1.5)

    down(p_map, p_odom, blue, "")
    add_text(ax, 5.35, 6.9, "SLAM（动态）", size=9, color=blue, ha="left")
    down(p_odom, p_base, blue, "")
    add_text(ax, 5.35, 5.3, "里程计（动态）", size=9, color=blue, ha="left")

    # base_link 到两个传感器（静态 TF）
    add_polyline_arrow(ax, [(p_base[0], p_base[1] - bh / 2), (p_base[0], 3.35),
                            (p_livox[0], 3.35), (p_livox[0], p_livox[1] + bh / 2)],
                       color=green, lw=1.5)
    add_polyline_arrow(ax, [(p_base[0], p_base[1] - bh / 2), (p_base[0], 3.35),
                            (p_rs[0], 3.35), (p_rs[0], p_rs[1] + bh / 2)],
                       color=orange, lw=1.5)
    add_text(ax, 2.7, 3.05, "静态 TF\n(0.22,$-$0.22,0)", size=8.5, color=green)
    add_text(ax, 7.3, 3.05, "静态 TF\n(0.275,0,0)", size=8.5, color=orange)

    # 图例说明
    add_text(ax, 5.0, 1.0, "实线箭头表示父 → 子坐标系变换；base\\_link 以下为机械固定的静态变换",
             size=9, color=COLORS["muted"])

    save_figure(fig, "机器人TF坐标变换树")


if __name__ == "__main__":
    main()
