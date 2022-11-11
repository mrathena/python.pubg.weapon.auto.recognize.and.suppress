import cv2
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt


from toolkit import Game


rets = Game.Image.load(r'image/3440.1440/weapon.attachment/foregrip')
row = 7
col = 11
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

plt.show()
