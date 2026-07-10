# -*- coding: utf-8 -*-
"""绘制第五章：聚类算法示意图（K-Means 不同 k 效果 + K-Means/DBSCAN 对比）。

统一风格：共用 chap06_figure_utils 的配色、字体与保存约定，输出 PDF+PNG。
K-Means 与 DBSCAN 均以 numpy 手写实现，避免依赖 sklearn。
"""

import numpy as np
import matplotlib.pyplot as plt

from chap06_figure_utils import COLORS, FONT, save_figure


# 统一的簇配色循环（取自全书调色板）
CLUSTER_COLORS = [
    COLORS["blue"],
    COLORS["orange"],
    COLORS["green"],
    COLORS["red"],
    COLORS["purple"],
]
NOISE_COLOR = COLORS["gray_dark"]


# --------------------------------------------------------------------------
# 聚类算法（numpy 手写实现）
# --------------------------------------------------------------------------
def kmeans(X, k, iters=100, seed=0):
    rng = np.random.default_rng(seed)
    centers = X[rng.choice(len(X), k, replace=False)].copy()
    labels = np.zeros(len(X), dtype=int)
    for _ in range(iters):
        d = np.linalg.norm(X[:, None, :] - centers[None, :, :], axis=2)
        new_labels = d.argmin(axis=1)
        if np.array_equal(new_labels, labels):
            break
        labels = new_labels
        for j in range(k):
            if np.any(labels == j):
                centers[j] = X[labels == j].mean(axis=0)
    return labels, centers


def dbscan(X, eps, min_pts):
    n = len(X)
    labels = np.full(n, -1, dtype=int)      # -1 表示噪声/未分配
    visited = np.zeros(n, dtype=bool)
    D = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)
    cid = -1
    for i in range(n):
        if visited[i]:
            continue
        visited[i] = True
        neigh = np.where(D[i] <= eps)[0]
        if len(neigh) < min_pts:
            continue                        # 标记为噪声
        cid += 1
        labels[i] = cid
        queue = list(neigh)
        while queue:
            q = queue.pop()
            if not visited[q]:
                visited[q] = True
                q_neigh = np.where(D[q] <= eps)[0]
                if len(q_neigh) >= min_pts:
                    queue.extend(q_neigh.tolist())
            if labels[q] == -1:
                labels[q] = cid
    return labels


# --------------------------------------------------------------------------
# 数据集
# --------------------------------------------------------------------------
def make_blobs(seed=7):
    rng = np.random.default_rng(seed)
    centers = np.array([[-2.4, 2.2], [2.6, 2.6], [-2.6, -2.4],
                        [2.2, -2.2], [0.1, 0.0]])
    pts = []
    for c in centers:
        pts.append(rng.normal(c, 0.68, size=(46, 2)))
    return np.vstack(pts)


def make_moons(seed=3, n=140, noise=0.06, n_outliers=10):
    rng = np.random.default_rng(seed)
    t = np.linspace(0, np.pi, n // 2)
    outer = np.column_stack([np.cos(t), np.sin(t)])
    inner = np.column_stack([1 - np.cos(t), 1 - np.sin(t) - 0.5])
    X = np.vstack([outer, inner])
    X += rng.normal(0, noise, X.shape)
    # 注入若干离群噪声点，用于展示 DBSCAN 的噪声剔除能力
    lo = X.min(axis=0) - 0.3
    hi = X.max(axis=0) + 0.3
    outliers = rng.uniform(lo, hi, size=(n_outliers, 2))
    return np.vstack([X, outliers])


# --------------------------------------------------------------------------
# 通用面板样式
# --------------------------------------------------------------------------
def _style_axes(ax, title):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor(COLORS["gray_dark"])
        spine.set_linewidth(0.9)
    ax.set_facecolor("#fbfcfd")
    ax.grid(True, color=COLORS["gray"], linewidth=0.5, alpha=0.6)
    ax.set_axisbelow(True)
    ax.set_title(title, fontproperties=FONT, fontsize=12, color=COLORS["ink"], pad=6)


def _scatter_clusters(ax, X, labels, centers=None):
    uniq = sorted(set(labels.tolist()))
    for lb in uniq:
        m = labels == lb
        if lb == -1:
            ax.scatter(X[m, 0], X[m, 1], s=18, facecolor="none",
                       edgecolor=NOISE_COLOR, linewidth=0.8, marker="x", alpha=0.8)
        else:
            c = CLUSTER_COLORS[lb % len(CLUSTER_COLORS)]
            ax.scatter(X[m, 0], X[m, 1], s=20, color=c,
                       edgecolor="white", linewidth=0.4, alpha=0.92)
    if centers is not None:
        ax.scatter(centers[:, 0], centers[:, 1], s=180, marker="*",
                   color=COLORS["ink"], edgecolor="white", linewidth=0.9, zorder=5)


# --------------------------------------------------------------------------
# 图 1：K-Means 在不同 k 下的聚类效果（2x2 合并）
# --------------------------------------------------------------------------
def fig_kmeans():
    X = make_blobs()
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 6.6))
    for ax, k in zip(axes.ravel(), [2, 3, 4, 5]):
        labels, centers = kmeans(X, k, seed=2)
        _scatter_clusters(ax, X, labels, centers)
        _style_axes(ax, f"(k = {k})")
    fig.subplots_adjust(wspace=0.08, hspace=0.16)
    save_figure(fig, "K-Means聚类效果示意图")


# --------------------------------------------------------------------------
# 图 2：K-Means 与 DBSCAN 在非凸数据上的对比
# --------------------------------------------------------------------------
def fig_compare():
    X = make_moons()
    km_labels, km_centers = kmeans(X, 2, seed=1)
    db_labels = dbscan(X, eps=0.22, min_pts=5)

    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.9))
    _scatter_clusters(axes[0], X, km_labels, km_centers)
    _style_axes(axes[0], "(a) K-Means（非凸数据被错误切分）")
    _scatter_clusters(axes[1], X, db_labels)
    _style_axes(axes[1], "(b) DBSCAN（正确识别 + 剔除噪声）")
    fig.subplots_adjust(wspace=0.12)
    save_figure(fig, "聚类效果对比示意图")


def main():
    fig_kmeans()
    fig_compare()


if __name__ == "__main__":
    main()
