#!/usr/bin/env python3
"""Lección 2 · teoría: qué pasa durante una actualización por web (subir, verificar, grabar, reiniciar, confirmar)."""
from _anim_akuvox import Anim, A, token, appear, note, finish, mark

a = Anim(T=24, kicker="AKUVOX · LEER EL FIRMWARE", title="Qué pasa mientras se actualiza por web")
a.steps([
    "La pestaña sube el archivo al equipo: no la cierres ni la refresques.",
    "El equipo verifica el archivo y lo graba en su memoria.",
    "Al terminar, el equipo reinicia: unos instantes sin web.",
    "La versión nueva aparece en Product Information: anotala en la ficha.",
], still=3)
PH = [(0, 25), (25, 50), (50, 75), (75, 100)]

# navegador
BX, BY, BW, BH = 48, 184, 400, 270
a.add(a.box(BX, BY, BW, BH, A.WHITE, A.LINE))
a.add(a.box(BX, BY, BW, 40, "#E6EEF6", None, rx=14))
for i in range(3):
    a.add(f'<circle cx="{BX + 20 + i * 16}" cy="{BY + 20}" r="5" fill="#B9C9D8"/>')
a.add(a.text(BX + 76, BY + 26, "Web del portero · Upgrade", 15, A.INK, A.SANS, 600))
a.add(a.text(BX + 20, BY + 74, "System > Basic > Select File > Upgrade", 14, A.BLUE, A.MONO, 600))
a.add(a.text(BX + 20, BY + 112, "archivo", 14, A.GREY, A.MONO))
a.add(a.text(BX + 110, BY + 112, "216.30.10.121.rom", 15, A.INK, A.MONO, 600))
a.add(a.box(BX + 20, BY + 140, BW - 40, 22, A.SLATE, None, rx=11))
fill = f'<rect x="{BX + 20}" y="{BY + 140}" width="{BW - 40}" height="22" rx="11" fill="{A.CYAN}"/>'
sc = a.keyframes([(0, 0.02), (2, 0.02), (23, 1), (100, 1)], prop="transform", fmt="scaleX({})")
from _anim_akuvox import cls  # noqa: E402
c = cls(a, f"transform-box:fill-box;transform-origin:left center;transform:scaleX(1);", sc)
a.add(f'<g class="{c}">{fill}</g>')
appear(a, a.text(BX + 20, BY + 196, "subiendo: no cierres ni refresques", 15, A.AMB, A.SANS, 600), 1, 24, still=0)
appear(a, a.text(BX + 20, BY + 196, "archivo entregado", 15, A.OK, A.SANS, 600), 24, 100, still=1)
appear(a, a.text(BX + 20, BY + 226, "la pestaña mantiene la transferencia", 14, A.GREY, A.MONO), 1, 100, still=1)

# flujo hacia el portero
for i in range(6):
    t0 = 2 + i * 3.4
    token(a, [(BX + BW + 6, BY + 151), (530, BY + 151)], t0, t0 + 3.4, '<rect x="-10" y="-7" width="20" height="14" rx="3" fill="#17A8D4"/>', hold=t0 + 3.6)
a.add(f'<line x1="{BX + BW}" y1="{BY + 151}" x2="536" y2="{BY + 151}" stroke="{A.LINE}" stroke-width="3"/>')

# portero
PX, PW = 536, 270
a.add(a.box(PX, BY, PW, BH, A.WHITE, A.LINE))
a.add(a.text(PX + 20, BY + 34, "Portero", 20, A.INK, A.HEAD, 600))
a.add(a.text(PX + 20, BY + 58, "E16 V2", 15, A.GREY, A.MONO))
stages = [("recibe el archivo", [0]), ("lo verifica", [1]), ("lo graba en memoria", [1]), ("reinicia", [2])]
for i, (lab, ph) in enumerate(stages):
    y = BY + 82 + i * 44
    a.add(a.box(PX + 16, y, PW - 32, 36, A.SLATE, None, rx=9))
    a.add(a.text(PX + 32, y + 24, lab, 15, A.TXT, A.SANS, 600))
    t0 = {0: 2, 1: 26, 2: 36, 3: 51}[i]
    t1 = {0: 25, 1: 36, 2: 50, 3: 75}[i]
    appear(a, a.box(PX + 16, y, PW - 32, 36, "#E4F5FB", A.CYAN, rx=9, sw=2) + a.text(PX + 32, y + 24, lab, 15, A.INK, A.SANS, 600), t0, t1, still=0, fade=0.8)
    appear(a, mark(a, PX + PW - 36, y + 18, True, 10), t1, 100, still=1)
appear(a, a.box(PX, BY, PW, BH, "#F7FAFD", None, rx=14, extra='opacity=".94"')
       + a.text(PX + PW / 2, BY + BH / 2 + 6, "reiniciando…", 18, A.GREY, A.MONO, 600, "middle"), 54, 72, still=0)

# Product Information
IX, IW = 852, 300
a.add(a.box(IX, BY, IW, BH, A.WHITE, A.LINE))
a.add(a.text(IX + 20, BY + 34, "Product Information", 17, A.INK, A.SANS, 600))
a.add(a.text(IX + 20, BY + 58, "Status > Basic", 14, A.GREY, A.MONO))
a.add(a.text(IX + 20, BY + 100, "Model", 14, A.GREY, A.MONO))
a.add(a.text(IX + 20, BY + 124, "E16", 17, A.INK, A.MONO, 600))
a.add(a.text(IX + 20, BY + 162, "Firmware Version", 14, A.GREY, A.MONO))
appear(a, a.text(IX + 20, BY + 188, "la anterior", 17, A.GREY, A.MONO, 600), 0, 52, still=0)
appear(a, a.text(IX + 20, BY + 188, "sin respuesta", 17, A.GREY, A.MONO, 600), 52, 76, still=0)
appear(a, a.box(IX + 12, BY + 172, IW - 24, 34, A.OKBG, A.OK, rx=8, sw=2) + a.text(IX + 20, BY + 195, "216.30.10.121", 17, A.OK, A.MONO, 600), 76, 100, still=1)
appear(a, a.text(IX + 20, BY + 234, "→ a la ficha del equipo", 15, A.OK, A.SANS, 600), 80, 100, still=1)

s, _ = note(a, 48, 482, 540, "Por qué no cerrar la pestaña",
            ["La transferencia vive en la pestaña: si la cerrás o", "la refrescás a mitad de camino, se corta."], "amb")
a.add(s)
s, _ = note(a, 612, 482, 540, "216.30.10.121, leído",
            ["216 = E16 V2 · 30 = logo Akuvox · 10 = rama con", "alta seguridad · 121 = versión dentro de esa rama."], "info")
a.add(s)

finish(a, "2-t1.svg", "Qué pasa durante una actualización por web",
       "Animación en cuatro tiempos con la web del portero en System > Basic > Select File > Upgrade, el portero E16 V2 y su página Product Information. "
       "1: la pestaña del navegador sube el archivo 216.30.10.121.rom al equipo; la transferencia vive en la pestaña, por eso no se cierra ni se refresca. "
       "2: el portero verifica el archivo y lo graba en su memoria. 3: al terminar, reinicia y la web no responde por un momento. "
       "4: la versión nueva, 216.30.10.121, aparece en Product Information y se anota en la ficha del equipo. "
       "Notas: si se cierra o se refresca la pestaña a mitad de camino, la transferencia se corta; 216.30.10.121 se lee como E16 V2, logo Akuvox, rama 10 con alta seguridad y versión 121.",
       [12, 38, 62, 90])
