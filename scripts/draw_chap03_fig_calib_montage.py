# -*- coding: utf-8 -*-
"""绘制第三章：标定图像采集拼图。

使用指定的6张红外标定图，拼成 2x3 蒙太奇，
展示棋盘格在不同角度/距离/位置下的采集样本。
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from chap06_figure_utils import FONT, save_figure


ROOT = Path(__file__).resolve().parents[2]  # d:\大论文仓库
CALIB_DIR = ROOT / "calib" / "calib_ir"


def main():
    # 用户指定的6张图像文件名
    filenames = [
        "ir_1782962852761_000012.png",  # 正对近距
        "ir_1782962896868_000018.png",  # 左倾
        "ir_1782962884889_000015.png",  # 右倾
        "ir_1782962874320_000014.png",  # 上下倾
        "ir_1782963089732_000037.png",  # 画面边缘
        "ir_1782963066904_000035.png",  # 远距
    ]

    labels = ["正对近距", "左倾", "右倾", "上下倾", "画面边缘", "远距"]

    images = []
    for fname in filenames:
        path = CALIB_DIR / fname
        if not path.exists():
            print(f"警告：图像不存在 {path}")
            images.append(None)
        else:
            images.append(np.asarray(Image.open(path).convert("L")))

    fig, axes = plt.subplots(2, 3, figsize=(9.2, 5.0))
    for i, ax in enumerate(axes.flat):
        if i < len(images) and images[i] is not None:
            ax.imshow(images[i], cmap="gray")
            ax.set_title(f"({chr(97+i)}) {labels[i]}", fontproperties=FONT, fontsize=11)
        ax.axis("off")

    fig.subplots_adjust(wspace=0.05, hspace=0.15)
    save_figure(fig, "红外相机标定图像采集")


if __name__ == "__main__":
    main()
