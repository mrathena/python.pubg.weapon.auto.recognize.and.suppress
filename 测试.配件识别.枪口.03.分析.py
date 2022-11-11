import os

import cv2
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt


def load(directory):
    """
    递归载入指定路径下的所有图片(灰度化二值化), 按照 (name, img) 的格式组合成为列表并返回
    """
    imgs = []
    for item in os.listdir(directory):
        # item, 不包含路径前缀
        # path, 完整路径
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            temp = load(path)
            imgs.extend(temp)
        elif os.path.isfile(path):
            name = os.path.splitext(item)[0]
            # 读取图片并灰度化
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            # pathname = os.path.join(directory, '_gray_' + name + '.jpg')
            # cv2.imwrite(pathname, img)
            # 二值化
            _, img = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY)
            imgs.append((name, img))
    return imgs if imgs else None


rets = load(r'image/3440.1440/weapon.attachment/muzzle')
imgs = [img for name, img in rets]

row = 11
col = 11
counter = 0
zeros = np.zeros(imgs[0].shape[:2], dtype="uint8")
plt.figure(figsize=(15, 10))

for name, img1 in rets:
    for name2, img2 in rets:
        counter += 1
        temp = cv2.merge([zeros, img1, img2])
        temp = cv2.cvtColor(temp, cv2.COLOR_BGR2RGB)
        # temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
        plt.subplot(row, col, counter)
        plt.imshow(temp, cmap='gray')

plt.show()
