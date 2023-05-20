import cv2
import numpy as np

img = cv2.imread('foto-prueba5.jpg')
imgCopy = img.copy()
ref_point = []
trTemplate = None
flag = 1

def computeL2Media(ref_point):
    # funcion que recibe las coordenadas seleccionadas en la función original,
    # determina el largo y ancho del cuadrilatero que resulta de ellas para luego determinar la relación de aspecto
    width_AD = np.sqrt(((ref_point[0][0]-ref_point[3][0])**2)+((ref_point[0][1]-ref_point[3][1])**2))
    width_BC = np.sqrt(((ref_point[1][0]-ref_point[2][0])**2)+((ref_point[1][1]-ref_point[2][1])**2))
    maxWidth = max(int(width_AD), int(width_BC))

    height_AB = np.sqrt(((ref_point[0][0]-ref_point[1][0])**2)+((ref_point[0][1]-ref_point[1][1])**2))
    height_CD = np.sqrt(((ref_point[2][0]-ref_point[3][0])**2)+((ref_point[2][1]-ref_point[3][1])**2))
    maxHeight = max(int(height_AB), int(height_CD))

    dimensions = (maxWidth, maxHeight)
    return dimensions


def draw_dots(event, x, y, flags, param):
    global ref_point, imgCopy, trTemplate, trImg

    if event == cv2.EVENT_LBUTTONDOWN:

        if len(ref_point) < 4:
            ref_point.append([x, y])
            cv2.circle(imgCopy, ref_point[-1], 4, (0, 255, 0), -1)
        if len(ref_point) == 4:
            maxWidth, maxHeight = computeL2Media(ref_point)

            scrCoordinates = np.array(ref_point).astype(np.float32)
            dstCoordinates = np.array([[0, 0], [0, maxHeight - 1], [maxWidth - 1, maxHeight - 1], [maxWidth - 1, 0]]).astype(np.float32)

            M = cv2.getPerspectiveTransform(scrCoordinates, dstCoordinates)
            trImg = cv2.warpPerspective(img, M, (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)
            trTemplate = trImg.copy()
            cv2.imshow('Calibrada para medición', trTemplate)
            cv2.imwrite('imagenPerspectiva.jpg',trImg)

def reset_image(event, x, y, flags, param):
    global ref_point, imgCopy, trTemplate

    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = []
        imgCopy = img.copy()
        trTemplate = None
        cv2.imshow('Calibrada para medición', imgCopy)

def distances(event, x, y, flags, param):
    pass

#cv2.namedWindow('TP4: Medición de objetos')
#cv2.setMouseCallback('TP4: Medición de objetos', draw_dots)

while True:
    
    if flag == 1:
        cv2.namedWindow('TP4: Medición de objetos')
        cv2.setMouseCallback('TP4: Medición de objetos', draw_dots)
        cv2.imshow('TP4: Medición de objetos', imgCopy)
        flag = 0
    
    if flag == 2:
        cv2.namedWindow('Imagen calibrada para medición')
        cv2.setMouseCallback('Imagen calibrada para medición', distances)
        cv2.imshow('Imagen calibrada para medición', trTemplate)
        flag = 0

    k = cv2.waitKey(1) & 0xFF

    if k == ord('q'):
        break
    elif k == ord('r'):
        cv2.destroyAllWindows() 
        imgCopy = img.copy()
        flag = 1
    if trTemplate is not None:
        cv2.destroyAllWindows()
        flag = 2


cv2.destroyAllWindows()
