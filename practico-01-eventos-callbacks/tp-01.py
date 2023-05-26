#!/usr/bin/env python
#-*-coding: utf-8-*-

import cv2 
import numpy as np

img = cv2.imread('hoja.png',cv2.IMREAD_GRAYSCALE)
buf = img.copy()

ref_point = []
crop = False
drawing = False
ix,iy = -1,-1



def draw_circle(event, x, y, flags, param):
    global ref_point, drawing, ix, iy, img, buf

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
        ref_point.append((x,y))
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        ref_point.append((x,y))    
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            img = buf.copy()
            cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),2)
            rect = (min(ix,x),min(iy,y),abs(ix-x),abs(iy-y))



cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)



while(1):   
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    
    if k == ord("g"):
        crop_img = buf[ref_point[0][1]:ref_point[1][1],ref_point[0][0]:ref_point[1][0]]
        cv2.imwrite('seleccion.png',crop_img)
        cv2.imshow("imagen recortada", crop_img)
        cv2.waitKey(0)
    elif k == ord("r"):
        img = buf.copy()
    elif k == ord("q"):
        break


cv2.destroyAllWindows()


