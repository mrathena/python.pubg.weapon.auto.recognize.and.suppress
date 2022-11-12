import cv2

from toolkit import Game

img = Game.Image.read('image/3440.1440/weapon.attachment/foregrip/Angled Foregrip.png', gray=True)

img = cv2.adaptiveThreshold(img, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=3, C=1)

img = Game.Image.remove_small_objects(img, 0)

cv2.imshow('1', img)
cv2.waitKey(0)
