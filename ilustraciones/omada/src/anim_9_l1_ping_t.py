#!/usr/bin/env python3
"""Lección 9 · Laboratorio, paso 5: ping continuo mientras se camina de un EAP al otro.
En el salto aparece algún Tiempo de espera agotado; en Clients se ve a qué EAP quedó asociada."""
from _anim_om_red import *

a = nueva(26, "ROAMING Y MESH", "Caminá con ping -t: el salto se ve en la terminal", "l")
F = a.steps([
    "Asociada al EAP 1, la notebook hace ping -t al gateway: una respuesta por segundo.",
    "Caminás hacia el EAP 2: la señal del EAP 1 baja, pero el ping sigue respondiendo.",
    "La notebook cambia al EAP 2. En el salto, un Tiempo de espera agotado: un corte.",
    "En Clients figura en el EAP 2. Anotá los cortes; en el paso 6, lo mismo con 802.11r.",
], still=2)

# pasillo
a.add(a.box(48, 182, 1104, 170, a.WHITE, a.LINE, rx=16))
E1, E2 = (200, 250), (1000, 250)
a.add(eap(a, *E1, 26) + a.text(E1[0], E1[1] + 50, "EAP 1", 15, a.INK, a.MONO, 600, "middle"))
a.add(eap(a, *E2, 26) + a.text(E2[0], E2[1] + 50, "EAP 2", 15, a.INK, a.MONO, 600, "middle"))
a.add(a.text(600, 210, "SSID Roaming-Lab en los dos · Fast Roaming (k y v)", 15, a.GREY, a.MONO, 400, "middle"))
# notebook que camina
NB = f'<rect x="-22" y="-14" width="44" height="28" rx="4" fill="{a.INK}"/><rect x="-28" y="14" width="56" height="6" rx="3" fill="{a.INK}"/>'
path = [(0, 300, 280), (25, 300, 280), (50, 560, 280), (58, 640, 280), (75, 760, 280), (100, 760, 280)]
a.add(a.group(NB, a.move(path), a.keyframes([(0, 1), (100, 1)]), still=0))
solo_fijo(a, f'<g transform="translate(640,280)">{NB}</g>')
# línea de asociación
at(a, line(E1[0] + 26, 254, 278, 272, a.BLUE, 3, "5 5"), 0, 25)
at(a, a.text(450, 330, "asociada al EAP 1 · señal buena", 15, a.BLUE, a.SANS, 600, "middle"), 0, 25)
at(a, a.text(450, 330, "asociada al EAP 1 · la señal baja", 15, a.AMB, a.SANS, 600, "middle"), 25, 54)
at(a, a.text(820, 330, "asociada al EAP 2", 15, a.OK, a.SANS, 600, "middle"), 56, 100, still=1)
at(a, chip(a, 600, 228, "salto", a.AMB, a.AMBBG, anchor="middle", stroke=a.AMB), 52, 60, still=1)

# terminal
TX, TY, TW, TH = 48, 372, 720, 220
a.add(a.box(TX, TY, TW, TH, a.INK, rx=14))
a.add(a.text(TX + 20, TY + 30, "PS> ping -t 192.168.88.1", 15, a.WHITE, a.MONO))
OK_ = "Respuesta desde 192.168.88.1: bytes=32 tiempo=4ms"
rows = [(2, OK_, MINT), (10, OK_, MINT), (18, OK_, MINT), (28, OK_, MINT), (38, OK_, MINT),
        (54, "Tiempo de espera agotado para esta solicitud.", "#FF9C87"), (62, OK_, MINT), (70, OK_, MINT)]
# ventana de 6 líneas que se desplaza a medida que llegan respuestas
VIS = 6
times = [r[0] for r in rows] + [100]
for j in range(len(rows)):            # instante j: ya salieron las líneas 0..j
    t0, t1 = times[j], times[j + 1]
    shown = rows[max(0, j - VIS + 1): j + 1]
    body = ""
    for k, (_, txt, col) in enumerate(shown):
        body += a.text(TX + 20, TY + 60 + k * 26, txt, 15, col, a.MONO, 600 if col != MINT else 400)
    at(a, body, t0, t1, still=1 if j == 5 else 0, fade=0.3)

# Clients
CX = 800
a.add(a.box(CX, TY, 352, TH, a.WHITE, a.LINE, rx=14))
a.add(a.text(CX + 20, TY + 32, "Clients", 16, a.INK, a.SANS, 600))
a.add(a.text(CX + 20, TY + 66, "notebook-lab", 15, a.TXT, a.MONO))
at(a, chip(a, CX + 20, TY + 82, "EAP 1", a.BLUE, "#E6F0FA", stroke=a.BLUE), 0, 56)
at(a, chip(a, CX + 20, TY + 82, "EAP 2", a.OK, a.OKBG, stroke=a.OK), 56, 100, still=1)
a.add(a.text(CX + 20, TY + 150, "Cortes con k y v:", 15, a.GREY, a.SANS, 600))
at(a, a.text(CX + 170, TY + 150, "1", 17, a.BAD, a.MONO, 600), 56, 100, still=1)
a.add(a.text(CX + 20, TY + 180, "Cortes con 802.11r:", 15, a.GREY, a.SANS, 600))
at(a, a.text(CX + 186, TY + 180, "paso 6", 15, a.GREY, a.MONO), 0, 100, still=1)

status(a, 628, [
    (0, 25, "El ping al gateway es la prueba más simple: cada respuesta es la red andando.", a.INK, 0),
    (25, 50, "Quien decide cuándo cambiar es el cliente, no el EAP.", a.INK, 0),
    (50, 75, "Cada Tiempo de espera agotado es un corte durante el salto.", a.BAD, 1),
    (75, 100, "Si nunca cambia de EAP, mirá la potencia: puede quedar pegada al primero.", a.AMB, 0),
], x=48, anchor="start", size=16)

write(a, 9, "l1", "El roaming visto con un ping continuo",
      "Animación en cuatro tiempos con un pasillo con el EAP 1 y el EAP 2 (mismo SSID Roaming-Lab y Fast Roaming), una notebook que camina, la terminal con ping -t 192.168.88.1 y la vista Clients. "
      "1: asociada al EAP 1, la notebook recibe una respuesta del gateway por segundo. "
      "2: al caminar hacia el EAP 2 la señal del EAP 1 baja, pero el ping sigue respondiendo; la decisión de cambiar es del cliente. "
      "3: la notebook cambia al EAP 2 y en el salto la terminal muestra un Tiempo de espera agotado para esta solicitud: un corte. "
      "4: en Clients la notebook figura en el EAP 2; se anotan los cortes con k y v, y en el paso 6 se repite con 802.11r. Si nunca cambia de EAP, el problema suele ser la potencia.",
      [8, 36, 60, 90])
