#!/usr/bin/env python3
"""Lección 1 · Resumen, "Cómo se ve en la red": llegás a la obra, te enchufás en ether1 (WAN) y no ves nada;
pasás a ether2 (LAN), el router se anuncia, entrás por la MAC y sacás el export inicial.
Fuentes: defconf (discover-interface-list=LAN, mac-winbox allowed-interface-list=LAN, input "drop all not coming from LAN")."""
from _anim_red_1_9 import *

a = Anim(T=24, kicker="MIKROTIK · ENTRAR SIN ROMPER · CÓMO SE VE EN LA RED", title="En ether1 el router no te ve; en ether2 entrás")
a.steps([
    "Te enchufás en ether1: es la WAN. No aparece en Neighbors y no te deja entrar.",
    "Pasás a ether2, en el bridge LAN: el router se anuncia y aparece en Neighbors.",
    "Clic en la MAC y Connect: la sesión de WinBox abre sin depender de la IP.",
    "Antes de tocar nada: /export file=inicial y el archivo va al legajo del cliente.",
], still=2)

# ---------- router con puertos
RX, RY, RW, RH = 48, 186, 440, 176
a.add(a.box(RX, RY, RW, RH, a.INK, rx=18))
a.add(a.text(RX + 22, RY + 36, "hAP de la obra", 20, a.WHITE, a.HEAD, 600))
a.add(a.text(RX + 22, RY + 60, "configuración por defecto", 15, SKY, a.MONO))
PW, PG, PY0 = 72, 10, RY + 118
PX = [RX + 20 + i * (PW + PG) for i in range(5)]
a.add(a.box(PX[0], RY + 80, PW, 28, "#3A1F1A", rx=8))
a.add(a.text(PX[0] + PW / 2, RY + 99, "WAN", 15, "#FF9E8A", a.MONO, 600, "middle"))
a.add(a.box(PX[1], RY + 80, PX[4] + PW - PX[1], 28, a.NAVY2, rx=8))
a.add(a.text((PX[1] + PX[4] + PW) / 2, RY + 99, "bridge · lista LAN", 15, MINT, a.MONO, 600, "middle"))
for i, x in enumerate(PX):
    a.add(a.box(x, PY0, PW, 40, "#12385C", rx=8))
    a.add(a.text(x + PW / 2, PY0 + 26, f"ether{i + 1}", 15, a.WHITE, a.MONO, 600, "middle"))
# puerto activo resaltado
a.add(during(a, a.box(PX[0] - 3, PY0 - 3, PW + 6, 46, "none", "#FF9E8A", rx=10, sw=3), 0, 25))
a.add(during(a, a.box(PX[1] - 3, PY0 - 3, PW + 6, 46, "none", MINT, rx=10, sw=3), 25, 100, still=1))

# ---------- notebook y cables
NX, NY, NW, NH = 60, 474, 380, 96
a.add(dev(a, NX, NY, NW, NH, "Notebook del técnico", "WinBox", icon="laptop"))
P1, P2 = PX[0] + PW / 2, PX[1] + PW / 2
C1 = ((P1, PY0 + 40), (P1 + 40, NY))
C2 = ((P2, PY0 + 40), (P2 + 40, NY))
a.add(during(a, line(*C1[0], *C1[1], a.BLUE, 4), 0, 25))
a.add(during(a, line(*C2[0], *C2[1], a.BLUE, 4), 25, 100, still=1))
a.add(during(a, a.text(NX + 62, NY + 80, "Neighbors: vacío", 15, a.BAD, a.MONO, 600), 4, 25))
a.add(during(a, a.text(NX + 62, NY + 80, "Neighbors: 1 equipo", 15, a.OK, a.MONO, 600), 36, 76, still=1))


def up(p0, p1, f):
    return (p1[0] + (p0[0] - p1[0]) * f, p1[1] + (p0[1] - p1[1]) * f)


# 1 · ether1: por IP y por MAC, nada
a.add(travel(a, pkt(a, "TCP 8291", a.AMB, size=15), [up(*C1, .1), up(*C1, .62)], 5, 9, hold=6))
a.add(during(a, xmark(a, P1 + 102, 393), 9, 15))
a.add(travel(a, pkt(a, "MAC-WinBox", a.AMB, size=15), [up(*C1, .1), up(*C1, .62)], 15, 19, hold=6))
a.add(during(a, xmark(a, P1 + 102, 393), 19, 25))
# 2 · ether2: anuncio MNDP
a.add(travel(a, pkt(a, "MNDP", a.BLUE, size=15), [up(*C2, .9), up(*C2, .25)], 29, 35, hold=2))
# 3 · clic en la MAC
a.add(travel(a, pkt(a, "MAC-WinBox", a.OK, size=15), [up(*C2, .1), up(*C2, .62)], 53, 58, hold=17))
a.add(still_only(a, place(a, pkt(a, "MAC-WinBox", a.OK, size=15), *up(*C2, .62))))
a.add(during(a, check(a, RX + RW - 30, RY + 30), 58, 100, still=1))
# 4 · el export baja a la notebook
a.add(travel(a, pkt(a, "inicial.rsc", a.CYAN, size=15), [up(*C2, .9), up(*C2, .25)], 80, 87, hold=11))

# ---------- panel derecho (cambia con el paso)
PX0, PY_, PWd, PH = 540, 186, 612, 392
a.add(a.box(PX0, PY_, PWd, PH, a.WHITE, a.LINE, rx=18))

# paso 1: por qué no
p1 = a.text(PX0 + 24, PY_ + 40, "Por qué en ether1 no entrás", 20, a.BAD, a.HEAD, 600)
rows = [
    ("/ip/neighbor/discovery-settings", "discover-interface-list=LAN", "Solo se anuncia en la LAN: en ether1 no aparece."),
    ("/tool/mac-server/mac-winbox", "allowed-interface-list=LAN", "Por la MAC, solo desde un puerto de la LAN."),
    ("/ip/firewall/filter · input", "drop all not coming from LAN", "Por IP, el pedido a 8291 se descarta."),
]
for i, (m1, m2, t) in enumerate(rows):
    y = PY_ + 64 + i * 104
    p1 += a.box(PX0 + 20, y, PWd - 40, 92, a.BADBG, rx=10)
    p1 += a.text(PX0 + 38, y + 28, m1, 15, a.INK, a.MONO, 600)
    p1 += a.text(PX0 + 38, y + 51, m2, 15, a.BAD, a.MONO, 600)
    p1 += a.text(PX0 + 38, y + 76, t, 15, a.INK, a.SANS)
a.add(during(a, p1, 0, 25))

# pasos 2 y 3: Neighbors
p2 = a.text(PX0 + 24, PY_ + 40, "WinBox · pestaña Neighbors", 20, a.INK, a.HEAD, 600)
TY = PY_ + 64
p2 += a.box(PX0 + 20, TY, PWd - 40, 36, a.SLATE, rx=8)
p2 += a.text(PX0 + 38, TY + 24, "MAC", 15, a.GREY, a.MONO)
p2 += a.text(PX0 + 260, TY + 24, "IP", 15, a.GREY, a.MONO)
p2 += a.text(PX0 + 420, TY + 24, "IDENTITY", 15, a.GREY, a.MONO)
row = a.box(PX0 + 20, TY + 44, PWd - 40, 42, a.WHITE, a.BLUE, rx=8)
row += a.text(PX0 + 38, TY + 71, "AA:BB:CC:00:11:22", 15, a.INK, a.MONO, 600)
row += a.text(PX0 + 260, TY + 71, "192.168.88.1", 15, a.TXT, a.MONO)
row += a.text(PX0 + 420, TY + 71, "MikroTik", 15, a.TXT, a.MONO)
row += a.text(PX0 + 24, TY + 118, "El anuncio MNDP llega porque ether2 está en la lista LAN.", 15, a.TXT, a.SANS)
a.add(during(a, p2, 25, 75, still=1))
a.add(during(a, row, 36, 75, still=1))
a.add(during(a, a.box(PX0 + 28, TY + 49, 176, 32, "none", a.OK, rx=6, sw=2.5), 47, 75, still=1))
conn = (a.box(PX0 + 20, TY + 148, PWd - 40, 132, a.OKBG, rx=10)
        + a.text(PX0 + 38, TY + 178, "Connect To: AA:BB:CC:00:11:22", 15, a.INK, a.MONO, 600)
        + a.text(PX0 + 38, TY + 204, "Login: admin", 15, a.INK, a.MONO, 600)
        + a.text(PX0 + 38, TY + 236, "Sesión abierta. Por la MAC no importa qué IP", 15, a.OK, a.SANS, 600)
        + a.text(PX0 + 38, TY + 258, "tenga el router ni si alguien la cambió.", 15, a.OK, a.SANS, 600))
a.add(during(a, conn, 58, 75, still=1))

# paso 4: export
p4 = a.text(PX0 + 24, PY_ + 40, "La foto de cómo estaba", 20, a.INK, a.HEAD, 600)
p4 += term(a, PX0 + 20, PY_ + 64, PWd - 40, ["/export file=inicial", "/file/print"], size=15)
p4 += a.box(PX0 + 20, PY_ + 162, PWd - 40, 42, a.SLATE, rx=8)
p4 += a.text(PX0 + 38, PY_ + 189, "inicial.rsc", 15, a.INK, a.MONO, 600)
p4 += a.text(PX0 + PWd - 38, PY_ + 189, "script · texto", 15, a.GREY, a.MONO, 400, "end")
p4 += a.text(PX0 + 24, PY_ + 240, "WinBox, Files: lo arrastrás a la notebook.", 15, a.TXT, a.SANS)
p4 += a.text(PX0 + 24, PY_ + 264, "Si después algo deja de andar, comparás contra este archivo.", 15, a.TXT, a.SANS)
a.add(during(a, p4, 77, 100))
a.add(during(a, a.text(NX + 62, NY + 80, "legajo: inicial.rsc", 15, a.BLUE, a.MONO, 600), 87, 100))

status(a, 628, [
    (0, 25, "ether1 es WAN: ni el anuncio, ni la MAC, ni el puerto 8291 funcionan desde ahí.", a.BAD, 0),
    (25, 50, "En ether2 el router se anuncia por MNDP: lo ves con su MAC aunque no conozcas su IP.", a.BLUE, 0),
    (50, 75, "Por la MAC, WinBox habla en capa 2 con el router: alcanza con estar en el mismo segmento.", a.OK, 1),
    (75, 100, "Primero el export: el estado de partida queda por escrito antes del primer cambio.", a.INK, 0),
])

write(a, 1, "r1", "Entrar sin romper: de ether1 a ether2",
      "Animación en cuatro tiempos con el hAP de la obra (ether1 WAN, ether2 a ether5 en el bridge de la lista LAN) y la notebook del técnico con WinBox. "
      "1: la notebook está en ether1. No aparece nada en Neighbors porque el router solo se anuncia en la lista LAN (discover-interface-list=LAN); "
      "el intento por MAC no entra porque mac-winbox solo escucha en la lista LAN, y el intento por IP al puerto 8291 lo descarta la regla de input drop all not coming from LAN. "
      "2: la notebook pasa a ether2; llega el anuncio MNDP y en Neighbors aparece el equipo con MAC AA:BB:CC:00:11:22, IP 192.168.88.1 e identidad MikroTik. "
      "3: clic en la MAC, usuario admin y Connect: la sesión abre en capa 2, sin depender de la IP. "
      "4: antes del primer cambio, /export file=inicial deja inicial.rsc en Files y el archivo baja a la notebook para el legajo del cliente.",
      [6, 18, 33, 62, 88])
