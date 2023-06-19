import cv2
import numpy as np


fondo = cv2.imread('hoja.png',cv2.IMREAD_GRAYSCALE)
testImg = cv2.imread('perspective.jpg',cv2.IMREAD_GRAYSCALE)
mask = np.zeros((fondo.shape[1],fondo.shape[0]),np.uint8)

def computeL2Media(ref_point):
    # funcion que recibe las coordenadas seleccionadas en la función original,
    # determina el largo y ancho del paralelogramo que resulta de ellas para luego determinar la relación de aspecto
    width_AD = np.sqrt(((ref_point[0][0]-ref_point[3][0])**2)+((ref_point[0][1]-ref_point[3][1])**2))
    width_BC = np.sqrt(((ref_point[1][0]-ref_point[2][0])**2)+((ref_point[1][1]-ref_point[2][1])**2))
    maxWidth = max(int(width_AD), int(width_BC))

    height_AB = np.sqrt(((ref_point[0][0]-ref_point[1][0])**2)+((ref_point[0][1]-ref_point[1][1])**2))
    height_CD = np.sqrt(((ref_point[2][0]-ref_point[3][0])**2)+((ref_point[2][1]-ref_point[3][1])**2))
    maxHeight = max(int(height_AB), int(height_CD))

    dimensions = (maxWidth, maxHeight)
    return dimensions


ref_point = []
result = None

def draw_dots():
    global ref_point,fondo,testImg,mask,result
   
    trImg_w_borders = np.zeros((fondo.shape[1],fondo.shape[0]),np.uint8)
    ref_point = [[480, 26], [468, 520], [657, 475], [666, 117]]

    maxWidth, maxHeight = computeL2Media(ref_point)
    
    srcCoordinates = np.array(ref_point).astype(np.float32)
    dstCoordinates = np.array([[0, 0], [0, maxHeight - 1], [maxWidth - 1, maxHeight - 1], [maxWidth - 1, 0]]).astype(np.float32)

    M = cv2.getPerspectiveTransform(srcCoordinates,dstCoordinates)
    trImg = cv2.warpPerspective(testImg,M,(maxWidth,maxHeight),flags=cv2.INTER_LINEAR)

    y_offset = (fondo.shape[1] - maxHeight) // 2
    x_offset = (fondo.shape[0] - maxWidth ) // 2    

    trImg_w_borders[y_offset:y_offset+maxHeight, x_offset:x_offset+maxWidth] = trImg

    mask = (trImg_w_borders > 0) * 1 
    result = (1 - mask) * fondo + (mask) * trImg_w_borders

cv2.namedWindow('image')
cv2.namedWindow('output')

while True:
    cv2.imshow('image',testImg)
    draw_dots()
    if result is not None:
        result = cv2.convertScaleAbs(result)
        cv2.imshow('output',result)

    k = cv2.waitKey(1) & 0xFF

    if k == ord("q"):
        cv2.destroyAllWindows()
        break
