from matplotlib.patches import Circle, Polygon, Rectangle

from chap06_figure_utils import COLORS, add_arrow, add_text, np, plt, save_figure


RED = "#d93b37"
GREEN = "#22b85a"
FOV_FILL = "#f5d64a"
FOV_EDGE = "#ddc22b"
OBSTACLE_FILL = "#f3f5f7"
OBSTACLE_EDGE = "#59656f"


def scatter_points(ax, points, color, size=28, zorder=7):
    pts = np.asarray(points, dtype=float)
    ax.scatter(
        pts[:, 0],
        pts[:, 1],
        s=size,
        marker="o",
        facecolor=color,
        edgecolor="#ffffff",
        linewidth=0.55,
        zorder=zorder,
    )


def draw_sensor(ax, x, y, color, label):
    ax.add_patch(
        Circle(
            (x, y),
            0.020,
            facecolor="#ffffff",
            edgecolor=color,
            linewidth=1.5,
            zorder=9,
        )
    )
    ax.plot([x - 0.038, x + 0.038], [y - 0.030, y - 0.030], color=color, linewidth=1.4, zorder=9)
    add_text(ax, x, y - 0.070, label, size=9.6, color=COLORS["ink"], bold=True)


def draw_detection_box(ax, xy, width, height, color, zorder):
    ax.add_patch(
        Rectangle(
            xy,
            width,
            height,
            facecolor="none",
            edgecolor=color,
            linewidth=1.45,
            linestyle=(0, (5, 3)),
            zorder=zorder,
        )
    )


def point_in_triangle(point, triangle):
    p = np.asarray(point, dtype=float)
    a, b, c = [np.asarray(v, dtype=float) for v in triangle]

    v0 = c - a
    v1 = b - a
    v2 = p - a
    dot00 = np.dot(v0, v0)
    dot01 = np.dot(v0, v1)
    dot02 = np.dot(v0, v2)
    dot11 = np.dot(v1, v1)
    dot12 = np.dot(v1, v2)
    inv_denom = 1.0 / (dot00 * dot11 - dot01 * dot01)
    u = (dot11 * dot02 - dot01 * dot12) * inv_denom
    v = (dot00 * dot12 - dot01 * dot02) * inv_denom
    return u >= -1e-9 and v >= -1e-9 and u + v <= 1.0 + 1e-9


def assert_points_in_fov(points, fov, name):
    outside = [point for point in points if not point_in_triangle(point, fov)]
    if outside:
        raise ValueError(f"{name} outside FOV: {outside}")


def assert_points_outside_fov(points, fov, name):
    inside = [point for point in points if point_in_triangle(point, fov)]
    if inside:
        raise ValueError(f"{name} unexpectedly inside previous FOV: {inside}")


def draw_legend(ax):
    y = 0.915
    scatter_points(ax, [(0.145, y)], RED, size=26, zorder=10)
    add_text(ax, 0.165, y, "$t-1$ 可见点", size=8.2, color=COLORS["muted"], ha="left")

    scatter_points(ax, [(0.330, y)], GREEN, size=26, zorder=10)
    add_text(ax, 0.350, y, "$t$ 新增点", size=8.2, color=COLORS["muted"], ha="left")


def draw():
    fig, ax = plt.subplots(figsize=(7.4, 3.25))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Two shifted fields of view expose a larger part of the same static obstacle.
    fov_prev = [(0.31, 0.14), (0.11, 0.84), (0.68, 0.84)]
    fov_curr = [(0.51, 0.14), (0.29, 0.84), (0.88, 0.84)]
    for fov in (fov_prev, fov_curr):
        ax.add_patch(
            Polygon(
                fov,
                closed=True,
                facecolor=FOV_FILL,
                edgecolor=FOV_EDGE,
                alpha=0.23,
                linewidth=1.15,
                zorder=1,
            )
        )

    draw_sensor(ax, 0.31, 0.14, COLORS["orange"], "$t-1$")
    draw_sensor(ax, 0.51, 0.14, GREEN, "$t$")
    add_arrow(ax, (0.37, 0.105), (0.46, 0.105), color=COLORS["gray_dark"], lw=1.2, ms=10)
    add_text(ax, 0.415, 0.065, "视场移动", size=8.5, color=COLORS["muted"])

    obstacle_xy = (0.39, 0.505)
    obstacle_w, obstacle_h = 0.37, 0.155
    ax.add_patch(
        Rectangle(
            obstacle_xy,
            obstacle_w,
            obstacle_h,
            facecolor=OBSTACLE_FILL,
            edgecolor=OBSTACLE_EDGE,
            linewidth=1.2,
            zorder=3,
        )
    )

    prev_box_xy = (0.383, 0.515)
    prev_box_w, prev_box_h = 0.124, 0.170
    draw_detection_box(ax, prev_box_xy, prev_box_w, prev_box_h, RED, zorder=6)
    draw_detection_box(ax, (0.485, 0.445), 0.330, 0.270, GREEN, zorder=5)

    prev_points = [
        (0.398, 0.538),
        (0.414, 0.585),
        (0.432, 0.636),
        (0.451, 0.548),
        (0.466, 0.604),
        (0.486, 0.662),
        (0.501, 0.528),
        (0.502, 0.575),
        (0.505, 0.628),
        (0.405, 0.620),
        (0.423, 0.560),
        (0.438, 0.670),
        (0.458, 0.636),
        (0.475, 0.542),
        (0.494, 0.602),
    ]
    new_points = [
        (0.525, 0.528),
        (0.545, 0.565),
        (0.565, 0.606),
        (0.590, 0.646),
        (0.603, 0.532),
        (0.622, 0.585),
        (0.642, 0.632),
        (0.662, 0.518),
        (0.680, 0.565),
        (0.700, 0.618),
        (0.720, 0.662),
        (0.720, 0.548),
        (0.754, 0.602),
        (0.575, 0.542),
        (0.596, 0.598),
        (0.616, 0.656),
        (0.642, 0.548),
        (0.666, 0.604),
        (0.688, 0.648),
        (0.712, 0.532),
        (0.736, 0.586),
    ]
    prev_box_corners = [
        prev_box_xy,
        (prev_box_xy[0] + prev_box_w, prev_box_xy[1]),
        (prev_box_xy[0], prev_box_xy[1] + prev_box_h),
        (prev_box_xy[0] + prev_box_w, prev_box_xy[1] + prev_box_h),
    ]
    assert_points_in_fov(prev_points + prev_box_corners, fov_prev, "$t-1$ visible points")
    assert_points_in_fov(new_points, fov_curr, "$t$ new points")
    assert_points_outside_fov(new_points, fov_prev, "$t$ new points")

    scatter_points(ax, prev_points, RED)
    scatter_points(ax, new_points, GREEN)

    prev_center = (0.445, 0.580)
    curr_center = (0.638, 0.580)
    ax.scatter([prev_center[0]], [prev_center[1]], s=78, marker="*", color=RED, edgecolor="#ffffff", linewidth=0.6, zorder=8)
    ax.scatter([curr_center[0]], [curr_center[1]], s=78, marker="*", color=GREEN, edgecolor="#ffffff", linewidth=0.6, zorder=8)
    add_arrow(ax, (prev_center[0] + 0.026, prev_center[1]), (curr_center[0] - 0.026, curr_center[1]), color=COLORS["gray_dark"], lw=1.15, ms=10)
    add_text(ax, 0.541, 0.675, "$V_{box}$", size=8.9, color=COLORS["muted"])

    add_text(ax, 0.725, 0.405, "剔除", size=8.2, color=GREEN, bold=True)
    add_arrow(ax, (0.704, 0.425), (0.684, 0.515), color=GREEN, lw=1.1, ms=9)
    draw_legend(ax)

    save_figure(fig, "去除无效点云示意图")


if __name__ == "__main__":
    draw()
