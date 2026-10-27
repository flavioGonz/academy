"""Teoría lección 5: el firewall evalúa perfil, puerto y origen para cada conexión entrante."""
from _awin import *

a = new(24, "Cómo decide el firewall una conexión entrante")
a.steps(["Placa en Privado, origen en la subred local: entra.",
         "Mismo puerto desde otra subred: el origen no coincide.",
         "La placa pasa a Público: la regla deja de actuar.",
         "Set-NetConnectionProfile a Privado: vuelve a entrar."], still=0)
# servidor con su placa y su regla
a.add(card(a, 760, 186, 392, 330, "Servidor del VMS", "escucha en 8443", dark=True))
a.add(a.text(784, 290, "Regla 'LAB VMS web 8443'", 16, "#FFFFFF", a.SANS, 600))
for i, s in enumerate(["TCP 8443 · entrante · permitir", "origen: LocalSubnet", "perfiles: Private, Domain"]):
    a.add(a.text(784, 322 + i * 28, s, 15, "#9FC3E3", a.MONO, 500))
a.add(a.text(784, 440, "Perfil de la placa:", 15, "#9FC3E3", a.SANS, 500))
at(a, chip(a, 940, 422, "Privado", "ok"), 0, 50, 1)
at(a, chip(a, 940, 422, "Público", "amb"), 50, 75, 0)
at(a, chip(a, 940, 422, "Privado", "ok"), 75, 100, 0)
# la pared del firewall
a.add(a.box(700, 186, 24, 330, a.SLATE, a.LINE, rx=8) + a.text(712, 540, "firewall", 15, a.GREY, a.MONO, 600, "middle"))
# clientes
a.add(card(a, 48, 200, 280, 96, "Puesto de monitoreo", "192.168.88.40 · misma subred"))
a.add(card(a, 48, 400, 280, 96, "Equipo de otra red", "10.20.0.5"))


def packet(y, s, e, ok, x_end=None):
    x_end = x_end or (728 if ok else 652)
    mv = a.move([(0, 330, y), (s, 330, y), (s + 10, x_end, y), (e, x_end, y), (100, x_end, y)])
    op = a.keyframes([(0, 0), (s, 0), (s + 0.5, 1), (e - 1, 1), (e, 0), (100, 0)])
    col = a.OK if ok else a.BAD
    a.add(a.group(f'<rect x="-34" y="-15" width="68" height="30" rx="15" fill="{col}"/><text x="0" y="6" font-family="{a.MONO}" font-size="15" font-weight="600" fill="#fff" text-anchor="middle">8443</text>', mv, op, still=0))


packet(248, 1, 25, True)
at(a, chip(a, 520, 196, "entra", "ok", anchor="middle"), 9, 25, 1)
at(a, a.arrow("M330 248H750", a.OK, 3, "8 6"), 0, 25, 1)
packet(448, 26, 50, False)
at(a, chip(a, 520, 396, "origen fuera de LocalSubnet", "bad", anchor="middle"), 34, 50, 0)
packet(248, 51, 75, False)
at(a, chip(a, 520, 196, "regla inactiva en Público", "bad", anchor="middle"), 59, 75, 0)
packet(248, 76, 100, True)
at(a, chip(a, 520, 196, "entra", "ok", anchor="middle"), 84, 100, 0)
caption(a, 610, [(0, 25, "La regla actúa: su perfil está activo y el origen está en la subred local del equipo.", a.OK),
                 (25, 50, "Mismo puerto, otro origen: no hay regla que lo permita, y lo entrante se bloquea.", a.BAD),
                 (50, 75, "El error clásico: la regla existe, pero la placa quedó como Pública.", a.BAD),
                 (75, 100, "Por eso se mira el perfil antes de culpar a la regla.", a.OK)], still=0)
write(a, "5-t1.svg", "Cómo decide el firewall una conexión entrante",
      "Animación en cuatro tiempos. A la derecha, un servidor del VMS que escucha en 8443 con la regla LAB VMS web 8443: TCP 8443 entrante, origen LocalSubnet, perfiles Private y Domain. "
      "A la izquierda, un puesto de monitoreo de la misma subred y un equipo de otra red. 1: con la placa en Privado, la conexión del puesto entra. "
      "2: la del equipo de otra red se bloquea porque el origen no está en la subred local. 3: la placa pasa a perfil Público y la misma conexión del puesto se bloquea porque la regla deja de actuar. "
      "4: con Set-NetConnectionProfile la placa vuelve a Privado y la conexión entra otra vez. El cuadro fijo muestra el primer caso.", pcts=(12, 37, 62, 90))
