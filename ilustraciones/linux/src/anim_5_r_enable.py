#!/usr/bin/env python3
"""Lección 5 (Status y journal), Resumen: start contra enable en una obra. start levanta el servicio ahora;
al arrancar, systemd levanta lo que cuelga de multi-user.target.wants, y enable es el que crea ese enlace.
Con start y sin enable, el servicio anda hasta el primer corte de luz. Fuentes: teoría de la lección
(enable crea un enlace en multi-user.target.wants/; start contra enable) y systemctl(1) (enable --now)."""
from _anims_lnx_rl import *

a = nueva(28, "LINUX · SYSTEMD · CÓMO SE VE", "start sin enable: anda hasta el primer corte de luz")
a.steps([
    "start: el servicio corre ahora, pero is-enabled dice disabled.",
    "Corte de luz: al arrancar, systemd no lo levanta. Queda parado.",
    "enable --now: crea el enlace en multi-user.target.wants y lo arranca.",
    "Próximo corte: al arrancar, systemd lo levanta solo.",
], still=3)

# ---- línea de tiempo
TY = 204
a.add(linea(60, TY, 1140, TY, a.LINE, 6))
EV = [(114, "start", a.BLUE, None), (362, "corte", a.BAD, "bolt"), (427, "arranque", a.INK, None),
      (654, "enable --now", a.OK, None), (924, "corte", a.BAD, "bolt"), (989, "arranque", a.INK, None)]
for x, lbl, c, ic in EV:
    a.add(f'<circle cx="{x}" cy="{TY}" r="8" fill="{c}"/>' + a.text(x, TY + 32, lbl, 15, c, a.MONO, 700, "middle"))
    if ic:
        a.add(glyph(a, ic, x - 12, TY - 40, a.BAD, 1.0, 2))
mv = a.move([(0, 60, TY), (100, 1140, TY)])
a.add(a.group(f'<circle r="11" fill="#FFFFFF" stroke="{a.BLUE}" stroke-width="4"/>', mv, still=0))
fijo(a, f'<circle cx="989" cy="{TY}" r="11" fill="#FFFFFF" stroke="{a.BLUE}" stroke-width="4"/>')

# ---- estado del servicio
PX, PY = 48, 258
a.add(a.box(PX, PY, 500, 256, a.WHITE, a.LINE, rx=16) + a.text(PX + 22, PY + 36, "app-obra.service (ejemplo)", 18, a.INK, a.HEAD, 600))
a.add(a.text(PX + 22, PY + 84, "Active", 15, a.GREY, a.MONO, 600) + a.text(PX + 22, PY + 140, "is-enabled", 15, a.GREY, a.MONO, 600))
def estado(t0, t1, act, aok, ena, eok, still=0):
    en(a, a.pill(PX + 150, PY + 62, act, a.OK if aok else a.BAD, a.OKBG if aok else a.BADBG, 15, 32)
       + a.pill(PX + 150, PY + 118, ena, a.OK if eok else a.AMB, a.OKBG if eok else a.AMBBG, 15, 32), t0, t1, still)


estado(0, 5, "inactive (dead)", False, "disabled", False)
estado(5, 28, "active (running)", True, "disabled", False)
estado(28, 55, "inactive (dead)", False, "disabled", False)
estado(55, 80, "active (running)", True, "enabled", True)
estado(80, 86, "inactive (dead)", False, "enabled", True)
estado(86, 100, "active (running)", True, "enabled", True, still=1)
en(a, a.text(PX + 22, PY + 196, "anda... mientras no se reinicie", 16, a.AMB, a.SANS, 700), 6, 28)
en(a, a.text(PX + 22, PY + 196, "nadie lo volvió a arrancar", 16, a.BAD, a.SANS, 700)
   + a.text(PX + 22, PY + 222, "el cliente: \"no anda desde el corte\"", 15, a.TXT, a.SANS, 500), 36, 55)
en(a, a.text(PX + 22, PY + 196, "corre ahora y queda para el booteo", 16, a.OK, a.SANS, 700), 57, 80)
en(a, a.text(PX + 22, PY + 196, "volvió solo, sin que nadie entre", 16, a.OK, a.SANS, 700), 87, 100, still=1)
en(a, a.text(PX + 22, PY + 196, "equipo apagado", 16, a.GREY, a.SANS, 700), 28, 34)
en(a, a.text(PX + 22, PY + 196, "equipo apagado", 16, a.GREY, a.SANS, 700), 80, 86)

# ---- carpeta wants
WX, WY, WW = 580, 258, 572
a.add(a.box(WX, WY, WW, 256, a.WHITE, a.LINE, rx=16) + a.text(WX + 22, WY + 36, "Lo que systemd levanta al arrancar", 18, a.INK, a.HEAD, 600))
a.add(mono(a, WX + 22, WY + 64, "/etc/systemd/system/multi-user.target.wants/", 14, a.GREY, 500))
LINKS = ["ssh.service", "cron.service"]
for i, l in enumerate(LINKS):
    a.add(a.box(WX + 22, WY + 82 + i * 50, WW - 44, 40, a.SLATE, None, rx=10) + mono(a, WX + 40, WY + 108 + i * 50, l + "  →  /usr/lib/systemd/system/" + l, 14, a.INK, 600))
en(a, a.box(WX + 22, WY + 182, WW - 44, 40, a.OKBG, a.OK, rx=10, sw=2.5) + mono(a, WX + 40, WY + 208, "app-obra.service  →  /etc/systemd/system/app-obra.service", 14, a.OK, 700), 57, 100, still=1)
en(a, a.box(WX + 22, WY + 182, WW - 44, 40, "none", a.BAD, rx=10, sw=2.5, extra='stroke-dasharray="7 5"')
   + a.text(WX + 40, WY + 208, "app-obra.service no está: no se levanta", 15, a.BAD, a.SANS, 700), 34, 55)
# barrido de arranque
for t0 in (34, 86):
    viaje(a, "", [(WX + 12, WY + 96), (WX + 12, WY + 206)], t0, t0 + 4,
          inner=f'<path d="M-8 -8 L4 0 L-8 8 z" fill="{a.BLUE}"/>', hold=1)
en(a, a.text(WX + 22, WY + 244, "enable crea el enlace; disable lo borra", 15, a.GREY, a.SANS, 500), 0, 100, still=1)

# ---- terminal
TTY = 530
a.add(tterm(a, 48, TTY, 1104, 64))
def cmd(s, t0, t1, still=0, com=None):
    inner = trow(a, 48, TTY + 38, s, 15)
    if com:
        inner += a.text(1136, TTY + 38, com, 15, T_COM, a.MONO, 500, "end")
    en(a, inner, t0, t1, still)


cmd("$ sudo systemctl start app-obra; systemctl is-enabled app-obra", 0, 28, 0, "# disabled")
cmd("$ systemctl status app-obra", 28, 55, 0, "# inactive (dead)")
cmd("$ sudo systemctl enable --now app-obra", 55, 80, 0, "# enable + start")
cmd("$ systemctl status app-obra", 80, 100, 1, "# active (running), enabled")

narr(a, [
    (0, 25, "start es para ahora: no deja nada anotado para el próximo arranque.", None),
    (25, 50, "Al bootear, systemd mira qué cuelga de multi-user.target: este no estaba.", a.BAD),
    (50, 75, "enable deja el enlace; --now además lo arranca en el momento.", a.OK),
    (75, 100, "Un servicio crítico lleva las dos cosas: corriendo y habilitado.", a.OK),
], still_idx=3)

escribir(a, "5-r1", "start sin enable: anda hasta el primer corte de luz",
         "Animación en cuatro tiempos con una línea de tiempo arriba (start, corte, arranque, enable --now, corte, arranque), el estado del servicio de ejemplo app-obra.service a la izquierda "
         "y, a la derecha, la carpeta /etc/systemd/system/multi-user.target.wants/ con los enlaces de ssh.service y cron.service. "
         "1: systemctl start lo deja active (running), pero is-enabled dice disabled. "
         "2: hay un corte de luz; al arrancar, systemd recorre multi-user.target.wants, app-obra.service no está y queda inactive (dead). "
         "3: systemctl enable --now crea el enlace app-obra.service en multi-user.target.wants y lo arranca: active y enabled. "
         "4: en el próximo corte, al arrancar, systemd lo encuentra en la carpeta y lo levanta solo.",
         [12, 40, 64, 92])
