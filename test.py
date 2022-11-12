import cv2

from toolkit import Game

img = Game.Image.read('image/3440.1440/weapon.attachment/sight/Holographic Sight.png')


# print(Game.Image.similarity(std, img, False, False, 100))

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img = cv2.adaptiveThreshold(img, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=3, C=1)

cv2.imshow('1', img)
cv2.waitKey(0)
