import time

import cv2
import mss
import numpy as np
import pynput

from toolkit import Image, Timer

# 载入对比图片
imgs1 = Image.load(r'image/3440.1440/weapon.attachment/sight/1', gray=True, binary=True)
imgs2 = Image.load(r'image/3440.1440/weapon.attachment/sight/2', gray=True, binary=True)


def mouse():

    sct = mss.mss()

    def grab(region):
        left, top, width, height = region
        return sct.grab(monitor={'left': left, 'top': top, 'width': width, 'height': height})

    def recognize(imgs, img):
        """
        入参图片需为 OpenCV 格式
        """
        img = Image.convert(img, gray=True, binary=True)
        for name, standard in imgs:
            similarity = Image.similarity(standard, img)
            print(similarity, name)
            if similarity > 0.9:
                return name
        return None

    def show():
        region1 = (2577, 154, 62, 31)  # 一号武器
        region2 = (2577, 460, 62, 31)  # 二号武器
        print('==========')
        t1 = time.perf_counter_ns()
        img1 = grab(region1)
        # mss.tools.to_png(img1.rgb, img1.size, output=f'{int(time.time())}.png')
        img1 = cv2.cvtColor(np.array(img1), cv2.COLOR_BGRA2BGR)
        name1 = recognize(imgs1, img1)
        t2 = time.perf_counter_ns()
        print('----------')
        img2 = grab(region2)
        # mss.tools.to_png(img2.rgb, img2.size, output=f'{int(time.time()) + 1}.png')
        img2 = cv2.cvtColor(np.array(img2), cv2.COLOR_BGRA2BGR)
        name2 = recognize(imgs2, img2)
        t3 = time.perf_counter_ns()
        print('----------')
        print(f'武器一: {name1}, {Timer.cost(t2 - t1)}')
        print(f'武器二: {name2}, {Timer.cost(t3 - t2)}')
        print(f'总耗时: {Timer.cost(t3 - t1)}')

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


