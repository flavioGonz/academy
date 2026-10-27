#!/usr/bin/env python3
"""Lección 2 · Teoría · El calibrador lee, cambia lo suyo y devuelve.
Sale de teoria_md (Cómo funciona): lee el XML de la regla con GET /ISAPI/Smart/LineDetection/1 (o FieldDetection/1),
cambia solo la geometría, el sentido, la sensibilidad o el objetivo y lo devuelve con PUT; así no pisa otros campos.
En canales de un NVR Dahua, la misma pantalla escribe la regla IVS en el NVR."""
from _anim_omni import new, out, when, travel, seq, box, check

a = new(20, "LA REGLA", "El calibrador no inventa: lee, cambia lo suyo y devuelve")
a.steps([
    "GET: la cámara devuelve el XML completo de la regla.",
    "El calibrador cambia solo geometría, sentido, sensibilidad u objetivo.",
    "PUT del mismo XML: los demás campos vuelven a la cámara tal cual.",
], still=2)

a.add(box(48, 186, 270, 84, "Calibrador", "OmniAccess", "laptop"))
a.add(box(882, 186, 270, 84, "Cámara", "Hikvision", "camera"))

seq(a, "M326 214 H872", 2, 100, a.BLUE, "GET /ISAPI/Smart/LineDetection/1", 600, 204)
travel(a, (350, 214), (850, 214), 2, 12, dot=8)
seq(a, "M872 250 H326", 13, 100, a.CYAN, "XML de la regla", 600, 242)
travel(a, (850, 250), (350, 250), 13, 26, label="XML", bg=a.CYAN, hold=4)

# documento XML
DX, DY, DW = 330, 290, 540
ROWS = [("geometría", "puntos de la línea"), ("sentido", "A→B"), ("sensibilidad", "40"), ("objetivo", "Persona"),
        ("otros campos", "los que tenga la cámara")]
RH = 44
a.add(a.box(DX, DY, DW, 30 + RH * len(ROWS) + 10, a.WHITE, a.LINE, rx=12))
a.add(a.text(DX + 20, DY + 24, "regla de cruce de línea · XML", 15, a.GREY, a.MONO, 600))
for i, (k, v) in enumerate(ROWS):
    y = DY + 36 + i * RH
    mine = i < 4
    a.add(a.box(DX + 12, y, DW - 24, RH - 8, a.SLATE if mine else "#F3F6F9", rx=8))
    a.add(a.text(DX + 28, y + 24, k, 16, a.INK if mine else a.GREY, a.MONO, 600))
    if i != 2:
        a.add(a.text(DX + 230, y + 24, v, 16, a.TXT if mine else a.GREY, a.SANS, 600 if mine else 400))
# editables resaltados
when(a, f'<rect x="{DX + 8}" y="{DY + 32}" width="{DW - 16}" height="{RH * 4}" rx="10" fill="none" stroke="{a.BLUE}" stroke-width="3" stroke-dasharray="8 6"/>'
     + a.text(DX - 14, DY + 36 + RH * 2, "lo que", 15, a.BLUE, a.MONO, 600, "end")
     + a.text(DX - 14, DY + 56 + RH * 2, "toca", 15, a.BLUE, a.MONO, 600, "end"), 34, 66, still=0)
# sensibilidad 40 -> 60
ys = DY + 36 + 2 * RH + 24
a.add(a.group(a.text(DX + 230, ys, "40", 16, a.TXT, a.SANS, 600), a.keyframes([(0, 1), (42, 1), (43, 0), (99, 0), (100, 1)]), still=0))
a.add(a.group(a.text(DX + 230, ys, "60", 16, a.AMB, a.SANS, 600) + a.pill(DX + 280, ys - 20, "cambiado", a.AMB, a.AMBBG, 15, 28),
              a.keyframes([(0, 0), (42, 0), (43, 1), (99, 1), (100, 0)]), still=1))
# otros campos intactos
yo = DY + 36 + 4 * RH
when(a, check(a, DX + DW - 40, yo + 18), 70, 100, still=1)
when(a, a.text(DX + DW + 20, yo + 14, "no se", 16, a.OK, a.MONO, 600)
     + a.text(DX + DW + 20, yo + 36, "pisan", 16, a.OK, a.MONO, 600), 70, 100, still=1)

# PUT
seq(a, f"M183 278 V{DY + 290} H1017 V280", 67, 100, a.BLUE, "PUT del mismo XML", 600, DY + 280, still=1)
travel(a, (200, DY + 290), (1000, DY + 290), 67, 80, label="XML", bg=a.BLUE, hold=3)

a.add(a.text(48, 646, "Con un NVR Dahua, la misma pantalla escribe la regla IVS en el NVR. Para la zona: GET y PUT de FieldDetection/1.", 16, a.TXT, a.SANS, 600))

out(a, 2, 2, "Leer, cambiar y devolver la regla",
    "Animación en tres tiempos entre el calibrador de OmniAccess, a la izquierda, y la cámara Hikvision, a la derecha. "
    "Tiempo 1: el calibrador pide GET /ISAPI/Smart/LineDetection/1 y la cámara devuelve el XML completo de la regla, que aparece en el centro con cinco filas: geometría, sentido, sensibilidad, objetivo y otros campos de la cámara. "
    "Tiempo 2: se resaltan las cuatro filas que el calibrador toca y la sensibilidad cambia de 40 a 60. "
    "Tiempo 3: el calibrador manda PUT del mismo XML; los otros campos vuelven a la cámara igual, con un tilde verde: no se pisan. "
    "Al pie: con un NVR Dahua, la misma pantalla escribe la regla IVS en el NVR; para la zona se usa FieldDetection/1.",
    [10, 50, 85])
