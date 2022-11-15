import time

import cv2

from toolkit import Pubg, Timer, Image

region = (2810, 1250, 240, 153)
# img = grab(region)
# mss.tools.to_png(img.rgb, img.size, output=f'image/test/{time.time_ns()}.png')
# img = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)

# imgs = Image.load(rf'image/test', True, {'adaptive': True}, {'threshold': 10})
imgs = Image.load(rf'image/test')

for name, img in imgs:

    img = Image.gray(img, True)
    cv2.imwrite(rf'image/test/{name}.jpg', img)

    img = Image.binary(img, adaptive=True, block=9)
    # img = Image.binary(img, threshold=210)
    # cv2.imwrite(rf'image/result/{time.time_ns()}.jpg', img)

    img = Image.binary_remove_small_objects(img, 10)
    # cv2.imwrite(rf'image/result/{time.time_ns()}.jpg', img)




