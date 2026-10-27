#!/usr/bin/env python3
"""Lección 8 · teoría: abrir con DTMF dentro de la llamada o con un GET HTTP sin llamada."""
from _anim_akuvox import Anim, A, token, chip, node, appear, mark, finish

a = Anim(T=24, kicker="AKUVOX · DOS PUERTAS", title="DTMF dentro de la llamada, HTTP sin llamada")
a.steps([
    "En la llamada, el monitor manda 732: el portero 1 dispara solo el relé B.",
    "Por HTTP: la PC abre TCP al puerto web del portero 2 y manda un GET.",
    "El portero valida la credencial y dispara el relé de DoorNum. Sin llamada.",
    "Sin TLS, todo viaja legible: cualquiera en esa red lee la credencial.",
], still=2)
PH = [(0, 25), (25, 50), (50, 75), (75, 100)]

# equipos
a.add(node(a, 48, 196, 220, 92, "Monitor", "teclas 731 y 732"))
a.add(node(a, 48, 436, 220, 92, "PC de laboratorio", "curl -u"))
a.add(a.box(430, 180, 330, 196, A.WHITE, A.LINE))
a.add(a.text(450, 214, "Portero 1", 20, A.INK, A.HEAD, 600))
a.add(a.text(450, 238, "en la llamada", 15, A.GREY, A.MONO))
a.add(a.box(430, 410, 330, 196, A.WHITE, A.LINE))
a.add(a.text(450, 444, "Portero 2", 20, A.INK, A.HEAD, 600))
a.add(a.text(450, 468, "192.168.88.21 · sin llamada", 15, A.GREY, A.MONO))


def relay_row(y, name, code):
    s = a.box(446, y, 298, 46, A.SLATE, None, rx=10)
    s += a.text(462, y + 29, name, 16, A.INK, A.SANS, 600)
    if code:
        s += a.text(560, y + 29, code, 16, A.TXT, A.MONO)
    return s


a.add(relay_row(258, "Relay A", "731 portón"))
a.add(relay_row(314, "Relay B", "732 hall"))
a.add(relay_row(520, "Relay A", "DoorNum=1"))
# llamada monitor - portero 1
a.add(a.box(268, 228, 162, 30, "#E4F5FB", None, rx=6) + a.text(349, 249, "llamada SIP", 14, A.CYAN, A.MONO, 600, "middle"))
token(a, [(280, 243), (420, 243)], 3, 10, chip(a, "732", bg=A.OK, size=15))
appear(a, a.box(446, 314, 298, 46, "none", A.OK, rx=10, sw=3) + a.pill(736, 323, "abre", A.OK, A.OKBG, 14, 28, "end"), 11, 100, still=1)
appear(a, a.pill(736, 267, "quieto", A.GREY, "#E6EDF4", 14, 28, "end"), 11, 100, still=1)
appear(a, a.text(450, 588, "el DTMF de otra llamada no le llega", 15, A.GREY, A.SANS, 600), 12, 25, still=0)

# HTTP PC - portero 2
a.add(f'<line x1="268" y1="482" x2="430" y2="482" stroke="{A.BLUE}" stroke-width="3"/>')
a.add(a.text(349, 456, "TCP · puerto 80", 14, A.BLUE, A.MONO, 600, "middle"))
token(a, [(280, 482), (420, 482)], 27, 31, chip(a, "SYN", bg=A.GREY, size=13, h=24), hold=31.5)
token(a, [(420, 498), (280, 498)], 31.5, 35, chip(a, "SYN-ACK", bg=A.GREY, size=13, h=24), hold=35.5)
token(a, [(280, 482), (420, 482)], 37, 45, chip(a, "GET", bg=A.BLUE, size=15))
appear(a, a.box(446, 520, 298, 46, "none", A.OK, rx=10, sw=3) + a.pill(736, 529, "abre", A.OK, A.OKBG, 14, 28, "end"), 56, 100, still=1)
appear(a, a.text(450, 588, "valida usuario y clave · sin llamada", 15, A.OK, A.SANS, 600), 54, 100, still=1)

# pedido HTTP
RX, RW = 800, 352
a.add(a.box(RX, 180, RW, 250, A.INK, None, rx=16))
a.add(a.text(RX + 20, 212, "EL PEDIDO HTTP", 13, "#9FC3E3", A.MONO, 600, extra='letter-spacing="2"'))
appear(a, a.text(RX + 20, 248, "GET /fcgi/OpenDoor", 16, A.WHITE, A.MONO, 600)
       + a.text(RX + 20, 272, "  ?action=OpenDoor", 16, A.WHITE, A.MONO)
       + a.text(RX + 20, 296, "  &DoorNum=1", 16, "#FFD28A", A.MONO, 600)
       + a.text(RX + 20, 334, "encabezado de autenticación:", 14, "#9FC3E3", A.MONO)
       + a.text(RX + 20, 358, "abre-lab · Ejemplo-Http-2026", 16, A.WHITE, A.MONO, 600), 37, 100, still=1)
appear(a, a.text(RX + 20, 402, "DoorNum=1 relé A · DoorNum=2 relé B", 14, "#5BE0A5", A.MONO, 600), 55, 100, still=1)
appear(a, a.box(RX + 12, 340, RW - 24, 28, "none", "#FF8A73", rx=6, sw=2.5), 76, 100, still=0)

# alguien mirando la red
a.add(a.box(RX, 452, RW, 154, A.WHITE, A.LINE))
a.add(a.text(RX + 20, 486, "Otro equipo en la misma red", 16, A.INK, A.SANS, 600))
a.add(a.text(RX + 20, 512, "ve pasar los paquetes", 14, A.GREY, A.MONO))
token(a, [(430, 498), (RX, 540)], 77, 84, chip(a, "copia", bg=A.BAD, size=13, h=24), hold=84.5)
appear(a, a.text(RX + 20, 552, "abre-lab · Ejemplo-Http-2026", 16, A.BAD, A.MONO, 600) + mark(a, RX + RW - 30, 482, False, 14)
       + a.text(RX + 20, 584, "por eso: solo red de porteros, nunca admin", 14, A.BAD, A.SANS, 600), 84, 100, still=0)

finish(a, "8-t1.svg", "DTMF dentro de la llamada y HTTP sin llamada",
       "Animación en cuatro tiempos con monitor, PC de laboratorio, portero 1 con Relay A código 731 portón y Relay B código 732 hall, y portero 2 en 192.168.88.21. "
       "1: durante la llamada el monitor manda 732; el portero 1 compara con los códigos de sus relés y dispara solo el relé B; el portero 2 no está en la llamada y no se entera. "
       "2: la PC abre una conexión TCP al puerto 80 del portero 2 y manda GET /fcgi/OpenDoor?action=OpenDoor&DoorNum=1 con el usuario abre-lab y su clave en el encabezado de autenticación. "
       "3: el portero 2 valida la credencial y dispara el relé A, sin ninguna llamada; DoorNum=1 es el relé A y DoorNum=2 el relé B. "
       "4: como HTTP no lleva TLS, otro equipo en la misma red puede leer el usuario y la clave; por eso el comando vive solo en la red de porteros y nunca con admin.",
       [12, 40, 65, 92])
