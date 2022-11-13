import cv2
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

from toolkit import Image


rets = Image.load(r'image/3440.1440/weapon.attachment/stock')
row = 11
col = 3
counter = 0
plt.figure(figsize=(10, 5))
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
    img = Image.convert(img, True, True)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')

plt.show()
