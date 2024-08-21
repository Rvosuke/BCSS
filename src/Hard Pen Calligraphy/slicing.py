import cv2
import numpy as np
import os


point_lu = []
point_rd = []

point_lux = []
point_luy = []
point_ldx = []
point_ldy = []
point_rux = []
point_ruy = []
point_rdx = []
point_rdy = []

scale_x = 10  # xy的分割数量，也是角点的搜索范围
scale_y = 14

single_size = 50

image_path = './img/105.jpg'
image=cv2.imread(image_path)
h = int(1000 * image.shape[1] / image.shape[0])
image = cv2.resize(image, (h, 1000))
image_ori = image.copy()
print(image_ori.shape)

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)# 转成灰度图片
ret, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)# 二值化操作

dst=cv2.cornerHarris(binary,4,5,0.06)#调用函数cornerHarris
# print(dst.shape)
dst_norm=np.empty(dst.shape,dtype=np.float32)
cv2.normalize(dst,dst_norm,alpha=0,beta=255,norm_type=cv2.NORM_MINMAX)  # 归一化

for i in range(int(dst_norm.shape[0] / 4)):
    for j in range(int(dst_norm.shape[1] / 4)):
        if int(dst_norm[i,j])>120:
            point_luy.append(i)
            point_lux.append(j)
            point_lu.append(i**2 + j**2)
            cv2.circle(image,(i, j),2,(0,255,0),2)
index = point_lu.index(min(point_lu))
lu = (point_lux[index], point_luy[index])
cv2.circle(image,(lu[0], lu[1]),2,(0,255,0),2)
print(lu)

for i in range(int(dst_norm.shape[0] / 4 * 3), dst_norm.shape[0]):
    for j in range(int(max(0, lu[0] - dst_norm.shape[1] / (scale_x*2))), int(lu[0] + dst_norm.shape[1] / (scale_x*2))):
        if int(dst_norm[i, j]) > 120:
            point_ldy.append(i)
            point_ldx.append(j)
            cv2.circle(image,(i, j),2,(0,255,0),2)
index = point_ldy.index(max(point_ldy))
ld = (point_ldx[index], point_ldy[index])
cv2.circle(image,(ld[0], ld[1]),2,(0,255,0),2)
print(ld)

for i in range(int(lu[1] - dst_norm.shape[0] / (scale_y*2)), min(dst_norm.shape[0], int(lu[1] + dst_norm.shape[0] / (scale_y*2)))):
    for j in range(int(dst_norm.shape[1] / 3 * 2), dst_norm.shape[1]):
    # for j in range(int(dst_norm.shape[1]), dst_norm.shape[1]):
        if int(dst_norm[i,j])>120:
            point_ruy.append(i)
            point_rux.append(j)
            cv2.circle(image,(i, j),2,(0,255,0),2)
# print(point_rux, point_ruy)
# cv2.imshow('image', image)
# cv2.waitKey(0)

index = point_rux.index(max(point_rux))
ru = (point_rux[index], point_ruy[index])
cv2.circle(image,(ru[0], ru[1]),2,(0,255,0),2)
print(ru)

for i in range(int(ld[1] - dst_norm.shape[0] / (scale_y*2)), min(dst_norm.shape[0], int(ld[1] + dst_norm.shape[0] / (scale_y*2)))):
    for j in range(int(ru[0] - dst_norm.shape[1] / (scale_x*1)), dst_norm.shape[1]):
        if int(dst_norm[i,j])>120:
            point_rdy.append(i)
            point_rdx.append(j)
            point_rd.append(i**2 + j**2)
            # cv2.circle(image,(i, j),2,(0,255,0),2)
# print(point_rdx, point_rdy)
index = point_rd.index(max(point_rd))
rd = (point_rdx[index], point_rdy[index])
cv2.circle(image,(rd[0], rd[1]),2,(0,255,0),2)
print(rd)

cv2.imshow('image', image)
cv2.waitKey(0)


pts1 = np.float32([lu, ld, rd, ru])
pts2 = np.float32([[0, 0], [0, dst_norm.shape[1]], [dst_norm.shape[0], dst_norm.shape[1]], [dst_norm.shape[0], 0]])
matrix = cv2.getPerspectiveTransform(pts1, pts2)
result = cv2.warpPerspective(image_ori, matrix, dst_norm.shape)
result = cv2.resize(result,(scale_x * single_size, scale_y * single_size))
cv2.imshow("Perspective transformation", result)
cv2.waitKey(0)

dir_save = './result-' + image_path.split('/')[-1].split('.jpg')[0] + '/'
if not os.path.exists(dir_save):
    os.makedirs(dir_save)
for i in range(scale_x):
    for j in range(scale_y):
        img_temp = result[j * single_size : (j + 1) * single_size, i * single_size : (i + 1) * single_size, :]
        cv2.imwrite(dir_save + str(i) + '-' + str(j) + '.png', img_temp)
