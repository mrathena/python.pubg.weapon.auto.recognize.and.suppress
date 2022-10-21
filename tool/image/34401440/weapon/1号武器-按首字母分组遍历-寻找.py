import os

import cv2


def load(directory, exclude=None, starter=None):
    imgs = []
    names = []
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            t1, t2 = load(path, exclude, starter)
            for temp in t1:
                imgs.append(temp)
            for temp in t2:
                names.append(temp)
        elif os.path.isfile(path):
            name = item.replace('.png', '')
            if exclude and name in exclude:
                continue
            if starter and not name.startswith(starter):
                continue
            imgs.append(cv2.imread(path, cv2.IMREAD_COLOR))
            names.append(name)
    return imgs, names


def letters(directory, l, t):
    data = []

    exclude = set()
    imgs, names = load(directory)
    # print(f'载入{len(imgs)}张图片')
    while len(imgs) > 0:
        for row in range(0, 42):
            # 注意 AWM 这个枪的名字, W 偏向了 A 的地方, 占了一部分空间, 所以 14,32 得缩小为
            for col in range(14, 30):
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
                    # print(f'用于验证的数据:{row}, {col} - 截图上的坐标:({col},{row}) - 对应游戏内的点的坐标:({l + col},{t + row}) - {name}')
                    exclude.add(name)
                    data.append((l + col, t + row, name))
        imgs, names = load(directory, exclude)
        # print(f'载入{len(imgs)}张图片')
    return data


def letter(directory, l, t, starter):
    data = []

    exclude = set()
    imgs, names = load(directory, starter=starter)
    # print(f'载入{len(imgs)}张图片')
    while len(imgs) > 0:
        for row in range(0, 42):
            for col in range(0, 260):
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
                    # print(f'用于验证的数据:{row}, {col} - 截图上的坐标:({col},{row}) - 对应游戏内的点的坐标:({l + col},{t + row}) - {name}')
                    exclude.add(name)
                    data.append((l + col, t + row, name))
        imgs, names = load(directory, exclude, starter=starter)
        # print(f'载入{len(imgs)}张图片')
    return data


# 图片尺寸: 260,42
l, t = 2253, 125
directory = 'one.en/letter'
first = letters(directory, l, t)
prefix = '\t\t\t\t'
print(f'{prefix}one: {"{"}')
print(f'{prefix}\tletter: [')
for item in first:
    print(f'{prefix}\t\t{item},')
print(f'{prefix}\t],')
directory = r'one.en/group'
for item in first:
    t1, t2, starter = item
    print(f'{prefix}\t{starter}: [')
    other = letter(directory, l, t, starter.upper())
    for item2 in other:
        print(f'{prefix}\t\t{item2},')
    print(f'{prefix}\t],')
print(f'{prefix}{"},"}')

# 替换 cfg.py - detect - 3440:1440 - name - 对应 letter 和 abcde ...









