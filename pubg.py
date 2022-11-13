import multiprocessing
from multiprocessing import Process

import pynput  # pip install pynput
import winsound

from toolkit import Pubg

end = 'end'
tab = 'tab'
fire = 'fire'
index = 'index'
switch = 'switch'
weapon = 'weapon'
weapon1 = 'weapon1'
weapon2 = 'weapon2'
recognize = 'recognize'
init = {
    end: False,  # 退出标记
    switch: False,  # 压枪开关
    tab: 0,  # 识别标记
    weapon1: None,  # 背包中的一号武器
    weapon2: None,  # 背包中的二号武器
    weapon: None,  # 当前持有的主武器
    fire: False,  # 开火状态
}


def mouse(data):

    def down(x, y, button, pressed):
        if button == pynput.mouse.Button.x1:
            # 侧下键
            if pressed:
                # 压枪开关
                data[switch] = not data.get(switch)
                winsound.Beep(800 if data[switch] else 400, 200)
        elif button == pynput.mouse.Button.left:
            data[fire] = pressed
        elif button == pynput.mouse.Button.x2:
            if data[weapon]:
                for item in data[weapon]:
                    print(item)

    with pynput.mouse.Listener(on_click=down) as m:
        m.join()


def keyboard(data):

    def release(key):
        if key == pynput.keyboard.Key.end:
            # 结束程序
            winsound.Beep(400, 200)
            data[end] = True
            return False
        elif key == pynput.keyboard.Key.tab:
            # tab:
            # 0: 默认状态
            # 1: 背包检测中
            # 2: 武器识别中
            # 3: 等待关闭背包
            if data[tab] == 0:  # 想要打开背包
                data[tab] = 1
            elif data[tab] == 1:  # 背包检测中, 中止检测, 恢复默认状态(循环中会有状态机式的状态感知)
                data[tab] = 0
            elif data[tab] == 2:  # 武器识别中, 中止识别, 恢复默认状态
                data[tab] = 0
            elif data[tab] == 3:  # 武器已识别, 等待关闭背包, 恢复默认状态
                data[tab] = 0
        # elif key == pynput.keyboard.KeyCode.from_char('1'):

    with pynput.keyboard.Listener(on_release=release) as k:
        k.join()


def suppress(data):

    pubg = Pubg()
    winsound.Beep(800, 200)

    counter = 0  # 检测计数器, 防止因不正常状态导致检测卡入死循环, 至多卡10个循环就会强制退出

    while True:

        if data.get(end):
            break
        if not data.get(switch):
            data[tab] = 0
            continue
        if not pubg.game():
            continue
        if data[tab] == 1:
            counter += 1
            if counter >= 10:
                data[tab] = 0
                counter = 0
            if pubg.backpack() and data[tab] == 1:
                data[tab] = 2
                counter = 0
                continue
        if data[tab] == 2:
            counter += 1
            if counter >= 10:
                data[tab] = 0
                counter = 0
            first, second = pubg.weapon()
            if data[tab] == 2:
                data[tab] = 3
                counter = 0
                winsound.Beep(600, 200)
                data[weapon1] = first
                data[weapon2] = second
                print('----------')
                print(first)
                print(second)
                continue
        # todo


if __name__ == '__main__':
    multiprocessing.freeze_support()
    manager = multiprocessing.Manager()
    data = manager.dict()
    data.update(init)
    # 将键鼠监听和压枪放到单独进程中跑
    pm = Process(target=mouse, args=(data,))
    pk = Process(target=keyboard, args=(data,))
    ps = Process(target=suppress, args=(data,))
    pm.start()
    pk.start()
    ps.start()
    pk.join()
    pm.terminate()
