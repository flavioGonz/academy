import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/unifi/src")
from _uf import *


def seg(x, y, w, lab, kind):
    bg, fg = {"a1": (SOFT, BLUE), "a2": ("#E0F5FA", CYAN), "gap": (ALERT_BG, ALERT)}[kind]
    d = "6 5" if kind == "gap" else None
    return rect(x, y, w, 40, bg, fg, rx=8, sw=2, dash=d) + mid(x + w / 2, y + 26, lab, 15, 600, fg, FM)


# ---------------------------------------------------------------- 12.svg: los tres patrones del historial
c = Canvas(K(), "Tres patrones en el historial del cliente")
lanes = [
    ("Roam en el borde de la celda", "ok", "Está bien: así tiene que verse.", [(0, 560, "AP 1", "a1"), (560, 520, "AP 2", "a2")]),
    ("Desconexión y reconexión", "alert", "Hueco de cobertura: perdió la red.", [(0, 480, "AP 1", "a1"), (480, 120, "sin red", "gap"), (600, 480, "AP 2", "a2")]),
    ("Ping-pong entre dos AP", "warn", "Potencia pareja de más entre esos dos.", [(0, 180, "AP 1", "a1"), (180, 180, "AP 2", "a2"), (360, 180, "AP 1", "a1"), (540, 180, "AP 2", "a2"), (720, 180, "AP 1", "a1"), (900, 180, "AP 2", "a2")]),
]
for i, (t, kd, mean, segs) in enumerate(lanes):
    y = 128 + i * 142
    col = {"ok": OK, "alert": ALERT, "warn": WARN}[kd]
    c.add(text(48, y + 22, t, 20, 600, col, FD))
    c.add(text(1152, y + 22, mean, 16, 500, INK2, FB, anchor="end"))
    for x0, w, lab, k in segs:
        c.add(seg(48 + x0 * 1104 / 1080, y + 40, w * 1104 / 1080 - 6, lab, k))
c.add(text(48, 560, "tiempo →", 15, 500, INK3, FM))
c.add(Note(48, 578, 1104, "Historial de conexión y roaming del cliente (Network 10.5 en adelante). Los tres patrones son los que describe Purple.", kind="info", size=15))
save(c, "12.svg")

# ---------------------------------------------------------------- 12-paso3: Time Machine
c = Canvas(K(3), "Time Machine: ¿qué cambió en las últimas 24 horas?")
c.add(Window(48, 128, 1104, 230, "UniFi Network", path="UniFi Devices > AP > AirView > Radios > Time Machine"))
c.add(hline(90, 1110, 290, INK3, 2))
for k, lab in enumerate(["-24 h", "-18 h", "-12 h", "-6 h", "ahora"]):
    x = 90 + k * 255
    c.add(f'<path d="M{x} 284V296" stroke="{INK3}" stroke-width="2"/>')
    c.add(mid(x, 320, lab, 15, 500, INK3, FM))
evs = [(330, "cambio de canal", WARN), (640, "cambio de potencia", WARN), (900, "cambio de config.", ALERT)]
for x, lab, col in evs:
    c.add(f'<circle cx="{x}" cy="290" r="11" fill="{col}" stroke="{WHITE}" stroke-width="3"/>')
    c.add(mid(x, 262, lab, 15, 600, col))
c.add(text(90, 230, "eventos de la radio (ilustrativo)", 15, 500, INK3, FM))
c.add(Step(48, 128, 3))
qs = [("¿Hubo cambio de canal?", "Channel AI, Auto o un radar en DFS."), ("¿Cambió la potencia?", "alguien bajó o subió un nivel."), ("¿Cambió la configuración?", "un cambio de ayer suele ser la causa de hoy.")]
for i, (q, a) in enumerate(qs):
    x = 48 + i * 376
    c.add(panel(x, 384, 352, 110, None, "info"))
    c.add(text(x + 20, 424, q, 18, 600, INK, FD))
    c.add(wrap(x + 20, 454, a, 312, 15, 400, INK2)[0])
c.add(Note(48, 516, 1104, "Paso 4: Port Manager > Time Machine del puerto del AP, con el filtro de clientes que flapean. Si el uplink se cayó y volvió, el problema no es de radio.", kind="warn"))
save(c, "12-paso3.svg")

# ---------------------------------------------------------------- 12-paso5: un cambio por vez
c = Canvas(K(5), "Un cambio por vez, y si empeora, volvé atrás")
loop = [("Mirar", "historial y Time Machine", 130, 230), ("Escribir", "qué pasó, en tres líneas", 470, 230), ("Un cambio", "el único que vas a probar", 810, 230),
        ("Probar", "caminata o el mismo cliente", 810, 420), ("¿Mejoró?", "comparalo con lo anotado", 470, 420)]
for i, (a, b, x, y) in enumerate(loop):
    kd = "ok" if i == 2 else "info"
    c.add(panel(x - 20, y - 70, 300, 110, None, kd))
    c.add(text(x, y - 24, a, 22, 600, INK, FD))
    c.add(text(x, y + 8, b, 15, 400, INK2, FB))
c.add(arrow((414, 215), (446, 215)))
c.add(arrow((754, 215), (786, 215)))
c.add(wire([(940, 274), (940, 346)], kind="flow", arrow=True))
c.add(arrow((786, 405), (754, 405)))
c.add(wire([(450, 405), (300, 405), (300, 274)], kind="ok", arrow=True))
c.add(text(118, 420, "sí: el siguiente", 15, 600, OK, FB))
c.add(Step(110, 160, 5))
c.add(Note(48, 494, 540, "No: volvé lo último que tocaste. Muchas veces volver a los valores por defecto es el primer paso (LazyAdmin).", title="Si empeora", kind="alert"))
c.add(Note(612, 494, 540, "Donde se pueda tender, cable: el WiFi comparte el aire entre todos y ninguna optimización arregla todo (std.rocks).", title="Y a veces", kind="info"))
save(c, "12-paso5.svg")
