#!/usr/bin/env python3
"""Lección 11 · teoría: restaurar en otro controlador (t1) y las etapas de una actualización (t2)."""
from _anim_unifi import *  # noqa

# ---------------- t1: restaurar con otra IP
a = new(24, "Backup y etapas", "Restaurar en otro controlador, con otra IP", [
    "El backup lleva configuración, dispositivos y clientes. Ni video ni logs.",
    "Se restaura en la misma versión o superior, y se entra con el usuario del backup.",
    "Los equipos siguen buscando la URL de inform vieja: aparecen offline.",
    "Option 43, DNS o set-inform con la IP nueva: vuelven a conectarse.",
], still=3)

OX, OY = 48, 196
a.add(node(a, OX, OY, 300, 96, "Controlador viejo", "Network 10.6", ssize=14, sub2="URL de inform vieja"))
vis(a, a.box(OX, OY, 300, 96, A.SLATE, A.GREY, rx=14) + a.text(OX + 20, OY + 40, "Controlador viejo", 20, A.GREY, A.HEAD, 600)
    + a.text(OX + 20, OY + 66, "ya no está", 15, A.BAD, A.MONO, 600), 2, 3)
BX, BY = 420, 190
a.add(a.box(BX, BY, 330, 210, A.WHITE, A.LINE, rx=14))
a.add(a.text(BX + 20, BY + 34, "Backup .unf", 20, A.INK, A.HEAD, 600))
for k, t in enumerate(["configuración", "dispositivos", "clientes"]):
    a.add(check(a, BX + 32, BY + 64 + k * 30, 10) + a.text(BX + 52, BY + 69 + k * 30, t, 15, A.TXT, A.MONO))
for k, t in enumerate(["video de Protect", "logs locales"]):
    a.add(xmark(a, BX + 32, BY + 154 + k * 30, 10) + a.text(BX + 52, BY + 159 + k * 30, t, 15, A.GREY, A.MONO))
NX = 830
a.add(node(a, NX, 190, 322, 96, "Controlador nuevo", "10.6 o superior", ssize=14, sub2="IP nueva"))
a.add(node(a, NX, 306, 322, 76, "Controlador más viejo", "versión anterior", ssize=14))

# equipos
DEV = [(330, "AP 1"), (560, "AP 2"), (790, "Switch")]
DY = 500
for x, n in DEV:
    a.add(node(a, x, DY, 200, 66, n, None))
for i, (lab, kind) in enumerate([("conectado", "ok"), ("conectado", "ok"), ("offline", "bad"), ("conectado", "ok")]):
    for x, n in DEV:
        vis(a, pill(a, x + 100, DY + 80, lab, kind, anchor="middle"), i)

# 1
s0, s1 = ph(a, 0)
token(a, [(OX + 300, 244), (BX - 10, 244)], s0 + 2, s0 + 10, "backup", bg=A.BLUE, hold=s0 + 11)
# 2
s0, s1 = ph(a, 1)
token(a, [(BX + 330, 230), (NX - 60, 230)], s0 + 2, s0 + 8, "restore", bg=A.BLUE, hold=s1 - 1)
token(a, [(BX + 330, 330), (NX - 60, 344)], s0 + 9, s0 + 14, "restore", bg=A.GREY, hold=s1 - 1)
vis(a, check(a, NX + 300, 214, 13), 1, 3)
vis(a, xmark(a, NX + 300, 330, 13), 1)
vis(a, pill(a, NX, 400, "entrás con el usuario del backup", "info"), 1)
# 3
s0, s1 = ph(a, 2)
for k, (x, n) in enumerate(DEV):
    token(a, [(x + 100, DY - 10), (OX + 50 + k * 95, OY + 124)], s0 + 2 + k * 2, s0 + 9 + k * 2, "inform", bg=A.CYAN, hold=s1 - 1)
vis(a, xmark(a, OX + 40, OY + 166, 14) + a.text(OX + 62, OY + 172, "nadie contesta", 15, A.BAD, A.MONO, 600), 2)
# 4
s0, s1 = ph(a, 3)
vis(a, pill(a, 585, 434, "option 43 · DNS · set-inform → IP nueva", "ok", anchor="middle"), 3)
for k, (x, n) in enumerate(DEV):
    token(a, [(x + 100, DY - 10), (790, 214 + k * 30)], s0 + 3 + k * 2, s0 + 10 + k * 2, "inform", bg=A.OK, hold=s1 - 1, still=1)

write(a, "11-t1.svg", "Restaurar un backup de UniFi con otra IP", mid_pcts(a))

# ---------------- t2: etapas en el tiempo
b = new(25, "Backup y etapas", "Actualizar por etapas: el riesgo, repartido en el tiempo", [
    "Backup antes de tocar nada: es el punto de vuelta atrás.",
    "Sale una versión Official: las notas dicen si el salto es posible.",
    "2 a 3 semanas de espera: otros encuentran las fallas antes que vos.",
    "Piloto: un solo sitio, con alguien atento.",
    "Recién después, el resto de los sitios, por tandas.",
], still=4)
AX0, AX1, AY = 60, 1140, 520
b.add(line(b, [(AX0, AY), (AX1, AY)], A.GREY, 3, arrow=True))
b.add(b.text(AX1, AY + 30, "tiempo", 14, A.GREY, A.MONO, anchor="end"))
CARDS = [(48, 200, "Backup", "dos copias", "fuera del equipo", A.OK),
         (268, 200, "Notas", "solo Official", "qué pide y qué saca", A.BLUE),
         (488, 220, "Espera", "2 a 3 semanas", "foros y pruebas", A.AMB),
         (728, 200, "Piloto", "un sitio", "con alguien atento", A.AMB),
         (948, 204, "El resto", "por tandas", "después del piloto", A.OK)]
for i, (x, w, t, s1_, s2_, col) in enumerate(CARDS):
    c = b.box(x, 230, w, 120, A.WHITE, A.LINE, rx=14) + f'<rect x="{x}" y="230" width="{w}" height="6" rx="3" fill="{col}"/>'
    c += b.text(x + 18, 270, f"{i + 1}. {t}", 19, A.INK, b.HEAD, 600) + b.text(x + 18, 298, s1_, 15, A.TXT, A.MONO) + b.text(x + 18, 322, s2_, 15, A.TXT, A.MONO)
    c += line(b, [(x + w / 2, 350), (x + w / 2, AY - 8)], A.LINE, 2) + f'<circle cx="{x + w / 2}" cy="{AY}" r="8" fill="{col}"/>'
    vis(b, c, i, 4)
    vis(b, b.box(x, 230, w, 120, "none", col, rx=14, sw=3), i)
# banda de espera
vis(b, b.box(488, AY - 10, 220, 20, b.AMBBG, A.AMB, rx=10, sw=1.5), 2, 4)
# notas al pie de cada tiempo
vis(b, note(b, 48, 580, 1104, "Si algo sale mal, el backup es el camino de vuelta.", "ok", size=16, h=44), 0)
vis(b, note(b, 48, 580, 1104, "Ejemplo: Network 11 pide UniFi OS 6.0, migra a PostgreSQL y borra el historial de estadísticas.", "info", size=16, h=44), 1)
vis(b, note(b, 48, 580, 1104, "Así HostiFi salteó la 7.5.174, que tenía redes WiFi que no se emitían.", "amb", size=16, h=44), 2)
vis(b, note(b, 48, 580, 1104, "Si el piloto muestra un problema, aparece en un solo cliente.", "amb", size=16, h=44), 3)
vis(b, note(b, 48, 580, 1104, "Antes de actualizar, backup, siempre, y un sitio piloto antes que el resto.", "ok", size=16, h=44), 4)
# sitios
b.add(b.text(728, 392, "sitios de clientes", 14, A.GREY, A.MONO))
SITES = [728 + k * 70 for k in range(6)]
for k, x in enumerate(SITES):
    b.add(b.box(x, 404, 56, 40, A.SLATE, A.LINE, rx=8, sw=1.5))
    on = 3 if k == 0 else 4
    s0, _ = ph(b, on)
    t = s0 + 3 + (0 if k == 0 else (k - 1) * 2.5)
    b.add(b.group(b.box(x, 404, 56, 40, A.OK if k else A.AMB, rx=8) + b.text(x + 28, 430, "ok" if k else "piloto", 13 if not k else 15, A.WHITE, A.MONO, 600, "middle"),
                  b.show(t, 100), still=1))
# la versión que avanza
b.add(b.group(b.pill(-60, -14, "versión", A.WHITE, A.BLUE, 14), b.move([(0, 148, AY - 40), (20, 148, AY - 40), (24, 368, AY - 40), (40, 368, AY - 40),
              (56, 598, AY - 40), (60, 598, AY - 40), (64, 828, AY - 40), (80, 828, AY - 40), (84, 1050, AY - 40), (100, 1050, AY - 40)]), still=0))

write(b, "11-t2.svg", "Actualizar UniFi por etapas", mid_pcts(b))
