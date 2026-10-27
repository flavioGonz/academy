"""Teoría de Roles y cuentas: el rol se evalúa al entrar y mientras dura la sesión."""
from _anim_hc import *

caps = ["19:30: guardia.lab inicia sesión; vigencia y horario, en verde.",
        "El SYS filtra por áreas visibles: ve solo Depósito y sus cámaras.",
        "07:00: termina el horario de permisos y el SYS cierra la sesión.",
        "10:00: intenta entrar de nuevo y el login se rechaza."]
a = new(26, "Roles", "El rol decide qué ve el usuario, y hasta cuándo", caps, still=1)

a.add(card(a, 48, 210, 260, 92, "guardia.lab", "rol Guardia"))
for i, h in enumerate(["19:30", "19:30", "07:00", "10:00"]):
    vis(a, a.pill(178, 330, f"hora: {h}", a.INK, a.SLATE, anchor="middle"), i)
a.add(a.box(360, 186, 380, 300, a.INK, a.INK, rx=18))
a.add(a.text(384, 222, "SYS revisa el rol", 19, a.WHITE, a.SANS, 600))
CHK = [("Vigencia", "hoy a fin de año"), ("Horario de permisos", "19:00 a 07:00"), ("Áreas visibles", "solo Depósito")]
for i, (k, v) in enumerate(CHK):
    y = 248 + i * 74
    a.add(a.box(384, y, 332, 60, a.NAVY2, rx=10))
    a.add(a.text(402, y + 26, k, 16, a.WHITE, a.SANS, 600))
    a.add(a.text(402, y + 48, v, 14, DARK_SUB, a.MONO))
    ok = '<circle cx="690" cy="{0}" r="13" fill="#E3F5EC"/><path d="M683 {0} l5 5 l9 -10" stroke="#0E8F5E" stroke-width="3" fill="none"/>'.format(y + 30)
    bad = '<circle cx="690" cy="{0}" r="13" fill="#FCEAE6"/><path d="M684 {1} l12 12 M696 {1} l-12 12" stroke="#D2492F" stroke-width="3"/>'.format(y + 30, y + 24)
    if i == 1:
        vis(a, ok, 0, 1); vis(a, bad, 2, 3)
    elif i == 0:
        vis(a, ok, 0, 3)
    else:
        vis(a, ok, 1)
s0, s1 = ph(a, 0)
token(a, "login", [(s0 + 3, 310, 256), (s0 + 12, 360, 256)], bg=a.BLUE)

# lo que ve
a.add(a.box(792, 186, 360, 300, a.WHITE, a.LINE, rx=18))
a.add(a.text(812, 218, "Lo que ve guardia.lab", 15, a.TXT, a.SANS, 600))
view = a.pill(812, 236, "Área: Depósito", a.INK, a.SLATE)
for k in range(4):
    x, y = 812 + (k % 2) * 164, 276 + (k // 2) * 82
    view += a.box(x, y, 156, 74, a.INK, rx=8) + a.text(x + 78, y + 43, f"CAM-0{k + 1}", 15, DARK_SUB, a.MONO, 600, "middle")
vis(a, view, 1)
vis(a, a.box(812, 300, 320, 110, a.BADBG, a.BAD, rx=12) + a.text(972, 348, "Sesión cerrada", 18, a.BAD, a.SANS, 600, "middle")
    + a.text(972, 376, "fuera del horario del rol", 15, a.BAD, a.MONO, 600, "middle"), 2)
vis(a, a.box(812, 300, 320, 110, a.BADBG, a.BAD, rx=12) + a.text(972, 348, "Login rechazado", 18, a.BAD, a.SANS, 600, "middle")
    + a.text(972, 376, "vuelve a las 19:00", 15, a.BAD, a.MONO, 600, "middle"), 3)
vis(a, a.text(812, 468, "las demás áreas no existen para él", 15, a.GREY, a.SANS, 600), 1)
s0, s1 = ph(a, 2)
token(a, "cerrar sesión", [(s0 + 3, 740, 330), (s0 + 12, 900, 330)], bg=a.BAD)

a.add(a.text(48, 560, "Si el rol vence o el reloj sale del horario de permisos, el usuario es expulsado y no", 17, a.TXT))
a.add(a.text(48, 588, "puede volver a entrar: sirve para contratistas, con fecha de fin, y para turnos.", 17, a.TXT))
a.add(a.text(48, 632, "Cada persona su usuario, cada usuario el rol mínimo.", 18, a.BLUE, a.SANS, 600))
write(a, "11-t1.svg", "El rol se evalúa en cada sesión", [10, 38, 62, 90])
