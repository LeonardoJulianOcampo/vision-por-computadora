#! /usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


fondo   = cv2.imread('hoja.png', cv2.IMREAD_GRAYSCALE)
testImg = cv2.imread('r-hse1.jpg', cv2.IMREAD_GRAYSCALE)

ref_point = []
mask = None


def draw_dots(event,x,y,flags,param):
    global ref_point,fondo,mask,result

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(ref_point)<3:
            ref_point.append([x,y])
            cv2.circle(fondo,ref_point[-1],3,(0,255,0),-1)
            cv2.imshow("Fondo",fondo)

        if len(ref_point)==3:

            srcTri = np.array([[0,       0], [testImg.shape[0], 0], [0, testImg.shape[1]]]).astype(np.float32)
            dstTri = np.array([ref_point[2],    ref_point[1]    ,        ref_point[0]]).astype(np.float32)

            M      = cv2.getAffineTransform(srcTri, dstTri)
            
            trImg  = cv2.warpAffine(testImg, M, (fondo.shape[1],fondo.shape[0]))

            mask   = (trImg > 0) * 1

            result = (1- mask) * fondo + (mask) * trImg


cv2.namedWindow('Fondo')
cv2.setMouseCallback('Fondo', draw_dots)


while True:
    cv2.imshow('Fondo',fondo)
    if mask is not None:
        result = cv2.convertScaleAbs(result)
        cv2.imshow('output',result)

    k = cv2.waitKey(1) & 0xFF

    if k == ord("q"):
        break;

cv2.destroyAllWindows();
