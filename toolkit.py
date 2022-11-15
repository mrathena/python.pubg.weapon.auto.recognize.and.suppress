import os
import time

import cv2
import d3dshot
import mss as pymss
import numpy as np
from skimage import measure  # pip install scikit-image

from win32api import GetSystemMetrics  # conda install pywin32
from win32con import SRCCOPY, SM_CXSCREEN, SM_CYSCREEN
from win32gui import GetDesktopWindow, GetWindowDC, DeleteObject, GetWindowText, GetForegroundWindow, GetDC, ReleaseDC, GetPixel
from win32ui import CreateDCFromHandle, CreateBitmap


class Capturer:

    @staticmethod
    def win(region):
        """
        region: tuple, (left, top, width, height)
        conda install pywin32, 用 pip 装的一直无法导入 win32ui 模块, 找遍各种办法都没用, 用 conda 装的一次成功
        """
        left, top, width, height = region
        hWin = GetDesktopWindow()
        hWinDC = GetWindowDC(hWin)
        srcDC = CreateDCFromHandle(hWinDC)
        memDC = srcDC.CreateCompatibleDC()
        bmp = CreateBitmap()
        bmp.CreateCompatibleBitmap(srcDC, width, height)
        memDC.SelectObject(bmp)
        memDC.BitBlt((0, 0), (width, height), srcDC, (left, top), SRCCOPY)
        array = bmp.GetBitmapBits(True)
        DeleteObject(bmp.GetHandle())
        memDC.DeleteDC()
        srcDC.DeleteDC()
        ReleaseDC(hWin, hWinDC)
        img = np.frombuffer(array, dtype='uint8')
        img.shape = (height, width, 4)
        return img

    @staticmethod
    def mss(instance, region):
        """
        region: tuple, (left, top, width, height)
        pip install mss
        """
        left, top, width, height = region
        return instance.grab(monitor={'left': left, 'top': top, 'width': width, 'height': height})

    @staticmethod
    def d3d(instance, region=None):
        """
        DXGI 普通模式
        region: tuple, (left, top, width, height)
        因为 D3DShot 在 Python 3.9 里会和 pillow 版本冲突, 所以使用大佬修复过的版本来替代
        pip install git+https://github.com/fauskanger/D3DShot#egg=D3DShot
        """
        if region:
            left, top, width, height = region
            return instance.screenshot((left, top, left + width, top + height))
        else:
            return instance.screenshot()

    @staticmethod
    def d3d_latest_frame(instance):
        """
        DXGI 缓存帧模式
        """
        return instance.get_latest_frame()

    @staticmethod
    def instance(mss=False, d3d=False, buffer=False, frame_buffer_size=60, target_fps=60, region=None):
        if mss:
            return pymss.mss()
        elif d3d:
            """
            buffer: 是否使用缓存帧模式
                否: 适用于 dxgi.screenshot
                是: 适用于 dxgi.get_latest_frame, 需传入 frame_buffer_size, target_fps, region
            """
            if not buffer:
                return d3dshot.create(capture_output="numpy")
            else:
                dxgi = d3dshot.create(capture_output="numpy", frame_buffer_size=frame_buffer_size)
                left, top, width, height = region
                dxgi.capture(target_fps=target_fps, region=(left, top, left + width, top + height))  # region: left, top, right, bottom, 需要适配入参为 left, top, width, height 格式的 region
                return dxgi

    @staticmethod
    def grab(win=False, mss=False, d3d=False, instance=None, region=None, buffer=False, convert=False):
        """
        win:
            region: tuple, (left, top, width, height)
        mss:
            instance: mss instance
            region: tuple, (left, top, width, height)
        d3d:
            buffer: 是否为缓存帧模式
                否: 需要 region
                是: 不需要 region
            instance: d3d instance, 区分是否为缓存帧模式
            region: tuple, (left, top, width, height), 区分是否为缓存帧模式
        convert: 是否转换为 opencv 需要的 numpy BGR 格式, 转换结果可直接用于 opencv
        """
        # 补全范围
        if (win or mss or (d3d and not buffer)) and not region:
            w, h = Monitor.resolution()
            region = 0, 0, w, h
        # 范围截图
        if win:
            img = Capturer.win(region)
        elif mss:
            img = Capturer.mss(instance, region)
        elif d3d:
            if not buffer:
                img = Capturer.d3d(instance, region)
            else:
                img = Capturer.d3d_latest_frame(instance)
        else:
            img = Capturer.win(region)
            win = True
        # 图片转换
        if convert:
            if win:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            elif mss:
                img = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)
            elif d3d:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img


class Monitor:

    @staticmethod
    def resolution():
        """
        显示分辨率
        """
        w = GetSystemMetrics(SM_CXSCREEN)
        h = GetSystemMetrics(SM_CYSCREEN)
        return w, h

    @staticmethod
    def center():
        """
        屏幕中心点
        """
        w, h = Monitor.resolution()
        return w // 2, h // 2


class Timer:

    @staticmethod
    def cost(interval):
        """
        转换耗时, 输入纳秒间距, 转换为合适的单位
        """
        if interval < 1000:
            return f'{interval}ns'
        elif interval < 1_000_000:
            return f'{round(interval / 1000, 3)}us'
        elif interval < 1_000_000_000:
            return f'{round(interval / 1_000_000, 3)}ms'
        else:
            return f'{round(interval / 1_000_000_000, 3)}s'


class Image:

    @staticmethod
    def gray(img, max=False):
        """
        灰度化
        :param img: OpenCV BGR
        :param max: 使用BGR3通道中的最大值作为灰度色值
        """
        """
        BGR3通道色值取平均值就是灰度色值, 灰度图将BGR3通道转换为灰度通道
        """
        if not max:
            return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            new = np.zeros(img.shape[:2], np.uint8)
            for row in range(0, img.shape[0]):
                for col in range(0, img.shape[1]):
                    (b, g, r) = img[row][col]
                    value = (b if b >= g else g)
                    new[row][col] = (value if value >= r else r)
            return new

    @staticmethod
    def binary(img, adaptive=False, threshold=None, block=3, c=1):
        """
        二值化
        :param img: 灰度图
        :param adaptive: 是否自适应二值化
        :param threshold: 二值化阈值(全局二值化), 大于该值的转为白色, 其他值转为黑色
        :param block: 分割的邻域大小(自适应二值化). 值越大, 参与计算阈值的邻域面积越大, 细节轮廓就变得越少, 整体轮廓将越粗越明显
        :param c: 常数(自适应二值化), 可复数. 值越大, 每个邻域内计算出的阈值将越小, 转换为 maxVal 的点将越多, 整体图像白色像素将越多
        """
        if not adaptive:
            # 全局二值化
            _, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
            """
            threshold(src, thresh, maxVal, type, dst=None)
                src: 灰度图
                thresh: 阈值
                maxVal: 指定的最大色值
                type:
                    THRESH_BINARY: 二值化, 大于阈值的赋最大色值, 其他赋0
                    THRESH_BINARY_INV: 二值化反转, 与 THRESH_BINARY 相反, 大于阈值的赋0, 其他赋最大色值
                    THRESH_TRUNC: 截断操作, 大于阈值的赋最大色值, 其他不变
                    THRESH_TOZERO: 化零操作, 大于阈值的不变, 其他赋0
                    THRESH_TOZERO_INV: 化零操作反转, 大于阈值的赋0, 其他不变
            """
        else:
            # 自适应二值化
            img = cv2.adaptiveThreshold(img, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=block, C=c)
            """
            adaptiveThreshold(src, maxValue, adaptiveMethod, thresholdType, blockSize, C, dst=None)
                src: 灰度图
                maxValue: 指定的最大色值
                adaptiveMethod: 自适应方法。有2种：ADAPTIVE_THRESH_MEAN_C 或 ADAPTIVE_THRESH_GAUSSIAN_C
                    ADAPTIVE_THRESH_MEAN_C，为局部邻域块的平均值，该算法是先求出块中的均值。
                    ADAPTIVE_THRESH_GAUSSIAN_C，为局部邻域块的高斯加权和。该算法是在区域中(x, y)周围的像素根据高斯函数按照他们离中心点的距离进行加权计算。
                thresholdType: 二值化方法，只能选 THRESH_BINARY 或者 THRESH_BINARY_INV
                    THRESH_BINARY: 二值化, 大于阈值的赋最大色值, 其他赋0
                    THRESH_BINARY_INV: 二值化反转, 与 THRESH_BINARY 相反, 大于阈值的赋0, 其他赋最大色值
                blockSize: 分割计算的区域大小，取奇数
                    当blockSize越大，参与计算阈值的区域也越大，细节轮廓就变得越少，整体轮廓越粗越明显
                C：常数，每个区域计算出的阈值的基础上在减去这个常数作为这个区域的最终阈值，可以为负数
                    当C越大，每个像素点的N*N邻域计算出的阈值就越小，中心点大于这个阈值的可能性也就越大，设置成255的概率就越大，整体图像白色像素就越多，反之亦然。
            """
        return img

    @staticmethod
    def binary_remove_small_objects(img, threshold):
        """
        消除二值图像中面积小于某个阈值的连通域(消除孤立点)
        :param img: 二值图像(白底黑图)
        :param threshold: 符合面积条件大小的阈值
        """
        img_label, num = measure.label(img, background=255, connectivity=2, return_num=True)  # 输出二值图像中所有的连通域
        props = measure.regionprops(img_label)  # 输出连通域的属性，包括面积等
        resMatrix = np.zeros(img_label.shape)  # 创建0图
        for i in range(0, len(props)):
            if props[i].area > threshold:
                tmp = (img_label == i + 1).astype(np.uint8)
                resMatrix += tmp  # 组合所有符合条件的连通域
        resMatrix *= 255
        return 255 - resMatrix  # 本来输出的是黑底百图, 这里特意转换了黑白

    @staticmethod
    def similarity(img1, img2, block=10):
        """
        求两张二值化图片的相似度(简单实现)
        :param img1: 图片1
        :param img2: 图片2
        :param block: 分块对比的块边长, 从1开始, 边长越大精度越低
        """
        if img1.shape != img2.shape:
            return 0
        # 遍历图片, 计算同一位置相同色占总色数的比例
        height, width = img1.shape  # 经过处理后, 通道数只剩1个了
        # 相似度列表
        similarities = []
        # 根据给定的block大小计算分割的行列数, 将图片分为row行col列个格子(注意最后一行和最后一列的格子不一定是block大小)
        row = 1 if block >= height else (height // block + (0 if height % block == 0 else 1))
        col = 1 if block >= width else (width // block + (0 if width % block == 0 else 1))
        # print(f'图片宽度:{width},高度:{height}, 以块边长:{block}, 分为{row}行{col}列')
        for i in range(0, row):
            for j in range(0, col):
                # print('-')
                # 计算当前格子的w和h
                w = block if j + 1 < col else (width - (col - 1) * block)
                h = block if i + 1 < row else (height - (row - 1) * block)
                # print(f'当前遍历第{i + 1}行第{j + 1}列的块, 该块的宽度:{w},高度:{h}, 即该块有{h}行{w}列')
                counter = 0
                for x in range(block * i, block * i + h):
                    for y in range(block * j, block * j + w):
                        # print(f'x:{x},y:{y}')
                        if img1[x][y] == img2[x][y]:
                            counter += 1
                similarity = counter / (w * h)
                # print(f'当前块的相似度是:{similarity}')
                similarities.append(similarity ** 3)
        # print(similarities)
        return sum(similarities) / len(similarities)

    @staticmethod
    def cut(img, region):
        """
        从 img 中截取 region 范围. 入参图片需为 OpenCV 格式
        """
        left, top, width, height = region
        return img[top:top + height, left:left + width]

    @staticmethod
    def convert(img, gray=False, binary=None, remove=None):
        """
        图片(OpenCV BGR 格式)做灰度化和二值化处理
        :param img: OpenCV BGR 图片
        :param gray: 是否做灰度化处理
        :param binary: dict 格式, 非 None 做二值化处理
            具体参照 binary 方法的参数说明
            adaptive: 是否自适应二值化
            threshold: 非自适应二值化, 二值化阈值
            block: 自适应二值化邻域大小
            c: 常数
        :param remove: dict 格式, 非 None 做孤立点消除操作
            threshold: 连通域面积阈值, 小于该面积的连通域将被消除(黑转白)
        """
        if gray:
            img = Image.gray(img)
            if binary:
                if not isinstance(binary, dict):
                    return img
                adaptive = binary.get('adaptive')
                threshold = binary.get('threshold')
                block = binary.get('block')
                c = binary.get('c')
                img = Image.binary(img, adaptive, threshold, block, c)
                if remove:
                    if not isinstance(remove, dict):
                        return img
                    threshold = remove.get('threshold')
                    img = Image.binary_remove_small_objects(img, threshold)
        return img

    @staticmethod
    def read(path, gray=False, binary=None, remove=None):
        """
        读取一张图片(OpenCV BGR 格式)并做灰度化和二值化处理
        :param path: 图片路径
        :param gray: 是否做灰度化处理
        :param binary: dict 格式, 非 None 做二值化处理
        :param remove: dict 格式, 非 None 做孤立点消除操作
        """
        img = cv2.imread(path)
        img = Image.convert(img, gray, binary, remove)
        return img

    @staticmethod
    def load(directory, gray=False, binary=None, remove=None):
        """
        递归载入指定路径下的所有图片(OpenCV BGR 格式), 按照 (name, img) 的格式组合成为列表并返回
        """
        imgs = []
        for item in os.listdir(directory):
            path = os.path.join(directory, item)
            if os.path.isdir(path):
                temp = Image.load(path, gray, binary, remove)
                imgs.extend(temp)
            elif os.path.isfile(path):
                name = os.path.splitext(item)[0]
                img = Image.read(path, gray, binary, remove)
                imgs.append((name, img))
        return imgs if imgs else None


import cfg
from structure import Weapon


class Pubg:

    @staticmethod
    def game():
        """
        是否游戏窗体在最前
        """
        return '绝地求生' in GetWindowText(GetForegroundWindow())

    def __init__(self):
        w, h = Monitor.resolution()
        self.key = f'{w}.{h}'  # 分辨率键
        self.binary = {'adaptive': True, 'block': 3, 'c': 1}
        self.remove = {'threshold': 10}
        self.std_img_backpack = Image.read(rf'image/{self.key}/backpack.png', gray=True, binary=self.binary, remove=self.remove)
        self.std_imgs_sight_1 = Image.load(rf'image/{self.key}/weapon/attachment/sight/1', gray=True, binary=self.binary, remove=self.remove)
        self.std_imgs_sight_2 = Image.load(rf'image/{self.key}/weapon/attachment/sight/2', gray=True, binary=self.binary, remove=self.remove)
        self.std_imgs_muzzle = Image.load(rf'image/{self.key}/weapon/attachment/muzzle', gray=True, binary=self.binary, remove=self.remove)
        self.std_imgs_foregrip = Image.load(rf'image/{self.key}/weapon/attachment/foregrip', gray=True, binary=self.binary, remove=self.remove)
        self.std_imgs_stock = Image.load(rf'image/{self.key}/weapon/attachment/stock', gray=True, binary=self.binary, remove=self.remove)
        self.std_names = cfg.detect.get(self.key).get(cfg.weapon).get(cfg.name)

    def backpack(self):
        """
        是否在背包界面
        """
        region = cfg.detect.get(self.key).get(cfg.backpack)
        img = Capturer.grab(win=True, region=region, convert=True)
        img = Image.convert(img, gray=True, binary=self.binary, remove=self.remove)
        return Image.similarity(self.std_img_backpack, img) > 0.9

    def weapon(self):
        """
        在背包库存界面识别两把主武器及其配件
        """
        data = cfg.detect.get(self.key).get(cfg.weapon)
        region = data.get(cfg.region)
        # 截图主武器部分
        img = Capturer.grab(win=True, region=region, convert=True)
        # 识别两把主武器武器
        weapon1 = self.recognize(img, data.get(cfg.one))
        weapon2 = self.recognize(img, data.get(cfg.two))
        return weapon1, weapon2

    def bullet(self):
        """
        是否有子弹
        效率很低且不稳定, 单点检测都要耗时1-10ms
        获取颜色, COLORREF 格式, 0x00FFFFFF
        结果是int,
        可以通过 print(hex(color)) 查看十六进制值
        可以通过 print(color == 0x00FFFFFF) 进行颜色判断
        """
        x, y = cfg.detect.get(self.key).get(cfg.bullet)
        hdc = GetDC(None)
        color = GetPixel(hdc, x, y)
        # print(color)
        ReleaseDC(None, hdc)
        return color != 255

    def attitude(self):
        """
        姿态识别
        """
        data = cfg.detect.get(self.key).get(cfg.attitude)
        region = data.get(cfg.region)
        # 截图姿态部分
        img = Capturer.grab(win=True, region=region, convert=True)
        # 灰度化二值化
        img = Image.convert(img, gray=True, binary=self.binary)
        # cv2.imwrite('1.jpg', img)
        # 判断是否是站立
        counter = 0
        points = data.get(cfg.stand)
        for point in points:
            if img[point] == 0:
                counter += 1
        if counter == len(points):
            return cfg.stand
        # 判断是否是蹲下
        counter = 0
        points = data.get(cfg.squat)
        for point in points:
            if img[point] == 0:
                counter += 1
        if counter == len(points):
            return cfg.squat
        # 判断是否是趴卧
        counter = 0
        points = data.get(cfg.prone)
        for point in points:
            if img[point] == 0:
                counter += 1
        if counter == len(points):
            return cfg.prone
        # 不是3种姿态
        return None

    def firemode(self):
        """
        射击模式识别, 只限突击步枪和冲锋枪
        """
        data = cfg.detect.get(self.key).get(cfg.firemode)
        region = data.get(cfg.region)
        # 截图模式部分
        img = Capturer.grab(win=True, region=region, convert=True)
        # 灰度化
        img = Image.gray(img)
        # 二值化
        img = Image.binary(img, threshold=230)
        # cv2.imwrite(f'{int(time.perf_counter_ns())}.jpg', img)
        # 判断射击模式
        counter = 0
        points = data.get(cfg.points)
        for point in points:
            # print(img[point])
            if img[point] == 255:
                counter += 1
        if counter == 1:
            return cfg.only
        elif counter == 2 or counter == 3:
            return cfg.semi
        elif counter == 4:
            return cfg.auto
        # 非四种射击模式
        return None

    def index(self):
        """
        1/2号武器识别, 0:未持有1/2武器, 1:持有1号武器, 2:持有2号武器
        判定时机:
        鼠标滚轮滚动/1/2/3/4/5/G(切雷)/F(落地捡枪)/Tab(调整位置)
        投掷武器,近战武器和单发火箭炮等,用光后不会导致切换武器
        能量和药包等消耗品,使用前如果持有武器,使用后会切回该武器,使用前未持有武器,使用后不会切换武器
        """
        """
        测试发现
        主界面上右下角武器位和主武器只有下面3种情况
        1号位上显示1号武器
        1号位上显示1号武器, 2号位上显示2号武器
        1号位上显示2号武器
        """
        data = cfg.detect.get(self.key).get(cfg.active)
        region = data.get(cfg.region)
        # 截图模式部分
        # original = Capturer.grab(win=True, region=region, convert=True)
        original = Image.read(rf'image/test/1668492261904782600.png')
        img = Image.gray(original)
        img = Image.binary(img, adaptive=True, block=9)
        # cv2.imwrite(rf'image/result/{time.time_ns()}.jpg', img)
        # 识别存在的武器序号
        indexes = []
        one = data.get(cfg.one)
        two = data.get(cfg.two)
        counter = 0
        for point in one.get(1):
            # print(point, img[point])
            if img[point] == 0:
                counter += 1
        if counter == len(one.get(1)):
            indexes.append(1)
            counter = 0
            # print()
            for point in two.get(2):
                # print(point, img[point])
                if img[point] == 0:
                    counter += 1
            if counter == len(two.get(2)):
                indexes.append(2)
        else:
            counter = 0
            # print()
            for point in one.get(2):
                # print(point, img[point])
                if img[point] == 0:
                    counter += 1
            if counter == len(one.get(2)):
                indexes.append(2)
        print(indexes)
        # 根据识别到的武器序号判断激活的武器
        if len(indexes) == 0:
            return None
        if len(indexes) == 1:
            # 识别1号位是否激活
            active = self.active(original, one)
            return indexes[0] if active else None
        if len(indexes) == 2:
            # 识别1号位是否激活
            active = self.active(original, one)
            if active:
                return 1
            else:
                # 判断2号位是否激活
                active = self.active(original, two)
                return 2 if active else None
        # 其他情况
        return None

    """
    ---------- ---------- ---------- ---------- ----------
    """

    def name(self, img):
        """
        识别武器名称, 入参图片需为 OpenCV 格式
        """
        # 截图灰度化
        img = Image.gray(img)
        # 截图二值化
        img = Image.binary(img, threshold=254)
        # 数纯白色点
        height, width = img.shape
        counter = 0
        for row in range(0, height):
            for col in range(0, width):
                if 255 == img[row, col]:
                    counter += 1
        return self.std_names.get(counter)

    def attachment(self, imgs, img):
        """
        识别武器配件, 入参图片需为 OpenCV 格式
        """
        img = Image.convert(img, gray=True, binary=self.binary, remove=self.remove)
        for name, standard in imgs:
            similarity = Image.similarity(standard, img)
            # print(similarity, name)
            if similarity > 0.925:
                return name
        return None

    def recognize(self, img, config):
        """
        传入武器大图和识别名称配件的配置项, 返回识别到的武器. 入参图片需为 OpenCV 格式
        """
        # 判断武器是否存在
        exist = np.mean(img[config.get(cfg.point)]) == 255  # 取 BGR 列表的均值, 判断是不是纯白色
        if not exist:
            return None
        # 武器存在, 先识别名称
        name = self.name(Image.cut(img, config.get(cfg.name)))
        if not name:
            return None
        # 识别出武器名称后再识别配件
        index = config.get(cfg.index)
        sight = self.attachment(self.std_imgs_sight_1 if index == 1 else self.std_imgs_sight_2, Image.cut(img, config.get(cfg.sight)))
        muzzle = self.attachment(self.std_imgs_muzzle, Image.cut(img, config.get(cfg.muzzle)))
        foregrip = self.attachment(self.std_imgs_foregrip, Image.cut(img, config.get(cfg.foregrip)))
        stock = self.attachment(self.std_imgs_stock, Image.cut(img, config.get(cfg.stock)))
        return Weapon(name, sight, muzzle, foregrip, stock)

    def active(self, img, config):
        region = config.get(cfg.region)
        img = Image.cut(img, region)
        img = Image.gray(img, True)
        # img = Image.binary(img, adaptive=True, block=9)
        # cv2.imwrite(rf'image/result/{time.time_ns()}.jpg', img)

        cv2.imshow('res', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


        return False

















