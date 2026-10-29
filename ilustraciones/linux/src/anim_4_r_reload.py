#!/usr/bin/env python3
"""Lección 4 (Copiá y validá), Resumen: el método completo sobre SSH sin perder la sesión.
Copia protegida del original, cambio en un snippet propio, sshd -t, reload (Debian: ExecReload corre sshd -t y
manda HUP al proceso principal, que relee la configuración; las sesiones abiertas son otros procesos y siguen),
y prueba desde una sesión nueva, que ya ve el Banner. Fuentes: teoría de la lección (ssh.service corre sshd -t antes
de recargar; reload no corta las sesiones abiertas) y sshd(8) (SIGHUP: relee la configuración)."""
from _anims_lnx_rl import *

a = nueva(28, "LINUX · SSH · CÓMO SE VE", "Cambiar SSH sin perder la sesión que funciona")
a.steps([
    "Copia del original sin permiso de escritura: tu punto de vuelta.",
    "El cambio va en 10-ies.conf; sshd -t lo lee como el servicio.",
    "reload: sshd -t otra vez y HUP al proceso principal; tu sesión sigue.",
    "Una sesión nueva entra con la configuración nueva: recién ahí cerrás.",
], still=2)

# ---- notebook y sesiones
a.add(dev(a, 48, 196, 250, 110, "Notebook", "técnico", "laptop", sub2="dos terminales"))
a.add(a.text(48, 340, "sesión A", 15, a.OK, a.MONO, 700) + a.text(48, 362, "la que funciona:", 15, a.TXT, a.SANS, 500)
      + a.text(48, 384, "no se cierra", 15, a.TXT, a.SANS, 500))
en(a, a.text(48, 420, "sesión B", 15, a.BLUE, a.MONO, 700) + a.text(48, 442, "nueva, para probar", 15, a.TXT, a.SANS, 500), 75, 100)

# ---- servidor
SX, SY, SW, SH = 360, 170, 792, 344
a.add(a.box(SX, SY, SW, SH, a.WHITE, "#C2D4E6", rx=18) + a.text(SX + 22, SY + 34, "Servidor 192.168.88.50", 18, a.INK, a.HEAD, 600))
a.add(a.text(SX + 22, SY + 64, "archivos", 15, a.GREY, a.SANS, 600) + a.text(SX + 452, SY + 64, "procesos", 15, a.GREY, a.SANS, 600))

FXx = SX + 22
def fbox(y, name, perm, color=None, extra=""):
    return (a.box(FXx, y, 400, 52, a.SLATE, color, rx=10, sw=2 if color else 0) + mono(a, FXx + 16, y + 22, name, 15, a.INK, 700)
            + mono(a, FXx + 16, y + 43, perm, 14, color or a.GREY, 500) + extra)


a.add(fbox(SY + 78, "/etc/ssh/sshd_config", "-rw-r--r--  del paquete"))
en(a, fbox(SY + 142, "sshd_config.original", "-r--r--r--  sin escritura", a.BLUE), 6, 100, still=1)
en(a, fbox(SY + 206, "sshd_config.d/10-ies.conf", "Banner /etc/issue.net", a.OK), 28, 100, still=1)
viaje(a, "cp", [(FXx + 200, SY + 104), (FXx + 200, SY + 168)], 3, 6, bg=a.BLUE, size=14, hold=1)
# sshd -t lee los archivos
en(a, a.pill(FXx, SY + 276, "sshd -t", "#FFFFFF", a.INK, 15, 30) + a.text(FXx + 104, SY + 297, "sin salida = sin errores", 15, a.OK, a.SANS, 700), 34, 50)
en(a, a.pill(FXx, SY + 276, "sshd -t", "#FFFFFF", a.INK, 15, 30) + a.text(FXx + 104, SY + 297, "ExecReload, antes del HUP", 15, a.OK, a.SANS, 700), 52, 62)
en(a, a.box(FXx - 6, SY + 72, 412, 192, "none", a.OK, rx=12, sw=2.5, extra='stroke-dasharray="7 5"'), 34, 46)

# procesos
PX = SX + 452
a.add(a.box(PX, SY + 78, 318, 44, a.SLATE, None, rx=10) + mono(a, PX + 16, SY + 106, "systemd · PID 1", 15, a.INK, 700))
a.add(a.box(PX, SY + 142, 318, 60, a.INK, None, rx=10) + a.text(PX + 16, SY + 166, "sshd principal", 16, "#FFFFFF", a.SANS, 600)
      + mono(a, PX + 16, SY + 190, "escucha en :22", 14, LIGHT, 500))
a.add(a.box(PX + 30, SY + 222, 288, 46, a.OKBG, a.OK, rx=10) + mono(a, PX + 46, SY + 251, "sshd: tecnico · sesión A", 14, a.OK, 700))
en(a, a.box(PX + 30, SY + 282, 288, 46, "#E5F0FB", a.BLUE, rx=10) + mono(a, PX + 46, SY + 311, "sshd: tecnico · sesión B", 14, a.BLUE, 700), 82, 100)
a.add(camino(f"M{PX + 14} {SY + 202} V{SY + 245} H{PX + 30}", "#C2D4E6", 2.5))
en(a, camino(f"M{PX + 14} {SY + 245} V{SY + 305} H{PX + 30}", "#C2D4E6", 2.5), 82, 100)
# HUP
viaje(a, "HUP", [(PX + 250, SY + 100), (PX + 250, SY + 168)], 58, 61, bg=a.AMB, size=14, hold=1)
en(a, a.box(PX - 3, SY + 139, 324, 66, "none", GOLD, rx=12, sw=3) + a.text(PX + 170, SY + 190, "relee la config", 14, GOLD, a.SANS, 700), 61, 75, still=1)
en(a, a.text(PX + 30, SY + 300, "sigue conectada:", 15, a.OK, a.SANS, 700) + a.text(PX + 30, SY + 322, "es otro proceso", 15, a.TXT, a.SANS, 500), 62, 75, still=1)

# conexiones
a.add(camino(f"M298 236 H{SX}", a.OK, 4))
a.add(camino(f"M{SX} 236 H{SX + 10}", a.OK, 4))
en(a, camino(f"M298 276 C 330 276, 330 276, {SX} 276", a.BLUE, 4, "9 6"), 77, 100)
viaje(a, "SYN :22", [(310, 276), (SX - 40, 276)], 77, 80, bg=a.BLUE, size=13, hold=0.5)
en(a, a.box(48, 470, 290, 46, "#E5F0FB", a.BLUE, rx=10) + mono(a, 64, 499, "B ve el Banner: aplicado", 14, a.BLUE, 700), 84, 100)

# ---- terminal
TY = 530
a.add(tterm(a, 48, TY, 1104, 64))
def cmd(s, t0, t1, still=0, com=None):
    inner = trow(a, 48, TY + 38, s, 15)
    if com:
        inner += a.text(1136, TY + 38, com, 15, T_COM, a.MONO, 500, "end")
    en(a, inner, t0, t1, still)


cmd("$ sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.original; sudo chmod a-w ...original", 0, 25)
cmd("$ echo \"Banner /etc/issue.net\" | sudo tee .../sshd_config.d/10-ies.conf; sudo sshd -t", 25, 50)
cmd("$ sudo systemctl reload ssh", 50, 75, 1, "# desde la sesión A")
cmd("$ ssh tecnico@192.168.88.50", 75, 100, 0, "# desde la sesión B")

narr(a, [
    (0, 25, "El archivo del paquete queda igual y la copia no se pisa sin querer.", None),
    (25, 50, "sshd -t no dice nada si está bien; si hay un error, te da archivo y línea.", a.OK),
    (50, 75, "reload relee la configuración sin cortar las sesiones abiertas.", a.AMB),
    (75, 100, "Si B no entra, A sigue adentro para corregir: por eso no se cierra antes.", a.OK),
], still_idx=2)

escribir(a, "4-r1", "Cambiar SSH sin perder la sesión que funciona",
         "Animación en cuatro tiempos. A la izquierda, la notebook del técnico con la sesión A abierta, la que funciona; a la derecha, el servidor 192.168.88.50 con sus archivos y sus procesos, y abajo la terminal. "
         "1: cp copia /etc/ssh/sshd_config a sshd_config.original y chmod a-w la deja sin escritura, como punto de vuelta. "
         "2: el cambio va en sshd_config.d/10-ies.conf con Banner /etc/issue.net, y sshd -t lee los archivos sin decir nada: no hay errores. "
         "3: systemctl reload ssh: el servicio corre sshd -t otra vez y le manda HUP al sshd principal, que relee la configuración; el proceso de la sesión A es otro y sigue conectado. "
         "4: desde la sesión B, ssh tecnico@192.168.88.50 abre una conexión nueva al puerto 22, nace el proceso de la sesión B y aparece el Banner: el cambio está aplicado. Recién ahí se cierra la sesión vieja.",
         [10, 38, 64, 90])
