#!/usr/bin/env python3
"""Lección 4 · Resumen, "Cómo se ve en la red": los tres caminos para que un EAP en otra subred sepa dónde está
el controlador (Discovery Utility, Inform URL, DHCP option 138). Después, el EAP llama directo y aparece en Pending."""
from _anim_om_red import *

a = nueva(26, "TRES CAMINOS", "Tres formas de decirle al EAP dónde está el controlador")
F = a.steps([
    "Discovery Utility: una PC en la VLAN 20 ve el EAP y le carga la dirección con Batch Setting.",
    "Inform URL: en la web local del EAP, System Tools > Controller Settings, queda guardada.",
    "Option 138: el DHCP de la VLAN 20 manda la dirección junto con la IP.",
    "Cualquiera de los tres: el EAP llama directo a 192.168.88.10 y aparece en Pending.",
], still=3)

Y = 300
a.add(dev(a, 48, 186, 290, 92, "Discovery Utility", "PC en la VLAN 20", icon="laptop"))
a.add(dev(a, 48, 300, 290, 92, "Web local del EAP", "Inform URL", icon="laptop"))
a.add(dev(a, 420, Y, 258, 92, "EAP", "VLAN 20 · 10.10.10.x", icon="wifi"))
a.add(dev(a, 700, Y, 236, 92, "Router", "DHCP de la VLAN 20", icon="server"))
a.add(dev(a, 970, Y, 182, 92, "Controlador", "192.168.88.10", dark=True))
YL = Y + 46
a.add(line(678, YL, 700, YL, a.BLUE, 4) + line(936, YL, 970, YL, a.BLUE, 4))
a.add(line(338, 232, 380, 232, a.LINE, 3, "5 5") + line(380, 232, 380, 330, a.LINE, 3, "5 5") + line(380, 330, 420, 330, a.LINE, 3, "5 5"))
a.add(line(338, 362, 420, 362, a.LINE, 3, "5 5"))

ADDR = "controlador: 192.168.88.10"
# 1: Discovery Utility
travel(a, dot(a, a.AMB, 8), [(420, 330), (380, 330), (380, 232), (338, 232)], 3, 7, hold=0.5)
at(a, a.text(346, 218, "ve el EAP (UDP 29810)", 15, a.AMB, a.MONO, 600), 3, 25)
travel(a, pkt(a, "Batch Setting", a.BLUE), [(300, 232), (380, 232), (380, 330), (470, 330)], 10, 15, hold=2)
at(a, chip(a, 543, 410, ADDR, a.INK, a.SLATE, anchor="middle"), 15, 25)
at(a, note(a, 48, 470, 1104, 92, "En lote, desde una PC de esa subred", ["Le manda a cada equipo la IP del controlador con su usuario y clave (de fábrica, admin / admin).", "Si las claves de los equipos son distintas, se hace de a uno."], "info"), 2, 25)
# 2: Inform URL
travel(a, pkt(a, "Inform URL", a.BLUE), [(300, 362), (470, 362)], 28, 33, hold=2)
at(a, chip(a, 543, 410, ADDR, a.INK, a.SLATE, anchor="middle"), 33, 50)
at(a, note(a, 48, 470, 1104, 92, "Queda guardada en el equipo", ["Sirve para un equipo puntual y para Omada Central, con la Site URL del dashboard.", "En Docker Desktop de Windows o macOS es el camino práctico."], "info"), 27, 50)
# 3: option 138
travel(a, pkt(a, "IP + option 138", a.OK), [(760, 346), (600, 346)], 54, 59, hold=2.5)
at(a, chip(a, 543, 410, ADDR, a.OK, a.OKBG, anchor="middle", stroke=a.OK), 59, 75)
at(a, note(a, 48, 470, 1104, 92, "La red se lo dice a todos, sin tocar los equipos", ["Sirve para sucursales y VLAN enteras. En un gateway Omada va la IP tal cual; en RouterOS, en hexadecimal.", "Llega con cada concesión nueva: un EAP que ya tenía IP no se entera hasta renovar."], "ok"), 52, 75)
# 4: el EAP llama directo
travel(a, dot(a, a.BLUE, 10), [(640, YL), (700, YL), (936, YL), (1000, YL)], 78, 84, hold=1)
at(a, check(a, 818, YL - 66, 14) + a.text(840, YL - 60, "unicast: el router lo rutea", 15, a.GREY, a.MONO), 82, 100, still=1)
at(a, chip(a, 1061, 410, "Pending", a.AMB, a.AMBBG, anchor="middle", stroke=a.AMB), 85, 100, still=1)
at(a, chip(a, 543, 410, ADDR, a.INK, a.SLATE, anchor="middle"), 76, 100, still=1)
at(a, note(a, 48, 470, 1104, 92, "El broadcast no cruza routers: por eso alguien tiene que decírselo", ["Con NAT entre sede y controlador: TCP y UDP del 29810 al 29817 reenviados, mismo puerto de los dos lados.", "Más prolijo: un túnel VPN entre sedes y la option 138 con la IP privada del controlador."], "amb"), 76, 100, still=1)

write(a, 4, "r1", "Tres formas de decirle a un EAP dónde está el controlador",
      "Animación en cuatro tiempos con un EAP en la VLAN 20 (10.10.10.x), una PC con Omada Discovery Utility en esa misma subred, la web local del EAP, "
      "el router que da DHCP en la VLAN 20 y el controlador en 192.168.88.10. "
      "1: la Discovery Utility ve el EAP por su broadcast al UDP 29810 y con Batch Setting le carga la IP del controlador junto con el usuario y la clave del equipo, de fábrica admin y admin. "
      "2: en la web local del EAP, System Tools > Controller Settings, se escribe la Inform URL, que queda guardada; sirve para un equipo puntual y para Omada Central con la Site URL. "
      "3: el DHCP de la VLAN 20 manda la option 138 con la dirección del controlador junto con la IP; llega con cada concesión nueva. "
      "4: con cualquiera de los tres, el EAP llama por unicast a 192.168.88.10, el router lo rutea y el equipo aparece en Pending. "
      "Con NAT en el medio se reenvían TCP y UDP del 29810 al 29817 con el mismo puerto; lo más prolijo es un túnel VPN entre sedes.",
      [8, 36, 64, 92])
