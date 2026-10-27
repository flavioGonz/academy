"""Teoría de Antes de tocar: licencia atada al hardware, con y sin desactivar antes."""
from _anim_hc import *

caps = ["Mal: se cambia el hardware del SYS sin desactivar la licencia.",
        "La huella no coincide: el SYS alterna Starting y Stopped; el nuevo da 1108.",
        "Bien: backup copiado afuera y licencia desactivada antes de tocar.",
        "Se cambia el hardware y se activa de nuevo: servicios en verde."]
a = new(28, "Licencias", "Desactivar antes de tocar el hardware", caps, still=3)

a.add(a.box(48, 186, 360, 300, a.WHITE, a.LINE, rx=18))
a.add(a.text(72, 222, "Servidor SYS", 19, a.INK, a.SANS, 600))
a.add(a.box(440, 186, 340, 300, a.WHITE, a.LINE, rx=18))
a.add(a.text(464, 222, "Servidor de licencias", 19, a.INK, a.SANS, 600))
a.add(a.box(812, 186, 340, 300, a.WHITE, a.LINE, rx=18))
a.add(a.text(836, 222, "Otra máquina", 19, a.INK, a.SANS, 600))
a.add(a.text(836, 248, "\\\\192.168.88.20\\backups", 15, a.GREY, a.MONO))

# hardware del SYS
a.add(a.text(72, 270, "hardware", 15, a.GREY, a.MONO))
vis(a, a.pill(72, 280, "huella original", a.INK, a.SLATE), 0, still=0)
vis(a, a.pill(72, 280, "hardware nuevo", a.BAD, a.BADBG), 1, still=0)
vis(a, a.pill(72, 280, "huella original", a.INK, a.SLATE), 2, still=0)
vis(a, a.pill(72, 280, "hardware nuevo", a.OK, a.OKBG), 3)
s0, s1 = ph(a, 0)
vis(a, a.text(72, 352, "se cambia el disco…", 16, a.BAD, a.SANS, 600), 0)
# estado del servicio
a.add(a.text(72, 400, "Service Manager", 15, a.GREY, a.MONO))
s0, s1 = ph(a, 1)
pts_a = [(0, 0), (s0, 0)]
pts_b = [(0, 0), (s0, 0)]
t, on = s0, True
while t < s1 - 1:
    pts_a += [(t, 1 if on else 0), (t + 2.4, 1 if on else 0)]
    pts_b += [(t, 0 if on else 1), (t + 2.4, 0 if on else 1)]
    t += 2.5; on = not on
pts_a += [(s1, 0), (100, 0)]; pts_b += [(s1, 0), (100, 0)]
a.add(a.group(a.pill(72, 412, "Starting", a.AMB, a.AMBBG), a.keyframes(pts_a), still=0))
a.add(a.group(a.pill(72, 412, "Stopped", a.BAD, a.BADBG), a.keyframes(pts_b), still=0))
vis(a, a.pill(72, 412, "Running", a.OK, a.OKBG), 3)
vis(a, a.pill(464, 412, "servidor nuevo: 1108", a.BAD, a.BADBG), 1)

# estado del código de licencia
a.add(a.text(464, 270, "código de activación", 15, a.GREY, a.MONO))
a.add(a.group(a.pill(464, 280, "usado por el SYS", a.INK, a.SLATE), a.show(0, ph(a, 2)[0] + 18), still=0))
a.add(a.group(a.pill(464, 280, "libre", a.OK, a.OKBG), a.show(ph(a, 2)[0] + 18, ph(a, 2)[1]), still=0))
vis(a, a.pill(464, 280, "activo en el SYS", a.OK, a.OKBG), 3)

# tiempo 3: backup afuera y desactivar
s0, s1 = ph(a, 2)
token(a, "backup", [(s0 + 1, 240, 352), (s0 + 9, 900, 352)], bg=a.BLUE)
token(a, "desactivar", [(s0 + 10, 240, 352), (s0 + 18, 560, 352)], bg=a.AMB)
vis(a, a.pill(836, 280, "backup del domingo", a.BLUE, a.SLATE), 2, 3)
a.add(a.group(a.pill(836, 316, "copia de hoy", a.OK, a.OKBG), a.show(ph(a, 2)[0] + 9, 100), still=1))
# tiempo 4: activar en el hardware nuevo
s0, s1 = ph(a, 3)
token(a, "activar", [(s0 + 2, 610, 352), (s0 + 10, 240, 352), (s0 + 13, 240, 352)], bg=a.OK)

a.add(a.text(48, 540, "Desactivar le avisa al servidor de licencias que el código queda libre. Sin eso,", 17, a.TXT))
a.add(a.text(48, 568, "el SYS con hardware nuevo no logra arrancar y el código figura usado en otro SYS.", 17, a.TXT))
a.add(a.text(48, 612, "Antes de tocar el servidor: backup afuera y licencia desactivada.", 18, a.BLUE, a.SANS, 600))
write(a, "4-t1.svg", "Desactivar antes de tocar el hardware", [12, 34, 62, 92])
