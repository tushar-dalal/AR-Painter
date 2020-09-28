import cv2
import numpy as np


def empty(a):
    pass


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 0)

myColours = [[[0, 118, 138], [29, 232, 255]],
             [[56, 39, 90], [88, 155, 125]]]

mycolourvals = [[20, 150, 240],
                [50, 40, 100]]

myPoints = []


def findColor(image, colours):
    imgHSV2 = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    cnt = 0
    for colour in colours:
        low = np.array(colour[0])
        up = np.array(colour[1])
        mask2 = cv2.inRange(imgHSV2, low, up)
        cv2.imshow("mask" + str(colour[0]), mask2)
        x, y = getContours(mask2)
        cv2.circle(imgResult, (x, y), 6, mycolourvals[cnt], cv2.FILLED)
        myPoints.append((x, y, mycolourvals[cnt]))
        cnt = cnt + 1


def getContours(imga):
    contours, hierarchy = cv2.findContours(imga, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            cv2.drawContours(imgResult, cnt, -1, (114, 85, 156), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.03 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y


def setColor(low, up):
    myColours.append([low, up])


def plotPoints(myPts):
    for x, y, ID in myPts:
        cv2.circle(imgResult, (x, y), 10, ID, cv2.FILLED)


# un-quote the following quote if ColourPicker.py doesnt work and use this section only
# press s to save a new colour to the list and k to exit selection mode and move to the painting section
'''
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 480)
cv2.createTrackbar("Hue min", "HSV", 0, 179, empty)
cv2.createTrackbar("Hue max", "HSV", 179, 179, empty)
cv2.createTrackbar("Sat min", "HSV", 0, 179, empty)
cv2.createTrackbar("Sat max", "HSV", 255, 255, empty)
cv2.createTrackbar("Val min", "HSV", 0, 255, empty)
cv2.createTrackbar("Val max", "HSV", 255, 255, empty)

while True:
    print(len(myColours))
    success, img = cap.read()
    h_min = cv2.getTrackbarPos("Hue min", "HSV")
    h_max = cv2.getTrackbarPos("Hue max", "HSV")
    s_min = cv2.getTrackbarPos("Sat min", "HSV")
    s_max = cv2.getTrackbarPos("Sat max", "HSV")
    v_min = cv2.getTrackbarPos("Val min", "HSV")
    v_max = cv2.getTrackbarPos("Val max", "HSV")
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, lower, upper)
    imgMasked = cv2.bitwise_and(img, img, mask=mask)
    imgResult = stackImages(0.6, [img, mask, imgMasked])
    cv2.imshow("WebCam", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        setColor(lower, upper)
    if cv2.waitKey(1) & 0xFF == ord('k'):
        break

cv2.destroyWindow("HSV")
'''

while True:
    success, img = cap.read()
    imgResult = img.copy()
    findColor(img, myColours)
    plotPoints(myPoints)
    cv2.imshow("WebCam", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
