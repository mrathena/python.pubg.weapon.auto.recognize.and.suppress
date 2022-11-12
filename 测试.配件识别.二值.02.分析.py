import cv2
import matplotlib

matplotlib.use('TkAgg')
from matplotlib import pyplot as plt


from toolkit import Game


rets = Game.Image.load(r'image/3440.1440/weapon.attachment/test.binary')
row = 11  # 有几张图片这里就写几
col = 24
counter = 0
plt.figure(figsize=(25, 12))
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
    plt.subplot(row, col, counter)
    plt.imshow(original, cmap='gray')

    counter += 1
    plt.subplot(row, col, counter)
    plt.imshow(gray, cmap='gray')

    counter += 1
    _, img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')

    counter += 1
    _, img = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')

    counter += 1
    _, img = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')

    counter += 1
    _, img = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')

    counter += 1
    _, img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')

    counter += 1
    plt.subplot(row, col, counter)
    plt.imshow(original, cmap='gray')

    counter += 1
    plt.subplot(row, col, counter)
    plt.imshow(gray, cmap='gray')

    counter += 1
    img = cv2.adaptiveThreshold(gray, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=11, C=1)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')

    counter += 1
    img = cv2.adaptiveThreshold(gray, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=9, C=1)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')

    counter += 1
    img = cv2.adaptiveThreshold(gray, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=7, C=1)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')

    counter += 1
    img = cv2.adaptiveThreshold(gray, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=5, C=1)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')

    counter += 1
    img = cv2.adaptiveThreshold(gray, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=3, C=1)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')

    counter += 1
    # 自适应二值化
    img = cv2.adaptiveThreshold(gray, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=3, C=1)
    # 全局二值化, 消除自适应二值化后的多值问题(不仅是0和255)
    # _, img = cv2.threshold(img, 254, 255, cv2.THRESH_BINARY)  # 非255全改0
    # 消除二值图像孤立点
    # img = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)  # 降噪, 对单独的黑点不管用
    # img = morphology.remove_small_objects(img, 10)  # numpy 中的值必须是 True / False 才能消除, 也就是需要转换二值图像
    img = Game.Image.remove_small_objects(img, 10)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')

plt.show()
