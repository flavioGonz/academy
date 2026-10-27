import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/bosch-incendio/src")
from _bi import *


def eol(x, y, w=64):
    return (rect(x, y - 18, w, 36, WHITE, INK2, rx=6, sw=2) +
            f'<path d="M{x + 10} {y}l6 -8l8 16l8 -16l8 16l8 -16l6 8" fill="none" stroke="{INK2}" stroke-width="2"/>')


def pts(x, y, n):
    return tag(x, y, f"{n} punto" + ("" if n == 1 else "s"), "ok" if n else "gray", size=14)


# ---------------------------------------------------------------- 7.svg: lo que cuelga del lazo
c = Canvas(K(), "Lo que cuelga del lazo además de los detectores")
c.add(rect(48, 130, 170, 70, DEEP, DEEP, rx=12)); c.add(text(68, 172, "Módulo LSN", 18, 600, WHITE, FD))
c.add(f'<path d="M218 165H1152" stroke="{BLUE}" stroke-width="4"/>')
c.add(text(1150, 152, "lazo LSN", 14, 600, BLUE, FM, anchor="end"))
xs = [320, 520, 720, 920, 1080]
for x in xs:
    c.add(f'<path d="M{x} 165V240" stroke="{BLUE}" stroke-width="3"/>')
c.add(pulsador(320, 272, 56, "Pulsador", "FMC-420RW"))
c.add(pts(320, 370, 1))
c.add(sirena(520, 272, 58, "Sirena y baliza", "FNX-425U", on=True))
c.add(pts(520, 370, 0))
c.add(text(520, 400, "84 por lazo con detectores,", 14, 500, INK3, FB, anchor="middle"))
c.add(text(520, 418, "127 sin detectores", 14, 500, INK3, FB, anchor="middle"))
c.add(box(650, 244, 140, 70, "FLM-430", [], size=15)); c.add(mid(720, 304, "I2M1", 15, 500, INK3, FM))
c.add(text(720, 342, "2 entradas,", 15, 500, INK2, FB, anchor="middle"))
c.add(text(720, 362, "1 salida supervisada", 15, 500, INK2, FB, anchor="middle"))
c.add(pts(720, 400, 2))
c.add(box(850, 244, 140, 70, "FLM-420", [], size=15)); c.add(mid(920, 304, "/4-CON", 15, 500, INK3, FM))
c.add(f'<path d="M920 314V470H1000" fill="none" stroke="{INK2}" stroke-width="3"/>')
for k, xx in enumerate((830, 900)):
    pass
c.add(f'<path d="M920 410H880" stroke="{INK2}" stroke-width="2"/>')
c.add(detector(860, 410, 18)); c.add(detector(860, 466, 18))
c.add(f'<path d="M920 466H880" stroke="{INK2}" stroke-width="2"/>')
c.add(eol(1000, 470)); c.add(text(1032, 508, "fin de línea", 14, 600, INK2, FB, anchor="middle"))
c.add(text(832, 444, "zona convencional", 14, 600, INK2, FB, anchor="end"))
c.add(box(1030, 244, 122, 70, "FLM-420", [], size=15)); c.add(mid(1091, 304, "RLE-S", 15, 500, ALERT, FM))
c.add(text(1091, 342, "extinción", 15, 600, ALERT, FB, anchor="middle"))
c.add(text(1091, 362, "hasta 8 por lazo", 14, 500, INK3, FB, anchor="middle"))
c.add(Note(48, 530, 540, "Cada entrada programada para dar alarma consume un punto de alarma del panel, aunque viva en un módulo.", title="Los puntos se cuentan por entrada", kind="info"))
c.add(Note(612, 530, 540, "En EN 54-2, silenciar o reponer avisadores es acción manual: un temporizador de duración solo vale para señales que no son EN 54.", title="Silenciar es a mano", kind="warn"))
c.add(text(48, 440, "Las zonas convencionales del FLM-420/4-CON", 15, 500, INK3))
c.add(text(48, 462, "terminan en una resistencia o un módulo de", 15, 500, INK3))
c.add(text(48, 484, "fin de línea: así el panel ve un cable cortado.", 15, 500, INK3))
save(c, "7.svg")

# ---------------------------------------------------------------- 7-paso1: contar puntos
c = Canvas(K(1), "Un punto por cada entrada programada como alarma")
c.add(rect(48, 130, 520, 400, WHITE, LINE2, rx=16))
c.add(text(72, 168, "Módulo de 8 entradas (ejemplo)", 19, 600, INK, FD))
uses = [("alarma", True), ("alarma", True), ("alarma", True), ("falla técnica", False), ("falla técnica", False), ("estado", False), ("sin usar", False), ("sin usar", False)]
for i, (u, a) in enumerate(uses):
    y = 200 + i * 40
    c.add(text(80, y + 20, f"Entrada {i + 1}", 16, 500, INK2, FM))
    c.add(tag(330, y + 21, u, "ok" if a else "gray", size=14, mono=False))
    c.add(text(500, y + 22, "1" if a else "0", 18, 700, OK if a else INK3, FM, anchor="middle"))
c.add(text(500, 192, "punto", 14, 600, INK3, FB, anchor="middle"))
c.add(hline(72, 544, 528 - 8, LINE))
c.add(Table(612, 130, ["Dispositivo", "Cant.", "Puntos"], [
    ["Detector FAP-425-O-R", "20", "20"], ["Pulsador FMC-420RW", "4", "4"], ["Sirena FNX-425U", "6", "0"],
    ["Módulo 8 entradas (3 alarma)", "1", "3"], ["Total de puntos", "", "27"]], [330, 100, 110], hl_row=4, row_h=46))
c.add(Note(612, 420, 540, "Una sirena avisa pero no da alarma: no suma. Un módulo de ocho entradas puede sumar hasta ocho, según cómo programes cada una.", title="Qué suma y qué no", kind="info"))
c.add(text(48, 580, "Cantidades de ejemplo para practicar la cuenta; la obra real sale del plano.", 15, 400, INK3))
save(c, "7-paso1.svg")

# ---------------------------------------------------------------- 7-paso2: salidas que mueven algo
c = Canvas(K(2), "En rojo, cada salida que mueve algo físico")
c.add(rect(470, 270, 260, 120, DEEP, DEEP, rx=16))
c.add(mid(600, 322, "Panel AVENAR", 21, 600, WHITE, FD))
c.add(mid(600, 350, "salidas por reglas", 15, 400, "#9FC3E3", FM))
outs = [((180, 170), "Extinción por gas", "FLM-420-RLE-S", "alert"), ((180, 340), "Retención de puertas", "módulo de salida", "alert"),
        ((180, 510), "Ascensores", "módulo de salida", "alert"), ((1020, 170), "Ventilación", "módulo de salida", "alert"),
        ((1020, 340), "Sirenas y balizas", "avisan", "info"), ((1020, 510), "Transmisión al monitoreo", "avisa", "info")]
for (x, y), t, s, kd in outs:
    col = ALERT if kd == "alert" else BLUE
    c.add(rect(x - 132, y - 46, 264, 92, ALERT_BG if kd == "alert" else WHITE, col, rx=14, sw=2.5 if kd == "alert" else 2))
    c.add(mid(x, y - 6, t, 18, 600, col if kd == "alert" else INK, FD))
    c.add(mid(x, y + 22, s, 15, 400, INK3, FM))
    sx = 470 if x < 600 else 730
    ex = x + 132 if x < 600 else x - 132
    c.add(f'<path d="M{sx} 330L{ex} {y}" stroke="{col}" stroke-width="2.5" stroke-dasharray="{"0" if kd == "alert" else "6 6"}"/>')
c.add(text(600, 620, "Rojo: mueve algo y necesita una forma documentada de aislarla antes de probar.", 17, 600, ALERT, FB, anchor="middle"))
save(c, "7-paso2.svg")
