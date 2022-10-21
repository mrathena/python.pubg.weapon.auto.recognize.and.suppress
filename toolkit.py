import ctypes
import time

from win32api import GetSystemMetrics
from win32con import SM_CXSCREEN, SM_CYSCREEN, SM_CXVIRTUALSCREEN, SM_CYVIRTUALSCREEN, DESKTOPHORZRES, DESKTOPVERTRES
from win32print import GetDeviceCaps
from win32gui import GetCursorPos, GetDC, ReleaseDC, GetPixel, GetWindowText, GetForegroundWindow  # conda install pywin32,

import cfg
from cfg import detect, weapon

try:
    driver = ctypes.CDLL('mouse.device.lgs.dll')  # 在Python的string前面加上‘r’, 是为了告诉编译器这个string是个raw string(原始字符串),不要转义backslash(反斜杠) '\'
    ok = driver.device_open() == 1
    if not ok:
        print('初始化罗技驱动失败, 未安装lgs/ghub驱动')
except FileNotFoundError:
    print('初始化罗技驱动失败, 缺少文件')


class Mouse:

    @staticmethod
    def move(x, y, absolute=False):
        if ok:
            if x == 0 and y == 0:
                return
            mx, my = x, y
            if absolute:
                ox, oy = GetCursorPos()
                mx = x - ox
                my = y - oy
            driver.moveR(mx, my, True)

    @staticmethod
    def down(code):
        if ok:
            driver.mouse_down(code)

    @staticmethod
    def up(code):
        if ok:
            driver.mouse_up(code)

    @staticmethod
    def click(code):
        """
        :param code: 1:左键, 2:中键, 3:右键, 4:侧下键, 5:侧上键, 6:DPI键
        :return:
        """
        if ok:
            driver.mouse_down(code)
            driver.mouse_up(code)


class Keyboard:

    @staticmethod
    def press(code):
        if ok:
            driver.key_down(code)

    @staticmethod
    def release(code):
        if ok:
            driver.key_up(code)

    @staticmethod
    def click(code):
        """
        键盘按键函数中，传入的参数采用的是键盘按键对应的键码
        :param code: 'a'-'z':A键-Z键, '0'-'9':0-9, 其他的没猜出来
        :return:
        """
        if ok:
            driver.key_down(code)
            driver.key_up(code)


class Monitor:
    """
    显示器
    """

    @staticmethod
    def pixel(x, y):
        """
        效率很低且不稳定, 单点检测都要耗时1-10ms
        获取颜色, COLORREF 格式, 0x00FFFFFF
        结果是int,
        可以通过 print(hex(color)) 查看十六进制值
        可以通过 print(color == 0x00FFFFFF) 进行颜色判断
        """
        hdc = GetDC(None)
        color = GetPixel(hdc, x, y)
        ReleaseDC(None, hdc)  # 一定要释放DC, 不然随着该函数调用次数增加会越来越卡, 表现就是不调用该函数, 系统会每两秒卡一下, 调用次数越多, 卡的程度越厉害
        return color

    class Resolution:
        """
        分辨率
        """

        @staticmethod
        def display():
            """
            显示分辨率
            """
            w = GetSystemMetrics(SM_CXSCREEN)
            h = GetSystemMetrics(SM_CYSCREEN)
            return w, h

        @staticmethod
        def virtual():
            """
            多屏幕组合的虚拟显示器分辨率
            """
            w = GetSystemMetrics(SM_CXVIRTUALSCREEN)
            h = GetSystemMetrics(SM_CYVIRTUALSCREEN)
            return w, h

        @staticmethod
        def physical():
            """
            物理分辨率
            """
            hdc = GetDC(None)
            w = GetDeviceCaps(hdc, DESKTOPHORZRES)
            h = GetDeviceCaps(hdc, DESKTOPVERTRES)
            ReleaseDC(None, hdc)
            return w, h


class Game:
    """
    游戏工具
    """

    @staticmethod
    def key():
        w, h = Monitor.Resolution.display()
        return f'{w}:{h}'

    @staticmethod
    def game():
        """
        是否游戏窗体在最前
        """
        return 'Apex Legends' == GetWindowText(GetForegroundWindow())

    @staticmethod
    def play():
        """
        是否正在玩
        """
        # 是在游戏中, 再判断下是否有血条和生存物品包
        data = detect.get(Game.key()).get(cfg.game)
        for item in data:
            x, y = item.get(cfg.point)
            if Monitor.pixel(x, y) != item.get(cfg.color):
                return False
        return True

    @staticmethod
    def index():
        """
        武器索引和子弹类型索引
        :return: 武器位索引, 1:1号位, 2:2号位, None:无武器
                 子弹类型索引, 1:轻型, 2:重型, 3:能量, 4:狙击, 5:霰弹, 6:空投, None:无武器
        """
        data = detect.get(Game.key()).get(cfg.pack)
        x, y = data.get(cfg.point)
        color = Monitor.pixel(x, y)
        if data.get(cfg.color) == color:
            return None, None
        else:
            bi = data.get(hex(color))
            return (1, bi) if color == Monitor.pixel(x, y + 1) else (2, bi)

    @staticmethod
    def name(index):
        """
        识别武器
        :param index: one/two
        """
        data = detect.get(Game.key()).get(cfg.name)
        color = data.get(cfg.color)
        # 判断首字母
        letter = None
        for item in data.get(index).get(cfg.letter):
            x, y, name = item
            if color == Monitor.pixel(x, y):
                letter = name
                break
        if not letter:
            return None
        # 判断名称
        # 特殊情况, 当该字母分组下只有一个数据时, 直接取该数据
        data = data.get(index).get(letter)
        if len(data) == 1:
            x, y, name = data[0]
            return name
        # 常规情况, 取该字母分组下的所有数据, 遍历取色
        result = None
        for item in data:
            x, y, name = item
            if color == Monitor.pixel(x, y):
                result = name
                break
        return result if result else None

    @staticmethod
    def one():
        """
        识别一号武器
        """
        return Game.name(cfg.one)

    @staticmethod
    def two():
        """
        识别二号武器
        """
        return Game.name(cfg.two)

    @staticmethod
    def mode():
        """
        武器模式
        :return:  1:全自动, 2:半自动, None:其他
        """
        data = detect.get(Game.key()).get(cfg.mode)
        color = data.get(cfg.color)
        x, y = data.get('1')
        if color == Monitor.pixel(x, y):
            return 1
        x, y = data.get('2')
        if color == Monitor.pixel(x, y):
            return 2
        return None

    @staticmethod
    def armed():
        """
        是否持有武器
        """
        return True

    @staticmethod
    def empty():
        """
        是否空弹夹
        """
        data = detect.get(Game.key()).get(cfg.empty)
        color = data.get(cfg.color)
        x, y = data.get('1')
        if color == Monitor.pixel(x, y):
            return False
        x, y = data.get('2')
        return color == Monitor.pixel(x, y)

    @staticmethod
    def detect(data):
        """
        决策是否需要压枪, 向信号量写数据
        """
        t1 = time.perf_counter_ns()
        one = Game.one()
        two = Game.two()
        t2 = time.perf_counter_ns()
        print(f'{one}, {two}, 约{(t2-t1)//1000000}ms')
