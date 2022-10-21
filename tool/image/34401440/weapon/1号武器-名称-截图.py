import os
import time
import numpy as np
import pynput  # pip install pynput
import mss  # pip install mss
import easyocr  # pip install easyocr


root = rf'one.cn\group\submachine.gun'
if not os.path.exists(root):
    os.makedirs(root)
sct = mss.mss()
reader = easyocr.Reader(['en'])  # ch_sim
print('load finish ...')


def grab(region):
    """
    region: tuple, (left, top, width, height)
    conda install mss / pip install mss
    """
    left, top, width, height = region
    return sct.grab(monitor={'left': left, 'top': top, 'width': width, 'height': height})


def click(x, y, button, pressed):
    if pressed:
        if button == pynput.mouse.Button.x1:
            # 侧下键
            """
            一号武器: l,t: 2253,125, w:260, h:42, 二号武器和一号武器就高度相差一点, 其他都一样
            l,t: 背包中1号武器位置, 标记1正方形的右上角, 偏右一个像素的位置, h: 这个正方形的高度
            w: 按照最长名字武器的名字长度来确定 width 
            """
            img = grab((2253, 125, 260, 42))
            result = reader.readtext(np.array(img), detail=0)
            # 名称使用 ocr 识字, 最后需要核对
            name = rf'{root}\{result[0].strip() if len(result) else int(time.time())}.png'
            mss.tools.to_png(img.rgb, img.size, output=name)
            print(name)
        elif button == pynput.mouse.Button.x2:
            # 侧上键
            return False


listener = pynput.mouse.Listener(on_click=click)
listener.start()
listener.join()

