import cv2
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

from toolkit import Image

rets = Image.load(r'image/3440.1440/attitude/prone')  # 某个姿态截一堆图, 自适应二值化后, 从姿态边框上找固定几个点来确认姿态
row = 9
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

    counter += 1
    img = Image.convert(img, True, True)
    plt.subplot(row, col, counter)
    plt.imshow(img, cmap='gray')
    # cv2.imwrite(rf'image/3440.1440/attitude/prone/{counter}.jpg', img)

plt.show()
