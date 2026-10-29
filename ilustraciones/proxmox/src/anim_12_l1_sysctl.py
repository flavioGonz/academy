#!/usr/bin/env python3
"""Lección 12 · Laboratorio, paso 5: en Proxmox VE 9, systemd-sysctl ya no lee /etc/sysctl.conf. Un host que rutea
las VMs de una red interna (net.ipv4.ip_forward = 1 en sysctl.conf) pierde ese ajuste en el primer arranque
después del upgrade; se encuentra con grep y se mueve a /etc/sysctl.d/<NN>-<nombre>.conf.
Fuentes: guía de upgrade 8 a 9 ("systemd-sysctl no longer reads /etc/sysctl.conf", sysctl.d/<NN>-<name>.conf,
ejemplo de reenvío de paquetes), tarjeta de la lección (comandos del paso 5)."""
from _anim_pmx_red import *

a = new(24, "Upgrade y rescate", "sysctl.conf en la 9: el ajuste que se pierde", lab=True)
a.steps([
    "En la 8, al arrancar se lee sysctl.conf: ip_forward = 1, el host rutea.",
    "Upgrade a la 9 y reinicio: sysctl.conf ya no se lee. ip_forward = 0.",
    "El paso 5 lo encuentra: la línea sigue en sysctl.conf, sin efecto.",
    "Se mueve a /etc/sysctl.d/99-ies.conf y vuelve a aplicarse al arrancar.",
], still=2)

# archivos
FX, FY, FW = 48, 182, 400
files = [("/etc/sysctl.conf", 0), ("/etc/sysctl.d/*.conf", 1), ("/usr/lib/sysctl.d/*.conf", 2)]
for name, i in files:
    y = FY + i * 74
    a.add(a.box(FX, y, FW, 60, a.WHITE, a.LINE, rx=12) + a.text(FX + 18, y + 36, name, 16, a.INK, a.MONO, 600))
at(a, a.text(FX + FW - 18, FY + 36, "ip_forward = 1", 15, a.BLUE, a.MONO, 700, "end"), 0, 75, still=1)
at(a, a.box(FX - 3, FY - 3, FW + 6, 66, "none", a.BAD, rx=14, sw=2.5, extra='stroke-dasharray="8 6"'), 26, 75, still=1)
at(a, a.text(FX + FW - 18, FY + 36, "ya movido", 15, a.GREY, a.MONO, 600, "end"), 75, 100)
at(a, a.box(FX, FY + 74, FW, 60, a.OKBG, a.OK, rx=12, sw=2) + a.text(FX + 18, FY + 110, "/etc/sysctl.d/99-ies.conf", 15, a.OK, a.MONO, 700) + a.text(FX + FW - 16, FY + 110, "ip_forward=1", 15, a.OK, a.MONO, 700, "end"), 78, 100)

# systemd-sysctl
SX, SY = 500, 236
a.add(a.box(SX, SY, 200, 96, a.INK, rx=14) + a.text(SX + 100, SY + 40, "systemd-sysctl", 17, a.WHITE, a.MONO, 700, "middle"))
at(a, a.text(SX + 100, SY + 70, "Proxmox VE 8", 15, SKY, a.MONO, 400, "middle"), 0, 25)
at(a, a.text(SX + 100, SY + 70, "Proxmox VE 9", 15, GOLD, a.MONO, 600, "middle"), 25, 100, still=1)
# lecturas
go(a, "lee", [(FX + FW, FY + 30), (SX, SY + 30)], 3, 7, a.BLUE, hold=0.5)
go(a, "lee", [(FX + FW, FY + 104), (SX, SY + 50)], 5, 9, a.BLUE, hold=0.5)
at(a, xmark(a, (FX + FW + SX) / 2, FY + 30, 14) + a.text((FX + FW + SX) / 2, FY - 8, "no lo lee", 15, a.BAD, a.SANS, 700, "middle"), 30, 75, still=1)
go(a, "lee", [(FX + FW, FY + 104), (SX, SY + 50)], 29, 33, a.BLUE, hold=0.5)
go(a, "lee", [(FX + FW, FY + 104 + 60), (SX, SY + 50)], 80, 84, a.OK, hold=0.5)

# kernel
KX, KY = 730, 220
a.add(a.box(KX, KY, 422, 128, a.WHITE, a.LINE, rx=14) + a.text(KX + 20, KY + 34, "kernel del host", 17, a.INK, a.SANS, 600))
for t0, t1, v, col, st in [(0, 27, "1", a.OK, 0), (27, 86, "0", a.BAD, 1), (86, 100, "1", a.OK, 0)]:
    at(a, a.text(KX + 20, KY + 80, "net.ipv4.ip_forward =", 17, a.INK, a.MONO) + a.text(KX + 260, KY + 80, v, 24, col, a.MONO, 700), t0, t1, still=st)
at(a, a.text(KX + 20, KY + 110, "el host rutea", 15, a.OK, a.SANS, 600), 0, 27)
at(a, a.text(KX + 20, KY + 110, "el host no rutea, sin ningún aviso", 15, a.BAD, a.SANS, 600), 27, 86, still=1)
at(a, a.text(KX + 20, KY + 110, "rutea otra vez", 15, a.OK, a.SANS, 600), 86, 100)

# VMs detrás del host
a.add(dev(a, 730, 392, 200, 76, "VMs en vmbr1", "red interna", icon="server", tsize=17))
a.add(dev(a, 990, 392, 162, 76, "Internet", "", icon="cloud", tsize=17))
a.add(line(930, 430, 990, 430, a.LINE, 3))
go(a, "salida", [(830, 392), (830, 360), (1070, 360), (1070, 378)], 10, 16, a.OK, hold=1)
go(a, "salida", [(830, 392), (830, 368)], 40, 42, a.BAD, hold=6)
at(a, xmark(a, 870, 372, 13), 42, 75)
go(a, "salida", [(830, 392), (830, 360), (1070, 360), (1070, 378)], 88, 94, a.OK, hold=2)

# terminal
TX, TY, TW, TH = 48, 496, 1104, 104
a.add(a.box(TX, TY, TW, TH, a.INK, rx=12))
at(a, tline(a, TX + 18, TY + 34, "arranque del host en la 8: los ajustes de sysctl.conf se aplican", SKY)
   + tline(a, TX + 18, TY + 62, "VMs de vmbr1 → host → internet", a.WHITE), 0, 25)
at(a, tline(a, TX + 18, TY + 34, "upgrade a la 9 · reinicio", GOLD) + tline(a, TX + 18, TY + 62, "las VMs de vmbr1 se quedan sin salida", CORAL), 25, 50)
at(a, tline(a, TX + 18, TY + 34, "# cat /etc/sysctl.conf | grep -v '^#' | grep .", MINT) + tline(a, TX + 18, TY + 58, "net.ipv4.ip_forward=1", GOLD)
   + tline(a, TX + 18, TY + 84, "# ls /etc/sysctl.d/      (no hay nada con ese ajuste)", MINT), 50, 75, still=1)
at(a, tline(a, TX + 18, TY + 34, "# echo 'net.ipv4.ip_forward=1' > /etc/sysctl.d/99-ies.conf", MINT)
   + tline(a, TX + 18, TY + 58, "# sysctl --system", MINT) + tline(a, TX + 18, TY + 84, "y en cada arranque se vuelve a aplicar", SKY), 75, 100)

status(a, 634, [
    (0, 25, "Los ajustes del kernel se cargan al arrancar, desde archivos de configuración.", a.INK, 0),
    (25, 50, "El upgrade no avisa: el cambio aparece en el primer reinicio.", a.BAD, 0),
    (50, 75, "Por eso se revisa sysctl.conf antes del upgrade, sin comentarios ni líneas vacías.", a.AMB, 1),
    (75, 100, "En la 9, cada ajuste va en su archivo NN-nombre.conf dentro de /etc/sysctl.d/.", a.OK, 0),
])

write(a, 12, "l1", "sysctl.conf en la 9: el ajuste que se pierde",
      "Animación en cuatro tiempos con los archivos /etc/sysctl.conf, /etc/sysctl.d/*.conf y /usr/lib/sysctl.d/*.conf, el servicio systemd-sysctl, el valor net.ipv4.ip_forward del kernel del host y unas VMs en una red interna vmbr1 que salen a internet a través del host. "
      "1: en Proxmox VE 8, al arrancar systemd-sysctl lee sysctl.conf, que tiene ip_forward = 1, y el host rutea la salida de las VMs. "
      "2: después del upgrade a la 9 y el reinicio, systemd-sysctl ya no lee /etc/sysctl.conf; ip_forward queda en 0, el host deja de rutear sin ningún aviso y las VMs se quedan sin salida. "
      "3: el paso 5 lo encuentra: cat /etc/sysctl.conf | grep -v '^#' | grep . muestra net.ipv4.ip_forward=1, y en /etc/sysctl.d/ no hay nada con ese ajuste. "
      "4: el ajuste se mueve a /etc/sysctl.d/99-ies.conf, sysctl --system lo aplica, systemd-sysctl lo lee en cada arranque y el host vuelve a rutear.",
      [8, 36, 62, 66, 94])
