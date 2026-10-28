#!/usr/bin/env python3
"""Lección 45 · Teoría · Group Call: suenan todos, atiende uno, y qué pasa al rechazar.
Sale de teoria_md (Cómo funciona) y de las guías Call Settings de E16, E18 y X915 y la nota Configure Group Call:
llama a todos los contactos del grupo a la vez; si uno rechaza, End This Call Only deja sonando a los demás
y End All Calls corta a todos."""
from _anim_akuvox_29_42 import new, out, when
from _botones import mon_mini
import ilus

a = new(24, "PORTERO · LLAMADAS", "Group Call: suenan todos, atiende uno")
a.steps([
    "Se aprieta el botón: suenan los dos monitores a la vez.",
    "Atiende la cocina: el living deja de sonar.",
    "El living rechaza con End This Call Only: la cocina sigue sonando.",
    "Con End All Calls, un rechazo corta la llamada en todos.",
], still=1)

a.add(ilus.Intercom(70, 196, "Portero E16", "Group Call", screen=True).svg())
LX, LY, CY = 620, 176, 420
P0 = (226, 320)


def arrow_to(y, t0, t1, still=0, color=None):
    d = f"M{P0[0]} {P0[1]} C420 {P0[1]} 420 {y} {LX - 10} {y}"
    when(a, a.arrow(d, color or a.CYAN, 4), t0, t1, still=still)


def mon(x, y, title, sub, state, t0, t1, still=0):
    when(a, mon_mini(x, y, title, sub, state, w=220, h=130), t0, t1, still=still)


L = ("Living", "192.168.88.64")
C = ("Cocina", "192.168.88.65")
a.add(mon_mini(LX, LY, *L, "idle", w=220, h=130))
a.add(mon_mini(LX, CY, *C, "idle", w=220, h=130))

# tiempo 1 y comienzo del 2: suenan los dos
for t0, t1 in ((2, 32),):
    arrow_to(LY + 65, t0, t1); arrow_to(CY + 65, t0, t1)
    mon(LX, LY, *L, "ring", t0, t1); mon(LX, CY, *C, "ring", t0, t1)
# tiempo 2: atiende la cocina
mon(LX, CY, *C, "ok", 32, 50, still=1)
arrow_to(CY + 65, 32, 50, still=1, color=a.OK)
mon(LX, LY, *L, "cut", 32, 50, still=1)
# tiempo 3: rechazo con End This Call Only
arrow_to(LY + 65, 51, 57); arrow_to(CY + 65, 51, 75)
mon(LX, LY, *L, "ring", 51, 57); mon(LX, CY, *C, "ring", 51, 75)
mon(LX, LY, *L, "refused", 57, 75)
when(a, a.text(LX + 110, 640, "Se cortó solo el living: la cocina puede atender.", 17, a.OK, a.SANS, 600, "middle"), 60, 75)
# tiempo 4: rechazo con End All Calls
arrow_to(LY + 65, 76, 82); arrow_to(CY + 65, 76, 82)
mon(LX, LY, *L, "ring", 76, 82); mon(LX, CY, *C, "ring", 76, 82)
mon(LX, LY, *L, "refused", 82, 100)
mon(LX, CY, *C, "cut", 82, 100)
when(a, a.text(LX + 110, 640, "Un rechazo cortó la visita en toda la casa.", 17, a.BAD, a.SANS, 600, "middle"), 85, 100)

# panel de ajustes
PX, PW = 900, 260
a.add(a.box(PX, 176, PW, 220, a.WHITE, a.LINE, rx=16))
a.add(a.text(PX + 20, 210, "Group Call", 20, a.INK, a.HEAD, 600))
a.add(a.text(PX + 20, 234, "Intercom > Basic", 15, a.BLUE, a.MONO, 600))
a.add(a.text(PX + 20, 284, "When Refused", 15, a.TXT, a.SANS, 600))
when(a, a.pill(PX + 20, 296, "End This Call Only", a.WHITE, a.BLUE, 15, 30), 0, 75, still=1)
when(a, a.pill(PX + 20, 296, "End All Calls", a.AMB, a.AMBBG, 15, 30), 75, 100, still=0)
a.add(a.text(PX + 20, 356, "Grupo: Directory > User", 15, a.TXT, a.SANS, 600))
a.add(a.text(PX + 20, 376, "> Group (táctiles)", 15, a.GREY, a.SANS, 600))
a.add(a.text(PX + 20, 440, "El primero que atiende", 16, a.INK, a.SANS, 600))
a.add(a.text(PX + 20, 464, "se queda con la visita.", 16, a.INK, a.SANS, 600))
a.add(a.text(PX + 20, 506, "Cuánto suena sin respuesta:", 16, a.TXT, a.SANS, 600))
a.add(a.text(PX + 20, 530, "Call Feature > Max Dial Time.", 16, a.TXT, a.SANS, 600))

out(a, 45, 2, "Group Call: suenan todos, atiende uno",
    "Animación con un portero E16 a la izquierda, dos monitores (living y cocina) en el centro y el bloque Group Call de la web a la derecha. "
    "Tiempo 1: se aprieta el botón y suenan los dos monitores a la vez. "
    "Tiempo 2: atiende la cocina, en verde, y el living deja de sonar. "
    "Tiempo 3: con When Refused en End This Call Only, el living rechaza y la cocina sigue sonando, lista para atender. "
    "Tiempo 4: When Refused pasa a End All Calls, en ámbar; el living rechaza y la cocina también deja de sonar: un rechazo cortó la visita en toda la casa. "
    "En el panel: el grupo se arma en Directory > User > Group en los táctiles, el primero que atiende se queda con la visita y cuánto suena sin respuesta se limita en Call Feature > Max Dial Time.",
    [12, 42, 68, 92])
