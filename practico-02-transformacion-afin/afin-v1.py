import cv2 
import numpy as np

fondo = cv2.imread('hoja.png')
copiaFondo = fondo.copy()

icono = cv2.imread('r-hse1.jpg')
print(icono.shape)

rows, cols = icono.shape[:2]
bRows, bCols = fondo.shape[:2]

ref_point = []
dst = None  # Declarar dst como variable global
bn_dst = None


mask = np.zeros_like(icono, dtype=np.uint8)
final = None


def draw_dots(event, x, y, flags, param):
    global ref_point, dst, bn_dst,fondo,mask

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(ref_point) < 3:
            ref_point.append([x, y])
            print(ref_point)
            cv2.circle(fondo, ref_point[-1], 1, (0, 255, 255), 2)
            cv2.imshow("image", fondo)

        if len(ref_point) == 3:
            srcTri = np.array([[0, 0], [icono.shape[0], 0], [0, icono.shape[1]]]).astype(np.float32)
            dstTri = np.array([ref_point[2], ref_point[1], ref_point[0]]).astype(np.float32)
            transform_mat = cv2.getAffineTransform(srcTri, dstTri)
            dst = cv2.warpAffine(icono, transform_mat, (cols, rows))
            contours(dst,fondo)


def contours(transformedImage, background):
    global bn_dst, rows, cols,mask,rellenada, bCols, bRows, copiaFondo
    bn_dst = cv2.cvtColor(transformedImage, cv2.COLOR_BGR2GRAY)
    umbral = 100  # Ajusta el valor del umbral según tus necesidades
    _, imagen_binaria = cv2.threshold(bn_dst, umbral, 255, cv2.THRESH_BINARY)
    contornos, _ = cv2.findContours(imagen_binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contorno_maximo = max(contornos, key=cv2.contourArea)

    cv2.drawContours(transformedImage, [contorno_maximo], -1, (0, 0, 255), 1)
    cv2.drawContours(mask, [contorno_maximo], -1, (255,255,255),2)
    
    points = np.array([contorno_maximo])
    cv2.fillPoly(mask, [contorno_maximo], color = (255,255,255))
    rellenada = cv2.bitwise_and(dst,mask)
    
    maskRows = rows
    maskCols = cols
    coordinates = []
    aux = 0

# hago un barrido por toda la mascara para determinar cuales son las coordenadas en los que los puntos son blancos


    for x in range(maskRows):
        for y in range(maskCols):
            if mask[x, y][0] == 255 and mask[x, y][1]==255 and mask[x, y][2]==255 :
                coordinates.append((x,y))

    dump(coordinates)

    for x in range(bRows):
        for y in range(bCols):
            if (x,y) in coordinates:
                copiaFondo[x, y] = transformedImage[x, y].copy()
                aux = aux + 1

                
def dump(coordinates):
    archivo = open("archivo.txt", "w")
    
    for valor in coordinates:
        archivo.write(str(valor) + "\n")


    archivo.close()

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_dots)

while True:
    cv2.imshow('image', fondo)
    if bn_dst is not None:
        cv2.imshow('mask',mask)
        cv2.imshow('Resultado Final',copiaFondo)
    k = cv2.waitKey(1) & 0xFF

    if k == ord("q"):
        print("fondo: {}".format(fondo.shape))
        print("dst: {}".format(dst.shape))
        print("copiafondo: {}".format(copiaFondo.shape))
        cv2.imwrite('mask.jpg',mask)
        cv2.imwrite('dst.jpg',copiaFondo)
        break

cv2.destroyAllWindows()
