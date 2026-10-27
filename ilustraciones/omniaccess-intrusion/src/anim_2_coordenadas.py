#!/usr/bin/env python3
"""Lección 2 · Teoría · La regla es geometría: coordenadas 0 a 1000, seguimiento y zona.
Sale de teoria_md (Cómo funciona): la línea es un segmento en coordenadas de la imagen; Hikvision guarda los puntos
de 0 a 1000 con el origen abajo a la izquierda y el calibrador invierte la altura para dibujarla; la cámara sigue
cada objeto entre cuadros y, cuando pasa de un lado al otro en el sentido permitido, genera el evento; la zona es un
polígono de tres puntos o más y dispara cuando un objeto entra y permanece dentro."""
from _anim_omni import new, out, when, travel, person

a = new(24, "LA REGLA", "La línea es un segmento; el cruce, un cambio de lado")
a.steps([
    "La cámara guarda los puntos de 0 a 1000, con el origen abajo a la izquierda.",
    "El calibrador invierte la altura para dibujar la línea sobre el cuadro.",
    "La cámara sigue al objeto cuadro a cuadro: pasa de A a B y hay evento.",
    "La zona es un polígono: el evento sale si el objeto entra y permanece.",
], still=2)

# ---- panel izquierdo: escala de la cámara
SX, SY, S = 96, 214, 300          # cuadrado 0..1000 (y crece hacia arriba)
def P(x, y):
    return SX + x * S / 1000, SY + S - y * S / 1000
a.add(a.text(48, 196, "Lo que guarda la cámara", 18, a.INK, a.SANS, 600))
a.add(a.box(SX, SY, S, S, a.WHITE, a.LINE, rx=4))
a.add(a.arrow(f"M{SX} {SY + S} V{SY - 4}", a.GREY, 2) + a.arrow(f"M{SX} {SY + S} H{SX + S + 8}", a.GREY, 2))
a.add(a.text(SX - 10, SY + S + 6, "0", 15, a.GREY, a.MONO, 600, "end"))
a.add(a.text(SX - 10, SY + 12, "1000", 15, a.GREY, a.MONO, 600, "end"))
a.add(a.text(SX + S, SY + S + 26, "1000", 15, a.GREY, a.MONO, 600, "middle"))
a.add(a.text(SX + 6, SY + S + 26, "origen", 15, a.GREY, a.MONO, 600))
A1, B1 = P(250, 800), P(750, 300)
when(a, f'<line x1="{A1[0]}" y1="{A1[1]}" x2="{B1[0]}" y2="{B1[1]}" stroke="{a.CYAN}" stroke-width="5" stroke-linecap="round"/>'
     f'<circle cx="{A1[0]}" cy="{A1[1]}" r="7" fill="{a.BLUE}"/><circle cx="{B1[0]}" cy="{B1[1]}" r="7" fill="{a.BLUE}"/>'
     + a.text(A1[0] + 14, A1[1] - 10, "(250, 800)", 15, a.INK, a.MONO, 600)
     + a.text(B1[0] - 10, B1[1] + 30, "(750, 300)", 15, a.INK, a.MONO, 600, "middle"), 2, 100, still=1)

# ---- panel derecho: cuadro de la cámara
FX, FY, FW, FH = 520, 214, 632, 340
def Q(x, y):  # coordenada 0..1000 de la cámara -> punto del cuadro (altura invertida)
    return FX + x * FW / 1000, FY + (1000 - y) * FH / 1000
a.add(a.text(FX, 196, "Lo que ve el calibrador", 18, a.INK, a.SANS, 600))
a.add(a.box(FX, FY, FW, FH, "#E6EDF4", a.LINE, rx=6))
a.add(f'<path d="M{FX} {FY + 90} L{FX + FW} {FY + 70}" stroke="#C9D6E3" stroke-width="3"/>')   # horizonte
a.add(a.text(FX + FW - 12, FY + 26, "cuadro de la cámara", 15, a.GREY, a.MONO, 600, "end"))
A2, B2 = Q(250, 800), Q(750, 300)
when(a, a.arrow(f"M{SX + S + 14} {SY + 150} H{FX - 12}", a.BLUE, 3)
     + a.text((SX + S + FX) / 2, SY + 136, "invierte", 15, a.BLUE, a.MONO, 600, "middle")
     + a.text((SX + S + FX) / 2, SY + 178, "la altura", 15, a.BLUE, a.MONO, 600, "middle"), 25, 50, still=0)
when(a, f'<line x1="{A2[0]}" y1="{A2[1]}" x2="{B2[0]}" y2="{B2[1]}" stroke="{a.CYAN}" stroke-width="5" stroke-linecap="round"/>'
     f'<circle cx="{A2[0]}" cy="{A2[1]}" r="7" fill="{a.BLUE}"/><circle cx="{B2[0]}" cy="{B2[1]}" r="7" fill="{a.BLUE}"/>', 26, 100, still=1)
when(a, a.pill(FX + 16, FY + FH - 44, "y del cuadro = 1000 − y de la cámara", a.BLUE, a.WHITE, 15, 30), 26, 50, still=0)
# lados A y B
when(a, a.text(Q(700, 250)[0], Q(700, 250)[1], "A", 26, a.AMB, a.HEAD, 600, "middle")
     + a.text(Q(560, 860)[0], Q(560, 860)[1], "B", 26, a.AMB, a.HEAD, 600, "middle"), 26, 100, still=1)

# ---- tiempo 3: seguimiento cuadro a cuadro
pts = [(600, 130), (618, 225), (636, 320), (654, 415), (672, 510), (690, 605)]
for i, (x, y) in enumerate(pts):
    cx, cy = Q(x, y)
    t = 52 + i * 3
    when(a, f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="7" fill="none" stroke="{a.INK}" stroke-width="2.5" stroke-dasharray="3 3"/>', t, 75, still=1 if i < 5 else 1, fade=0.6)
cx0, cy0 = Q(*pts[0]); cx1, cy1 = Q(*pts[-1])
travel(a, (cx0, cy0), (cx1, cy1), 52, 67, inner=person(a, 0, 0, a.INK, 0.9), hold=8)
when(a, a.pill(FX + FW - 16, FY + 44, "evento: cruce de A a B", a.WHITE, a.BAD, 15, 30, "end"), 61, 75, still=1)
when(a, a.text(FX, FY + FH + 30, "Cada círculo es la posición del objeto en un cuadro. El evento sale cuando cambia de lado.", 16, a.TXT, a.SANS, 600), 51, 75, still=1)

# ---- tiempo 4: zona
zone = [Q(60, 470), Q(330, 500), Q(360, 90), Q(40, 70)]
d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in zone) + " z"
when(a, f'<path d="{d}" fill="{a.BAD}" fill-opacity=".14" stroke="{a.BAD}" stroke-width="3" stroke-dasharray="9 6"/>'
     + "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="6" fill="{a.BAD}"/>' for x, y in zone)
     + a.text(Q(200, 120)[0], Q(200, 120)[1] + 4, "zona", 16, a.BAD, a.MONO, 600, "middle"), 76, 100, still=0)
z0, z1 = Q(120, 900), Q(190, 300)
travel(a, z0, z1, 78, 84, inner=person(a, 0, 0, a.INK, 0.9), hold=16)
# permanece: barra que se llena
bar = a.box(FX + 360, FY + FH - 46, 180, 14, a.WHITE, a.LINE, rx=7)
when(a, bar + a.text(FX + 360, FY + FH - 56, "permanece dentro", 15, a.INK, a.MONO, 600), 84, 100, still=0)
fill = a.keyframes([(0, 0), (84, 0), (93, 1), (100, 1)], "transform", "scaleX({})")
a.n += 1
c = f"c{a.n}"
a.css.append(f".{c}{{transform-box:fill-box;transform-origin:left;transform:scaleX(1);animation:{fill} {a.T}s linear infinite}}")
when(a, f'<rect class="{c}" x="{FX + 360}" y="{FY + FH - 46}" width="180" height="14" rx="7" fill="{a.BAD}"/>', 84, 100, still=0)
when(a, a.pill(FX + FW - 16, FY + 44, "evento de zona", a.WHITE, a.BAD, 15, 30, "end"), 93, 100, still=0)
when(a, a.text(FX, FY + FH + 30, "La zona necesita tres puntos o más. Entrar no alcanza: el objeto tiene que quedarse.", 16, a.TXT, a.SANS, 600), 76, 100, still=0)
when(a, a.text(48, FY + FH + 30, "Hikvision: puntos de 0 a 1000.", 16, a.TXT, a.SANS, 600), 0, 50, still=0)

when(a, a.text(48, 640, "Cuánto tiene que quedarse depende de la sensibilidad (y en otras marcas, del tiempo mínimo y el tamaño).", 16, a.TXT, a.SANS, 600), 76, 100, still=0)

out(a, 2, 1, "Coordenadas, seguimiento y zona",
    "Animación en cuatro tiempos con dos paneles. A la izquierda, lo que guarda la cámara: un cuadrado con escala de 0 a 1000 y el origen abajo a la izquierda, "
    "con una línea entre los puntos (250, 800) y (750, 300). A la derecha, el cuadro de la cámara como lo ve el calibrador. "
    "Tiempo 1: la cámara guarda los puntos de 0 a 1000 con el origen abajo a la izquierda. "
    "Tiempo 2: el calibrador invierte la altura (y del cuadro igual a 1000 menos y de la cámara) y dibuja la misma línea sobre el cuadro, con el lado A abajo y el B arriba. "
    "Tiempo 3: una persona camina de A hacia B; cada círculo punteado es su posición en un cuadro; cuando pasa al otro lado de la línea aparece el evento de cruce de A a B. "
    "Tiempo 4: aparece una zona de cuatro puntos; la persona entra, una barra de permanencia se llena y recién entonces sale el evento de zona. "
    "Al pie: cuánto tiene que quedarse depende de la sensibilidad y, en otras marcas, del tiempo mínimo y el tamaño.",
    [12, 38, 70, 97])
