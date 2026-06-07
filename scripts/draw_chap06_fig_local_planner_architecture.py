from matplotlib.patches import FancyBboxPatch

from chap06_figure_utils import COLORS, add_box, add_polyline_arrow, add_text, plt, save_figure


def draw():
    fig, ax = plt.subplots(figsize=(8.8, 4.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.add_patch(
        FancyBboxPatch(
            (0.035, 0.13),
            0.225,
            0.76,
            boxstyle="round,pad=0.02,rounding_size=0.025",
            linewidth=1.3,
            edgecolor=COLORS["blue"],
            facecolor="#f7fbff",
        )
    )
    add_text(ax, 0.147, 0.845, "第4章感知与地图输出", size=9.6, bold=True, color=COLORS["blue"])

    y0 = 0.705
    input_boxes = [
        (y0, "局部地图\n$\\mathcal{M}_l$"),
        (y0 - 0.155, "实时点云\n聚类边界"),
        (y0 - 0.310, "AABB/椭圆包络\n边界采样"),
        (y0 - 0.465, "动态状态估计\n$\\hat{\\mathbf{S}}_j(t)$"),
    ]
    for y, label in input_boxes:
        add_box(ax, 0.065, y, 0.165, 0.105, label, COLORS["blue_light"], COLORS["blue"], size=9.5)

    add_text(ax, 0.480, 0.845, "点级障碍表示与距离特征", size=8.9, color=COLORS["muted"])
    add_box(ax, 0.340, 0.620, 0.165, 0.115, "统一障碍点集\n$\\mathcal{P}_t$", COLORS["orange_light"], COLORS["orange"], size=9.6, bold=True)
    add_box(ax, 0.585, 0.620, 0.165, 0.115, "预测点流\n$\\mathbf{p}_{k|t}^{i}$", COLORS["orange_light"], COLORS["orange"], size=9.6, bold=True)
    add_box(ax, 0.340, 0.355, 0.165, 0.115, "机器人局部坐标\n$\\bar{\\mathbf{p}}_{k|t}^{i}$", COLORS["purple_light"], COLORS["purple"], size=9.4)
    add_box(ax, 0.585, 0.355, 0.165, 0.115, "距离特征编码器\n$\\Phi_{\\Theta}(\\cdot)$", COLORS["purple_light"], COLORS["purple"], size=9.4, bold=True)

    add_text(ax, 0.850, 0.845, "滚动优化与输出", size=8.9, color=COLORS["muted"])
    add_box(ax, 0.810, 0.690, 0.150, 0.100, "RRT全局路径\n$Path_g$", COLORS["green_light"], COLORS["green"], size=9.4)
    add_box(ax, 0.800, 0.430, 0.170, 0.145, "MPC滚动优化\n$J,\\ f,\\ I_{k,i}$\n速度/安全距离约束", "#eef7f0", COLORS["green"], size=8.8, bold=True)
    add_box(ax, 0.800, 0.180, 0.170, 0.115, "局部轨迹 $Path_l$\n首项控制 $\\mathbf{u}_0^*$", "#eef7f0", COLORS["green"], size=9.2, bold=True)

    # Perception outputs are merged through a vertical bus before entering the point set.
    bus_x = 0.285
    for y, _ in input_boxes[:3]:
        add_polyline_arrow(ax, [(0.230, y + 0.052), (bus_x, y + 0.052)], COLORS["orange"], lw=1.2, ms=9)
    ax.plot([bus_x, bus_x], [0.397, 0.758], color=COLORS["orange"], linewidth=1.2)
    add_polyline_arrow(ax, [(bus_x, 0.678), (0.340, 0.678)], COLORS["orange"], lw=1.4, ms=12)

    # Dynamic state is mainly used for point-flow prediction.
    add_polyline_arrow(ax, [(0.230, y0 - 0.465 + 0.052), (0.530, y0 - 0.465 + 0.052), (0.530, 0.565), (0.625, 0.565), (0.625, 0.620)], COLORS["orange"], lw=1.3, ms=12)
    add_polyline_arrow(ax, [(0.505, 0.678), (0.585, 0.678)], COLORS["orange"], lw=1.4, ms=12)

    add_polyline_arrow(ax, [(0.750, 0.678), (0.765, 0.678), (0.765, 0.535), (0.423, 0.535), (0.423, 0.470)], COLORS["purple"], lw=1.4, ms=12)
    add_polyline_arrow(ax, [(0.505, 0.413), (0.585, 0.413)], COLORS["purple"], lw=1.4, ms=12)
    add_polyline_arrow(ax, [(0.750, 0.413), (0.775, 0.413), (0.775, 0.502), (0.800, 0.502)], COLORS["purple"], lw=1.4, ms=12)

    add_polyline_arrow(ax, [(0.885, 0.690), (0.885, 0.575)], COLORS["green"], lw=1.4, ms=12)
    add_polyline_arrow(ax, [(0.885, 0.430), (0.885, 0.295)], COLORS["green"], lw=1.4, ms=12)

    # Closed-loop feedback after executing the first control action.
    add_polyline_arrow(ax, [(0.885, 0.180), (0.885, 0.085), (0.145, 0.085), (0.145, 0.130)], COLORS["gray_dark"], lw=1.0, ms=9)
    add_text(ax, 0.515, 0.055, "执行控制后更新定位与感知", size=8.8, color=COLORS["muted"])

    save_figure(fig, "学习增强MPC局部规划架构图")


if __name__ == "__main__":
    draw()
