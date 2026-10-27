#!/usr/bin/env python3
"""Lección 6 · teoría: el portero junta los dígitos DTMF, compara con el código del relé y revisa la lista blanca."""
from _anim_akuvox import Anim, A, token, chip, appear, mark, finish

a = Anim(T=24, kicker="AKUVOX · DTMF", title="Cómo decide el portero si el código abre")
a.steps([
    "El monitor manda cada tecla como evento RFC 2833 dentro del RTP.",
    "Con los 3 dígitos del DTMF Mode, el portero compara con el código del relé.",
    "Quien llama está en contactos (lista blanca): dispara el relé A.",
    "Monitor en SIP INFO y portero en RFC 2833: el código nunca llega.",
], still=2)

YS, YR = 292, 404          # carriles: señalización SIP y RTP
MX1, PX0 = 280, 604
# monitor
a.add(a.box(48, 236, 232, 210, A.WHITE, A.LINE))
a.add(a.text(70, 276, "Monitor", 21, A.INK, A.HEAD, 600))
a.add(a.text(70, 302, "DTMF Type", 14, A.GREY, A.MONO))
appear(a, a.text(70, 326, "RFC2833", 17, A.OK, A.MONO, 600), 0, 75, still=1)
appear(a, a.text(70, 326, "SIP INFO", 17, A.BAD, A.MONO, 600), 75, 100, still=0)
a.add(a.text(70, 372, "tecla de apertura", 14, A.GREY, A.MONO))
a.add(a.box(70, 384, 120, 40, A.CYAN, None, rx=10) + a.text(130, 410, "Abrir", 16, A.WHITE, A.SANS, 600, "middle"))

# carriles
a.add(f'<line x1="{MX1}" y1="{YS}" x2="{PX0}" y2="{YS}" stroke="{A.GREY}" stroke-width="2.5" stroke-dasharray="7 6"/>')
a.add(a.text((MX1 + PX0) / 2, YS - 16, "señalización SIP", 15, A.GREY, A.MONO, 600, "middle"))
a.add(a.box(MX1, YR - 20, PX0 - MX1, 40, "#E4F5FB", None, rx=8))
a.add(a.text((MX1 + PX0) / 2, YR + 46, "RTP · el mismo camino que el audio", 15, A.CYAN, A.MONO, 600, "middle"))
aud = f'<rect x="-11" y="-6" width="22" height="12" rx="3" fill="#9FD7EA"/>'
for k in range(16):
    t0 = k * 6.2
    token(a, [(MX1 + 14, YR), (PX0 - 14, YR)], t0, min(t0 + 6, 99.6), aud, hold=min(t0 + 6.1, 99.8))

# portero
a.add(a.box(PX0, 180, 548, 380, A.WHITE, A.LINE, rx=18))
a.add(a.text(PX0 + 24, 216, "Portero", 21, A.INK, A.HEAD, 600))
a.add(a.text(PX0 + 124, 216, "DTMF Type: RFC2833 · DTMF Mode: 3 dígitos", 14, A.GREY, A.MONO))
a.add(a.text(PX0 + 24, 268, "dígitos recibidos", 15, A.TXT, A.SANS, 600))
SL = [PX0 + 24 + i * 64 for i in range(3)]
for x in SL:
    a.add(a.box(x, 282, 54, 60, A.SLATE, A.LINE, rx=10))
a.add(a.text(PX0 + 236, 322, "=", 28, A.GREY, A.MONO, 600, "middle"))
a.add(a.text(PX0 + 272, 268, "Relay A · código", 15, A.TXT, A.SANS, 600))
a.add(a.box(PX0 + 272, 282, 150, 60, A.SLATE, A.LINE, rx=10) + a.text(PX0 + 347, 322, "731", 26, A.INK, A.MONO, 600, "middle"))

digits = "731"
for i, d in enumerate(digits):
    t0 = 2 + i * 6.5
    t1 = t0 + 6
    token(a, [(MX1, YR), (PX0 - 30, YR), (PX0 - 30, 312), (SL[i] + 27, 312)], t0, t1, chip(a, d, bg=A.OK, size=18, h=32))
    appear(a, a.text(SL[i] + 27, 324, d, 28, A.INK, A.MONO, 600, "middle"), t1, 75, still=1)

# comparación
appear(a, a.box(SL[0] - 4, 278, 190, 68, "none", A.OK, rx=12, sw=3) + a.box(PX0 + 268, 278, 158, 68, "none", A.OK, rx=12, sw=3)
       + a.text(PX0 + 236, 372, "coinciden", 15, A.OK, A.MONO, 600, "middle"), 28, 75, still=1)
# lista blanca
a.add(a.text(PX0 + 24, 416, "Open Relay Via DTMF: Only Contacts List", 15, A.TXT, A.MONO))
appear(a, mark(a, PX0 + 40, 448, True, 14) + a.text(PX0 + 64, 454, "quien llama está en contactos", 16, A.OK, A.SANS, 600), 53, 75, still=1)
appear(a, a.pill(PX0 + 24, 488, "Relé A abre", A.OK, A.OKBG, 17, 40), 58, 75, still=1)

# tiempo 4: SIP INFO por la señalización, el portero no lo escucha
for i, d in enumerate(digits):
    t0 = 77 + i * 4.5
    token(a, [(MX1, YS), (PX0 - 6, YS)], t0, t0 + 5, chip(a, "INFO " + d, bg=A.AMB), hold=t0 + 5.4)
appear(a, mark(a, PX0, YS, False, 16), 82, 100, still=0)
appear(a, a.text(PX0 + 24, 372, "espera RFC 2833: no escucha el INFO", 15, A.BAD, A.MONO, 600), 82, 100, still=0)
appear(a, a.pill(PX0 + 24, 488, "atienden y no abre", A.BAD, A.BADBG, 17, 40), 90, 100, still=0)

finish(a, "6-t1.svg", "Cómo decide el portero si el código DTMF abre",
       "Animación en cuatro tiempos. A la izquierda el monitor, a la derecha el portero, unidos por dos carriles: la señalización SIP y el RTP del audio. "
       "1: con DTMF Type RFC2833, el monitor manda las teclas 7, 3 y 1 como eventos dentro del RTP, por el mismo camino que el audio, y el portero las guarda. "
       "2: con los 3 dígitos que fija el DTMF Mode, el portero compara 731 con el código del Relay A: coinciden. "
       "3: la lista blanca, Only Contacts List, confirma que quien llama está en contactos y el portero dispara el relé A. "
       "4: si el monitor pasa a SIP INFO, las teclas viajan por la señalización; el portero espera RFC 2833, no las escucha y la puerta no abre aunque la llamada ande.",
       [12, 37, 62, 92])
