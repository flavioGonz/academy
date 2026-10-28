#!/usr/bin/env python3
"""Lección 35 (Vigilar con Netwatch), Resumen: ping contra tcp-conn sobre el NVR de un local.
Con el servicio de video caído el NVR sigue contestando el ping, pero el SYN al 554 recibe RST: la sonda tcp-conn
pasa a down y corre el down-script una vez; cuando el servicio vuelve, el saludo de tres pasos se completa y corre el up-script."""
from _anims_10_19 import Anim, en, ventanas, fijo, dev, viaje, linea, narr, escribir, pill_c, place, marca, LIGHT, GOLD, MINT, CORAL, GHOST

a = Anim(T=28, kicker="MIKROTIK · NETWATCH · EN LA RED", title="El NVR contesta el ping, pero el video no anda")
a.steps([
    "NVR sano: vuelve el ping y se completa SYN, SYN-ACK, ACK.",
    "Se cae el servicio de video: el ping vuelve, el 554 contesta RST.",
    "tcp-conn pasa a down y corre el down-script, una sola vez.",
    "Vuelve el servicio: el saludo se completa, up y up-script.",
], still=2)

a.add(dev(a, 48, 186, 240, 116, "Router", "Netwatch", None, dark=True, sub2="dos sondas al NVR"))
a.add(a.box(912, 186, 240, 116, a.WHITE, "#C2D4E6", rx=16) + a.text(932, 218, "NVR", 19, a.INK, a.SANS, 600)
      + a.text(932, 242, "192.168.88.50", 15, a.GREY, a.MONO))
en(a, a.pill(932, 258, "554 escuchando", a.OK, a.OKBG, 14, 28), 0, 26)
en(a, a.pill(932, 258, "554 cerrado", a.BAD, a.BADBG, 14, 28), 26, 76, still=1)
en(a, a.pill(932, 258, "554 escuchando", a.OK, a.OKBG, 14, 28), 76, 100)
YA, YB = 214, 274
a.add(linea(288, YA, 912, YA, a.LINE, 3) + linea(288, YB, 912, YB, a.LINE, 3))
L, R = 380, 820
a.add(a.text(600, YA - 20, "sonda simple: ping", 15, a.GREY, a.MONO, 400, "middle") + a.text(600, YB - 20, "sonda tcp-conn: saludo TCP al 554", 15, a.GREY, a.MONO, 400, "middle"))


def ida(lbl, y, t0, c=a.BLUE):
    viaje(a, lbl, [(L, y), (R, y)], t0, t0 + 5, bg=c, size=14, hold=0.4)


def vuelta(lbl, y, t0, c=a.OK):
    viaje(a, lbl, [(R, y), (L, y)], t0, t0 + 5, bg=c, size=14, hold=0.4)


# sonda simple (ping)
for t0 in (2, 28, 56, 80):
    ida("echo request", YA, t0)
    vuelta("echo reply", YA, t0 + 6)
# sonda tcp-conn
ida("SYN :554", YB, 3)
vuelta("SYN-ACK", YB, 9)
ida("ACK", YB, 15)
ida("SYN :554", YB, 38)
vuelta("RST", YB, 44, a.BAD)
ida("SYN :554", YB, 60)
vuelta("RST", YB, 66, a.BAD)
ida("SYN :554", YB, 78)
vuelta("SYN-ACK", YB, 84)
ida("ACK", YB, 90)
fijo(a, place(pill_c(a, "RST", "#FFFFFF", a.BAD, 14), 600, YB))

# ---- estado de cada sonda
CY = 324


def tarjeta(x, titulo, sub, estados):
    a.add(a.box(x, CY, 540, 116, a.WHITE, a.LINE, rx=16) + a.text(x + 22, CY + 34, titulo, 17, a.INK, a.HEAD, 600)
          + a.text(x + 22, CY + 58, sub, 15, a.GREY, a.MONO))
    for t0, t1, s, fg, bg, st, nota, nc in estados:
        en(a, a.pill(x + 22, CY + 72, s, fg, bg, 15, 30) + a.text(x + 140, CY + 93, nota, 16, nc, a.SANS, 600), t0, t1, still=st)


tarjeta(48, "type=simple", "ping al NVR", [
    (0, 25, "up", a.OK, a.OKBG, 0, "el equipo está prendido", a.OK),
    (25, 100, "up", a.OK, a.OKBG, 1, "no se entera: el ping vuelve", a.AMB)])
tarjeta(612, "type=tcp-conn port=554", "saludo TCP al servicio", [
    (0, 50, "up", a.OK, a.OKBG, 0, "el servicio atiende", a.OK),
    (50, 93, "down", a.BAD, a.BADBG, 1, "el 554 rechaza la conexión", a.BAD),
    (93, 100, "up", a.OK, a.OKBG, 0, "saludo completo otra vez", a.OK)])

# ---- log
LY = 458
a.add(a.box(48, LY, 1104, 140, a.INK, rx=16) + a.text(70, LY + 30, "/log/print where message~\"NVR\"", 15, LIGHT, a.MONO))
en(a, a.text(70, LY + 64, "down  ·  NVR 192.168.88.50 caido  ·  sale el mail a soporte", 16, CORAL, a.MONO, 600), 51, 100, still=1)
en(a, a.text(70, LY + 94, "(la prueba siguiente también falla: el script no se repite)", 15, LIGHT, a.MONO), 70, 100, still=1)
en(a, a.text(70, LY + 124, "up  ·  NVR 192.168.88.50 volvio", 16, MINT, a.MONO, 600), 93, 100)

narr(a, [
    (0, 25, "El ping dice que el equipo está prendido; tcp-conn, que el servicio atiende.", a.TXT),
    (25, 50, "El NVR sigue prendido, pero nadie escucha en el 554: el SYN recibe RST.", a.BAD),
    (50, 75, "Un aviso por cambio de estado: te enterás antes de que el cliente quiera ver una grabación.", a.AMB),
    (75, 100, "Para un NVR, la sonda que importa es la del puerto del servicio.", a.OK),
], y=640, still_idx=2)

escribir(a, "35-r1", "El NVR contesta el ping, pero el video no anda",
         "Animación en cuatro tiempos con el router y el NVR del local, 192.168.88.50, y dos sondas de Netwatch: arriba una simple, con ping; abajo una tcp-conn al puerto 554. "
         "Debajo, el estado de cada sonda y el log. 1: el NVR está sano; el ping vuelve y el saludo TCP se completa con SYN, SYN-ACK y ACK: las dos sondas en up. "
         "2: se cae el servicio de video y el 554 queda cerrado; el ping sigue volviendo y la sonda simple sigue up sin enterarse, mientras el SYN al 554 recibe RST. "
         "3: la sonda tcp-conn pasa a down y corre el down-script una vez, que deja el aviso en el log y manda el mail; la prueba siguiente también falla y el script no se repite. "
         "4: vuelve el servicio, el saludo se completa, la sonda pasa a up y corre el up-script.",
         [10, 30, 46, 62, 88, 97])
