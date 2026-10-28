#!/usr/bin/env python3
"""Lección 27 (Rutas estáticas), Laboratorio paso 2: la ruta por un gateway que no existe queda activa,
el router pregunta por ARP la MAC de .250, nadie contesta y el ping se pierde sin salir."""
from _anims_10_19 import Anim, en, fijo, dev, viaje, linea, narr, escribir, pill_c, place, marca, LIGHT, GOLD, MINT, CORAL

a = Anim(T=22, kicker="MIKROTIK · LABORATORIO · PASO 2", title="Ruta activa, gateway muerto: el ping no sale")
a.steps([
    "Agregás la ruta: .250 está en la red del bridge y queda activa.",
    "El ping busca la MAC de .250: ARP pregunta a toda la LAN.",
    "Nadie contesta: el router insiste y el ping se pierde.",
    "La ruta sigue con A: nadie probó el gateway todavía.",
], still=2)

# ---- red del banco
a.add(a.box(48, 176, 300, 96, a.INK, a.INK, rx=16) + a.text(70, 212, "Router de banco", 19, "#FFFFFF", a.SANS, 600)
      + a.text(70, 236, "bridge 192.168.88.1/24", 15, LIGHT, a.MONO) + a.text(70, 257, "ruta: 10.20.30.0/24 por .250", 15, LIGHT, a.MONO))
a.add(linea(198, 272, 198, 360, a.LINE, 4))
a.add(linea(80, 360, 560, 360, a.LINE, 4))
a.add(a.text(570, 365, "LAN", 15, a.GREY, a.MONO))
a.add(linea(160, 360, 160, 420, a.LINE, 4))
a.add(linea(440, 360, 440, 420, a.LINE, 4))
a.add(dev(a, 48, 420, 240, 84, "Notebook", "ether2 · DHCP", "laptop"))
a.add(a.box(324, 420, 240, 84, "#FFFFFF", "#C2D4E6", rx=16, sw=2, extra='stroke-dasharray="7 6"')
      + a.text(344, 454, "192.168.88.250", 18, a.GREY, a.MONO, 600) + a.text(344, 480, "no existe (a propósito)", 15, a.GREY, a.SANS))

# ARP: dos intentos, sin respuesta
for t in (27, 52):
    viaje(a, "ARP ¿quién es .250?", [(198, 300), (198, 360), (300, 360)], t, t + 6, bg=a.AMB, size=14, hold=0.5)
    viaje(a, "ARP", [(300, 360), (160, 360), (160, 396)], t + 6.5, t + 10, bg=a.AMB, size=14, hold=1.5)
    viaje(a, "ARP", [(300, 360), (440, 360), (440, 396)], t + 6.5, t + 10, bg=a.AMB, size=14, hold=1.5)
    en(a, a.text(168, 540, "no es mi IP: la ignora", 15, a.GREY, a.SANS, 600, "middle"), t + 10, t + 22)
    en(a, marca(a, 548, 420, ok=False) + a.text(444, 540, "nadie contesta", 15, a.BAD, a.SANS, 600, "middle"), t + 10, t + 22)
fijo(a, place(pill_c(a, "ARP ¿quién es .250?", "#FFFFFF", a.AMB, 14), 392, 334)
     + marca(a, 548, 420, ok=False) + a.text(444, 540, "nadie contesta", 15, a.BAD, a.SANS, 600, "middle"))
# el ping queda esperando en el router y se descarta
en(a, place(pill_c(a, "ping a 10.20.30.1", "#FFFFFF", a.BLUE, 14), 268, 152 + 140), 25, 74)
en(a, place(pill_c(a, "ping descartado", "#FFFFFF", a.BAD, 14), 268, 292), 74, 100)
fijo(a, place(pill_c(a, "ping a 10.20.30.1", "#FFFFFF", a.BLUE, 14), 268, 292))
en(a, a.text(48, 586, "Sin la MAC del gateway, el paquete no tiene a quién entregarse.", 16, a.TXT, a.SANS, 600), 30, 100, still=1)

# ---- terminal
X, Y, W = 610, 176, 542
a.add(a.box(X, Y, W, 392, a.INK, rx=16))
a.add(a.text(X + 22, Y + 32, "TERMINAL", 13, LIGHT, a.MONO, 400, extra='letter-spacing="1.8"'))
L = [Y + 66, Y + 90, Y + 132, Y + 186, Y + 222, Y + 264, Y + 300]
a.add(a.text(X + 22, L[0], "> /ip/route/add dst-address=10.20.30.0/24", 15, "#FFFFFF", a.MONO))
a.add(a.text(X + 58, L[1], "gateway=192.168.88.250", 15, "#FFFFFF", a.MONO))
a.add(a.text(X + 22, L[2], "> /ip/route/print where dst-address=10.20.30.0/24", 15, "#FFFFFF", a.MONO))
row = (a.box(X + 14, L[3] - 26, W - 28, 40, a.NAVY2, rx=10)
       + a.text(X + 26, L[3], "As", 16, MINT, a.MONO, 700) + a.text(X + 70, L[3], "10.20.30.0/24", 16, "#FFFFFF", a.MONO, 600)
       + a.text(X + 236, L[3], "192.168.88.250", 16, "#FFFFFF", a.MONO) + a.text(X + W - 30, L[3], "1", 16, "#FFFFFF", a.MONO, 600, "end"))
en(a, row, 6, 100, still=1)
en(a, a.text(X + 22, L[4], "A = activa: .250 cae en 192.168.88.0/24", 15, MINT, a.MONO), 8, 75, still=1)
en(a, a.text(X + 22, L[5], "> /ping 10.20.30.1 count=3", 15, "#FFFFFF", a.MONO), 25, 100, still=1)
en(a, a.text(X + 22, L[6], "sent=3 received=0 packet-loss=100%", 15, CORAL, a.MONO, 600), 66, 100, still=1)
en(a, a.text(X + 22, L[6] + 46, "La ruta no sabe si .250 está vivo.", 16, GOLD, a.SANS, 600)
   + a.text(X + 22, L[6] + 70, "Paso 3: check-gateway=ping lo prueba.", 16, GOLD, a.SANS, 600), 75, 100)
en(a, a.box(X + 14, L[3] - 26, W - 28, 40, "none", GOLD, rx=10, sw=2.5), 75, 100)

narr(a, [
    (0, 25, "Un gateway dentro de una red conectada activa cuenta como alcanzable.", a.TXT),
    (25, 50, "Para entregar el paquete a .250 el router necesita su MAC: la pide por ARP, en broadcast.", a.AMB),
    (50, 75, "Sin respuesta, el ping nunca sale de la LAN: 100% de pérdida.", a.BAD),
    (75, 100, "Activa quiere decir que el gateway cae en una red conectada, no que conteste.", a.AMB),
], still_idx=2)

escribir(a, "27-l1", "Ruta activa, gateway muerto",
         "Animación en cuatro tiempos del paso 2. A la izquierda, el router de banco con el bridge 192.168.88.1/24, la notebook en ether2 "
         "y un recuadro punteado para 192.168.88.250, que no existe a propósito; a la derecha, la terminal. "
         "1: se agrega la ruta 10.20.30.0/24 con gateway 192.168.88.250 y el print la muestra con As, activa, porque .250 cae dentro de la red conectada. "
         "2: con /ping 10.20.30.1 el router necesita la MAC de .250 y manda un ARP en broadcast a toda la LAN; la notebook lo recibe y lo ignora porque no es su IP. "
         "3: nadie contesta, el router vuelve a preguntar y el ping se descarta sin salir: sent=3 received=0 packet-loss=100%. "
         "4: la ruta sigue activa porque nadie probó el gateway; en el paso 3, check-gateway=ping lo prueba.",
         [10, 30, 45, 62, 72, 90])
