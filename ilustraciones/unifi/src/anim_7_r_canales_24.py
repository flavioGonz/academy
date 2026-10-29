#!/usr/bin/env python3
"""Lección 7 · Resumen, "Cómo se ve en la red": la banda de 2.4 GHz. Canales numerados cada 5 MHz, cada transmisión
ocupa unos 20 MHz; 1, 6 y 11 no se pisan; un AP en el mismo canal es co-canal y comparte el aire por turnos; un AP en
el canal 3 se superpone en parte con el 1 y el 6. Fuentes: theory_md e idea_md de la lección (802.11b, canales cada
5 MHz, unos 20 MHz por transmisión; en un canal transmite uno por vez). Frecuencias centrales 2412 + 5·(n-1) MHz."""
from _anim_red_unifi import *  # noqa

a = new(26, "Canales angostos", "2.4 GHz: por qué solo 1, 6 y 11", [
    "Los canales van cada 5 MHz, pero cada transmisión ocupa unos 20 MHz.",
    "1, 6 y 11 no se pisan: tres AP con tres aires distintos, hablan a la vez.",
    "Un cuarto AP en el 6 es co-canal: comparte ese aire y se turnan.",
    "Un AP del vecino en el 3 pisa en parte al 1 y al 6: se ensucian los dos.",
], still=3)

BASE, HUMP = 540, 230
f2x = lambda f: 100 + (f - 2400) * 13.33  # noqa: E731
cx = lambda n: f2x(2412 + 5 * (n - 1))  # noqa: E731
W2 = 10 * 13.33  # medio ancho de 20 MHz


def hump(n, color, fill_op=0.16, sw=3.5, dash=""):
    c = cx(n)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="M{c - W2:.1f} {BASE} C{c - W2 * 0.55:.1f} {BASE - HUMP * 1.32:.1f} {c + W2 * 0.55:.1f} {BASE - HUMP * 1.32:.1f} {c + W2:.1f} {BASE} Z" '
            f'fill="{color}" fill-opacity="{fill_op}" stroke="{color}" stroke-width="{sw}"{da}/>')


# eje
a.add(wire(90, BASE, 1110, BASE, a.INK, 2.5))
for n in range(1, 12):
    x = cx(n)
    a.add(wire(x, BASE, x, BASE + 10, a.INK, 2))
    a.add(a.text(x, BASE + 34, str(n), 16, a.INK if n in (1, 6, 11) else a.GREY, a.MONO, 600 if n in (1, 6, 11) else 400, "middle"))
a.add(a.text(1110, BASE + 34, "canal", 15, a.GREY, a.MONO, 400, "end"))
a.add(a.text(90, BASE + 62, "2.4 GHz · frecuencia central 2412 MHz en el canal 1, +5 MHz por canal", 15, a.GREY, a.SANS))

# 1 · un canal ocupa 20 MHz
s0, s1 = ph(a, 0)
vis(a, hump(1, a.BLUE), 0)
vis(a, a.arrow(f"M{cx(1)} {BASE - 250} H{cx(1) + W2 - 4}", a.BLUE, 2.5) + a.arrow(f"M{cx(1)} {BASE - 250} H{cx(1) - W2 + 4}", a.BLUE, 2.5)
    + a.text(cx(1), BASE - 262, "unos 20 MHz", 16, a.BLUE, a.MONO, 600, "middle"), 0)
vis(a, a.box(cx(1) - 2, BASE - 26, cx(2) - cx(1) + 4, 18, a.AMBBG, None, rx=4)
    + a.text((cx(1) + cx(2)) / 2, BASE - 36, "5 MHz", 15, a.AMB, a.MONO, 600, "middle"), 0)
vis(a, nbox(a, 600, 250, 552, 110, "Canal 2, 3, 4…", ["Están a 5 MHz uno del otro: cualquier par", "a menos de 5 canales de distancia se pisa."], "info"), 0)

# 2 · 1, 6 y 11
COL = {1: a.BLUE, 6: a.OK, 11: a.CYAN}
for n, lab in ((1, "AP 1"), (6, "AP 2"), (11, "AP 3")):
    vis(a, hump(n, COL[n]), 1, 3)
    vis(a, pill(a, cx(n), BASE - HUMP - 24, lab, "info" if n != 6 else "ok", anchor="middle"), 1)
    vis(a, pill(a, cx(n), BASE - HUMP - 24, lab, "info" if n != 6 else "ok", anchor="middle"), 3)
s0, s1 = ph(a, 1)
for n in (1, 6, 11):
    for k in range(3):
        t = s0 + 3 + k * 7
        during(a, hump(n, COL[n], 0.42, 0), t, t + 3.5)
during(a, a.text(600, 236, "los tres transmiten al mismo tiempo, cada uno en su aire", 17, a.OK, a.SANS, 600, "middle"), s0 + 3, s1)

# 3 · co-canal en el 6: turnos
s0, s1 = ph(a, 2)
during(a, pill(a, cx(1), BASE - HUMP - 24, "AP 1", "info", anchor="middle") + pill(a, cx(11), BASE - HUMP - 24, "AP 3", "info", anchor="middle"), s0, s1)
for k in range(4):
    t = s0 + 1 + k * 6
    who, other = ("AP 2", "AP 4") if k % 2 == 0 else ("AP 4", "AP 2")
    during(a, pill(a, cx(6) - 52, BASE - HUMP - 24, f"{who} habla", "ok", anchor="middle")
           + pill(a, cx(6) + 66, BASE - HUMP - 24, f"{other} espera", "grey", anchor="middle")
           + hump(6, a.OK, 0.42, 0), t, t + 5.6, still=0)
during(a, a.text(600, 236, "mismo canal: uno por vez, se reparten el tiempo de aire", 17, a.AMB, a.SANS, 600, "middle"), s0 + 2, s1, still=0)

# 4 · el vecino en el 3
s0, s1 = ph(a, 3)
during(a, hump(3, a.BAD, 0.22, 3.5, "9 6"), s0 + 2, 100, still=1)
during(a, pill(a, cx(3), BASE - HUMP - 64, "vecino · canal 3 · pisa al 1 y al 6", "bad", anchor="middle"), s0 + 2, 100, still=1)
# zonas pisadas
ov1 = f'<rect x="{cx(3) - W2:.1f}" y="{BASE - 70}" width="{cx(1) + W2 - (cx(3) - W2):.1f}" height="70" fill="{a.BAD}" fill-opacity=".28"/>'
ov2 = f'<rect x="{cx(6) - W2:.1f}" y="{BASE - 70}" width="{cx(3) + W2 - (cx(6) - W2):.1f}" height="70" fill="{a.BAD}" fill-opacity=".28"/>'
during(a, ov1 + ov2, s0 + 6, 100, still=1)

status(a, 640, [
    (0, 25, "Cada número es un paso de 5 MHz; cada transmisión necesita unos 20.", a.INK, 0),
    (25, 50, "Por eso en 2.4 GHz se usan solo 1, 6 y 11, y siempre en 20 MHz.", a.OK, 0),
    (50, 75, "Co-canal no es falla: es compartir. Con muchos AP, menos aire para cada uno.", a.AMB, 0),
    (75, 100, "Mirá el espectro antes de elegir: lo que usa el vecino también cuenta.", a.BAD, 1),
])

write(a, 7, "r1", "2.4 GHz: canales que se pisan y co-canal",
      "Animación en cuatro tiempos sobre la banda de 2.4 GHz con los canales 1 a 11 en un eje de frecuencia (el canal 1 en 2412 MHz y 5 MHz más por canal). "
      "1: los canales están a 5 MHz uno del otro, pero cada transmisión ocupa unos 20 MHz, así que canales cercanos se pisan. "
      "2: el AP 1 en el canal 1, el AP 2 en el 6 y el AP 3 en el 11 no se superponen: cada uno tiene su aire y los tres transmiten a la vez. "
      "3: un cuarto AP en el canal 6 es co-canal con el AP 2: comparten el mismo aire y se turnan, uno habla y el otro espera. "
      "4: un AP del vecino en el canal 3 se superpone en parte con el 1 y con el 6 y ensucia a los dos. Por eso en 2.4 GHz se usan 1, 6 y 11 en 20 MHz, y se mira el espectro antes de elegir.",
      [12, 40, 62, 90])
