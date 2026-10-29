#!/usr/bin/env python3
"""Lección 18 (Diagnóstico de línea) · Resumen, "Cómo se ve en la red": el método aplicado al caso del FXO2 que se ocupa
y se libera solo. Cada prueba saca un sospechoso: el par medido sin la central, los equipos en paralelo, el cruce de
pares entre FXO1 y FXO2 y, con eso, el reclamo a Antel con datos. Los resultados son un ejemplo de uno de los caminos.
Fuentes: la lección (orden: medir el par sin la central, teléfono de prueba, desconectar lo que cuelga, cruzar pares,
revisar ruta y detección, grabar; si la falla sigue a la línea es la línea, si se queda en el puerto es la UCM;
reclamos al 121, *121 desde un móvil Antel, empresas 0800 2599, con número, síntoma, horarios, tensión y cruce)."""
from _anim_gs_red import R

g = R(T=28, fix=66, kicker="GRANDSTREAM · DIAGNÓSTICO DE LÍNEA · CÓMO SE VE EN LA RED",
      title="Del síntoma al reclamo: cada prueba saca un sospechoso")
g.steps([
    "El FXO2 se ocupa y se libera solo. Medís el par sin la central: compará con la ficha.",
    "Desconectás todo lo que cuelga del par 2 y repetís: si la falla se va, era un equipo.",
    "Cruzás los pares: la línea 2 al FXO1. Si la falla la sigue, es la línea; si no, la UCM.",
    "Con los datos, el reclamo: número, síntoma, horarios, tensión y el resultado del cruce.",
])

PAR = "#3B4D61"
def par(pts, col=PAR):
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    return (f'<path d="{d}" stroke="{col}" stroke-width="8" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="#F7FAFD" stroke-width="2" fill="none" stroke-linejoin="round"/>')

L1, L2 = 206, 330
g.add(g.dev(48, L1, 200, 76, "Línea 1", "par A", icon="antel"))
g.add(g.dev(48, L2, 200, 76, "Línea 2", "par B", icon="antel"))
PX = 640
def puertos(s1, s2, t0, t1):
    g.appear(g.port(PX, L1 + 16, "FXO1", s1, w=200) + g.port(PX, L2 + 16, "FXO2", s2, w=200), t0, t1)
puertos("libre", "uso", 0, 52)
puertos("uso", "libre", 52, 100)
# pares derechos y cruzados
g.appear(par([(248, L1 + 38), (PX, L1 + 38)]) + par([(248, L2 + 38), (PX, L2 + 38)]), 0, 52)
g.appear(par([(248, L1 + 38), (440, L1 + 38), (520, L2 + 38), (PX, L2 + 38)]) + par([(248, L2 + 38), (440, L2 + 38), (520, L1 + 38), (PX, L1 + 38)]), 52, 100)
# la falla
loop = lambda: g.chip("loop ~10 s", bg=R.USO, size=13, h=24)
g.token([(PX + 100, L2 - 4), (PX + 100, L2 - 4)], 0, 50, loop(), hold=51)
g.token([(PX + 100, L1 - 4), (PX + 100, L1 - 4)], 54, 100, loop(), hold=100)
g.fijo_only(f'<g transform="translate({PX + 100} {L1 - 4})">' + loop() + '</g>')
# 1 · medición
g.appear(g.box(300, L2 + 86, 300, 40, g.SLATE, None, rx=10) + g.text(318, L2 + 112, "par B, reposo: como la ficha", 15, g.INK, g.MONO, 600), 4, 25)
# 2 · paralelos
g.appear(g.box(300, L2 + 86, 300, 40, g.SLATE, None, rx=10) + g.text(318, L2 + 112, "alarma, posnet, fax: afuera", 15, g.INK, g.MONO, 600), 29, 50)
g.appear(g.text(450, L2 + 150, "la falla sigue (ejemplo)", 15, g.AMB, g.SANS, 600, "middle"), 34, 50)
# 3 · cruce
g.appear(g.text(450, L2 + 112, "la falla pasó al FXO1: sigue a la línea 2", 15, g.BAD, g.SANS, 600, "middle"), 58, 75)

# sospechosos
SX, SW = 880, 272
g.add(g.box(SX, 186, SW, 290, g.WHITE, g.LINE, rx=14))
g.add(g.text(SX + 18, 214, "sospechosos", 15, g.GREY, g.MONO))
sus = [("par y Antel", 75), ("equipo en paralelo", 40), ("puerto FXO2", 66), ("troncal, ruta, detección", 66)]
for k, (n, t_out) in enumerate(sus):
    y = 248 + k * 52
    g.add(g.box(SX + 14, y - 26, SW - 28, 40, g.SLATE, None, rx=8) + g.text(SX + 30, y, n, 15, g.INK, g.SANS, 600))
    if t_out < 75 or k == 0:
        pass
for k, t_out in ((1, 40), (2, 66), (3, 66)):
    y = 248 + k * 52
    g.appear(f'<line x1="{SX + 26}" y1="{y - 6}" x2="{SX + SW - 26}" y2="{y - 6}" stroke="{g.BAD}" stroke-width="2.5"/>', t_out, 100)
g.appear(g.box(SX + 14, 222, SW - 28, 40, "none", g.BAD, rx=8, sw=3), 66, 100)

# reclamo
g.appear(g.term(48, 500, 1104, 112, "Reclamo a Antel: 121 (o *121 desde un móvil Antel) · empresas 0800 2599", [
    ("línea 2 · loop cada ~10 s desde ayer de mañana · reposo como la ficha", g.MINT),
    ("sin equipos en paralelo sigue · al cruzar pares la falla siguió a la línea", g.MINT),
], size=16, lh=28), 77, 100)
g.appear(g.note(48, 500, 1104, None, ["Los resultados son un ejemplo de uno de los caminos. Si al cruzar la falla se queda en el FXO2, se sigue por la central:", "troncal, ruta entrante, Ring Timeout, polaridad y la grabación del puerto."], "info"), 0, 77)

g.done(18, "r1", "Del síntoma al reclamo: cada prueba saca un sospechoso",
       "Animación en cuatro tiempos con las líneas 1 y 2 de Antel, sus pares A y B, los puertos FXO1 y FXO2 y, a la derecha, la lista de sospechosos: par y Antel, equipo en paralelo, puerto FXO2, y troncal, ruta y detección. Los resultados son un ejemplo de uno de los caminos. "
       "1: el FXO2 se ocupa y se libera solo, un loop de unos 10 segundos; se mide el par B sin la central y se compara con la ficha: en reposo da como siempre. "
       "2: se desconecta todo lo que cuelga del par 2 (alarma, posnet, fax) y la falla sigue: sale de la lista el equipo en paralelo. "
       "3: se cruzan los pares, la línea 2 al FXO1 y la línea 1 al FXO2; la falla pasa al FXO1 y sigue a la línea 2: salen el puerto y la configuración, y queda el par y Antel. Si se hubiera quedado en el FXO2, se seguiría por la central. "
       "4: el reclamo a Antel, al 121, al *121 desde un móvil Antel o al 0800 2599 para empresas, con el número, el síntoma, desde cuándo, la tensión medida y el resultado del cruce. Después, cada par vuelve a su puerto.",
       [10, 38, 62, 90])
