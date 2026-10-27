#!/usr/bin/env python3
"""Lección 41 · Teoría · Equipo viejo: del firmware al reemplazo.
Sale de teoria_md (Cómo funciona): identificar por A.B.C.D (A = modelo, 111 es E11; C de 10 o más = rama de
alta seguridad, que cifra la comunicación, los comandos de apertura y el guardado de contraseñas), asegurar
mientras siga instalado, y reemplazar con un equipo vigente del mismo tipo que pase la tabla de métodos de
acceso y la de alimentación. Firmwares mínimos para SR01 y patentes."""
from _anim_akuvox_29_42 import new, out, box, travel, when, check

a = new(24, "PARQUE INSTALADO", "Equipo viejo: del firmware al reemplazo")
a.steps([
    "El bloque A dice el modelo: 111 es un E11, un portero.",
    "El bloque C dice la rama: de 10 en adelante, alta seguridad.",
    "El reemplazo vigente, del mismo tipo, pasa por la tabla de métodos de acceso.",
    "Y por la tabla de alimentación: recién ahí es un reemplazo con datos.",
], still=3)

# firmware A.B.C.D
FW = [("111", "A · modelo"), ("B", "B · OEM"), ("C", "C · rama"), ("D", "D · versión")]
for i, (v, lbl) in enumerate(FW):
    x = 48 + i * 122
    a.add(a.box(x, 184, 96, 60, a.WHITE, a.LINE, rx=12))
    a.add(a.text(x + 48, 223, v, 22, a.INK, a.MONO, 600, "middle"))
    a.add(a.text(x + 48, 270, lbl, 15, a.GREY, a.MONO, 400, "middle"))
    if i:
        a.add(a.text(x - 13, 226, ".", 22, a.GREY, a.MONO, 600, "middle"))
when(a, f'<rect x="48" y="184" width="96" height="60" rx="12" fill="none" stroke="{a.CYAN}" stroke-width="3.5"/>', 2, 25)
when(a, f'<rect x="292" y="184" width="96" height="60" rx="12" fill="none" stroke="{a.CYAN}" stroke-width="3.5"/>', 26, 50)
when(a, a.pill(560, 180, "111 → E11 · portero", a.INK, "#D7ECF8", 16, 30), 4, 100, still=1)
when(a, a.pill(560, 222, "C de 10 o más → rama de alta seguridad", a.OK, a.OKBG, 15, 30)
     + a.text(574, 276, "cifra la comunicación, los comandos de apertura", 15, a.TXT, a.MONO)
     + a.text(574, 298, "y el guardado de contraseñas", 15, a.TXT, a.MONO), 28, 100, still=1)

# tubería del reemplazo
a.add(f'<path d="M268 412 H1000" stroke="{a.LINE}" stroke-width="4" stroke-dasharray="8 7"/>')
a.add(box(48, 370, 220, 84, "E11R", "portero viejo", "bell"))


def gate(x, t1, t2):
    a.add(a.box(x, 352, 270, 120, a.WHITE, a.LINE, rx=16))
    a.add(a.text(x + 20, 384, t1, 18, a.INK, a.SANS, 600))
    a.add(a.text(x + 20, 410, t2[0], 15, a.GREY, a.MONO))
    a.add(a.text(x + 20, 432, t2[1], 15, a.GREY, a.MONO))


gate(320, "Tabla de métodos", ("¿acepta las credenciales", "que el edificio ya usa?"))
gate(640, "Tabla de alimentación", ("¿le sirven el PoE o la", "fuente que ya están?"))
a.add(box(960, 370, 192, 84, "Reemplazo", "con datos", "check"))

# candidato que viaja
CAND = "vigente · mismo tipo"
when(a, a.pill(158, 470, CAND, a.WHITE, a.BLUE, 15, 28, "middle"), 51, 56)
travel(a, (158, 484), (455, 500), 56, 62, CAND, a.WHITE, a.BLUE, hold=14)
when(a, check(a, 570, 352) + f'<rect x="320" y="352" width="270" height="120" rx="16" fill="none" stroke="{a.OK}" stroke-width="3"/>', 62, 100, still=1)
travel(a, (455, 500), (775, 500), 77, 83, CAND, a.WHITE, a.BLUE, hold=3)
when(a, check(a, 890, 352) + f'<rect x="640" y="352" width="270" height="120" rx="16" fill="none" stroke="{a.OK}" stroke-width="3"/>', 84, 100, still=1)
travel(a, (775, 500), (1044, 500), 86, 90, CAND, a.WHITE, a.OK, hold=10, still=1)
when(a, f'<rect x="958" y="368" width="196" height="88" rx="17" fill="none" stroke="{a.OK}" stroke-width="3"/>', 90, 100, still=1)

a.add(a.box(48, 534, 1104, 104, a.WHITE, a.LINE, rx=16))
a.add(a.text(72, 568, "Mientras siga en la pared: firmware al día, clave propia y VLAN de porteros, sin reenvío de puertos.", 17, a.INK, a.SANS, 600))
a.add(a.text(72, 598, "SR01, lectura de patentes y otras funciones piden un firmware mínimo que un equipo viejo", 17, a.TXT, a.SANS, 600))
a.add(a.text(72, 622, "puede no tener.", 17, a.TXT, a.SANS, 600))

out(a, 41, 1, "Equipo viejo: del firmware al reemplazo",
    "Animación en cuatro tiempos sobre un equipo viejo. Arriba, el firmware en cuatro bloques A.B.C.D. "
    "Tiempo 1: se resalta el bloque A, 111, que corresponde a un E11, un portero. "
    "Tiempo 2: se resalta el bloque C; de 10 en adelante es la rama de alta seguridad, que cifra la comunicación, los comandos de apertura y el guardado de contraseñas. "
    "Tiempo 3: un reemplazo vigente del mismo tipo sale del E11R y pasa por la tabla de métodos de acceso: acepta las credenciales que el edificio ya usa. "
    "Tiempo 4: pasa por la tabla de alimentación, le sirven el PoE o la fuente que ya están, y llega a reemplazo con datos. "
    "Abajo: mientras siga instalado, firmware al día, clave propia y VLAN de porteros sin reenvío de puertos; SR01 y patentes piden firmware mínimo.",
    [12, 40, 66, 95])
