#!/usr/bin/env python3
"""Lección 5 · Laboratorio, paso 2: restart de ssh con PasswordAuthentication yess en un snippet.
ssh.service de Debian corre sshd -t como ExecStartPre; con el error, sshd -t escribe archivo y línea (al journal,
con la unidad ssh.service) y sale con 255; systemd no arranca sshd y deja la unidad en failed (Result: exit-code).
status y journalctl -u ssh muestran el motivo. Fuentes: teoría de la lección 3 y 4 (ssh.service corre sshd -t
antes de arrancar), systemd.exec/systemd.service (ExecStartPre, Result: exit-code) y el laboratorio."""
from _anims_lnx_rl import *

a = nueva(26, "LINUX · SYSTEMD · LABORATORIO", "restart con un error: qué pasa por dentro")
a.steps([
    "systemctl restart ssh: systemd para el servicio para volver a arrancarlo.",
    "Antes de arrancar corre sshd -t, que encuentra yess y lo escribe.",
    "sshd -t sale con 255: sshd no arranca y la unidad queda en failed.",
    "status y journalctl -u ssh muestran el motivo, con archivo y línea.",
], still=3)

X = {"vos": 140, "systemd": 430, "sshd": 720, "journal": 1010}
HEAD = {"vos": ("Vos", "consola de la VM"), "systemd": ("systemd", "PID 1"), "sshd": ("sshd -t", "ExecStartPre"), "journal": ("journald", "el journal")}
for k, x in X.items():
    t, s = HEAD[k]
    dark = k == "systemd"
    a.add(a.box(x - 120, 168, 240, 64, a.INK if dark else a.WHITE, None if dark else "#C2D4E6", rx=14)
          + a.text(x, 196, t, 18, "#FFFFFF" if dark else a.INK, a.SANS, 600, "middle") + a.text(x, 220, s, 14, LIGHT if dark else a.GREY, a.MONO, 500, "middle"))
    a.add(lifeline(a, x, 232, 470))

msg(a, X["vos"], X["systemd"], 270, "systemctl restart ssh", 4, still=1)
msg(a, X["systemd"], X["sshd"], 310, "ExecStartPre=/usr/sbin/sshd -t", 27, still=1, lsize=14)
en(a, a.box(X["sshd"] - 116, 318, 232, 50, a.BADBG, a.BAD, rx=10) + a.text(X["sshd"], 338, "lee 99-roto.conf", 15, a.BAD, a.SANS, 700, "middle")
   + a.text(X["sshd"], 360, "yess no es yes ni no", 15, a.INK, a.SANS, 500, "middle"), 31, 100, still=1)
msg(a, X["sshd"], X["journal"], 402, "line 1: unsupported option", 37, color=a.BAD, still=1, lsize=14)
msg(a, X["sshd"], X["systemd"], 430, "status=255/EXCEPTION", 52, color=a.BAD, still=1, lsize=14)
msg(a, X["systemd"], X["journal"], 462, "Failed with result 'exit-code'", 60, color=a.BAD, still=1, lsize=14)
en(a, a.pill(X["systemd"] - 136, 344, "failed", a.BAD, a.BADBG, 15, 30), 58, 100, still=1)
en(a, a.text(X["systemd"] - 136, 396, "sshd no arranca", 15, a.BAD, a.SANS, 700), 58, 100, still=1)

# ---- terminal con status y journal (paso 4)
TY = 482
T = tterm(a, 48, TY, 1104, 128)
T += trow(a, 48, TY + 28, "$ systemctl status ssh", 14)
T += trow(a, 48, TY + 50, ("  Active: failed (Result: exit-code)", T_ERR), 14)
T += trow(a, 48, TY + 72, ("  Process: ExecStartPre=/usr/sbin/sshd -t (code=exited, status=255/EXCEPTION)", T_OUT), 14)
T += trow(a, 48, TY + 96, "$ sudo journalctl -u ssh -n 20", 14)
T += trow(a, 48, TY + 118, ('  sshd: /etc/ssh/sshd_config.d/99-roto.conf line 1: unsupported option "yess".', T_WARN), 14)
en(a, T, 76, 100, still=1)

narr(a, [
    (0, 25, "restart = stop + start: el servicio se baja aunque la configuración nueva esté rota.", None),
    (25, 50, "El validador corre igual que cuando lo usás a mano, y lo que dice queda en el journal.", a.AMB),
    (50, 75, "Sin sshd escuchando, nadie más entra por SSH: por eso este paso va desde la consola.", a.BAD),
    (75, 100, "status te da el resumen; journalctl -u ssh, el archivo y la línea para corregir.", a.OK),
], y=642, still_idx=3)

escribir(a, "5-l1", "restart con un error: qué pasa por dentro",
         "Animación en cuatro tiempos en forma de diagrama de secuencia, con cuatro columnas: vos en la consola de la VM, systemd, sshd -t como ExecStartPre y el journal. "
         "1: systemctl restart ssh llega a systemd, que baja el servicio para volver a arrancarlo. "
         "2: antes de arrancar, systemd corre /usr/sbin/sshd -t, que lee 99-roto.conf, encuentra yess, que no es yes ni no, y escribe line 1: unsupported option en el journal. "
         "3: sshd -t sale con status=255/EXCEPTION, systemd no arranca sshd, deja la unidad en failed y anota Failed with result exit-code. "
         "4: una terminal muestra systemctl status ssh con Active: failed (Result: exit-code) y el ExecStartPre con status 255, y journalctl -u ssh con la línea de /etc/ssh/sshd_config.d/99-roto.conf line 1: unsupported option yess.",
         [10, 38, 62, 92])
