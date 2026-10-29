#!/usr/bin/env python3
"""Lección 3 · Laboratorio, paso 1: DHCP option 43 en RouterOS 7. El AP pide IP (Discover), el MikroTik del sitio
responde Offer y Ack con 192.168.88.20 y la opción 43 (0x01040A0A0A05), el AP la lee como 10.10.10.5 y manda el inform
a http://10.10.10.5:8080/inform. Fuentes: lab.md y theory_md de la lección (subopción 1, largo 4, IP en hex);
RFC 2131 (Discover, Offer, Request, Ack) y RFC 2132 (opción 43, información del fabricante)."""
from _anim_red_unifi import *  # noqa

a = new(24, "Inform remoto", "Option 43: la dirección del controlador viaja con la IP", [
    "Discover: el AP reseteado pide IP por broadcast en 192.168.88.0/24.",
    "Offer y Ack traen la IP y la opción 43 que cargaste en el MikroTik.",
    "El AP lee la opción: subopción 1, largo 4 y la IP 10.10.10.5.",
    "Manda el inform a http://10.10.10.5:8080/inform y queda pendiente.",
], still=2, paso=1)

APX, MK, CT = 168, 560, 1032
a.add(dev(a, 48, 180, 240, 86, "AP reseteado", "sitio remoto", ap=True))
a.add(dev(a, 410, 180, 300, 86, "MikroTik", "DHCP · 192.168.88.1", icon="server", dark=True))
a.add(dev(a, 892, 180, 260, 86, "Controlador", "10.10.10.5", icon="server", dark=True))
lifeline(a, APX, 266, 600)
lifeline(a, MK, 266, 600)
lifeline(a, CT, 266, 600)

s0, s1 = ph(a, 0)
msg(a, APX, MK, 312, "DHCP Discover", s0 + 3, end=100, still=1, sub="broadcast")

s0, s1 = ph(a, 1)
msg(a, MK, APX, 372, "Offer · 192.168.88.20", s0 + 2, end=100, still=1, color=a.OK, sub="+ opción 43", subcolor=a.AMB)
msg(a, APX, MK, 432, "Request", s0 + 9, end=100, still=1)
msg(a, MK, APX, 480, "Ack · opción 43", s0 + 15, end=100, still=1, color=a.OK)

# 3 · los seis bytes
s0, s1 = ph(a, 2)
BX, BY = 640, 300
panel = a.box(BX, BY, 512, 176, a.WHITE, a.LINE, rx=14)
panel += a.text(BX + 20, BY + 34, "opción 43 = 0x01040A0A0A05", 17, a.INK, a.MONO, 600)
BYTES = [("01", "sub 1", a.BLUE), ("04", "largo 4", a.BLUE), ("0A", "10", a.OK), ("0A", "10", a.OK), ("0A", "10", a.OK), ("05", "5", a.OK)]
for i, (b, lab, c) in enumerate(BYTES):
    x = BX + 20 + i * 80
    panel += a.box(x, BY + 54, 68, 50, "#EEF4FA", c, rx=10, sw=2.5)
    panel += a.text(x + 34, BY + 86, b, 19, c, a.MONO, 600, "middle")
    panel += a.text(x + 34, BY + 128, lab, 15, a.TXT, a.MONO, 400, "middle")
panel += a.text(BX + 20 + 2 * 80, BY + 160, "IP del controlador: 10.10.10.5", 15, a.OK, a.SANS, 600)
during(a, panel, s0 + 2, s1, still=1)

# 4 · inform
s0, s1 = ph(a, 3)
msg(a, APX, CT, 548, "inform · http://10.10.10.5:8080/inform", s0 + 3, end=100, still=0, sub="por la ruta entre el sitio y el controlador")
during(a, pill(a, CT, 284, "Pending Adoption", "amb", anchor="middle"), s0 + 9, 100)

status(a, 640, [
    (0, 25, "El AP no sabe dónde está el controlador: lo va a aprender con la IP.", a.INK, 0),
    (25, 50, "dhcp-option=unifi-inform en la red 192.168.88.0/24 la agrega a cada respuesta.", a.INK, 0),
    (50, 75, "Con 10.10.10.20 serían otros bytes: 0x01040A0A0A14.", a.AMB, 1),
    (75, 100, "Llega en cada arranque: sobrevive a reinicios y actualizaciones.", a.OK, 0),
])

write(a, 3, "l1", "DHCP option 43 con la dirección del controlador",
      "Animación en cuatro tiempos del paso 1 entre el AP reseteado del sitio remoto, el MikroTik que es el servidor DHCP en 192.168.88.1 y el controlador en 10.10.10.5. "
      "1: el AP manda DHCP Discover por broadcast. "
      "2: el MikroTik contesta Offer con 192.168.88.20 y la opción 43, el AP pide con Request y el Ack trae otra vez la opción 43, "
      "porque dhcp-option=unifi-inform está en la red 192.168.88.0/24. "
      "3: el AP lee el valor 0x01040A0A0A05 en seis bytes: 01 subopción 1, 04 largo 4, y 0A 0A 0A 05, que son 10, 10, 10 y 5: la IP del controlador 10.10.10.5. "
      "Con 10.10.10.20 sería 0x01040A0A0A14. "
      "4: el AP manda el inform a http://10.10.10.5:8080/inform por la ruta entre el sitio y el controlador y aparece Pending Adoption. "
      "Como llega en cada arranque, sobrevive a reinicios y actualizaciones.",
      [12, 40, 62, 90])
