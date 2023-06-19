import cv2
import numpy as np
import math

img = cv2.imread('foto_prueba.jpg')
imgCopy = img.copy()
ref_point = []
l_ref_point = []
trTemplate = None
trTemplate2 = None
flag = 0
drawing = False


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


def calibrate():
    global ref_point, imgCopy, trTemplate, trImg, trTemplate2

    ref_point = [[608, 301], [241, 706], [651, 936], [968, 436]] 
    maxWidth, maxHeight = computeL2Media(ref_point)

    scrCoordinates = np.array(ref_point).astype(np.float32)
    dstCoordinates = np.array([[0, 0], [0, maxHeight - 1], [maxWidth - 1, maxHeight - 1], [maxWidth - 1, 0]]).astype(np.float32)

    M = cv2.getPerspectiveTransform(scrCoordinates, dstCoordinates)
    trImg = cv2.warpPerspective(img, M, (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)
    trTemplate = trImg.copy()
    trTemplate2 = trImg.copy()
    #cv2.imshow('imagen_claibrada', trTemplate)
    cv2.imwrite('imagenPerspectiva.jpg',trImg)


def draw_lines(event,x,y,flags,param):
    global lines_ref_point, drawing, ix, iy, trTemplate, trImg, trTemplate2

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
        l_ref_point.append((x,y))
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        l_ref_point.append((x,y))
        trTemplate2 = trImg.copy()
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            trImg = trTemplate2.copy()
            cv2.line(trImg,(ix,iy),(x,y),(0,255,0),2)
            dist = measure_distance((ix,iy),(x,y))
            print_distance(dist,(ix,iy),(x,y))


#Los argumentos son tuplas de la forma dotA = (x,y) dotB = (ix,iy)
def measure_distance(dotA,dotB):        
    distance = np.sqrt((dotA[0]-dotB[0])**2 + (dotA[1]-dotB[1])**2) 
    return distance


def pixels_to_mm(distance,angle_rads):

    x_pattern_in_mm = 50
    y_pattern_in_mm = 70

    x_pattern_in_px = 446
    y_pattern_in_px = 591

    x_dist_in_px = math.cos(angle_rads) * distance
    y_dist_in_px = math.sin(angle_rads) * distance
    
    x_dist_in_mm = (x_dist_in_px * x_pattern_in_mm) / x_pattern_in_px
    y_dist_in_mm = (y_dist_in_px * y_pattern_in_mm) / y_pattern_in_px
   
    h_dist_in_mm = np.sqrt(x_dist_in_mm ** 2 + y_dist_in_mm ** 2) 
    
    return round(h_dist_in_mm,2)
    


def print_distance(distance,dotA,dotB):

    global trImg
   
    center  = determine_position(dotA,dotB)[0] #La funcion devuelve el centro del segmento y su angulo
    angle   = determine_position(dotA,dotB)[1]
    text    = str(pixels_to_mm(distance,angle)) + ' mm'
    font    = cv2.FONT_HERSHEY_SIMPLEX
    scale   = 1
    color   = (255,0,0)
    width   = 2
    spacing = 2    
    

    cv2.putText(trImg, text, center ,font, scale, color, width, cv2.LINE_AA)





#funcion que determina el centro y angulo del segmento que mide una distancia marcada por el usuario

def determine_position(dotA, dotB): 
    dx = dotA[0] - dotB[0]
    dy = dotA[1] - dotB[1]
    center_x = (dotA[0] + dotB[0]) / 2
    center_y = (dotA[1] + dotB[1]) / 2
    angle_rad = math.atan2(dy,dx)
    angle_deg = math.degrees(angle_rad)
    return (int(center_x), int(center_y)), angle_rad

flag = 0

cv2.namedWindow('TP4')

while True:
    while flag == 0:
        cv2.imshow('TP4',imgCopy)
        
        k = cv2.waitKey(1) & 0xFF

        if k == ord("q"):
            cv2.destroyAllWindows()
            flag = 1
            break

        if k == ord("c"):
            calibrate()
            flag = 2
    
    if flag == 1:
        break

    if flag == 2:
        cv2.namedWindow('imagen_calibrada')
        cv2.setMouseCallback('imagen_calibrada', draw_lines)
        
        while True:
            cv2.imshow('imagen_calibrada',trImg)
            k = cv2.waitKey(1) & 0xFF
            
            if k == ord("q"):
                cv2.destroyAllWindows()
                flag = 1
                break

            if k == ord("r"):
                trImg = trTemplate
                trTemplate2 = trTemplate.copy()
                ref_point.clear()
                

