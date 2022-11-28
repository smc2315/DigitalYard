
# gps 좌표를 x,y 좌표로 변환
import math
#data = [{'x':0,'y':0,'lat':128.673729, 'lon':34.879354},{'x':6815/2,'y':0,'lat':128.693538, 'lon':34.873877},{'x':0,'y':int(7555/2),'lat':128.690564, 'lon':34.866509}]
data = [{'x':0,'y':0,'lat':128.690494, 'lon':34.870724},{'x':6815/2,'y':0,'lat':128.693538, 'lon':34.873877},{'x':0,'y':int(7555/2),'lat':128.690564, 'lon':34.866509}]

targetLon = 34.87
radiusOfEarth = 6371.009
circumferenceOfEarth = 2 * math.pi * radiusOfEarth
distancePerLat = circumferenceOfEarth / 360
distancePerLon = math.cos(targetLon * math.pi / 180) * circumferenceOfEarth / 360


def calcTheta(origin_x, origin_y, x, y, is_rad):
    a = y - origin_y
    b = x - origin_x

    theta = math.atan(a / b)

    if is_rad:
        return theta
    else:
        return theta * (180 / math.pi)


def convertUnitToLat(lonValue):
    return lonValue * distancePerLon / distancePerLat

def convertUnitToLon(LatValue):
    return LatValue * distancePerLat / distancePerLon

theta = calcTheta(convertUnitToLat(data[0]['lon']), data[0]['lat'], convertUnitToLat(data[1]['lon']), data[1]['lat'], True) * -1
theta = theta-0.01


def calcCoordinatesAfterRotation(origin_x, origin_y, x, y, theta, is_rad):
    rebased_x = x - origin_x
    rebased_y = y - origin_y

    rad_theta = 0

    if is_rad:
        rad_theta = theta
    else:
        rad_theta = theta * (math.pi / 180)

    rotatedX = (rebased_x * math.cos(rad_theta)) - (rebased_y * math.sin(rad_theta))
    rotatedY = (rebased_x * math.sin(rad_theta)) + (rebased_y * math.cos(rad_theta))

    xx = rotatedX + origin_x
    yy = rotatedY + origin_y

    return {'x': xx, 'y': yy}


tempCoordi = calcCoordinatesAfterRotation(convertUnitToLat(data[0]['lon']), data[0]['lat'], convertUnitToLat(data[1]['lon']), data[1]['lat'], theta, True)
tempCoordi['x'] = convertUnitToLon(tempCoordi['x'])
data[1]['lon_rotated'] = tempCoordi['x']
data[1]['lat_rotated'] = tempCoordi['y']

tempCoordi2 = calcCoordinatesAfterRotation(convertUnitToLat(data[0]['lon']), data[0]['lat'], convertUnitToLat(data[2]['lon']), data[2]['lat'], theta, True)
tempCoordi2['x'] = convertUnitToLon(tempCoordi2['x'])
data[2]['lon_rotated'] = tempCoordi2['x']
data[2]['lat_rotated']= tempCoordi2['y']


def makeLinearEquation(origin_x, origin_y, to_x, to_y):
    x_variation = to_x - origin_x
    y_variation = to_y - origin_y
    slope = y_variation / x_variation

    intercept = origin_y - (slope * origin_x)

    return {'slope': slope, 'intercept': intercept}


lonQuation=0
latQuation=0

lonQuation = makeLinearEquation(data[0]['lon'], data[0]['x'], data[1]['lon_rotated'], data[1]['x'])
latQuation = makeLinearEquation(data[0]['lat'], data[0]['y'], data[2]['lat_rotated'], data[2]['y'])



def calcScreenCoordinates(lat, lon):
    tempCoordi = calcCoordinatesAfterRotation(convertUnitToLat(data[0]['lon']), data[0]['lat'], convertUnitToLat(lon), lat, theta, True)
    tempCoordi['x'] = convertUnitToLon(tempCoordi['x'])

    x = lonQuation['slope'] * tempCoordi['x'] + lonQuation['intercept']
    y = latQuation['slope'] * tempCoordi['y'] + latQuation['intercept']
    return { 'x': x, 'y': y }


from PIL import Image
from PIL.ExifTags import TAGS

# 이미지 파일에서 gps정보 불러오기
def getGPS(path):
    image = Image.open(path)
    info = image._getexif()
    image.close()

    # 새로운 딕셔너리 생성

    taglabel = {}

    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        taglabel[decoded] = value

    exifGPS = taglabel['GPSInfo']

    latData = exifGPS[2]
    lonData = exifGPS[4]

    # 도, 분, 초 계산
    latDeg = latData[0]
    latMin = latData[1]
    latSec = latData[2]

    lonDeg = lonData[0]
    lonMin = lonData[1]
    lonSec = lonData[2]

    # 도, 분, 초로 나타내기
    Lat = str(int(latDeg)) + "°" + str(int(latMin)) + "'" + str(latSec) + "\"" + exifGPS[1]
    Lon = str(int(lonDeg)) + "°" + str(int(lonMin)) + "'" + str(lonSec) + "\"" + exifGPS[3]

    # 도 decimal로 나타내기
    # 위도 계산
    Lat = (latDeg + (latMin + latSec / 60.0) / 60.0)
    # 북위, 남위인지를 판단, 남위일 경우 -로 변경
    if exifGPS[1] == 'S': Lat = Lat * -1

    # 경도 계산
    Lon = (lonDeg + (lonMin + lonSec / 60.0) / 60.0)
    # 동경, 서경인지를 판단, 서경일 경우 -로 변경
    if exifGPS[3] == 'W': Lon = Lon * -1

    return Lat, Lon



import math
from math import pi
def LatLontoXY(lat_center,lon_center):
    C =(256/(2*pi) )

    x=C*(math.radians(lon_center)+pi)
    y=C*(pi-math.log(math.tan((pi/4) + math.radians(lat_center)/2)))
    degree=54
    newX = x*math.cos(degree/180*pi) - y*math.sin(degree/180*pi)
    newY = x*math.sin(degree/180*pi) + y*math.cos(degree/180*pi)
    x = (newX - 46.89980042107082) * 100 * 4927.78
    y = (newY - 237.2438511323537) * 100 * 4927.77

    return x,y

import os
import cv2
import numpy as np
from getLabel import getLabel

def setBackground(path,file_list):
    minX = 100000
    minY = 100000
    maxX = 0
    maxY = 0
    plusX = 0
    plusY = 0
    for img in file_list:
        imgPath = path + '/' + img
        lon,lat = getGPS(imgPath)
        gps = calcScreenCoordinates(lat,lon)
        x = gps['x']
        y = gps['y']

        if minX > x:
            minX = x
        if minY > y:
            minY = y
        if maxX < x:
            maxX = x
        if maxY < y:
            maxY = y

    plusX = plusX-minX+10000

    plusY = plusY - minY+10000
    return int((maxX+50000-minX)/4), int((maxY+20000 - minY)/4),int(plusX/4),int(plusY/4)

#이미지와 라벨들을 1/4 로 축소 후 이미지의 gps 좌표값을 기준으로 mapping
def stitchImage(path):
    file_list1 = os.listdir(path)
    file_list1.sort()
    lenX,lenY,plusX,plusY = setBackground(path,file_list1)
    lenY = lenY+1000-lenY%1000
    lenX = lenX+1000-lenX%1000


    # background = np.zeros((15000,30000,3),dtype = 'u1')
    # background2 = np.zeros((15000,30000),dtype = 'u1')
    # background = np.zeros((8000, 15000, 3), dtype='u1')
    # background2 = np.zeros((8000,15000), dtype='u1')

    background = np.zeros((lenY, lenX, 3), dtype='u1')
    background2 = np.zeros((lenY,lenX), dtype='u1')

    for img in file_list1:
        imgPath = path + '/' + img
        lon, lat = getGPS(imgPath)
        img = cv2.imread(imgPath)
        # img = cv2.resize(img, (2028, 1520))
        img = cv2.resize(img, (1014, 760))
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        label = getLabel(imgPath)[0].astype(np.dtype('uint8'))
        # label = cv2.resize(label,(2028,1520))
        label = cv2.resize(label, (1014, 760))
        label = cv2.rotate(label, cv2.ROTATE_90_CLOCKWISE)
        h=2028/2
        w= 1520/2
        gps = calcScreenCoordinates(lat, lon)
        x = gps['x']
        y = gps['y'] + 100

        x = x-(y-5200)*220/870*0.9
        y = y*1.1-x*0.05
        x=x/2
        y=y/2+500
        x = x+plusX
        y = y*0.575+plusY
        # background[int(y * 0.575 - h / 2):int(y * 0.575 + h / 2), int(x - w / 2):int(x + w / 2)] = img
        # background2[int(y * 0.575 - h / 2):int(y * 0.575 + h / 2), int(x - w / 2):int(x + w / 2)] = label
        background[int(y  - h / 2):int(y  + h / 2), int(x - w / 2):int(x + w / 2)] = img
        background2[int(y  - h / 2):int(y  + h / 2), int(x - w / 2):int(x + w / 2)] = label
    return background, background2

def stitchImage1(path):
    file_list1 = os.listdir(path)
    file_list1.sort()
    # background = np.zeros((15000,30000,3),dtype = 'u1')
    # background2 = np.zeros((15000,30000),dtype = 'u1')
    background = np.zeros((15000, 30000, 3), dtype='u1')
    background2 = np.zeros((15000,30000), dtype='u1')

    for img in file_list1:
        imgPath = path + '/' + img
        lon, lat = getGPS(imgPath)
        print(lat,lon)
        img = cv2.imread(imgPath)
        # img = cv2.resize(img, (2028, 1520))
        img = cv2.resize(img, (1014, 760))
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        label = getLabel(imgPath)[0].astype(np.dtype('uint8'))
        # label = cv2.resize(label,(2028,1520))
        label = cv2.resize(label, (1014, 760))
        label = cv2.rotate(label, cv2.ROTATE_90_CLOCKWISE)
        h=2028/2
        w= 1520/2
        x,y= LatLontoXY(lon,lat)
        print(x,y)

        background[int(y*0.575-h/2):int(y*0.575+h/2), int(x-w/2):int(x+w/2)] = img
        background2[int(y*0.575-h/2):int(y*0.575+h/2), int(x-w/2):int(x+w/2)] = label
    return background, background2


