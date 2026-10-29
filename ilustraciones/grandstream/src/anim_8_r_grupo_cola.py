#!/usr/bin/env python3
"""Lección 8 (Grupo o cola) · Resumen, "Cómo se ve en la red": tres llamadas casi juntas, primero contra un grupo
y después contra una cola. El grupo hace sonar y, si no hay quien atienda, manda al destino del grupo; la cola
retiene con música y entrega cuando un agente se libera (después del descanso). Fuentes: manual UCM630x (Ring Group:
Ring Simultaneously, Skip Busy Agent, buzón o Default Destination si nadie atiende) y la lección (cola: música,
estrategia, Agent Rest Time 10 s, Max Queue Length)."""
from _anim_gs_red import R

g = R(T=28, fix=70, kicker="GRANDSTREAM · GRUPO O COLA · CÓMO SE VE EN LA RED",
      title="Tres llamadas juntas: el grupo suena, la cola espera")
g.steps([
    "Grupo 6000, a la vez: entra A, suenan la 1001 y la 1002, atiende la 1001.",
    "Entra B: con Skip Busy Agent suena solo la 1002. Entra C: no hay nadie y va al buzón.",
    "Cola 6500: A y B van a los agentes y C espera en la fila, con música.",
    "La 1001 corta, descansa 10 s y la cola le entrega a C: nadie se fue al buzón.",
])

CX, CY, CW, CH = 330, 190, 470, 220
AX, AW = 900, 252
A1, A2 = 196, 300
g.add(g.dev(AX, A1, AW, 84, "1001", icon="tel"))
g.add(g.dev(AX, A2, AW, 84, "1002", icon="tel"))
g.add(g.text(48, 200, "llamadas que entran", 15, g.GREY, g.MONO))

# escena 1: grupo
g.appear(g.box(CX, CY, CW, CH, g.WHITE, g.LINE, rx=16)
         + g.text(CX + 20, CY + 34, "Ring Group 6000", 19, g.INK, g.HEAD, 600)
         + g.text(CX + 20, CY + 64, "Ring Simultaneously", 15, g.TXT, g.MONO)
         + g.text(CX + 20, CY + 88, "Skip Busy Agent: Sí", 15, g.TXT, g.MONO)
         + g.text(CX + 20, CY + 112, "sin espera: suena o sigue", 15, g.GREY, g.SANS), 0, 50)
g.appear(g.box(CX, CY + CH + 20, CW, 64, g.SLATE, None, rx=12)
         + g.text(CX + 20, CY + CH + 58, "si nadie atiende: buzón del grupo", 16, g.INK, g.SANS, 600), 0, 50)
# escena 2: cola
g.appear(g.box(CX, CY, CW, CH, g.WHITE, g.LINE, rx=16)
         + g.text(CX + 20, CY + 34, "Call Queue 6500", 19, g.INK, g.HEAD, 600)
         + g.text(CX + 20, CY + 64, "Least Recent · Max Queue Length 5", 15, g.TXT, g.MONO)
         + g.text(CX + 20, CY + 100, "fila", 15, g.GREY, g.MONO), 50, 100)
for k in range(3):
    g.appear(g.box(CX + 70 + k * 130, CY + 82, 116, 40, g.SLATE, None, rx=10), 50, 100)
g.appear(g.box(CX, CY + CH + 20, CW, 64, g.SLATE, None, rx=12)
         + g.text(CX + 20, CY + CH + 58, "si se llena o no hay agentes: Failover Destination", 16, g.INK, g.SANS, 600), 50, 100)

chip = lambda s, c: g.chip(s, bg=c, size=14, h=28)
IN = {"A": 248, "B": 300, "C": 352}
def entra(n, t0, dest, t1, hold, c=None):
    g.token([(140, IN[n]), (CX + CW / 2, CY + CH / 2 + 50), dest], t0, t1, chip(f"llamada {n}", c or g.CYAN), hold=hold)

# 1 · A al grupo
entra("A", 2, (AX - 60, A1 + 42), 9, 50)
g.appear(g.pillc(AX + 196, A1 + 30, "suena", g.CYAN, "#E3F4FA", 13, 24) + g.pillc(AX + 196, A2 + 30, "suena", g.CYAN, "#E3F4FA", 13, 24), 9, 14)
g.appear(g.pillc(AX + 182, A1 + 30, "hablando con A", g.OK, g.OKBG, 13, 24), 14, 50)
# 2 · B solo a la 1002; C al buzón
entra("B", 26, (AX - 60, A2 + 42), 32, 50)
g.appear(g.pillc(AX + 196, A2 + 30, "suena", g.CYAN, "#E3F4FA", 13, 24), 32, 36)
g.appear(g.pillc(AX + 182, A2 + 30, "hablando con B", g.OK, g.OKBG, 13, 24), 36, 50)
g.token([(140, IN["C"]), (CX + CW / 2, CY + CH / 2 + 50), (CX + CW - 60, CY + CH + 52)], 39, 45, chip("llamada C", g.AMB), hold=50)
g.appear(g.text(CX + 20, CY + CH + 104, "C no espera: nadie libre, al buzón", 16, g.AMB, g.SANS, 600), 45, 50)
# 3 · cola
entra("A", 52, (AX - 60, A1 + 42), 57, 77)
entra("B", 55, (AX - 60, A2 + 42), 60, 100)
g.appear(g.pillc(AX + 182, A1 + 30, "hablando con A", g.OK, g.OKBG, 13, 24), 57, 77)
g.appear(g.pillc(AX + 182, A2 + 30, "hablando con B", g.OK, g.OKBG, 13, 24), 60, 100)
g.token([(140, IN["C"]), (CX + 128, CY + 102)], 62, 67, chip("C", g.AMB), hold=88)
g.appear(g.text(CX + 20, CY + 160, "♪ C escucha música en la fila", 16, g.CYAN, g.SANS, 600), 67, 88)
# 4 · descanso y entrega
g.appear(g.pillc(AX + 182, A1 + 30, "descansa 10 s", g.AMB, g.AMBBG, 13, 24), 77, 88)
g.token([(CX + 128, CY + 102), (AX - 60, A1 + 42)], 88, 93, chip("llamada C", g.CYAN), hold=100)
g.appear(g.pillc(AX + 182, A1 + 30, "hablando con C", g.OK, g.OKBG, 13, 24), 93, 100)
g.fijo_only(f'<g transform="translate({CX + 128} {CY + 102})">' + chip("C", g.AMB) + '</g>'
            + f'<g transform="translate({AX - 60} {A1 + 42})">' + chip("llamada A", g.CYAN) + '</g>'
            + f'<g transform="translate({AX - 60} {A2 + 42})">' + chip("llamada B", g.CYAN) + '</g>')

g.status(620, [
    (0, 25, "El grupo hace sonar teléfonos; no retiene a nadie.", g.INK),
    (25, 50, "Con todos ocupados, el grupo no tiene dónde dejar la llamada: sigue de largo.", g.AMB),
    (50, 75, "La cola retiene a quien llama y lo ordena en una fila.", g.OK),
    (75, 100, "Cuando un agente queda libre, la cola le entrega la próxima.", g.OK),
])

g.done(8, "r1", "Tres llamadas juntas: el grupo suena, la cola espera",
       "Animación en cuatro tiempos con tres llamadas, A, B y C, que entran casi juntas, y dos agentes, la 1001 y la 1002; primero contra un grupo y después contra una cola. "
       "1: Ring Group 6000 en Ring Simultaneously: entra A, suenan la 1001 y la 1002 a la vez y atiende la 1001. "
       "2: entra B y, con Skip Busy Agent, suena solo la 1002, que atiende; entra C, no hay nadie libre y, como el grupo no retiene, va al buzón del grupo. "
       "3: Call Queue 6500 con Least Recent y Max Queue Length 5: A y B van a los agentes y C espera en la fila escuchando música. "
       "4: la 1001 corta, descansa los 10 segundos de Agent Rest Time y la cola le entrega C; ninguna llamada fue al buzón. "
       "Si la cola se llena o se queda sin agentes, la llamada va al Failover Destination.",
       [8, 32, 46, 70, 82, 96])
