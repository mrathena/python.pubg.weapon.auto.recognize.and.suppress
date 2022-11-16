one = 'one'
two = 'two'
game = 'game'
only = 'only'
semi = 'semi'
auto = 'auto'
name = 'name'
data = 'data'
sight = 'sight'
color = 'color'
point = 'point'
index = 'index'
speed = 'speed'
count = 'count'
armed = 'armed'
empty = 'empty'
stock = 'stock'
stand = 'stand'
squat = 'squat'
prone = 'prone'
weapon = 'weapon'
region = 'region'
points = 'points'
muzzle = 'muzzle'
switch = 'switch'
bullet = 'bullet'
active = 'active'
backpack = 'backpack'
foregrip = 'foregrip'
attitude = 'attitude'
firemode = 'firemode'
interval = 'interval'
ballistic = 'ballistic'

# 检测数据
detect = {
    "3440.1440": {
        backpack: (936, 78, 80, 40),  # 检测背包是否打开的位置
        weapon: {
            region: (2212, 125, 632, 577),  # 一二号武器全截图
            one: {
                index: 1,
                point: (16, 20),  # (y, x), 判断一号武器是否存在的点(纯白色)
                name: (42, 0, 260, 42),
                sight: (365, 29, 62, 31),
                muzzle: (2, 207, 62, 62),
                foregrip: (138, 207, 62, 62),
                stock: (568, 207, 62, 62),
            },
            two: {
                index: 2,
                point: (319, 18),  # (y, x), 判断二号武器是否存在的点(纯白色)
                name: (42, 308, 260, 42),
                sight: (365, 335, 62, 31),
                muzzle: (2, 514, 62, 62),
                foregrip: (138, 514, 62, 62),
                stock: (568, 514, 62, 62),
            },
            name: {
                769: 'ACE32',
                561: 'AKM',
                511: 'AUG',
                1269: 'Beryl M762',
                716: 'G36C',
                568: 'Groza',
                309: 'K2',
                794: 'M16A4',
                646: 'M416',
                1360: 'Mk47 Mutant',
                552: 'QBZ',
                798: 'SCAR-L',
                669: 'Mini14',
                602: 'Mk12',
                588: 'Mk14',
                597: 'QBU',
                494: 'SKS',
                1627: 'SLR',
                464: 'VSS',
                636: 'Crossbow',
                715: 'DP-28',
                710: 'M249 ',
                605: 'MG3',
                846: 'Mortar',
                1325: 'Panzerfaust',
                564: 'DBS',
                423: 'O12',
                556: 'S12K',
                758: 'S1897',
                737: 'S686',
                647: 'AWM',
                872: 'Kar98k',
                993: 'Lynx AMR',
                513: 'M24',
                1611: 'Mosin Nagant',
                740: 'Win94',
                934: 'Micro UZI',
                742: 'MP5K',
                608: 'MP9',
                559: 'P90',
                1207: 'PP-19 Bizon',
                1567: 'Tommy Gun',
                880: 'UMP45',
                624: 'Vector',
                1917: 'Blue Chip Detector',
                1553: 'Drone Tablet',
                1664: 'EMT Gear',
                843: 'Spotter Scope',
                947: 'Tactical Pack',
            },
        },
        attitude: {  # 姿态识别
            region: (1374, 1312, 66, 59),
            stand: [(37, 33), (37, 28), (17, 28), (20, 17)],  # (y, x), 纯黑色
            squat: [(19, 39), (20, 51), (36, 13), (41, 28)],
            prone: [(33, 48), (34, 60), (39, 25), (41, 18)],
        },
        firemode: {  # 武器模式识别
            region: (1649, 1331, 27, 31),
            points: [(3, 13), (8, 13), (14, 13), (19, 13)]
        },
        bullet: (1712, 1324),  # 纯红色则没有子弹
        active: {  # 识别当前使用的武器序号
            region: (2810, 1250, 240, 153),
            one: {  # 主界面右下角一号武器展示位
                # region: (0, 89, 207, 65),
                region: (0, 112, 207, 1),
                1: [(98, 217), (98, 215), (100, 217), (102, 217), (104, 217), (106, 217)],  # 一号武器展示位展示1号武器
                2: [(99, 215), (97, 215), (97, 217), (97, 219), (97, 217), (102, 217), (106, 215), (106, 220)],  # 一号武器展示位展示2号武器
            },
            two: {
                # region: (0, 10, 207, 65),
                region: (0, 33, 207, 1),
                2: [(20, 215), (18, 215), (18, 217), (18, 219), (20, 219), (22, 219), (27, 215), (27, 220)],  # 主界面右下角二号武器展示位
            },
        },
    },
    "2560.1440": {

    },
    "2560.1080": {

    },
    "1920.1080": {

    }
}

# 翻译数据
translation = {
    'ACE32': 'ACE32',
    'AKM': 'AKM',
    'AUG': 'AUG',
    'Beryl M762': 'Beryl M762',
    'G36C': 'G36C',
    'Groza': 'Groza',
    'K2': 'K2',
    'M16A4': 'M16A4',
    'M416': 'M416',
    'Mk47 Mutant': 'Mk47 Mutant',
    'QBZ': 'QBZ',
    'SCAR-L': 'SCAR-L',
    'Mini14': 'Mini14',
    'Mk12': 'Mk12',
    'Mk14': 'Mk14',
    'QBU': 'QBU',
    'SKS': 'SKS',
    'SLR': '自动装填步枪',
    'VSS': 'VSS',
    'Crossbow': '十字弩',
    'DP-28': 'DP-28',
    'M249 ': 'M249 ',
    'MG3': 'MG3',
    'Mortar': '迫击炮',
    'Panzerfaust': '铁拳火箭筒',
    'DBS': 'DBS',
    'O12': 'O12',
    'S12K': 'S12K',
    'S1897': 'S1897',
    'S686': 'S686',
    'AWM': 'AWM',
    'Kar98k': 'Kar98k',
    'Lynx AMR': 'Lynx AMR',
    'M24': 'M24',
    'Mosin Nagant': '莫辛纳甘步枪',
    'Win94': 'Win94',
    'Micro UZI': '微型 UZI',
    'MP5K': 'MP5K',
    'MP9': 'MP9',
    'P90': 'P90',
    'PP-19 Bizon': 'PP-19 Bizon',
    'Tommy Gun': '汤姆逊冲锋枪',
    'UMP45': 'UMP45',
    'Vector': 'Vector',
    'Blue Chip Detector': '蓝色晶片探测器',
    'Drone Tablet': '无人机控制器',
    'EMT Gear': '应急处理装备',
    'Spotter Scope': '观测镜',
    'Tactical Pack': '战术背包',
    'Angled Foregrip': '直角前握把',
    'Haalfgrip': '半截式握把',
    'Laser Sight': '激光瞄准器',
    'Lightweight Grip': '轻型握把',
    'Quiver': '箭袋',
    'Thumbgrip': '拇指握把',
    'Vertical Foregrip': '垂直握把',
    'Choke SG': '扼流圈',
    'Compensator AR': '后座补偿器',
    'Compensator SR': '后座补偿器',
    'Compenstor SMG': '枪口补偿器',
    'Duckbill SG': '鸭嘴枪口',
    'Flash Hider AR': '消焰器',
    'Flash Hider SMG': '消焰器',
    'Flash Hider SR': '消焰器',
    'Suppressor AR': '消音器',
    'Suppressor SMG': '消音器',
    'Suppressor SR': '消音器',
    '15x Scope': '15x镜',
    '2x Scope': '2x镜',
    '3x Scope': '3x镜',
    '4x Scope': '4x镜',
    '6x Scope': '6x镜',
    '8x Scope': '8x镜',
    'Holographic Sight': '全息',
    'Red Dot Sight': '红点',
    'Bullet Loops': '子弹袋',
    'Cheek Pad': '托腮板',
    'Folding Stock': '折叠式枪托',
    'Heavy Stock': '重型枪托',
    'Tactical Stock': '战术枪托',
}

# 武器数据, 在列表中的武器才会执行压制
weapons = {
    'M416': {
        interval: 85,  # 全自动射击间隔
        attitude: {  # 姿态影响因子
            stand: 1,
            squat: 0.75,
            prone: 0.5,
        },
        sight: {  # 瞄具影响因子
            '2x Scope': 1.7,
            '3x Scope': 2.6,
            '4x Scope': 3.6,
            '6x Scope': 5.1,
            'Holographic Sight': 1,
            'Red Dot Sight': 1,
        },
        muzzle: {  # 枪口影响因子
            'Compensator AR': 0.84,
            'Flash Hider AR': 0.84,
            'Suppressor AR': 1,
        },
        foregrip: {  # 握把影响因子
            'Angled Foregrip': 1,
            'Haalfgrip': 0.77,
            'Laser Sight': 1,
            'Lightweight Grip': 0.77,
            'Thumbgrip': 0.92,
            'Vertical Foregrip': 0.77,
        },
        stock: {  # 枪托影响因子
            'Heavy Stock': 0.965,
            'Tactical Stock': 0.965,
        },
        ballistic: [36, 23, 24, 23, 33, 34, 34, 34, 40, 40, 40, 40, 41, 41, 41, 42, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 50, 51, 50, 51, 50, 50, 50]
    },

}
