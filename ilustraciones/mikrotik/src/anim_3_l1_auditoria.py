#!/usr/bin/env python3
"""Lección 3 (Cerrar puertas) · Laboratorio paso 3: lo que deja adentro un equipo tomado (Mēris) y qué print lo muestra."""
from _anim_r20_31 import *

a, _ = nuevo(24, "MIKROTIK · CERRAR PUERTAS · PASO 3", "Un equipo tomado sigue tomado después de actualizar",
             ["Una tarea del scheduler hace fetch y baja un script de un dominio ajeno.",
              "El script prende SOCKS en el 5678 y una regla de input que lo acepta.",
              "Desde afuera usan el router de proxy; un cliente L2TP propio llama al atacante.",
              "Cada print de la auditoría muestra una de esas piezas."], still=3)

# router heredado
a.add(a.box(48, 178, 552, 392, a.INK, rx=18))
a.add(a.text(70, 212, "Router heredado", 20, a.WHITE, a.HEAD, 600))
a.add(a.text(250, 212, "RouterOS ya actualizado, misma config", 15, SKY, a.MONO))
ROWS = [("/system/scheduler", "tarea: fetch + import"),
        ("/system/script", "script que nadie conoce"),
        ("/ip/socks", "enabled=yes port=5678"),
        ("/ip/firewall/filter", "accept dst-port=5678"),
        ("/interface/l2tp-client", "name=lvpn, dominio ajeno")]
Y0, DY, RH = 236, 64, 52
ry = []
for i, (path, desc) in enumerate(ROWS):
    y = Y0 + i * DY
    ry.append(y + RH / 2)
    a.add(a.box(66, y, 516, RH, a.NAVY2, rx=10))
    a.add(a.text(84, y + 32, path, 15, a.WHITE, a.MONO, 600))
    a.add(a.text(318, y + 32, desc, 15, SKY, a.MONO))

def lit(i, t0, t1=100, col=None, still=0):
    en(a, ring(a, 63, Y0 + i * DY - 3, 522, RH + 6, col or a.BAD, rx=12, sw=3), t0, t1, still)

# lado de afuera
afuera = (dev(a, 820, 190, 332, 96, "Servidor del atacante", "dominio desconocido", "detrás de un proxy web", kind="bad", ssize=14, add=False)
          + dev(a, 820, 330, 332, 84, "Cliente del proxy", "usa tu router de salida", kind="bad", ssize=14, add=False)
          + dev(a, 820, 458, 332, 96, "Internet", "el tráfico sale con la IP", "pública del cliente", kind="isp", ssize=14, add=False))
en(a, afuera, 0, 76)

# 1. scheduler → fetch → script
lit(0, 2, 25)
go(a, "fetch", [(600, ry[0]), (790, ry[0]), (790, 250), (820, 250)], 4, 10, hold=1, bg=a.AMB, size=14)
go(a, "script", [(820, 270), (700, 270), (700, ry[1]), (600, ry[1])], 13, 20, hold=3, bg=a.BAD, size=14)
lit(1, 20, 25)

# 2. el script prende SOCKS y la regla
lit(1, 25, 50)
lit(2, 30, 75)
lit(3, 36, 75)
en(a, a.text(700, ry[2] - 4, "abre el 5678", 15, a.BAD, a.MONO, 600, "middle"), 32, 50)

# 3. proxy y túnel
go(a, "pedido", [(820, 372), (650, 372), (650, ry[2]), (600, ry[2])], 52, 58, hold=1, bg=a.BAD, size=14)
go(a, "con tu IP", [(600, ry[2] + 14), (760, ry[2] + 14), (760, 506), (820, 506)], 59, 66, hold=4, bg=a.GREY, size=14)
lit(4, 62, 75)
en(a, poly([(600, ry[4]), (790, ry[4]), (790, 262), (816, 262)], a.BAD, 3, "8 6"), 64, 75)
en(a, a.text(800, ry[4] + 30, "lvpn sale solo, hacia afuera", 15, a.BAD, a.MONO, 600), 64, 75)

# 4. auditoría: cada print encuentra una pieza
for i in range(5):
    t = 77 + i * 3.5
    lit(i, t, 100, a.AMB, still=1)
en(a, mono_box(a, 640, 196, 512, [
    "/system/scheduler/print",
    "/system/script/print",
    "/ip/socks/print",
    "/ip/firewall/filter/print",
    "  where dst-port~\"5678\"",
    "/interface/l2tp-client/print"], "La auditoría del paso 3", "amb", size=15, lh=26)
   + note(a, 640, 430, 512, 126, "Si algo no lo reconoce nadie", ["Va al legajo y se deshabilita. Contraseña", "nueva para todos los usuarios y revisión", "del firewall."], "bad"), 76, 100, still=1)

narr(a, [
    (0, 25, "Actualizar corrige la falla, pero no borra lo que el atacante configuró.", a.TXT),
    (25, 50, "Son funciones normales de RouterOS: nada avisa que están ahí.", a.BAD),
    (50, 75, "El enlace del cliente queda trabajando para otro, y con su IP pública.", a.BAD),
    (75, 100, "Cinco prints alcanzan para saber si el equipo es tuyo de verdad.", a.AMB),
], still_idx=3)

escribir(a, "3-l1.svg", "Auditoría de un equipo heredado",
         "Animación en cuatro tiempos con un router heredado, ya actualizado pero con la configuración que dejó un atacante, y del lado de afuera el servidor del atacante, "
         "un cliente que usa el router de proxy e internet. Adentro del router hay cinco piezas: una tarea del scheduler, un script desconocido, SOCKS habilitado en el puerto 5678, "
         "una regla de input que acepta el 5678 y un cliente L2TP llamado lvpn. 1: la tarea del scheduler hace fetch a un dominio ajeno y baja un script. "
         "2: el script prende SOCKS en el 5678 y la regla que lo acepta. 3: desde afuera mandan pedidos al 5678 y salen a internet con la IP pública del cliente; "
         "el cliente L2TP lvpn llama solo hacia el atacante. 4: los cinco prints de la auditoría del paso 3 marcan cada una de esas piezas; lo que nadie reconoce va al legajo, "
         "se deshabilita y se cambian todas las contraseñas.",
         [12, 18, 40, 62, 88])
