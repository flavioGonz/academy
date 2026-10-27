#!/usr/bin/env python3
"""Teoría lección 2 (Host dedicado): la configuración vive en el volumen; el contenedor se borra y se recrea
sin perder nada; las variables ya guardadas en la base mandan (WEB_CONFIG_OVERRIDE=true).
Salida: site2/ilustraciones/omada/2-t1.svg"""
import sys
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _anim_omada import *  # noqa

a = nueva(22, "DOCKER", "El contenedor se cambia; el volumen se queda")
F = a.steps([
    "El contenedor corre: todo lo que configurás se escribe en el volumen.",
    "Se borra el contenedor, por ejemplo para cambiar de imagen. El volumen queda.",
    "Contenedor nuevo, mismo volumen: tarda 1 a 2 minutos y vuelve todo.",
    "Lo guardado en la base manda: para cambiar puertos, WEB_CONFIG_OVERRIDE=true.",
], still=2)

# --- VM
a.add(a.box(48, 180, 640, 416, "none", a.GREY, rx=18, sw=2, extra='stroke-dasharray="7 7"'))
a.add(chip(a, 70, 166, "VM Linux · Docker", a.GREY, a.WHITE, stroke=a.LINE))

# ranura del contenedor
SX, SY, SW, SH = 96, 226, 420, 104
a.add(a.box(SX, SY, SW, SH, "none", a.LINE, rx=14, sw=2, extra='stroke-dasharray="5 6"'))
viejo = nodo(a, SX, SY, SW, SH, "omada-controller", "contenedor · Java + MongoDB", tsize=21, ssize=15)
fase(a, viejo, F, 0, 0)
# fase 2: el viejo se va
fase(a, a.box(SX, SY, SW, SH, a.SLATE, a.BAD, rx=14, sw=2, extra='stroke-dasharray="6 5"')
     + a.text(SX + SW / 2, SY + 46, "contenedor borrado", 20, a.BAD, a.HEAD, 600, "middle")
     + a.text(SX + SW / 2, SY + 74, "docker compose pull · up -d", 15, a.GREY, a.MONO, 400, "middle"), F, 1)
# fase 3 y 4: el nuevo
nuevo = nodo(a, SX, SY, SW, SH, "omada-controller", "contenedor nuevo, mismo volumen", tsize=21, ssize=15)
fase(a, nuevo, F, 2, 3, still=1)

# volumen (cilindro)
VX, VY, VW, VH = 96, 430, 420, 130
cil = (f'<path d="M{VX} {VY + 18} V{VY + VH - 18} A{VW / 2} 18 0 0 0 {VX + VW} {VY + VH - 18} V{VY + 18}" fill="{a.OKBG}" stroke="{a.OK}" stroke-width="2"/>'
       f'<ellipse cx="{VX + VW / 2}" cy="{VY + 18}" rx="{VW / 2}" ry="18" fill="#F2FBF6" stroke="{a.OK}" stroke-width="2"/>')
a.add(cil)
a.add(a.text(VX + 24, VY + 66, "volumen omada-data", 20, a.INK, a.HEAD, 600))
a.add(a.text(VX + 24, VY + 94, "/opt/tplink/EAPController/data", 15, a.TXT, a.MONO))

# montaje
a.add(linea(a, SX + SW / 2, SY + SH, SX + SW / 2, VY, a.OK, 3, "6 6"))
a.add(a.text(SX + SW / 2 - 16, (SY + SH + VY) / 2 + 5, "montado", 15, a.OK, a.MONO, 400, "end"))
fase(a, bad(a, SX + SW / 2, (SY + SH + VY) / 2, 13), F, 1)

# fase 1: escrituras hacia el volumen
for k, lab in enumerate(["sitio", "SSID", "equipos"]):
    t0 = F[0][0] + 4 + k * 6
    viaje(a, paquete(a, lab, a.BLUE), [SX + 300, SX + 300, SX + 300][k], SY + SH + 18, [SX + 300, SX + 300, SX + 300][k], VY + 30, t0, t0 + 5, hold=1)

# --- columna derecha: qué guarda el volumen
RX, RW = 730, 422
a.add(a.box(RX, 196, RW, 200, a.WHITE, a.LINE))
a.add(a.text(RX + 22, 230, "En el volumen", 19, a.INK, a.HEAD, 600))
for i, s in enumerate(["sitios, redes y SSID", "equipos adoptados", "cuentas y ajustes", "la base de MongoDB"]):
    a.add(f'<circle cx="{RX + 30}" cy="{263 + i * 33}" r="4" fill="{a.OK}"/>')
    a.add(a.text(RX + 44, 268 + i * 33, s, 17, a.TXT, a.SANS))
fase(a, chip(a, RX + RW - 18, 210, "intacto", a.OK, a.OKBG, anchor="end"), F, 1, 3, still=1)

# fase 3: arranque
arr = (a.box(RX, 420, RW, 150, a.WHITE, a.LINE)
       + a.text(RX + 22, 454, "Arranque del contenedor nuevo", 18, a.INK, a.HEAD, 600)
       + a.box(RX + 22, 474, RW - 44, 18, a.SLATE, rx=9)
       + a.text(RX + 22, 524, "1 a 2 minutos · unos 1,9 GB de RAM", 16, a.TXT, a.MONO)
       + a.text(RX + 22, 552, "Reiniciarlo por impaciencia solo lo demora.", 16, a.AMB, a.SANS, 600))
fase(a, arr, F, 2, still=1)
bar = a.keyframes([(0, "0"), (F[2][0], "0"), (F[2][0] + 18, "1"), (100, "1")], "transform", "scaleX({})")
a.add(a.group(a.box(RX + 22, 474, RW - 44, 18, a.OK, rx=9), bar, a.show(F[2][0], F[2][1], 0.6), still=1,
              origin=f"{RX + 22}px 483px"))

# fase 4: variables guardadas
env = (a.box(RX, 420, RW, 150, a.INK, rx=14)
       + a.text(RX + 22, 452, "docker-compose.yml · environment", 15, DARK_SUB, a.MONO)
       + a.text(RX + 22, 484, "puerto nuevo → se ignora", 16, "#FFB4A3", a.MONO, 600)
       + a.text(RX + 22, 510, "manda lo guardado en la base", 15, DARK_SUB, a.MONO)
       + a.text(RX + 22, 548, "+ WEB_CONFIG_OVERRIDE=true → se aplica", 16, "#5BE0A5", a.MONO, 600))
fase(a, env, F, 3)

pie(a, F, [
    "El contenedor es el programa; la configuración está afuera, en el volumen.",
    "Borrar el contenedor no toca el volumen.",
    "Mientras el volumen exista, el contenedor se puede borrar y recrear sin perder nada.",
    "Después del primer arranque, muchas variables quedan guardadas en la base.",
], y=645, still=2, colores=[a.INK, a.INK, a.OK, a.AMB])

salida(a, 2, 1, "El contenedor se cambia; el volumen se queda",
       "Animación en cuatro tiempos dentro de una VM Linux con Docker. 1: el contenedor omada-controller corre y escribe sitio, SSID y "
       "equipos en el volumen omada-data, montado en /opt/tplink/EAPController/data. 2: se borra el contenedor, por ejemplo para cambiar "
       "de imagen, y el volumen queda intacto. 3: un contenedor nuevo monta el mismo volumen; tarda de 1 a 2 minutos y unos 1,9 GB de RAM "
       "en arrancar y vuelve con toda la configuración. 4: un puerto nuevo puesto en las variables del compose se ignora porque manda lo "
       "guardado en la base; con WEB_CONFIG_OVERRIDE=true se aplica.",
       [12, 37, 66, 88])
