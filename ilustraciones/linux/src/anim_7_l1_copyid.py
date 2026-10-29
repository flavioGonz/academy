#!/usr/bin/env python3
"""Lección 7 · Laboratorio, paso 2: ssh-copy-id tecnico@192.168.88.50. Toma la llave pública, entra una última
vez con la contraseña del servidor (antes prueba si la llave ya estaba), agrega la línea al final de
~/.ssh/authorized_keys del usuario (crea ~/.ssh y el archivo con permisos restringidos si faltan) y desde ahí ssh entra
con la llave. La privada no se copia. Fuentes: ssh-copy-id(1), teoría y laboratorio de la lección (700 y 600)."""
from _anims_lnx_rl import *

a = nueva(26, "LINUX · SSH · LABORATORIO", "ssh-copy-id: la pública viaja, la privada se queda")
a.steps([
    "ssh-copy-id toma tu pública: ~/.ssh/id_ed25519.pub.",
    "Entra una última vez con la contraseña del servidor.",
    "Agrega tu línea al final de ~/.ssh/authorized_keys de tecnico.",
    "ssh tecnico@192.168.88.50 ya entra con la llave, sin esa contraseña.",
], still=2)

# notebook
a.add(a.box(48, 170, 400, 270, a.WHITE, "#C2D4E6", rx=16) + glyph(a, "laptop", 66, 184, a.BLUE) + a.text(110, 206, "Notebook del técnico", 18, a.INK, a.HEAD, 600))
a.add(a.box(68, 236, 360, 70, a.BADBG, a.BAD, rx=10, sw=2) + glyph(a, "lock", 82, 254, a.BAD, 1.2) + mono(a, 120, 264, "~/.ssh/id_ed25519", 15, a.BAD, 700)
      + a.text(120, 290, "privada · 600 · no se copia", 15, a.INK, a.SANS, 500))
a.add(a.box(68, 322, 360, 70, a.OKBG, a.OK, rx=10, sw=2) + glyph(a, "key", 82, 340, a.OK, 1.2) + mono(a, 120, 350, "~/.ssh/id_ed25519.pub", 15, a.OK, 700)
      + a.text(120, 376, "pública · se puede mostrar", 15, a.INK, a.SANS, 500))
en(a, a.box(62, 316, 372, 82, "none", a.BLUE, rx=13, sw=3), 4, 25)
a.add(a.text(68, 424, "la frase de paso protege la privada acá", 15, a.GREY, a.SANS, 500))

# servidor
SX = 752
a.add(a.box(SX, 170, 400, 270, a.INK, None, rx=16) + glyph(a, "server", SX + 18, 184, a.CYAN) + a.text(SX + 62, 206, "Servidor 192.168.88.50", 18, "#FFFFFF", a.HEAD, 600))
a.add(mono(a, SX + 20, 252, "/home/tecnico/.ssh/   700", 15, LIGHT, 600))
a.add(a.box(SX + 20, 266, 360, 150, "#0B3A66", None, rx=10) + mono(a, SX + 34, 292, "authorized_keys   600", 15, "#FFFFFF", 700))
en(a, mono(a, SX + 34, 322, "(vacío o con otras llaves)", 14, LIGHT, 500), 0, 52)
en(a, mono(a, SX + 34, 330, "ssh-ed25519 AAAAC3NzaC1lZDI1", 14, MINT, 700) + mono(a, SX + 34, 352, "NTE5AAAA...", 14, MINT, 700)
   + mono(a, SX + 34, 374, "tecnico@notebook-2026", 14, MINT, 700), 58, 100, still=1)
en(a, a.box(SX + 24, 308, 352, 78, "none", GOLD, rx=8, sw=2.5), 58, 75, still=1)
en(a, a.text(SX + 34, 404, "una línea por llave, al final", 14, GOLD, a.SANS, 700), 58, 75, still=1)

# canal
a.add(camino(f"M448 300 H{SX}", "#C2D4E6", 4))
viaje(a, "contraseña del servidor", [(500, 288), (SX - 110, 288)], 30, 40, bg=a.AMB, size=14, hold=6)
en(a, a.text(600, 330, "una sola vez, cifrada por SSH", 15, a.AMB, a.SANS, 700, "middle"), 30, 50)
viaje(a, "id_ed25519.pub", [(500, 300), (SX - 90, 300)], 52, 58, bg=a.OK, size=14, hold=1)
viaje(a, "firma con la privada", [(500, 300), (SX - 110, 300)], 78, 84, bg=a.BLUE, size=14, hold=4)
en(a, a.text(600, 336, "la privada firma, no viaja", 15, a.BLUE, a.SANS, 700, "middle"), 78, 100)

# terminal
TY = 456
a.add(tterm(a, 48, TY, 1104, 150))
def filas(rows, t0, t1, still=0):
    en(a, "".join(trow(a, 48, TY + 32 + i * 26, r, 15) for i, r in enumerate(rows)), t0, t1, still)


filas(["$ ssh-copy-id tecnico@192.168.88.50", ("Source of key(s) to be installed: \"/home/tecnico/.ssh/id_ed25519.pub\"", T_OUT)], 0, 25)
filas(["$ ssh-copy-id tecnico@192.168.88.50", ("... attempting to log in with the new key(s), to filter out any that are already installed", T_COM),
       ("tecnico@192.168.88.50's password:", T_WARN)], 25, 50)
filas(["$ ssh-copy-id tecnico@192.168.88.50", ("tecnico@192.168.88.50's password:", T_OUT), ("Number of key(s) added: 1", T_OK)], 50, 75, still=1)
filas(["$ ssh tecnico@192.168.88.50", ("Enter passphrase for key '/home/tecnico/.ssh/id_ed25519':", T_OUT),
       ("# la frase de paso es local: no viaja", T_COM), ("tecnico@servidor:~$", T_OK)], 75, 100)

narr(a, [
    (0, 25, "Al servidor solo va la pública: con ella no se puede entrar a ningún lado.", None),
    (25, 50, "Si la llave ya estaba, no la duplica; si no, usa la contraseña por última vez.", a.AMB),
    (50, 75, "Crea ~/.ssh y authorized_keys con los permisos que SSH exige si faltaban.", a.OK),
    (75, 100, "Si no entra con la llave, journalctl -fu ssh en el servidor dice por qué.", None),
], y=640, still_idx=2)

escribir(a, "7-l1", "ssh-copy-id: la pública viaja, la privada se queda",
         "Animación en cuatro tiempos. A la izquierda, la notebook con ~/.ssh/id_ed25519, la privada, con permisos 600, que no se copia, y ~/.ssh/id_ed25519.pub, la pública. "
         "A la derecha, el servidor 192.168.88.50 con /home/tecnico/.ssh en 700 y authorized_keys en 600; abajo, la terminal. "
         "1: ssh-copy-id toma la pública. "
         "2: prueba si la llave ya estaba instalada y, como no, pide una última vez la contraseña del servidor, que viaja cifrada por SSH. "
         "3: la pública viaja y queda como una línea al final de authorized_keys: ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA y el comentario tecnico@notebook-2026; la terminal dice Number of key(s) added: 1. "
         "4: ssh tecnico@192.168.88.50 pide la frase de paso de la llave, que es local y no viaja, la privada firma y se entra sin la contraseña del servidor.",
         [10, 38, 64, 92])
