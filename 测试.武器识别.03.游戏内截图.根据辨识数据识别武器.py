import time

import cv2
import mss
import numpy as np
import pynput

# 识别数据
data = {
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


def mouse():

    sct = mss.mss()

    def grab(region):
        left, top, width, height = region
        return sct.grab(monitor={'left': left, 'top': top, 'width': width, 'height': height})

    def recognize(img):
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
        return data.get(counter)

    def show():
        region1 = (2253, 125, 260, 42)  # 一号武器
        region2 = (2253, 432, 260, 42)  # 二号武器
        t1 = time.perf_counter_ns()
        img1 = grab(region1)
        img2 = grab(region2)
        t2 = time.perf_counter_ns()
        img = cv2.cvtColor(np.array(img1), cv2.COLOR_BGRA2BGR)
        name1 = recognize(img)
        t3 = time.perf_counter_ns()
        img = cv2.cvtColor(np.array(img2), cv2.COLOR_BGRA2BGR)
        name2 = recognize(img)
        t4 = time.perf_counter_ns()
        print('----------')
        print(f'武器一: {name1}')
        print(f'武器二: {name2}')
        interval = t2 - t1
        print(f'截图耗时: {interval}ns, {interval // 1_000_000}ms')
        interval = t4 - t2
        print(f'识别耗时: {interval}ns, {interval // 1_000_000}ms')
        interval = t4 - t1
        print(f'总耗时: {interval}ns, {interval // 1_000_000}ms')


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
