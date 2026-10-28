#!/usr/bin/env python3
"""Lección 45 · Teoría · Sequence Call: de a uno, con Call Timeout y When Refused.
Sale de teoria_md (Cómo funciona) y de las guías Call Settings de E16, R29 y X915 y la nota Configure Sequence Call:
llama al primero; si en el Call Timeout nadie atiende, pasa al siguiente; si rechaza, Call Next sigue y
Do Not Call Next corta. En los táctiles, el orden sale de la Priority of Call del grupo."""
from _anim_akuvox_29_42 import new, out, when
from _botones import mon_mini
import ilus

a = new(24, "PORTERO · LLAMADAS", "Sequence Call: de a uno, y qué pasa al rechazar")
a.steps([
    "Se aprieta el botón: suena el living (Primary).",
    "Nadie atiende en 20 s (Call Timeout): pasa a la cocina.",
    "El living rechaza con Call Next: suena la cocina enseguida.",
    "Con Do Not Call Next, el rechazo corta la secuencia.",
], still=1)

a.add(ilus.Intercom(70, 196, "Portero E16", "Sequence Call", screen=True).svg())
LX, LY, CY = 620, 176, 420
P0 = (226, 320)


def arrow_to(y, t0, t1, still=0, color=None):
    d = f"M{P0[0]} {P0[1]} C420 {P0[1]} 420 {y} {LX - 10} {y}"
    when(a, a.arrow(d, color or a.CYAN, 4), t0, t1, still=still)


def mon(x, y, title, sub, state, t0, t1, still=0):
    when(a, mon_mini(x, y, title, sub, state, w=220, h=130), t0, t1, still=still)


# base en reposo
a.add(mon_mini(LX, LY, "Living", "192.168.88.64 · Primary", "idle", w=220, h=130))
a.add(mon_mini(LX, CY, "Cocina", "192.168.88.65 · Secondary", "idle", w=220, h=130))

# tiempo 1 y comienzo del 2: suena el living
arrow_to(LY + 65, 2, 36)
mon(LX, LY, "Living", "192.168.88.64 · Primary", "ring", 2, 36)
when(a, a.pill(LX + 110, LY + 182, "20 s sin atender", a.AMB, a.AMBBG, 15, 30, "middle"), 28, 50, still=1)
# tiempo 2: timeout y pasa
mon(LX, LY, "Living", "192.168.88.64 · Primary", "noanswer", 36, 50, still=1)
arrow_to(CY + 65, 38, 50, still=1)
mon(LX, CY, "Cocina", "192.168.88.65 · Secondary", "ring", 38, 50, still=1)
# tiempo 3: rechazo con Call Next
arrow_to(LY + 65, 51, 57)
mon(LX, LY, "Living", "192.168.88.64 · Primary", "ring", 51, 57)
mon(LX, LY, "Living", "192.168.88.64 · Primary", "refused", 57, 75)
arrow_to(CY + 65, 60, 75)
mon(LX, CY, "Cocina", "192.168.88.65 · Secondary", "ring", 60, 75)
# tiempo 4: rechazo con Do Not Call Next
arrow_to(LY + 65, 76, 82)
mon(LX, LY, "Living", "192.168.88.64 · Primary", "ring", 76, 82)
mon(LX, LY, "Living", "192.168.88.64 · Primary", "refused", 82, 100)
mon(LX, CY, "Cocina", "192.168.88.65 · Secondary", "never", 85, 100)
when(a, a.text(LX + 110, 640, "La cocina no suena: la secuencia terminó en el rechazo.", 17, a.BAD, a.SANS, 600, "middle"), 85, 100)

# panel de ajustes
PX, PW = 900, 260
a.add(a.box(PX, 176, PW, 300, a.WHITE, a.LINE, rx=16))
a.add(a.text(PX + 20, 210, "Sequence Call", 20, a.INK, a.HEAD, 600))
a.add(a.text(PX + 20, 234, "Intercom > Basic", 15, a.BLUE, a.MONO, 600))
a.add(a.text(PX + 20, 280, "Call Timeout (Sec)", 15, a.TXT, a.SANS, 600))
a.add(a.pill(PX + 20, 292, "20", a.INK, a.SLATE, 16, 30))
a.add(a.text(PX + 20, 360, "When Refused", 15, a.TXT, a.SANS, 600))
when(a, a.pill(PX + 20, 372, "Call Next", a.WHITE, a.BLUE, 16, 30), 0, 75, still=1)
when(a, a.pill(PX + 20, 372, "Do Not Call Next", a.AMB, a.AMBBG, 16, 30), 75, 100, still=0)
a.add(a.text(PX + 20, 440, "Orden: Priority of Call", 15, a.TXT, a.SANS, 600))
a.add(a.text(PX + 20, 460, "del grupo (Directory)", 15, a.GREY, a.SANS, 600))
when(a, a.text(PX + 20, 520, "No atender: cuenta el tiempo.", 16, a.INK, a.SANS, 600) +
     a.text(PX + 20, 546, "Rechazar: decide When Refused.", 16, a.INK, a.SANS, 600), 0, 100, still=1)

out(a, 45, 1, "Sequence Call: de a uno, y qué pasa al rechazar",
    "Animación con un portero E16 a la izquierda, dos monitores (living, Primary, y cocina, Secondary) en el centro y el bloque Sequence Call de la web a la derecha, con Call Timeout 20. "
    "Tiempo 1: se aprieta el botón y suena el living. "
    "Tiempo 2: pasan 20 segundos sin atender, el living queda en Sin respuesta y empieza a sonar la cocina. "
    "Tiempo 3: con When Refused en Call Next, el living rechaza y la cocina suena enseguida. "
    "Tiempo 4: When Refused pasa a Do Not Call Next, en ámbar; el living rechaza y la cocina no suena: la secuencia termina en el rechazo. "
    "Al pie del panel: no atender hace correr el tiempo; rechazar lo decide When Refused.",
    [12, 42, 68, 92])
