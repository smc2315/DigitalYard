import cv2 as cv
import numpy as np
import imutils
import matplotlib.pyplot as plt



# cv2_image = cv.imread('C:/Users/yt/Desktop/20220908163000/DJI_20220908160357_0001_W.JPG', cv.IMREAD_COLOR)
# M = np.float32([[1, 0, 25],
#                 [0, 1, 50]])
# shifted = cv.warpAffine(cv2_image, M, (cv2_image.shape[1], cv2_image.shape[0]))
#cv2_image = cv.imread('C:/Users/yt/capstone/yolov5/data/images/zidane.jpg')
# def move_image(img,x1,y1,x2,y2,dir):
#     dx = [10,-10,0,0]
#     dy = [0,0,10,-10]
#     nx1 = x1+dx[dir]
#     nx2 = x2+dx[dir]
#     ny1 = y1+dy[dir]
#     ny2 = y2 + dy[dir]
#     move_area = img[y1:y2, x1:x2]
#     img[ny1:ny2, nx1:nx2] = move_area
#
#     if dir==0:
#         img[y1:y2,x1:nx1] = 0
#     elif dir ==1:
#         img[y1:y2, nx2:x2] = 0
#     elif dir == 2:
#         img[y1:ny1,x1:x2] = 0
#     else:
#         img[ny2:y2, x1:x2] = 0
#     # M = np.float32([[1, 0, 20],
#     #                 [0, 1, 0]])
#     # img = cv.warpAffine(img, M, (img.shape[1], img.shape[0]))
#     return img
def move_image(self,dir):
    dx = [10,-10,0,0]
    dy = [0,0,10,-10]
    nx1 = self.x1+dx[dir]
    nx2 = self.x2+dx[dir]
    ny1 = self.y1+dy[dir]
    ny2 = self.y2 + dy[dir]
    move_area = self.img[self.y1:self.y2, self.x1:self.x2]
    move_area_block = self.layerBlock[self.y1:self.y2, self.x1:self.x2]
    move_area_struct = self.layerStruct[self.y1:self.y2, self.x1:self.x2]
    move_area_road = self.layerRoad[self.y1:self.y2, self.x1:self.x2]

    self.img[ny1:ny2, nx1:nx2] = move_area
    self.layerBlock[ny1:ny2, nx1:nx2] = move_area_block
    self.layerStruct[ny1:ny2, nx1:nx2] = move_area_struct
    self.layerRoad[ny1:ny2, nx1:nx2] = move_area_road

    if dir==0:
        self.img[self.y1:self.y2,self.x1:nx1] = 0
        self.layerBlock[self.y1:self.y2, self.x1:nx1] = 0
        self.layerStruct[self.y1:self.y2, self.x1:nx1] = 0
        self.layerRoad[self.y1:self.y2, self.x1:nx1] = 0
    elif dir ==1:
        self.img[self.y1:self.y2, nx2:self.x2] = 0
        self.layerStruct[self.y1:self.y2, nx2:self.x2] = 0
        self.layerRoad[self.y1:self.y2, nx2:self.x2] = 0
        self.layerBlock[self.y1:self.y2, nx2:self.x2] = 0
    elif dir == 2:
        self.img[self.y1:ny1,self.x1:self.x2] = 0
        self.layerRoad[self.y1:ny1, self.x1:self.x2] = 0
        self.layerBlock[self.y1:ny1, self.x1:self.x2] = 0
        self.layerStruct[self.y1:ny1, self.x1:self.x2] = 0

    else:
        self.img[ny2:self.y2, self.x1:self.x2] = 0
        self.layerBlock[ny2:self.y2, self.x1:self.x2] = 0
        self.layerStruct[ny2:self.y2, self.x1:self.x2] = 0
        self.layerRoad[ny2:self.y2, self.x1:self.x2] = 0



