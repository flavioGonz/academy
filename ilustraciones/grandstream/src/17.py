import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _fxo import *


def nodo(x, y, w, h, t, s=None, kind="info", mono=True):
    bg, st = {"info": (WHITE, LINE2), "ok": (OK_BG, OK), "alert": (ALERT_BG, ALERT), "dark": (DEEP, DEEP)}[kind]
    tc = WHITE if kind == "dark" else INK
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{bg}" stroke="{st}" stroke-width="2"/>'
    out += text(x + w / 2, y + (h / 2 - 3 if s else h / 2 + 6), t, 17, 600, tc, FM if mono else FB, anchor="middle")
    if s:
        out += text(x + w / 2, y + h / 2 + 19, s, 15, 400, "#9FC3E3" if kind == "dark" else INK3, FB, anchor="middle")
    return out


# ---------------------------------------------------------------- 17.svg: de la línea al destino
c = Canvas(K(), "Sin número llamado: la ruta se elige por troncal")
# línea 1
c.add(nodo(48, 150, 170, 64, "FXO1", "línea 1", "dark"))
c.add(nodo(262, 150, 200, 64, "Antel_Linea1"))
c.add(nodo(506, 150, 120, 64, "s", "arranque"))
c.add(nodo(670, 150, 230, 64, "Ruta entrante", "Pattern _.", "info"))
c.add(nodo(944, 128, 208, 50, "IVR 7000", None, "ok"))
c.add(nodo(944, 190, 208, 50, "Grupo 6000", None, "ok"))
for a, b in [((218, 182), (262, 182)), ((462, 182), (506, 182)), ((626, 182), (670, 182))]:
    c.add(Arrow(a, b, kind="flow"))
c.add(Arrow((900, 170), (944, 153), kind="ok"))
c.add(Arrow((900, 194), (944, 215), kind="ok"))
c.add(text(922, 268, "en horario / fuera de horario", 15, 500, OK, FB, anchor="middle"))
# línea 2
c.add(nodo(48, 320, 170, 64, "FXO2", "línea 2", "dark"))
c.add(nodo(262, 320, 200, 64, "Antel_Linea2"))
c.add(nodo(506, 320, 120, 64, "s", "arranque"))
c.add(nodo(670, 320, 230, 64, "Ruta entrante", "Pattern _.", "info"))
c.add(nodo(944, 327, 208, 50, "Fax", None, "ok", mono=False))
for a, b in [((218, 352), (262, 352)), ((462, 352), (506, 352)), ((626, 352), (670, 352)), ((900, 352), (944, 352))]:
    c.add(Arrow(a, b, kind="flow" if a[0] < 900 else "ok"))
# sin ruta
c.add(nodo(48, 470, 170, 64, "FXO3", "línea nueva", "dark"))
c.add(nodo(262, 470, 200, 64, "Antel_Linea3", "sin ruta entrante"))
c.add(nodo(506, 470, 120, 64, "s", "se queda", "alert"))
c.add(Arrow((218, 502), (262, 502), kind="flow"))
c.add(Arrow((462, 502), (506, 502), kind="flow"))
c.add(Note(670, 452, 482, "Si en Active Calls una llamada queda en s, lo más probable es que su troncal no tenga ruta entrante o que el patrón no coincida.", kind="alert", size=16))
c.add(Note(48, 576, 1104, "Toda llamada analógica entra a la extensión s (Asterisk). El patrón _. acepta cualquier cosa; el destino lo pone la ruta.", kind="info", size=16))
save(c, "17.svg")

# ---------------------------------------------------------------- 17-paso1: ruta entrante
c = Canvas(K(1), "Una ruta entrante por troncal, con destino")
c.add(Window(48, 132, 600, 300, "UCM · web", path="Extension/Trunk > Inbound Routes > Add",
             rows=[("Trunks", "Antel_Linea1"), ("Pattern", "_."), ("Default Destination", "IVR 7000"),
                   ("Time Condition", "Office Time: IVR 7000"), ("fuera de horario", "Ring Group 6000")], hl=2))
c.add(Step(48, 132, 1))
c.add(panel(690, 132, 462, 160, "Por qué _.", "info"))
svg, _ = wrap(710, 194, "El punto acepta uno o más caracteres de cualquier tipo. Por una línea analógica no llega número llamado: el patrón no filtra nada.", 420, 16, 400, INK2)
c.add(svg)
c.add(Note(690, 312, 462, "El IVR 7000 y el grupo 6000 son los de las lecciones IVR con horario y Grupo o cola.", kind="ok", size=16))
c.add(Note(48, 460, 1104, "Repetí con Antel_Linea2 y su propio destino. Después llamá a cada línea desde un celular y mirá Active Calls: el destino nunca es s.", kind="info", size=16))
save(c, "17-paso1.svg")

# ---------------------------------------------------------------- 17-paso4: salida por dos líneas
c = Canvas(K(4), "Salida por las líneas de Antel, con failover")
c.add(Window(48, 132, 560, 360, "UCM · web", path="Extension/Trunk > Outbound Routes > Add",
             rows=[("Pattern", "_2XXXXXXX"), ("", "_4XXXXXXX"), ("", "_09XXXXXXX"), ("", "_911"),
                   ("Privilege Level", "National"), ("Use Trunk", "Antel_Linea1"), ("Failover Trunk", "Antel_Linea2")], hl=6))
c.add(Step(48, 132, 4))
c.add(panel(652, 132, 500, 196, "Qué marca cada patrón", "info"))
lst, _ = bullet_list(672, 196, ["Fijos: 8 cifras, empiezan con 2 o 4", "Celulares: 9 cifras, empiezan con 09", "Emergencias: 911"], 460, size=16, gap=8)
c.add(lst)
c.add(panel(652, 348, 500, 144, "Qué número ve el que recibe", "warn"))
svg, _ = wrap(672, 410, "El de la línea por la que salió: Outbound Route CID no aplica a troncales analógicas.", 460, 16, 400, INK2)
c.add(svg)
c.add(Note(48, 516, 1104, "Si preferís un prefijo para tomar línea: _9X. con Strip 1, como el ejemplo de Grandstream. El 911 no se usa para pruebas.", kind="info", size=16))
save(c, "17-paso4.svg")
