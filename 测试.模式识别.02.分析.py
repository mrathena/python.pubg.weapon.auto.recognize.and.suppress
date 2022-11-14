import cv2
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

from toolkit import Image

rets = Image.load(r'image/3440.1440/weapon/mode')
row = 17
col = 3
counter = 0
plt.figure(figsize=(10, 10))
for name, img in rets:

    counter += 1
    original = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.subplot(row, col, counter)
    plt.imshow(original, cmap='gray')

    counter += 1
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plt.subplot(row, col, counter)
    plt.imshow(gray, cmap='gray')
    print(gray[3][13], gray[8][13], gray[14][13], gray[19][13])
    # cv2.imwrite(rf'image/3440.1440/weapon/mode/_g_{counter}.jpg', img)

    counter += 1
    _, img = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')
    cv2.imwrite(rf'image/3440.1440/weapon/mode/_b_{counter}.jpg', img)

plt.show()
