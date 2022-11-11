import time

import cv2
import mss
import numpy as np
import pynput

# 识别数据
data = [
    ((43, 12), (46, 8), 'Vertical Foregrip'),
    ((58, 10), (61, 7), 'Haalfgrip'),
    ((35, 13), (35, 10), 'Lightweight Grip'),
    ((44, 50), (47, 53), 'Thumbgrip'),
    ((21, 26), (18, 23), 'Laser Sight'),
    ((31, 56), (31, 59), 'Angled Foregrip'),
    ((28, 36), (25, 33), 'Quiver'),
]


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
        # 遍历对比点位颜色差值
        for item in data:
            inner, outer, name = item
            x, y = inner
            a, b = outer
            # print(gray[b][a], gray[y][x], name)
            if int(gray[b][a]) - int(gray[y][x]) > 10:
                return name
        return None

    def cost(interval):
        """
        输入纳秒间距, 转换为合适的单位
        """
        if interval < 1000:
            return f'{interval}ns'
        elif interval < 1_000_000:
            return f'{interval / 1000}us'
        elif interval < 1_000_000_000:
            return f'{interval / 1_000_000}ms'
        else:
            return f'{interval / 1_000_000_000}s'

    def show():
        region1 = (2348, 330, 66, 66)  # 一号武器
        region2 = (2348, 636, 66, 66)  # 二号武器
        t1 = time.perf_counter_ns()
        img = grab(region1)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)
        name1 = recognize(img)
        t2 = time.perf_counter_ns()
        img = grab(region2)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)
        name2 = recognize(img)
        t3 = time.perf_counter_ns()
        print('----------')
        print(f'武器一: {name1}, {cost(t2 - t1)}')
        print(f'武器二: {name2}, {cost(t3 - t2)}')
        print(f'总耗时: {cost(t3 - t1)}')

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
