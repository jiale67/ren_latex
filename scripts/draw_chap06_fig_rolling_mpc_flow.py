from matplotlib.patches import FancyBboxPatch

from chap06_figure_utils import COLORS, add_box, add_polyline_arrow, add_text, plt, save_figure


def draw():
    fig, ax = plt.subplots(figsize=(7.6, 3.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_text(ax, 0.115, 0.925, "输入信息", size=9.0, color=COLORS["muted"])
    add_box(ax, 0.045, 0.730, 0.150, 0.105, "当前状态\n$\\mathbf{s}(t)$", COLORS["blue_light"], COLORS["blue"], size=9.5, bold=True)
    add_box(ax, 0.045, 0.545, 0.150, 0.105, "RRT全局路径\n$Path_g$", COLORS["green_light"], COLORS["green"], size=9.2)
    add_box(ax, 0.045, 0.360, 0.150, 0.105, "感知结果\n$\\mathcal{O}_t,\\mathcal{M}_l$", COLORS["blue_light"], COLORS["blue"], size=9.3, bold=True)

    add_text(ax, 0.315, 0.925, "时域数据构造", size=9.0, color=COLORS["muted"])
    add_box(ax, 0.250, 0.645, 0.165, 0.105, "截取参考序列\n$\\mathbf{s}_{0:N}^{ref}$", COLORS["green_light"], COLORS["green"], size=9.2)
    add_box(ax, 0.250, 0.360, 0.165, 0.105, "预测障碍点流\n$\\mathbf{p}_{k|t}^{i}$", COLORS["orange_light"], COLORS["orange"], size=9.2, bold=True)

    ax.add_patch(
        FancyBboxPatch(
            (0.470, 0.245),
            0.350,
            0.560,
            boxstyle="round,pad=0.02,rounding_size=0.025",
            linewidth=1.2,
            edgecolor=COLORS["gray_dark"],
            facecolor="#fcfcfc",
        )
    )
    add_text(ax, 0.645, 0.770, "感知-运动耦合迭代  $l=1,\\ldots,K_{max}$", size=9.2, color=COLORS["muted"])

    add_box(ax, 0.500, 0.600, 0.125, 0.105, "局部坐标变换\n$\\bar{\\mathbf{p}}_{k|t}^{i}$", COLORS["purple_light"], COLORS["purple"], size=8.8)
    add_box(ax, 0.665, 0.600, 0.125, 0.105, "距离特征编码\n$\\mu,\\lambda$", COLORS["purple_light"], COLORS["purple"], size=8.8, bold=True)
    add_box(ax, 0.665, 0.350, 0.125, 0.105, "构造并求解MPC\n$J,\\mathcal{I}_{k}$", "#eef7f0", COLORS["green"], size=8.6, bold=True)
    add_box(ax, 0.500, 0.350, 0.125, 0.105, "名义轨迹更新\n$\\bar{\\mathbf{s}},\\bar{\\mathbf{u}}$", "#eef7f0", COLORS["green"], size=8.8)

    add_text(ax, 0.908, 0.925, "输出执行", size=9.0, color=COLORS["muted"])
    add_box(ax, 0.840, 0.575, 0.135, 0.110, "输出\n$Path_l,\\mathbf{u}_0^*$", "#eef7f0", COLORS["green"], size=9.2, bold=True)
    add_box(ax, 0.840, 0.265, 0.135, 0.115, "执行首个控制量\n进入下一周期", "#f7f7f7", COLORS["gray_dark"], size=9.0, bold=True)

    # Input streams.
    add_polyline_arrow(ax, [(0.195, 0.782), (0.220, 0.782), (0.220, 0.698), (0.250, 0.698)], COLORS["blue"], lw=1.3, ms=11)
    add_polyline_arrow(ax, [(0.195, 0.598), (0.220, 0.598), (0.220, 0.698), (0.250, 0.698)], COLORS["green"], lw=1.3, ms=11)
    add_polyline_arrow(ax, [(0.195, 0.412), (0.250, 0.412)], COLORS["orange"], lw=1.4, ms=12)

    # Preprocessed data enters the inner optimization loop without diagonal lines.
    add_polyline_arrow(ax, [(0.415, 0.412), (0.455, 0.412), (0.455, 0.652), (0.500, 0.652)], COLORS["orange"], lw=1.4, ms=12)
    add_polyline_arrow(ax, [(0.415, 0.698), (0.440, 0.698), (0.440, 0.735), (0.645, 0.735), (0.645, 0.505), (0.680, 0.505), (0.680, 0.455)], COLORS["green"], lw=1.2, ms=11)

    # Inner rolling-optimization loop.
    add_polyline_arrow(ax, [(0.625, 0.652), (0.665, 0.652)], COLORS["purple"], lw=1.4, ms=12)
    add_polyline_arrow(ax, [(0.728, 0.600), (0.728, 0.455)], COLORS["green"], lw=1.4, ms=12)
    add_polyline_arrow(ax, [(0.665, 0.402), (0.625, 0.402)], COLORS["green"], lw=1.4, ms=12)
    add_polyline_arrow(ax, [(0.562, 0.455), (0.562, 0.600)], COLORS["gray_dark"], lw=1.1, ms=10)

    # Optimized result and closed-loop feedback.
    add_polyline_arrow(ax, [(0.790, 0.402), (0.825, 0.402), (0.825, 0.630), (0.840, 0.630)], COLORS["green"], lw=1.4, ms=12)
    add_polyline_arrow(ax, [(0.908, 0.575), (0.908, 0.380)], COLORS["green"], lw=1.4, ms=12)
    add_polyline_arrow(ax, [(0.908, 0.265), (0.908, 0.145), (0.025, 0.145), (0.025, 0.782), (0.045, 0.782)], COLORS["gray_dark"], lw=1.0, ms=9)
    add_text(ax, 0.315, 0.120, "执行后更新定位与感知", size=8.4, color=COLORS["muted"])

    save_figure(fig, "学习增强MPC滚动优化流程图")


if __name__ == "__main__":
    draw()
