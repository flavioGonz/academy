#!/usr/bin/env python3
"""Lección 18 · Capturas del caso real (enviadas por Nico), sin datos del cliente.
- ucm-fxo-interfaz-troncales.png (893x602): Interface Status con FXO1 y FXO2 ocupados y las dos troncales Busy.
  Se reemplazan Antel_22008180 por Antel_Linea1 y Antel_22045594 por Antel_Linea2 (Lato, alineación izquierda).
- ucm-fxo-active-calls.png (984x563): dos llamadas activas. Se reemplazan los nombres de troncal (centrados)
  y el nombre de la extensión "Cajas" por "Recepción" (centrado debajo de 100). Se recorta el pie con el menú.
Salida: site2/ilustraciones/grandstream/18-captura-troncales.webp y 18-captura-active-calls.webp,
        con vista previa PNG en ilustraciones/grandstream/."""
import sys
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from PIL import Image
from _captura import CAPT, reemplazar, guardar

im = Image.open(CAPT / "ucm-fxo-interfaz-troncales.png").convert("RGB")
print(reemplazar(im, (490, 258, 700, 282), "Antel_22008180", "Antel_Linea1", "left"))
print(reemplazar(im, (490, 290, 700, 314), "Antel_22045594", "Antel_Linea2", "left"))
im = im.crop((40, 112, 862, 540))     # Interface Status y Trunks, sin el gráfico de recursos
guardar(im, "18-captura-troncales")

im = Image.open(CAPT / "ucm-fxo-active-calls.png").convert("RGB")
print(reemplazar(im, (320, 272, 450, 292), "Antel_22045594", "Antel_Linea2", "center"))
print(reemplazar(im, (630, 254, 750, 274), "Antel_22008180", "Antel_Linea1", "center"))
print(reemplazar(im, (760, 274, 820, 292), "Cajas", "Recepción", "center"))
im = im.crop((0, 0, 984, 362))        # sin el menú de abajo ni el globo de ayuda
guardar(im, "18-captura-active-calls")
