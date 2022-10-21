import os

import cv2


directory = r'picture\group'


def load(directory):
    imgs = []
    names = []
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            t1, t2 = load(path)
            for temp in t1:
                imgs.append(temp)
            for temp in t2:
                names.append(temp)
        elif os.path.isfile(path):
            imgs.append(cv2.imread(path, cv2.IMREAD_COLOR))
            names.append(item.replace('.png', ''))
    return imgs, names


imgs, names = load(directory)
row, col = 12, 71
for i in range(0, len(imgs)):
    img = imgs[i]
    (b, g, r) = img[row, col]
    if (b, g, r) == (255, 255, 255):
        print(f'{img[row, col]} - {names[i]}')











