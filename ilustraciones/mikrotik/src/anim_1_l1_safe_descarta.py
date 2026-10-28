#!/usr/bin/env python3
"""Lección 1 · Laboratorio, pasos 4 y 5: Ctrl+X, la regla prueba-safe se aplica y queda con F,
Ctrl+D sale deshaciendo, y al volver a entrar el print no la encuentra.
Fuente: Configuration Management (Ctrl+X / F4, Safe Mode taken, F floating-undo, Ctrl+D deshace, /quit no)."""
from _anim_red_1_9 import *

a = Anim(T=24, kicker="MIKROTIK · ENTRAR SIN ROMPER · LABORATORIO", title="Lo que hace Ctrl+D con la regla de prueba")
a.steps([
    "Ctrl+X: Safe Mode tomado, el prompt muestra <SAFE>.",
    "Agregás prueba-safe: se aplica en el acto y queda en el historial con F.",
    "Ctrl+D: salís descartando y RouterOS deshace lo marcado con F.",
    "Volvés a entrar y el print con where no encuentra la regla.",
], still=3)

TX, TY, TW = 48, 180, 600
a.add(a.box(TX, TY, TW, 430, a.INK, rx=16))
a.add(a.text(TX + 18, TY + 30, "NEW TERMINAL", 13, SKY, a.MONO, 400, extra='letter-spacing="1.8"'))
L = [
    ("[admin@MikroTik] > Ctrl+X", a.WHITE, 2, 0),
    ("[Safe Mode taken]", GOLD, 5, 0),
    ("[admin@MikroTik] <SAFE> /ip/firewall/filter/add", a.WHITE, 27, 0),
    ('  chain=forward action=passthrough comment="prueba-safe"', a.WHITE, 27, 18),
    ("[admin@MikroTik] <SAFE> Ctrl+D", a.WHITE, 52, 0),
    ("sesión cerrada", SKY, 55, 0),
    ("[admin@MikroTik] > /ip/firewall/filter/print", a.WHITE, 77, 0),
    ('  where comment="prueba-safe"', a.WHITE, 77, 18),
    ("sin resultados: la regla no está", MINT, 82, 0),
]
for i, (t, c, t0, dx) in enumerate(L):
    y = TY + 66 + i * 38 + (14 if i >= 6 else 0)
    a.add(during(a, a.text(TX + 18 + dx, y, t, 15, c, a.MONO, 600 if c != a.WHITE else 400), t0, 100, still=1))
a.add(during(a, f'<line x1="{TX + 18}" y1="{TY + 66 + 5 * 38 + 18}" x2="{TX + TW - 18}" y2="{TY + 66 + 5 * 38 + 18}" stroke="#2E5C88" stroke-width="1.5" stroke-dasharray="5 5"/>', 70, 100, still=1))
a.add(during(a, a.text(TX + TW - 18, TY + 66 + 5 * 38 + 38, "volvés a entrar", 15, SKY, a.MONO, 400, "end"), 70, 100, still=1))

# tabla de filtros
FX, FW = 676, 476
a.add(a.box(FX, TY, FW, 212, a.WHITE, a.LINE, rx=16))
a.add(a.text(FX + 20, TY + 32, "/ip/firewall/filter", 16, a.INK, a.MONO, 600))
a.add(a.box(FX + 16, TY + 50, FW - 32, 40, a.SLATE, rx=8))
a.add(a.text(FX + 32, TY + 76, "reglas de la defconf", 15, a.TXT, a.MONO))
row = (a.box(FX + 16, TY + 100, FW - 32, 40, a.OKBG, rx=8)
       + a.text(FX + 32, TY + 126, "forward · passthrough · prueba-safe", 15, a.INK, a.MONO, 600))
a.add(during(a, row, 30, 56))
a.add(during(a, row + f'<line x1="{FX + 30}" y1="{TY + 121}" x2="{FX + FW - 30}" y2="{TY + 121}" stroke="{a.BAD}" stroke-width="3"/>', 56, 64))
a.add(during(a, a.text(FX + 20, TY + 176, "la regla ya está activa", 15, a.OK, a.SANS, 600), 32, 56))
a.add(during(a, a.text(FX + 20, TY + 176, "deshecha: vuelve a como estaba", 15, a.BAD, a.SANS, 600), 58, 100, still=1))

# historial
HY = TY + 232
a.add(a.box(FX, HY, FW, 198, a.INK, rx=16))
a.add(a.text(FX + 20, HY + 32, "/system/history", 16, a.WHITE, a.MONO, 600))
h = (a.box(FX + 16, HY + 52, FW - 32, 44, a.NAVY2, rx=8)
     + a.text(FX + 34, HY + 80, "F", 17, GOLD, a.MONO, 600)
     + a.text(FX + 64, HY + 80, "filter rule added", 15, a.WHITE, a.MONO, 600)
     + a.text(FX + FW - 34, HY + 80, "admin", 15, SKY, a.MONO, 400, "end"))
a.add(during(a, h, 32, 58))
a.add(during(a, a.text(FX + 20, HY + 126, "F: se deshace si la sesión de Safe Mode", 15, "#C9DDF0", a.SANS, 600)
             + a.text(FX + 20, HY + 148, "termina mal o salís con Ctrl+D.", 15, "#C9DDF0", a.SANS, 600), 32, 58))
a.add(during(a, a.text(FX + 20, HY + 126, "Ctrl+D deshace todo lo de Safe Mode.", 15, "#FF9E8A", a.SANS, 600)
             + a.text(FX + 20, HY + 148, "Para quedártelo: Ctrl+X otra vez o /quit.", 15, MINT, a.SANS, 600), 58, 100, still=1))

a.add(a.text(48, 646, "Hasta 100 acciones: un script largo saca solo del modo seguro y ya no deshace nada.", 16, a.AMB, a.SANS, 600))

write(a, 1, "l1", "Safe Mode y Ctrl+D en el laboratorio",
      "Animación en cuatro tiempos con la terminal, la tabla /ip/firewall/filter y /system/history. "
      "1: Ctrl+X muestra Safe Mode taken y el prompt pasa a SAFE. "
      "2: se agrega la regla forward passthrough con comment prueba-safe; se aplica en el acto y en el historial aparece filter rule added con la marca F. "
      "3: Ctrl+D cierra la sesión descartando; RouterOS deshace lo marcado con F y la regla desaparece de la tabla. "
      "4: al volver a entrar, /ip/firewall/filter/print where comment=prueba-safe no muestra resultados. "
      "Para quedarse con un cambio se sale con Ctrl+X otra vez o con /quit. Safe Mode guarda hasta 100 acciones.",
      [10, 36, 60, 90])
