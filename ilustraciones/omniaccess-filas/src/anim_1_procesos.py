#!/usr/bin/env python3
"""Lección 1 · Teoría · Los tres procesos que mueven un número.
Sale de teoria_md (Cómo funciona): la cámara cuenta; omniaccess-web busca los eventos ONVIF cada 5 segundos y, cuando un
valor cambia, lo guarda como evento de fila (canal Aforo, Entrada o Salida, con la hora); el evento se reenvía en vivo a
los navegadores (omniaccess-webhooks); si el aforo llega al umbral, se arma un despacho que dispatch-worker manda por
Telegram, WhatsApp o push."""
from _anim_omni import new, out, when, travel, seq, lane

a = new(24, "EL RECORRIDO", "Un cambio de aforo, proceso por proceso")
a.steps([
    "Con aforo 7, la pregunta vuelve sin cambios. Después la cámara cuenta 8.",
    "5 s después pregunta otra vez: el valor cambió y lo guarda.",
    "omniaccess-webhooks lo reenvía en vivo a los navegadores abiertos.",
    "Llegó al umbral: se arma un despacho y dispatch-worker lo manda.",
], still=1)

XS = [140, 370, 600, 830, 1060]
TOP, BOT = 178, 590
lane(a, XS[0], TOP, BOT, "Cámara Bosch", "IVA Pro", w=210)
lane(a, XS[1], TOP, BOT, "omniaccess-web", "sondeo ONVIF", w=210)
lane(a, XS[2], TOP, BOT, "webhooks", "en vivo", w=210)
lane(a, XS[3], TOP, BOT, "Navegadores", "Monitor, kiosko", w=210)
lane(a, XS[4], TOP, BOT, "dispatch-worker", "avisos", w=210)

# 1: la cámara cuenta
a.add(a.group(a.pill(XS[0], 262, "Aforo 7", a.INK, a.SLATE, 16, 32, "middle"), a.keyframes([(0, 1), (14, 1), (15, 0), (99, 0), (100, 1)]), still=0))
a.add(a.group(a.pill(XS[0], 262, "Aforo 8", a.WHITE, a.BLUE, 16, 32, "middle"), a.keyframes([(0, 0), (14, 0), (15, 1), (99, 1), (100, 0)]), still=1))

# 2: sondeo cada 5 s (dos preguntas; la segunda trae el cambio)
seq(a, f"M{XS[1] - 6} 318 H{XS[0] + 8}", 3, 50, a.GREY, "PullMessages", (XS[0] + XS[1]) / 2, 308, still=0, dash="6 5")
seq(a, f"M{XS[0] + 6} 344 H{XS[1] - 8}", 6, 50, a.GREY, "sin cambios", (XS[0] + XS[1]) / 2, 364, still=0, dash="6 5")
seq(a, f"M{XS[1] - 6} 400 H{XS[0] + 8}", 36, 100, a.BLUE, "PullMessages · 5 s después", (XS[0] + XS[1]) / 2, 390, still=1)
seq(a, f"M{XS[0] + 6} 428 H{XS[1] - 8}", 39, 100, a.BLUE, "Changed · Aforo 8", (XS[0] + XS[1]) / 2, 450, still=1)
travel(a, (XS[0] + 20, 428), (XS[1] - 20, 428), 39, 44, dot=8)
when(a, a.box(XS[1] + 12, 300, 200, 70, a.WHITE, a.BLUE, rx=10, sw=2)
     + a.text(XS[1] + 26, 326, "evento de fila", 15, a.BLUE, a.MONO, 600)
     + a.text(XS[1] + 26, 352, "Aforo · 8 · hora", 15, a.INK, a.MONO, 600), 44, 100, still=1)

# 3: en vivo
seq(a, f"M{XS[1] + 6} 480 H{XS[2] - 8}", 52, 100, a.CYAN, "evento", (XS[1] + XS[2]) / 2, 470, still=0)
seq(a, f"M{XS[2] + 6} 480 H{XS[3] - 8}", 56, 100, a.CYAN, "en vivo", (XS[2] + XS[3]) / 2, 470, still=0)
travel(a, (XS[1] + 20, 480), (XS[3] - 20, 480), 52, 60, dot=8, bg=a.CYAN)
when(a, a.pill(XS[3], 500, "Aforo 8", a.WHITE, a.BLUE, 16, 32, "middle"), 60, 100, still=0)

# 4: umbral y despacho
when(a, a.pill(XS[1], 548, "umbral 8: despacho", a.BAD, a.BADBG, 15, 30, "middle"), 77, 100, still=0)
seq(a, f"M{XS[1] + 90} 563 H{XS[4] - 8}", 79, 100, a.BAD, "despacho", (XS[2] + XS[3]) / 2, 553, still=0)
travel(a, (XS[1] + 110, 563), (XS[4] - 20, 563), 79, 86, dot=8, bg=a.BAD)
when(a, a.box(XS[4] - 92, 272, 184, 136, a.WHITE, a.LINE, rx=12) + a.text(XS[4], 300, "Telegram", 16, a.INK, a.SANS, 600, "middle") + a.text(XS[4], 330, "WhatsApp", 16, a.INK, a.SANS, 600, "middle")
     + a.text(XS[4], 360, "push", 16, a.INK, a.SANS, 600, "middle") + a.text(XS[4], 392, "con reintentos", 15, a.GREY, a.MONO, 600, "middle"), 87, 100, still=0)

a.add(a.text(48, 636, "Todo esto corre en el Modo Cola. Si el número está mal, mirá la cámara; si no llega, mirá el camino.", 16, a.TXT, a.SANS, 600))

out(a, 1, 1, "Un cambio de aforo, proceso por proceso",
    "Animación en cuatro tiempos, como diagrama de secuencia con cinco columnas: la cámara Bosch con IVA Pro, omniaccess-web (sondeo ONVIF), omniaccess-webhooks (en vivo), los navegadores (Monitor, kiosko) y dispatch-worker (avisos). "
    "Tiempo 1: con aforo 7, omniaccess-web pregunta con PullMessages y vuelve sin cambios; después la cámara cuenta y el aforo de la zona de la fila pasa a 8. "
    "Tiempo 2: 5 segundos después vuelve a preguntar y llega Changed con Aforo 8; lo guarda como evento de fila con canal Aforo, valor 8 y la hora. "
    "Tiempo 3: el evento pasa a omniaccess-webhooks, que lo reenvía en vivo a los navegadores abiertos, que muestran Aforo 8. "
    "Tiempo 4: el aforo llegó al umbral de 8, se arma un despacho y dispatch-worker lo manda por Telegram, WhatsApp o push, con reintentos. "
    "Al pie: todo esto corre en el Modo Cola; si el número está mal se mira la cámara, si no llega se mira el camino.",
    [8, 46, 66, 94])
