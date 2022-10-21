import os
import cv2

directory = r'34401440\group'

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
print(f'载入{len(imgs)}张图片')


left, top, width, height = 2253, 125, 260, 42
exclude = set()
data = []
# 图片尺寸: 260,42
for row in range(0, height):
    for col in range(0, width):
        # 轮流遍历每张图片的同一个点, 如果该点只有一张图片是纯白色, 则该点为该图片的识别点, 输入记录
        # 某点纯白色次数
        counter = 0
        temp = -1
        for i in range(0, len(imgs)):
            img = imgs[i]
            name = names[i]
            if name in exclude:
                continue
            (b, g, r) = img[row, col]
            if (b, g, r) == (255, 255, 255):
                counter += 1
                temp = i
        if counter == 1:
            name = names[temp]
            print(f'用于验证的数据:{row}, {col} - 截图上的坐标:({col},{row}) - 对应游戏内的点的坐标:({left + col},{top + row}) - {name}')
            exclude.add(name)
            data.append((left + col, top + row, name))


print(f'data = [')
for item in data:
    print(f'    {item},')
print(f']')
