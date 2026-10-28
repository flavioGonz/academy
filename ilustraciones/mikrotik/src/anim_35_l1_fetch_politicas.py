#!/usr/bin/env python3
"""Lección 35 (Vigilar con Netwatch), Laboratorio paso 4: por qué el fetch a Telegram lleva output=none.
Netwatch corre el up-script como *sys con read, write, test y reboot; sin output=none, fetch quiere guardar un archivo,
eso pide la política ftp y el script no corre. Con output=none sale el HTTPS y llega el mensaje."""
from _anims_10_19 import Anim, en, ventanas, fijo, dev, viaje, linea, narr, escribir, pill_c, place, marca, LIGHT, GOLD, MINT, CORAL, GHOST

a = Anim(T=24, kicker="MIKROTIK · LABORATORIO · PASO 4", title="El aviso a Telegram y el permiso que le falta")
a.steps([
    "El NVR vuelve: Netwatch corre el up-script como *sys.",
    "Sin output=none, fetch quiere un archivo: pide ftp y no corre.",
    "Con output=none no guarda nada: sale el HTTPS a Telegram.",
    "Llega el aviso al celular. Probalo desenchufando el NVR.",
], still=2)

a.add(dev(a, 48, 186, 260, 104, "Netwatch", "nvr · tcp-conn 554", None, dark=True, sub2="event up"))
PX, PY, PW = 350, 176, 430
a.add(a.box(PX, PY, PW, 200, a.WHITE, a.LINE, rx=16) + a.text(PX + 22, PY + 32, "Políticas de un script de Netwatch", 16, a.INK, a.HEAD, 600)
      + a.text(PX + 22, PY + 56, "corre como el usuario *sys", 15, a.GREY, a.MONO))
POL = [("read", True), ("write", True), ("test", True), ("reboot", True), ("ftp", False)]
for i, (p, ok) in enumerate(POL):
    x = PX + 22 + i * 80
    a.add(a.box(x, PY + 76, 72, 34, a.OKBG if ok else GHOST, a.OK if ok else "#C2D4E6", rx=17, sw=1.5)
          + a.text(x + 36, PY + 99, p, 15, a.OK if ok else a.GREY, a.MONO, 600, "middle"))
a.add(a.text(PX + 22 + 4 * 80 + 36, PY + 132, "no la tiene", 15, a.GREY, a.SANS, 600, "middle"))
en(a, a.box(PX + 22 + 4 * 80 - 4, PY + 72, 80, 42, "none", a.BAD, rx=21, sw=3)
   + a.text(PX + 22, PY + 168, "guardar la respuesta en un archivo pide ftp", 15, a.BAD, a.SANS, 700), 30, 50)
en(a, a.box(PX + 18, PY + 72, 4 * 80, 42, "none", a.OK, rx=21, sw=3)
   + a.text(PX + 22, PY + 168, "output=none: alcanza con estas cuatro", 15, a.OK, a.SANS, 700), 52, 100, still=1)

a.add(dev(a, 840, 176, 312, 92, "api.telegram.org", "HTTPS · sendMessage", "cloud"))
a.add(dev(a, 840, 292, 312, 84, "Celular", "del técnico", "phone"))
a.add(linea(780, 222, 840, 222, a.LINE, 4) + linea(996, 268, 996, 292, a.LINE, 4))
a.add(linea(308, 238, 350, 238, a.LINE, 4))

viaje(a, "up-script", [(260, 238), (420, 238)], 3, 9, bg=a.NAVY2, size=14, hold=14)
en(a, marca(a, 64, 326, ok=False) + a.text(88, 332, "el script no corre", 16, a.BAD, a.SANS, 700), 36, 50)
viaje(a, "HTTPS", [(730, 222), (812, 222)], 56, 62, bg=a.BLUE, size=14, hold=5)
fijo(a, place(pill_c(a, "HTTPS", "#FFFFFF", a.BLUE, 14), 812, 222))
en(a, a.box(1004, 300, 140, 34, a.OKBG, a.OK, rx=10, sw=1.5) + a.text(1074, 322, "NVR volvio", 15, a.OK, a.SANS, 700, "middle"), 78, 100)

# ---- el comando
CY = 398
a.add(a.box(48, CY, 1104, 200, a.INK, rx=16) + a.text(70, CY + 30, "up-script del paso 4", 15, LIGHT, a.MONO))
L1 = '/tool/fetch mode=https address=api.telegram.org'
L2 = 'src-path="bot123456:TOKEN-EJEMPLO/sendMessage\\?chat_id=...&text=NVR%20volvio"'
L3 = 'check-certificate=yes'
a.add(a.text(70, CY + 66, L1, 16, "#FFFFFF", a.MONO, 600))
a.add(a.text(70, CY + 94, L2, 15, "#FFFFFF", a.MONO))
a.add(a.text(70, CY + 122, L3, 16, "#FFFFFF", a.MONO, 600))
en(a, a.box(296, CY + 102, 138, 30, a.BAD, rx=8) + a.text(365, CY + 123, "sin output", 15, "#FFFFFF", a.MONO, 700, "middle"), 25, 50)
en(a, a.box(296, CY + 102, 138, 30, a.OK, rx=8) + a.text(365, CY + 123, "output=none", 15, "#FFFFFF", a.MONO, 700, "middle"), 50, 100, still=1)
en(a, a.text(70, CY + 168, "Desde RouterOS 7.13: en la terminal anda igual, desde Netwatch no. No queda ningún error a la vista.", 15, GOLD, a.SANS, 600), 25, 50)
en(a, a.text(70, CY + 168, "El \\? es para que la terminal no abra la ayuda al pegarlo.", 15, LIGHT, a.SANS, 600), 50, 100, still=1)

narr(a, [
    (0, 25, "Netwatch corre el script solo, sin nadie logueado, con permisos acotados.", a.TXT),
    (25, 50, "Si un comando pide más permisos de los que tiene, el script entero no corre.", a.BAD),
    (50, 75, "output=none: fetch hace el pedido y no escribe nada en el router.", a.OK),
    (75, 100, "Después de cada actualización, desenchufá y enchufá el NVR para probar el aviso.", a.AMB),
], y=640, still_idx=2)

escribir(a, "35-l1", "El aviso a Telegram y el permiso que le falta",
         "Animación en cuatro tiempos del paso 4. A la izquierda Netwatch con la sonda nvr; en el centro, las políticas con las que corre un script de Netwatch, como el usuario *sys: "
         "read, write, test y reboot, sin ftp; a la derecha api.telegram.org y el celular del técnico. Abajo, el up-script con /tool/fetch mode=https address=api.telegram.org, el src-path con sendMessage y check-certificate=yes. "
         "1: el NVR vuelve, la sonda pasa a up y Netwatch corre el up-script. "
         "2: sin output=none, fetch quiere guardar la respuesta en un archivo, eso pide la política ftp que Netwatch no tiene, y el script no corre: desde RouterOS 7.13 no llega nada y no queda error a la vista. "
         "3: con output=none fetch no guarda nada, alcanza con las cuatro políticas y sale el pedido HTTPS a Telegram. "
         "4: llega el aviso NVR volvio al celular; después de cada actualización conviene probarlo desenchufando el NVR.",
         [8, 35, 45, 60, 88])
