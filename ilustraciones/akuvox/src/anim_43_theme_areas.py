#!/usr/bin/env python3
"""Lección 43 · Teoría · La misma pantalla del monitor: theme, área y protector.
Sale de teoria_md (Cómo funciona): el theme cambia la forma (Default o Call List) sin tocar las áreas;
el botón de alarma es el tipo Arming de un área y se cambia por Unlock "Portón"; sin uso durante Sleep Time
entra el protector y un toque lo despierta. Rutas: guías de pantalla de C319, S567, IT88, X933 y S562."""
from _anim_akuvox_29_42 import new, out, when
from _theme import mon_screen
import ilus

a = new(24, "MONITOR · PANTALLA", "Theme, áreas y protector sobre la misma pantalla")
a.steps([
    "Theme Default: la hora y cuatro áreas; el área 4 tiene Arming.",
    "Theme Call List: la misma pantalla pasa a lista de contactos.",
    "Otra vez Default: el área 4 cambia de tipo a Unlock, Portón.",
    "Sin uso durante Sleep Time entra el protector; un toque lo despierta.",
], still=2)

MX, MY, MW, MH = 48, 172, 560, 360
PORTON = [("Llamar", "call"), ("Mensajes", "msg"), ("DND", "dnd"), ("Portón", "unlock")]
a.add(mon_screen(MX, MY, MW, MH, "default", hl_area=(3, ilus.WARN)))                       # base (fondo del tiempo 1)
when(a, mon_screen(MX, MY, MW, MH, "default", hl_area=(3, ilus.WARN)), 0, 25, still=0)
when(a, mon_screen(MX, MY, MW, MH, "calllist"), 25, 50, still=0)
when(a, mon_screen(MX, MY, MW, MH, "default", areas=PORTON, hl_area=(3, ilus.OK)), 50, 77, still=1)
when(a, mon_screen(MX, MY, MW, MH, "saver"), 77, 93, still=0)
when(a, mon_screen(MX, MY, MW, MH, "default", areas=PORTON, hl_area=(3, ilus.OK)), 93, 100, still=0)
# el toque que despierta
tap = (f'<circle cx="{MX + MW / 2}" cy="{MY + MH / 2 + 20}" r="34" fill="none" stroke="{a.CYAN}" stroke-width="4"/>'
       + a.pill(MX + MW / 2, MY + MH / 2 + 66, "toque", a.WHITE, a.CYAN, 15, 28, "middle"))
when(a, tap, 90, 96, still=0)

# panel de ajustes a la derecha
PX, PW = 650, 500
a.add(a.box(PX, 172, PW, 360, a.WHITE, a.LINE, rx=18))
a.add(a.text(PX + 24, 208, "Lo que cambia en la web", 20, a.INK, a.HEAD, 600))
rows = [(250, "Device > Display Setting > Theme"), (340, "Home Page Display · Área 4"), (430, "Display Settings · Sleep Time")]
for y, lab in rows:
    a.add(a.text(PX + 24, y, lab, 15, a.GREY, a.MONO, 600))
# resaltado de la fila activa
for (t0, t1), y in [((0, 25), 250), ((25, 50), 250), ((50, 77), 340), ((77, 100), 430)]:
    when(a, a.box(PX + 10, y - 26, PW - 20, 76, "none", a.CYAN, rx=12, sw=2.5), t0, t1, still=1 if y == 340 else 0)
# valores
when(a, a.pill(PX + 24, y := 262, "Default", a.INK, a.SLATE, 16, 30), 0, 25, still=0)
when(a, a.pill(PX + 24, 262, "Call List", a.WHITE, a.BLUE, 16, 30), 25, 50, still=0)
when(a, a.pill(PX + 24, 262, "Default", a.INK, a.SLATE, 16, 30), 50, 100, still=1)
when(a, a.pill(PX + 24, 352, "Arming · Alarma", a.AMB, a.AMBBG, 16, 30), 0, 50, still=0)
when(a, a.pill(PX + 24, 352, "Unlock · Portón", a.OK, a.OKBG, 16, 30), 50, 100, still=1)
a.add(a.pill(PX + 24, 442, "1 min", a.INK, a.SLATE, 16, 30))
a.add(a.text(PX + 130, 463, "con protector: Local Pictures", 15, a.TXT, a.SANS, 600))
when(a, a.text(PX + 24, 510, "El theme cambia la forma, no las áreas.", 16, a.BLUE, a.SANS, 600), 25, 50, still=0)
when(a, a.text(PX + 24, 510, "El botón se cambia en el área, no en el theme.", 16, a.OK, a.SANS, 600), 50, 77, still=1)
when(a, a.text(PX + 24, 510, "El protector entra solo y un toque lo saca.", 16, a.BLUE, a.SANS, 600), 77, 100, still=0)

a.add(a.text(48, 584, "C319, S567, IT88, X933 y S562: Device > Display Setting > Theme (Default o Call List).", 17, a.INK, a.SANS, 600))
a.add(a.text(48, 612, "C313 Linux: Device > Key/Display > Home Page Mode (Classic o Call List Simple).", 17, a.TXT, a.SANS, 600))

out(a, 43, 1, "Theme, áreas y protector sobre la misma pantalla",
    "Animación con un monitor interior esquemático a la izquierda y, a la derecha, los ajustes de la web que cambian. "
    "Tiempo 1: theme Default, con la hora y cuatro áreas (Llamar, Mensajes, DND o no molestar, y Alarma); el área 4 tiene el tipo Arming y se marca en ámbar. "
    "Tiempo 2: el theme pasa a Call List y la pantalla muestra la lista de contactos para llamar, con botones chicos al costado; las áreas no se borran. "
    "Tiempo 3: de vuelta en Default, el área 4 cambia de tipo a Unlock con la etiqueta Portón y se marca en verde. "
    "Tiempo 4: después de un minuto sin uso (Sleep Time) entra el protector con una imagen del edificio; un toque lo despierta y vuelve la pantalla de inicio. "
    "Abajo: C319, S567, IT88, X933 y S562 usan Device > Display Setting > Theme; el C313 Linux usa Device > Key/Display > Home Page Mode.",
    [12, 37, 62, 85, 95])
