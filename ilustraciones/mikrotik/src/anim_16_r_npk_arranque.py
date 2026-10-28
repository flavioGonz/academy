#!/usr/bin/env python3
"""Lección 16 · Paquetes al día · Resumen ("Cómo se ve en la red").
Actualización sin internet: la PC baja los .npk de la arquitectura del equipo, van a la raíz de Files, y al arrancar
RouterOS revisa cada uno (de MikroTik, arquitectura, misma versión) antes de instalarlo.
"""
from _anim_mk_32_39 import *

a = Anim(T=28, kicker="MIKROTIK · PAQUETES AL DÍA · CÓMO SE VE EN LA RED", title="Qué revisa el router antes de instalar un .npk")
a.steps([
    "En la PC bajás de mikrotik.com routeros y wifi-qcom de la misma versión, para arm64.",
    "Los arrastrás a la raíz de Files con WinBox y reiniciás.",
    "Al arrancar, cada .npk se revisa: de MikroTik, de su arquitectura. Pasan: se instalan.",
    "Un .npk de otra arquitectura (mipsbe) no se instala: el log dice por qué.",
    "Si subís routeros sin el wifi-qcom de la misma versión, arranca sin WiFi.",
], still=2, size=17)

TY, TH = 182, 96
a.add(dev(a, 48, TY, 300, TH, "PC con internet", "mikrotik.com", "laptop"))
a.add(router(a, 450, TY, 300, TH, "hAP ax · Files /", "architecture-name=arm64"))
a.add(router(a, 852, TY, 300, TH, "Arranque", "RouterBOOT → RouterOS"))
a.add(line(348, TY + 48, 450, TY + 48, a.LINE, 3, "5 7"))
a.add(a.arrow(f"M754 {TY + 48} H846", a.GREY, 2.5))
a.add(during(a, a.box(848, TY - 4, 308, TH + 8, "none", GOLD, rx=18, sw=3.5) + a.pill(1002, TY + TH + 10, "reinicio", a.INK, GOLD, 14, 26, "middle"), 34, 42))

# archivos bajados en la PC
F1, F2, F3 = "routeros-7.x-arm64.npk", "wifi-qcom-7.x-arm64.npk", "routeros-7.x-mipsbe.npk"
a.add(during(a, a.pill(48, 292, F1, a.INK, a.SLATE, 14, 26), 4, 100, still=1))
a.add(during(a, a.pill(48, 324, F2, a.INK, a.SLATE, 14, 26), 8, 100, still=1))
# viajan a Files
a.add(travel(a, pkt(a, ".npk", a.CYAN, size=14, h=26), [(330, TY + 48), (440, TY + 48)], 22, 26, hold=0.5))
a.add(travel(a, pkt(a, ".npk", a.CYAN, size=14, h=26), [(330, TY + 48), (440, TY + 48)], 27, 31, hold=0.5))
a.add(during(a, a.pill(450, 292, F1, a.INK, a.SLATE, 14, 26), 26, 100, still=1))
a.add(during(a, a.pill(450, 324, F2, a.INK, a.SLATE, 14, 26), 31, 80, still=1))
a.add(during(a, a.pill(450, 324, "(wifi-qcom no subido)", a.BAD, a.BADBG, 14, 26), 81, 100))
a.add(during(a, a.pill(450, 356, F3, a.BAD, a.BADBG, 14, 26), 60, 80))
a.add(during(a, a.text(692, 310, "← en la raíz,", 15, a.TXT, a.SANS, 600) + a.text(692, 332, "no en una carpeta", 15, a.TXT, a.SANS, 600), 22, 40))

# tabla de revisión
X0, Y0 = 48, 392
COLS = [(X0 + 16, "paquete"), (X0 + 380, "de MikroTik"), (X0 + 560, "arquitectura"), (X0 + 740, "versión"), (X0 + 900, "resultado")]
a.add(during(a, a.box(X0, Y0, 1104, 184, a.WHITE, a.LINE, rx=14) + "".join(a.text(x, Y0 + 28, t, 15, a.GREY, a.MONO) for x, t in COLS), 42, 100, still=1))
ROWS = [
    (F1, (True, True, True), "se instala", a.OK, 44, 100, 1),
    (F2, (True, True, True), "se instala", a.OK, 48, 80, 1),
    (F3, (True, False, None), "no se instala", a.BAD, 61, 80, 0),
    ("wifi-qcom instalado, versión vieja", (True, True, False), "arranca sin WiFi", a.BAD, 82, 100, 0),
]
for i, (f, ok, res, col, t0, t1, st) in enumerate(ROWS):
    y = Y0 + 44 + (i if i < 3 else 1) * 44
    inner = a.box(X0 + 8, y, 1088, 38, a.SLATE if col == a.OK else a.BADBG, rx=8) + a.text(X0 + 16, y + 25, f, 15, a.INK, a.MONO, 600)
    for k, v in enumerate(ok):
        if v is None:
            pass  # no llega a revisarse
        else:
            inner += (check if v else xmark)(a, COLS[k + 1][0] + 40, y + 19, 12)
    inner += a.text(COLS[4][0], y + 25, res, 15, col, a.SANS, 600)
    a.add(during(a, inner, t0, t1, still=st))
a.add(during(a, a.text(COLS[2][0] + 60, Y0 + 44 + 2 * 44 + 25, "mipsbe ≠ arm64", 14, a.BAD, a.MONO, 600), 62, 80))

narr(a, 48, 612, [
    (0, 20, "Primero mirá architecture-name en System > Resources: el .npk tiene que ser de esa.", a.TXT, 0),
    (20, 40, "Nada se instala en caliente: el router los toma en el próximo arranque.", a.TXT, 0),
    (40, 60, "Todos los paquetes del equipo quedan en la misma versión.", a.OK, 1),
    (60, 80, "No rompe nada: lo saltea. /log/print where topics~\"system\" dice qué pasó.", a.BAD, 0),
    (80, 100, "El paquete de radio va siempre junto con routeros, de la misma versión.", a.BAD, 0),
])
a.add(a.text(48, 646, "/file/print where name~\".npk\"  ·  /system/reboot", 16, a.TXT, a.MONO))

write(a, 16, "r1", "Qué revisa el router antes de instalar un .npk",
      "Animación en cinco tiempos con una PC con internet, un hAP ax con architecture-name=arm64 y su arranque (RouterBOOT y después RouterOS), y abajo una tabla de revisión por paquete. "
      "1: en la PC se bajan de mikrotik.com routeros y wifi-qcom de la misma versión, para arm64. "
      "2: se arrastran a la raíz de Files con WinBox, no a una carpeta, y se reinicia. "
      "3: al arrancar, cada .npk se revisa: que sea un paquete de MikroTik y de la arquitectura del equipo, y que la versión acompañe; los dos pasan y se instalan. "
      "4: un .npk de otra arquitectura, mipsbe, no se instala; el log dice por qué. "
      "5: si se sube routeros sin el wifi-qcom de la misma versión, el paquete de radio no acompaña y el equipo arranca sin WiFi.",
      [6, 26, 38, 50, 66, 88])
