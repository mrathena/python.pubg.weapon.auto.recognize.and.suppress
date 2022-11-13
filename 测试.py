import time

import winsound

import pynput
from toolkit import Pubg, Timer

pubg = Pubg()
winsound.Beep(800, 200)


def mouse():

    def down(x, y, button, pressed):
        if button == pynput.mouse.Button.x2:
            winsound.Beep(400, 200)
            return False
        elif button == pynput.mouse.Button.x1:
            if pressed:
                t1 = time.perf_counter_ns()
                print(pubg.backpack())
                t2 = time.perf_counter_ns()
                print(f'耗时:{Timer.cost(t2 - t1)}')

    with pynput.mouse.Listener(on_click=down) as m:
        m.join()


mouse()
