#!/usr/bin/env python3
"""Lección 1 · Laboratorio, paso 3: el instalador de UniFi OS Server muestra la dirección de acceso (https, IP de la VM
y puerto); la notebook la abre, se crea el admin local y se entra a UniFi Network para anotar las dos versiones.
Fuente: lab.md de la lección (paso 3 y paso 4) e idea_md (Network 11 pide UniFi OS 6.0 o superior).
El puerto no se dibuja con número porque lo indica el instalador."""
from _anim_red_unifi import *  # noqa

a = new(24, "Quién manda", "Primer acceso: la dirección, el admin local y las versiones", [
    "El instalador termina y muestra la dirección: https, la IP de la VM y el puerto.",
    "La notebook abre esa dirección: la conexión va cifrada por HTTPS hasta la VM.",
    "Creás el admin local: el usuario queda en el server, con tu contraseña.",
    "Entrás a UniFi Network y anotás la versión de UniFi OS y la de Network.",
], still=3, paso=3)

NB, VM = 168, 690
a.add(dev(a, 48, 180, 240, 86, "Notebook", "del técnico", icon="laptop"))
a.add(dev(a, 500, 180, 380, 108, "VM Ubuntu 24.04", "UniFi OS Server", icon="server", dark=True, sub2="10.10.10.5"))
lifeline(a, NB, 266, 590)
lifeline(a, VM, 288, 590)

# 1 · el instalador
s0, s1 = ph(a, 0)
during(a, term(a, 900, 180, 252, ["sudo ./<instalador>", "...", "Listo. Abrí:", "https://10.10.10.5", ":<puerto>"],
               colors={3: GOLD, 4: GOLD}), 0, s1, still=0)
go(a, [(880, 236), (900, 236)], s0 + 3, s0 + 5, inner=dot(a, GOLD), hold=s0 + 6)

# 2 · HTTPS
s0, s1 = ph(a, 1)
msg(a, NB, VM, 340, "https://10.10.10.5:<puerto>", s0 + 2, end=100, still=1, sub="TLS: la sesión va cifrada")
msg(a, VM, NB, 412, "página de UniFi OS", s0 + 12, end=100, still=1, color=a.OK)

# 3 · admin local
s0, s1 = ph(a, 2)
msg(a, NB, VM, 470, "crear admin local", s0 + 2, end=100, still=1, color=a.BLUE)
during(a, a.box(900, 300, 252, 130, a.WHITE, a.LINE, rx=14)
       + a.text(920, 334, "Admin local", 18, a.INK, a.SANS, 600)
       + a.text(920, 362, "usuario propio", 15, a.TXT, a.MONO)
       + a.text(920, 386, "contraseña anotada", 15, a.TXT, a.MONO)
       + a.text(920, 410, "en la ficha", 15, a.TXT, a.MONO), s0 + 5, 100, still=1)
during(a, check(a, 1136, 300, 15), s0 + 5, 100, still=1)

# 4 · UniFi Network y versiones
s0, s1 = ph(a, 3)
msg(a, NB, VM, 530, "abrir UniFi Network", s0 + 2, end=100, still=1)
msg(a, VM, NB, 580, "versiones de UniFi OS y Network", s0 + 10, end=100, still=1, color=a.OK)
during(a, a.box(900, 446, 252, 144, "#EEF4FA", a.LINE, rx=14)
       + a.text(920, 478, "Planilla del sitio", 17, a.INK, a.SANS, 600)
       + a.text(920, 508, "UniFi OS:  anotada", 15, a.INK, a.MONO)
       + a.text(920, 534, "Network:   anotada", 15, a.INK, a.MONO)
       + a.text(920, 566, "Network 11 → OS 6.0+", 15, a.AMB, a.MONO, 600), s0 + 14, 100, still=1)

status(a, 640, [
    (0, 25, "La dirección exacta la da el instalador: copiala tal cual, con el puerto.", a.INK, 0),
    (25, 50, "Todo pasa entre tu notebook y la VM: el server es tuyo, en tu red.", a.INK, 0),
    (50, 75, "El admin local entra aunque no haya internet: guardalo en la ficha.", a.OK, 0),
    (75, 100, "Las dos versiones dicen qué notas leer antes de actualizar.", a.INK, 1),
])

write(a, 1, "l1", "Primer acceso a UniFi OS Server",
      "Animación en cuatro tiempos del paso 3 entre la notebook del técnico y la VM Ubuntu 24.04 con UniFi OS Server en 10.10.10.5. "
      "1: el instalador termina y muestra la dirección de acceso: https, la IP de la VM y el puerto que indique. "
      "2: la notebook abre esa dirección por HTTPS, la sesión va cifrada hasta la VM y vuelve la página de UniFi OS. "
      "3: se crea el admin local con usuario propio y la contraseña anotada en la ficha; queda guardado en el server. "
      "4: se abre UniFi Network, se leen la versión de UniFi OS y la de Network y se anotan en la planilla del sitio; Network 11 pide UniFi OS 6.0 o superior.",
      [12, 40, 65, 92])
