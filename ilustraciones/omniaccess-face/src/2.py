import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-face/src")
from _face import *

FLOOR = 610
M = 200  # píxeles por metro


def y_of(m):
    return FLOOR - m * M


def person(x, h_m, col, dashed=False, label=None):
    """Silueta de perfil mirando a la derecha, de h_m metros, pies en x."""
    top = y_of(h_m)
    hr = 0.11 * M
    dash = ' stroke-dasharray="7 6"' if dashed else ""
    fill = "none" if dashed else col
    out = [f'<circle cx="{x + 34:.1f}" cy="{top + hr:.1f}" r="{hr:.1f}" fill="{fill}" stroke="{col}" stroke-width="3"{dash}/>',
           f'<path d="M{x + 6:.1f} {top + 2*hr + 8:.1f}h56l6 {(h_m*M) - 2*hr - 8:.1f}h-68z" fill="{fill}" stroke="{col}" stroke-width="3"{dash} opacity="{1 if dashed else .9}"/>']
    if label:
        out.append(text(x + 34, top - 10, label, 15, 600, col, FM, anchor="middle"))
    return "".join(out)


# ---------------------------------------------------------------- 2.svg: vista de costado
c = Canvas("OmniAccess Face · Lección 2", "La cámara ve de frente a 50 cm, sin luz detrás")
W = 600
c.add(f'<path d="M48 {FLOOR}H{W + 22}" stroke="{INK3}" stroke-width="3"/>')
c.add(f'<rect x="{W}" y="140" width="22" height="{FLOOR-140}" fill="#E3EAF1" stroke="{LINE2}"/>')
cam_y = y_of(1.40)
c.add(f'<rect x="{W - 24}" y="{cam_y - 50:.1f}" width="24" height="110" rx="6" fill="#26323F"/>')
c.add(f'<circle cx="{W - 24}" cy="{cam_y:.1f}" r="6" fill="{CYAN}"/>')
c.add(text(W - 40, cam_y - 62, "Terminal", 16, 600, INK, FB, anchor="end"))
c.add(f'<path d="M{W + 50} {FLOOR}V{cam_y:.1f}" stroke="{BLUE}" stroke-width="2" marker-end="url(#a-blue)" marker-start="url(#a-blue)"/>')
c.add(text(W + 62, (FLOOR + cam_y) / 2 + 6, "1,30 a 1,48 m", 16, 600, BLUE, FM))
c.add(text(W + 62, (FLOOR + cam_y) / 2 + 28, "hasta la cámara", 15, 400, INK3, FB))
px = W - 24 - 0.5 * M - 70
c.add(person(px, 1.90, INK3, dashed=True))
c.add(person(px, 1.55, BLUE))
c.add(text(px - 12, y_of(1.90) + 26, "1,90 m", 15, 600, INK3, FM, anchor="end"))
c.add(text(px - 12, y_of(1.55) + 26, "1,55 m", 15, 600, BLUE, FM, anchor="end"))
c.add(f'<path d="M{px + 70:.1f} {FLOOR + 22}H{W - 24}" stroke="{INK3}" stroke-width="2" marker-end="url(#a-gray)" marker-start="url(#a-gray)"/>')
c.add(text((px + 70 + W - 24) / 2, FLOOR + 48, "≈ 0,5 m", 15, 600, INK2, FM, anchor="middle"))
for m_ in (1.75, 1.42):
    c.add(f'<path d="M{px + 50:.1f} {y_of(m_):.1f}L{W - 24} {cam_y:.1f}" stroke="{CYAN}" stroke-width="2" stroke-dasharray="5 5"/>')
import math
c.add(f'<rect x="70" y="250" width="150" height="230" rx="6" fill="#FFF6D6" stroke="{WARN}" stroke-width="2.5"/>')
c.add(f'<circle cx="145" cy="330" r="34" fill="#F7C948" stroke="{WARN}" stroke-width="2"/>')
for i in range(8):
    a = i * math.pi / 4
    c.add(f'<path d="M{145 + 44*math.cos(a):.1f} {330 + 44*math.sin(a):.1f}L{145 + 58*math.cos(a):.1f} {330 + 58*math.sin(a):.1f}" stroke="{WARN}" stroke-width="3" stroke-linecap="round"/>')
c.add(text(145, 510, "ventana o vidrio", 15, 600, WARN, FB, anchor="middle"))
c.add(text(145, 530, "detrás de la persona", 15, 600, WARN, FB, anchor="middle"))
c.add(Note(812, 140, 348, "Contraluz: la cara queda en sombra y el terminal no la encuentra. Mové el equipo, usá WDR o sumá luz de frente.", title="Lo que más falla", kind="alert", size=16))
c.add(Note(812, 350, 348, "ClockRite 1,1 m · Control iD 1,30 m · Synerion cámara a 1,48 m · Hikvision: personas de 1,4 a 1,9 m a 0,5 m. Manda la ficha del modelo.", title="Las fuentes no coinciden en el número", kind="info", size=15))
save(c, "2.svg")

# ---------------------------------------------------------------- 2-paso3: la prueba con dos personas y tres distancias
c = Canvas("OmniAccess Face · Lección 2 · Paso 3", "Probá con la más baja, la más alta y tres distancias")
c.add(Table(48, 140, ["Prueba", "30 cm", "50 cm", "1 m"],
            [["Persona más baja", "¿reconoce?", "¿reconoce?", "¿reconoce?"],
             ["Persona más alta", "¿reconoce?", "¿reconoce?", "¿reconoce?"],
             ["Con sol de la tarde", "¿reconoce?", "¿reconoce?", "¿reconoce?"]], [260, 170, 170, 170], hl_row=None, row_h=46))
c.add(Step(820, 140, 3))
c.add(Note(48, 360, 520, "Anotá desde qué distancia dispara. Si la más alta tiene que agacharse, el equipo está bajo; si la más baja tiene que estirarse, está alto.", title="Qué mirar", kind="info", size=16))
c.add(Note(600, 360, 552, "Si solo falla a cierta hora, es la luz. Corregí la luz antes de tocar el umbral del terminal.", title="Regla", kind="ok", size=16))
c.add(f'<g>{face_thumb(880, 150, 80, ok=True)}{face_thumb(990, 150, 80, ok=False, bad="dark")}</g>')
c.add(text(920, 262, "de frente", 15, 600, OK, FB, anchor="middle"))
c.add(text(1030, 262, "a contraluz", 15, 600, ALERT, FB, anchor="middle"))
save(c, "2-paso3.svg")

# ---------------------------------------------------------------- 2-paso4: planta del hall, mal y bien
c = Canvas("OmniAccess Face · Lección 2 · Paso 4", "Mirá qué queda detrás de la persona")
for i, (ox, ok) in enumerate([(48, False), (620, True)]):
    c.add(card(ox, 130, 532, 400, "Así no: puerta de vidrio detrás" if not ok else "Así sí: luz de frente, pared detrás", fill=WHITE))
    # planta: puerta vidriada en la pared inferior
    c.add(f'<rect x="{ox + 40}" y="180" width="452" height="300" rx="8" fill="{GROUND}" stroke="{LINE2}" stroke-width="2"/>')
    c.add(f'<rect x="{ox + 196}" y="472" width="140" height="16" fill="#BFE3F5" stroke="{BLUE}"/>')
    c.add(text(ox + 266, 512, "puerta de vidrio · calle", 15, 500, INK3, FB, anchor="middle"))
    if not ok:
        tx, ty, pxp, pyp = ox + 266, 214, ox + 266, 300
        c.add(f'<rect x="{tx - 30}" y="{ty - 8}" width="60" height="16" rx="4" fill="#26323F"/>')
        c.add(f'<circle cx="{pxp}" cy="{pyp}" r="22" fill="{BLUE}"/>')
        c.add(f'<path d="M{pxp} {pyp + 30}L{pxp} 466" stroke="{WARN}" stroke-width="3" stroke-dasharray="6 5"/>')
        c.add(text(pxp + 14, 400, "sol de la tarde", 15, 600, WARN, FB))
        c.add(Mark(ox + 470, 160, False))
    else:
        tx, ty, pxp, pyp = ox + 56, 330, ox + 150, 330
        c.add(f'<rect x="{tx - 8}" y="{ty - 30}" width="16" height="60" rx="4" fill="#26323F"/>')
        c.add(f'<circle cx="{pxp}" cy="{pyp}" r="22" fill="{BLUE}"/>')
        c.add(f'<path d="M{pxp + 30} {pyp}H{ox + 470}" stroke="{OK}" stroke-width="2" stroke-dasharray="4 6"/>')
        c.add(text(ox + 330, pyp - 14, "detrás: pared, sin vidrio", 15, 600, OK, FB, anchor="middle"))
        c.add(f'<circle cx="{ox + 96}" cy="244" r="12" fill="#F7C948" stroke="{WARN}"/>')
        c.add(text(ox + 116, 250, "luz de frente", 15, 600, OK, FB))
        c.add(Mark(ox + 470, 160, True))
    c.add(text(tx, ty + 32 if not ok else ty + 56, "terminal", 15, 600, INK, FB, anchor="middle"))
c.add(Step(48, 560, 4))
c.add(Note(84, 548, 1068, "Si queda vidrio o ventana detrás de la persona, marcá la obra como \"contraluz\" y resolvelo antes de enrolar a nadie.", kind="warn", size=16))
save(c, "2-paso4.svg")
