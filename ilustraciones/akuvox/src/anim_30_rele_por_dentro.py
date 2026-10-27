#!/usr/bin/env python3
"""Lección 30 · Teoría · Un relé es un interruptor movido por un electroimán.
Sale de teoria_md (Cómo funciona): el monitor alimenta la bobina, los contactos (aislados del circuito
interno) abren o cierran lo que conectes; circuito de banco: + fuente a un borne, otro borne a la lámpara,
lámpara al - de la fuente."""
from _anim_akuvox_29_42 import new, out, box, when

a = new(20, "RELÉ DEL MONITOR", "El relé por dentro: un imán que mueve un contacto")
a.steps([
    "Reposo: la bobina no tiene corriente y el resorte deja el contacto abierto.",
    "El monitor energiza la bobina: el electroimán atrae la armadura.",
    "El contacto cierra el circuito de la fuente: la lámpara prende.",
    "La bobina se apaga: el resorte abre el contacto y la lámpara se apaga.",
], still=2)

RED, BLK = "#D2492F", "#2B2B2B"
ON = (27, 77)          # bobina energizada
CLOSED = (48, 77)      # contacto cerrado
MID = [(40, 48), (77, 80)]

# ---- monitor (lado del control)
a.add(box(48, 330, 250, 84, "Monitor S", "maneja la bobina", "server"))
# cables de la bobina (siempre) y su versión energizada
a.add(f'<path d="M298 358 H380 V352 H408" fill="none" stroke="{a.GREY}" stroke-width="3"/>')
a.add(f'<path d="M298 388 H380 V448 H408" fill="none" stroke="{a.GREY}" stroke-width="3"/>')
when(a, f'<path d="M298 358 H380 V352 H408" fill="none" stroke="{a.BLUE}" stroke-width="4"/>'
     f'<path d="M298 388 H380 V448 H408" fill="none" stroke="{a.BLUE}" stroke-width="4"/>', *ON, still=1)

# ---- bobina (núcleo + espiras)
CX, CY0, CY1 = 460, 330, 470
a.add(f'<rect x="{CX - 22}" y="{CY0}" width="44" height="{CY1 - CY0}" rx="6" fill="#C9D6E3" stroke="{a.GREY}" stroke-width="2"/>')
coil = "".join(f'<path d="M{CX - 34} {y} Q{CX} {y + 9} {CX + 34} {y}" fill="none" stroke="#B26A00" stroke-width="3"/>' for y in range(342, 462, 12))
a.add(coil)
when(a, "".join(f'<path d="M{CX - 34} {y} Q{CX} {y + 9} {CX + 34} {y}" fill="none" stroke="{a.BLUE}" stroke-width="3.5"/>' for y in range(342, 462, 12)), *ON, still=1)
# campo magnético (pulsa mientras está energizada)
field = "".join(f'<path d="M{CX - 44 - k * 18} {CY0 + 10} C{CX - 90 - k * 30} {CY0 + 50} {CX - 90 - k * 30} {CY1 - 50} {CX - 44 - k * 18} {CY1 - 10}" fill="none" stroke="{a.CYAN}" stroke-width="2" stroke-dasharray="5 5"/>'
                f'<path d="M{CX + 44 + k * 18} {CY0 + 10} C{CX + 90 + k * 30} {CY0 + 50} {CX + 90 + k * 30} {CY1 - 50} {CX + 44 + k * 18} {CY1 - 10}" fill="none" stroke="{a.CYAN}" stroke-width="2" stroke-dasharray="5 5"/>' for k in range(2))
when(a, field, ON[0] + 1, ON[1], still=1)
a.add(a.text(CX, 504, "bobina", 16, a.INK, a.MONO, 600, "middle"))
when(a, a.text(CX, 526, "electroimán encendido", 15, a.BLUE, a.MONO, 600, "middle"), *ON, still=1)

# ---- armadura (palanca con pivote) y contacto fijo
PX, PY = 410, 300       # pivote = borne común
TIPX = 720


def lever(tip_y, spring_bottom_y=None):
    ly = PY + (tip_y - PY) * (640 - PX) / (TIPX - PX)
    spring_bottom_y = ly + 8
    return (f'<line x1="{PX}" y1="{PY}" x2="{TIPX}" y2="{tip_y}" stroke="{a.INK}" stroke-width="9" stroke-linecap="round"/>'
            f'<circle cx="{TIPX}" cy="{tip_y}" r="8" fill="#E0A100" stroke="{a.INK}" stroke-width="2"/>'
            f'<path d="M640 212 l-12 8 l24 8 l-24 8 l24 8 l-24 8 l24 8 l-12 {spring_bottom_y - 268}" fill="none" stroke="{a.GREY}" stroke-width="2.5"/>')


open_y, mid_y, closed_y = 250, 278, 300
# posición abierta: visible fuera de la ventana de cierre
a.add(a.group(lever(open_y), a.keyframes([(0, 1), (40, 1), (40.5, 0), (79.5, 0), (80, 1), (100, 1)]), still=0))
a.add(a.group(lever(mid_y), a.keyframes([(0, 0), (40, 0), (40.5, 1), (47.5, 1), (48, 0), (77, 0), (77.5, 1), (79.5, 1), (80, 0), (100, 0)]), still=0))
a.add(a.group(lever(closed_y), a.keyframes([(0, 0), (47.5, 0), (48, 1), (77, 1), (77.5, 0), (100, 0)]), still=1))
a.add(f'<rect x="628" y="200" width="24" height="12" rx="3" fill="{a.GREY}"/>')
a.add(a.text(668, 206, "resorte", 15, a.GREY, a.MONO, 600))
a.add(f'<circle cx="{PX}" cy="{PY}" r="10" fill="{a.WHITE}" stroke="{a.INK}" stroke-width="3"/>')
# contacto fijo
a.add(f'<rect x="{TIPX - 20}" y="{closed_y + 8}" width="40" height="10" rx="3" fill="#E0A100" stroke="{a.INK}" stroke-width="2"/>')
a.add(a.text(TIPX - 28, closed_y + 34, "contacto", 15, a.INK, a.MONO, 600, "end"))

# ---- circuito de la carga (rojo +, cian por el relé, negro -)
a.add(box(900, 180, 250, 84, "Fuente 12 V", "de banco", "bolt"))
a.add(f'<path d="M{PX} {PY - 10} V222 H900" fill="none" stroke="{RED}" stroke-width="4"/>')
a.add(a.text(560, 214, "+12 V", 15, RED, a.MONO, 600, "middle"))
a.add(f'<path d="M{TIPX} {closed_y + 18} V340 H820 V470 H905" fill="none" stroke="{a.CYAN}" stroke-width="4"/>')
a.add(f'<path d="M965 470 H1110 V264" fill="none" stroke="{BLK}" stroke-width="4"/>')
a.add(a.text(1120, 380, "−", 22, BLK, a.MONO, 600))
# lámpara apagada / prendida
LX, LY = 935, 470
a.add(f'<circle cx="{LX}" cy="{LY}" r="30" fill="{a.WHITE}" stroke="{a.INK}" stroke-width="3"/>'
      f'<path d="M{LX - 20} {LY - 20} L{LX + 20} {LY + 20} M{LX + 20} {LY - 20} L{LX - 20} {LY + 20}" stroke="{a.INK}" stroke-width="3"/>')
lit = (f'<circle cx="{LX}" cy="{LY}" r="52" fill="#FFD28A" opacity=".55"/>'
       f'<circle cx="{LX}" cy="{LY}" r="30" fill="#FFE7A8" stroke="{a.INK}" stroke-width="3"/>'
       f'<path d="M{LX - 20} {LY - 20} L{LX + 20} {LY + 20} M{LX + 20} {LY - 20} L{LX - 20} {LY + 20}" stroke="{a.INK}" stroke-width="3"/>')
when(a, lit, 50, CLOSED[1], still=1)
a.add(a.text(LX, LY + 62, "Lámpara 12 V", 16, a.INK, a.SANS, 600, "middle"))
when(a, a.text(LX, LY + 84, "prendida", 15, a.OK, a.MONO, 600, "middle"), 50, CLOSED[1], still=1)
when(a, a.text(LX, LY + 84, "apagada", 15, a.GREY, a.MONO, 600, "middle"), 0, 49.5)
when(a, a.text(LX, LY + 84, "apagada", 15, a.GREY, a.MONO, 600, "middle"), 78, 100)

# ---- aislación
a.add(f'<line x1="560" y1="250" x2="560" y2="560" stroke="{a.AMB}" stroke-width="2" stroke-dasharray="3 7" opacity="0"/>')
a.add(a.pill(48, 560, "dos circuitos aislados", a.AMB, a.AMBBG, 15, 30))
a.add(a.text(48, 618, "El monitor solo maneja la bobina. El contacto conmuta lo que conectes,", 17, a.TXT, a.SANS, 600))
a.add(a.text(48, 642, "dentro de la carga del modelo (S562: 30 V 1 A; S563, S565 y S567: 30 V 2 A).", 17, a.TXT, a.SANS, 600))

out(a, 30, 1, "El relé por dentro",
    "Animación de un relé en cuatro tiempos. A la izquierda, el monitor conectado a la bobina; arriba, una armadura con pivote y un resorte; "
    "a la derecha, el circuito de banco: positivo de la fuente de 12 V al borne común, el contacto a la lámpara y la lámpara al negativo. "
    "Tiempo 1: en reposo la bobina no tiene corriente, el resorte mantiene el contacto abierto y la lámpara está apagada. "
    "Tiempo 2: el monitor energiza la bobina, aparece el campo del electroimán y la armadura baja. "
    "Tiempo 3: el contacto cierra el circuito de la fuente y la lámpara prende. "
    "Tiempo 4: la bobina se apaga, el resorte abre el contacto y la lámpara se apaga. "
    "Los dos circuitos están aislados: el monitor solo maneja la bobina.",
    [12, 38, 44, 62, 90])
