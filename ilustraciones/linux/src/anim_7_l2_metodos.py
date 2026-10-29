#!/usr/bin/env python3
"""Lección 7 · Laboratorio, paso 4: probar desde otra terminal que la contraseña ya no entra.
El cliente pregunta con el método none y el servidor contesta qué métodos acepta: antes publickey,password; con
PasswordAuthentication no y KbdInteractiveAuthentication no, solo publickey. Con -o PubkeyAuthentication=no el
cliente no tiene qué ofrecer y sale Permission denied (publickey); sin -o, la llave entra.
Fuentes: RFC 4252 (método none, USERAUTH_FAILURE con la lista de métodos, publickey), sshd_config(5) y el laboratorio."""
from _anims_lnx_rl import *

a = nueva(28, "LINUX · SSH · LABORATORIO", "Qué métodos ofrece el servidor, antes y después")
a.steps([
    "Antes: el cliente pregunta con none y el servidor ofrece publickey,password.",
    "Con el archivo 10-ies-acceso.conf y reload, solo queda publickey.",
    "Con -o PubkeyAuthentication=no no hay qué ofrecer: Permission denied.",
    "Sin el -o, la llave entra: recién ahí cerrás la sesión A.",
], still=2)

C, S = 300, 900
a.add(dev(a, C - 150, 166, 300, 66, "Terminal B", "nueva, desde la notebook", "laptop", ssize=14))
a.add(dev(a, S - 150, 166, 300, 66, "Servidor", "sshd · 192.168.88.50", "server", dark=True, ssize=14))
a.add(lifeline(a, C, 232, 440))
a.add(lifeline(a, S, 232, 440))

def fase(t0, t1, lista, col, extra, still=0):
    msg(a, C, S, 276, "userauth: método none", t0 + 2, end=t1, still=still, lsize=15)
    msg(a, S, C, 316, f"FAILURE · puede seguir: {lista}", t0 + 7, end=t1, color=col, still=still, lsize=15)
    extra(t0, t1, still)


def f1(t0, t1, st):
    msg(a, C, S, 356, "password", t0 + 13, end=t1, color=a.AMB, still=st, lsize=15)
    en(a, a.text(C - 150, 376, "la contraseña todavía sirve", 15, a.AMB, a.SANS, 700), t0 + 15, t1, st)


def f2(t0, t1, st):
    en(a, nota(a, S + 20, 252, 236, 150, "10-ies-acceso.conf", ["PasswordAuthentication no", "KbdInteractive... no", "PermitRootLogin no", "sshd -t && reload"], "ok", 15, 15), t0 + 1, t1, st)


def f3(t0, t1, st):
    en(a, a.box(C - 150, 340, 260, 74, a.BADBG, a.BAD, rx=10) + a.text(C - 134, 366, "PubkeyAuthentication=no:", 15, a.BAD, a.MONO, 600)
       + a.text(C - 134, 392, "no tiene qué ofrecer", 15, a.INK, a.SANS, 600), t0 + 12, t1, st)


def f4(t0, t1, st):
    msg(a, C, S, 356, "publickey ssh-ed25519 + firma", t0 + 11, end=t1, still=st, lsize=15)
    msg(a, S, C, 396, "SUCCESS", t0 + 16, end=t1, color=a.OK, still=st, lsize=15)


fase(0, 25, "publickey,password", a.AMB, f1)
f2(25, 100, 1)
fase(50, 75, "publickey", a.OK, f3, still=1)
fase(75, 100, "publickey", a.OK, f4)
en(a, a.text(S + 20, 430, "de fábrica (ejemplo Debian/Ubuntu)", 14, a.GREY, a.SANS, 500), 0, 25)

# terminal B
TY = 456
a.add(tterm(a, 48, TY, 1104, 140, "TERMINAL B"))
def filas(rows, t0, t1, still=0):
    en(a, "".join(trow(a, 48, TY + 54 + i * 26, r, 15) for i, r in enumerate(rows)), t0, t1, still)


filas(["$ ssh tecnico@192.168.88.50", ("tecnico@192.168.88.50's password:      # si no hay llave, la pide", T_WARN)], 0, 25)
filas([("# en la sesión A, que sigue abierta:", T_COM), "$ sudo sshd -t && sudo systemctl reload ssh"], 25, 50)
filas(["$ ssh -o PubkeyAuthentication=no tecnico@192.168.88.50", ("tecnico@192.168.88.50: Permission denied (publickey).", T_ERR),
       ("# lo que querés ver: sin llave, rechazado", T_COM)], 50, 75, still=1)
filas(["$ ssh tecnico@192.168.88.50", ("tecnico@servidor:~$", T_OK), ("# con llave, adentro: ahora sí podés cerrar la sesión A", T_COM)], 75, 100)

narr(a, [
    (0, 25, "El servidor dice qué métodos acepta antes de que pruebes ninguno.", None),
    (25, 50, "El archivo propio apaga las dos puertas de contraseña.", a.OK),
    (50, 75, "Entre paréntesis, el error dice qué métodos quedan: solo publickey.", a.OK),
    (75, 100, "Si B no entrara con la llave, desde A corregís sin quedar afuera.", a.AMB),
], y=640, still_idx=2)

escribir(a, "7-l2", "Qué métodos ofrece el servidor, antes y después",
         "Animación en cuatro tiempos en forma de diagrama de secuencia entre la terminal B, nueva, y el servidor 192.168.88.50; abajo, lo que muestra la terminal. "
         "1: antes del cambio, el cliente pregunta con el método none y el servidor contesta que puede seguir con publickey,password: la contraseña todavía sirve. "
         "2: en la sesión A, el archivo 10-ies-acceso.conf con PasswordAuthentication no, KbdInteractiveAuthentication no y PermitRootLogin no, sshd -t y reload. "
         "3: con ssh -o PubkeyAuthentication=no, el servidor solo ofrece publickey, el cliente no tiene qué ofrecer y sale Permission denied (publickey): sin llave, rechazado. "
         "4: sin el -o, el cliente manda publickey ssh-ed25519 con la firma, el servidor responde SUCCESS y se entra; recién ahí se cierra la sesión A.",
         [10, 38, 62, 92])
