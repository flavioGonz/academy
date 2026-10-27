import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-lpr/src")
from _lpr import *

# ---------------------------------------------------------------- 2.svg: dos cerebros deciden la barrera
c = Canvas(K(), "¿Quién sube la barrera: la cámara o el servidor?")
c.add(panel(48, 130, 420, 400, "Cerebro 1 · la cámara", "info", sub="lista cargada desde OmniAccess"))
c.add(cam_icon(90, 240, 1.3))
c.add(plate(330, 214, "SBA 1234", w=170, size=24))
c.add(text(330, 290, "está en su lista blanca", 16, 500, OK, FB, anchor="middle"))
c.add(wire([(130, 268), (130, 360), (267, 360), (267, 420)], kind="relay", arrow=False))
c.add(text(140, 340, "relé", 16, 600, CYAN, FM))
c.add(barrier(250, 490, up=True))
c.add(text(330, 452, "semáforo verde", 16, 600, OK, FB))
c.add(text(330, 476, "y barrera arriba", 16, 500, INK2, FB))
c.add(text(68, 512, "Lista negra: pasa a la lista de bloqueo.", 15, 400, INK3, FB))

c.add(panel(500, 130, 652, 400, "Cerebro 2 · el servidor", "info", sub="decide en este orden"))
rows = [
    ("1", "¿La cámara informó su lista?", "sí: manda la cámara", "blue"),
    ("2", "¿La matrícula está en el padrón?", "sí: Autorizado (Modo LPR en Lista Blanca)", "ok"),
    ("3", "Ninguna de las dos", "Denegado", "warn"),
]
for i, (n, q, a, kd) in enumerate(rows):
    y = 214 + i * 92
    c.add(Step(540, y + 10, n))
    c.add(text(572, y + 16, q, 18, 600, INK, FB))
    c.add(tag(572, y + 56, a, kd, size=15))
c.add(text(520, 506, "Antirrebote: 5 s por matrícula, 20 s por cámara.", 15, 500, INK2, FM))

for i, (lbl, kd, what) in enumerate([("Autorizado", "ok", "pasa solo"), ("Denegado", "warn", "se verifica"), ("Lista negra", "alert", "protocolo")]):
    x = 48 + i * 372
    c.add(tag(x, 590, lbl, kd, size=17))
    c.add(text(x + 150, 590, what, 17, 500, INK2, FB))
save(c, "2.svg")

# ---------------------------------------------------------------- 2-paso2: la prueba con curl y lo que responde
c = Canvas(K(2), "Mandá la misma lectura tres veces y leé la respuesta")
t = c.add(Terminal(48, 130, 700, [
    "$ curl ... <licensePlate>SBA1234</licensePlate>",
    ('{"status":"processed","decision":"DENY"}', "#FFB4A6"),
    "$ curl ...   (enseguida, mismo comando)",
    ('{"message":"Debounced","plate":"SBA1234"}', "#FFE08A"),
    "   ... Registrar desde el monitor, esperar 25 s ...",
    "$ curl ...",
    ('{"status":"processed","decision":"GRANT"}', "#7EE2B8"),
], title="PC DE LA RED DE PRUEBA → 192.0.2.10:10000"))
# línea de tiempo
y0 = 470
c.add(f'<path d="M80 {y0}H1120" stroke="{INK3}" stroke-width="2"/>')
for x, lbl, kd, sub in [(110, "0 s", "warn", "DENY"), (230, "2 s", "gray", "Debounced"), (640, "alta", "blue", "Registrar"), (980, "27 s", "ok", "GRANT")]:
    c.add(f'<circle cx="{x}" cy="{y0}" r="8" fill="{INK}"/>')
    c.add(text(x, y0 - 18, lbl, 15, 600, INK, FM, anchor="middle"))
    c.add(tag(x, y0 + 46, sub, kd, size=15, anchor="middle"))
c.add(f'<rect x="110" y="{y0 - 6}" width="300" height="12" rx="6" fill="{AMBER}" opacity=".45"/>')
c.add(text(260, y0 + 90, "ventana de 5 s", 15, 500, WARN, FM, anchor="middle"))
c.add(Note(790, 130, 362, "Solo en una instalación de prueba: cada envío crea un evento real que se ve en el monitor y en el historial.", title="Cuidado", kind="warn", size=16))
c.add(Note(790, 300, 362, "La lectura sin chapa (NO_LEIDA) nunca se descarta: dos lecturas sin chapa pueden ser dos autos.", kind="info", size=15))
save(c, "2-paso2.svg")
