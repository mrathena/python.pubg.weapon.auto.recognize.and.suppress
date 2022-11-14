import cfg


class Weapon:

    def __init__(self, name, sight, muzzle, foregrip, stock):
        self.name = name
        self.sight = sight
        self.muzzle = muzzle
        self.foregrip = foregrip
        self.stock = stock
        self.data = cfg.weapons.get(self.name)
        self.suppress = True if self.data else False  # 该武器是否可以执行压制
        if self.data:
            self.interval = self.data.get(cfg.interval)  # 射击间隔
            self.ballistic = self.data.get(cfg.ballistic)  # 垂直弹道
            self.factor = self.data.get(cfg.sight).get(self.sight, 1) \
                          * self.data.get(cfg.muzzle).get(self.muzzle, 1) \
                          * self.data.get(cfg.foregrip).get(self.foregrip, 1) \
                          * self.data.get(cfg.stock).get(self.stock, 1)

    def attitude(self, attitude):
        """
        根据传入的姿态, 获取该武器对应数据中的姿态影响因子
        """
        return self.data.get(cfg.attitude).get(attitude, 1)

    def __str__(self):
        name = cfg.translation.get(self.name)
        sight = cfg.translation.get(self.sight)
        muzzle = cfg.translation.get(self.muzzle)
        foregrip = cfg.translation.get(self.foregrip)
        stock = cfg.translation.get(self.stock)
        string = f'[{name}]'
        if sight:
            string += f', {sight}'
        if muzzle:
            string += f', {muzzle}'
        if foregrip:
            string += f', {foregrip}'
        if stock:
            string += f', {stock}'
        # print(f'武器:{self.name}, 瞄具:{self.sight}, 枪口:{self.muzzle}, 握把:{self.foregrip}, 枪托:{self.stock}')
        return string
