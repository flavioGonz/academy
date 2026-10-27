#!/usr/bin/env python3
"""Lección 31, teoría "La regla de NAT" y "Las condiciones": qué le pasa al encabezado de una consulta DNS redirigida."""
from _anim_mt2739 import escribir, Anim, SITE, PREV, en, ventanas, fijo, paquete, nodo, marca, narr, pill_c, LIGHT, GOLD, MINT

a = Anim(T=25, kicker="MIKROTIK · DNS TRANSPARENTE", title="Redirect: el router cambia el destino y lo deshace a la vuelta")
a.steps([
    "La tele pregunta a 8.8.8.8:53 y entra por el bridge.",
    "dstnat, redirect: el destino pasa a ser el router, puerto 53.",
    "Contesta el resolver del router, con sus estáticas y bloqueos.",
    "A la vuelta el router deshace el cambio: parece 8.8.8.8.",
    "Una consulta que ya iba al router no se toca: !local.",
], still=3)

# ---- fila de equipos
nodo(a, 48, 182, 220, 80, "Tele o DVR", "192.168.88.40", dark=False)
nodo(a, 932, 182, 220, 80, "8.8.8.8", "Google DNS", dark=False)
RX, RY, RW, RH = 410, 172, 380, 132
a.add(a.box(RX, RY, RW, RH, a.INK, rx=18))
a.add(a.text(RX + 22, RY + 34, "MikroTik", 20, "#FFFFFF", a.HEAD, 600))
a.add(a.text(RX + RW - 22, RY + 34, "192.168.88.1", 15, LIGHT, a.MONO, 400, "end"))
for i, s in enumerate(["dstnat · redirect", "resolver · :53"]):
    y = RY + 50 + i * 38
    a.add(a.box(RX + 16, y, RW - 32, 32, a.NAVY2, rx=9) + a.text(RX + 30, y + 22, s, 16, "#FFFFFF", a.MONO, 600))
def hl(i, wins, color, still=0):
    y = RY + 50 + i * 38
    ventanas(a, f'<rect x="{RX + 14}" y="{y - 2}" width="{RW - 28}" height="36" rx="10" fill="none" stroke="{color}" stroke-width="3"/>', wins, still)
hl(0, [(21, 40)], GOLD)
hl(0, [(61, 80)], MINT, still=1)
hl(1, [(41, 60)], MINT)

LY = 338
for x, y0 in ((158, 262), (600, RY + RH), (1042, 262)):
    a.add(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{LY}" stroke="{a.LINE}" stroke-width="3"/>')
a.add(f'<line x1="158" y1="{LY}" x2="600" y2="{LY}" stroke="{a.LINE}" stroke-width="2" stroke-dasharray="4 6"/>')
a.add(f'<line x1="600" y1="{LY}" x2="1042" y2="{LY}" stroke="{a.LINE}" stroke-width="2" stroke-dasharray="2 8"/>')
paquete(a, "a 8.8.8.8:53", [(1, 158, LY), (12, 600, LY), (20, 600, LY)], 1, 21)
en(a, a.arrow(f"M800 {LY - 30} H920", a.BAD, 3, "7 6") + marca(a, 860, LY - 30, ok=False) + a.text(860, LY + 4, "no le llega", 15, a.BAD, a.MONO, 600, "middle"), 22, 60)
paquete(a, "de 8.8.8.8:53", [(62, 600, LY), (74, 158, LY), (79.5, 158, LY)], 62, 79.5, bg=a.OK)
paquete(a, "a 192.168.88.1:53", [(81, 158, LY), (92, 600, LY), (99.5, 600, LY)], 81, 99.5, bg=a.BLUE)
fijo(a, f'<g transform="translate(158 {LY})">' + pill_c(a, "de 8.8.8.8:53", "#FFFFFF", a.OK) + "</g>")

# ---- encabezado del paquete
HX, HY, HW, HH = 48, 380, 560, 210
a.add(a.box(HX, HY, HW, HH, a.WHITE, a.LINE, rx=16))
a.add(a.text(HX + 22, HY + 32, "Encabezado", 18, a.INK, a.HEAD, 600))
TIP = [(0, 40, "consulta"), (40, 80, "respuesta"), (80, 100, "consulta")]
for t0, t1, s in TIP:
    en(a, a.text(HX + HW - 22, HY + 32, s, 15, a.GREY, a.MONO, 600, "end"), t0, t1, still=1 if s == "respuesta" else 0)
for i, lab in enumerate(["origen", "destino"]):
    y = HY + 54 + i * 70
    a.add(a.box(HX + 16, y, HW - 32, 56, a.SLATE, rx=12))
    a.add(a.text(HX + 34, y + 35, lab, 16, a.GREY, a.MONO))
VAL = {  # (fila, t0, t1, texto, color, resaltado, fijo)
    "o": [(0, 40, "192.168.88.40", a.INK, None, 0), (40, 60, "192.168.88.1:53", a.INK, None, 0),
          (60, 80, "8.8.8.8:53", a.OK, a.OK, 1), (80, 100, "192.168.88.40", a.INK, None, 0)],
    "d": [(0, 21, "8.8.8.8:53", a.INK, None, 0), (21, 40, "192.168.88.1:53", a.AMB, a.AMB, 0),
          (40, 80, "192.168.88.40", a.INK, None, 1), (80, 100, "192.168.88.1:53", a.INK, None, 0)],
}
for k, i in (("o", 0), ("d", 1)):
    y = HY + 54 + i * 70
    for t0, t1, s, c, hlc, st in VAL[k]:
        g = a.text(HX + 150, y + 36, s, 20, c, a.MONO, 600)
        if hlc:
            g = f'<rect x="{HX + 14}" y="{y - 2}" width="{HW - 28}" height="60" rx="13" fill="none" stroke="{hlc}" stroke-width="3"/>' + g
        en(a, g, t0, t1, still=st)
en(a, a.text(HX + HW - 34, HY + 54 + 70 + 36, "cambió", 15, a.AMB, a.MONO, 600, "end"), 21, 40)
en(a, a.text(HX + HW - 34, HY + 54 + 36, "deshecho", 15, a.OK, a.MONO, 600, "end"), 61, 80, still=1)

# ---- la regla
QX, QW = 640, 512
a.add(a.box(QX, HY, QW, HH, a.INK, rx=16))
a.add(a.text(QX + 22, HY + 32, "/ip/firewall/nat", 16, LIGHT, a.MONO))
CONDS = ["chain=dstnat action=redirect to-ports=53", "protocol=udp dst-port=53  (y otra tcp)",
         "in-interface-list=LAN", "dst-address-type=!local", "src-address-list=!dns-libre"]
for i, s in enumerate(CONDS):
    y = HY + 66 + i * 28
    a.add(a.text(QX + 22, y, s, 15, "#FFFFFF" if i < 2 else LIGHT, a.MONO, 600 if i < 2 else 400))
    if i >= 2:
        en(a, marca(a, QX + QW - 36, y - 5, ok=True, r=11), 22, 80, still=1)
        if i == 3:
            en(a, marca(a, QX + QW - 36, y - 5, ok=False, r=11) + a.text(QX + QW - 56, y, "ya iba al router", 15, GOLD, a.MONO, 600, "end"), 90, 100)
        else:
            en(a, marca(a, QX + QW - 36, y - 5, ok=True, r=11), 90, 100)

narr(a, [
    (0, 20, "La tele tiene el DNS clavado: no le pregunta al router.", a.TXT),
    (20, 40, "Las tres condiciones se cumplen: el destino cambia por una dirección del router.", a.AMB),
    (40, 60, "Las estáticas, adlists y bloqueos del router pasan a valer para la tele.", a.TXT),
    (60, 80, "La tele ve que le contestó 8.8.8.8. Hacen falta dos reglas: UDP y TCP.", a.OK),
    (80, 100, "dst-address-type=!local deja quietas las consultas que ya iban al router.", a.BLUE),
], y=636, still_idx=3)

escribir(a, f"{SITE}/31-t1.svg", "Redirect de DNS: ida y vuelta",
         "Animación en cinco tiempos. 1: una tele con el DNS clavado manda una consulta de 192.168.88.40 a 8.8.8.8 puerto 53, que entra al router por el bridge. "
         "2: en la cadena dstnat, la regla redirect cambia el destino por 192.168.88.1 puerto 53; se cumplen in-interface-list=LAN, dst-address-type=!local y src-address-list=!dns-libre; 8.8.8.8 no recibe nada. "
         "3: contesta el resolver del router, con sus estáticas y bloqueos: la respuesta sale de 192.168.88.1:53 hacia la tele. "
         "4: a la vuelta el router deshace el cambio y el origen pasa a ser 8.8.8.8:53; la tele cree que le contestó 8.8.8.8. "
         "5: una consulta que ya iba a 192.168.88.1 no cumple dst-address-type=!local y no se toca. Hacen falta dos reglas, UDP y TCP.",
         [8, 30, 50, 70, 95], f"{PREV}/_t31")
