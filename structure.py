

class Weapon:

    def __init__(self, name, sight, muzzle, foregrip, stock):
        self.name = name
        self.sight = sight
        self.muzzle = muzzle
        self.foregrip = foregrip
        self.stock = stock

    def __str__(self):
        return f'武器:{self.name}, 瞄具:{self.sight}, 枪口:{self.muzzle}, 握把:{self.foregrip}, 枪托:{self.stock}'
