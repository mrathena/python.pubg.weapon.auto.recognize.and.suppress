import multiprocessing
import time
from multiprocessing import Process

import pynput  # pip install pynput
import winsound

from toolkit import Pubg

end = 'end'
tab = 'tab'
mode = 'mode'
fire = 'fire'
index = 'index'
right = 'right'
switch = 'switch'
weapon = 'weapon'
attitude = 'attitude'
recognize = 'recognize'
timestamp = 'timestamp'
init = {
    end: False,  # 退出标记
    switch: False,  # 压枪开关
    tab: 0,  # Tab键检测, 背包检测与武器识别的状态
    weapon: None,  # 当前识别出来的主武器, dict
    index: 0,  # 当前持有的武器, 1:1号武器, 2:2号武器
    right: 0,  # 右键检测, 包括当前的角色姿态, 当前激活的武器, 武器的射击模式
    attitude: None,  # 姿态, stand:站, squat:蹲, prone:爬, 开火时检测(开火时要按右键,按右键后会出现姿态标识)
    mode: None,  # 射击模式, auto:全自动, semi:半自动(点射), only:单发
    timestamp: None,  # 按下左键开火时的时间戳
    fire: False,  # 开火状态
}


def mouse(data):

    def down(x, y, button, pressed):
        if Pubg.game():
            if button == pynput.mouse.Button.x1:
                # 侧下键
                if pressed:
                    # 压枪开关
                    data[switch] = not data.get(switch)
                    winsound.Beep(800 if data[switch] else 400, 200)
            elif button == pynput.mouse.Button.left:
                data[fire] = pressed
                if pressed:
                    data[timestamp] = time.perf_counter_ns()
            elif button == pynput.mouse.Button.right:
                if pressed:
                    data[right] = 1  # 非0开始检测
            elif button == pynput.mouse.Button.x2:
                # 侧上键
                if pressed:
                    print('========== ==========')
                    if data[weapon]:
                        for key, value in data[weapon].items():
                            print(f'{key}: {value}')
                    print(f'index: {data[index]}, {data[attitude]}, {data[mode]}')

    with pynput.mouse.Listener(on_click=down) as m:
        m.join()


def keyboard(data):

    def release(key):
        if key == pynput.keyboard.Key.end:
            # 结束程序
            winsound.Beep(400, 200)
            data[end] = True
            return False
        if Pubg.game():
            if key == pynput.keyboard.Key.tab:
                # tab: 背包检测与武器识别的状态
                # 0: 默认状态
                # 1: 背包检测中
                # 2: 武器识别中
                # 3: 等待关闭背包
                if data[tab] == 0:  # 等待打开背包
                    data[tab] = 1
                elif data[tab] == 1:  # 背包检测中, 中止检测, 恢复默认状态(循环中会有状态机式的状态感知)
                    data[tab] = 0
                elif data[tab] == 2:  # 武器识别中, 中止识别, 恢复默认状态
                    data[tab] = 0
                elif data[tab] == 3:  # 武器已识别, 等待关闭背包, 恢复默认状态
                    data[tab] = 0
            elif key == pynput.keyboard.KeyCode.from_char('1'):
                if data[weapon] and data[weapon].get('1'):
                    data[index] = '1'
            elif key == pynput.keyboard.KeyCode.from_char('2'):
                if data[weapon] and data[weapon].get('2'):
                    data[index] = '2'

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
            data[tab] = 0  # 开关关闭时, 每次循环都会重置检测状态
            continue
        if not pubg.game():
            continue
        if data[tab] == 1:
            # 异常状态检测并自动重置检测状态
            counter += 1
            if counter >= 10:  # 举例: 开着背包的时候, 启动辅助并打开开关, 按Tab键关闭背包, 触发辅助更新为状态1, 因为背包已关闭不可能判定是在背包界面, 导致卡状态1
                data[tab] = 0
                counter = 0
            # 背包检测
            if pubg.backpack() and data[tab] == 1:
                data[tab] = 2
                counter = 0
                continue
        if data[tab] == 2:
            # 异常状态检测并自动重置检测状态
            counter += 1
            if counter >= 10:
                data[tab] = 0
                counter = 0
            # 武器识别
            first, second = pubg.weapon()
            if data[tab] == 2:
                data[tab] = 3
                counter = 0
                winsound.Beep(600, 200)  # 通知武器识别结束
                data[weapon] = {
                    '1': first,
                    '2': second,
                }
                continue
        if data[right] != 0:
            data[right] = 0
            # 检测姿态
            data[attitude] = pubg.attitude()
            # 射击模式
            data[mode] = pubg.mode()
            # 激活武器
            # todo
        if data[fire]:
            # 只要开火就默认是右键瞄准射击而不是腰射

            # 判断是否识别了背包中的武器
            if not data[weapon]:
                continue
            # 判断当前选定的武器是否需要压枪
            gun = data[weapon].get(data[index])
            if gun and not gun.suppress:
                continue
            # 判断射击模式, 突击步枪/冲锋枪 才可能是全自动模式
            # 这里有个额外的效果, 如果是 None, 说明当前要么没枪, 要么枪不需要压
            if data[mode] != 'auto':
                print('非全自动')
                continue
            # 判断是否有子弹
            if not pubg.bullet():
                print('弹夹空')
                continue
            # 判断姿态
            factor = gun.factor * gun.attitude(data[attitude])
            print(factor)



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
