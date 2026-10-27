#!/usr/bin/env python3
"""Lección 1 · Teoría · El recorrido de un evento, en orden.
Sale de teoria_md (Cómo funciona): la cámara analiza su video y, cuando la regla se cumple, manda el evento
por HTTP al proceso de webhooks en el puerto 10000; el servidor clasifica (Cruce de línea, Intrusión, Entra a zona,
Sale de zona), busca la cámara por IP o MAC y guarda la detección; si no es movimiento pide la foto
(/ISAPI/Streaming/channels/101/picture) y la sube al bucket intrusion; en paralelo avisa por socket a las pantallas.
El movimiento simple se descarta."""
from _anim_omni import new, out, when, travel, seq, lane, card

a = new(24, "EL EVENTO", "Un cruce, de la cámara a la pantalla")
a.steps([
    "La regla se cumple: la cámara manda el evento por HTTP al puerto 10000.",
    "OmniAccess lo clasifica, busca la cámara por IP o MAC y guarda la detección.",
    "En paralelo: pide la foto y la sube al bucket; avisa por socket a las pantallas.",
    "Si es movimiento simple, se descarta: no se guarda ni se muestra.",
], still=2)

XC, XO, XM, XP = 150, 470, 820, 1070
TOP, BOT = 178, 600
lane(a, XC, TOP, BOT, "Cámara", "analiza su video", w=230)
lane(a, XO, TOP, BOT, "OmniAccess", "webhooks :10000", w=230)
lane(a, XM, TOP, BOT, "MinIO", "bucket intrusion", w=210)
lane(a, XP, TOP, BOT, "Pantallas", "Monitor, Mapa, pared", w=230)

# 1 · evento por HTTP
when(a, a.pill(XC, 252, "regla cumplida", a.INK, a.AMBBG, 15, 28, "middle"), 1, 100, still=1)
seq(a, f"M{XC + 6} 300 H{XO - 8}", 5, 100, a.BLUE, "POST evento → :10000", (XC + XO) / 2, 290)
travel(a, (XC + 30, 300), (XO - 30, 300), 5, 14, dot=8)

# 2 · clasifica y guarda
cls_card = (a.box(XO + 14, 312, 300, 112, a.WHITE, a.LINE, rx=10)
            + a.text(XO + 30, 336, "tipo de evento", 15, a.GREY, a.MONO)
            + a.pill(XO + 30, 346, "Cruce de línea", a.WHITE, a.BLUE, 15, 28)
            + a.text(XO + 194, 366, "Intrusión", 15, a.GREY, a.MONO)
            + a.text(XO + 30, 396, "busca la cámara por IP o MAC", 15, a.TXT, a.SANS)
            + a.text(XO + 30, 414, "y guarda la detección", 15, a.INK, a.SANS, 600))
when(a, cls_card, 26, 100, still=1)

# 3 · foto y socket, en paralelo
seq(a, f"M{XO - 6} 462 H{XC + 8}", 51, 100, a.BLUE, "pide la foto · …/channels/101/picture", (XC + XO) / 2, 452, lsize=15)
seq(a, f"M{XC + 6} 496 H{XO - 8}", 55, 100, a.CYAN, "foto JPEG", (XC + XO) / 2, 486)
seq(a, f"M{XO + 6} 524 H{XM - 8}", 59, 100, a.CYAN, "sube la foto", (XO + XM) / 2, 514)
seq(a, f"M{XO + 6} 270 H{XP - 8}", 51, 100, a.BAD, "socket: nueva detección", (XM + XP) / 2, 262)
travel(a, (XO + 20, 270), (XP - 24, 270), 51, 57, dot=8, bg=a.BAD)
when(a, a.pill(XP, 292, "canal en rojo", a.WHITE, a.BAD, 15, 30, "middle"), 57, 100, still=1)
when(a, a.text(XP, 344, "en segundos", 15, a.BAD, a.MONO, 600, "middle"), 57, 100, still=1)

# 4 · movimiento simple
seq(a, f"M{XC + 6} 568 H{XO - 8}", 77, 100, a.GREY, "evento de movimiento", (XC + XO) / 2, 558, dash="7 6", still=0)
when(a, a.pill(XO + 16, 554, "se descarta", a.BAD, a.BADBG, 15, 28), 81, 100, still=0)

a.add(a.text(48, 640, "Con un NVR Dahua, OmniAccess mantiene abierta una suscripción al NVR y recibe los eventos de todos sus canales.", 16, a.TXT, a.SANS, 600))

out(a, 1, 1, "El recorrido de un evento de intrusión",
    "Animación en cuatro tiempos, como diagrama de secuencia con cuatro columnas: la cámara, que analiza su video; OmniAccess, "
    "con el proceso de webhooks en el puerto 10000; MinIO, con el bucket intrusion; y las pantallas (Monitor, Mapa, pared). "
    "Tiempo 1: la regla se cumple y la cámara manda el evento por HTTP al puerto 10000. "
    "Tiempo 2: OmniAccess clasifica el evento (Cruce de línea, Intrusión, Entra a zona o Sale de zona), busca la cámara por IP o MAC y guarda la detección. "
    "Tiempo 3: en paralelo, pide la foto a la cámara en /ISAPI/Streaming/channels/101/picture, la recibe y la sube al bucket, "
    "y avisa por socket a las pantallas: el canal se pone rojo en segundos. "
    "Tiempo 4: llega un evento de movimiento simple y se descarta, no se guarda ni se muestra. "
    "Al pie: con un NVR Dahua, OmniAccess mantiene abierta una suscripción al NVR y recibe los eventos de todos sus canales.",
    [10, 35, 62, 90])
