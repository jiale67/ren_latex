"""
Generate Fig. for Chapter 5 §5.4.2:
    Two-stage ICP initial alignment between the start-up accumulated source
    point cloud and the offline pre-built PCD map.

Layout (1 x 4 composite):
    (a) approximate initial pose      — obvious R/t bias
    (b) ICP iteration                 — nearest-neighbour correspondences
    (c) converged alignment           — T* applied, written into filter state
    (d) residual RMSE vs iteration    — convergence curve

Run:  python draw_icp_alignment.py
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ── font / dpi ────────────────────────────────────────────────────────────────
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
DPI = 300

# ── colour palette (aligned with draw_chap05_figs.py) ─────────────────────────
C_MAP    = '#9DB6CC'   # pre-built map points (cool grey-blue, secondary)
C_SRC    = '#E07B39'   # source cloud, mis-aligned (signal — sensor input)
C_FINAL  = '#2E8B57'   # converged source cloud (validated output)
C_LINK   = '#7B5EA7'   # NN correspondence lines (purple, optimisation)
C_BLUE   = '#2C6FAC'   # convergence curve
C_GRAY   = '#888888'


# ── 1. synthetic 2-D scene: indoor corridor + columns + partition ─────────────
def make_scene(rng):
    pts = []
    # outer walls (rectangular room ~12 x 8)
    for x in np.linspace(-6, 6, 220):
        pts.append([x,  4.0])
        pts.append([x, -4.0])
    for y in np.linspace(-4, 4, 150):
        pts.append([-6.0, y])
        pts.append([ 6.0, y])
    # two equipment columns
    for ang in np.linspace(0, 2 * np.pi, 70, endpoint=False):
        pts.append([ 1.6 + 0.55 * np.cos(ang),  1.1 + 0.55 * np.sin(ang)])
        pts.append([-2.2 + 0.45 * np.cos(ang), -1.0 + 0.45 * np.sin(ang)])
    # internal partition (L-shape)
    for x in np.linspace(-4.0, -2.0, 35):
        pts.append([x, 2.4])
    for y in np.linspace(0.2, 2.4, 32):
        pts.append([-4.0, y])
    pts = np.array(pts)
    pts += rng.normal(0, 0.04, pts.shape)
    return pts


def downsample(arr, n, rng):
    if len(arr) <= n:
        return arr
    idx = rng.choice(len(arr), size=n, replace=False)
    return arr[idx]


# ── 2. minimal 2-D point-to-point ICP ─────────────────────────────────────────
def nearest_neighbour(src, tgt):
    diffs = src[:, None, :] - tgt[None, :, :]
    dists = np.linalg.norm(diffs, axis=-1)
    idx = np.argmin(dists, axis=1)
    return idx, dists[np.arange(len(src)), idx]


def icp_2d(src, tgt, max_iter=12):
    src_cur = src.copy()
    history = [src_cur.copy()]
    residuals = []
    for _ in range(max_iter):
        idx, d = nearest_neighbour(src_cur, tgt)
        residuals.append(float(np.sqrt((d ** 2).mean())))
        m_s = src_cur.mean(axis=0)
        m_t = tgt[idx].mean(axis=0)
        H = (src_cur - m_s).T @ (tgt[idx] - m_t)
        U, _, Vt = np.linalg.svd(H)
        D = np.diag([1.0, np.sign(np.linalg.det(Vt.T @ U.T))])
        R = Vt.T @ D @ U.T
        t = m_t - R @ m_s
        src_cur = (R @ src_cur.T).T + t
        history.append(src_cur.copy())
    idx, d = nearest_neighbour(src_cur, tgt)
    residuals.append(float(np.sqrt((d ** 2).mean())))
    return history, residuals


# ── 3. main figure ────────────────────────────────────────────────────────────
def fig_icp_alignment():
    rng = np.random.default_rng(7)
    full = make_scene(rng)

    # source = subset of the map (start-up FoV is partial), then perturb
    mask = (full[:, 0] > -4.2) & (full[:, 0] < 4.0) & \
           (full[:, 1] > -3.0) & (full[:, 1] < 3.4)
    src_gt = downsample(full[mask], 220, rng)
    map_pts = downsample(full, 460, rng)

    # apply initial misalignment to source (approximate prior)
    theta0 = np.deg2rad(26)
    R0 = np.array([[np.cos(theta0), -np.sin(theta0)],
                   [np.sin(theta0),  np.cos(theta0)]])
    t0 = np.array([0.75, 0.55])
    src_init = (R0 @ src_gt.T).T + t0

    history, residuals = icp_2d(src_init, map_pts, max_iter=12)
    src_mid   = history[3]
    src_final = history[-1]

    # ── canvas ────────────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(13.6, 4.0))
    gs = fig.add_gridspec(1, 3, wspace=0.05,
                          left=0.02, right=0.98,
                          top=0.97, bottom=0.20)
    axes = [fig.add_subplot(gs[0, i]) for i in range(3)]

    # ── (a) approximate initial pose ──────────────────────────────────────────
    ax = axes[0]
    ax.scatter(map_pts[:, 0], map_pts[:, 1], s=2.0, c=C_MAP, alpha=0.85)
    ax.scatter(src_init[:, 0], src_init[:, 1], s=5.0, c=C_SRC, alpha=0.90)

    # ── (b) ICP iteration with NN correspondences ─────────────────────────────
    ax = axes[1]
    ax.scatter(map_pts[:, 0], map_pts[:, 1], s=2.0, c=C_MAP, alpha=0.85)
    ax.scatter(src_mid[:, 0], src_mid[:, 1], s=5.0, c=C_SRC, alpha=0.90)
    # subsampled correspondences
    idx_mid, _ = nearest_neighbour(src_mid, map_pts)
    sel = np.linspace(0, len(src_mid) - 1, 45, dtype=int)
    for i in sel:
        ax.plot([src_mid[i, 0], map_pts[idx_mid[i], 0]],
                [src_mid[i, 1], map_pts[idx_mid[i], 1]],
                color=C_LINK, lw=0.55, alpha=0.65, zorder=2)

    # ── (c) converged alignment ───────────────────────────────────────────────
    ax = axes[2]
    ax.scatter(map_pts[:, 0], map_pts[:, 1], s=2.0, c=C_MAP, alpha=0.85)
    ax.scatter(src_final[:, 0], src_final[:, 1], s=5.0, c=C_FINAL, alpha=0.90)

    # uniform style for the three scene panels (no frame, tight extent)
    for ax in axes:
        ax.set_aspect('equal')
        ax.set_xlim(-7.0, 7.0)
        ax.set_ylim(-4.9, 4.9)
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(False)

    # ── subfigure labels below each panel ─────────────────────────────────────
    labels = ['(a)', '(b)', '(c)']
    for ax, lbl in zip(axes, labels):
        ax.text(0.5, -0.06, lbl, ha='center', va='top',
                transform=ax.transAxes, fontsize=11, fontweight='bold')

    # ── arrows centred in the gaps between panels ─────────────────────────────
    from matplotlib.patches import FancyArrowPatch
    fig.canvas.draw()  # finalise layout so positions are exact
    y_c = 0.5 * (axes[0].get_position().y0 + axes[0].get_position().y1)
    for left_ax, right_ax in [(axes[0], axes[1]), (axes[1], axes[2])]:
        x_l = left_ax.get_position().x1
        x_r = right_ax.get_position().x0
        x_mid = 0.5 * (x_l + x_r)
        half = 0.016
        arr = FancyArrowPatch((x_mid - half, y_c), (x_mid + half, y_c),
                              transform=fig.transFigure,
                              arrowstyle='-|>', mutation_scale=22,
                              lw=2.2, color='#555555', zorder=10,
                              clip_on=False)
        fig.add_artist(arr)

    # ── unified legend (coloured dots) at the bottom ──────────────────────────
    from matplotlib.lines import Line2D
    def dot(color, label, ms):
        return Line2D([0], [0], marker='o', color='none',
                      markerfacecolor=color, markeredgecolor='none',
                      markersize=ms, label=label)
    legend_elements = [
        dot(C_MAP,   r'预建PCD地图', 8),
        dot(C_SRC,   r'累积源点云', 8),
        dot(C_FINAL, r'对齐后源点云', 8),
    ]
    fig.legend(handles=legend_elements, loc='lower center',
               ncol=3, fontsize=9.5, frameon=False,
               handletextpad=0.4, columnspacing=2.0,
               bbox_to_anchor=(0.5, 0.015))

    out_pdf = 'd:/大论文仓库/ren_latex/pic/两阶段ICP初始对齐.pdf'
    out_eps = out_pdf.replace('.pdf', '.eps')
    fig.savefig(out_pdf, dpi=DPI, bbox_inches='tight', facecolor='white')
    fig.savefig(out_eps, dpi=DPI, bbox_inches='tight', facecolor='white',
                format='eps')
    plt.close(fig)
    print(f'Saved: {out_pdf}')
    print(f'Saved: {out_eps}')


if __name__ == '__main__':
    fig_icp_alignment()
    print('Done.')
