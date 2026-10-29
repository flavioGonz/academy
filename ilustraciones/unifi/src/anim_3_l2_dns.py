#!/usr/bin/env python3
"""Lección 3 · Laboratorio, paso 2: el nombre unifi en el DNS del sitio. El AP reseteado recibe por DHCP el DNS del
MikroTik, consulta el nombre de fábrica unifi, la entrada /ip dns static contesta 10.10.10.5 y el AP manda el inform.
Fuentes: lab.md y theory_md de la lección (el equipo reseteado busca unifi por defecto, http://unifi:8080/inform);
RouterOS 7, /ip/dns (static y allow-remote-requests para responder a la LAN)."""
from _anim_red_unifi import *  # noqa

a = new(24, "Inform remoto", "DNS: el nombre unifi lleva al controlador", [
    "Con la IP, el DHCP le dio al AP el DNS del sitio: el MikroTik, 192.168.88.1.",
    "El AP busca el nombre de fábrica: consulta unifi por UDP 53.",
    "La entrada estática del MikroTik contesta: unifi = 10.10.10.5.",
    "Con esa IP manda el inform al 8080 y aparece pendiente para adoptar.",
], still=2, paso=2)

APX, MK, CT = 168, 560, 1032
a.add(dev(a, 48, 180, 240, 86, "AP reseteado", "192.168.88.20", ap=True))
a.add(dev(a, 410, 180, 300, 86, "MikroTik", "DHCP y DNS · .88.1", icon="server", dark=True))
a.add(dev(a, 892, 180, 260, 86, "Controlador", "10.10.10.5", icon="server", dark=True))
lifeline(a, APX, 266, 600)
lifeline(a, MK, 266, 600)
lifeline(a, CT, 266, 600)

s0, s1 = ph(a, 0)
msg(a, MK, APX, 316, "Ack · DNS 192.168.88.1", s0 + 3, end=100, still=1, color=a.OK, sub="junto con 192.168.88.20")

s0, s1 = ph(a, 1)
msg(a, APX, MK, 386, "consulta: unifi · UDP 53", s0 + 3, end=100, still=1)
during(a, pill(a, APX - 120, 420, "http://unifi:8080/inform", "grey"), s0 + 1, s1 + 25)

s0, s1 = ph(a, 2)
msg(a, MK, APX, 466, "respuesta: unifi = 10.10.10.5", s0 + 3, end=100, still=1, color=a.OK)
during(a, term(a, 640, 300, 512, ["/ip dns static add name=unifi \\", "    address=10.10.10.5"], title="entrada en el MikroTik"),
       s0 + 1, 100, still=1)
during(a, nbox(a, 640, 412, 512, 80, "", ["Para responder a la LAN, el DNS del MikroTik", "tiene allow-remote-requests=yes."], "amb", lh=22),
       s0 + 6, s1, still=1)

s0, s1 = ph(a, 3)
msg(a, APX, CT, 548, "inform · http://unifi:8080/inform → 10.10.10.5", s0 + 3, end=100, still=0)
during(a, pill(a, CT, 284, "Pending Adoption", "amb", anchor="middle"), s0 + 9, 100)

status(a, 640, [
    (0, 25, "El DNS que usa el AP es el que le entrega el DHCP del sitio.", a.INK, 0),
    (25, 50, "Un equipo reseteado apunta a http://unifi:8080/inform: necesita resolver unifi.", a.INK, 0),
    (50, 75, "Si el DNS del sitio es tuyo, el nombre sobrevive a reinicios y actualizaciones.", a.OK, 1),
    (75, 100, "Mismo resultado que option 43, pero por nombre.", a.OK, 0),
])

write(a, 3, "l2", "El nombre unifi en el DNS del sitio",
      "Animación en cuatro tiempos del paso 2 entre el AP reseteado (192.168.88.20), el MikroTik del sitio, que es DHCP y DNS en 192.168.88.1, y el controlador en 10.10.10.5. "
      "1: junto con la IP, el Ack del DHCP le da al AP el DNS del sitio, 192.168.88.1. "
      "2: el AP tiene la URL de fábrica http://unifi:8080/inform y consulta el nombre unifi por UDP 53. "
      "3: la entrada /ip dns static add name=unifi address=10.10.10.5 contesta unifi = 10.10.10.5; "
      "para responder consultas de la LAN, el DNS del MikroTik tiene allow-remote-requests=yes. "
      "4: con esa IP el AP manda el inform al puerto 8080 del controlador y aparece Pending Adoption. "
      "Si el DNS del sitio es tuyo, el nombre sobrevive a reinicios y actualizaciones, como option 43.",
      [12, 37, 62, 90])
