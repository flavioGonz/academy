#!/usr/bin/env python3
"""Lección 4 · Laboratorio, paso 2: desde una PC del sitio, Resolve-DnsName unifi.ui.com (consulta DNS por UDP 53) y
Test-NetConnection unifi.ui.com -Port 443 (SYN y SYN-ACK: TcpTestSucceeded True; si la salida está bloqueada el SYN no
vuelve y da False); después, las reglas de salida: TCP 443 y 8883, UDP 53 y UDP 123. La dirección de unifi.ui.com no
se dibuja: es la que devuelva el DNS. Fuentes: lab.md (paso 2) y theory_md de la lección; RFC 9293 (inicio de TCP)."""
from _anim_red_unifi import *  # noqa

a = new(24, "Muchos sitios", "Probar la salida desde una PC del sitio", [
    "Resolve-DnsName unifi.ui.com: consulta por UDP 53 y vuelve la dirección.",
    "Test-NetConnection -Port 443: SYN y SYN-ACK, la salida está abierta.",
    "Si el firewall bloquea la salida 443, el SYN no vuelve: da False.",
    "Las reglas de salida: TCP 443 y 8883, UDP 53 y UDP 123.",
], still=1, paso=2)

PC, FW, DNS, UI = 150, 450, 760, 1050
a.add(dev(a, 48, 180, 210, 86, "PC del sitio", "PowerShell", icon="laptop"))
a.add(dev(a, 330, 180, 240, 86, "Firewall", "salida del sitio", icon="shield", dark=True))
a.add(dev(a, 640, 180, 240, 86, "Servidor DNS", "UDP 53", icon="server"))
a.add(dev(a, 930, 180, 222, 86, "unifi.ui.com", "TCP 443", icon="cloud"))
for x in (PC, FW, DNS, UI):
    lifeline(a, x, 266, 470)

# 1 · DNS
s0, s1 = ph(a, 0)
msg(a, PC, DNS, 310, "consulta: unifi.ui.com · UDP 53", s0 + 2, end=100, still=1)
msg(a, DNS, PC, 360, "respuesta: su dirección", s0 + 9, end=100, still=1, color=a.OK)
T1 = ["> Resolve-DnsName unifi.ui.com", "  Name: unifi.ui.com · IPAddress: ..."]
during(a, term(a, 48, 492, 640, T1, colors={1: MINT}), s0 + 12, s1)

# 2 · 443 abierto
s0, s1 = ph(a, 1)
msg(a, PC, UI, 410, "SYN · TCP 443", s0 + 2, end=s1, still=1)
msg(a, UI, PC, 452, "SYN-ACK", s0 + 9, end=s1, still=1, color=a.OK)
T2 = ["> Test-NetConnection unifi.ui.com -Port 443", "  TcpTestSucceeded : True"]
during(a, term(a, 48, 492, 640, T2, colors={1: MINT}), s0 + 12, s1, still=1)

# 3 · 443 bloqueado
s0, s1 = ph(a, 2)
msg(a, PC, FW, 410, "SYN · TCP 443", s0 + 2, end=s1, still=0, color=a.AMB, dash="8 6")
during(a, xmark(a, FW + 22, 410, 15), s0 + 5, s1)
during(a, a.text(UI, 452, "no le llega", 15, a.GREY, a.MONO, 600, "middle"), s0 + 6, s1)
T3 = ["> Test-NetConnection unifi.ui.com -Port 443", "  TcpTestSucceeded : False"]
during(a, term(a, 48, 492, 640, T3, colors={1: GOLD}), s0 + 10, s1)

# 4 · reglas de salida
s0, s1 = ph(a, 3)
R = a.box(712, 492, 440, 124, a.WHITE, a.LINE, rx=14) + a.text(732, 522, "Reglas de salida del firewall", 16, a.INK, a.SANS, 600)
for i, (p, d) in enumerate((("TCP 443", "HTTPS"), ("TCP 8883", "MQTT y TLS"), ("UDP 53", "DNS"), ("UDP 123", "NTP"))):
    x = 732 + (i % 2) * 210
    y = 556 + (i // 2) * 34
    R += check(a, x + 10, y - 5, 10) + a.text(x + 28, y, p, 15, a.INK, a.MONO, 600) + a.text(x + 112, y, d, 15, a.TXT, a.SANS)
during(a, R, s0 + 2, 100)
during(a, term(a, 48, 492, 640, ["Sitio que no aparece, en orden:", "Remote Management · 443 y 8883", "DNS y NTP · la cuenta con la que entraste"]),
       s0 + 4, 100)

status(a, 646, [
    (0, 25, "Si el nombre no resuelve, no hay salida que probar: empezá por el DNS.", a.INK, 0),
    (25, 50, "True: la PC sale por 443. Lo mismo tiene que poder la consola.", a.OK, 1),
    (50, 75, "Sin respuesta, la conexión no se arma: el sitio no aparece en Site Manager.", a.BAD, 0),
    (75, 100, "Sin NTP la hora queda mal y TLS no valida: también se revisa.", a.AMB, 0),
], size=16)

write(a, 4, "l1", "Probar la salida desde una PC del sitio",
      "Animación en cuatro tiempos del paso 2 con una PC del sitio en PowerShell, el firewall de salida, un servidor DNS y unifi.ui.com. "
      "1: Resolve-DnsName unifi.ui.com manda la consulta por UDP 53 y vuelve la dirección del nombre. "
      "2: Test-NetConnection unifi.ui.com -Port 443 manda un SYN al puerto 443 y vuelve SYN-ACK: TcpTestSucceeded True, la salida está abierta. "
      "3: si el firewall bloquea la salida 443, el SYN no le llega a unifi.ui.com, no vuelve nada y el resultado es TcpTestSucceeded False; "
      "sin esa salida el sitio no aparece en Site Manager. "
      "4: en las reglas de salida del firewall tienen que estar TCP 443 (HTTPS), TCP 8883 (MQTT sobre TLS), UDP 53 (DNS) y UDP 123 (NTP); "
      "el orden de revisión es Remote Management, 443 y 8883, DNS y NTP, y la cuenta con la que se entró.",
      [12, 40, 64, 92])
