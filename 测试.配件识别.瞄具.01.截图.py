import time
import mss
import pynput
import winsound


def mouse():

    sct = mss.mss()

    def grab(region):
        left, top, width, height = region
        return sct.grab(monitor={'left': left, 'top': top, 'width': width, 'height': height})

    def down(x, y, button, pressed):
        if pressed:
            # 鼠标, 侧上键:结束, 侧下键:识别
            if button == pynput.mouse.Button.x2:
                return False
            elif button == pynput.mouse.Button.x1:
                # 截图, 3440×1440
                img = grab((2577, 154, 62, 31))
                mss.tools.to_png(img.rgb, img.size, output=f'image/3440.1440/weapon.attachment/sight/{time.time_ns()}.png')
                winsound.Beep(800, 200)

    with pynput.mouse.Listener(on_click=down) as m:
        m.join()


mouse()
