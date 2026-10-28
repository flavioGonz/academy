#!/usr/bin/env python3
"""Lección 12 (Torch y sniffer), Laboratorio paso 3: el sniffer en el bridge con ip-address=192.168.88.50/32.
Pasa el tráfico de todos, pero solo se copian al archivo los paquetes de la cámara; el .pcap crece desde los 24 bytes
de la cabecera y en Wireshark, con filtro dns, se ve a qué nombre quiere llegar la cámara."""
from _anims_10_19 import Anim, en, ventanas, fijo, dev, viaje, linea, narr, escribir, pill_c, place, marca, LIGHT, GOLD, MINT, CORAL, GHOST

a = Anim(T=24, kicker="MIKROTIK · LABORATORIO · PASO 3", title="El sniffer copia solo lo de la cámara")
a.steps([
    "Arrancás el sniffer en el bridge, filtrado por la cámara.",
    "Pasa todo, pero solo se copian los paquetes de .50.",
    "stop y /file/print: el archivo pesa más que 24 bytes.",
    "En Wireshark, filtro dns: a qué nombre quiere llegar.",
], still=1)

a.add(dev(a, 48, 176, 222, 80, "Cámara", "192.168.88.50", "camera"))
a.add(dev(a, 48, 268, 222, 80, "PC", "192.168.88.20", "laptop"))
a.add(a.box(330, 176, 330, 172, a.INK, rx=18) + a.text(350, 206, "Router · bridge", 18, "#FFFFFF", a.SANS, 600)
      + a.box(350, 222, 290, 64, a.NAVY2, "#4E7396", rx=10, sw=1.5) + a.text(366, 248, "sniffer", 15, "#FFFFFF", a.MONO, 700)
      + a.text(366, 272, "ip-address=192.168.88.50/32", 15, LIGHT, a.MONO))
a.add(dev(a, 720, 176, 200, 80, "Internet", "lo de todos", "globe"))
a.add(a.box(720, 268, 200, 80, a.WHITE, "#C2D4E6", rx=16) + a.text(740, 298, "camara.pcap", 17, a.INK, a.MONO, 700))
a.add(dev(a, 952, 268, 200, 80, "Wireshark", "en la notebook", "laptop"))
a.add(linea(270, 216, 330, 240, a.LINE, 3) + linea(270, 308, 330, 290, a.LINE, 3))
a.add(linea(660, 216, 720, 216, a.LINE, 4) + linea(660, 308, 720, 308, a.CYAN, 3, "6 6") + linea(920, 308, 952, 308, a.LINE, 3, "6 6"))
a.add(a.text(690, 336, "copia", 15, a.CYAN, a.MONO, 600, "middle"))
for t0, t1, s, c, st in ((0, 30, "24 B: solo la cabecera", a.GREY, 0), (30, 40, "1.1KiB", a.TXT, 0), (40, 50, "9.6KiB", a.TXT, 1),
                         (50, 100, "18.2KiB (ej.)", a.OK, 0)):
    en(a, a.text(740, 326, s, 15, c, a.MONO, 600), t0, t1, still=st)

for t0 in (27, 39):
    viaje(a, "de .50", [(250, 200), (360, 306), (600, 306)], t0, t0 + 4, bg=a.BLUE, size=14, hold=0.2)
    viaje(a, "de .50", [(600, 306), (680, 216)], t0 + 4.5, t0 + 7, bg=a.BLUE, size=14, hold=0.5)
    viaje(a, "copia", [(620, 306), (690, 306)], t0 + 4.5, t0 + 7, bg=a.CYAN, size=14, hold=0.8)
    viaje(a, "de .20", [(250, 320), (360, 330), (600, 330)], t0 + 1.5, t0 + 5.5, bg=a.GREY, size=14, hold=0.2)
    viaje(a, "de .20", [(600, 330), (680, 216)], t0 + 6, t0 + 8.5, bg=a.GREY, size=14, hold=0.5)
fijo(a, place(pill_c(a, "de .50 · se copia", "#FFFFFF", a.BLUE, 14), 495, 306) + place(pill_c(a, "de .20: no se copia", "#FFFFFF", a.GREY, 14), 495, 372))
en(a, a.text(495, 378, "lo de .20 pasa y no se copia", 15, a.GREY, a.SANS, 700, "middle"), 30, 50)
viaje(a, "descargar", [(860, 290), (1010, 290)], 60, 66, bg=a.NAVY2, size=14, hold=4)

# ---- terminal
TX, TY, TW = 48, 400, 664
a.add(a.box(TX, TY, TW, 196, a.INK, rx=16) + a.text(TX + 22, TY + 30, "TERMINAL", 13, LIGHT, a.MONO, 400, extra='letter-spacing="1.8"'))
CMDS = [(0, "> /tool/sniffer/set file-name=camara.pcap file-limit=10000KiB"), (4, "> /tool/sniffer/start interface=bridge ip-address=192.168.88.50/32"),
        (52, "> /tool/sniffer/stop"), (55, '> /file/print where name~"pcap"')]
for i, (t0, c) in enumerate(CMDS):
    en(a, a.text(TX + 22, TY + 62 + i * 28, c, 15, "#FFFFFF", a.MONO), t0, 100, still=1 if t0 < 25 else 0)
en(a, a.text(TX + 22, TY + 178, "camara.pcap  18.2KiB", 15, MINT, a.MONO, 700) + a.text(TX + 270, TY + 178, "si pesa 24 B, no capturó nada", 15, GOLD, a.SANS, 600), 57, 100)

# ---- wireshark
WX, WW = 732, 420
a.add(a.box(WX, TY, WW, 196, a.WHITE, a.LINE, rx=16) + a.text(WX + 22, TY + 32, "Wireshark · camara.pcap", 16, a.INK, a.HEAD, 600))
a.add(a.box(WX + 22, TY + 46, WW - 44, 32, a.SLATE, rx=8) + a.text(WX + 34, TY + 68, "filtro:", 14, a.GREY, a.MONO))
en(a, a.text(WX + 100, TY + 68, "dns", 16, a.INK, a.MONO, 700), 75, 100)
en(a, a.text(WX + 22, TY + 108, ".50 → .1  consulta A nube.ejemplo.com", 15, a.INK, a.MONO, 600)
   + a.text(WX + 22, TY + 136, ".1 → .50  respuesta 198.51.100.30", 15, a.OK, a.MONO, 600)
   + a.text(WX + 22, TY + 174, "Nombre de ejemplo: cada marca usa el suyo.", 15, a.GREY, a.SANS), 78, 100)
en(a, a.text(WX + 22, TY + 120, "todavía sin abrir", 15, a.GREY, a.SANS), 0, 66)
en(a, a.text(WX + 22, TY + 120, "abierto: falta filtrar", 15, a.GREY, a.SANS), 66, 78)

narr(a, [
    (0, 25, "file-limit evita que una captura llene el disco del router.", a.TXT),
    (25, 50, "El sniffer copia: el tráfico sigue su camino igual que antes.", a.OK),
    (50, 75, "Un .pcap vacío pesa 24 bytes: es solo la cabecera del archivo.", a.AMB),
    (75, 100, "Con el nombre en la mano, sabés qué hay que dejar pasar o qué resolver.", a.OK),
], y=640, still_idx=1)

escribir(a, "12-l1", "El sniffer copia solo lo de la cámara",
         "Animación en cuatro tiempos del paso 3. La cámara 192.168.88.50 y una PC 192.168.88.20 entran al bridge del router, donde corre el sniffer con ip-address=192.168.88.50/32; "
         "a la derecha internet, el archivo camara.pcap y Wireshark en la notebook. Abajo, la terminal y la ventana de Wireshark. "
         "1: se configura file-name=camara.pcap con file-limit=10000KiB y se arranca en interface=bridge; el archivo pesa 24 bytes, solo la cabecera. "
         "2: pasa el tráfico de los dos equipos hacia internet, pero solo se copian al archivo los paquetes de 192.168.88.50; lo de .20 pasa y no se copia, y el archivo crece. "
         "3: con stop y /file/print where name~\"pcap\" el archivo pesa, de ejemplo, 18.2KiB; si pesara 24 bytes no habría capturado nada. Se descarga a la notebook. "
         "4: en Wireshark, con el filtro dns, se ve la consulta de la cámara por un nombre de ejemplo, nube.ejemplo.com, y la respuesta.",
         [10, 35, 46, 62, 90])
