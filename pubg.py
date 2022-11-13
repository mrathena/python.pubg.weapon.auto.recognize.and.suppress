import multiprocessing
from multiprocessing import Process

import pynput  # pip install pynput
import winsound

from toolkit import Pubg

end = 'end'
fire = 'fire'
shake = 'shake'
speed = 'speed'
count = 'count'
switch = 'switch'
restart = 'restart'
restrain = 'restrain'
strength = 'strength'
init = {
    end: False,  # 退出标记
    switch: True,  # 压枪开关
    fire: False,  # 开火状态
    shake: None,  # 抖枪参数
    restrain: None,  # 压枪参数
}


def mouse(data):

    def down(x, y, button, pressed):
        if button == pynput.mouse.Button.right:
            if pressed:
                pass
        elif button == pynput.mouse.Button.left:
            data[fire] = pressed

    with pynput.mouse.Listener(on_click=down) as m:
        m.join()


def keyboard(data):

    def release(key):
        if key == pynput.keyboard.Key.end:
            # 结束程序
            winsound.Beep(400, 200)
            data[end] = True
            return False
        elif key == pynput.keyboard.Key.home:
            # 压枪开关
            data[switch] = not data.get(switch)
            winsound.Beep(800 if data[switch] else 400, 200)

    with pynput.keyboard.Listener(on_release=release) as k:
        k.join()


def suppress(data):
    while True:
        if data.get(end):
            break
        if data.get(switch) is False:
            continue


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
