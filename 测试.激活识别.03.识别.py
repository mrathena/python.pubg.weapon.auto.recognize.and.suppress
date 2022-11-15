import time

import mss
import winsound

import pynput
from toolkit import Pubg, Timer, Image

sct = mss.mss()
pubg = Pubg()

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

                t1 = time.perf_counter_ns()
                pubg.index()
                print(f'耗时:{Timer.cost(time.perf_counter_ns() - t1)}')

    with pynput.mouse.Listener(on_click=down) as m:
        m.join()


mouse()
