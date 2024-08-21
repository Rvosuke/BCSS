import cv2
import numpy as np


image=cv2.imread('./img/105.jpg')
# print(image.shape)
h = int(1000 * image.shape[1] / image.shape[0])

image = cv2.resize(image, (600, h))
# image = cv2.resize(image, (273,364))


#设定颜色HSV范围，假定为红色
# redLower = np.array([100, 20, 25])
# redUpper = np.array([200, 150, 150])
#
# # hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#
# #去除颜色范围外的其余颜色
# mask = cv2.inRange(image, redLower, redUpper)

# 转成灰度图片
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY);
# 二值化操作
ret, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)


# dst = cv2.cornerHarris(src=binary, blockSize=4, ksize=5, k=0.04)
# # 变量a的阈值为0.01 * dst.max()，如果dst的图像值大于阈值，那么该图像的像素点设为True，否则为False
# # 将图片每个像素点根据变量a的True和False进行赋值处理，赋值处理是将图像角点勾画出来
# a = dst>0.01 * dst.max()
# binary[a] = [0, 0, 255]
# cv2.imshow('corners_', binary)
# cv2.waitKey(0)           # 按Esc查看下一张


dst=cv2.cornerHarris(binary,4,5,0.06)#调用函数cornerHarris
print(dst.shape)

dst_norm=np.empty(dst.shape,dtype=np.float32)
print(dst_norm.shape)


cv2.normalize(dst,dst_norm,alpha=0,beta=255,norm_type=cv2.NORM_MINMAX)#归一化

print(dst_norm)

for i in range(dst_norm.shape[0]):
    for j in range(dst_norm.shape[1]):
        if int(dst_norm[i,j])>120:
            cv2.circle(image,(j,i),2,(0,255,0),2)

cv2.imshow('image', image)

cv2.waitKey(0)