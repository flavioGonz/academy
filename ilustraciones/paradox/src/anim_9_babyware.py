"""Teoría lección 9: BabyWare conecta, verifica las dos llaves y lee la central."""
from _apdx import *

a = new(20, "Cómo entra BabyWare y por qué una sesión ocupa el lugar")
a.steps(["BabyWare llama a la central con ID de panel y contraseña de PC.",
         "La central compara con [910] y [911]: coinciden, acepta.",
         "Recepción completa: toda la programación viaja a la PC.",
         "Con la sesión abierta, otra conexión por el módulo IP queda afuera."], still=2)
a.add(card(a, 48, 180, 250, 340, "BabyWare", "notebook"))
a.add(card(a, 902, 180, 250, 340, "Central", "SP+ o MG", dark=True))
a.add(a.box(922, 260, 210, 70, "#0B3A66", None, rx=10) + a.text(938, 288, "[910] 1A2B", 16, "#fff", a.MONO, 600) + a.text(938, 314, "[911] 3C4D", 16, "#fff", a.MONO, 600))
a.add(line(a, "M298 350H902", a.LINE, 3))
a.add(a.text(600, 340, "307USB o módulo IP", 15, a.GREY, a.MONO, 600, "middle"))
# mensaje 1
at(a, a.arrow("M300 260H896", a.BLUE) + chip(a, 600, 230, "ID 1A2B · PC 3C4D", "info", anchor="middle"), 0, 25, 0)
at(a, a.arrow("M900 300H304", a.OK) + chip(a, 600, 268, "coinciden: conectado", "ok", anchor="middle"), 25, 100, 1)
# recepción
a.add(a.box(68, 400, 210, 22, a.SLATE, None, rx=11))
bar = a.keyframes([(0, 0.02), (50, 0.02), (72, 1), (100, 1)], "transform", "scaleX({})")
a.add(a.group(a.box(68, 400, 210, 22, a.CYAN, None, rx=11), bar, still=1, origin="68px 411px"))
a.add(a.text(68, 450, "copia de la central", 15, a.GREY, a.SANS, 600))
at(a, chip(a, 68, 466, "guardada: obra y fecha", "ok"), 72, 100, 1)
# intruso
at(a, card(a, 520, 400, 260, 110, "App o integración", "por el módulo IP") + a.arrow("M650 400V364", a.BAD) + chip(a, 650, 520, "ocupado: una conexión", "bad", anchor="middle"), 75, 100, 0)
caption(a, 600, [(0, 25, "No es el código de instalador: son dos llaves aparte, en hexadecimal.", None),
                 (25, 50, "Si no coinciden, BabyWare no conecta. Si siguen de fábrica, conecta cualquiera.", a.AMB),
                 (50, 75, "Esa copia es tu punto de vuelta antes de cualquier cambio.", a.OK),
                 (75, 100, "Por eso se desconecta BabyWare al terminar.", a.BAD)], still=2)
write(a, "9-t1.svg", "Cómo entra BabyWare y por qué una sesión ocupa el lugar",
      "Animación en cuatro tiempos entre BabyWare en una notebook y la central. 1: BabyWare llama con ID de panel 1A2B y contraseña de PC 3C4D, valores de ejemplo. "
      "2: la central compara con sus secciones 910 y 911, coinciden y acepta. 3: una barra muestra la recepción completa de la programación, que queda guardada con el nombre de la obra y la fecha. "
      "4: con la sesión abierta, una app o integración que entra por el módulo IP queda afuera, porque el módulo atiende una conexión a la vez.")
