#!/usr/bin/env python3
"""Lección 10 · teoría: portal cautivo con pre y post autorización (t1) y Allow Return + aislamiento (t2)."""
from _anim_unifi import *  # noqa

# ---------------- t1: portal cautivo
a = new(25, "Invitados", "Portal cautivo: antes y después de autorizar", [
    "El invitado se conecta a la red Invitados (zona Hotspot) y abre una página.",
    "Todavía no está autorizado: el gateway lo redirige a la página del portal.",
    "Pre-Authorization Allowances: pasa el dominio que el portal necesita, nada más.",
    "Ingresa el voucher: queda autorizado y sale a internet.",
    "Post-Authorization Restrictions: los rangos privados siguen bloqueados.",
], still=4)

a.add(a.box(48, 290, 220, 110, A.WHITE, A.LINE, rx=14) + phone_icon(a, 84, 330)
      + a.text(112, 326, "Invitado", 20, A.INK, A.HEAD, 600) + a.text(112, 350, "zona Hotspot", 14, A.AMB, A.MONO, 600))
for i, (lab, kind) in enumerate([("abre una página", "grey"), ("ve el portal", "amb"), ("ve el portal", "amb"), ("autorizado", "ok"), ("autorizado", "ok")]):
    vis(a, pill(a, 158, 364, lab, kind, anchor="middle"), i)
GX, GY, GW, GH = 400, 290, 230, 110
a.add(node(a, GX, GY, GW, GH, "Gateway UniFi", "portal · zonas", dark=True, ssize=14))
a.add(line(a, [(268, 345), (GX, 345)], A.LINE, 3))
for i, (lab, kind) in enumerate([("no autorizado", "amb"), ("no autorizado", "amb"), ("no autorizado", "amb"), ("autorizado", "ok"), ("autorizado", "ok")]):
    vis(a, pill(a, GX + GW / 2, GY + GH + 14, lab, kind, anchor="middle"), i)

RX = 840
DEST = [("Página del portal", "voucher · condiciones"), ("Proveedor del portal", "dominio permitido antes"),
        ("Internet", "cualquier sitio"), ("Impresora de Staff", "10.10.10.50 · puerto 80")]
DY = [186, 278, 370, 462]
for (t, s), y in zip(DEST, DY):
    a.add(node(a, RX, y, 312, 72, t, s, ssize=14))
    a.add(line(a, [(GX + GW, 345), (760, 345), (760, y + 36), (RX, y + 36)], A.LINE, 2.5))


def to_dest(t0, idx, lab, col, ok, hold, still=0):
    y = DY[idx] + 36
    token(a, [(200, 312), (GX - 60, 312)], t0, t0 + 3, lab, bg=col, hold=t0 + 3.1)
    token(a, [(GX + GW + 10, 312), (740, 312), (740, y - 30), (RX - 100, y - 30)], t0 + 3.2, t0 + 7, lab, bg=col, hold=hold, still=still)
    a.add(a.group(check(a, RX + 288, y, 14) if ok else xmark(a, RX + 288, y, 14), a.show(t0 + 7, hold, 0.4), still=still))


# 1: abre una página
s0, s1 = ph(a, 0)
token(a, [(200, 312), (GX - 60, 312)], s0 + 3, s0 + 9, "una página", bg=A.CYAN, hold=s1 - 1)
# 2: redirección
s0, s1 = ph(a, 1)
token(a, [(GX - 20, 312), (GX - 60, 312)], s0 + 0.5, s0 + 1, "una página", bg=A.CYAN, hold=s0 + 2)
token(a, [(GX - 10, 378), (330, 430), (200, 430)], s0 + 3, s0 + 10, "redirige al portal", bg=A.AMB, hold=s1 - 1)
vis(a, a.box(RX, DY[0], 312, 72, "none", A.AMB, rx=14, sw=3), 1, 3)
# 3: pre-autorización
s0, s1 = ph(a, 2)
to_dest(s0 + 1, 1, "dominio permitido", A.OK, True, s1 - 1)
to_dest(s0 + 9, 2, "otro sitio", A.GREY, False, s1 - 1)
# 4: voucher e internet
s0, s1 = ph(a, 3)
token(a, [(200, 312), (GX - 60, 312)], s0 + 1, s0 + 5, "voucher", bg=A.BLUE, hold=s0 + 6)
to_dest(s0 + 8, 2, "otro sitio", A.OK, True, s1 - 1)
# 5: post-autorización
s0, s1 = ph(a, 4)
to_dest(s0 + 2, 3, "10.10.10.50", A.CYAN, False, s1 - 1, still=1)
vis(a, a.text(48, 560, "Post-Authorization Restrictions, de fábrica:", 16, A.INK, A.SANS, 600), 4)
for k, r in enumerate(["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]):
    vis(a, pill(a, 48 + k * 190, 576, r, "bad"), 4)
vis(a, a.text(RX, 566, "tiene que vencer el tiempo", 16, A.BAD, A.SANS, 600), 4)
vis(a, note(a, 48, 560, 1104, "Con HTTPS Redirection, el campo Domain hace que la redirección use un nombre que coincida con el certificado.", "info", size=15, h=44), 1)

write(a, "10-t1.svg", "Portal cautivo de invitados en UniFi", mid_pcts(a))

# ---------------- t2: Allow Return y aislamiento
b = new(20, "Invitados", "Allow Return: el invitado contesta, nunca inicia", [
    "Una PC de Internal inicia hacia un invitado: Internal → Hotspot es Allow All.",
    "El invitado contesta esa conexión: Allow Return deja volver la respuesta.",
    "El invitado intenta iniciar hacia Internal: Allow Return lo bloquea.",
    "Client Device Isolation: dos invitados en el mismo AP no se ven.",
], still=2)
b.add(b.text(48, 200, "ZONA INTERNAL", 14, A.BLUE, A.MONO, 600, extra='letter-spacing="1.5"'))
b.add(b.box(40, 212, 340, 320, "none", A.BLUE, rx=16, sw=1.5, extra='stroke-dasharray="6 6"'))
b.add(node(b, 70, 300, 280, 84, "PC de Staff", "10.10.10.x", ssize=14))
b.add(b.text(830, 200, "ZONA HOTSPOT", 14, A.AMB, A.MONO, 600, extra='letter-spacing="1.5"'))
b.add(b.box(820, 212, 340, 320, "none", A.AMB, rx=16, sw=1.5, extra='stroke-dasharray="6 6"'))
for y, n in ((240, "Celular 1"), (424, "Celular 2")):
    b.add(b.box(850, y, 280, 80, A.WHITE, A.LINE, rx=14) + phone_icon(b, 884, y + 40) + b.text(912, y + 36, n, 19, A.INK, A.HEAD, 600)
          + b.text(912, y + 60, "mismo AP", 14, A.GREY, A.MONO))
GX, GY = 480, 290
b.add(node(b, GX, GY, 240, 104, "Gateway UniFi", "Zone Matrix", dark=True, ssize=14))
b.add(line(b, [(350, 342), (GX, 342)], A.LINE, 3))
b.add(line(b, [(GX + 240, 342), (780, 342), (780, 280), (850, 280)], A.LINE, 3))

for i, (lab, kind) in enumerate([("Internal → Hotspot: Allow All", "ok"), ("Hotspot → Internal: respuesta, pasa", "ok"),
                                  ("Hotspot → Internal: inicia, bloqueado", "bad"), ("Client Device Isolation", "info")]):
    vis(b, pill(b, 600, 412, lab, kind, anchor="middle"), i)

s0, s1 = ph(b, 0)
token(b, [(300, 320), (GX - 50, 320)], s0 + 2, s0 + 7, "inicia", bg=A.BLUE, hold=s0 + 7.2)
token(b, [(GX + 280, 320), (760, 320), (760, 258), (790, 258)], s0 + 8, s0 + 14, "inicia", bg=A.BLUE, hold=s1 - 1)
vis(b, check(b, 830, 300, 13), 0)
s0, s1 = ph(b, 1)
token(b, [(790, 258), (760, 258), (760, 320), (GX + 280, 320)], s0 + 2, s0 + 8, "respuesta", bg=A.OK, hold=s0 + 8.2)
token(b, [(GX - 50, 320), (420, 320)], s0 + 9, s0 + 12, "respuesta", bg=A.OK, hold=s1 - 1)
vis(b, check(b, 420, 285, 13), 1)
s0, s1 = ph(b, 2)
token(b, [(790, 258), (760, 258), (760, 320), (GX + 280, 320)], s0 + 2, s0 + 9, "inicia", bg=A.AMB, hold=s1 - 1, still=1)
b.add(b.group(xmark(b, GX + 215, 320, 14), b.show(s0 + 9, s1 - 1, 0.4), still=1))
s0, s1 = ph(b, 3)
token(b, [(990, 334), (990, 380)], s0 + 2, s0 + 7, "inicia", bg=A.AMB, hold=s1 - 1)
vis(b, xmark(b, 1060, 362, 14), 3)
b.add(note(b, 48, 560, 1104, "Tres capas: zona Hotspot, Post-Authorization Restrictions y, opcional, Client Device Isolation.", "info", size=16))

write(b, "10-t2.svg", "Allow Return y aislamiento de invitados", mid_pcts(b))
