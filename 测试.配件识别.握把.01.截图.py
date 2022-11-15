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
                winsound.Beep(800, 200)
                # 截图, 3440×1440
                img = grab((2350, 332, 62, 62))
                mss.tools.to_png(img.rgb, img.size, output=f'image/3440.1440/weapon.attachment/foregrip/{time.time_ns()}.png')

                # img = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)
                # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # # cv2.imwrite(f'image/3440.1440/weapon.attachment/foregrip/_gray_{time.time_ns()}.jpg', img)
                # _, img = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY)
                # cv2.imwrite(f'image/3440.1440/weapon.attachment/foregrip/_binary_{time.time_ns()}.jpg', img)

    with pynput.mouse.Listener(on_click=down) as m:
        m.join()


mouse()
