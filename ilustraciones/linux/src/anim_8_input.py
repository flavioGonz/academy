"""Teoría lección 8: la cadena input con policy drop; la primera regla que coincide decide."""
from _alnx import *

a = new(24, "La cadena input: la primera regla que coincide")
a.steps(["Respuesta de un apt update: ct state established, pasa.",
         "SSH desde 10.10.10.25: coincide la regla de gestión, pasa.",
         "SSH desde 203.0.113.7: ninguna regla, policy drop.",
         "Ping desde la red: icmp echo-request, pasa."], still=2)

rules = ["ct state established,related accept", "iif lo accept", "ip saddr 10.10.10.0/24 tcp dport 22 accept",
         "icmp type echo-request accept", "meta l4proto ipv6-icmp accept"]
RX, RY, RW, RH = 400, 196, 560, 50
a.add(a.box(RX - 20, 160, RW + 40, 40 + len(rules) * (RH + 8) + 64, a.WHITE, a.LINE, rx=16))
a.add(mono(a, RX, 186, "chain input { policy drop; }", 15, a.GREY, 600))
for i, r in enumerate(rules):
    y = RY + 8 + i * (RH + 8)
    a.add(a.box(RX, y, RW, RH, a.SLATE, None, rx=10) + mono(a, RX + 16, y + 32, r, 15, a.INK, 600))
YP = RY + 8 + len(rules) * (RH + 8)
a.add(a.box(RX, YP, RW, RH, a.BADBG, a.BAD, rx=10, sw=2) + mono(a, RX + 16, YP + 32, "(ninguna coincide) policy drop", 15, a.BAD, 700))

pk = [("respuesta apt", 0, a.BLUE), ("10.10.10.25:22", 2, a.OK), ("203.0.113.7:22", None, a.BAD), ("ping", 3, a.CYAN)]
for k, (lab, hit, col) in enumerate(pk):
    t0 = k * 25
    yh = (RY + 8 + hit * (RH + 8) + RH / 2) if hit is not None else YP + RH / 2
    # el paquete entra por la izquierda, baja por las reglas y sale a la derecha (o se descarta)
    pts = [(0, 140, 230), (t0, 140, 230), (t0 + 6, 200, yh), (t0 + 12, 200, yh)]
    if hit is not None:
        pts += [(t0 + 20, 1070, yh), (100, 1070, yh)]
    else:
        pts += [(t0 + 20, 200, yh), (100, 200, yh)]
    a.add(a.group(pkt(a, lab, col), a.move(pts), a.show(t0 + 0.5, t0 + 23), still=0))
    rowy = yh - RH / 2
    kind_col = a.BAD if hit is None else a.OK
    at(a, a.box(RX, rowy, RW, RH, "none", kind_col, rx=10, sw=3), t0 + 9, t0 + 25, 1 if k == 2 else 0)
    if hit is not None:
        at(a, chip(a, RX + RW - 10, int(yh) - 15, "accept", "ok", anchor="end"), t0 + 14, t0 + 25, 0)
at(a, chip(a, 200, int(YP + RH / 2) + 22, "descartado", "bad", anchor="middle"), 63, 75, 1)
# fuente del 3 en el fijo
a.add(a.group(f'<g transform="translate(200 {YP + RH / 2})">{pkt(a, "203.0.113.7:22", a.BAD)}</g>', a.keyframes([(0, 0), (100, 0)]), still=1))

caption(a, 622, [(0, 25, "La primera regla deja pasar las respuestas de lo que el propio equipo pidió.", None),
                 (25, 50, "SSH entra solo desde la red de gestión: el origen está en la regla.", a.OK),
                 (50, 75, "Lo que no coincide con ninguna regla cae en la política: drop.", a.BAD),
                 (75, 100, "ICMP y ICMPv6 se permiten: sin ICMPv6, IPv6 no funciona.", None)], still=2)
write(a, "8-t1.svg", "La cadena input: la primera regla que coincide",
      "Animación en cuatro tiempos sobre la cadena input con policy drop y cinco reglas en orden: ct state established,related accept; iif lo accept; ip saddr 10.10.10.0/24 tcp dport 22 accept; icmp type echo-request accept; meta l4proto ipv6-icmp accept; y abajo, en rojo, la política drop. "
      "1: llega la respuesta de un apt update, coincide con la primera regla y pasa. 2: llega SSH desde 10.10.10.25, baja hasta la regla de la red de gestión y pasa. "
      "3: llega SSH desde 203.0.113.7, no coincide con ninguna regla y cae en la política: descartado. 4: llega un ping, coincide con la regla de echo-request y pasa. El cuadro fijo muestra el tiempo 3.")
