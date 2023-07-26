import cv2
import numpy as np


fondo = cv2.imread('hoja.png',cv2.IMREAD_GRAYSCALE)
testImg = cv2.imread('perspective.jpg',cv2.IMREAD_GRAYSCALE)
mask = np.zeros((fondo.shape[1],fondo.shape[0]),np.uint8)
ref_point = []
c_ord = []
result = None


def computeL2Media(ref_point):
    # funcion que recibe las coordenadas seleccionadas en la función original,
    # determina el largo y ancho del paralelogramo que resulta de ellas para luego determinar la relación de aspecto
    width_AD = np.sqrt(((ref_point[0][0]-ref_point[1][0])**2)+((ref_point[0][1]-ref_point[1][1])**2))
    width_BC = np.sqrt(((ref_point[2][0]-ref_point[3][0])**2)+((ref_point[2][1]-ref_point[3][1])**2))
    maxWidth = max(int(width_AD), int(width_BC))

    height_AB = np.sqrt(((ref_point[0][0]-ref_point[3][0])**2)+((ref_point[0][1]-ref_point[3][1])**2))
    height_CD = np.sqrt(((ref_point[1][0]-ref_point[2][0])**2)+((ref_point[1][1]-ref_point[2][1])**2))
    maxHeight = max(int(height_AB), int(height_CD))

    dimensions = (maxWidth, maxHeight)
    #dimensions = (maxHeight,maxWidth)
    return dimensions

def ordena(coordenadas):
    # Copiar la lista original para evitar modificarla
    c_ordenado_x = []
    c_ordenado_y = []
    c_ordenado = coordenadas.copy()
    c_ord = [[0,0]]*len(coordenadas)
     
    c_ordenado.sort(key=lambda punto: punto[0])
    c_ordenado_x = c_ordenado.copy()
    x_c = sum(punto[0] for punto in c_ordenado) // len(c_ordenado)

    c_ordenado.sort(key=lambda punto: punto[1])
    c_ordenado_y = c_ordenado.copy()
    y_c = sum(punto[1] for punto in c_ordenado) // len(c_ordenado)
        
    for i in range(len(c_ordenado)):
        if(c_ordenado[i][0] < x_c and c_ordenado[i][1] < y_c):   #0,0
            c_ord[0]=c_ordenado[i]
        if(c_ordenado[i][0] > x_c and c_ordenado[i][1] < y_c):   #8,1
            c_ord[1]=c_ordenado[i]
        if(c_ordenado[i][0] > x_c and c_ordenado[i][1] > y_c):   #7,10
            c_ord[2]=c_ordenado[i]
        if(c_ordenado[i][0] < x_c and c_ordenado[i][1] > y_c):   #1,8
            c_ord[3]=c_ordenado[i]

    return c_ord    

def draw_dots(event,x,y,flags,param):
    global ref_point,c_ord,fondo,testImg,mask,result,trImg
    
    angle = 270

    trImg_w_borders = np.zeros((fondo.shape[1],fondo.shape[0]),np.uint8)
    #ref_point = [[480, 26], [468, 520], [657, 475], [666, 117]]
    
    if event == cv2.EVENT_LBUTTONDOWN:  
        if len(ref_point)<4:
            ref_point.append([x,y])
            cv2.circle(testImg,ref_point[-1],3,(0,0,255),-1)
            cv2.imshow("image",testImg)
        if len(ref_point) == 4:
            c_ord=ordena(ref_point); 
            maxWidth, maxHeight = computeL2Media(c_ord)
            srcCoordinates = np.array(c_ord).astype(np.float32)
            dstCoordinates = np.array([[0, 0], [maxWidth -1,0], [maxWidth - 1, maxHeight - 1], [0, maxHeight-1]]).astype(np.float32)

            M = cv2.getPerspectiveTransform(srcCoordinates,dstCoordinates)
            trImg = cv2.warpPerspective(testImg,M,(maxWidth,maxHeight),flags=cv2.INTER_LINEAR)
            
            cv2.imshow("image",trImg)
            y_offset = (fondo.shape[0] - maxHeight) // 2
            x_offset = (fondo.shape[1] - maxWidth ) // 2    

            trImg_w_borders[y_offset:y_offset+maxHeight, x_offset:x_offset+maxWidth] = trImg

            mask = (trImg_w_borders > 0) * 1 
            result = (1 - mask) * fondo + (mask) * trImg_w_borders


cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_dots)

while True:
    cv2.imshow('image',testImg)
    if result is not None:
        result = cv2.convertScaleAbs(result)
        cv2.namedWindow('output')
        cv2.imshow('output',result)

    k = cv2.waitKey(1) & 0xFF

    if k == ord("q"):
        cv2.destroyAllWindows()
        break



'''
---------------------------------------------------->version anterior

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

------------------------------------------------->fin version anterior
'''
