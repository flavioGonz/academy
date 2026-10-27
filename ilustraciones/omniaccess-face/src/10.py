import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-face/src")
from _face import *

# ---------------------------------------------------------------- 10.svg: las cuatro capas
c = Canvas("OmniAccess Face · Lección 10", "Diagnóstico por capas: de a una, en orden")
layers = [("1", "¿Llega el aviso?", "ícono Push azul · Configuración → Sistema → Webhooks", "URL al puerto 10000, firewall, MAC en la ficha del equipo"),
          ("2", "¿Trae foto?", "ícono Pull verde · contadores Faces y Tags · Hora / NTP", "usuario y clave de API, autenticación, red de vuelta al terminal"),
          ("3", "¿Se vincula con la ficha?", "ficha del evento: Autorizado o No registrado", "nombre idéntico; si persiste, soporte de Infratec"),
          ("4", "¿El terminal reconoce?", "\"Desconocido\" para alguien enrolado", "luz, foto de alta, y recién después el umbral del terminal")]
for i, (n, q, where, fix) in enumerate(layers):
    y = 130 + i * 112
    c.add(card(48, y, 1104, 96, stroke=BLUE if i < 3 else OK, sw=2))
    c.add(Step(84, y + 48, n))
    c.add(text(120, y + 40, q, 20, 600, INK, FD))
    c.add(text(120, y + 70, where, 15, 500, INK3, FB))
    c.add(text(700, y + 40, "Si falla:", 15, 600, ALERT, FB))
    s_, _ = wrap(700, y + 64, fix, 430, 15, 500, INK2)
    c.add(s_)
c.add(text(48, 600, "En OmniAccess: capas 1 a 3.  En el terminal: capa 4.", 17, 600, BLUE, FB))
save(c, "10.svg")

# ---------------------------------------------------------------- 10-paso3: qué dice la ficha del evento
c = Canvas("OmniAccess Face · Lección 10 · Paso 3", "La ficha del evento te dice en qué capa estás")
rows = [("Nombre correcto + Autorizado", "vinculado: todo bien", True, None),
        ("Nombre correcto + No registrado", "capa 3: el terminal reconoció; OmniAccess no halló la ficha", None, "warn"),
        ("\"Desconocido\"", "capa 4: el terminal no reconoció la cara", False, None)]
for i, (a_, b_, ok, k) in enumerate(rows):
    y = 140 + i * 96
    col = OK if ok is True else (WARN if k == "warn" else ALERT)
    c.add(card(48, y, 1104, 80, stroke=col, sw=2))
    c.add(face_thumb(64, y + 8, 64))
    c.add(text(148, y + 34, a_, 18, 600, INK, FB))
    c.add(text(148, y + 60, b_, 15, 500, INK2, FB))
    if ok is not None:
        c.add(Mark(1110, y + 40, ok))
c.add(Step(48, 140, 3))
c.add(Note(48, 440, 1104, "Con Akuvox, OmniAccess vincula buscando una credencial de rostro con el nombre que manda el terminal. En la versión revisada, las fichas creadas desde Usuarios & Residentes no la crean: con Lista Blanca el evento queda Denegado aunque la puerta abrió.", title="Por qué aparece No registrado", kind="warn", size=15))
save(c, "10-paso3.svg")

# ---------------------------------------------------------------- 10-paso4: el umbral reparte errores
c = Canvas("OmniAccess Face · Lección 10 · Paso 4", "Bajar el umbral reparte el error, no lo arregla")
x0, y0, W, H = 90, 150, 620, 360
c.add(f'<path d="M{x0} {y0}V{y0 + H}H{x0 + W}" fill="none" stroke="{INK3}" stroke-width="2"/>')
c.add(text(x0 + W / 2, y0 + H + 40, "umbral del terminal  →  más exigente", 15, 600, INK2, FB, anchor="middle"))
c.add(text(x0 - 14, y0 + 10, "errores", 15, 600, INK2, FB, anchor="end"))
c.add(f'<path d="M{x0} {y0 + 20}C{x0 + 200} {y0 + 120},{x0 + 330} {y0 + 300},{x0 + W} {y0 + H - 14}" fill="none" stroke="{ALERT}" stroke-width="4"/>')
c.add(f'<path d="M{x0} {y0 + H - 14}C{x0 + 290} {y0 + H - 40},{x0 + 420} {y0 + 240},{x0 + W} {y0 + 30}" fill="none" stroke="{BLUE}" stroke-width="4"/>')
c.add(text(x0 + 30, y0 + 30, "falsas aceptaciones (abre a un parecido)", 15, 600, ALERT, FB))
c.add(text(x0 + W - 10, y0 + 22, "falsos rechazos (no abre a quien está)", 15, 600, BLUE, FB, anchor="end"))
c.add(f'<path d="M{x0 + 330} {y0 + 30}V{y0 + H}" stroke="{OK}" stroke-width="2" stroke-dasharray="6 6"/>')
c.add(text(x0 + 336, y0 + H - 20, "punto de trabajo", 15, 600, OK, FB))
c.add(Step(x0 + W + 40, 150, 4))
c.add(Note(790, 190, 362, "Subirlo baja falsas aceptaciones y sube falsos rechazos (Hikvision, AWS, NIST). No hay un valor universal.", title="Lo que dicen las fuentes", kind="info", size=15))
c.add(Note(790, 360, 362, "Primero luz y foto de alta. Probá con varias personas distintas: NIST encontró diferencias según el grupo en la mayoría de los algoritmos.", title="Antes de tocarlo", kind="warn", size=15))
save(c, "10-paso4.svg")
