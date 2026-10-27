#!/usr/bin/env python3
"""Lección 36 · Teoría · Del terminal al piso: el flujo del EC33 en el tiempo.
Sale de teoria_md (Cómo funciona): 1 validación en el terminal, 2 pisos permitidos, 3 pedido HTTP al EC33
como Server 1 (Unlock) con usuario y clave de Open Relay via HTTP, 4 relé de cada piso autorizado durante el
Hold Delay. Device Location para llamar al ascensor; Server 2 (Execute); Floor Starts From -1."""
from _anim_akuvox_29_42 import new, out, box, travel, when

a = new(24, "ASCENSOR EC33", "Del terminal al piso: la orden viaja por HTTP")
a.steps([
    "El usuario se valida en el terminal: tarjeta, PIN o rostro.",
    "El terminal busca los pisos permitidos de ese usuario: el piso 3.",
    "Pedido HTTP al EC33 (Server 1, Unlock) con el usuario y la clave.",
    "El EC33 activa el relé del piso 3 durante el Hold Delay y vuelve a reposo.",
], still=3)

# cable lógico terminal -> EC33
a.add(f'<path d="M290 300 H470" fill="none" stroke="{a.LINE}" stroke-width="3" stroke-dasharray="6 6"/>')
a.add(box(48, 258, 242, 84, "Terminal", "A08 o portero", "card"))
a.add(box(470, 244, 290, 112, "EC33", "Server 1 · Unlock", "elevator", dark=True))

# t1: credencial
travel(a, (169, 196), (169, 250), 3, 10, "tarjeta", a.WHITE, a.BLUE, hold=4)
when(a, a.pill(169, 360, "usuario válido", a.OK, a.OKBG, 15, 28, "middle"), 13, 100, still=1)
# t2: pisos permitidos
when(a, a.box(60, 404, 218, 64, a.WHITE, a.BLUE, rx=12) + a.text(76, 430, "pisos permitidos", 15, a.GREY, a.MONO)
     + a.text(76, 456, "piso 3", 18, a.INK, a.MONO, 600), 28, 100, still=1)
# t3: HTTP
travel(a, (300, 300), (462, 300), 53, 66, "HTTP", a.WHITE, a.BLUE, hold=6)
when(a, a.text(380, 230, "usuario + clave", 15, a.BLUE, a.MONO, 600, "middle")
     + a.text(380, 250, "Open Relay via HTTP", 15, a.BLUE, a.MONO, 600, "middle"), 52, 75, still=0)
when(a, a.text(470, 384, "+ Device Location: planta baja", 15, a.TXT, a.MONO, 600)
     + a.text(470, 406, "(para llamar al ascensor)", 15, a.GREY, a.MONO), 60, 100, still=1)

# botonera con relés
FL = ["4", "3", "2", "1", "PB", "-1"]
BX, BY0 = 940, 184
a.add(a.box(900, 170, 252, 400, a.SLATE, a.LINE, rx=18))
a.add(a.text(1026, 198, "relés del EC33", 15, a.GREY, a.MONO, 600, "middle"))
for i, f in enumerate(FL):
    y = 216 + i * 56
    a.add(f'<circle cx="{BX + 10}" cy="{y + 20}" r="20" fill="{a.WHITE}" stroke="{a.LINE}" stroke-width="2"/>')
    a.add(a.text(BX + 10, y + 26, f, 16, a.INK, a.MONO, 600, "middle"))
    a.add(a.text(BX + 44, y + 26, "reposo", 15, a.GREY, a.MONO))
# cable EC33 -> botonera
a.add(f'<path d="M760 300 H900" stroke="{a.CYAN}" stroke-width="4"/>')
# relé del piso 3 activo durante Hold Delay
y3 = 216 + 56
on = (f'<circle cx="{BX + 10}" cy="{y3 + 20}" r="22" fill="{a.OKBG}" stroke="{a.OK}" stroke-width="3"/>'
      + a.text(BX + 10, y3 + 26, "3", 16, a.OK, a.MONO, 700, "middle")
      + f'<rect x="{BX + 40}" y="{y3 + 4}" width="160" height="30" fill="{a.SLATE}"/>'
      + a.text(BX + 44, y3 + 26, "activo", 15, a.OK, a.MONO, 600))
when(a, on, 76, 95, still=1)
# barra Hold Delay (se vacía)
a.add(a.group(a.box(560, 470, 300, 20, a.WHITE, a.LINE, rx=10), a.show(76, 96), still=1))
bar = a.keyframes([(0, 1), (76, 1), (95, 0.02), (100, 0.02)], "transform", "scaleX({})")
a.n += 1
c = f"c{a.n}"
a.css.append(f".{c}{{transform-box:fill-box;transform-origin:left center;transform:scaleX(.55);animation:{bar} {a.T}s linear infinite}}")
a.add(a.group(f'<rect class="{c}" x="560" y="470" width="300" height="20" rx="10" fill="{a.OK}"/>', a.show(76, 96), still=1))
when(a, a.text(560, 460, "Hold Delay", 16, a.INK, a.MONO, 600), 76, 96, still=1)
when(a, a.pill(560, 500, "vuelve a reposo", a.GREY, "#E6EDF4", 15, 28), 95, 100)

a.add(a.text(48, 612, "Con un segundo EC33 como Server 2 (Execute): recibe el llamado y, si el usuario tiene", 17, a.TXT, a.SANS, 600))
a.add(a.text(48, 638, "un solo piso, también ese piso. Con varios pisos, la habilitación queda en el Server 1.", 17, a.TXT, a.SANS, 600))

out(a, 36, 1, "Del terminal al piso: la orden viaja por HTTP",
    "Animación del flujo de ascensor con un terminal, un EC33 configurado como Server 1 (Unlock) y una columna de relés por piso, del -1 al 4. "
    "Tiempo 1: el usuario pasa su tarjeta y el terminal lo valida. "
    "Tiempo 2: el terminal busca los pisos permitidos de ese usuario: el piso 3. "
    "Tiempo 3: el terminal manda un pedido HTTP al EC33 con el usuario y la clave de Open Relay via HTTP, y además el Device Location, planta baja, para llamar al ascensor. "
    "Tiempo 4: el EC33 activa solo el relé del piso 3 mientras se vacía la barra del Hold Delay; al terminar, el relé vuelve a reposo. "
    "Abajo: con un segundo EC33 como Server 2 (Execute), este recibe el llamado y el piso solo cuando el usuario tiene uno.",
    [8, 40, 60, 82, 97])
