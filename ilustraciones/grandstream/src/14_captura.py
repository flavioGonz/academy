#!/usr/bin/env python3
"""Lección 14 · Captura del Dashboard de un UCM6304A (enviada por Nico), recortada a Interface Status y Trunks.
La original muestra el número real de la línea en el nombre de la troncal: se reemplaza Antel_22008180 por
Antel_Linea1 con la misma fuente (Lato), alineación izquierda, altura y color. El recorte deja afuera el usuario,
el plan de RemoteConnect y el resto de los paneles.
Entrada: ilustraciones/grandstream/capturas/ucm-dashboard.png (1600x792)
Salida:  site2/ilustraciones/grandstream/14-captura-dashboard.webp y vista previa PNG en ilustraciones/grandstream/."""
import sys
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from PIL import Image
from _captura import CAPT, reemplazar, guardar

im = Image.open(CAPT / "ucm-dashboard.png").convert("RGB")
print(reemplazar(im, (905, 448, 1100, 472), "Antel_22008180", "Antel_Linea1", "left", umbral=200))
im = im.crop((545, 336, 1232, 690))   # paneles Interface Status y Trunks
guardar(im, "14-captura-dashboard")
