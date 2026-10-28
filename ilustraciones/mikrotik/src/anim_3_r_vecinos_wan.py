#!/usr/bin/env python3
"""Lección 3 (Cerrar puertas) · Resumen: lo que ve el vecino del segmento del proveedor, antes y después de dejar MAC server y descubrimiento solo hacia la LAN."""
from _anim_r20_31 import *

a, _ = nuevo(24, "MIKROTIK · CERRAR PUERTAS · EN LA RED", "Lo que ve el vecino del lado del proveedor",
             ["Antes: el router se anuncia por todos los puertos, también por ether1.",
              "Antes: desde la red del proveedor se abre WinBox por MAC, sin IP.",
              "Después: anuncio y acceso por MAC salen solo hacia la LAN.",
              "Adentro no cambia nada: la notebook lo ve y entra por MAC."], still=2)

# zonas
a.add(a.box(48, 178, 340, 392, a.SLATE, a.LINE, rx=18))
a.add(a.text(66, 206, "RED DEL PROVEEDOR · ether1", 14, a.GREY, a.MONO, 600, extra='letter-spacing="1.4"'))
a.add(a.box(892, 178, 260, 392, a.SLATE, a.LINE, rx=18))
a.add(a.text(910, 206, "LAN · bridge", 14, a.GREY, a.MONO, 600, extra='letter-spacing="1.4"'))

dev(a, 66, 226, 304, 84, "Router de otro local", "mismo segmento")
dev(a, 66, 330, 304, 84, "Notebook de otro técnico", "WinBox · Neighbors")
dev(a, 908, 330, 228, 84, "Tu notebook", "192.168.88.10")

# router del cliente
RX, RY, RW, RH = 520, 306, 240, 132
a.add(wire(370, 372, RX, 372, a.BLUE, 3))
a.add(wire(RX + RW, 372, 908, 372, a.BLUE, 3))
dev(a, RX, RY, RW, RH, "hAP del cliente", "identity hap-local-12", "RouterOS 7", kind="router")
a.add(a.text(RX - 6, 350, "ether1", 14, a.GREY, a.MONO, 600, "end"))
a.add(a.text(RX + RW + 6, 350, "bridge", 14, a.GREY, a.MONO, 600))

# paneles Neighbors
def vecinos(x, y, w, titulo):
    a.add(a.box(x, y, w, 120, a.WHITE, a.LINE, rx=12))
    a.add(a.text(x + 16, y + 28, titulo, 15, a.INK, a.SANS, 600))
    a.add(a.text(x + 16, y + 54, "IDENTITY      VERSION BOARD", 13, a.GREY, a.MONO))
    a.add(wire(x + 14, y + 64, x + w - 14, y + 64, a.LINE, 1.5))

vecinos(66, 430, 304, "Neighbors de su WinBox")
vecinos(908, 430, 228, "Neighbors de tu WinBox")
fila = a.text(0, 0, "hap-local-12  7.x     hAP", 14, a.INK, a.MONO, 600)
en(a, at(fila, 82, 520), 9, 55, still=0)
en(a, a.text(82, 520, "vacío: no lo ve", 14, a.OK, a.MONO, 600), 60, 100, still=1)
en(a, at(fila, 922, 520), 9, 100, still=1)

# 1. anuncios MNDP para los dos lados
go(a, "MNDP", [(RX - 30, 372), (404, 372)], 3, 8, hold=2, bg=a.AMB, size=14)
go(a, "MNDP", [(RX + RW + 30, 372), (874, 372)], 3, 8, hold=2, bg=a.CYAN, size=14)
en(a, a.text(218, 562, "identity, versión y placa, regalados", 15, a.BAD, a.SANS, 600, "middle"), 10, 25)

# 2. MAC-WinBox desde la WAN
go(a, "MAC", [(400, 372), (RX - 30, 372)], 28, 33, hold=1, bg=a.BAD, size=14)
go(a, "login", [(RX - 34, 372), (410, 372)], 36, 41, hold=8, bg=a.AMB, size=14)
en(a, a.text(445, 412, "pide usuario", 14, a.AMB, a.MONO, 600, "middle") + a.text(445, 432, "y contraseña", 14, a.AMB, a.MONO, 600, "middle"), 37, 50)
en(a, a.text(218, 562, "solo falta adivinar la contraseña", 15, a.BAD, a.SANS, 600, "middle"), 38, 50)

# 3. después: solo hacia la LAN
cmd = term(a, 470, 456, 340, ["/tool/mac-server/mac-winbox/set", "  allowed-interface-list=LAN", "/ip/neighbor/discovery-settings/set", "  discover-interface-list=LAN"],
           title="DESPUÉS", size=13, lh=22)
en(a, cmd, 50, 100, still=1)
go(a, "MNDP", [(RX + RW + 30, 372), (874, 372)], 53, 58, hold=2, bg=a.CYAN, size=14)
en(a, mark(a, 445, 372, ok=False), 53, 75, still=1)
en(a, a.text(445, 410, "no contesta", 14, a.BAD, a.MONO, 600, "middle"), 53, 75, still=1)
go(a, "MAC", [(400, 340), (470, 340)], 61, 64, hold=10, bg=a.BAD, size=14)
en(a, a.text(218, 562, "del lado del proveedor no aparece nada", 15, a.OK, a.SANS, 600, "middle"), 60, 100, still=1)

# 4. adentro sigue igual
go(a, "MAC", [(876, 372), (RX + RW + 30, 372)], 78, 83, hold=1, bg=a.BLUE, size=14)
go(a, "login", [(RX + RW + 34, 372), (874, 372)], 86, 91, hold=9, bg=a.OK, size=14)
en(a, a.text(834, 340, "entra", 14, a.OK, a.MONO, 600, "middle"), 87, 100)
en(a, mark(a, 834, 412, ok=True), 88, 100, still=0)

narr(a, [
    (0, 25, "El descubrimiento llega a todo el segmento: en un shopping, a los otros locales.", a.TXT),
    (25, 50, "El acceso por MAC no necesita IP: alcanza con estar en el mismo segmento.", a.BAD),
    (50, 75, "Con la lista LAN, ether1 deja de anunciar y de atender por MAC.", a.OK),
    (75, 100, "Hacia la LAN es una ayuda: lo encontrás y entrás aunque la IP esté mal.", a.TXT),
], still_idx=2)

escribir(a, "3-r1.svg", "Descubrimiento y MAC server solo hacia la LAN",
         "Animación en cuatro tiempos. A la izquierda la red del proveedor de un shopping, con el router de otro local y la notebook de otro técnico; "
         "al centro el hAP del cliente con ether1 hacia esa red y el bridge hacia la LAN; a la derecha la notebook del técnico en ether2. "
         "1: antes del cambio, el hAP manda su anuncio de descubrimiento (MNDP) por los dos lados y el otro técnico lo ve en Neighbors con identity, versión y placa. "
         "2: desde la red del proveedor se abre WinBox por MAC, sin IP, y el router pide usuario y contraseña. "
         "3: con mac-winbox allowed-interface-list=LAN y discover-interface-list=LAN, el anuncio sale solo hacia la LAN, el acceso por MAC desde ether1 no contesta y "
         "del lado del proveedor deja de aparecer. 4: adentro no cambia nada: la notebook en ether2 lo ve en Neighbors y entra por MAC.",
         [12, 38, 45, 62, 90])
