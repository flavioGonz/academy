#!/usr/bin/env python3
"""Lección 3 · Teoría · La vida de una suscripción pull point.
Sale de teoria_md (Cómo funciona): CreatePullPointSubscription crea el buzón; las propiedades llegan con PropertyOperation
Initialized al crear la suscripción y Changed cuando cambia el valor; OmniAccess pregunta con PullMessages cada 5 segundos,
la suscripción dura 300 segundos y se renueva antes de vencer; dos sondeos seguidos fallidos abren un corte de cámara;
el push es opcional y, mientras entrega, el pull se calla para no contar doble."""
from _anim_omni import new, out, when, seq

a = new(26, "ONVIF", "La vida de una suscripción, en el tiempo")
a.steps([
    "CreatePullPointSubscription por 300 s: llegan los valores con Initialized.",
    "Cada 5 s, PullMessages: vuelve vacío, o con Changed si el valor cambió.",
    "Antes de que venza, OmniAccess renueva la suscripción.",
    "Dos sondeos seguidos fallan: se abre un corte de cámara.",
    "Si el push entrega, el pull se calla para no contar doble.",
], still=3)

YO, YC = 250, 420
a.add(a.text(48, YO + 6, "omniaccess-web", 16, a.INK, a.MONO, 600))
a.add(a.text(48, YC + 6, "cámara", 16, a.INK, a.MONO, 600))
a.add(f'<line x1="196" y1="{YO}" x2="1152" y2="{YO}" stroke="{a.INK}" stroke-width="3"/>')
a.add(f'<line x1="196" y1="{YC}" x2="1152" y2="{YC}" stroke="{a.INK}" stroke-width="3"/>')

# puntos del tiempo (no proporcional)
P = {"0": 240, "5": 390, "10": 520, "ren": 690, "t": 810, "t5": 915, "t10": 1015}
LBL = {"0": "0 s", "5": "5 s", "10": "10 s", "ren": "antes de 300 s", "t": "t", "t5": "t + 5 s", "t10": "t + 10 s"}
for k, x in P.items():
    a.add(a.text(x, YC + 30, LBL[k], 15, a.GREY, a.MONO, 600, "middle"))
for x in ((P["10"] + P["ren"]) / 2 + 10, (P["ren"] + P["t"]) / 2):
    a.add(a.text(x, (YO + YC) / 2 + 8, "…", 28, a.GREY, a.MONO, 600, "middle"))


def ex(x, t0, t1, req, resp, color, rcolor=None, still=1, fail=False, ry=310):
    """pedido hacia abajo y respuesta hacia arriba en la posición x."""
    seq(a, f"M{x - 10} {YO + 8} V{YC - 10}", t0, t1, color, still=still, width=2.5)
    if req:
        when(a, a.text(x - 20, ry, req, 15, color, a.MONO, 600, "end"), t0, t1, still=still)
    if fail:
        when(a, f'<path d="M{x - 22} {YC - 34} l24 24 M{x + 2} {YC - 34} l-24 24" stroke="{a.BAD}" stroke-width="4" stroke-linecap="round"/>', t0 + 1, t1, still=still)
        return
    seq(a, f"M{x + 10} {YC - 8} V{YO + 10}", t0 + 1.5, t1, rcolor or color, still=still, width=2.5)
    if resp:
        when(a, a.text(x + 20, YC - 16, resp, 15, rcolor or color, a.MONO, 600), t0 + 1.5, t1, still=still)


# 1 · crear
ex(P["0"], 2, 100, "Create", "Initialized", a.BLUE, ry=340)
when(a, a.pill(P["0"], YC + 46, "Aforo 3", a.BLUE, a.WHITE, 15, 28, "middle"), 4, 100, still=1)
when(a, a.box(P["0"], YO - 52, P["t5"] - P["0"], 26, a.OKBG, a.OK, rx=6, sw=1.5)
     + a.text(P["0"] + 12, YO - 34, "suscripción · 300 s", 15, a.OK, a.MONO, 600), 4, 100, still=1)
# 2 · sondeos
ex(P["5"], 21, 100, "PullMessages", "vacío", a.GREY, ry=290)
ex(P["10"], 27, 100, "", "Changed", a.BLUE)
when(a, a.pill(P["10"], YC + 46, "Aforo 4", a.WHITE, a.BLUE, 15, 28, "middle"), 29, 100, still=1)
# 3 · renovar
ex(P["ren"], 41, 100, "renueva", "", a.OK, still=1)
when(a, a.box(P["ren"], YO - 52, 1152 - P["ren"], 26, a.OK, rx=6)
     + a.text(P["ren"] + 12, YO - 34, "renovada · 300 s más", 15, a.WHITE, a.MONO, 600), 43, 100, still=1)
# 4 · dos fallas
ex(P["t"], 61, 100, "", "vacío", a.GREY, still=1)
ex(P["t5"], 64, 100, "", "", a.BAD, still=1, fail=True)
ex(P["t10"], 68, 100, "", "", a.BAD, still=1, fail=True)
when(a, a.box(P["t5"] - 30, YC + 44, 1152 - P["t5"] + 30, 40, a.BADBG, a.BAD, rx=8, sw=2)
     + a.text(P["t5"] - 14, YC + 70, "corte de cámara abierto", 16, a.BAD, a.SANS, 600), 70, 100, still=1)

# 5 · push
when(a, a.box(48, 560, 1104, 50, a.WHITE, a.CYAN, rx=10, sw=2)
     + a.text(68, 591, "Push opcional: la cámara manda Notify a /api/onvif/notify. Mientras entrega, el pull se calla.", 16, a.INK, a.SANS, 600), 81, 100, still=0)
seq(a, f"M1110 {YC - 8} V{YO + 10}", 82, 100, a.CYAN, still=0, width=3, dash="7 5")
when(a, a.text(1100, YO + 40, "Notify", 15, a.CYAN, a.MONO, 600, "end"), 82, 100, still=0)

a.add(a.text(48, 646, "Cada mensaje trae tópico, fuente, nombre de la regla y datos. Deleted avisa que la propiedad desapareció.", 16, a.TXT, a.SANS, 600))

out(a, 3, 1, "La vida de una suscripción pull point",
    "Animación en cinco tiempos sobre una línea de tiempo no proporcional entre omniaccess-web, arriba, y la cámara Bosch, abajo. "
    "Tiempo 1: a los 0 s OmniAccess manda CreatePullPointSubscription; la suscripción dura 300 s y la cámara responde con los valores marcados Initialized, por ejemplo Aforo 3. "
    "Tiempo 2: cada 5 s pregunta con PullMessages; a los 5 s vuelve vacío y a los 10 s vuelve Changed con Aforo 4. "
    "Tiempo 3: antes de los 300 s, antes de que venza, OmniAccess renueva la suscripción por 300 s más. "
    "Tiempo 4: más tarde, en un momento t, el sondeo vuelve vacío; a t más 5 s y a t más 10 s falla; con dos fallas seguidas se abre un corte de cámara. "
    "Tiempo 5: el push es opcional; la cámara manda Notify a /api/onvif/notify y, mientras entrega, el pull se calla para no contar doble. "
    "Al pie: cada mensaje trae tópico, fuente, nombre de la regla y datos; Deleted avisa que la propiedad desapareció.",
    [10, 30, 50, 75, 94])
