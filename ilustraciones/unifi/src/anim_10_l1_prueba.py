#!/usr/bin/env python3
"""Lección 10 · Laboratorio, paso 5: la prueba desde el celular. Con el voucher, internet abre (SYN, SYN-ACK);
hacia la impresora de Staff (10.10.10.50:80) el SYN llega al gateway y no vuelve nada; el celular reintenta y se
vence el tiempo. Fuentes: lab.md (pasos 4 y 5) y theory_md de la lección (Post-Authorization Restrictions con
10.0.0.0/8, 172.16.0.0/12 y 192.168.0.0/16; Hotspot hacia Internal es Allow Return); RFC 9293 (inicio de TCP)."""
from _anim_red_unifi import *  # noqa

a = new(24, "Invitados aislados", "La prueba del celular: internet sí, la impresora no", [
    "Con el voucher, el celular navega: SYN, SYN-ACK y la página abre.",
    "Abre http://10.10.10.50: el SYN llega al gateway y ahí se queda.",
    "El celular reintenta: nadie contesta, ni siquiera un rechazo.",
    "Se vence el tiempo: así se ve un invitado aislado.",
], still=3, paso=5)

CL, GW, NET, PR = 150, 470, 800, 1060
a.add(dev(a, 48, 180, 210, 86, "Celular", "voucher OK", icon="phone"))
a.add(dev(a, 350, 180, 240, 86, "Gateway", "zona Hotspot", icon="server", dark=True))
a.add(dev(a, 680, 180, 240, 86, "Internet", "203.0.113.80", icon="globe"))
a.add(dev(a, 952, 180, 200, 86, "Impresora", "10.10.10.50", icon="server"))
for x in (CL, GW, NET, PR):
    lifeline(a, x, 266, 560)

s0, s1 = ph(a, 0)
msg(a, CL, NET, 312, "SYN · TCP 443", s0 + 2, end=100, still=1)
msg(a, NET, CL, 362, "SYN-ACK", s0 + 9, end=100, still=1, color=a.OK)
during(a, check(a, CL - 30, 362, 13), s0 + 12, 100, still=1)

s0, s1 = ph(a, 1)
msg(a, CL, GW, 420, "SYN → 10.10.10.50:80", s0 + 2, end=100, still=1)
during(a, xmark(a, GW + 24, 420, 15), s0 + 5, 100, still=1)
during(a, nbox(a, 560, 392, 592, 100, "Por qué no pasa", ["10.0.0.0/8 está en las Post-Authorization Restrictions", "y Hotspot hacia Internal es Allow Return."], "info"),
       s0 + 6, 100, still=1)

s0, s1 = ph(a, 2)
for k in range(2):
    msg(a, CL, GW, 470 + k * 44, "SYN (reintento)", s0 + 2 + k * 9, end=100, still=1, color=a.AMB, dash="8 6")
    during(a, xmark(a, GW + 24, 470 + k * 44, 13), s0 + 5 + k * 9, 100, still=1)
during(a, a.text(PR, 520, "nunca le llega", 15, a.GREY, a.MONO, 600, "middle"), s0 + 6, 100, still=1)

s0, s1 = ph(a, 3)
during(a, a.box(48, 580, 380, 40, a.BADBG, None, rx=10) + a.text(238, 606, "navegador: se agotó el tiempo", 16, a.BAD, a.SANS, 600, "middle"),
       s0 + 2, 100, still=1)
during(a, a.text(460, 606, "Si la página de la impresora abre: revisá la zona y el paso 4.", 16, a.INK, a.SANS, 600),
       s0 + 6, 100, still=1)

status(a, 648, [
    (0, 25, "Primero comprobá que el invitado navega: sin eso, la prueba no dice nada.", a.INK, 0),
    (25, 50, "Para el invitado, la red de Staff existe, pero no es alcanzable.", a.INK, 0),
    (50, 75, "Un rechazo sería una respuesta; acá no vuelve nada.", a.AMB, 0),
    (75, 100, "", a.INK, 1),
], size=16)

write(a, 10, "l1", "La prueba del celular en el WiFi de invitados",
      "Animación en cuatro tiempos del paso 5 con el celular ya autorizado con el voucher, el gateway con la red en zona Hotspot, un servidor de internet (203.0.113.80) "
      "y la impresora de Staff en 10.10.10.50. "
      "1: el celular abre una página: manda SYN al puerto TCP 443, vuelve SYN-ACK y navega. "
      "2: abre http://10.10.10.50; el SYN hacia el puerto 80 llega al gateway y se descarta, porque 10.0.0.0/8 está en las Post-Authorization Restrictions "
      "y Hotspot hacia Internal es Allow Return. "
      "3: el celular reintenta el SYN dos veces y nadie contesta, ni siquiera un rechazo; a la impresora nunca le llega. "
      "4: en el navegador se agota el tiempo: así se ve un invitado aislado. Si la página de la impresora abre, hay que revisar la zona Hotspot y las restricciones del paso 4.",
      [12, 40, 64, 92])
