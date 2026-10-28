#!/usr/bin/env python3
"""Lección 16 · Paquetes al día · Laboratorio paso 3: habilitar un paquete extra y deshacerlo.
enable marca, apply-changes lo baja y reinicia, al arrancar queda instalado; uninstall + apply-changes lo quita en el arranque siguiente.
"""
from _anim_mk_32_39 import *

a = Anim(T=28, kicker="MIKROTIK · PAQUETES AL DÍA · PASO 3", title="Un paquete extra: se marca, se aplica, se reinicia")
a.steps([
    "/system/package/print: zerotier figura con X A, disponible pero no instalado.",
    "enable zerotier deja el cambio marcado. Todavía no se instala nada.",
    "apply-changes: baja el paquete del servidor de MikroTik y reinicia.",
    "Al arrancar queda instalado. /log/print where topics~\"system\" lo confirma.",
    "uninstall y apply-changes: se quita en el arranque siguiente.",
], still=3, size=17)

# ---- terminal
TX, TY, TW = 48, 176, 600
a.add(a.box(TX, TY, TW, 312, a.INK, rx=14))
a.add(a.text(TX + 18, TY + 30, "TERMINAL", 13, SKY, a.MONO, 400, extra='letter-spacing="1.6"'))
CMDS = [
    ("/system/package/print", 0),
    ("/system/package/enable zerotier", 20),
    ("/system/package/apply-changes", 40),
    ('/log/print where topics~"system"', 62),
    ("/system/package/uninstall zerotier", 80),
    ("/system/package/apply-changes", 86),
]
for i, (c, t) in enumerate(CMDS):
    y = TY + 66 + i * 40
    txt = a.text(TX + 18, y, c, 16, a.WHITE, a.MONO)
    a.add(during(a, txt, t, 100, still=1 if t < 70 else 0) if t else txt)
    a.add(during(a, a.box(TX + 8, y - 26, TW - 16, 36, "none", GOLD, rx=8, sw=2.5), t + 0.5, t + 8))

# ---- lista de paquetes
PX, PY, PW = 690, 176, 462
a.add(a.box(PX, PY, PW, 176, a.WHITE, a.LINE, rx=14))
a.add(a.text(PX + 18, PY + 30, "paquetes del equipo", 15, a.GREY, a.MONO))
a.add(a.box(PX + 14, PY + 46, PW - 28, 50, a.SLATE, rx=10))
a.add(a.text(PX + 30, PY + 77, "routeros", 17, a.INK, a.MONO, 600))
a.add(a.text(PX + PW - 30, PY + 77, "instalado", 15, a.OK, a.SANS, 600, "end"))
a.add(a.box(PX + 14, PY + 106, PW - 28, 50, a.SLATE, rx=10))
a.add(a.text(PX + 30, PY + 137, "zerotier", 17, a.INK, a.MONO, 600))
ST = [
    (0, 20, "X A", "disponible, no instalado", a.GREY, 0),
    (20, 40, "X A", "marcado para instalar", a.AMB, 0),
    (40, 60, "", "se instala al arrancar", a.AMB, 0),
    (60, 80, "", "instalado", a.OK, 1),
    (80, 96, "", "marcado para quitar", a.AMB, 0),
    (96, 100, "X A", "quitado", a.GREY, 0),
]
for t0, t1, fl, lab, col, st in ST:
    s = a.text(PX + PW - 30, PY + 137, lab, 15, col, a.SANS, 600, "end")
    if fl:
        s += a.pill(PX + 130, PY + 118, fl, a.INK, "#E6EDF4", 14, 26)
    a.add(during(a, s, t0, t1, still=st))
a.add(during(a, a.box(PX + 10, PY + 102, PW - 20, 58, "none", GOLD, rx=12, sw=3), 21, 30))
a.add(during(a, a.box(PX + 10, PY + 102, PW - 20, 58, "none", a.OK, rx=12, sw=3), 60, 70, still=1))

# ---- servidor y reinicio
a.add(dev(a, 952, 376, 200, 92, "Servidor", "MikroTik", "cloud", tsize=17))
a.add(router(a, 690, 376, 220, 92, "Router", "RouterOS"))
a.add(line(910, 422, 952, 422, a.LINE, 3, "5 7"))
a.add(travel(a, pkt(a, "zerotier", a.CYAN, size=14, h=26), [(1050, 360), (800, 360)], 42, 48, hold=1))
for t0 in (50, 92):
    a.add(during(a, a.box(690, 376, 220, 92, a.INK, rx=16) + a.text(800, 430, "reiniciando…", 18, GOLD, a.SANS, 600, "middle"), t0, t0 + 6))

narr(a, 48, 540, [
    (0, 20, "X significa deshabilitado; A, que está disponible para bajar.", a.TXT, 0),
    (20, 40, "Habilitar, quitar o actualizar: todo queda pendiente hasta el reinicio.", a.AMB, 0),
    (40, 60, "Los paquetes no se cambian en caliente: se aplican en el arranque.", a.AMB, 0),
    (60, 80, "Después del reinicio, revisá el log: dice si se instaló o por qué no.", a.OK, 1),
    (80, 100, "Deshacer también lleva reinicio. En un cliente, hacelo con ventana de corte.", a.AMB, 0),
])
a.add(a.text(48, 600, "zerotier es de ejemplo: en un equipo sin ese paquete, elegí otro de la lista.", 16, a.TXT, a.SANS, 600))

write(a, 16, "l1", "Un paquete extra: se marca, se aplica, se reinicia",
      "Animación en cinco tiempos con la terminal, la lista de paquetes del equipo (routeros instalado y zerotier), el servidor de MikroTik y el router. "
      "1: /system/package/print muestra zerotier con las marcas X A: deshabilitado y disponible para bajar, no instalado. "
      "2: /system/package/enable zerotier deja el cambio marcado; todavía no se instala nada. "
      "3: /system/package/apply-changes baja el paquete del servidor de MikroTik y reinicia. "
      "4: al arrancar, zerotier queda instalado; /log/print where topics~\"system\" lo confirma. "
      "5: /system/package/uninstall zerotier y otra vez apply-changes lo marcan para quitar, y se quita en el arranque siguiente.",
      [6, 26, 46, 52, 66, 86, 95])
