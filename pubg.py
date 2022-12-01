import ctypes
import multiprocessing
import time
from multiprocessing import Process
import pynput  # pip install pynput
import winsound

from toolkit import Pubg, Timer

end = 'end'
tab = 'tab'
ads = 'ads'
fire = 'fire'
temp = 'temp'
debug = 'debug'
index = 'index'
right = 'right'
switch = 'switch'
weapon = 'weapon'
weapons = 'weapons'
attitude = 'attitude'
firemode = 'firemode'
recognize = 'recognize'
timestamp = 'timestamp'
init = {
    end: False,  # 退出标记
    switch: True,  # 压枪开关
    tab: 0,  # 背包检测信号, 非0触发检测. Tab键触发修改, 用于检测背包界面中的武器信息
    weapons: None,  # 背包界面中的两把主武器信息, 字典格式, {1:武器1, 2:武器2}
    index: 0,  # 激活检测信号, 非0触发检测. 鼠标滚轮滚动/1/2/3/4/5/G(切雷)/F(落地捡枪)/X(收起武器)/Tab(调整位置)/ 等按键触发修改
    weapon: None,  # 当前持有的主武器
    right: 0,  # 右键检测信号, 非0触发检测. 右键触发修改, 包括当前的角色姿态, 当前激活的武器, 武器的射击模式
    attitude: None,  # 姿态, stand:站, squat:蹲, prone:爬, 开火时检测(开火时要按右键,按右键后会出现姿态标识)
    firemode: None,  # 射击模式, auto:全自动, semi:半自动(点射), only:单发
    timestamp: None,  # 按下左键开火时的时间戳
    fire: False,  # 开火状态
    ads: 2,  # 基准倍数
    debug: False,  # 调试模式开关
    temp: None,  # 调试下压力度数据使用
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
                    data[timestamp] = time.time_ns()
            elif button == pynput.mouse.Button.right:
                if pressed:
                    data[right] = 1
            elif button == pynput.mouse.Button.x2:  # todo 调试弹道
                if pressed and data[debug]:
                    with open('debug', 'r') as file:
                        try:
                            exec(file.read())
                            print(data[temp])
                        except Exception as e:
                            print(e.args)
                            print(str(e))
                            print(repr(e))

    def scroll(x, y, dx, dy):
        if Pubg.game():
            data[index] = 1

    with pynput.mouse.Listener(on_click=down, on_scroll=scroll) as m:
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
                    data[index] = 1
                elif data[tab] == 2:  # 武器识别中, 中止识别, 恢复默认状态
                    data[tab] = 0
                    data[index] = 1
                elif data[tab] == 3:  # 武器已识别, 等待关闭背包, 恢复默认状态
                    data[tab] = 0
                    data[index] = 1
            elif key == pynput.keyboard.KeyCode.from_char('1'):
                data[index] = 1
                # todo
                if data[weapons] is not None and data[weapons].get(1) is not None:
                    data[weapon] = data[weapons].get(1)
            elif key == pynput.keyboard.KeyCode.from_char('2'):
                data[index] = 1
                # todo
                if data[weapons] is not None and data[weapons].get(2) is not None:
                    data[weapon] = data[weapons].get(2)
            elif key == pynput.keyboard.KeyCode.from_char('3'):
                data[index] = 1
            elif key == pynput.keyboard.KeyCode.from_char('4'):
                data[index] = 1
            elif key == pynput.keyboard.KeyCode.from_char('5'):
                data[index] = 1
            elif key == pynput.keyboard.KeyCode.from_char('g'):
                data[index] = 1
            elif key == pynput.keyboard.KeyCode.from_char('f'):
                data[index] = 1
            elif key == pynput.keyboard.KeyCode.from_char('x'):
                data[index] = 1

    with pynput.keyboard.Listener(on_release=release) as k:
        k.join()


def suppress(data):

    try:
        driver = ctypes.CDLL('logitech.driver.dll')
        ok = driver.device_open() == 1  # 该驱动每个进程可打开一个实例
        if not ok:
            print('Error, GHUB or LGS driver not found')
    except FileNotFoundError:
        print('Error, DLL file not found')

    def move(x, y):
        if ok:
            driver.moveR(x, y, True)

    pubg = Pubg()
    winsound.Beep(800, 200)

    counter = 0  # 检测计数器, 防止因不正常状态导致背包检测和武器识别陷入死循环, 10个循环内没有结果就会强制退出

    def show():
        print('==========')
        if data[weapons]:
            for k, v in data[weapons].items():
                print(f'{k}: {v}')
        print(f'index: {data[index]}, {data[attitude]}, {data[firemode]}')

    while True:

        if data.get(end):  # 退出程序
            break
        if not data.get(switch):
            data[tab] = 0  # 开关关闭时, 每次循环都会重置背包检测信号
            continue
        if not pubg.game():  # 如果不在游戏中
            continue
        if data[tab] == 1:  # 背包界面检测
            counter += 1
            if counter >= 10:  # 举例: 开着背包的时候, 启动辅助并打开开关, 按Tab键关闭背包, 触发辅助更新为状态1, 因为背包已关闭不可能判定是在背包界面, 导致卡状态1
                data[tab] = 0
                counter = 0
            if pubg.backpack() and data[tab] == 1:  # 背包界面检测
                data[tab] = 2
                counter = 0
                continue
        if data[tab] == 2:  # 背包中武器识别
            counter += 1
            if counter >= 10:
                data[tab] = 0
                counter = 0
            first, second = pubg.weapon()  # 背包中武器识别
            if data[tab] == 2:
                data[tab] = 3
                counter = 0
                winsound.Beep(600, 200)  # 通知武器识别结束
                data[weapons] = {
                    1: first,
                    2: second,
                }
                show()
                continue
        if data[index] != 0:  # 检测当前激活的是几号武器
            data[index] = 0
            time.sleep(0.2)  # 防止UI还没有改变
            if not data[weapons]:  # 如果还没有识别过背包中的武器, 则不检测当前激活的是几号武器
                continue
            count = 0  # 如果识别过背包中的武器, 但识别到的都是 None, 则不检测当前激活的是几号武器
            for key, value in data[weapons].items():
                if not value:
                    count += 1
            if count == 0:
                continue
            # data[weapon] = data[weapons].get(pubg.index())  # 检测当前激活的是几号武器  # todo
            show()
            continue
        if data[right] != 0:  # 右键检测
            data[right] = 0
            time.sleep(0.2)  # 防止UI还没有改变
            data[attitude] = pubg.attitude()  # 检测角色姿态
            data[firemode] = pubg.firemode()  # 检测射击模式
            show()
        if data[fire]:  # 开火检测, 默认开火前一定按下了右键, 做了右键检测
            gun = data[weapon]
            if gun is None:  # 如果不确定当前武器则不压枪
                print('武器不确定')
                continue
            if gun.suppress is False:  # 如果当前武器不支持压枪
                print('武器不支持')
                continue
            data[firemode] = pubg.firemode()
            if data[firemode] != 'auto':  # 全自动才压枪(突击步枪/冲锋枪). 这里有隐藏效果,不在对局中/未持枪/背包界面等情景下返回值都是None
                print('武器非自动')
                continue
            if not pubg.bullet():  # 如果弹夹空了
                print('武器弹夹空')
                continue
            print('----------')
            cost = time.time_ns() - data[timestamp]  # 开火时长
            base = gun.interval * 1_000_000  # 基准间隔时间转纳秒
            i = cost // base  # 本回合的压枪力度数值索引
            distance = int(data[ads] * gun.ballistic[i] * gun.factor * gun.attitude(data[attitude]))  # 下移距离
            distance = int(data[ads] * gun.ballistic[i] * data[temp]) if data[temp] else distance  # 下移距离, 去除武器因子和姿态因子的影响, 用于测试当前弹道力度下某单一因素的影响因子值(比如测不同握把的影响)
            print(f'开火时长:{Timer.cost(cost)}, {i}, 压制力度:{distance}, 武器因子:{gun.factor}, 姿态因子:{gun.attitude(data[attitude])}')
            cost = time.time_ns() - data[timestamp]
            left = base - cost % base  # 本回合剩余时间纳秒
            mean = left / distance  # 平缓压枪每个实际力度的延时
            for i in range(0, distance):
                begin = time.perf_counter_ns()
                while time.perf_counter_ns() - begin < mean:
                    pass
                move(0, 1)


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
