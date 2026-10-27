#!/usr/bin/env python3
"""Lección 7 · Teoría · La cola de despachos en el tiempo.
Sale de teoria_md (Cómo funciona): un despacho entra en la cola dispatch; dispatch-worker procesa hasta 4 a la vez; si el
envío falla vuelve a Pendiente y la cola lo reintenta con 5, 10, 20 y 40 segundos de espera (2 elevado al intento menos
uno, por el retardo base); al quinto intento queda Fallido; un despacho con canal email termina en "Canal no soportado";
Reintentar crea un despacho nuevo con el mismo contenido."""
from _anim_omni import new, out, when, box

a = new(26, "DESPACHOS", "La cola de despachos, en el tiempo")
a.steps([
    "Una alerta crea despachos en la cola; el worker toma hasta 4 a la vez.",
    "Tres salen. El de Telegram falla y vuelve a Pendiente.",
    "Reintenta tras 5, 10, 20 y 40 s. Al quinto intento, Fallido.",
    "El de email termina en Canal no soportado: no hay envío por correo.",
    "Reintentar crea un despacho nuevo con el mismo contenido.",
], still=2)

# ---- worker con 4 lugares
WX, WY = 48, 186
a.add(a.box(WX, WY, 520, 176, a.WHITE, a.LINE, rx=14))
a.add(a.text(WX + 20, WY + 32, "dispatch-worker · hasta 4 a la vez", 17, a.INK, a.SANS, 600))
SLOT = [(WX + 20 + i * 124, WY + 54) for i in range(4)]
for x, y in SLOT:
    a.add(a.box(x, y, 112, 100, a.SLATE, rx=10))
JOBS = [("#101", "push"), ("#102", "WhatsApp"), ("#103", "push"), ("#104", "Telegram")]
for (x, y), (jid, ch) in zip(SLOT, JOBS):
    when(a, a.text(x + 56, y + 40, jid, 17, a.INK, a.MONO, 600, "middle") + a.text(x + 56, y + 68, ch, 15, a.TXT, a.MONO, 600, "middle"), 3, 38, still=0)
x5, y5 = SLOT[0]
when(a, a.text(x5 + 56, y5 + 40, "#105", 17, a.INK, a.MONO, 600, "middle") + a.text(x5 + 56, y5 + 68, "email", 15, a.TXT, a.MONO, 600, "middle"), 62, 80, still=0)

# ---- estados (Despachos)
SX, SW = 600, 552
a.add(a.box(SX, WY, SW, 290, a.WHITE, a.LINE, rx=14))
a.add(a.text(SX + 20, WY + 32, "Despachos", 17, a.INK, a.SANS, 600))
ROWS = ["#101 · push", "#102 · WhatsApp", "#103 · push", "#104 · Telegram", "#105 · email", "#106 · copia de #104"]
RY0, RH = WY + 50, 38
PEND, PROC, ENV = ("Pendiente", a.AMB, a.AMBBG), ("Procesando", a.BLUE, "#DCEBFA"), ("Enviado", a.OK, a.OKBG)
FAIL, NOSUP = ("Fallido", a.WHITE, a.BAD), ("Canal no soportado", a.BAD, a.BADBG)


def row(i, states, appear=0, still_state=None):
    y = RY0 + i * RH
    when(a, a.text(SX + 24, y + 24, ROWS[i], 16, a.INK, a.MONO, 600), appear, 100, still=1 if appear < 50 else 0)
    for t0, t1, (lab, fg, bg) in states:
        when(a, a.pill(SX + SW - 20, y + 4, lab, fg, bg, 15, 28, "end"), t0, t1, still=1 if still_state == lab else 0, fade=0.6)


row(0, [(1, 3, PEND), (3, 20, PROC), (20, 100, ENV)], still_state="Enviado")
row(1, [(1, 3, PEND), (3, 21, PROC), (21, 100, ENV)], still_state="Enviado")
row(2, [(1, 3, PEND), (3, 22, PROC), (22, 100, ENV)], still_state="Enviado")
row(3, [(1, 3, PEND), (3, 24, PROC), (24, 41, PEND), (41, 43, PROC), (43, 45, PEND), (45, 47, PROC), (47, 49, PEND), (49, 52, PROC), (52, 54, PEND), (54, 57, PROC), (57, 100, FAIL)], still_state="Fallido")
row(4, [(1, 62, PEND), (62, 66, PROC), (66, 100, NOSUP)], still_state="Pendiente")
row(5, [(82, 100, PEND)], appear=82)
when(a, a.pill(SX + 330, RY0 + 3 * RH + 4, "Reintentar", a.BLUE, a.WHITE, 15, 28, "end"), 80, 100, still=0)

# ---- línea de reintentos del #104
TX0, TX1, TY = 120, 1110, 548
SC = (TX1 - TX0) / 75
a.add(a.text(48, 512, "#104 · intentos", 16, a.INK, a.MONO, 600))
a.add(f'<line x1="{TX0}" y1="{TY}" x2="{TX1}" y2="{TY}" stroke="{a.LINE}" stroke-width="3"/>')
ATT = [(0, 26), (5, 42), (15, 46), (35, 50), (75, 55)]
prev = None
for k, (sec, t) in enumerate(ATT):
    x = TX0 + k * (TX1 - TX0) / 4
    when(a, f'<circle cx="{x:.0f}" cy="{TY}" r="13" fill="{a.BAD}"/>' + a.text(x, TY + 5, f"{k + 1}", 15, a.WHITE, a.MONO, 600, "middle")
         + a.text(x, TY + 32, f"{sec} s", 15, a.GREY, a.MONO, 600, "middle"), t, 100, still=1)
    if prev is not None:
        w = sec - prev[0]
        when(a, a.text((prev[1] + x) / 2, TY - 12, f"espera {w} s", 15, a.TXT, a.MONO, 600, "middle"), t, 100, still=1)
    prev = (sec, x)
when(a, a.pill(TX1, TY + 46, "al quinto intento: Fallido", a.WHITE, a.BAD, 15, 28, "end"), 57, 100, still=1)
a.add(a.text(48, 646, "Cada espera es el retardo base por 2 elevado al intento menos uno: 5, 10, 20, 40.", 16, a.TXT, a.SANS, 600))

out(a, 7, 1, "La cola de despachos, en el tiempo",
    "Animación en cinco tiempos. Arriba a la izquierda, dispatch-worker con cuatro lugares; arriba a la derecha, la lista de Despachos con su estado; abajo, la línea de intentos del despacho #104. "
    "Tiempo 1: una alerta crea despachos en la cola dispatch y el worker toma cuatro a la vez: #101 push, #102 WhatsApp, #103 push y #104 Telegram, que pasan de Pendiente a Procesando. "
    "Tiempo 2: #101, #102 y #103 quedan Enviado; #104 falla y vuelve a Pendiente. "
    "Tiempo 3: #104 se reintenta tras esperas de 5, 10, 20 y 40 segundos, en los segundos 0, 5, 15, 35 y 75; al quinto intento queda Fallido. "
    "Tiempo 4: #105, con canal email, pasa por el worker y termina en Canal no soportado, porque en esta versión no hay envío por correo. "
    "Tiempo 5: el botón Reintentar del #104 crea un despacho nuevo, #106, copia del #104, Pendiente, con el mismo contenido. "
    "Al pie: cada espera es el retardo base por 2 elevado al intento menos uno.",
    [12, 32, 58, 72, 94])
