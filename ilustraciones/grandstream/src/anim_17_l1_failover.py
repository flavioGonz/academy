#!/usr/bin/env python3
"""Lección 17 (Hasta que suene) · Laboratorio, paso 6: desconectar el FXO1 y repetir la llamada al celular. Con la
línea 1 la llamada sale con su número; sin ella, si el failover anda sale por la línea 2 y el celular ve el número de
la 2; si no sale, la alternativa es una troncal con las dos FXO en Ascend. Fuentes: la lección (ruta Uruguay_Antel con
_09XXXXXXX, Use Trunk Antel_Linea1, Failover Trunk Antel_Linea2; el que recibe ve el número de la línea por la que
salió porque Outbound Route CID no aplica a analógicas; si no sale, Antel_Grupo en Ascend)."""
from _anim_gs_red import R

g = R(T=26, fix=62, kicker="GRANDSTREAM · HASTA QUE SUENE · LABORATORIO",
      title="Sin la línea 1: ¿sale por la 2 y con qué número?")
g.steps([
    "La 1001 marca 098 000 000: coincide con _09XXXXXXX y sale por Antel_Linea1.",
    "Desconectás el cable del FXO1 y repetís: la ruta no puede usar Antel_Linea1.",
    "Si el failover anda, sale por Antel_Linea2: el celular ve el número de la línea 2.",
    "Si no sale, la alternativa es Antel_Grupo con FXO 1 y 2 en Ascend. Volvé a conectar.",
])

Y = 196
g.add(g.dev(48, Y + 60, 200, 84, "1001", "marca afuera", icon="tel"))
RX, RW = 290, 330
g.add(g.box(RX, Y - 6, RW, 196, g.WHITE, g.LINE, rx=14))
g.add(g.text(RX + 18, Y + 22, "Outbound Route · Uruguay_Antel", 15, g.INK, g.MONO, 600))
g.add(g.text(RX + 18, Y + 52, "Pattern _09XXXXXXX (y otros)", 14, g.TXT, g.MONO))
g.add(g.text(RX + 18, Y + 88, "Use Trunk", 14, g.GREY, g.MONO) + g.text(RX + 18, Y + 110, "Antel_Linea1", 16, g.INK, g.MONO, 600))
g.add(g.text(RX + 18, Y + 146, "Failover Trunk", 14, g.GREY, g.MONO) + g.text(RX + 18, Y + 168, "Antel_Linea2", 16, g.INK, g.MONO, 600))
g.appear(g.box(RX + 8, Y + 70, RW - 16, 50, "none", g.OK, rx=8, sw=2.5), 4, 25)
g.appear(g.box(RX + 8, Y + 70, RW - 16, 50, "none", g.BAD, rx=8, sw=2.5), 27, 50)
g.appear(g.box(RX + 8, Y + 128, RW - 16, 50, "none", g.OK, rx=8, sw=2.5), 52, 75)
g.add(g.wire(248, Y + 102, RX, Y + 102, g.BLUE))

PX = 680
g.appear(g.port(PX, Y + 6, "FXO1", "libre", w=190), 0, 4)
g.appear(g.port(PX, Y + 6, "FXO1", "uso", w=190), 4, 25)
g.appear(g.port(PX, Y + 6, "FXO1", "gris", w=190), 27, 100)
g.appear(g.port(PX, Y + 6, "FXO1", "libre", w=190), 92, 100)
g.appear(g.port(PX, Y + 120, "FXO2", "libre", w=190), 0, 52)
g.appear(g.port(PX, Y + 120, "FXO2", "uso", w=190), 52, 75)
g.appear(g.port(PX, Y + 120, "FXO2", "libre", w=190), 75, 100)
g.add(g.wire(RX + RW, Y + 95, PX, Y + 28, g.LINE, 3))
g.add(g.wire(RX + RW, Y + 153, PX, Y + 142, g.LINE, 3))
g.appear(g.mark(PX + 214, Y + 28, False, 14) + g.text(PX + 236, Y + 34, "cable afuera", 15, g.BAD, g.MONO, 600), 29, 90)

CX = 960
g.add(g.dev(CX, Y + 50, 192, 104, "Celular", "098 000 000", icon="phone"))
g.appear(g.box(CX, Y + 170, 192, 74, "#03213C", None, rx=12) + g.text(CX + 16, Y + 196, "le aparece", 13, g.SKY, g.MONO)
         + g.text(CX + 16, Y + 226, "número línea 1", 16, g.MINT, g.MONO, 600), 10, 25)
g.appear(g.box(CX, Y + 170, 192, 74, "#03213C", None, rx=12) + g.text(CX + 16, Y + 196, "le aparece", 13, g.SKY, g.MONO)
         + g.text(CX + 16, Y + 226, "número línea 2", 16, g.GOLD, g.MONO, 600), 60, 75)
g.token([(148, Y + 40), (148, Y - 24), (1056, Y - 24)], 3, 10, g.chip("098 000 000", bg=g.BLUE, size=13, h=24), hold=11)
g.appear(g.text(455, Y - 18, "Antel_Linea1 no está", 15, g.BAD, g.MONO, 600, "middle"), 33, 50)
g.token([(250, Y + 216), (930, Y + 216)], 53, 60, g.chip("098 000 000", bg=g.OK, size=13, h=24), hold=61)

g.appear(g.note(48, 470, 1104, None, ["El celular ve el número de la línea por la que salió: Outbound Route CID no aplica a troncales analógicas. Se le avisa al cliente antes de entregar."], "info"), 0, 75)
g.appear(g.note(48, 470, 1104, "Si no salió por la 2", ["Una troncal Antel_Grupo con FXO 1 y 2 y DAHDI Out Line Selection en Ascend toma la línea libre. Después de probar, cada cable vuelve a su FXO."], "amb"), 75, 100)
g.add(g.text(48, 600, "098 000 000 es un número de ejemplo. El 911 no se usa para pruebas.", 15, g.GREY, g.SANS))

g.done(17, "l1", "Sin la línea 1: ¿sale por la 2 y con qué número?",
       "Animación en cuatro tiempos con la interna 1001, la ruta saliente Uruguay_Antel (patrón _09XXXXXXX entre otros, Use Trunk Antel_Linea1 y Failover Trunk Antel_Linea2), los puertos FXO1 y FXO2 y un celular de ejemplo, 098 000 000. "
       "1: la 1001 marca el celular, coincide con _09XXXXXXX y la llamada sale por Antel_Linea1: el celular ve el número de la línea 1. "
       "2: se desconecta el cable del FXO1, el puerto queda gris y al repetir la llamada la ruta no puede usar Antel_Linea1. "
       "3: si el failover anda, sale por Antel_Linea2 y el celular ve el número de la línea 2, porque Outbound Route CID no aplica a troncales analógicas. "
       "4: si no sale, la alternativa es una troncal Antel_Grupo con FXO 1 y 2 y DAHDI Out Line Selection en Ascend, que toma la libre; al terminar, cada cable vuelve a su FXO. "
       "El 911 no se usa para pruebas.",
       [8, 36, 62, 92])
