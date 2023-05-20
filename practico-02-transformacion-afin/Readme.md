# Práctico 02: Transformación Afín:

## afin-v1.py

Este programa carga una imagen predeterminada ("hoja.png") y la muestra en una ventana. Luego permite al usuario la selección de tres puntos pertenecientes a la misma.
Esos tres puntos serán utilizados para determinar una transformación afín a una segunda imagen predeterminada ("r-hse1.jpg").

Dicha transformación será finalmente incrustada en el área demarcada por los tres puntos iniciales de la primera ventana.

Al no usar la biblioteca `numpy` el rendimiento del algoritmo es muy pobre. Requiere al menos dos o tres minutos para terminar el proceso.

## afin-v2.py

Este programa realiza el mismo proceso que el anterior pero emplea un algoritmo mejorado basándose en arreglos del tipo `numpy` logrando un rendimiento superior.
