"""Teoría lección 6: con NLA, la autenticación pasa antes de que el servidor arme la sesión."""
from _awin import *

a = new(20, "NLA: primero quién sos, después el escritorio")
a.steps(["El cliente llega al 3389 y arman un canal cifrado (TLS).",
         "Con NLA, las credenciales viajan antes de abrir sesión.",
         "Credencial válida: recién ahí el servidor arma el escritorio.",
         "Credencial mala: se corta sin dibujar ninguna pantalla."], still=2)
XL, XR = 330, 860
a.add(card(a, 48, 186, 250, 100, "Cliente RDP", "por VPN · por nombre", dark=True))
a.add(card(a, 892, 186, 260, 100, "Servidor del VMS", "3389 · NLA activa"))
a.add(line(a, f"M{XL} 200V540", a.LINE, 2, "6 6") + line(a, f"M{XR} 200V540", a.LINE, 2, "6 6"))


def msg(y, label, color, s, e, back=False, still=0):
    x1, x2 = (XR, XL + 8) if back else (XL, XR - 8)
    at(a, a.arrow(f"M{x1} {y}H{x2}", color, 4) + a.text((XL + XR) / 2, y - 12, label, 16, color, a.MONO, 600, "middle"), s, e, still)


# 1: TCP + TLS
at(a, a.box(XL, 236, XR - XL, 34, "#E5F0FB", None, rx=17) + a.text((XL + XR) / 2, 259, "TCP 3389 · canal TLS", 16, a.BLUE, a.MONO, 600, "middle"), 0, 100, 1)
# 2: credenciales antes de la sesión
msg(330, "credenciales (NLA · CredSSP)", a.BLUE, 25, 100, still=1)
at(a, a.box(892, 300, 260, 70, a.SLATE, a.LINE, rx=12) + a.text(910, 330, "valida contra AD o", 15, a.TXT, a.SANS, 500)
   + a.text(910, 354, "cuentas locales", 15, a.TXT, a.SANS, 500), 27, 100, 1)
# 3: válida -> escritorio
msg(410, "ok · abro la sesión", a.OK, 50, 75, back=True, still=1)
at(a, a.box(48, 386, 250, 150, a.OKBG, a.OK, rx=14, sw=2) + a.text(68, 420, "Escritorio remoto", 18, a.OK, a.HEAD, 600)
   + a.text(68, 448, "sesión creada después", 15, a.TXT, a.SANS, 500) + a.text(68, 470, "de autenticar", 15, a.TXT, a.SANS, 500), 53, 75, 1)
# 4: mala -> corte
msg(410, "credencial rechazada · fin", a.BAD, 75, 100, back=True)
at(a, a.box(48, 386, 250, 150, a.BADBG, a.BAD, rx=14, sw=2) + a.text(68, 420, "Sin pantalla", 18, a.BAD, a.HEAD, 600)
   + a.text(68, 448, "el servidor no gastó", 15, a.TXT, a.SANS, 500) + a.text(68, 470, "recursos en una sesión", 15, a.TXT, a.SANS, 500), 78, 100, 0)
caption(a, 600, [(0, 25, "El cifrado protege las credenciales en el camino: nadie en el medio las lee.", None),
                 (25, 50, "En dominio, conectá por nombre: por IP puede no haber Kerberos y NLA falla.", a.AMB),
                 (50, 75, "El escritorio existe solo para quien ya probó quién es.", a.OK),
                 (75, 100, "Sin NLA, cualquiera que llegue al puerto hace que el servidor arme una pantalla de inicio.", a.BAD)], still=2)
write(a, "6-t1.svg", "NLA: primero quién sos, después el escritorio",
      "Animación en cuatro tiempos entre un cliente RDP que entra por VPN y por nombre, y el servidor del VMS con NLA activa en el 3389. "
      "1: se establece la conexión TCP al 3389 y un canal cifrado TLS. 2: con NLA, el cliente manda las credenciales por CredSSP antes de que exista una sesión, y el servidor las valida contra Active Directory o las cuentas locales. "
      "3: si la credencial es válida, recién ahí el servidor arma el escritorio remoto. 4: si es mala, la conexión se corta sin dibujar ninguna pantalla ni gastar recursos en una sesión. "
      "Las notas recuerdan que en dominio conviene conectar por nombre porque por IP puede no haber Kerberos.")
