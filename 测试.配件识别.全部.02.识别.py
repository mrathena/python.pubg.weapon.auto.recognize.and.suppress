import time

import cv2
import mss
import numpy as np
import pynput

from toolkit import Game, Timer

one = 'one'
two = 'two'
name = 'name'
sight = 'sight'
muzzle = 'muzzle'
foregrip = 'foregrip'
stock = 'stock'
data = {
    one: {
        name: (42, 0, 260, 42),
        sight: (365, 29, 62, 31),
        muzzle: (2, 207, 62, 62),
        foregrip: (138, 207, 62, 62),
        stock: (568, 207, 62, 62),
    },
    two: {
        name: (42, 308, 260, 42),
        sight: (365, 335, 62, 31),
        muzzle: (2, 514, 62, 62),
        foregrip: (138, 514, 62, 62),
        stock: (568, 514, 62, 62),
    },
    name: {
        769: 'ACE32',
        561: 'AKM',
        511: 'AUG',
        1269: 'Beryl M762',
        716: 'G36C',
        568: 'Groza',
        309: 'K2',
        794: 'M16A4',
        646: 'M416',
        1360: 'Mk47 Mutant',
        552: 'QBZ',
        798: 'SCAR-L',
        669: 'Mini14',
        602: 'Mk12',
        588: 'Mk14',
        597: 'QBU',
        494: 'SKS',
        1627: 'SLR',
        464: 'VSS',
        636: 'Crossbow',
        715: 'DP-28',
        710: 'M249 ',
        605: 'MG3',
        846: 'Mortar',
        1325: 'Panzerfaust',
        564: 'DBS',
        423: 'O12',
        556: 'S12K',
        758: 'S1897',
        737: 'S686',
        647: 'AWM',
        872: 'Kar98k',
        993: 'Lynx AMR',
        513: 'M24',
        1611: 'Mosin Nagant',
        740: 'Win94',
        934: 'Micro UZI',
        742: 'MP5K',
        608: 'MP9',
        559: 'P90',
        1207: 'PP-19 Bizon',
        1567: 'Tommy Gun',
        880: 'UMP45',
        624: 'Vector',
        1917: 'Blue Chip Detector',
        1553: 'Drone Tablet',
        1664: 'EMT Gear',
        843: 'Spotter Scope',
        947: 'Tactical Pack',
    }
}


# 载入对比图片
imgs_sight_1 = Game.Image.load(r'image/3440.1440/weapon.attachment/sight/1', gray=True, binary=True)
imgs_sight_2 = Game.Image.load(r'image/3440.1440/weapon.attachment/sight/2', gray=True, binary=True)
imgs_muzzle = Game.Image.load(r'image/3440.1440/weapon.attachment/muzzle', gray=True, binary=True)
imgs_foregrip = Game.Image.load(r'image/3440.1440/weapon.attachment/foregrip', gray=True, binary=True)
imgs_stock = Game.Image.load(r'image/3440.1440/weapon.attachment/stock', gray=True, binary=True)


def cut(img, region):
    """
    入参图片需为 OpenCV 格式
    """
    left, top, width, height = region
    return img[top:top + height, left:left + width]


def recognize_name(img):
    """
    入参图片需为 OpenCV 格式
    """
    # 截图灰度化
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 截图二值化
    ret, img = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)
    # 数纯白色点
    height, width = img.shape
    counter = 0
    for row in range(0, height):
        for col in range(0, width):
            if 255 == img[row, col]:
                counter += 1
    return data[name].get(counter)


def recognize_attachment(imgs, img):
    """
    入参图片需为 OpenCV 格式
    """
    img = Game.Image.convert(img, gray=True, binary=True)
    for name, standard in imgs:
        similarity = Game.Image.similarity(standard, img)
        print(similarity, name)
        if similarity > 0.925:
            return name
    return None


sct = mss.mss()


def grab(region):
    left, top, width, height = region
    return sct.grab(monitor={'left': left, 'top': top, 'width': width, 'height': height})


def show():
    region = (2212, 125, 632, 577)
    t1 = time.perf_counter_ns()
    img = grab(region)
    # mss.tools.to_png(img1.rgb, img1.size, output=f'{int(time.time())}.png')
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)
    # img = cv2.imread(r'image/3440.1440/weapon.attachment/all/1668274401.png')
    t2 = time.perf_counter_ns()
    # 分割图片
    img_name_1 = cut(img, data[one][name])
    img_sight_1 = cut(img, data[one][sight])
    img_muzzle_1 = cut(img, data[one][muzzle])
    img_foregrip_1 = cut(img, data[one][foregrip])
    img_stock_1 = cut(img, data[one][stock])
    img_name_2 = cut(img, data[two][name])
    img_sight_2 = cut(img, data[two][sight])
    img_muzzle_2 = cut(img, data[two][muzzle])
    img_foregrip_2 = cut(img, data[two][foregrip])
    img_stock_2 = cut(img, data[two][stock])
    # 识别图片
    name_1 = recognize_name(img_name_1)
    sight_1 = recognize_attachment(imgs_sight_1, img_sight_1)
    muzzle_1 = recognize_attachment(imgs_muzzle, img_muzzle_1)
    foregrip_1 = recognize_attachment(imgs_foregrip, img_foregrip_1)
    stock_1 = recognize_attachment(imgs_stock, img_stock_1)
    name_2 = recognize_name(img_name_2)
    sight_2 = recognize_attachment(imgs_sight_2, img_sight_2)
    muzzle_2 = recognize_attachment(imgs_muzzle, img_muzzle_2)
    foregrip_2 = recognize_attachment(imgs_foregrip, img_foregrip_2)
    stock_2 = recognize_attachment(imgs_stock, img_stock_2)
    t3 = time.perf_counter_ns()
    print('----------')
    print(f'武器一: {name_1}, {sight_1}, {muzzle_1}, {foregrip_1}, {stock_1}')
    print(f'武器二: {name_2}, {sight_2}, {muzzle_2}, {foregrip_2}, {stock_2}')
    print(f'总耗时: {Timer.cost(t3 - t1)}, 截图:{Timer.cost(t2 - t1)}, 识别:{Timer.cost(t3 - t2)}')


def mouse():

    def down(x, y, button, pressed):
        if pressed:
            # 鼠标, 侧上键:结束, 侧下键:识别
            if button == pynput.mouse.Button.x2:
                return False
            elif button == pynput.mouse.Button.x1:
                show()

    with pynput.mouse.Listener(on_click=down) as m:
        m.join()


mouse()


