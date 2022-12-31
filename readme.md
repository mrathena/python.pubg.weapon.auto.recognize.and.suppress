
# 说明

通过监听键鼠来触发武器自动识别, 将自动识别武器和加载压枪数据的操作分散在常规操作中. 按下左键开火时, 执行对应的压枪数据

功能说明
- 已完成项: 背包识别, 武器识别, 配件识别, 射击模式识别, 角色姿态识别, 剩余弹药识别, 游戏内键鼠操作, 自动识别与压枪主循环逻辑
- 未完成项: 自动识别当前激活的主武器, 是1号还是2号, 可以稍微修改下主逻辑, 用按1/2手动指定激活武器来代替自动识别

数据说明, 可自行精修
- 压枪数据来自于 [GitHub PUBGRecognizeAndGunpress](https://github.com/Cjy-CN/PUBGRecognizeAndGunpress), 没有做精修(其实是不会), 勉强能用, 可调整初始化参数中的 ADS 来修改基准倍率

按键说明, 可自行修改适合自己的键位
- 结束程序: End
- 开关切换: 鼠标侧下键
- 武器识别: 鼠标滚轮滚动/1/2/3/4/5/G(切雷)/F(落地捡枪)/X(收起武器)/Tab(调整位置)/ 等按键触发修改
- 姿态识别: 鼠标右键按下
- 模式识别: 鼠标右键按下

适配说明, 目前仅适配了 3440×1440 分辨率下无边框窗口模式, 其他分辨率可自行适配

源码说明
- logitech.driver.dll: 大佬封装的可以直接调用罗技驱动的库
- logitech.test.py: 调用 logitech.driver.dll 的演示, 以及测试罗技驱动环境是否有效(是否能通过代码操纵鼠标移动)
- cfg.py: 数据, 包括检测数据和武器数据
- toolkit.py: 工具包, 包括截图工具, 屏幕工具, 游戏内检测功能封装等
- pubg.py: 自动识别与压枪主程序
  - 参数: ads: 基本可以认为是游戏内的鼠标灵敏度, 通过调整该参数并测试效果, 在压枪效果达到最好时, ads 值就是合适的值
  
# 环境准备

```shell
conda create -n pubg python=3.10 # 使用 conda 创建名为 pubg 的虚拟环境
conda remove -n pubg --all # 删除虚拟环境
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple # 安装依赖
pyinstaller pubg.py -p cfg.py -p toolkit.py -p structure.py -p mouse.device.lgs.dll # 打包
  -F: 打包成一个 exe 文件
  -w: 运行时不显示黑框
```

## 操纵键鼠

大多FPS游戏都屏蔽了操作鼠标的Win函数, 要想在游戏中用代码操作鼠标, 需要一些特殊的办法, 其中罗技驱动算是最简单方便的了

代码直接控制罗技驱动向操作系统(游戏)发送鼠标命令, 达到了模拟鼠标操作的效果, 这种方式是鼠标无关的, 任何鼠标都可以实现

我们不会直接调用罗技驱动, 但是有大佬已经搭过桥了, 有现成的调用驱动的dll, 只是需要安装指定版本的罗技驱动配合才行

### 驱动安装和系统设置

> [百度网盘 罗技键鼠驱动](https://pan.baidu.com/s/1VkE2FQrNEOOkW6tCOLZ-kw?pwd=yh3s)

罗技驱动分 LGS (老) 和 GHub (新), LGS 的话, 需要使用 9.02.65 版本的, GHub 的话, 需要使用 2021.11 之前的, 二者自选其一即可

装好驱动后, 无需重启电脑. 运行 `屏蔽GHUB更新.exe` 防止更新

另外需要确保 控制面板-鼠标-指针选项 中下面两个设置
- 提高指针精确度 选项去掉, 不然会造成实际移动距离变大
- 选择指针移动速度 要在正中间, 靠右会导致实际移动距离过大, 靠左会导致指针移动距离过小

### 代码

大佬封装的 `logitech.driver.dll` 没有文档, 下面是某老哥列出的该库里面的方法, 具体用法参考 `logitech.test.py`

![](https://github.com/mrathena/python.apex.weapon.auto.recognize.and.suppress/blob/master/readme/20221204.131618.213.png)

## 键鼠监听

> [Pynput 说明](https://pypi.org/project/pynput/)

注意调试回调方法的时候, 不要打断点, 不然会卡死IO, 导致鼠标键盘失效

回调方法如果返回 False, 监听线程就会自动结束, 所以不要随便返回 False

键盘的特殊按键采用 `keyboard.Key.tab` 这种写法，普通按键用 `keyboard.KeyCode.from_char('c')` 这种写法, 有些键不知道该怎么写, 可以 `print(key)` 查看信息

> 钩子函数本身是阻塞的。也就是说钩子函数在执行的过程中，用户正常的键盘/鼠标操作是无法输入的。所以在钩子函数里面必须写成有限的操作（即O(1)时间复杂度的代码），也就是说像背包内配件及枪械识别，还有下文会讲到的鼠标压枪这类时间开销比较大或者持续时间长的操作，都不适合写在钩子函数里面。这也解释了为什么在检测到Tab（打开背包）、鼠标左键按下时，为什么只是改变信号量，然后把这些任务丢给别的进程去做的原因。

# 扩展

## Python 武器自动识别与压枪

> [GitHub python.apex.weapon.auto.recognize.and.suppress](https://github.com/mrathena/python.apex.weapon.auto.recognize.and.suppress)

> [GitHub python.pubg.weapon.auto.recognize.and.suppress](https://github.com/mrathena/python.pubg.weapon.auto.recognize.and.suppress)

## Python YOLO AI 目标检测与自瞄

> [CSDN Python Apex YOLO V5 6.2 目标检测与自瞄 全过程记录](https://blog.csdn.net/mrathena/article/details/126860226)

> [GitHub python.yolo.apex.autoaim.helper](https://github.com/mrathena/python.yolo.apex.autoaim.helper)

因为没有计算机视觉相关方向的专业知识, 所以做出来的东西, 有一定效果, 但是还有很多不足

不同的游戏, 都需要准备大量精准的数据集做训练, 才能取得比较好的效果

# 拓展 通用型人体骨骼检测 与 自瞄, 训练一次, FPS 游戏通用

> [【亦】警惕AI外挂！我写了一个枪枪爆头的视觉AI，又亲手“杀死”了它](https://www.bilibili.com/video/BV1Lq4y1M7E2/)

> [YOLO V7 keypoint 人体关键点检测](https://xugaoxiang.com/2022/07/21/yolov7/)

大多数 FPS 游戏中要检测的目标都为人形, 可以训练一个 通用型人体骨骼检测模型, 在类似游戏中应该有不错的效果
