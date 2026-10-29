#!/usr/bin/env python3
"""Lección 2 · Resumen, "Cómo se ve en la red": Concurrent Registrations. La extensión 1001 con límite 2:
el GRP del escritorio y la app Wave registran; un equipo ajeno con las credenciales filtradas no encuentra lugar.
Con el valor de fábrica (3) el mismo intento entra sin que nadie lo note. Fuente: manual UCM630x y la lección
(Concurrent Registrations: 3 de fábrica, hasta 10; con el límite cubierto, la central rechaza el registro de más)."""
from _anim_gs_red import R

g = R(T=26, fix=70, kicker="GRANDSTREAM · EXTENSIÓN SÓLIDA · CÓMO SE VE EN LA RED",
      title="Una cuenta, varios equipos: cuántos registran")
g.steps([
    "El GRP del escritorio registra la 1001: ocupa el primero de los 2 registros permitidos.",
    "La app Wave de la misma persona registra la 1001: ocupa el segundo.",
    "Un equipo ajeno con la clave filtrada pide registrar: no hay lugar y la central lo rechaza.",
    "Con 3, el valor de fábrica, el mismo pedido entra y nadie lo anotó en la ficha.",
])

DX, DW, DH = 48, 300, 84
rows = [(178, "GRP del escritorio", "192.168.88.31", "tel"),
        (290, "App Wave", "celular · 198.51.100.7", "phone"),
        (402, "Equipo ajeno", "203.0.113.66", "bug")]
for y, t, s, ic in rows:
    g.add(g.dev(DX, y, DW, DH, t, s, icon=ic, hl=g.BAD if ic == "bug" else None))

UX, UY, UW, UH = 760, 178, 392, 308
g.add(g.box(UX, UY, UW, UH, g.WHITE, g.LINE, rx=16))
g.add(g.box(UX, UY, UW, 64, g.INK, rx=16) + g.box(UX, UY + 40, UW, 24, g.INK, rx=0))
g.add(g.ico(UX + 16, UY + 16, "ucm", g.CYAN, 1.35))
g.add(g.text(UX + 62, UY + 40, "UCM · extensión 1001", 19, g.WHITE, g.HEAD, 600))
g.add(g.text(UX + 20, UY + 96, "Concurrent Registrations", 15, g.GREY, g.MONO))
g.appear(g.text(UX + UW - 20, UY + 96, "2", 20, g.INK, g.MONO, 600, "end"), 0, 75)
g.appear(g.text(UX + UW - 20, UY + 96, "3", 20, g.BAD, g.MONO, 600, "end"), 75, 100)
g.add(g.text(UX + 20, UY + 132, "registros activos", 15, g.GREY, g.MONO))
SL = [UY + 146, UY + 196, UY + 246]
for k, sy in enumerate(SL):
    g.add(g.box(UX + 16, sy, UW - 32, 42, g.SLATE, None, rx=10))
    g.add(g.text(UX + 32, sy + 27, f"{k + 1}", 16, g.GREY, g.MONO, 600))
# contenido de los registros
g.appear(g.text(UX + 60, SL[0] + 27, "GRP · 192.168.88.31", 16, g.OK, g.MONO, 600), 12, 100)
g.appear(g.text(UX + 60, SL[1] + 27, "Wave · 198.51.100.7", 16, g.OK, g.MONO, 600), 37, 100)
g.appear(g.text(UX + 60, SL[2] + 27, "no permitido (límite 2)", 16, g.GREY, g.MONO, 400), 0, 75)
g.appear(g.box(UX + 16, SL[2], UW - 32, 42, "none", g.BAD, rx=10, sw=2.5), 58, 75)
g.appear(g.box(UX + 16, SL[2], UW - 32, 42, g.BADBG, g.BAD, rx=10, sw=2.5)
         + g.text(UX + 32, SL[2] + 27, "3", 16, g.BAD, g.MONO, 600)
         + g.text(UX + 60, SL[2] + 27, "?? · 203.0.113.66", 16, g.BAD, g.MONO, 600), 86, 100)

# mensajes
X1, X2 = DX + DW, UX
def ida_vuelta(y, t0, resp, rcol, ok=True):
    g.token([(X1 + 70, y), (X2 - 70, y)], t0, t0 + 7, g.chip("REGISTER 1001", bg=g.BLUE, size=13, h=26), hold=t0 + 7.5)
    g.token([(X2 - 70, y), (X1 + 70, y)], t0 + 9, t0 + 15, g.chip(resp, bg=rcol, size=13, h=26), hold=t0 + 15.5)

for y, *_ in rows:
    g.add(g.wire(X1, y + DH / 2, X2, y + DH / 2, g.LINE, 2, "6 6"))
ida_vuelta(178 + DH / 2, 2, "200 OK", g.OK)
ida_vuelta(290 + DH / 2, 27, "200 OK", g.OK)
ida_vuelta(402 + DH / 2, 52, "rechazado", g.BAD)
ida_vuelta(402 + DH / 2, 77, "200 OK", g.AMB)
g.appear(g.pillc(DX + DW / 2, 178 + DH + 6, "registrado", g.OK, g.OKBG, 13, 24), 17, 100)
g.appear(g.pillc(DX + DW / 2, 290 + DH + 6, "registrado", g.OK, g.OKBG, 13, 24), 42, 100)
g.appear(g.pillc(DX + DW / 2, 402 + DH + 6, "afuera", g.BAD, g.BADBG, 13, 24), 67, 75)
g.appear(g.pillc(DX + DW / 2, 402 + DH + 6, "adentro, sin que nadie lo vea", g.BAD, g.BADBG, 13, 24), 92, 100)

g.add(g.note(DX, 532, 1104, None, ["Cada registro es un equipo que puede llamar con esa cuenta. Se deja 1, o 2 si la persona usa Wave, y se anota qué equipo ocupa cada uno."], "info"))

g.status(636, [
    (0, 25, "REGISTER y 200 OK: el GRP queda registrado con la 1001.", g.INK),
    (25, 50, "Dos equipos, dos registros: los dos que la ficha dice que existen.", g.OK),
    (50, 75, "El límite frena al tercero aunque tenga la clave correcta.", g.BAD),
    (75, 100, "Con lugar libre, un registro ajeno es un equipo más que llama a cuenta del cliente.", g.BAD),
])

g.done(2, "r1", "Una cuenta, varios equipos: cuántos registran",
       "Animación en cuatro tiempos con tres equipos a la izquierda, el GRP del escritorio (192.168.88.31), la app Wave en un celular (198.51.100.7) y un equipo ajeno (203.0.113.66), y a la derecha la extensión 1001 de la UCM con Concurrent Registrations en 2 y la lista de registros activos. "
       "1: el GRP manda REGISTER 1001, la central contesta 200 OK y ocupa el primer registro. "
       "2: la app Wave registra la misma cuenta y ocupa el segundo. "
       "3: un equipo ajeno con la clave filtrada pide registrar la 1001; no hay lugar y la central lo rechaza. "
       "4: con Concurrent Registrations en 3, el valor de fábrica, el mismo pedido recibe 200 OK y ocupa el tercer registro sin que nadie lo note. "
       "Nota: cada registro es un equipo que puede llamar con esa cuenta; se deja 1, o 2 si la persona usa Wave, y se anota qué equipo ocupa cada uno.",
       [10, 36, 64, 90])
