
import cfg


class Weapon:

    def __init__(self, name, sight, muzzle, foregrip, stock):
        self.name = name
        self.sight = sight
        self.muzzle = muzzle
        self.foregrip = foregrip
        self.stock = stock

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
