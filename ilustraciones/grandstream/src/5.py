import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _gs import *

# ---------------------------------------------------------------- 5.svg: escalera de privilegios
c = Canvas(K(), "La extensión usa la ruta si su nivel alcanza")
lv = ["Internal", "Local", "National", "International"]
for i, n_ in enumerate(lv):
    x, y, h = 48 + i * 130, 470 - i * 70, 70 + i * 70
    c.add(f'<rect x="{x}" y="{y}" width="124" height="{h}" rx="10" fill="{SOFT if i < 3 else OK_BG}" stroke="{BLUE if i < 3 else OK}" stroke-width="2"/>')
    c.add(text(x + 62, y + 30, n_, 14, 600, INK, FM, anchor="middle"))
c.add(text(48, 170, "Cada extensión y cada ruta", 20, 600, INK, FD))
c.add(text(48, 198, "tienen un Privilege Level:", 20, 600, INK, FD))
c.add(text(48, 572, "menos", 15, 600, INK3, FM))
c.add(text(562, 572, "más permiso", 15, 600, OK, FM, anchor="end"))
c.add(arrow((110, 590), (556, 590)))
c.add(Table(600, 150, ["Extensión", "nacional", "internacional"],
            [["Nivel Local", "✗ no sale", "✗ no sale"], ["Nivel National", "✓ sale", "✗ no sale"], ["Nivel International", "✓ sale", "✓ pide PIN"]],
            [210, 160, 182], row_h=46))
c.add(text(600, 136, "RUTA NACIONAL: NATIONAL · RUTA INTERNACIONAL: INTERNATIONAL + PIN", 13, 600, INK3, FM, ls=0.6))
c.add(Note(600, 360, 552, "Si roban la contraseña de una interna National, el fraude choca contra la ruta internacional: no le alcanza el nivel. Y si roban una International, todavía falta el PIN.", title="Por qué protege", kind="ok", size=16))
c.add(Note(600, 506, 552, "Nivel igual o mayor que el de la ruta: pasa. Menor: la central rechaza la llamada.", kind="info", size=16))
save(c, "5.svg")

# ---------------------------------------------------------------- 5-paso1: leer un patrón
c = Canvas(K(1), "Leé el patrón carácter por carácter")


def cells(x, y, parts, w=46, h=56):
    out, cx = [], x
    for s, kd in parts:
        ww = max(w, len(s) * 15 + 18)
        bg, fg = KC[kd]
        out.append(f'<rect x="{cx}" y="{y}" width="{ww}" height="{h}" rx="8" fill="{bg}" stroke="{fg}" stroke-width="2"/>')
        out.append(text(cx + ww / 2, y + h / 2 + 8, s, 22, 600, INK, FM, anchor="middle"))
        cx += ww + 6
    return "".join(out), cx


svg, end = cells(48, 150, [("_", "gray"), ("[24]", "cyan"), ("X", "soft"), ("X", "soft"), ("X", "soft"), ("X", "soft"), ("X", "soft"), ("X", "soft"), ("X", "soft")])
c.add(svg)
c.add(text(48, 236, "fijo: 2 o 4, y 7 dígitos más", 17, 600, INK, FB))
c.add(text(48, 262, "marca 29001007  ✓", 16, 600, OK, FM))
svg, end = cells(48, 300, [("_", "gray"), ("0", "cyan"), ("9", "cyan"), ("X", "soft"), ("X", "soft"), ("X", "soft"), ("X", "soft"), ("X", "soft"), ("X", "soft"), ("X", "soft")])
c.add(svg)
c.add(text(48, 386, "celular: 09 y 7 dígitos más", 17, 600, INK, FB))
c.add(text(48, 412, "marca 0912345  ✗ (le faltan dígitos)", 16, 600, ALERT, FM))
c.add(Step(48, 150, 1))
c.add(Table(680, 150, ["Comodín", "Significa"], [["_", "empieza un patrón"], ["X", "un dígito de 0 a 9"], ["Z", "un dígito de 1 a 9"], ["N", "un dígito de 2 a 9"], ["[24]", "uno de esos: 2 o 4"], [".", "uno o más, lo que sea"]], [150, 322], mono_cols=(0,), row_h=40))
c.add(Note(48, 456, 590, "Cada patrón cuenta dígitos exactos: si el número tiene uno de más o de menos, no matchea y la central no lo manda por esa ruta.", kind="info", size=16))
c.add(Note(680, 456, 472, "El punto agarra todo lo que siga: en una ruta internacional va con PIN y privilegio International.", kind="warn", size=16))
save(c, "5-paso1.svg")

# ---------------------------------------------------------------- 5-paso3: Strip 1 saca el 9
c = Canvas(K(3), "Strip 1: el 9 sirve para elegir la ruta y se saca")
c.add(text(48, 158, "1. La interna marca", 18, 600, INK, FB))
dig = "929001007"
for i, d in enumerate(dig):
    x = 48 + i * 58
    kd = "warn" if i == 0 else "soft"
    bg, fg = KC[kd]
    c.add(f'<rect x="{x}" y="176" width="50" height="60" rx="8" fill="{bg}" stroke="{fg}" stroke-width="2"/>')
    c.add(text(x + 25, 216, d, 26, 600, INK, FM, anchor="middle"))
c.add(text(48, 290, "2. Matchea el patrón", 18, 600, INK, FB))
c.add(code(48, 306, 300, "_9NXXXXXXX", 20, h=48))
c.add(text(370, 338, "9 fijo · N de 2 a 9 · 7 dígitos más", 16, 500, INK2, FB))
c.add(text(48, 410, "3. Strip 1 saca el primer dígito", 18, 600, INK, FB))
for i, d in enumerate(dig):
    x = 48 + i * 58
    if i == 0:
        c.add(f'<rect x="{x}" y="428" width="50" height="60" rx="8" fill="{WHITE}" stroke="{ALERT}" stroke-width="2" stroke-dasharray="5 4"/>')
        c.add(text(x + 25, 468, d, 26, 600, ALERT, FM, anchor="middle"))
        c.add(f'<path d="M{x + 8} 480L{x + 42} 436" stroke="{ALERT}" stroke-width="3"/>')
    else:
        c.add(f'<rect x="{x}" y="428" width="50" height="60" rx="8" fill="{OK_BG}" stroke="{OK}" stroke-width="2"/>')
        c.add(text(x + 25, 468, d, 26, 600, INK, FM, anchor="middle"))
c.add(arrow((580, 458), (680, 458), kind="ok"))
c.add(Generic(700, 416, "Proveedor_Lab", "recibe 29001007", icon="cloud", w=300, hl=OK))
c.add(Step(48, 176, 3))
c.add(Note(720, 160, 432, "Si el patrón incluye el 9 y no ponés Strip, el 9 viaja al proveedor pegado al número: 929001007.", title="Sin Strip", kind="alert", size=16))
c.add(Note(48, 528, 1104, "El prefijo de salida es una costumbre de la oficina, no parte del número: el patrón lo usa para elegir la ruta y Strip lo quita antes del troncal.", kind="info", size=16))
save(c, "5-paso3.svg")
