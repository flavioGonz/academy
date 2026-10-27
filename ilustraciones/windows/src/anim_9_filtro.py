"""Teoría lección 9: FilterHashtable filtra en el origen; Where-Object trae todo y filtra después."""
from _awin import *

a = new(20, "Dónde se filtra: en el registro o en PowerShell")
a.steps(["Con Where-Object, Get-WinEvent trae todos los eventos.",
         "PowerShell los revisa uno por uno y descarta casi todos.",
         "Con -FilterHashtable, el pedido viaja con el filtro.",
         "El registro devuelve solo los que coinciden: mucho más rápido."], still=3)
# registro de eventos
a.add(card(a, 48, 186, 330, 360, "Log System", "miles de eventos"))
ids = ["7036", "7036", "1074", "10016", "7036", "6008", "7040", "7036", "1014"]
for i, ev in enumerate(ids):
    y = 290 + i * 28
    hit = ev in ("1074",)
    a.add(a.box(72, y - 20, 282, 26, "#E5F0FB" if hit else a.SLATE, a.BLUE if hit else None, rx=6, sw=1.5)
          + a.text(84, y - 2, f"Id {ev}", 15, a.BLUE if hit else a.GREY, a.MONO, 600))
a.add(card(a, 822, 186, 330, 150, "PowerShell", "tu consola", dark=True))
a.add(a.box(822, 380, 330, 166, a.WHITE, a.LINE, rx=14, sw=2) + a.text(842, 414, "Resultado", 18, a.INK, a.HEAD, 600))
at(a, a.text(842, 448, "Id 1074 · quién reinició", 16, a.BLUE, a.MONO, 600), 40, 50, 0)
at(a, a.text(842, 448, "Id 1074 · quién reinició", 16, a.BLUE, a.MONO, 600), 85, 100, 1)
# 1-2: todos viajan
for k in range(9):
    t0 = 1 + k * 2.2
    mv = a.move([(0, 380, 260), (t0, 380, 260), (t0 + 8, 812, 260), (100, 812, 260)])
    op = a.keyframes([(0, 0), (t0, 0), (t0 + 0.5, 1), (t0 + 8, 1), (t0 + 8.5, 0), (100, 0)])
    a.add(a.group(f'<rect x="-30" y="-11" width="60" height="22" rx="6" fill="{a.GREY}"/>', mv, op, still=0))
at(a, chip(a, 600, 210, "todos los eventos", "grey", anchor="middle"), 0, 50, 0)
at(a, chip(a, 600, 300, "| Where-Object Id -eq 1074", "amb", anchor="middle"), 25, 50, 0)
at(a, a.text(987, 300, "revisando…", 16, "#9FC3E3", a.MONO, 600, "middle"), 25, 48, 0)
# 3-4: el filtro viaja y vuelve uno solo
at(a, a.arrow("M812 300H392", a.BLUE, 4) + a.text(600, 284, "@{LogName='System'; Id=1074}", 16, a.BLUE, a.MONO, 600, "middle"), 50, 100, 1)
mv = a.move([(0, 380, 360), (76, 380, 360), (84, 812, 360), (100, 812, 360)])
op = a.keyframes([(0, 0), (76, 0), (76.5, 1), (99, 1), (100, 0)])
a.add(a.group(f'<rect x="-34" y="-12" width="68" height="24" rx="6" fill="{a.BLUE}"/>', mv, op, still=0))
at(a, chip(a, 600, 336, "solo el 1074", "info", anchor="middle"), 76, 100, 1)
caption(a, 600, [(0, 25, "En un servidor con meses de registro, eso son decenas de miles de objetos.", None),
                 (25, 50, "Funciona, pero tarda: casi todo lo que viajó se tira.", a.AMB),
                 (50, 75, "El filtro (log, ID, nivel, fecha) lo aplica el servicio de registro.", a.BLUE),
                 (75, 100, "Mismo resultado, una fracción del trabajo: por eso FilterHashtable primero.", a.OK)], still=3)
write(a, "9-t1.svg", "Dónde se filtra: en el registro o en PowerShell",
      "Animación en cuatro tiempos con el log System a la izquierda, con eventos 7036, 1074, 10016, 6008 y otros, y la consola de PowerShell a la derecha. "
      "1: con Where-Object, Get-WinEvent trae todos los eventos a PowerShell. 2: PowerShell los revisa uno por uno y descarta casi todos, quedando solo el 1074. "
      "3: con -FilterHashtable, el pedido viaja al registro con el filtro LogName System e Id 1074. 4: el registro devuelve solo el evento que coincide. El cuadro fijo muestra el pedido con filtro y el resultado.")
