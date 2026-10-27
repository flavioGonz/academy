from _oai import *


def linea(x1, y1, x2, y2, col=CYAN, w=5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"{d}/>'


def flecha(x, y, dy, col=WARN):
    """Flecha vertical que indica el sentido de cruce (dy>0 hacia abajo)."""
    tip = y + dy
    s = 1 if dy > 0 else -1
    return (f'<path d="M{x} {y}V{tip - 8 * s}" stroke="{col}" stroke-width="4" stroke-linecap="round"/>'
            f'<path d="M{x - 9} {tip - 12 * s}L{x} {tip}L{x + 9} {tip - 12 * s}z" fill="{col}"/>')


# ---------- 2.svg
c = Canvas("OmniAccess Intrusión · Lección 2", "Línea, sentido y objetivo, escritos en la cámara")
c.add(frame(48, 140, 620, 380, "Perímetro Norte 12", night=True))
fy = 140 + 380 * 0.55
c.add(linea(70, fy + 30, 646, fy + 30))
c.add(text(76, fy + 58, "A", 18, 700, CYAN, FD))
c.add(text(76, fy + 8, "B", 18, 700, CYAN, FD))
c.add(text(640, fy + 58, "afuera", 14, 600, "#9FC3E3", FB, anchor="end"))
c.add(text(640, fy - 50, "adentro", 14, 600, "#9FC3E3", FB, anchor="end"))
for x in (220, 400, 560):
    c.add(flecha(x, fy + 60, -52))
c.add(f'<polygon points="440,{fy + 70} 640,{fy + 70} 640,{fy + 150} 470,{fy + 150}" fill="rgba(244,63,94,0.22)" stroke="#f43f5e" stroke-width="2.5"/>')
c.add(text(470, fy + 120, "zona", 15, 600, "#FFB4C0", FB))
c.add(person(300, fy + 120, 1.0))
c.add(tag(120, 505, "Persona", "ok", 15))
ctl = [("Línea", "2 puntos sobre el cerco"), ("Zona", "3 puntos o más"), ("Sentido", "A→B · Ambos · B→A"), ("Sensibilidad", "40 · 60 · 80"), ("Objetivo", "Persona · Vehículo · Ambos")]
c.add(panel(700, 140, 452, 300, "Calibrador de intrusión", kind="info"))
for i, (k, v) in enumerate(ctl):
    y = 200 + i * 46
    c.add(text(724, y, k, 17, 600, INK))
    c.add(text(1128, y, v, 15, 500, BLUE, FM, anchor="end"))
    if i < len(ctl) - 1:
        c.add(f'<path d="M724 {y + 16}H1128" stroke="{LINE}" stroke-width="1"/>')
c.add(Note(700, 460, 452, "Auto-perfil: sensibilidad 60, personas y vehículos, y aviso a OmniAccess. Es un punto de partida.", title="Perímetro recomendado", kind="ok", size=15))
save(c, "2.svg")

# ---------- 2-paso2.svg: dónde va la línea
c = Canvas("OmniAccess Intrusión · Lección 2 · Paso 2", "La línea corta todo el paso, lejos del borde")
for j, ok in enumerate([False, True]):
    x0 = 48 + j * 572
    c.add(frame(x0, 140, 532, 300, None, night=True))
    fy = 140 + 300 * 0.55
    # árbol
    c.add(f'<circle cx="{x0 + 400}" cy="{fy - 70}" r="42" fill="#2E5A35"/><rect x="{x0 + 394}" y="{fy - 34}" width="12" height="40" fill="#5A4632"/>')
    if not ok:
        c.add(linea(x0 + 330, fy + 12, x0 + 520, fy + 12, ALERT, 5))
        c.add(linea(x0 + 515, fy - 80, x0 + 515, fy + 100, ALERT, 5))
    else:
        c.add(linea(x0 + 30, fy + 30, x0 + 500, fy + 30, OK, 5))
    c.add(Mark(x0 + 500, 172, ok=ok))
c.add(Note(48, 460, 532, "Corta y sobre el árbol, otra pegada al borde: la cámara ve al intruso cuando ya pasó y el árbol dispara con el viento.", title="Así no", kind="alert", size=15))
c.add(Note(620, 460, 532, "De punta a punta del paso, a media altura del cuadro y lejos de árboles, postes y autos estacionados.", title="Así sí", kind="ok", size=15))
save(c, "2-paso2.svg")

# ---------- 2-paso5.svg: prueba caminando
c = Canvas("OmniAccess Intrusión · Lección 2 · Paso 5", "Cruzá en los dos sentidos: con A→B dispara uno")
for j, (txt, dy, ok) in enumerate([("Entra: de A hacia B", -70, True), ("Sale: de B hacia A", 70, False)]):
    x0 = 48 + j * 572
    c.add(frame(x0, 140, 532, 300, None, night=False))
    fy = 140 + 300 * 0.55
    c.add(linea(x0 + 30, fy + 30, x0 + 500, fy + 30, CYAN, 5))
    c.add(text(x0 + 36, fy + 56, "A", 17, 700, CYAN, FD))
    c.add(text(x0 + 36, fy + 10, "B", 17, 700, CYAN, FD))
    py = fy + 110 if dy < 0 else fy - 10
    c.add(person(x0 + 260, py, 0.9))
    c.add(flecha(x0 + 320, (fy + 70) if dy < 0 else (fy - 20), dy, WARN))
    c.add(text(x0 + 266, 470, txt, 18, 600, INK, FB, anchor="middle"))
    c.add(tag(x0 + 266, 515, "aparece en Detecciones" if ok else "no dispara", "ok" if ok else "gray", 16, anchor="middle"))
c.add(Note(48, 560, 1104, "Si las dos pasadas disparan, el sentido está en Ambos o al revés: mirá las flechas que dibuja el calibrador.", kind="info", size=16))
save(c, "2-paso5.svg")
