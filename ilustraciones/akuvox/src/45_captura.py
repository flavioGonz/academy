#!/usr/bin/env python3
"""Lección 45 · Captura de Intercom > Basic del E16C V2.0 (enviada por Nico) con el campo Number reemplazado.
La captura original tiene IP reales de una obra: se tapa el texto del campo Number y se escribe
192.168.88.65,192.168.88.64 con la misma alineación (centrado en el campo) y un gris parecido.
Entrada: ilustraciones/akuvox/capturas/e16c-intercom-basic.png (1900x923)
Salida:  site2/ilustraciones/akuvox/45-captura-basic.webp (ancho 1600) y una vista previa PNG en ilustraciones/akuvox/."""
from PIL import Image, ImageDraw, ImageFont

SRC = "/home/claude/ies-training/ilustraciones/akuvox/capturas/e16c-intercom-basic.png"
OUT = "/home/claude/ies-training/site2/ilustraciones/akuvox/45-captura-basic.webp"
PREV = "/home/claude/ies-training/ilustraciones/akuvox/45-captura-basic.png"
FONT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"  # métrica de Times New Roman, como la web del equipo
NEW = "192.168.88.65,192.168.88.64"
OLD_W = 1314 - 1146 + 1          # ancho medido del texto original
FIELD = (1043, 445, 1417, 471)   # interior blanco del campo Number (sin el borde)
CY = 458                         # centro vertical del texto original (452 a 464)
GRAY = (95, 95, 95)              # gris principal del texto de la captura

im = Image.open(SRC).convert("RGB")
W, H = im.size
d = ImageDraw.Draw(im)
d.rectangle(FIELD, fill=(255, 255, 255))
# tamaño que reproduce el ancho por carácter del original (25 caracteres, el nuevo tiene 27)
size = 16
for s in range(12, 22):
    f = ImageFont.truetype(FONT, s)
    if f.getlength("172.20.30.65,172.20.30.64") <= OLD_W + 2:
        size = s
f = ImageFont.truetype(FONT, size)
cx = (1040 + 1420) / 2
d.text((cx, CY), NEW, font=f, fill=GRAY, anchor="mm")
im.save(PREV)
im.resize((1600, round(H * 1600 / W)), Image.LANCZOS).save(OUT, "WEBP", quality=88, method=6)
print("ok", OUT, "tamaño de letra", size)
