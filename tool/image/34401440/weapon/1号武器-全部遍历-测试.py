import time

import pynput
from win32gui import GetDC, ReleaseDC, GetPixel  # conda install pywin32,

data = [
    (2382, 134, 'Beryl M762'),
    (2394, 134, 'Blue Chip Detector'),
    (2412, 134, 'Tactical Pack'),
    (2380, 135, 'Spotter Scope'),
    (2391, 135, 'Drone Tablet '),
    (2269, 136, 'Tommy Gun'),
    (2359, 136, 'Mosin Nagant'),
    (2360, 136, 'Lynx AMR'),
    (2363, 136, 'Micro UZI'),
    (2349, 137, 'Kar98k'),
    (2358, 137, 'Panzerfaust'),
    (2334, 138, 'ACE32'),
    (2339, 138, 'UMP45'),
    (2340, 138, 'DP-28'),
    (2342, 138, 'Mk47 Mutant'),
    (2343, 138, 'Crossbow'),
    (2345, 138, 'PP-19 Bizon'),
    (2346, 138, 'SCAR-L'),
    (2327, 139, 'EMT Gear'),
    (2328, 139, 'S1897'),
    (2335, 139, 'M16A4'),
    (2336, 139, 'Win94'),
    (2276, 140, 'K2'),
    (2328, 140, 'MP5K'),
    (2329, 140, 'S686'),
    (2330, 140, 'M249 '),
    (2330, 141, 'Mini14'),
    (2331, 141, 'G36C'),
    (2294, 143, 'M416'),
    (2323, 143, 'AWM'),
    (2325, 144, 'Vector'),
    (2342, 144, 'Mortar'),
    (2293, 145, 'Groza'),
    (2294, 145, 'DBS'),
    (2319, 145, 'Mk12'),
    (2320, 145, 'Mk14'),
    (2274, 147, 'VSS'),
    (2274, 148, 'P90'),
    (2293, 148, 'MP9'),
    (2295, 149, 'M24'),
    (2296, 149, 'AUG'),
    (2303, 149, 'AKM'),
    (2308, 149, 'QBZ'),
    (2309, 149, 'SKS'),
    (2310, 149, 'S12K'),
    (2315, 149, 'QBU'),
    (2316, 149, 'MG3'),
    (2270, 150, 'O12'),
    (2278, 150, 'SLR'),
]


def pixel(x, y):
    hdc = GetDC(None)
    color = GetPixel(hdc, x, y)
    ReleaseDC(None, hdc)  # 一定要释放DC, 不然随着该函数调用次数增加会越来越卡, 表现就是不调用该函数, 系统会每两秒卡一下, 调用次数越多, 卡的程度越厉害
    return color


def click(x, y, button, pressed):
    if pressed:
        if button == pynput.mouse.Button.right:
            # 侧下键
            flag = False
            t1 = time.perf_counter_ns()
            for item in data:
                x, y, name = item
                if 0x00FFFFFF == pixel(x, y):
                    flag = True
                    print(item)
                    break
            t2 = time.perf_counter_ns()
            if flag:
                print(f'{(t2 - t1) // 1000 // 1000}ms')
            else:
                print('失败')

        elif button == pynput.mouse.Button.x2:
            # 侧上键
            return False


listener = pynput.mouse.Listener(on_click=click)
listener.start()
listener.join()

