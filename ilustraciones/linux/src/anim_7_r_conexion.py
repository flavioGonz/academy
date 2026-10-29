#!/usr/bin/env python3
"""Lección 7 (Llave, no contraseña), Resumen: la primera conexión SSH completa. TCP al 22 e intercambio de
versiones; intercambio de claves (en OpenSSH 10, mlkem768x25519-sha256 por defecto, post cuántico) que arma un
secreto de sesión que no viaja, con la firma del servidor hecha con su llave de host; la primera vez, la huella
se confirma y queda en ~/.ssh/known_hosts; ya cifrado, la autenticación con la llave del usuario contra
authorized_keys. Fuentes: RFC 4253 (versiones, KEXINIT, NEWKEYS, firma de la llave de host), RFC 4252
(publickey), notas de versión de OpenSSH 10.0 (mlkem768x25519-sha256 por defecto) y la teoría de la lección."""
from _anims_lnx_rl import *

a = nueva(30, "LINUX · SSH · EN LA RED", "Primera conexión SSH: dos llaves, dos preguntas")
a.steps([
    "TCP al 22 y se presentan: SSH-2.0-OpenSSH_10.2 de cada lado.",
    "Intercambio de claves: arman un secreto que nunca viaja; el servidor firma.",
    "Primera vez: la huella del servidor se confirma y queda en known_hosts.",
    "Ya cifrado, tu llave prueba quién sos contra authorized_keys.",
], still=3)

N, S = 470, 1010
a.add(dev(a, N - 140, 166, 280, 66, "Notebook", "ssh tecnico@192.168.88.50", "laptop", ssize=14))
a.add(dev(a, S - 132, 166, 264, 66, "Servidor", "sshd · :22", "server", dark=True))
a.add(lifeline(a, N, 232, 534))
a.add(lifeline(a, S, 232, 534))

msg(a, N, S, 262, "TCP :22 · SSH-2.0-OpenSSH_...", 2, still=1, lsize=14)
msg(a, S, N, 290, "SSH-2.0-OpenSSH_10.2", 7, color=a.CYAN, still=1, lsize=14)
msg(a, N, S, 330, "KEXINIT · mlkem768x25519-sha256", 27, still=1, lsize=14)
msg(a, S, N, 358, "su parte + llave de host + firma", 33, color=a.CYAN, still=1, lsize=14)
en(a, a.box(N + 20, 372, S - N - 40, 34, a.SLATE, None, rx=8) + a.text((N + S) / 2, 395, "cada lado calcula el mismo secreto: no viaja", 15, a.INK, a.SANS, 700, "middle"), 39, 100, still=1)
msg(a, N, S, 434, "NEWKEYS: desde acá, todo cifrado", 62, color=a.OK, still=1, lsize=14)
msg(a, N, S, 476, "publickey ssh-ed25519 + firma", 77, still=1, lsize=14)
msg(a, S, N, 512, "USERAUTH_SUCCESS", 86, color=a.OK, still=1, lsize=14)
# candado de cifrado sobre las líneas de vida
en(a, a.box(N - 10, 448, 20, 90, a.OK, None, rx=6, extra='opacity=".25"') + a.box(S - 10, 448, 20, 90, a.OK, None, rx=6, extra='opacity=".25"'), 64, 100, still=1)

# notas a la izquierda
en(a, nota(a, 48, 300, 380, 124, "Primera vez: ¿confiás en este servidor?", ["ED25519 key fingerprint is SHA256:...", "Comparala con la del servidor; con yes", "queda en ~/.ssh/known_hosts."], "amb", 16, 15), 52, 100, still=1)
en(a, nota(a, 48, 440, 380, 96, "En el servidor", ["la pública está en authorized_keys:", "verifica la firma y te deja entrar."], "ok", 16, 15), 82, 100, still=1)
en(a, a.text(48, 280, "la llave privada no sale de la notebook", 15, a.TXT, a.SANS, 600), 76, 100, still=1)

# resumen: las dos llaves
SY = 552
a.add(a.box(48, SY, 540, 58, a.WHITE, a.LINE, rx=12) + glyph(a, "server", 64, SY + 13, a.BLUE, 1.3)
      + a.text(106, SY + 25, "llave de host del servidor", 15, a.INK, a.SANS, 700) + mono(a, 106, SY + 47, "→ ~/.ssh/known_hosts (notebook)", 14, a.BLUE, 600))
a.add(a.box(612, SY, 540, 58, a.WHITE, a.LINE, rx=12) + glyph(a, "key", 628, SY + 13, a.OK, 1.3)
      + a.text(670, SY + 25, "tu llave ed25519", 15, a.INK, a.SANS, 700) + mono(a, 670, SY + 47, "→ ~/.ssh/authorized_keys (servidor)", 14, a.OK, 600))
en(a, a.box(44, SY - 4, 548, 66, "none", a.AMB, rx=14, sw=3), 50, 75)
en(a, a.box(608, SY - 4, 548, 66, "none", a.OK, rx=14, sw=3), 75, 100, still=1)

narr(a, [
    (0, 25, "Antes de cualquier clave, los dos acuerdan versión y algoritmos.", None),
    (25, 50, "El intercambio de claves de OpenSSH 10 es post cuántico por defecto.", a.CYAN),
    (50, 75, "La huella protege contra un equipo que se haga pasar por el servidor.", a.AMB),
    (75, 100, "Con la sesión cifrada, la llave reemplaza a la contraseña: nada que adivinar.", a.OK),
], y=642, still_idx=3)

escribir(a, "7-r1", "Primera conexión SSH: dos llaves, dos preguntas",
         "Animación en cuatro tiempos en forma de diagrama de secuencia entre la notebook, que corre ssh tecnico@192.168.88.50, y el servidor con sshd en el puerto 22; abajo, las dos llaves. "
         "1: la conexión TCP al 22 y el intercambio de versiones, SSH-2.0-OpenSSH de cada lado. "
         "2: KEXINIT con mlkem768x25519-sha256; el servidor manda su parte, su llave de host y una firma, y cada lado calcula el mismo secreto, que no viaja. "
         "3: la primera vez, la notebook muestra la huella ED25519 SHA256 del servidor; se compara, con yes queda en ~/.ssh/known_hosts, y con NEWKEYS todo pasa a ir cifrado. "
         "4: la notebook manda publickey ssh-ed25519 con una firma hecha con la llave privada, que no sale de la notebook; el servidor encuentra la pública en authorized_keys, verifica la firma y responde USERAUTH_SUCCESS.",
         [10, 38, 62, 92])
