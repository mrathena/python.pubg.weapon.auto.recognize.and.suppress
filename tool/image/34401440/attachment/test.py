import time

import cv2
import numpy as np

big = cv2.imread(r'C:\\Users\\mrathena\\Desktop\\20221020.160001.963.png')
t1 = time.perf_counter_ns()
small = cv2.imdecode(np.fromfile(r'C:\\Users\\mrathena\\Desktop\\战术枪托.png', dtype=np.uint8), -1)
small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
result = cv2.matchTemplate(big, small, cv2.TM_SQDIFF_NORMED)
# 归一化处理
cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX, -1)
# 寻找矩阵（一维数组当做向量，用Mat定义）中的最大值和最小值的匹配结果及其位置
minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
print(minVal, maxVal, minLoc, maxLoc)
t2 = time.perf_counter_ns()
print((t2 - t1) // 1000 // 1000)
# 对于cv2.TM_SQDIFF及cv2.TM_SQDIFF_NORMED方法min_val越趋近与0匹配度越好，匹配位置取min_loc; 其他方法max_val越趋近于1匹配度越好，匹配位置取max_loc
# 绘制矩形边框，将匹配区域标注出来
# min_loc：矩形定点
# (min_loc[0]+twidth,min_loc[1]+theight)：矩形的宽高
# (0,0,225)：矩形的边框颜色；2：矩形边框宽度
height, width = small.shape[:2]
cv2.rectangle(big, minLoc, (minLoc[0] + width, minLoc[1] + height), (0, 225, 0), 1)
# 显示结果,并将匹配值显示在标题栏上
cv2.imshow(str(minVal), big)
cv2.waitKey()
cv2.destroyAllWindows()
