#!/usr/bin/env python3
"""Lección 19 · Back To Home. Teoría "Cómo funciona": claves en lugar de usuarios. El router conoce la clave
pública de cada usuario; lo firmado con una clave desconocida se ignora sin responder; borrar un usuario es
borrar su clave; revoked-and-disabled borra todas.
"""
from _anim_mikrotik_14_26 import Anim, packet, out

a = Anim(T=26, kicker="MIKROTIK · BACK TO HOME", title="WireGuard: claves en lugar de usuarios")
a.steps([
    "Cada equipo tiene su par de claves. El router guarda la pública de cada usuario.",
    "Llega un paquete de tecnico-lucia: la clave es conocida y entra al túnel.",
    "Llega uno con una clave que no está en la lista: se ignora, sin responder.",
    "Borrás el usuario invitado: su clave sale de la lista y queda afuera.",
    "revoked-and-disabled borra todas las claves. Nadie entra.",
], still=1)

CL = [("tecnico-lucia", "clave L", a.BLUE), ("invitado", "clave I", a.AMB), ("equipo desconocido", "clave X", a.GREY)]
CY0, CH, CG = 186, 96, 22
for i, (n, k, col) in enumerate(CL):
    y = CY0 + i * (CH + CG)
    a.add(a.box(48, y, 330, CH, a.WHITE, a.LINE, rx=16))
    a.add(a.text(72, y + 38, n, 19, a.INK, a.MONO, 600))
    a.add(a.pill(72, y + 54, k, a.WHITE, col, 15))
    a.add(a.text(200, y + 74, "privada + pública", 15, a.GREY, a.MONO))

# router
RX, RY, RW, RH = 748, 178, 404, 372
a.add(a.box(RX, RY, RW, RH, a.INK, rx=18))
a.add(a.text(RX + 24, RY + 40, "MikroTik", 21, a.WHITE, a.HEAD, 600))
a.add(a.text(RX + 24, RY + 66, "back-to-home-vpn 192.168.216.1/24", 15, "#9FC3E3", a.MONO))
a.add(a.text(RX + 24, RY + 108, "CLAVES PÚBLICAS QUE CONOCE", 15, "#9FC3E3", a.MONO, 600))


def row(y, n, k, col, off, still):
    inner = (a.box(RX + 16, y, RW - 32, 60, a.NAVY2, rx=10) + a.text(RX + 32, y + 26, n, 17, a.WHITE, a.MONO, 600)
             + a.pill(RX + 32, y + 32, k, a.WHITE, col, 14, 24)
             + a.text(RX + RW - 30, y + 50, "su IP del túnel", 15, "#9FC3E3", a.MONO, 400, "end"))
    a.add(a.group(inner, a.show(2, off), still=still))


row(RY + 124, "tecnico-lucia", "clave L", a.BLUE, 82, 1)
row(RY + 196, "invitado", "clave I", a.AMB, 63, 1)
a.add(a.group(f'<line x1="{RX + 24}" y1="{RY + 226}" x2="{RX + RW - 24}" y2="{RY + 226}" stroke="{a.BAD}" stroke-width="3"/>', a.show(60, 64), still=0))
a.add(a.group(a.text(RX + RW / 2, RY + 300, "lista vacía: claves y puerto nuevos", 16, "#FFD28A", a.MONO, 600, "middle")
              + a.text(RX + RW / 2, RY + 326, "al reactivar, cada equipo se configura otra vez", 15, "#C9DDF0", a.SANS, 600, "middle"),
              a.show(83, 100), still=0))

a.add(a.group(a.box(RX + 16, RY + 124, RW - 32, 60, "none", "#5BE0A5", rx=10, sw=3), a.show(26, 38), still=1))

# paquetes
ly = [CY0 + CH / 2 + i * (CH + CG) for i in range(3)]
X1, X2 = 400, 730
for y in ly:
    a.add(f'<line x1="{X1 - 10}" y1="{y}" x2="{X2 + 10}" y2="{y}" stroke="{a.LINE}" stroke-width="2.5" stroke-dasharray="5 7"/>')


def send(i, t, label, col, good):
    y = ly[i]
    packet(a, label, [(0, X1 + 70, y), (t, X1 + 70, y), (t + 5, X2 - 70, y), (100, X2 - 70, y)], t, t + 7.5 if good else t + 9, col)
    if good:
        a.add(a.group(a.pill(X2 - 10, y - 50, "entra al túnel", a.OK, a.OKBG, 15, 30, "end"), a.show(t + 5, t + 14), still=0))
        packet(a, "respuesta", [(0, X2 - 70, y), (t + 8, X2 - 70, y), (t + 13, X1 + 70, y), (100, X1 + 70, y)], t + 8, t + 13.5, a.OK)
    else:
        a.add(a.group(a.pill(X2 - 10, y - 50, "se ignora · sin respuesta", a.BAD, a.BADBG, 15, 30, "end"), a.show(t + 5, t + 16), still=0))


send(0, 22, "clave L", a.BLUE, True)
send(2, 42, "clave X", a.GREY, False)
send(1, 66, "clave I", a.AMB, False)
send(0, 86, "clave L", a.BLUE, False)

# cuadro fijo: lucia entra
_off = a.keyframes([(0, 0), (100, 0)])
a.add(a.group(a.arrow(f"M{X1} {ly[0]} H{X2}", a.OK, 3) + a.pill(X2 - 10, ly[0] - 50, "entra al túnel", a.OK, a.OKBG, 15, 30, "end")
              + a.arrow(f"M{X1} {ly[2]} H{X2 - 60}", a.GREY, 3, "7 6") + a.pill(X2 - 10, ly[2] - 50, "se ignora · sin respuesta", a.BAD, a.BADBG, 15, 30, "end"),
              _off, still=1))

# nota
NY = 616
NOTES = [(0, 40, "Un usuario por equipo: cada celular tiene su propia clave."),
         (40, 60, "Una clave desconocida no recibe ni un rechazo: el router no contesta nada."),
         (60, 80, "Dar de baja a una persona es borrar su usuario. Los demás siguen igual."),
         (80, 100, "Revocar todo obliga a configurar de nuevo cada equipo: para una baja, borrá un usuario.")]
for s_, e, t in NOTES:
    a.add(a.group(a.text(48, NY, t, 18, a.INK, a.SANS, 600), a.show(s_, e), still=1 if s_ == 0 else 0))

out(a, 19, 1, "WireGuard: claves en lugar de usuarios",
    "Animación en cinco tiempos. A la izquierda tres equipos, cada uno con su par de claves: tecnico-lucia, invitado y un equipo desconocido. "
    "A la derecha el MikroTik con back-to-home-vpn 192.168.216.1/24 y la lista de claves públicas que conoce, cada una con su IP del túnel. "
    "1: el router guarda la clave pública de tecnico-lucia y la de invitado. 2: llega un paquete con la clave de tecnico-lucia, es conocida, entra al túnel y vuelve la respuesta. "
    "3: llega un paquete con una clave que no está en la lista: el router lo ignora y no responde. "
    "4: se borra el usuario invitado; su clave sale de la lista y su próximo paquete se ignora. "
    "5: revoked-and-disabled borra todas las claves; ni siquiera tecnico-lucia entra, y al reactivar hay claves y puerto nuevos y cada equipo se configura otra vez.",
    [10, 30, 52, 74, 94])
