import time

import pynput

from toolkit import Pubg, Timer
pubg = Pubg()


def mouse():

    def down(x, y, button, pressed):
        if pressed:
            # 鼠标, 侧上键:结束, 侧下键:识别
            if button == pynput.mouse.Button.x2:
                return False
            elif button == pynput.mouse.Button.x1:
                t1 = time.perf_counter_ns()
                print(pubg.bullet(), f'{Timer.cost(time.perf_counter_ns() - t1)}')

    with pynput.mouse.Listener(on_click=down) as m:
        m.join()


mouse()


