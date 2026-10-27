#!/usr/bin/env python3
"""Lección 1 · teoría: entrada a la web (80 → 8089 HTTPS) y bloqueo de 5 minutos tras 5 fallos."""
from _anim_grandstream import G

g = G(T=26, fix=70, kicker="GRANDSTREAM · PRIMER INGRESO", title="La web de la UCM: HTTPS, y 5 fallos la cierran")
g.steps([
    "Escribís la IP sola: con Redirect From Port 80 activo, te lleva al 8089 por HTTPS.",
    "Primer ingreso: admin y la contraseña única de la etiqueta. Ahí mismo se cambia.",
    "Un barrido prueba contraseñas: cada intento fallido suma.",
    "Al quinto fallo, la central bloquea el acceso durante 5 minutos.",
    "Pasado el bloqueo se puede volver a probar. Sin ese límite, la fuerza bruta no frena.",
])

# ---------- navegador
BX, BY, BW, BH = 48, 180, 470, 340
g.add(g.box(BX, BY, BW, BH, g.WHITE, g.LINE, rx=16))
g.add(f'<path d="M{BX} {BY + 16} a16 16 0 0 1 16 -16 H{BX + BW - 16} a16 16 0 0 1 16 16 V{BY + 46} H{BX} z" fill="{g.SLATE}"/>')
for i in range(3):
    g.add(f'<circle cx="{BX + 22 + i * 16}" cy="{BY + 23}" r="5" fill="{g.LINE}"/>')
g.add(g.box(BX + 76, BY + 9, BW - 92, 28, g.WHITE, g.LINE, rx=14, sw=1.5))
g.appear(g.text(BX + 92, BY + 29, "192.168.88.20", 15, g.INK, g.MONO, 600), 0, 11)
g.appear(g.text(BX + 92, BY + 29, "https://192.168.88.20:8089", 15, g.INK, g.MONO, 600), 11, 100)

g.add(g.text(BX + 24, BY + 88, "UCM6300 · Login", 20, g.INK, g.HEAD, 600))
g.add(g.text(BX + 24, BY + 124, "Usuario", 15, g.GREY, g.SANS))
g.add(g.box(BX + 24, BY + 132, BW - 48, 36, g.SLATE, None, rx=8))
g.add(g.text(BX + 24, BY + 194, "Contraseña", 15, g.GREY, g.SANS))
g.add(g.box(BX + 24, BY + 202, BW - 48, 36, g.SLATE, None, rx=8))
g.appear(g.text(BX + 40, BY + 156, "admin", 16, g.INK, g.MONO, 600), 21, 100)
g.appear(g.text(BX + 40, BY + 226, "la de la etiqueta trasera", 16, g.INK, g.MONO, 600), 22, 40)
for i, (pw, t) in enumerate([("admin", 41), ("1234", 44.5), ("123456", 48), ("password", 51.5), ("admin123", 55)]):
    g.appear(g.text(BX + 40, BY + 226, pw, 16, g.BAD, g.MONO, 600), t, t + 3.5 if i < 4 else 80)
# línea de estado
SY = BY + 290
g.appear(g.mark(BX + 40, SY - 6, True, 14) + g.text(BX + 64, SY, "entra: cambiá la clave ya (10 a 30 caracteres)", 15, g.OK, g.SANS, 600), 27, 40)
g.appear(g.mark(BX + 40, SY - 6, False, 14) + g.text(BX + 64, SY, "contraseña incorrecta", 15, g.BAD, g.SANS, 600), 42, 60)
g.appear(g.mark(BX + 40, SY - 6, False, 14) + g.text(BX + 64, SY, "acceso bloqueado: esperá 5 minutos", 15, g.BAD, g.SANS, 600), 60, 80)
g.appear(g.text(BX + 24, SY, "listo para volver a probar", 15, g.TXT, g.SANS, 600), 80, 100)

# ---------- UCM
UX, UY, UW = 680, 180, 472
g.add(g.node(UX, UY, UW, 70, "UCM6300", "192.168.88.20", dark=True))
g.add(g.pillc(UX + 120, UY + 86, ":80 · redirige", g.GREY, g.SLATE))
g.add(g.pillc(UX + 352, UY + 86, ":8089 · HTTPS", g.BLUE, g.WHITE))
g.msg(BX + BW + 8, UX - 8, 214, ":80", g.GREY, 2, 5.5, hold=20)
g.msg(UX - 8, BX + BW + 8, 248, "al 8089", g.GREY, 6.5, 9.5, hold=20, dashed=True)
g.msg(BX + BW + 8, UX - 8, 282, "HTTPS", g.BLUE, 12, 15.5, hold=100)

# ---------- contador de intentos
CY = 360
g.add(g.text(UX, CY - 22, "Intentos fallidos de login", 17, g.INK, g.SANS, 600))
for i in range(5):
    cx = UX + 26 + i * 62
    g.add(f'<circle cx="{cx}" cy="{CY + 20}" r="22" fill="{g.WHITE}" stroke="{g.LINE}" stroke-width="2"/>'
          + g.text(cx, CY + 26, str(i + 1), 17, g.GREY, g.MONO, 600, "middle"))
    t = 43 + i * 3.5
    g.appear(f'<circle cx="{cx}" cy="{CY + 20}" r="22" fill="{g.BAD}"/>' + g.text(cx, CY + 26, str(i + 1), 17, g.WHITE, g.MONO, 600, "middle"), t, 80)

# bloqueo
LY = 430
g.appear(g.box(UX, LY, UW, 96, g.BADBG, g.BAD, rx=14, sw=2)
         + g.text(UX + 22, LY + 34, "Login bloqueado 5 minutos", 19, g.BAD, g.HEAD, 600)
         + g.box(UX + 22, LY + 56, UW - 44, 18, g.WHITE, None, rx=9), 60, 80)
g.bar(UX + 22, LY + 56, UW - 44, 18, 61, 79, g.BAD, hold=80)
g.appear(g.box(UX, LY, UW, 96, g.OKBG, g.OK, rx=14, sw=2)
         + g.text(UX + 22, LY + 38, "Pasaron 5 minutos", 19, g.OK, g.HEAD, 600)
         + g.text(UX + 22, LY + 66, "la central vuelve a aceptar intentos de login", 16, g.TXT, g.SANS), 80, 100)

# nota final
g.appear(g.note(48, 556, 1104, "Sin límite no hay freno", [
    "La UCM6510 hasta la versión 1.0.20.52 no limitaba los intentos de login (CVE-2025-28172). Firmware al día, con backup antes."], "amb"), 82, 100)
g.appear(g.note(48, 556, 1104, None, [
    "Equipos fabricados desde enero de 2017: contraseña de admin única, impresa en la etiqueta. admin/admin es de equipos anteriores."], "info"), 0, 40)

g.finish(1, 1, "La web de la UCM: HTTPS, y 5 fallos la cierran",
         "Animación en cinco tiempos con un navegador a la izquierda y la UCM6300 en 192.168.88.20 a la derecha. "
         "1: se escribe la IP sola; el pedido llega al puerto 80, la central redirige al 8089 y la página se abre por HTTPS en https://192.168.88.20:8089. "
         "2: primer ingreso con usuario admin y la contraseña única de la etiqueta trasera; entra, y la contraseña se cambia ahí mismo, de 10 a 30 caracteres. "
         "Nota: los equipos fabricados desde enero de 2017 traen contraseña única; admin/admin es de equipos anteriores. "
         "3: un barrido prueba contraseñas (admin, 1234, 123456, password, admin123) y el contador de intentos fallidos sube de 1 a 5. "
         "4: al quinto fallo la central bloquea el login durante 5 minutos. "
         "5: pasados los 5 minutos vuelve a aceptar intentos de login. Nota: la UCM6510 hasta la versión 1.0.20.52 no limitaba los intentos de login (CVE-2025-28172); por eso firmware al día, con backup antes.",
         [8, 30, 52, 70, 92])
