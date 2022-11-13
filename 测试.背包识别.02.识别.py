import time

import cv2
import mss
import numpy as np
import pynput

from toolkit import Image

# 载入对比图片
std = Image.read(r'image/3440.1440/backpack.png', gray=True, binary=True)


def mouse():

    sct = mss.mss()

    def grab(region):
        left, top, width, height = region
        return sct.grab(monitor={'left': left, 'top': top, 'width': width, 'height': height})

    def recognize(img):
        """
        入参图片需为 OpenCV 格式
        """
        img = Image.convert(img, gray=True, binary=True)
        similarity = Image.similarity(std, img)
        print(similarity)
        return similarity > 0.9

    def show():
        region = (936, 78, 80, 40)
        img = grab(region)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)
        print(recognize(img))

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


