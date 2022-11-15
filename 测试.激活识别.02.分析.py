import time

import cv2
import mss
import numpy as np
import winsound

import pynput
from toolkit import Pubg, Timer, Image

sct = mss.mss()

def grab(region):
    left, top, width, height = region
    return sct.grab(monitor={'left': left, 'top': top, 'width': width, 'height': height})

def mouse():

    def down(x, y, button, pressed):
        if button == pynput.mouse.Button.x2:
            winsound.Beep(400, 200)
            return False
        elif button == pynput.mouse.Button.x1:
            if pressed:
                winsound.Beep(800, 200)
                region = (2808, 1128, 240, 300)
                img = grab(region)
                mss.tools.to_png(img.rgb, img.size, output=f'image/test/{time.time_ns()}.png')
                img = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)

                img = Image.gray(img, True)
                cv2.imwrite(rf'image/3440.1440/test/{time.perf_counter_ns()}.jpg', img)

                # img = Image.binary(img, adaptive=True)
                img = Image.binary(img, threshold=210)
                # cv2.imwrite(rf'image/3440.1440/test/{time.perf_counter_ns()}.jpg', img)

                img = Image.binary_remove_small_objects(img, 10)
                cv2.imwrite(rf'image/3440.1440/test/{time.perf_counter_ns()}.jpg', img)



    with pynput.mouse.Listener(on_click=down) as m:
        m.join()


mouse()
