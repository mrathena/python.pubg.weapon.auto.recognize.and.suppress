import os
import cv2
import d3dshot
import mss as pymss
import numpy as np
from skimage import measure  # pip install scikit-image

from win32api import GetSystemMetrics  # conda install pywin32
from win32con import SRCCOPY, SM_CXSCREEN, SM_CYSCREEN
from win32gui import GetDesktopWindow, GetWindowDC, DeleteObject, ReleaseDC, GetWindowText, GetForegroundWindow
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
            return f'{interval / 1000}us'
        elif interval < 1_000_000_000:
            return f'{interval / 1_000_000}ms'
        else:
            return f'{interval / 1_000_000_000}s'


class Image:

    @staticmethod
    def cut(img, region):
        """
        从 img 中截取 region 范围. 入参图片需为 OpenCV 格式
        """
        left, top, width, height = region
        return img[top:top + height, left:left + width]

    @staticmethod
    def remove_small_objects(img, threshold):
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
    def convert(img, gray=False, binary=False):
        """
        图片(OpenCV BGR 格式)做灰度化和二值化处理
        """
        if gray:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if binary:
                # 自适应二值化
                img = cv2.adaptiveThreshold(img, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=3, C=1)
                # 消除二值图像孤立点
                img = Image.remove_small_objects(img, 10)
        return img

    @staticmethod
    def read(path, gray=False, binary=False):
        """
        读取一张图片(OpenCV BGR 格式)并做灰度化和二值化处理
        """
        if gray:
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if binary:
                # 自适应二值化
                img = cv2.adaptiveThreshold(img, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=3, C=1)
                # 消除二值图像孤立点
                img = Image.remove_small_objects(img, 10)
        else:
            img = cv2.imread(path)
        return img

    @staticmethod
    def load(directory, gray=False, binary=False):
        """
        递归载入指定路径下的所有图片(OpenCV BGR 格式), 按照 (name, img) 的格式组合成为列表并返回
        :param directory: 目录
        :param gray: 图片是否灰做度化处理
        :param binary: 在灰度化处理的基础上, 图片是否做二值化处理
        :param threshold: 二值化阈值, 灰度图中, 大于该值的被赋值255, 小于等于该值的赋值0
        """
        imgs = []
        for item in os.listdir(directory):
            # item, 不包含路径前缀
            # path, 完整路径
            path = os.path.join(directory, item)
            if os.path.isdir(path):
                temp = Image.load(path, gray, binary)
                imgs.extend(temp)
            elif os.path.isfile(path):
                name = os.path.splitext(item)[0]
                img = Image.read(path, gray, binary)
                imgs.append((name, img))
        return imgs if imgs else None

    @staticmethod
    def similarity(img1, img2, gray=False, binary=False, block=10):
        """
        两张相同宽高和通道数的 OpenCV BGR 格式图片
        或 两张相同 shape OpenCV BGR 格式图片 经过指定的灰度化与二值化处理后的图片
        简单求的相似度(图片需经过灰度化与二值化处理)
        :param img1: 图片1
        :param img2: 图片2
        :param gray: 图片是否灰做度化处理
        :param binary: 在灰度化处理的基础上, 图片是否做二值化处理
        :param threshold: 二值化阈值, 灰度图中, 大于该值的被赋值255, 小于等于该值的赋值0
        :param block: 分块对比的块边长, 从1开始, 边长越大精度越低
        """
        if img1.shape != img2.shape:
            return 0
        img1 = Image.convert(img1, gray, binary)
        img2 = Image.convert(img2, gray, binary)
        # cv2.imwrite('1.jpg', img1)
        # cv2.imwrite('2.jpg', img2)
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


import cfg
from structure import Weapon


class Pubg:

    def __init__(self):
        w, h = Monitor.resolution()
        self.key = f'{w}.{h}'  # 分辨率键
        self.std_img_backpack = Image.read(rf'image/{self.key}/backpack.png', gray=True, binary=True)
        self.std_imgs_sight_1 = Image.load(rf'image/{self.key}/weapon.attachment/sight/1', gray=True, binary=True)
        self.std_imgs_sight_2 = Image.load(rf'image/{self.key}/weapon.attachment/sight/2', gray=True, binary=True)
        self.std_imgs_muzzle = Image.load(rf'image/{self.key}/weapon.attachment/muzzle', gray=True, binary=True)
        self.std_imgs_foregrip = Image.load(rf'image/{self.key}/weapon.attachment/foregrip', gray=True, binary=True)
        self.std_imgs_stock = Image.load(rf'image/{self.key}/weapon.attachment/stock', gray=True, binary=True)
        self.std_names = cfg.detect.get(self.key).get(cfg.weapon).get(cfg.name)

    def game(self):
        """
        是否游戏窗体在最前
        """
        return '绝地求生' in GetWindowText(GetForegroundWindow())

    def backpack(self):
        """
        是否在背包界面
        """
        region = cfg.detect.get(self.key).get(cfg.backpack)
        img = Capturer.grab(win=True, region=region, convert=True)
        img = Image.convert(img, gray=True, binary=True)
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

    """
    ---------- ---------- ---------- ---------- ----------
    """

    @staticmethod
    def translate(weapon):
        """
        翻译武器和配件名称
        """
        if not weapon or not isinstance(weapon, Weapon):
            return None
        name = cfg.translation.get(weapon.name)
        sight = cfg.translation.get(weapon.sight)
        muzzle = cfg.translation.get(weapon.muzzle)
        foregrip = cfg.translation.get(weapon.foregrip)
        stock = cfg.translation.get(weapon.stock)
        string = f'[{name}]'
        if sight:
            string += f', {sight}'
        if muzzle:
            string += f', {muzzle}'
        if foregrip:
            string += f', {foregrip}'
        if stock:
            string += f', {stock}'
        return string

    """
    ---------- ---------- ---------- ---------- ----------
    """

    def name(self, img):
        """
        识别武器名称, 入参图片需为 OpenCV 格式
        """
        # 截图灰度化
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 截图二值化
        ret, img = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)
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
        img = Image.convert(img, gray=True, binary=True)
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


















