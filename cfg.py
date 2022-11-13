one = 'one'
two = 'two'
mode = 'mode'
name = 'name'
game = 'game'
data = 'data'
pack = 'pack'
sight = 'sight'
color = 'color'
point = 'point'
index = 'index'
shake = 'shake'
speed = 'speed'
count = 'count'
armed = 'armed'
empty = 'empty'
exist = 'exist'
stock = 'stock'
weapon = 'weapon'
region = 'region'
muzzle = 'muzzle'
letter = 'letter'
switch = 'switch'
bullet = 'bullet'  # 子弹
differ = 'differ'
turbo = 'turbo'
trigger = 'trigger'
restrain = 'restrain'
strength = 'strength'
positive = 'positive'  # 肯定的
negative = 'negative'  # 否定的
backpack = 'backpack'
foregrip = 'foregrip'
inventory = 'inventory'

# 检测数据
detect = {
    "3440.1440": {
        inventory: (936, 78, 80, 40),  # 检测背包是否打开的位置
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

        mode: {  # 武器模式, 全自动/半自动/单发/其他
            color: 0x00FFFFFF,
            '1': (3151, 1347),  # 全自动
            '2': (3171, 1351),  # 半自动
        },
        armed: {  # 是否持有武器(比如有武器但用拳头就是未持有武器)

        },
        empty: {  # 是否空弹夹(武器里子弹数为0)
            color: 0x00FFFFFF,
            '1': (3204, 1306),  # 十位数, 该点白色即非0, 非0则一定不空
            '2': (3229, 1294),  # 个位数, 该点白色即为0, 十位为0且个位为0为空
        },
    },
    "2560.1440": {

    },
    "2560.1080": {

    },
    "1920.1080": {

    }
}

# 武器数据
data = {

}
