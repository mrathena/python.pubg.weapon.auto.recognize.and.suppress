from toolkit import Game

img1 = Game.Image.read('image/3440.1440/weapon.attachment/foregrip/Angled Foregrip.png')
img2 = Game.Image.read('image/3440.1440/weapon.attachment/foregrip/Angled Foregrip.png')

print(Game.Image.similarity(img1, img2, gray=True, binary=True, threshold=40, block=11))
