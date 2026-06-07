from matplotlib.patches import Ellipse, Polygon, Rectangle

from chap06_figure_utils import (
    COLORS,
    add_arrow,
    add_text,
    np,
    plt,
    sample_polyline,
    save_figure,
)


def panel_point(origin, scale, point):
    return origin[0] + point[0] * scale, origin[1] + point[1] * scale


def panel_points(origin, scale, points):
    return [panel_point(origin, scale, point) for point in points]


def draw_l_obstacle(ax, origin, scale, alpha=0.72, edge=COLORS["ink"], face=COLORS["gray"]):
    l_poly = [(1.05, 0.75), (3.30, 0.75), (3.30, 1.38), (1.82, 1.38), (1.82, 3.10), (1.05, 3.10)]
    patch = Polygon(
        panel_points(origin, scale, l_poly),
        closed=True,
        facecolor=face,
        edgecolor=edge,
        linewidth=1.15,
        alpha=alpha,
        zorder=3,
    )
    ax.add_patch(patch)
    return l_poly


def smooth_points(points, samples_per_segment=24, curve=0.32):
    pts = np.array(points, dtype=float)
    smoothed = []
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1 = pts[i]
        p2 = pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        m1 = curve * (p2 - p0)
        m2 = curve * (p3 - p1)
        for t in np.linspace(0, 1, samples_per_segment, endpoint=False):
            h00 = 2 * t**3 - 3 * t**2 + 1
            h10 = t**3 - 2 * t**2 + t
            h01 = -2 * t**3 + 3 * t**2
            h11 = t**3 - t**2
            smoothed.append(h00 * p1 + h10 * m1 + h01 * p2 + h11 * m2)
    smoothed.append(pts[-1])
    return np.array(smoothed)


def draw_smooth_path(ax, origin, scale, points, color, linestyle="-", lw=2.0):
    local_path = smooth_points(points)
    verts = np.array(panel_points(origin, scale, local_path))
    xs = verts[:, 0]
    ys = verts[:, 1]
    ax.plot(
        xs,
        ys,
        color=color,
        linewidth=lw,
        linestyle=linestyle,
        solid_capstyle="round",
        dash_capstyle="round",
        solid_joinstyle="round",
        zorder=6,
    )
    add_arrow(ax, tuple(verts[-8]), tuple(verts[-1]), color=color, lw=lw, ms=12)


def draw_start_goal(ax, origin, scale, start, goal):
    sx, sy = panel_point(origin, scale, start)
    gx, gy = panel_point(origin, scale, goal)
    ax.scatter([sx], [sy], s=38, facecolor="#ffffff", edgecolor=COLORS["blue"], linewidth=1.4, zorder=7)
    ax.scatter([gx], [gy], s=46, marker="*", facecolor="#ffffff", edgecolor=COLORS["green"], linewidth=1.4, zorder=7)
    add_text(ax, sx - 0.18, sy + 0.18, "S", size=8.8, color=COLORS["blue"], bold=True)
    add_text(ax, gx + 0.18, gy + 0.16, "G", size=8.8, color=COLORS["green"], bold=True)


def draw():
    fig, ax = plt.subplots(figsize=(8.2, 2.95))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.8)
    ax.axis("off")

    scale = 0.88
    left_origin = (0.50, 0.40)
    right_origin = (5.35, 0.40)
    start = (0.35, 3.35)
    goal = (3.72, 2.32)

    # Left panel: the true L-shaped obstacle remains visible under the conservative envelope.
    draw_l_obstacle(ax, left_origin, scale, alpha=0.36)
    rx, ry = panel_point(left_origin, scale, (1.05, 0.75))
    ax.add_patch(
        Rectangle(
            (rx, ry),
            2.25 * scale,
            2.35 * scale,
            facecolor=COLORS["red_light"],
            edgecolor=COLORS["red"],
            linewidth=1.2,
            linestyle="--",
            alpha=0.42,
            zorder=2,
        )
    )
    ex, ey = panel_point(left_origin, scale, (2.18, 1.92))
    ax.add_patch(
        Ellipse(
            (ex, ey),
            2.65 * scale,
            2.95 * scale,
            angle=0,
            facecolor="#f8c9c4",
            alpha=0.18,
            edgecolor=COLORS["red"],
            linewidth=1.1,
            linestyle="-.",
            zorder=1,
        )
    )
    draw_l_obstacle(ax, left_origin, scale, alpha=0.34)
    draw_smooth_path(
        ax,
        left_origin,
        scale,
        [
            start,
            (0.55, 3.72),
            (2.10, 3.82),
            (3.62, 3.66),
            (3.95, 3.08),
            goal,
        ],
        COLORS["red"],
        linestyle=(0, (5, 4)),
        lw=1.9,
    )
    draw_start_goal(ax, left_origin, scale, start, goal)

    # Right panel: boundary points preserve the free space inside the non-convex outline.
    right_l_poly = draw_l_obstacle(ax, right_origin, scale, alpha=0.68)
    samples = sample_polyline(right_l_poly, 8)
    samples = np.array(panel_points(right_origin, scale, samples))
    ax.scatter(samples[:, 0], samples[:, 1], s=16, color=COLORS["orange"], edgecolors="#ffffff", linewidths=0.35, zorder=5)
    draw_smooth_path(
        ax,
        right_origin,
        scale,
        [
            start,
            (0.88, 3.48),
            (1.70, 3.48),
            (2.10, 3.12),
            (2.58, 2.68),
            (3.14, 2.46),
            goal,
        ],
        COLORS["green"],
        lw=2.0,
    )
    draw_start_goal(ax, right_origin, scale, start, goal)

    add_text(ax, 2.40, 0.12, "(a) 包络约束下的保守绕行", size=10.0, color=COLORS["ink"], bold=True)
    add_text(ax, 7.20, 0.12, "(b) 点级表示下的局部通行", size=10.0, color=COLORS["ink"], bold=True)

    save_figure(fig, "包络约束与点级表示对比图")


if __name__ == "__main__":
    draw()
