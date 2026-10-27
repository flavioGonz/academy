#!/usr/bin/env python3
"""Lección 9 · Teoría · Un episodio de alerta, de punta a punta.
Sale de teoria_md (Cómo funciona): cuando un cambio de aforo cumple una alerta, OmniAccess avisa a los navegadores,
manda despachos, Telegram con foto y push; en el panel aparece el recuadro "Alerta de aforo" (Excede umbral, aforo contra
el límite, acción requerida), que se puede silenciar o descartar y vuelve a aparecer si la fila baja y vuelve a subir;
mientras sigue sobre el umbral un reloj cuenta y, al pasar el tiempo de escalamiento (5 minutos por defecto), sale una
sola vez el aviso de escalamiento por Telegram."""
from _anim_omni import new, out, when

a = new(26, "ATENDER LA ALERTA", "Un episodio de alerta, de punta a punta")
a.steps([
    "El aforo llega al umbral: aparece el recuadro y salen los avisos.",
    "El operador descarta el recuadro; la fila sigue arriba.",
    "Pasan 5 minutos sobre el umbral: sale una vez el escalamiento.",
    "El aforo baja del umbral: el episodio se cierra.",
    "La fila vuelve a subir: el recuadro aparece otra vez.",
], still=2)

# ---- gráfico
CX0, CX1, CY0 = 110, 676, 456
MMAX = 16
PXM = (CX1 - CX0) / MMAX
UY = 21


def X(m):
    return CX0 + m * PXM


def Y(v):
    return CY0 - v * UY


a.add(a.box(48, 182, 676, 318, a.WHITE, a.LINE, rx=14))
a.add(a.text(68, 210, "Fila Caja 1 · aforo", 15, a.GREY, a.MONO, 600))
for v in (0, 4, 8):
    a.add(a.text(CX0 - 12, Y(v) + 5, str(v), 15, a.GREY, a.MONO, 600, "end"))
for m in range(0, MMAX + 1, 4):
    a.add(a.text(X(m), CY0 + 30, f"{m} min", 15, a.GREY, a.MONO, 600, "middle"))
a.add(f'<line x1="{CX0}" y1="{CY0}" x2="{CX1}" y2="{CY0}" stroke="{a.LINE}" stroke-width="2"/>')
a.add(f'<line x1="{CX0}" y1="{Y(8)}" x2="{CX1}" y2="{Y(8)}" stroke="{a.BAD}" stroke-width="2.5" stroke-dasharray="8 6"/>')
a.add(a.text(CX1 - 4, Y(8) + 24, "umbral 8", 15, a.BAD, a.MONO, 600, "end"))

SERIE = [(0, 6), (1.5, 7), (2, 9), (10, 6), (13, 9), (16, 9)]
pts = []
for i, (m, v) in enumerate(SERIE):
    if i:
        pts.append((X(m), Y(SERIE[i - 1][1])))
    pts.append((X(m), Y(v)))
d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts)
# tramo sobre el umbral: minutos 2 a 10; escalamiento a los 7
when(a, f'<path d="M{X(2):.0f} {Y(9) - 14} v-8 H{X(7):.0f} v8" fill="none" stroke="{a.AMB}" stroke-width="2.5"/>'
     + a.text((X(2) + X(7)) / 2, Y(9) - 30, "5 min sobre el umbral", 15, a.AMB, a.MONO, 600, "middle"), 44, 100, still=1)
# revelado progresivo de la curva
reveal = a.keyframes([(0, 0), (1, 0.02), (20, 2.6 / MMAX), (40, 4.5 / MMAX), (60, 7.3 / MMAX), (80, 10.5 / MMAX), (96, 1), (100, 1)], "transform", "scaleX({})")
a.n += 1
c = f"c{a.n}"
a.css.append(f".{c}{{transform-box:view-box;transform-origin:{CX0}px 0;transform:scaleX({7.3 / MMAX:.3f});animation:{reveal} {a.T}s linear infinite}}")
a.add(f'<defs><clipPath id="rev9"><rect class="{c}" x="{CX0}" y="190" width="{CX1 - CX0 + 10}" height="300"/></clipPath></defs>')
a.add(f'<g clip-path="url(#rev9)"><path d="{d}" fill="none" stroke="{a.BLUE}" stroke-width="4" stroke-linejoin="round"/></g>')

# marcas en el gráfico
def mark(m, v, lab, col, t0, still=0, dy=-14, anchor="middle"):
    when(a, f'<circle cx="{X(m):.0f}" cy="{Y(v):.0f}" r="8" fill="{col}"/>' + a.text(X(m), Y(v) + dy, lab, 15, col, a.MONO, 600, anchor), t0, 100, still=still)


mark(2, 9, "", a.BAD, 8, still=1)
mark(4.3, 9, "", a.GREY, 36, still=1)
mark(7, 9, "", a.AMB, 57, still=1)
mark(10, 6, "", a.OK, 76, still=0)
mark(13, 9, "", a.BAD, 92, still=0)

# ---- panel del operador
PX0, PY0, PW = 752, 182, 400
a.add(a.box(PX0, PY0, PW, 318, a.INK, rx=14))
a.add(a.text(PX0 + 20, PY0 + 32, "Panel · Filas", 17, a.WHITE, a.SANS, 600))
rec = (a.box(PX0 + 120, PY0 + 140, 260, 160, "#2A1414", a.BAD, rx=12, sw=2.5)
       + a.text(PX0 + 136, PY0 + 168, "Alerta de aforo", 17, "#FFB4A6", a.SANS, 600)
       + a.box(PX0 + 136, PY0 + 180, 228, 56, "#1B3A57", rx=6) + a.text(PX0 + 250, PY0 + 214, "video en vivo", 15, "#9FC3E3", a.MONO, 600, "middle")
       + a.text(PX0 + 136, PY0 + 260, "Excede umbral · 9 / 8", 15, a.WHITE, a.MONO, 600)
       + a.text(PX0 + 136, PY0 + 284, "Acción requerida", 15, "#FFB4A6", a.SANS, 600))
when(a, rec, 8, 36, still=0)
when(a, rec, 92, 100, still=0)
when(a, a.text(PX0 + 20, PY0 + 70, "recuadro descartado", 16, "#9FC3E3", a.SANS, 600)
     + a.text(PX0 + 20, PY0 + 96, "la fila sigue en 9", 15, "#9FC3E3", a.MONO), 37, 75, still=1)
when(a, a.text(PX0 + 20, PY0 + 70, "episodio cerrado", 16, "#8EF0C0", a.SANS, 600), 77, 91, still=0)

# ---- registro de avisos
LY = 522
a.add(a.text(48, LY + 6, "Avisos", 16, a.INK, a.SANS, 600))
EV = [(8, "alerta: navegadores, despachos, Telegram, push", a.WHITE, a.BAD, 120, LY - 14, 1),
      (57, "escalamiento por Telegram · una sola vez", a.INK, a.AMBBG, 120, LY + 24, 1),
      (76, "baja del umbral: se cierra el episodio", a.OK, a.OKBG, 600, LY + 24, 0),
      (92, "sube de nuevo: recuadro otra vez", a.WHITE, a.BAD, 600, LY - 14, 0)]
for t0, lab, fg, bg, x, y, st in EV:
    when(a, a.pill(x, y, lab, fg, bg, 15, 30), t0, 100, still=st)

a.add(a.text(48, 640, "Silenciar o descartar no cambia la fila: primero mirá la imagen y después decidí.", 16, a.TXT, a.SANS, 600))

out(a, 9, 1, "Un episodio de alerta",
    "Animación en cinco tiempos. A la izquierda, el aforo de la Fila Caja 1 durante 16 minutos con el umbral de 8 como línea roja punteada; a la derecha, el panel de Filas del operador; abajo, los avisos. "
    "Tiempo 1: a los 2 minutos el aforo llega a 9, por encima del umbral; aparece el recuadro Alerta de aforo con video en vivo, Excede umbral 9 / 8 y Acción requerida, y salen los avisos a navegadores, despachos, Telegram y push. "
    "Tiempo 2: el operador descarta el recuadro; la fila sigue en 9. "
    "Tiempo 3: a los 7 minutos se cumplen 5 minutos sobre el umbral y sale una sola vez el escalamiento por Telegram. "
    "Tiempo 4: a los 10 minutos el aforo baja a 6, debajo del umbral, y el episodio se cierra. "
    "Tiempo 5: a los 13 minutos la fila vuelve a 9 y el recuadro aparece otra vez. "
    "Al pie: silenciar o descartar no cambia la fila; primero se mira la imagen y después se decide.",
    [12, 32, 52, 72, 96])
