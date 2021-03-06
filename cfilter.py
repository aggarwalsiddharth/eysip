import cv2
import imutils
import numpy as np

kernel = np.ones((5,5), np.uint8)
image = cv2.imread("test2.jpg")
resized = imutils.resize(image, width=600)
ratio = image.shape[0] / float(resized.shape[0])
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.bilateralFilter(gray, 11, 17, 17)
# blurred = cv2.erode(blurred, kernel, iterations=1)
# blurred = cv2.GaussianBlur(gray, (5, 5), 0)
blurredopen = cv2.morphologyEx(blurred, cv2.MORPH_OPEN, kernel)
blurredclose = cv2.morphologyEx(blurred, cv2.MORPH_CLOSE, kernel)
ret,thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_OTSU)
edged = cv2.Canny(blurredclose, 30, 200)

cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
cntsSorted = sorted(cnts, key=lambda x: cv2.contourArea(x) ,reverse=True)
for c in cntsSorted:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.01 * peri, True)

    # if our approximated contour has four points, then
    # we can assume that we have found our screen
    if len(approx) == 4:
        screenCnt = approx
        break
print(screenCnt)
cv2.drawContours(resized, [screenCnt], -1, (0, 255, 0), 3)
cv2.imshow('frame', resized)
cv2.imshow('frame1', blurred)
cv2.imshow('frame2', edged)
cv2.imshow('frame3', thresh)
cv2.imshow('frame4', blurredopen)
cv2.imshow('frame5', blurredclose)
cv2.waitKey(0)
cv2.destroyAllWindows()