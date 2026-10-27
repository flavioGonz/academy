import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-face/src")
from _face import *

# ---------------------------------------------------------------- 6.svg: esquema del Monitor Facial
c = Canvas("OmniAccess Face · Lección 6", "Cómo se lee el Monitor Facial")
c.add(f'<rect x="48" y="126" width="1104" height="500" rx="16" fill="{WHITE}" stroke="{LINE2}" stroke-width="2"/>')
c.add(text(72, 162, "Monitor Facial", 20, 600, INK, FD))
c.add(text(72, 184, "Reconocimiento en tiempo real", 15, 400, INK3, FB))
c.add(Chip(650, 166, "LIVE", "ok"))
for xx, lab, kind in [(740, "Todos", "dark"), (822, "Permitidos", "gray"), (946, "Denegados", "gray")]:
    c.add(Chip(xx, 166, lab, kind, mono=False))
c.add(f'<path d="M48 202H1152" stroke="{LINE}" stroke-width="1.5"/>')
colx = [(72, 280, "ENTRADA"), (376, 448, "ÚLTIMO EVENTO · CAPTURAS RECIENTES"), (848, 280, "SALIDA")]
for x, w, lab in colx:
    c.add(text(x, 232, lab, 14, 600, INK3, FM, ls=1.2))
    c.add(f'<rect x="{x}" y="244" width="{w}" height="{120 if w == 280 else 180}" rx="10" fill="#0B1A28"/>')
c.add(text(212, 310, "video en vivo", 15, 500, "#9FC3E3", FB, anchor="middle"))
c.add(text(212, 332, "o foto cada 5 s", 15, 500, "#9FC3E3", FB, anchor="middle"))
c.add(text(988, 310, "\"Sin señal\" si no", 15, 500, "#9FC3E3", FB, anchor="middle"))
c.add(text(988, 332, "hay video configurado", 15, 500, "#9FC3E3", FB, anchor="middle"))
c.add(face_thumb(396, 262, 140, ok=True))
c.add(text(556, 300, "Ana Ejemplo", 22, 600, WHITE, FD))
c.add(text(556, 326, "Lote 12 · Portería peatonal", 15, 500, "#9FC3E3", FB))
c.add(Chip(556, 366, "Autorizado", "ok", mono=False))
c.add(Chip(680, 366, "Entrada", "blue", mono=False))
for j in range(3):
    c.add(face_thumb(72 + j * 92, 380, 80))
    c.add(face_thumb(848 + j * 92, 380, 80))
for j in range(5):
    c.add(face_thumb(376 + j * 90, 438, 78))
c.add(f'<rect x="378" y="440" width="74" height="74" rx="6" fill="none" stroke="{ALERT}" stroke-width="4"/>')
c.add(Note(72, 538, 500, "Borde rojo = Denegado. Tocá la foto para abrir la ficha del evento.", kind="alert", size=15))
c.add(Note(600, 538, 528, "LIVE: tu pantalla recibe eventos al instante. OFFLINE: recargá y revisá la red del puesto.", kind="info", size=15))
save(c, "6.svg")

# ---------------------------------------------------------------- 6-paso4: leer la ficha del evento
c = Canvas("OmniAccess Face · Lección 6 · Paso 4", "Abrí el Denegado y leé qué te dice la ficha")
c.add(Table(48, 140, ["La ficha muestra", "Qué significa", "Qué hace el guardia"],
            [["Nombre + Autorizado", "reconocido y vinculado a su ficha", "nada: todo bien"],
             ["Nombre + No registrado", "el terminal reconoció; OmniAccess no halló la ficha", "anotar para el técnico"],
             ["\"Desconocido\" en ámbar", "el terminal no reconoció la cara", "atender en persona"]], [280, 470, 300], row_h=52, hl_row=1))
c.add(Step(48, 140, 4))
c.add(Note(48, 380, 540, "Mirá si la foto es la captura de la puerta o la del alta: si el servidor no pudo traer la captura, muestra la de la ficha.", kind="info", size=16))
c.add(Note(612, 380, 540, "Si el guardia vio que la puerta abrió y la ficha dice No registrado, no es un intruso: es un vínculo que falta (lección 10).", kind="warn", size=16))
save(c, "6-paso4.svg")
