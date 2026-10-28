import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _fxo import *


def mini_ucm(x, y, ports, state):
    """Fila de FXO 1 a 4 sola, para comparar esquemas."""
    out = [f'<rect x="{x}" y="{y}" width="250" height="64" rx="12" fill="{DEEP}"/>', text(x + 14, y + 40, "FXO", 15, 600, "#9FC3E3", FM)]
    anchors = {}
    for i in range(4):
        px = x + 62 + i * 46
        st = state.get(i + 1)
        fill = {"libre": LIBRE, "uso": USO}.get(st, "#2C4A66")
        out.append(f'<rect x="{px}" y="{y + 13}" width="38" height="38" rx="7" fill="{fill}" stroke="{fill}" stroke-width="2"/>')
        out.append(text(px + 19, y + 38, str(i + 1), 15, 600, WHITE, FM, anchor="middle"))
        anchors[i + 1] = (px + 19, y + 64)
    return "".join(out), anchors


# ---------------------------------------------------------------- 14.svg: una troncal por línea o varias
c = Canvas(K(), "¿Una troncal por línea o varias FXO en una?")
# izquierda: una por línea
c.add(panel(48, 128, 540, 450, "Una troncal por línea", "ok", title_size=20))
c.add(text(68, 184, "Cada línea entra a un lugar distinto", 16, 500, INK2, FB))
s, a = mini_ucm(68, 206, None, {1: "libre", 2: "libre"})
c.add(s)
for i, (tr, dst, sub) in enumerate([("Antel_Linea1", "Grupo 6000", "atención"), ("Antel_Linea2", "Fax", "su extensión")]):
    x = 70 + i * 260
    px, py = a[i + 1]
    c.add(Cable((px, py), (x + 110, 316), kind="flow", arrow=True))
    c.add(f'<rect x="{x}" y="320" width="240" height="56" rx="12" fill="{WHITE}" stroke="{OK}" stroke-width="2"/>')
    c.add(text(x + 120, 354, tr, 17, 600, INK, FM, anchor="middle"))
    c.add(Cable((x + 120, 376), (x + 120, 420), kind="flow", arrow=True))
    c.add(dev(x, 424, dst, sub, icon="fax" if dst == "Fax" else "tel", w=240, h=76))
c.add(text(68, 552, "La ruta entrante se elige por troncal.", 16, 600, OK, FB))
# derecha: varias en una
c.add(panel(612, 128, 540, 450, "Varias FXO en una troncal", "info", title_size=20))
c.add(text(632, 184, "Todas las líneas son iguales", 16, 500, INK2, FB))
s, a = mini_ucm(632, 206, None, {1: "uso", 2: "libre"})
c.add(s)
c.add(Cable(a[1], (780, 316), kind="flow", arrow=True))
c.add(Cable(a[2], (820, 316), kind="flow", arrow=True))
c.add(f'<rect x="652" y="320" width="300" height="56" rx="12" fill="{WHITE}" stroke="{BLUE}" stroke-width="2"/>')
c.add(text(802, 354, "Antel_Grupo", 17, 600, INK, FM, anchor="middle"))
tbl = [("Ascend", "la primera libre (de fábrica)"), ("Poll", "alterna 1, 2, 1, 2"), ("Descend", "arranca por la última")]
for i, (k, v) in enumerate(tbl):
    y = 440 + i * 38
    c.add(Chip(652, y, k, "blue" if i == 0 else "gray", mono=True))
    c.add(text(770, y + 1, v, 16, 500, INK2, FB))
c.add(text(632, 408, "DAHDI Out Line Selection, para salir:", 16, 600, INK, FB))
c.add(text(632, 552, "Si el 1 está en uso, sale por el 2.", 16, 600, BLUE, FB))
c.add(Note(48, 596, 1104, "Si las líneas entran a lugares distintos, cada una necesita su troncal: en analógico no llega número llamado.", kind="info", size=16))
save(c, "14.svg")

# ---------------------------------------------------------------- 14-paso1: Analog Hardware
c = Canvas(K(1), "País de la línea y PCMA, antes de entregar")
c.add(Window(48, 132, 600, 300, "UCM · web", path="PBX Settings > Interface Settings > Analog Hardware",
             rows=[("FXO Opermode", "país de la línea"), ("PCMA Override", "PCMA"), ("Tone Region", "tonos del FXS"), ("FXO Ports (ACIM)", "Detect (más adelante)")], hl=1))
c.add(Step(48, 132, 1))
c.add(panel(690, 132, 462, 140, "PCMA Override", "info"))
svg, _ = wrap(710, 194, "El manual: Norteamérica usa PCMU; el resto del mundo, PCMA salvo que se sepa otra cosa. Viene en PCMU.", 420, 16, 400, INK2)
c.add(svg)
c.add(panel(690, 292, 462, 140, "FXO Opermode", "info"))
svg, _ = wrap(710, 354, "Impedancia, umbral de timbre y corriente de lazo por país. Viene en Estados Unidos; si Uruguay no está, anotá lo que quedó.", 420, 16, 400, INK2)
c.add(svg)
c.add(Note(48, 470, 1104, "PCMA Override reinicia la central. En un comercio abierto, coordiná el horario antes de guardar.", kind="warn", size=16))
save(c, "14-paso1.svg")

# ---------------------------------------------------------------- 14-paso2: crear la troncal
c = Canvas(K(2), "Una troncal por línea, con un nombre que se puede mostrar")
c.add(Window(48, 132, 560, 260, "UCM · web", path="Extension/Trunk > Analog Trunks > Create",
             rows=[("FXO Port", "1"), ("Trunk Name", "Antel_Linea1"), ("Advanced Options", "las vemos después")], hl=1))
c.add(Step(48, 132, 2))
c.add(Window(48, 412, 560, 170, "UCM · web", path="Extension/Trunk > Analog Trunks > Create",
             rows=[("FXO Port", "2"), ("Trunk Name", "Antel_Linea2")], hl=1))
c.add(panel(652, 132, 500, 160, "El nombre sale en todos lados", "warn"))
lst, _ = bullet_list(672, 196, ["Rutas entrantes y salientes", "Dashboard y Active Calls", "Capturas que mandás por WhatsApp"], 460, size=16, gap=8)
c.add(lst)
c.add(Note(652, 316, 500, "Sin el número real en el nombre: Antel_Linea1, Antel_Linea2. El número va en la ficha de la línea.", kind="ok", size=16))
c.add(Note(652, 432, 500, "Si las dos líneas van al mismo destino, una sola troncal con FXO 1 y 2 y DAHDI Out Line Selection en Ascend.", kind="info", size=16))
save(c, "14-paso2.svg")
