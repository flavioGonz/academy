#!/usr/bin/env python3
"""Lección 39 (Dos WAN: IP fija + DHCP), Resumen: con la fija caída el local sale por el 4G y el paquete
cambia de origen en tres NAT (MikroTik, router 4G, CGNAT del operador). La respuesta vuelve, pero nada de afuera
puede entrar; Back To Home se arma por el relay."""
from _anims_10_19 import Anim, en, ventanas, fijo, dev, viaje, linea, narr, escribir, pill_c, place, marca, LIGHT, GOLD, MINT, CORAL, GHOST

a = Anim(T=28, kicker="MIKROTIK · IP FIJA + DHCP · EN LA RED", title="Por el 4G sale todo, pero no entra nada")
a.steps([
    "Sale por el 4G: el origen cambia en tres NAT.",
    "La respuesta vuelve: cada NAT deshace lo suyo.",
    "La central quiere entrar: el CGNAT no sabe a quién darlo.",
    "Back To Home: router y celular se encuentran en el relay.",
], still=2)

COLS = [(48, 180, "PC", "en la LAN", "laptop"), (262, 190, "MikroTik", "masquerade", None),
        (486, 190, "Router 4G", "NAT propio", "wifi"), (710, 200, "CGNAT", "del operador", "globe"),
        (944, 208, "Servidor", "192.0.2.80", "server")]
CX = []
for i, (x, w, t, s, ic) in enumerate(COLS):
    a.add(dev(a, x, 176, w, 84, t, s, ic, dark=(i == 1)))
    CX.append(x + w / 2)
    if i:
        px = COLS[i - 1][0] + COLS[i - 1][1]
        a.add(linea(px, 218, x, 218, a.LINE, 4))

a.add(a.text(48, 294, "ida: origen del paquete", 15, a.GREY, a.MONO))
a.add(a.text(48, 364, "vuelta: destino", 15, a.GREY, a.MONO))
IDA = ["192.168.88.20", "192.168.8.100", "100.64.12.34", "198.51.100.77", "ve .77"]
VUE = ["192.168.88.20", "192.168.8.100", "100.64.12.34", "198.51.100.77", "a .77"]
for i, s in enumerate(IDA):
    t0 = 2 + i * 4.5
    c = a.BLUE if i in (0, 4) else a.AMB
    en(a, place(pill_c(a, s, "#FFFFFF", c, 14), CX[i], 320), t0, 100, still=1)
for i in range(4, -1, -1):
    t0 = 27 + (4 - i) * 4.5
    c = a.OK
    en(a, place(pill_c(a, VUE[i], "#FFFFFF", c, 14), CX[i], 390), t0, 100, still=1)
for i, t in ((1, "masquerade"), (2, "NAT del 4G"), (3, "CGNAT")):
    en(a, a.text(CX[i], 280, t, 15, a.AMB, a.MONO, 600, "middle"), 2 + i * 4.5, 50)
en(a, marca(a, CX[0] + 86, 390, ok=True), 45, 100, still=1)

# ---- abajo: lo que entra
BY = 430
a.add(a.box(48, BY, 1104, 176, a.WHITE, a.LINE, rx=16))
en(a, a.text(72, BY + 60, "El servidor solo ve 198.51.100.77, la IP pública del CGNAT.", 17, a.INK, a.SANS, 600)
   + a.text(72, BY + 88, "La PC, el MikroTik y el router 4G quedan escondidos detrás.", 16, a.TXT, a.SANS), 22, 50)
en(a, a.text(72, BY + 128, "Cada NAT anota la conexión: por eso la respuesta encuentra el camino de vuelta.", 16, a.OK, a.SANS, 600), 40, 50)
# 3: la central
en(a, dev(a, 912, BY + 22, 220, 84, "Central", "198.51.100.50", "shield"), 50, 75, still=1)
viaje(a, "SYN a 198.51.100.77:8443", [(780, BY + 64), (700, BY + 64)], 52, 58, bg=a.BLUE, size=14, hold=17)
en(a, marca(a, 560, BY + 64, ok=False) + a.text(540, BY + 70, "CGNAT", 16, a.BAD, a.MONO, 700, "end") + a.text(72, BY + 132, "El CGNAT no tiene ninguna conexión que coincida: lo descarta.", 17, a.BAD, a.SANS, 600)
   + a.text(72, BY + 156, "Lo publicado por la IP fija no se ve mientras dure el corte.", 16, a.TXT, a.SANS), 59, 75, still=1)
fijo(a, place(pill_c(a, "SYN a 198.51.100.77:8443", "#FFFFFF", a.BLUE, 14), 700, BY + 64))
# 4: back to home por el relay
en(a, dev(a, 72, BY + 22, 220, 84, "MikroTik", "detrás del 4G", None, dark=True) + dev(a, 470, BY + 22, 260, 84, "Relay de MikroTik", "Back To Home", "cloud")
   + dev(a, 912, BY + 22, 220, 84, "Celular", "del técnico", "phone"), 75, 100)
en(a, linea(292, BY + 64, 470, BY + 64, a.LINE, 3, "6 6")
   + linea(730, BY + 64, 912, BY + 64, a.LINE, 3, "6 6"), 75, 100)
viaje(a, "sale el router", [(330, BY + 64), (420, BY + 64)], 77, 83, bg=a.NAVY2, size=14, hold=0.5)
viaje(a, "sale el celular", [(900, BY + 64), (760, BY + 64)], 79, 84, bg=a.NAVY2, size=14, hold=0.5)
en(a, a.text(72, BY + 140, "Los dos abren hacia afuera y el relay los une: el técnico entra igual.", 17, a.OK, a.SANS, 600), 85, 100)

narr(a, [
    (0, 25, "Con la fija caída, el router sale por ether2: tres traducciones en fila.", a.AMB),
    (25, 50, "Cada NAT guarda la conexión y sabe a quién devolver la respuesta.", a.OK),
    (50, 75, "Para entrar hace falta una conexión armada desde adentro, y nadie la armó.", a.BAD),
    (75, 100, "Avisale al cliente: con el 4G andando sale todo, pero no entra lo publicado.", a.TXT),
], y=640, still_idx=2)

escribir(a, "39-r1", "Por el 4G sale todo, pero no entra nada",
         "Animación en cuatro tiempos, con la IP fija caída y el local saliendo por el 4G. Arriba, en fila: la PC 192.168.88.20, el MikroTik con masquerade, "
         "el router 4G con su NAT propio, el CGNAT del operador y un servidor de internet, 192.0.2.80. "
         "1: el paquete sale y cambia de origen tres veces: 192.168.88.20, luego 192.168.8.100 por el masquerade del MikroTik, luego 100.64.12.34 por el NAT del router 4G, "
         "y 198.51.100.77 por el CGNAT; el servidor ve 198.51.100.77. "
         "2: la respuesta vuelve y cada NAT deshace su traducción hasta llegar a la PC. "
         "3: la central de monitoreo, 198.51.100.50, manda un SYN a 198.51.100.77:8443; el CGNAT no tiene ninguna conexión que coincida y lo descarta: lo publicado por la IP fija no se ve mientras dure el corte. "
         "4: con Back To Home, el router y el celular del técnico abren conexiones hacia el relay de MikroTik y el relay los une. Todas las direcciones son de ejemplo.",
         [10, 35, 62, 70, 90])
