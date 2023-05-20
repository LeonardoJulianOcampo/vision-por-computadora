import cv2
import numpy as np


fondo = cv2.imread('hoja.png',cv2.IMREAD_GRAYSCALE)
testImg = cv2.imread('hse1.jpg',cv2.IMREAD_GRAYSCALE)


ref_point = []
mask = None

def draw_dots(event,x,y,flags,param):
    global ref_point,fondo,testImg,mask,result

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(ref_point)<4:
            ref_point.append([x,y])
            cv2.circle(fondo,ref_point[-1],3,(0,0,255),-1)
            cv2.imshow("image",fondo)
        if len(ref_point) == 4:
            scrCoordinates = np.array([[0,0],[testImg.shape[1],0],[testImg.shape[1],testImg.shape[0]],[0,testImg.shape[0]]]).astype(np.float32)

            dstCoordinates = np.array([ref_point[0],ref_point[1],ref_point[2],ref_point[3]]).astype(np.float32)
            M = cv2.getPerspectiveTransform(scrCoordinates,dstCoordinates)
            trImg = cv2.warpPerspective(testImg,M,(fondo.shape[1],fondo.shape[0]))
            mask = (trImg > 0) * 1 
            result = (1 - mask) * fondo + (mask) * trImg

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_dots)

while True:
    cv2.imshow('image',fondo)
    if mask is not None:
        result = cv2.convertScaleAbs(result)
        cv2.imshow('output',result)

    k = cv2.waitKey(1) & 0xFF

    if k == ord("q"):
        break;

cv2.destroyAllWindows()
