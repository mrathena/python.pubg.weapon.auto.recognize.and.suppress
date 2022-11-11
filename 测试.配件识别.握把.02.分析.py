import os

import cv2
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
            img = cv2.imread(path)
            imgs.append((name, img))
    return imgs if imgs else None


rets = load(r'image/3440.1440/weapon.attachment/foregrip')
row = 7
col = 12
counter = 0
plt.figure(figsize=(19, 10))
for name, img in rets:

    counter += 1
    original = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.subplot(row, col, counter)
    plt.imshow(original, cmap='gray')

    counter += 1
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plt.subplot(row, col, counter)
    plt.imshow(gray, cmap='gray')

    counter += 1
    _, img = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')

    counter += 1
    _, img = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')

    counter += 1
    _, img = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')

    counter += 1
    _, img = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')

    counter += 1
    _, img = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')

    counter += 1
    _, img = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')

    counter += 1
    _, img = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')

    counter += 1
    img = cv2.adaptiveThreshold(gray, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=11, C=1)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')

    counter += 1
    img = cv2.adaptiveThreshold(gray, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=3, C=1)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')

    counter += 1
    img = cv2.adaptiveThreshold(gray, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=33, C=1)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')

plt.show()
