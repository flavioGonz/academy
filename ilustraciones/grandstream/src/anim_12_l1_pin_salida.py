#!/usr/bin/env python3
"""Lección 12 (Portero en la central) · Laboratorio, paso 3: Enable DTMF Open Door, Remote PIN y la salida de alarma
en Open Door. El PIN viaja como eventos RFC 4733, el GDS lo compara y activa la salida configurada como Open Door;
si la salida tiene otra función, el PIN se acepta y la puerta no se mueve. Fuentes: la lección (Enable DTMF Open Door,
Remote PIN to Open the Door 4829 de ejemplo, ALMOUT1 en Open Door; aviso de la salida mal configurada; probar con la
puerta abierta o alguien adentro)."""
from _anim_gs_red import R

g = R(T=26, fix=62, kicker="GRANDSTREAM · PORTERO EN LA CENTRAL · LABORATORIO",
      title="Del PIN a la cerradura: la salida tiene que estar en Open Door")
g.steps([
    "Durante la llamada, recepción marca 4829#: cada tecla llega al GDS como evento RFC 4733.",
    "Con Enable DTMF Open Door, el GDS compara con su Remote PIN: coincide.",
    "ALMOUT1 está en Open Door: el GDS activa la salida y la cerradura se libera.",
    "Si ALMOUT1 tiene otra función, el PIN se acepta igual y la puerta no se mueve.",
])

Y, H = 196, 96
YL = Y + H / 2
g.add(g.dev(48, Y, 220, H, "Recepción", "GRP en llamada", icon="tel"))
g.add(g.dev(318, Y, 180, H, "UCM", "8001 ↔ 6000", icon="ucm", dark=True))
GX, GW = 548, 380
g.add(g.box(GX, Y - 10, GW, H + 150, g.WHITE, g.LINE, rx=16))
g.add(g.ico(GX + 16, Y + 4, "door", g.BLUE, 1.3))
g.add(g.text(GX + 60, Y + 26, "GDS3710 · extensión 8001", 18, g.INK, g.HEAD, 600))
g.add(g.wire(268, YL, 318, YL, g.BLUE))
g.add(g.wire(498, YL, GX, YL, g.BLUE))
# comparación
g.add(g.box(GX + 20, Y + 46, GW - 40, 70, g.SLATE, None, rx=10))
g.add(g.text(GX + 36, Y + 72, "Remote PIN to Open the Door", 14, g.GREY, g.MONO))
g.add(g.text(GX + 36, Y + 100, "4829", 20, g.INK, g.MONO, 600))
g.appear(g.text(GX + 120, Y + 100, "recibido:", 15, g.GREY, g.MONO), 6, 100)
for k, d in enumerate("4829#"):
    g.appear(g.text(GX + 210 + k * 18, Y + 100, d, 20, g.BLUE, g.MONO, 600), 8 + k * 3, 100)
g.appear(g.mark(GX + GW - 44, Y + 81, True, 14), 28, 100)
# salida
g.add(g.box(GX + 20, Y + 130, GW - 40, 90, g.SLATE, None, rx=10))
g.add(g.text(GX + 36, Y + 156, "ALMOUT1 Feature", 14, g.GREY, g.MONO))
g.appear(g.text(GX + 36, Y + 186, "Open Door", 20, g.OK, g.MONO, 600), 0, 75)
g.appear(g.text(GX + 36, Y + 186, "otra función", 20, g.BAD, g.MONO, 600), 75, 100)
# contacto del relé
RX0, RY = GX + GW - 120, Y + 176
def contacto(closed, t0, t1, col):
    if closed:
        s = f'<line x1="{RX0}" y1="{RY}" x2="{RX0 + 60}" y2="{RY}" stroke="{col}" stroke-width="5" stroke-linecap="round"/>'
    else:
        s = f'<line x1="{RX0}" y1="{RY}" x2="{RX0 + 54}" y2="{RY - 24}" stroke="{col}" stroke-width="5" stroke-linecap="round"/>'
    s += f'<circle cx="{RX0}" cy="{RY}" r="6" fill="{col}"/><circle cx="{RX0 + 60}" cy="{RY}" r="6" fill="{col}"/>'
    g.appear(s, t0, t1)
contacto(False, 0, 52, g.GREY)
contacto(True, 52, 75, g.OK)
contacto(False, 75, 100, g.GREY)
# cerradura
LX = 1000
g.add(g.box(LX, Y + 90, 152, 120, g.WHITE, g.LINE, rx=14))
g.add(g.ico(LX + 56, Y + 104, "lock", g.BLUE, 1.6))
g.add(g.text(LX + 76, Y + 172, "cerradura", 16, g.INK, g.SANS, 600, "middle"))
g.add(f'<path d="M{RX0 + 66} {RY}H{LX}" stroke="{g.CYAN}" stroke-width="4" fill="none"/>')
g.appear(g.pillc(LX + 76, Y + 226, "trabada", g.GREY, g.SLATE, 13, 26), 0, 54)
g.appear(g.pillc(LX + 76, Y + 226, "se libera", g.OK, g.OKBG, 13, 26), 54, 75)
g.appear(g.pillc(LX + 76, Y + 226, "no se mueve", g.BAD, g.BADBG, 13, 26), 80, 100)

# teclas viajando
LANE = Y - 30
for k, d in enumerate(["4", "8", "2", "9", "#"]):
    t = 3 + k * 3
    g.token([(158, LANE), (GX + 60, LANE)], t, t + 4, g.chip(f"tecla {d}", bg=g.BLUE, size=13, h=24), hold=t + 4.2)
g.token([(158, LANE), (GX + 60, LANE)], 77, 81, g.chip("4829#", bg=g.BLUE, size=13, h=24), hold=81.2)
g.appear(g.mark(GX + GW - 44, Y + 81, True, 14), 81, 100)

g.add(g.note(48, 470, 440, "Probalo seguro", ["Con la puerta abierta o con alguien", "del lado de adentro: un relé mal", "configurado traba o deja abierta."], "amb"))
g.appear(g.note(512, 470, 640, None, ["Door System Settings > Basic Settings: Enable DTMF Open Door en Sí y", "Remote PIN propio (4829 es de ejemplo)."], "info"), 0, 50)
g.appear(g.note(512, 470, 640, None, ["La salida de alarma que maneja la cerradura tiene que estar en", "Open Door: es la que el PIN activa."], "ok"), 50, 75)
g.appear(g.note(512, 470, 640, None, ["El PIN coincide y nada se mueve: revisá la función de ALMOUT1", "antes que la cerradura y el cableado."], "bad"), 75, 100)

g.status(632, [
    (0, 25, "El PIN viaja por el mismo camino que la voz, tecla por tecla.", g.INK),
    (25, 50, "El # cierra el PIN; el GDS lo compara con el suyo.", g.INK),
    (50, 75, "Salida en Open Door: el contacto se cierra y la cerradura abre.", g.OK),
    (75, 100, "Con otra función en la salida, el PIN se acepta y la puerta queda igual.", g.BAD),
])

g.done(12, "l1", "Del PIN a la cerradura: la salida tiene que estar en Open Door",
       "Animación en cuatro tiempos con el GRP de recepción en una llamada con el portero, la UCM, el GDS3710 registrado como extensión 8001, con su Remote PIN y su salida de alarma ALMOUT1, y la cerradura conectada a esa salida. "
       "1: durante la llamada, recepción marca 4829#; cada tecla viaja como evento RFC 4733 hasta el GDS. "
       "2: con Enable DTMF Open Door, el GDS compara lo recibido con su Remote PIN to Open the Door, 4829: coincide. "
       "3: ALMOUT1 está en Open Door; el GDS activa la salida, el contacto se cierra y la cerradura se libera. "
       "4: si ALMOUT1 tiene otra función, el PIN se acepta igual y la puerta no se mueve: hay que revisar la función de la salida antes que la cerradura y el cableado. "
       "Se prueba con la puerta abierta o con alguien del lado de adentro. 4829 es un PIN de ejemplo.",
       [8, 36, 62, 92])
