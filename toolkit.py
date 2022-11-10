import cv2
import d3dshot
import mss as pymss
import numpy as np

from win32api import GetSystemMetrics
from win32con import SRCCOPY, SM_CXSCREEN, SM_CYSCREEN
from win32gui import GetDesktopWindow, GetWindowDC, DeleteObject, ReleaseDC
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
