"""Teoría lección 1: qué pide un cliente SMB de Windows 11 24H2 o Server 2025 al abrir una carpeta."""
from _awin import *

a = new(20, "Abrir una carpeta con Windows 11 24H2")
a.steps(["El cliente negocia SMB y exige firmar cada mensaje.",
         "NAS viejo que no firma: Windows no sigue.",
         "Sin usuario, como invitado: Pro 24H2 no entra.",
         "NAS al día y usuario propio: sesión firmada."], still=3)

XL, XR = 300, 900
a.add(card(a, 48, 190, 252, 330, "Windows 11", "24H2 · cliente SMB", dark=True))
a.add(card(a, 900, 190, 252, 330, "NAS o grabador", "\\\\IP\\carpeta"))
a.add(line(a, f"M{XL + 40} 200V510", a.LINE, 2, "6 6") + line(a, f"M{XR - 40} 200V510", a.LINE, 2, "6 6"))
a.add(a.text(68, 300, "Firma SMB:", 16, "#9FC3E3", a.SANS, 500) + a.text(68, 326, "obligatoria", 17, "#FFFFFF", a.MONO, 600))
a.add(a.text(68, 380, "Invitado:", 16, "#9FC3E3", a.SANS, 500) + a.text(68, 406, "deshabilitado", 17, "#FFFFFF", a.MONO, 600))
at(a, a.text(920, 300, "firmware viejo", 17, a.BAD, a.MONO, 600) + a.text(920, 326, "sin firma SMB", 16, a.GREY, a.SANS, 500), 25, 50, 0)
at(a, a.text(920, 300, "carpeta sin", 17, a.BAD, a.MONO, 600) + a.text(920, 326, "usuario", 17, a.BAD, a.MONO, 600), 50, 75, 0)
at(a, a.text(920, 300, "firmware al día", 17, a.OK, a.MONO, 600) + a.text(920, 326, "usuario propio", 16, a.GREY, a.SANS, 500), 75, 100, 1)


def msg(y, label, color, s, e, back=False, still=0):
    x1, x2 = (XR - 40, XL + 40) if back else (XL + 40, XR - 40)
    d = f"M{x1} {y}H{x2 + (8 if back else -8)}"
    at(a, a.arrow(d, color, 4) + a.text((XL + XR) / 2, y - 12, label, 16, color, a.MONO, 600, "middle"), s, e, still)


# 1: negociación con firma requerida (se ve en todo el ciclo)
msg(240, "negociar · firma requerida", a.BLUE, 0, 100, still=1)
# 2: NAS viejo sin firma
msg(300, "no firmo", a.BAD, 25, 50, back=True)
at(a, chip(a, 600, 330, "conexión cortada", "bad", anchor="middle"), 27, 50, 0)
# 3: invitado
msg(300, "sesión como invitado", a.BAD, 50, 75)
at(a, chip(a, 600, 330, "Pro 24H2: invitado deshabilitado", "bad", anchor="middle"), 52, 75, 0)
# 4: usuario propio y firma
msg(300, "firmo · ok", a.OK, 75, 100, back=True, still=1)
msg(370, "usuario y contraseña del NAS", a.OK, 77, 100, still=1)
msg(440, "carpeta abierta, mensajes firmados", a.OK, 80, 100, back=True, still=1)
at(a, a.box(900, 190, 252, 330, "none", a.OK, rx=14, sw=4), 80, 100, 1)
at(a, a.box(900, 190, 252, 330, "none", a.BAD, rx=14, sw=4), 25, 75, 0)
caption(a, 600, [(0, 25, "La firma prueba que cada mensaje viene de quien dice y no fue tocado en el camino.", None),
                 (25, 50, "Un equipo que no sabe firmar queda afuera: parece falla de red, pero el cable está bien.", a.BAD),
                 (50, 75, "Sin usuario no hay a quién atribuir la sesión: por eso se cortó el invitado en Pro.", a.BAD),
                 (75, 100, "Firmware al día y una cuenta propia del equipo: abre sin bajar la seguridad.", a.OK)], still=3)
write(a, "1-t1.svg", "Abrir una carpeta con Windows 11 24H2",
      "Animación en cuatro tiempos entre un Windows 11 24H2 a la izquierda y un NAS o grabador a la derecha. 1: el cliente negocia SMB y exige que cada mensaje vaya firmado. "
      "2: un NAS viejo responde que no firma y la conexión se corta. 3: si se intenta entrar como invitado, sin usuario, Windows 11 Pro 24H2 no lo permite. "
      "4: con el NAS actualizado y un usuario propio del equipo, el NAS firma, acepta el usuario y la carpeta abre con los mensajes firmados. El cuadro fijo muestra el caso que funciona.")
