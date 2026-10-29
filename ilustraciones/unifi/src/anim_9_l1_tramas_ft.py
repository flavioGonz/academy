#!/usr/bin/env python3
"""Lección 9 · Laboratorio, paso 3: la caminata con llamada. Qué pasa en el aire cuando el celular cambia del AP 1 al
AP 2: sin FT, Authentication (Open System), Reassociation y el 4-way handshake (y en 802.1X un intercambio EAP
completo con RADIUS); con FT, Authentication con el algoritmo 2 y Reassociation, con las claves derivadas por
adelantado. Fuentes: theory_md de la lección (802.11r, algoritmo de autenticación número 2) y Purple (captura: FT usa
el algoritmo 2 en lugar de Open System; sin FT cada roam puede disparar un EAP completo); IEEE 802.11r e 802.11i."""
from _anim_red_unifi import *  # noqa

a = new(26, "Roaming sin magia", "Caminar con una llamada: qué tramas viajan en el roam", [
    "La llamada va por el AP 1; el celular se aleja y decide pasar al AP 2.",
    "Sin FT: Authentication Open System, Reassociation y el 4-way handshake.",
    "Con FT: Authentication con el algoritmo 2 y Reassociation. Las claves ya estaban.",
    "Menos tramas en el medio del roam: la voz sigue y el historial muestra un roam.",
], still=2, paso=3)

CL, A1, A2 = 168, 560, 1000
a.add(dev(a, 48, 180, 240, 86, "Celular", "en llamada", icon="phone"))
a.add(dev(a, 420, 180, 280, 86, "AP 1", "se aleja", ap=True))
a.add(dev(a, 860, 180, 292, 86, "AP 2", "mismo SSID", ap=True))
lifeline(a, CL, 266, 560)
lifeline(a, A1, 266, 560)
lifeline(a, A2, 266, 560)


def pair(y, label, t, end, color, still, sub=None):
    msg(a, CL, A2, y, label, t, end=end, color=color, still=still, sub=None)
    msg(a, A2, CL, y + 16, "", t + 3, end=end, color=color, still=still)
    if sub:
        during(a, a.text((CL + A2) / 2, y + 42, sub, 15, a.TXT, a.SANS, 400, "middle"), t + 3, end, still=still)


# 1 · la llamada por el AP 1
s0, s1 = ph(a, 0)
for k in range(3):
    msg(a, CL, A1, 330 + k * 36, "voz", s0 + 2 + k * 6, end=s1, color=a.CYAN, still=0, dur=2)
during(a, a.text(A1 + 24, 420, "la señal baja", 16, a.AMB, a.SANS, 600), s0 + 10, s1)

# 2 · sin FT
s0, s1 = ph(a, 1)
pair(316, "Authentication · Open System", s0 + 1, s1, a.GREY, 0)
pair(392, "Reassociation", s0 + 6, s1, a.GREY, 0)
pair(468, "4-way handshake · EAPOL ×4", s0 + 11, s1, a.GREY, 0, sub="en 802.1X, antes, un EAP completo con el RADIUS")
during(a, pill(a, 1152, 534, "8 tramas o más", "amb", anchor="end"), s0 + 16, s1)

# 3 · con FT
s0, s1 = ph(a, 2)
pair(330, "Authentication · algoritmo 2 (FT)", s0 + 1, 100, a.BLUE, 1)
pair(420, "Reassociation · con datos FT", s0 + 7, 100, a.BLUE, 1, sub="las claves para el AP 2 se derivaron por adelantado")
during(a, pill(a, 1152, 534, "4 tramas", "ok", anchor="end"), s0 + 12, 100, still=1)

# 4 · la voz sigue
s0, s1 = ph(a, 3)
for k in range(2):
    msg(a, CL, A2, 506 + k * 24, "voz" if k == 0 else "", s0 + 4 + k * 5, end=100, color=a.CYAN, still=0, dur=2.5)
during(a, a.box(48, 576, 520, 40, a.OKBG, None, rx=10) + a.text(64, 602, "Historial del cliente: AP 1 → AP 2, roam", 16, a.OK, a.SANS, 600),
       s0 + 8, 100)

status(a, 646, [
    (0, 25, "La decisión de cambiar es del celular, no del AP.", a.INK, 0),
    (25, 50, "Cada trama del roam es tiempo sin voz; con RADIUS en la nube, más.", a.AMB, 0),
    (50, 75, "En una captura, FT se reconoce por el algoritmo de autenticación 2.", a.BLUE, 1),
    (75, 100, "Si en el historial ves desconexión y reconexión, no fue un roam.", a.INK, 0),
], size=16)

write(a, 9, "l1", "Las tramas de un roam con y sin FT",
      "Animación en cuatro tiempos del paso 3 con un celular en llamada, el AP 1 del que se aleja y el AP 2 del mismo SSID. "
      "1: la voz va por el AP 1, la señal baja y el celular decide pasar al AP 2. "
      "2: sin FT, el celular y el AP 2 intercambian Authentication con Open System, Reassociation y el 4-way handshake de cuatro tramas EAPOL: ocho tramas o más, "
      "y en redes 802.1X antes hay un intercambio EAP completo con el RADIUS. "
      "3: con FT, Authentication usa el algoritmo 2 y sigue Reassociation con los datos de FT: cuatro tramas, porque las claves para el AP 2 se derivaron por adelantado; "
      "en una captura FT se reconoce por ese algoritmo de autenticación 2. "
      "4: con menos tramas en el medio la voz sigue por el AP 2 y el historial del cliente muestra AP 1 → AP 2 como roam; si muestra desconexión y reconexión, no fue un roam.",
      [12, 40, 64, 92])
