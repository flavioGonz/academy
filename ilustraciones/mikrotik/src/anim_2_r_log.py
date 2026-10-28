#!/usr/bin/env python3
"""Lección 2 · Resumen, "Cómo se ve en la red": con admin compartido el log no dice quién fue;
con un usuario por técnico sí, y dar de baja a uno no toca a los demás.
Formato de log: "user <nombre> logged in from <ip> via winbox" (teoría de la lección) y
"login failure for user <nombre> from <ip> via ..." (manual, bruteforce prevention)."""
from _anim_red_1_9 import *

a = Anim(T=26, kicker="MIKROTIK · USUARIOS PROPIOS · CÓMO SE VE EN LA RED", title="Con un usuario por técnico, el log dice quién fue")
a.steps([
    "Con admin compartido, tres técnicos de la oficina entran con el mismo nombre.",
    "Alguien agrega una regla: el historial dice admin y no hay forma de saber quién.",
    "Con un usuario por técnico, cada ingreso y cada cambio llevan su nombre.",
    "Juan deja la empresa: /user/disable juan.tecnico. Los demás siguen entrando.",
], still=2)

TECH = [("Lucía", "lucia.tecnico"), ("Pedro", "pedro.tecnico"), ("Juan", "juan.tecnico")]
TX, TW, TH = 48, 262, 80
RXc, RYc, RWc, RHc = 368, 262, 140, 104
for i, (n, u) in enumerate(TECH):
    y = 186 + i * 94
    a.add(a.box(TX, y, TW, TH, a.WHITE, a.LINE, rx=14))
    a.add(glyph(a, "user", TX + 16, y + 22, a.BLUE))
    a.add(a.text(TX + 58, y + 34, n, 19, a.INK, a.SANS, 600))
    a.add(during(a, a.text(TX + 58, y + 58, "usuario: admin", 15, a.AMB, a.MONO, 600), 0, 50))
    if i < 2:
        a.add(during(a, a.text(TX + 58, y + 58, u, 15, a.OK, a.MONO, 600), 50, 100, still=1))
    else:
        a.add(during(a, a.text(TX + 58, y + 58, u, 15, a.OK, a.MONO, 600), 50, 76, still=1))
        a.add(during(a, a.text(TX + 58, y + 58, "deshabilitado", 15, a.BAD, a.MONO, 600), 76, 100))
    a.add(line(TX + TW, y + TH / 2, RXc, RYc + RHc / 2, a.LINE, 3))

a.add(a.box(RXc, RYc, RWc, RHc, a.INK, rx=16))
a.add(glyph(a, "server", RXc + RWc / 2 - 16, RYc + 16, a.CYAN))
a.add(a.text(RXc + RWc / 2, RYc + 74, "Router", 18, a.WHITE, a.SANS, 600, "middle"))
a.add(a.text(RXc + RWc / 2, RYc + 94, "del cliente", 15, SKY, a.MONO, 400, "middle"))


def login(i, t0, color):
    y = 186 + i * 94 + TH / 2
    x0, x1 = TX + TW + 18, RXc - 22
    a.add(travel(a, f'<circle cx="0" cy="0" r="9" fill="{color}"/>', [(x0, y + (RYc + RHc / 2 - y) * 0.1), (x1, y + (RYc + RHc / 2 - y) * 0.92)], t0, t0 + 2.5, hold=0.5))


for i, t0 in enumerate((2, 6, 10)):
    login(i, t0, a.AMB)
login(1, 28, a.BAD)
login(0, 52, a.OK)
login(1, 56, a.OK)
login(1, 61, a.BAD)
login(2, 82, a.GREY)
a.add(during(a, xmark(a, RXc - 30, RYc + 114), 85, 100))

# ---------- log
LX, LY, LW, LH = 540, 186, 612, 266
a.add(a.box(LX, LY, LW, LH, a.INK, rx=16))
a.add(a.text(LX + 20, LY + 32, "/log/print y /system/history", 16, SKY, a.MONO, 600))
A = [("user admin logged in from 198.51.100.20 via winbox", a.WHITE, 4),
     ("user admin logged in from 198.51.100.20 via winbox", a.WHITE, 8),
     ("user admin logged in from 198.51.100.20 via winbox", a.WHITE, 12),
     ("/system/history · filter rule added · admin", GOLD, 31)]
for j, (t, c, t0) in enumerate(A):
    a.add(during(a, a.text(LX + 20, LY + 70 + j * 32, t, 15, c, a.MONO, 600 if c != a.WHITE else 400), t0, 50))
a.add(during(a, a.text(LX + 20, LY + 70 + 4 * 32 + 8, "¿Lucía, Pedro o Juan? Misma IP, mismo nombre.", 16, "#FF9E8A", a.SANS, 600), 35, 50))
B = [("user lucia.tecnico logged in from 198.51.100.20 via winbox", a.WHITE, 53),
     ("user pedro.tecnico logged in from 198.51.100.20 via winbox", a.WHITE, 57),
     ("/system/history · filter rule added · pedro.tecnico", MINT, 63),
     ("login failure for user juan.tecnico", "#FF9E8A", 85),
     ("from 198.51.100.20 via winbox", "#FF9E8A", 85)]
for j, (t, c, t0) in enumerate(B):
    a.add(during(a, a.text(LX + (56 if t.startswith("from") else 20), LY + 70 + j * 32, t, 15, c, a.MONO, 600 if c != a.WHITE else 400), t0, 100, still=1 if t0 < 70 else 0))
a.add(during(a, a.text(LX + 20, LY + 70 + 3 * 32 + 8, "Fue Pedro: queda con su nombre.", 16, MINT, a.SANS, 600), 66, 80, still=1))

# ---------- pie
FY = 478
a.add(a.box(48, FY, 1104, 140, a.WHITE, a.LINE, rx=10, sw=1.5))
caption_items = [
    (0, 50, ["Con una cuenta compartida, cuando alguien se va hay que cambiar la clave de admin", "en cada router y avisarle a todos los que se quedan."], a.AMB, 0),
    (50, 76, ["/user/add name=pedro.tecnico group=full password=\"…\"", "Una cuenta por persona, con contraseña de 12 caracteres o más."], a.OK, 1),
    (76, 100, ["/user/disable juan.tecnico", "Su ingreso se rechaza; Lucía y Pedro siguen con sus propias claves."], a.BAD, 0),
]
for t0, t1, (l1, l2), col, st in caption_items:
    mono = l1.startswith("/")
    body = (f'<rect x="48" y="{FY}" width="6" height="140" rx="2" fill="{col}"/>'
            + a.text(76, FY + 54, l1, 17, a.INK, a.MONO if mono else a.SANS, 600)
            + a.text(76, FY + 92, l2, 17, a.TXT, a.SANS, 400 if mono else 600))
    a.add(during(a, body, t0, t1, still=st))

write(a, 2, "r1", "Admin compartido contra un usuario por técnico",
      "Animación en cuatro tiempos con tres técnicos de la oficina (Lucía, Pedro y Juan), el router del cliente y su log. "
      "1: los tres entran con el usuario admin desde la misma IP de la oficina, 198.51.100.20; el log anota tres veces user admin logged in from 198.51.100.20 via winbox. "
      "2: uno de ellos agrega una regla y /system/history la anota como filter rule added por admin: no hay forma de saber quién fue. "
      "3: con un usuario por técnico, el log dice user lucia.tecnico logged in y user pedro.tecnico logged in, y el historial anota filter rule added por pedro.tecnico. "
      "4: Juan deja la empresa y alcanza con /user/disable juan.tecnico: su intento queda como login failure for user juan.tecnico from 198.51.100.20 via winbox, "
      "y Lucía y Pedro siguen entrando con sus propias claves, sin cambiar nada en sus cuentas.",
      [10, 40, 62, 70, 90])
