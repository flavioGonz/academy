#!/usr/bin/env python3
"""Lección 10 · Laboratorio, paso 4: sudo systemctl restart de un servicio que consume. systemd manda su señal de
parada (SIGTERM por defecto), espera a que salga; si no sale en TimeoutStopSec (90 s por defecto) manda SIGKILL;
después lo arranca de nuevo con otro PID, y todo queda en el journal. Fuentes: teoría de la lección (restart es
mejor que kill: systemd lo baja con su señal de parada, espera y lo vuelve a levantar, y queda en el journal) y
systemd.kill(5) / systemd.service(5) (KillSignal=SIGTERM, TimeoutStopSec, SIGKILL al vencer)."""
from _anims_lnx_rl import *

a = nueva(28, "LINUX · PROCESOS · LABORATORIO", "systemctl restart: pedir, esperar y recién ahí forzar")
a.steps([
    "restart: systemd le manda SIGTERM al proceso principal del servicio.",
    "El grabador cierra el archivo y sale; systemd lo anota en el journal.",
    "Si no saliera en TimeoutStopSec (90 s por defecto), sigue SIGKILL.",
    "Lo vuelve a arrancar con un PID nuevo, y queda todo registrado.",
], still=3)

X = {"vos": 140, "systemd": 430, "svc": 740, "journal": 1030}
HEAD = {"vos": ("Vos", "sudo systemctl"), "systemd": ("systemd", "PID 1"), "svc": ("grabador.service", "PID 1502 · ejemplo"), "journal": ("journald", "el journal")}
for k, x in X.items():
    t, s = HEAD[k]
    dark = k == "systemd"
    a.add(a.box(x - 122, 168, 244, 64, a.INK if dark else a.WHITE, None if dark else "#C2D4E6", rx=14)
          + a.text(x, 196, t, 18, "#FFFFFF" if dark else a.INK, a.SANS, 600, "middle") + a.text(x, 220, s, 14, LIGHT if dark else a.GREY, a.MONO, 500, "middle"))
    a.add(lifeline(a, x, 232, 452))

msg(a, X["vos"], X["systemd"], 270, "restart grabador", 3, still=1)
msg(a, X["systemd"], X["svc"], 300, "SIGTERM (15)", 8, still=1)
en(a, a.box(X["svc"] - 112, 316, 224, 50, a.OKBG, a.OK, rx=10) + a.text(X["svc"], 338, "cierra video.mp4", 15, a.OK, a.SANS, 700, "middle")
   + a.text(X["svc"], 358, "y sale", 15, a.INK, a.SANS, 500, "middle"), 28, 50)
msg(a, X["svc"], X["systemd"], 388, "salió", 34, end=50, color=a.OK, still=0)
ventanas(a, a.box(X["svc"] - 112, 316, 224, 50, a.OKBG, a.OK, rx=10) + a.text(X["svc"], 338, "cierra video.mp4", 15, a.OK, a.SANS, 700, "middle")
   + a.text(X["svc"], 358, "y sale", 15, a.INK, a.SANS, 500, "middle")
   + a.arrow(f"M{X['svc']} 388 H{X['systemd'] + 2}", a.OK, 3) + a.text((X["svc"] + X["systemd"]) / 2, 377, "salió", 16, a.OK, a.MONO, 600, "middle"), [(75, 100)], still=1)
en(a, a.box(X["svc"] - 112, 316, 224, 50, a.BADBG, a.BAD, rx=10) + a.text(X["svc"], 338, "no responde", 15, a.BAD, a.SANS, 700, "middle")
   + a.text(X["svc"], 358, "(caso alternativo)", 15, a.INK, a.SANS, 500, "middle"), 52, 75)
# caso alternativo (paso 3): reloj y SIGKILL
en(a, a.box(X["vos"] + 16, 300, 256, 120, a.AMBBG, a.AMB, rx=12, sw=2)
   + a.text(X["vos"] + 32, 328, "si no saliera:", 16, a.AMB, a.SANS, 700)
   + a.text(X["vos"] + 32, 354, "espera TimeoutStopSec", 15, a.INK, a.MONO, 600)
   + a.text(X["vos"] + 32, 378, "(90 s por defecto)", 15, a.INK, a.SANS, 500)
   + a.text(X["vos"] + 32, 404, "y manda SIGKILL (9)", 15, a.BAD, a.MONO, 700), 52, 75)
viaje(a, "SIGKILL (9)", [(X["systemd"] + 160, 440), (X["svc"] - 40, 440)], 60, 66, bg=a.BAD, size=14, hold=6)
# arranque nuevo
msg(a, X["systemd"], X["svc"], 430, "arranca de nuevo", 78, still=1, color=a.BLUE)
en(a, a.pill(X["svc"] + 16, 412, "PID 1733", a.BLUE, "#E5F0FB", 15, 30), 81, 100, still=1)
# cada evento al journal
for t, y in ((10, 312), (36, 382), (80, 424)):
    viaje(a, "", [(X["systemd"] + 8, y), (X["journal"], y)], t, t + 4, inner=f'<circle r="6" fill="{a.GREY}"/>', hold=0)

# terminal journal
TY = 482
a.add(tterm(a, 48, TY, 1104, 124, "JOURNALCTL -U GRABADOR · EJEMPLO"))
en(a, trow(a, 48, TY + 50, ("systemd[1]: Stopping grabador.service - Grabador de video...", T_OUT), 14), 12, 100, still=1)
ventanas(a, trow(a, 48, TY + 74, ("systemd[1]: grabador.service: Deactivated successfully.", T_OK), 14), [(38, 50), (75, 100)], still=1)
en(a, trow(a, 48, TY + 74, ("systemd[1]: grabador.service: State 'stop-sigterm' timed out. Killing.", T_ERR), 14)
   + a.text(1136, TY + 74, "(solo si no sale)", 14, T_COM, a.MONO, 500, "end"), 56, 75)
en(a, trow(a, 48, TY + 98, ("systemd[1]: Started grabador.service - Grabador de video.", T_OK), 14), 82, 100, still=1)

narr(a, [
    (0, 25, "La misma señal que manda kill PID, pero la manda systemd y espera la respuesta.", None),
    (25, 50, "Un programa que atrapa SIGTERM cierra sus archivos antes de salir.", a.OK),
    (50, 75, "SIGKILL queda como último recurso, y systemd lo deja anotado.", a.BAD),
    (75, 100, "systemctl status muestra el PID nuevo y desde cuándo corre.", a.OK),
], y=642, still_idx=3)

escribir(a, "10-l2", "systemctl restart: pedir, esperar y recién ahí forzar",
         "Animación en cuatro tiempos en forma de diagrama de secuencia, con cuatro columnas: vos con sudo systemctl, systemd, el servicio de ejemplo grabador.service con PID 1502 y el journal; abajo, journalctl -u grabador. "
         "1: restart grabador llega a systemd, que le manda SIGTERM (15) al proceso, y el journal anota Stopping. "
         "2: el grabador cierra video.mp4, sale, y el journal anota Deactivated successfully. "
         "3: el caso alternativo: si no saliera, systemd espera TimeoutStopSec, 90 segundos por defecto, y manda SIGKILL (9); el journal anotaría State stop-sigterm timed out. Killing. "
         "4: systemd lo arranca de nuevo con el PID 1733 y el journal anota Started grabador.service.",
         [10, 40, 64, 92])
