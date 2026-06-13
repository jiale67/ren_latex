"""
Generate three publication-quality figures for Chapter 5 (FAST_LIO2).
Run with:  python draw_chap05_figs.py
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# ── font setup ────────────────────────────────────────────────────────────────
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
DPI = 300

# ── colour palette (colourblind-friendly) ──────────────────────────────────────
C_BLUE   = '#2C6FAC'   # core / proposed path
C_GREEN  = '#2E8B57'   # output / validated
C_ORANGE = '#E07B39'   # sensor input
C_GRAY   = '#B0B8C1'   # secondary / infra
C_RED    = '#C0392B'   # warning / fallback
C_PURPLE = '#7B5EA7'   # optimisation
C_LBLUE  = '#D6E8F7'   # light fill for blue
C_LGRAY  = '#F0F2F4'   # light fill for gray
C_LGREEN = '#D5EDE3'   # light fill for green
C_LORANGE= '#FCE8D8'   # light fill for orange

def box(ax, x, y, w, h, label, fc, ec, fs=9, bold=False,
        tc='white', radius=0.04):
    rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                          boxstyle=f"round,pad=0.02,rounding_size={radius}",
                          fc=fc, ec=ec, lw=1.5, zorder=3)
    ax.add_patch(rect)
    weight = 'bold' if bold else 'normal'
    ax.text(x, y, label, ha='center', va='center',
            fontsize=fs, color=tc, fontweight=weight, zorder=4,
            multialignment='center')

def arrow(ax, x1, y1, x2, y2, color='#555555', lw=1.4, style='->', shrink=4):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color,
                                lw=lw, shrinkA=shrink, shrinkB=shrink))

def label_arrow(ax, x, y, text, fs=7.5, color='#444444'):
    ax.text(x, y, text, ha='center', va='center',
            fontsize=fs, color=color, zorder=5)

# ══════════════════════════════════════════════════════════════════════════════
# Figure 1: SLAM System Architecture
# ══════════════════════════════════════════════════════════════════════════════
def fig1_slam_arch():
    fig, ax = plt.subplots(figsize=(13, 8))
    ax.set_xlim(0, 13); ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_facecolor('white'); fig.patch.set_facecolor('white')

    # ── title ─────────────────────────────────────────────────────────────────
    ax.text(6.5, 7.65, 'SLAM 系统架构与技术分类',
            ha='center', va='center', fontsize=13, fontweight='bold',
            color='#1a1a2e')

    # ── sensor row ────────────────────────────────────────────────────────────
    box(ax, 3.0, 7.0, 2.4, 0.65, '激光雷达 (LiDAR)\n点云序列', C_ORANGE, C_ORANGE, fs=8.5, tc='white')
    box(ax, 6.5, 7.0, 2.0, 0.65, 'IMU\n角速度 / 加速度', C_ORANGE, C_ORANGE, fs=8.5, tc='white')
    box(ax, 10.0,7.0, 2.4, 0.65, '视觉相机 / 其他\n（可选）', C_GRAY, C_GRAY, fs=8.5, tc='white')

    # ── front-end block ────────────────────────────────────────────────────────
    box(ax, 6.5, 5.8, 11.0, 1.0, '', C_LBLUE, C_BLUE, tc='black', radius=0.06)
    ax.text(6.5, 6.05, '前端里程计（Front-end Odometry）',
            ha='center', va='center', fontsize=10, fontweight='bold', color=C_BLUE)
    ax.text(6.5, 5.62,
            '相邻帧数据关联 · 增量运动估计 · 局部轨迹/地图生成（误差随时间累积）',
            ha='center', va='center', fontsize=8.5, color='#333333')

    # sub-types of front-end
    box(ax, 2.2,  5.05, 2.8, 0.60, '激光雷达 SLAM\n(LiDAR SLAM)', C_BLUE, C_BLUE, fs=8, tc='white')
    box(ax, 5.3,  5.05, 2.8, 0.60, '视觉 SLAM\n(Visual SLAM)',    C_BLUE, C_BLUE, fs=8, tc='white')
    box(ax, 8.5,  5.05, 3.4, 0.60, '多传感器融合 SLAM\n(Multi-sensor Fusion)', C_BLUE, C_BLUE, fs=8, tc='white')
    box(ax, 11.6, 5.05, 2.0, 0.60, '紧耦合 LiDAR-IMU\n(FAST-LIO2 ★)', C_RED, C_RED, fs=8, tc='white')

    # back-end group
    box(ax, 3.5, 3.85, 5.0, 0.80,
        '基于滤波器的 SLAM\nEKF / FastSLAM / IEKF', C_PURPLE, C_PURPLE, fs=8.5, tc='white')
    box(ax, 9.5, 3.85, 5.0, 0.80,
        '基于图优化的 SLAM\ng2o / GTSAM / Ceres', C_PURPLE, C_PURPLE, fs=8.5, tc='white')

    ax.text(6.5, 4.40, '后端优化（Back-end Optimization）',
            ha='center', va='center', fontsize=10, fontweight='bold', color=C_PURPLE)
    rect_be = FancyBboxPatch((1.0, 3.38), 11.0, 1.28,
                             boxstyle='round,pad=0.02,rounding_size=0.06',
                             fc='#F0EAF8', ec=C_PURPLE, lw=1.5, zorder=2)
    ax.add_patch(rect_be)

    # mapping
    box(ax, 6.5, 2.5, 5.5, 0.70,
        '建图模块（Mapping）\n占据栅格地图 / 点云地图 / 体素地图', C_GREEN, C_GREEN, fs=8.5, tc='white')

    # loop closure
    box(ax, 6.5, 1.5, 5.5, 0.70,
        '回环检测（Loop Closure Detection）\n全局描述子匹配 · 添加回环约束', C_GRAY, '#666', fs=8.5, tc='white')

    # output
    box(ax, 6.5, 0.5, 7.0, 0.65,
        '输出：全局一致轨迹 + 环境地图（定位 / 导航 / 感知）', C_GREEN, C_GREEN, fs=9, tc='white', bold=True)

    # ── arrows ─────────────────────────────────────────────────────────────────
    for sx in [3.0, 6.5, 10.0]:
        arrow(ax, sx, 6.67, sx, 6.32, color=C_ORANGE)

    # sensors -> front-end (merge)
    arrow(ax, 6.5, 6.32, 6.5, 6.32, color='#aaa')  # dummy

    # front-end -> backend
    arrow(ax, 6.5, 5.3, 6.5, 4.70, color=C_BLUE, lw=1.6)
    label_arrow(ax, 5.6, 5.02, '位姿估计 +\n局部约束', fs=7)

    # backend -> mapping
    arrow(ax, 6.5, 3.38, 6.5, 2.88, color=C_PURPLE, lw=1.6)
    label_arrow(ax, 5.6, 3.12, '优化轨迹', fs=7)

    # loop closure -> backend (curved)
    ax.annotate('', xy=(3.0, 3.38), xytext=(3.0, 1.5),
                arrowprops=dict(arrowstyle='->', color=C_GRAY, lw=1.4,
                                connectionstyle='arc3,rad=-0.3'))
    ax.text(1.5, 2.5, '回环约束', ha='center', va='center',
            fontsize=7.5, color='#666666', rotation=90)

    # mapping -> output
    arrow(ax, 6.5, 2.15, 6.5, 0.85, color=C_GREEN, lw=1.6)

    # loop closure horizontal arrow from mapping
    arrow(ax, 6.5, 2.15, 6.5, 1.87, color='#aaa', lw=0.5)
    arrow(ax, 6.5, 1.87, 6.5, 1.87, color='#aaa', lw=0.5)

    # mapping to loop closure
    arrow(ax, 5.5, 2.15, 5.5, 1.87, color='#aaa', lw=1.0)

    plt.tight_layout(pad=0.3)
    path = 'd:/大论文仓库/ren_latex/pic/SLAM系统架构图.pdf'
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor='white')
    path2 = path.replace('.pdf', '.eps')
    fig.savefig(path2, dpi=DPI, bbox_inches='tight', facecolor='white',
                format='eps')
    print(f'Saved: {path}  &  {path2}')
    plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# Figure 2: FAST_LIO2 Processing Pipeline
# ══════════════════════════════════════════════════════════════════════════════
def fig2_fastlio2_pipeline():
    fig, ax = plt.subplots(figsize=(14, 5.5))
    ax.set_xlim(0, 14); ax.set_ylim(0, 5.5)
    ax.axis('off')
    ax.set_facecolor('white'); fig.patch.set_facecolor('white')

    ax.text(7.0, 5.2, 'FAST-LIO2 系统处理流程',
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1a1a2e')

    # ── input sensors (top) ────────────────────────────────────────────────────
    box(ax, 1.5, 4.3, 2.4, 0.75, 'IMU 测量\n(~200 Hz)', C_ORANGE, C_ORANGE, fs=8.5, tc='white')
    box(ax, 4.3, 4.3, 2.4, 0.75, '激光雷达点云\n(10–20 Hz)', C_ORANGE, C_ORANGE, fs=8.5, tc='white')

    # ── step 1: IMU propagation ────────────────────────────────────────────────
    box(ax, 1.5, 3.0, 2.4, 0.90,
        'IMU 状态传播\n前向积分\n(预测位姿/速度/偏置)', C_BLUE, C_BLUE, fs=8, tc='white')

    # ── step 2: undistortion ──────────────────────────────────────────────────
    box(ax, 4.3, 3.0, 2.4, 0.90,
        '运动畸变补偿\n逐点时间戳对齐\n统一到帧末时刻', C_BLUE, C_BLUE, fs=8, tc='white')

    # ── step 3: voxel downsample ──────────────────────────────────────────────
    box(ax, 7.0, 3.0, 2.2, 0.90,
        '体素降采样\n点云坐标变换\n(激光→世界坐标系)', C_BLUE, C_BLUE, fs=8, tc='white')

    # ── step 4: ikd-Tree ──────────────────────────────────────────────────────
    box(ax, 9.7, 3.0, 2.2, 0.90,
        'ikd-Tree 近邻搜索\n局部平面拟合\n点到平面残差', C_PURPLE, C_PURPLE, fs=8, tc='white')

    # ── step 5: IEKF update ───────────────────────────────────────────────────
    box(ax, 12.4, 3.0, 2.4, 0.90,
        'IEKF 状态更新\n流形迭代误差修正\n收敛判断', C_GREEN, C_GREEN, fs=8, tc='white')

    # ── output ────────────────────────────────────────────────────────────────
    box(ax, 12.4, 1.7, 2.4, 0.75,
        '状态输出\n位姿 / 速度 / 偏置', C_GREEN, C_GREEN, fs=8.5, tc='white', bold=True)

    # ── ikd-Tree map box (bottom) ──────────────────────────────────────────────
    box(ax, 7.0, 1.7, 4.5, 0.75,
        'ikd-Tree 增量地图\n（插入 · 删除 · 重平衡 · 近邻搜索）',
        C_LGRAY, '#888', fs=8.5, tc='#333')

    # ── arrows ─────────────────────────────────────────────────────────────────
    # sensors to steps
    arrow(ax, 1.5, 3.93, 1.5, 3.48, color=C_ORANGE)
    arrow(ax, 4.3, 3.93, 4.3, 3.48, color=C_ORANGE)

    # pipeline
    for x1, x2 in [(2.72, 3.10), (5.52, 5.90), (8.12, 8.60), (10.82, 11.20)]:
        arrow(ax, x1, 3.0, x2, 3.0, color=C_BLUE, lw=1.8)

    # IMU → undistortion (IMU传播结果用于去畸变)
    ax.annotate('', xy=(3.10, 3.18), xytext=(2.72, 3.18),
                arrowprops=dict(arrowstyle='->', color='#aaa', lw=1.0,
                                connectionstyle='arc3,rad=0'))

    # ikd-Tree map ↔ step 4
    arrow(ax, 9.7, 2.55, 9.7, 2.10, color='#888', lw=1.2)
    ax.text(10.5, 1.88, '近邻查询', ha='left', va='center', fontsize=7.5, color='#666')

    # After IEKF: map update
    ax.annotate('', xy=(9.47, 1.72), xytext=(12.2, 2.56),
                arrowprops=dict(arrowstyle='->', color='#888', lw=1.0,
                                connectionstyle='arc3,rad=0.25'))
    ax.text(10.9, 2.0, '增量插入', ha='center', va='center', fontsize=7.5, color='#666')

    # IEKF → output
    arrow(ax, 12.4, 2.55, 12.4, 2.10, color=C_GREEN, lw=1.6)

    # ── state vector annotation ────────────────────────────────────────────────
    sv_box = FancyBboxPatch((0.1, 0.15), 13.8, 1.15,
                            boxstyle='round,pad=0.03,rounding_size=0.05',
                            fc='#F8F9FA', ec='#CCCCCC', lw=1.2, zorder=1)
    ax.add_patch(sv_box)
    ax.text(7.0, 1.0, r'状态向量  $\mathbf{x}$  =  [${}^G\mathbf{p}_I$,  ${}^G\mathbf{R}_I$,  ${}^I\mathbf{R}_L$,  ${}^I\mathbf{p}_L$,  ${}^G\mathbf{v}_I$,  $\mathbf{b}_g$,  $\mathbf{b}_a$,  ${}^G\mathbf{g}$]',
            ha='center', va='center', fontsize=9, color='#333', style='italic')
    ax.text(7.0, 0.50,
            '位置  ·  姿态  ·  激光-IMU外参  ·  速度  ·  陀螺仪偏置  ·  加速度计偏置  ·  重力向量',
            ha='center', va='center', fontsize=8, color='#666')

    plt.tight_layout(pad=0.3)
    path = 'd:/大论文仓库/ren_latex/pic/FAST_LIO2系统流程图.pdf'
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor='white')
    path2 = path.replace('.pdf', '.eps')
    fig.savefig(path2, dpi=DPI, bbox_inches='tight', facecolor='white', format='eps')
    print(f'Saved: {path}  &  {path2}')
    plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# Figure 3: Pre-built Map Localisation Framework
# ══════════════════════════════════════════════════════════════════════════════
def fig3_map_localisation():
    fig, ax = plt.subplots(figsize=(13, 8.5))
    ax.set_xlim(0, 13); ax.set_ylim(0, 8.5)
    ax.axis('off')
    ax.set_facecolor('white'); fig.patch.set_facecolor('white')

    ax.text(6.5, 8.2, '基于预建地图的 FAST-LIO2 定位框架',
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1a1a2e')

    # ── inputs (left column) ──────────────────────────────────────────────────
    box(ax, 1.4, 7.2, 2.4, 0.70, 'LiDAR 点云\n+ IMU 数据', C_ORANGE, C_ORANGE, fs=8.5, tc='white')
    box(ax, 1.4, 5.9, 2.4, 0.70, '预建 PCD 地图\n（离线构建）', C_BLUE, C_BLUE, fs=8.5, tc='white')
    box(ax, 1.4, 4.6, 2.4, 0.70, '近似初始位姿\n（人工/任务先验）', C_GRAY, '#666', fs=8.5, tc='white')

    # ── phase A: initialisation ────────────────────────────────────────────────
    rect_a = FancyBboxPatch((3.5, 3.8), 5.2, 3.9,
                            boxstyle='round,pad=0.03,rounding_size=0.07',
                            fc='#EAF3FC', ec=C_BLUE, lw=1.8, zorder=2)
    ax.add_patch(rect_a)
    ax.text(6.1, 7.55, '阶段 A：初始化', ha='center', va='center',
            fontsize=10, fontweight='bold', color=C_BLUE)

    box(ax, 6.1, 7.0, 4.4, 0.70,
        '地图加载 & 体素降采样\n构建 ikd-Tree 空间索引', C_BLUE, C_BLUE, fs=8.5, tc='white')
    box(ax, 6.1, 6.0, 4.4, 0.70,
        'IMU 静态初始化\n估计重力方向 / 偏置 / 协方差\n累积激光帧作源点云', C_BLUE, C_BLUE, fs=8, tc='white')
    box(ax, 6.1, 4.95, 4.4, 0.80,
        '两阶段初始对齐\n① 近似初值 → ② ICP 精配准\n得到 $T^*$，写入滤波器状态', C_BLUE, C_BLUE, fs=8, tc='white')

    # ICP fail branch
    box(ax, 6.1, 3.95, 3.0, 0.60,
        '配准失败 → 退化为 SLAM 模式\n或等待更好初值', C_RED, C_RED, fs=7.5, tc='white')

    # ── phase B: online localisation ──────────────────────────────────────────
    rect_b = FancyBboxPatch((3.5, 0.7), 5.2, 2.8,
                            boxstyle='round,pad=0.03,rounding_size=0.07',
                            fc='#EAF8F0', ec=C_GREEN, lw=1.8, zorder=2)
    ax.add_patch(rect_b)
    ax.text(6.1, 3.42, '阶段 B：在线定位', ha='center', va='center',
            fontsize=10, fontweight='bold', color=C_GREEN)

    box(ax, 6.1, 2.95, 4.4, 0.70,
        'IMU 传播 + 点云去畸变', C_GREEN, C_GREEN, fs=8.5, tc='white')
    box(ax, 6.1, 2.05, 4.4, 0.70,
        '点云变换 → 地图坐标系\nikd-Tree 近邻搜索 & 局部平面拟合', C_GREEN, C_GREEN, fs=8.5, tc='white')
    box(ax, 6.1, 1.10, 4.4, 0.70,
        'IEKF 状态更新\n输出全局位姿（连续）', C_GREEN, C_GREEN, fs=8.5, tc='white')

    # ── right side: two modes ─────────────────────────────────────────────────
    box(ax, 11.0, 5.9, 3.0, 1.10,
        '纯定位模式\n地图固定，不更新\n适合固定巡检路线', C_BLUE, C_BLUE, fs=8, tc='white')
    box(ax, 11.0, 4.35, 3.0, 1.10,
        '混合建图模式\n定位稳定后增量更新\n适合地图扩展任务', C_GREEN, C_GREEN, fs=8, tc='white')

    # ── output ────────────────────────────────────────────────────────────────
    box(ax, 11.0, 2.6, 3.0, 0.90,
        '输出\n全局位姿 + 连续轨迹\n供规划/感知/控制使用',
        C_GREEN, C_GREEN, fs=8.5, tc='white', bold=True)

    # ── arrows ─────────────────────────────────────────────────────────────────
    # inputs → phase A
    arrow(ax, 2.62, 7.2,  3.85, 7.2,  color=C_ORANGE)
    arrow(ax, 2.62, 5.9,  3.85, 6.3,  color=C_BLUE)
    arrow(ax, 2.62, 4.6,  3.85, 5.2,  color='#888')

    # within phase A
    arrow(ax, 6.1, 6.65, 6.1, 6.38, color=C_BLUE, lw=1.6)
    arrow(ax, 6.1, 5.65, 6.1, 5.38, color=C_BLUE, lw=1.6)
    # ICP fail
    arrow(ax, 6.1, 4.55, 6.1, 4.28, color=C_RED, lw=1.2)

    # phase A → phase B (success path)
    ax.annotate('', xy=(6.1, 3.33), xytext=(6.1, 4.55),
                arrowprops=dict(arrowstyle='->', color=C_GREEN, lw=1.8))
    ax.text(6.9, 3.9, '初始化\n成功', ha='left', va='center',
            fontsize=8, color=C_GREEN)

    # within phase B
    arrow(ax, 6.1, 2.60, 6.1, 2.43, color=C_GREEN, lw=1.6)
    arrow(ax, 6.1, 1.70, 6.1, 1.48, color=C_GREEN, lw=1.6)

    # feedback loop (IEKF → IMU propagation)
    ax.annotate('', xy=(3.7, 2.95), xytext=(3.7, 1.1),
                arrowprops=dict(arrowstyle='->', color='#aaa', lw=1.1,
                                connectionstyle='arc3,rad=-0.3'))
    ax.text(2.8, 2.1, '持续\n循环', ha='center', va='center',
            fontsize=8, color='#888')

    # phase B → modes
    arrow(ax, 8.72, 1.10, 9.4, 5.0, color='#888', lw=1.0)
    arrow(ax, 9.4, 5.0, 9.52, 5.9, color=C_BLUE, lw=1.2)
    arrow(ax, 9.4, 5.0, 9.52, 4.35, color=C_GREEN, lw=1.2)

    # modes → output
    arrow(ax, 11.0, 4.82, 11.0, 3.08, color='#888', lw=1.2)

    plt.tight_layout(pad=0.3)
    path = 'd:/大论文仓库/ren_latex/pic/预建地图定位框架图.pdf'
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor='white')
    path2 = path.replace('.pdf', '.eps')
    fig.savefig(path2, dpi=DPI, bbox_inches='tight', facecolor='white', format='eps')
    print(f'Saved: {path}  &  {path2}')
    plt.close(fig)


if __name__ == '__main__':
    fig1_slam_arch()
    fig2_fastlio2_pipeline()
    fig3_map_localisation()
    print('All done.')

