#!/usr/bin/env python3
"""Teoría lección 3 (Adopción limpia): los cuatro momentos de la adopción y en cuál se corta según el mensaje.
Salida: site2/ilustraciones/omada/3-t1.svg"""
import sys
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _anim_omada import *  # noqa

a = nueva(24, "ADOPCIÓN", "El síntoma dice en qué momento se cortó")
F = a.steps([
    "Adopción completa: anuncio, respuesta, adopción y gestión.",
    "Nunca aparece en Devices: el anuncio no llegó.",
    "Aparece, pero falla con usuario o clave: el equipo ya tenía dueño.",
    "Aparece, pero no responde a los comandos: el camino está roto.",
], still=2)

BX, BW, BH, GAP, BY = 48, 250, 104, 24, 184
M = [("1", "Anuncio", "broadcast UDP 29810"), ("2", "Respuesta", "queda en Pending"),
     ("3", "Adopción", "Device Account"), ("4", "Gestión", "queda Connected")]
CXS = [BX + i * (BW + GAP) + BW / 2 for i in range(4)]
for i, (n, t, s) in enumerate(M):
    x = BX + i * (BW + GAP)
    a.add(a.box(x, BY, BW, BH, a.WHITE, a.LINE))
    a.add(f'<circle cx="{x + 34}" cy="{BY + 36}" r="16" fill="{a.SLATE}"/>' + a.text(x + 34, BY + 42, n, 16, a.INK, a.MONO, 600, "middle"))
    a.add(a.text(x + 60, BY + 43, t, 20, a.INK, a.HEAD, 600))
    a.add(a.text(x + 20, BY + 80, s, 15, a.GREY, a.MONO))
    if i < 3:
        a.add(a.arrow(f"M{x + BW + 3} {BY + BH / 2} H{x + BW + GAP - 3}", a.GREY, 2.5))

# carril del equipo
TY = 330
a.add(linea(a, CXS[0], TY, CXS[3], TY, a.LINE, 3, "4 8"))
a.add(a.text(BX, TY + 5, "EAP", 15, a.GREY, a.MONO))


def token(i0, i1, t0, t1, end, still=0):
    """el EAP recorre del momento i0 al i1 entre t0 y t1, y queda quieto hasta 'end'."""
    mv = a.move([(0, CXS[i0], TY), (t0, CXS[i0], TY), (t1, CXS[i1], TY), (100, CXS[i1], TY)])
    a.add(a.group(eap(a, 0, 0, 22), mv, a.show(t0, end, 0.6), still=still))


def marca(i, kind, t0, t1, still=0):
    x = BX + i * (BW + GAP)
    col = a.OK if kind == "ok" else a.BAD
    inner = a.box(x, BY, BW, BH, "none", col, rx=14, sw=3) + (ok if kind == "ok" else bad)(a, x + BW - 30, BY + 36, 14)
    en(a, inner, t0, t1, still)


# fase 1: todo verde
s0, e0 = F[0]
token(0, 3, s0 + 3, s0 + 19, e0)
for i in range(4):
    marca(i, "ok", s0 + 3 + i * 5.3, e0)
# fase 2: se corta en el anuncio
s1, e1 = F[1]
token(0, 0, s1, s1 + 1, e1)
marca(0, "bad", s1 + 5, e1)
# fases 3 y 4: se corta en la adopción
for k, st in ((2, 1), (3, 0)):
    s, e = F[k]
    token(0, 2, s + 1, s + 10, e)
    marca(0, "ok", s + 2, e, st)
    marca(1, "ok", s + 6, e, st)
    marca(2, "bad", s + 11, e, st)

solo_fijo(a, eap(a, CXS[2], TY, 22))

# panel de diagnóstico
PY, PH = 380, 200
a.add(a.box(48, PY, 1104, PH, a.WHITE, a.LINE))
a.add(a.text(72, PY + 36, "Qué ves", 15, a.GREY, a.MONO, 400, extra='letter-spacing="1.5"'))
a.add(a.text(440, PY + 36, "Qué pasó", 15, a.GREY, a.MONO, 400, extra='letter-spacing="1.5"'))
a.add(a.text(808, PY + 36, "Qué revisar", 15, a.GREY, a.MONO, 400, extra='letter-spacing="1.5"'))
a.add(linea(a, 420, PY + 20, 420, PY + PH - 20, a.LINE, 2))
a.add(linea(a, 788, PY + 20, 788, PY + PH - 20, a.LINE, 2))


def col(x, y, lines, color=None, size=17, w=600):
    return "".join(a.text(x, y + i * 26, ln, size, color or a.TXT, a.SANS, w if i == 0 else 400) for i, ln in enumerate(lines))


DIAG = [
    (chip(a, 72, PY + 58, "Connected", a.OK, a.OKBG, stroke=a.OK) + col(72, PY + 124, ["Las credenciales de fábrica", "se reemplazan por las de", "Device Account."], a.TXT, 16, 400),
     col(440, PY + 76, ["Los cuatro momentos pasaron.", "El controlador cargó la", "configuración del sitio y la", "web local dejó de mandar."], a.INK),
     col(808, PY + 76, ["Nada: el equipo se gestiona", "desde el controlador."], a.OK)),
    (chip(a, 72, PY + 58, "no aparece en Devices", a.BAD, a.BADBG, stroke=a.BAD),
     col(440, PY + 76, ["El broadcast no llegó: el", "equipo está en otra VLAN", "o en otra subred."], a.INK),
     col(808, PY + 76, ["La VLAN, o uno de los", "métodos para otra subred."], a.INK)),
    (chip(a, 72, PY + 58, "username or password", a.BAD, a.BADBG, stroke=a.BAD) + chip(a, 72, PY + 96, "is incorrect", a.BAD, a.BADBG, stroke=a.BAD),
     col(440, PY + 76, ["El equipo ya tenía dueño:", "lo configuraron por su web", "o estaba en otro controlador."], a.INK),
     col(808, PY + 76, ["Retry con la clave de la web", "local, o la Device Account", "del otro controlador."], a.INK)),
    (chip(a, 72, PY + 58, "does not respond", a.BAD, a.BADBG, stroke=a.BAD) + chip(a, 72, PY + 96, "to adopt commands", a.BAD, a.BADBG, stroke=a.BAD),
     col(440, PY + 76, ["El camino está roto en algún", "punto entre el equipo y el", "controlador."], a.INK),
     col(808, PY + 76, ["Tags de VLAN hasta el DHCP,", "un loop o un firewall. En una", "PC, su firewall o antivirus."], a.INK)),
]
for i, parts in enumerate(DIAG):
    fase(a, "".join(parts), F, i, still=1 if i == 2 else 0)

pie(a, F, [
    "Cada momento depende del anterior.",
    "El reset es el último recurso: borra también lo que hacía falta conservar.",
    "El reset es el último recurso: borra también lo que hacía falta conservar.",
    "El reset es el último recurso: borra también lo que hacía falta conservar.",
], y=630, still=2, colores=[a.INK, a.AMB, a.AMB, a.AMB])

salida(a, 3, 1, "El síntoma dice en qué momento se cortó la adopción",
       "Animación en cuatro tiempos sobre los cuatro momentos de la adopción: anuncio por broadcast al UDP 29810, respuesta y Pending, "
       "adopción con Device Account y gestión en Connected. 1: el EAP pasa los cuatro y queda Connected; las credenciales de fábrica se "
       "reemplazan por las de Device Account. 2: el equipo nunca aparece en Devices porque el anuncio no llegó; está en otra VLAN o subred. "
       "3: aparece pero falla con username or password is incorrect porque ya tenía dueño; se resuelve con Retry y la clave de la web local "
       "o la Device Account del otro controlador. 4: aparece pero does not respond to adopt commands porque el camino está roto: tags de "
       "VLAN, un loop o un firewall. El reset queda como último recurso.",
       [12, 37, 62, 88])
