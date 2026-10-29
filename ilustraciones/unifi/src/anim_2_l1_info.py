#!/usr/bin/env python3
"""Lección 2 · Laboratorio, paso 3: SSH a 192.168.88.20 con ubnt/ubnt e info. El AP contesta Model, Version, IP Address
y Status (Not Adopted, http://unifi:8080/inform); mientras, se anuncia en la red local por UDP 10001.
Fuentes: lab.md y theory_md de la lección (LazyAdmin); help.ui.com, Required Ports (UDP 10001: descubrimiento en la adopción)."""
from _anim_red_unifi import *  # noqa

a = new(24, "Adopción limpia", "info por SSH: lo que dice el AP antes de adoptar", [
    "La notebook abre SSH, TCP 22, a 192.168.88.20 con ubnt / ubnt.",
    "info: el AP contesta modelo, versión de firmware, IP y estado.",
    "Status Not Adopted: apunta a http://unifi:8080/inform y espera.",
    "Mientras, se anuncia por UDP 10001 y el controlador lo ve pendiente.",
], still=2, paso=3)

NB, APX, CT = 168, 560, 1032
a.add(dev(a, 48, 180, 240, 86, "Notebook", "del técnico", icon="laptop"))
a.add(dev(a, 410, 180, 300, 86, "AP reseteado", "192.168.88.20", ap=True))
a.add(dev(a, 892, 180, 260, 86, "Controlador", "misma red y VLAN", icon="server", dark=True))
lifeline(a, NB, 266, 600)
lifeline(a, APX, 266, 600)
lifeline(a, CT, 266, 600)

s0, s1 = ph(a, 0)
msg(a, NB, APX, 318, "SSH · TCP 22", s0 + 2, end=100, still=1, sub="usuario ubnt, clave ubnt")
msg(a, APX, NB, 386, "sesión abierta", s0 + 12, end=100, still=1, color=a.OK)

s0, s1 = ph(a, 1)
msg(a, NB, APX, 436, "info", s0 + 2, end=s1 + 25, still=1)
TL = ["Model:       <modelo>", "Version:     <firmware>", "IP Address:  192.168.88.20", "Status:      Not Adopted",
      "             (http://unifi:8080/inform)"]
during(a, term(a, 48, 470, 492, TL, h=134, lh=22, colors={3: GOLD, 4: GOLD}), s0 + 8, s1 + 25, still=1)
during(a, a.box(46, 468, 496, 138, "none", GOLD, rx=13, sw=3).replace('fill="none"', 'fill="none"'), ph(a, 2)[0], ph(a, 2)[1], still=1)

# 3 · qué mirar
s0, s1 = ph(a, 2)
during(a, nbox(a, 600, 300, 260, 150, "Qué mirar", ["Model: ¿es el equipo?", "Version: comparala", "IP: ¿red del controlador?", "Status: a qué inform"], "info", lh=24),
       s0 + 2, s1, still=1)

# 4 · anuncio y pendiente
s0, s1 = ph(a, 3)
for k in range(3):
    go(a, [(APX + 14, 340 + k * 40), (CT - 14, 340 + k * 40)], s0 + 2 + k * 5, s0 + 9 + k * 5, "aviso UDP 10001", a.GREY, hold=s0 + 9.5 + k * 5)
during(a, pill(a, 1152, 284, "Pending Adoption", "amb", anchor="end"), s0 + 10, 100)
during(a, nbox(a, 600, 480, 552, 108, "Si la IP es de otra red", ["hay dos DHCP o el AP está en otra VLAN:", "el anuncio no llega al controlador."], "amb"),
       s0 + 14, 100)

status(a, 640, [
    (0, 25, "El usuario de fábrica solo vale en un equipo reseteado.", a.INK, 0),
    (25, 50, "info es la radiografía del equipo: se mira antes de tocar nada.", a.INK, 0),
    (50, 75, "Un equipo reseteado busca el nombre unifi en el puerto 8080.", a.AMB, 1),
    (75, 100, "El descubrimiento es en capa 2: misma red, un solo DHCP.", a.OK, 0),
])

write(a, 2, "l1", "info por SSH antes de adoptar",
      "Animación en cuatro tiempos del paso 3 con la notebook, el AP reseteado en 192.168.88.20 y el controlador en la misma red y VLAN. "
      "1: la notebook abre SSH por TCP 22 con el usuario de fábrica ubnt y la clave ubnt, que solo valen en un equipo reseteado. "
      "2: con info, el AP contesta Model, Version (el firmware), IP Address 192.168.88.20 y Status. "
      "3: Status Not Adopted con http://unifi:8080/inform: el equipo espera un controlador; qué mirar en cada línea: si es el equipo, la versión para comparar, si la IP es de la red del controlador y a qué inform apunta. "
      "4: mientras tanto el AP se anuncia en la red local por UDP 10001 y el controlador lo muestra Pending Adoption; si la IP es de otra red, hay dos DHCP o el AP está en otra VLAN y el anuncio no llega.",
      [12, 37, 62, 92])
