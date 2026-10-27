import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _gs import *

# ---------------------------------------------------------------- 7.svg: el árbol del IVR con horario
c = Canvas(K(), "Cada tecla con su horario, y destino para el silencio")
c.add(f'<rect x="48" y="246" width="250" height="150" rx="18" fill="{DEEP}"/>')
c.add(icon(68, 268, "bell", CYAN, 1.3))
c.add(text(108, 292, "IVR principal", 20, 600, WHITE, FD))
c.add(text(68, 330, "extensión 7000", 15, 400, "#9FC3E3", FM))
c.add(text(68, 356, "prompt de bienvenida", 15, 400, "#9FC3E3", FM))
rows = [("Tecla 1", "blue", [("Office Time", "Ring Group ventas", "info"), ("Out of Office", "Buzón 1001", "info")]),
        ("Tecla 2", "blue", [("All Time", "Interna 1002", "info")]),
        ("No marca nada", "warn", [("Response Timeout", "Ring Group recepción", "ok")]),
        ("Marca mal", "warn", [("Invalid", "Ring Group recepción", "ok")])]
for i, (k, kd, dests) in enumerate(rows):
    y = 128 + i * 104
    c.add(Cable((298, 321), (380, y + 44), kind="flow", arrow=False))
    c.add(Chip(388, y + 52, k, kd, mono=False))
    for j, (cond, dst, dk) in enumerate(dests):
        x = 580 + j * 302
        bw = 272 if j == 0 else 270
        bg, fg = KC[dk]
        c.add(f'<rect x="{x}" y="{y + 6}" width="{bw}" height="84" rx="14" fill="{bg}" stroke="{fg if dk == "ok" else LINE2}" stroke-width="2"/>')
        c.add(text(x + 18, y + 38, cond, 15, 600, INK3, FM))
        c.add(text(x + 18, y + 68, dst, 18, 600, INK, FB))
        if j == 0:
            c.add(arrow((x - 30, y + 48), (x - 2, y + 48)))
        else:
            c.add(text(x - 15, y + 54, "o", 17, 600, INK3, FB, anchor="middle"))
c.add(Note(48, 566, 540, "Hasta cinco destinos por tecla, cada uno con su horario: un solo IVR para día, noche y feriados.", kind="info", size=16))
c.add(Note(612, 566, 540, "Si Timeout o Invalid quedan sin destino, al terminar las repeticiones la central corta: el que no marca nada se queda afuera.", kind="alert", size=16))
save(c, "7.svg")

# ---------------------------------------------------------------- 7-paso4: lista blanca de internas
c = Canvas(K(4), "Marcar internas desde el IVR, solo las públicas")
c.add(Generic(48, 160, "Quien llama", "está en el IVR 7000", icon="phone", w=270))
c.add(arrow((322, 190), (520, 190), kind="ok", label="marca 1002", label_dy=-12))
c.add(arrow((322, 230), (520, 330), kind="alert", label="marca 1010", label_at=0.55, label_dy=-14))
c.add(Generic(530, 150, "Interna 1002", "recepción · en la lista", icon="user", w=340, hl=OK))
c.add(Generic(530, 300, "Interna 1010", "gerencia · fuera de la lista", icon="user", w=340, hl=ALERT))
c.add(Mark(906, 192, ok=True)); c.add(text(936, 198, "suena", 17, 600, OK, FB))
c.add(Mark(906, 342, ok=False)); c.add(text(936, 348, "no se puede marcar", 17, 600, ALERT, FB))
c.add(Window(48, 420, 560, 190, "UCM · IVR 7000", path="Basic Call Features > IVR", rows=[("Dial Other Extensions", "Sí"), ("Dial Block/Allowlist", "Allowlist: 1002")], hl=1))
c.add(Step(48, 420, 4))
c.add(Note(640, 420, 512, "Sin lista, cualquiera que conozca un número de interna llega directo: el gerente, la sala de reuniones o un equipo que no debería atender llamadas de afuera.", kind="warn", size=16))
save(c, "7-paso4.svg")

# ---------------------------------------------------------------- 7-paso5: qué pasa si no marca nada
c = Canvas(K(5), "Llamá al 7000 y no marques nada")
tl = [("Bienvenida", "suena el prompt"), ("Espera 10 s", "Response Timeout"), ("Repite", "3 veces de fábrica")]
for j, (ttl, kd, end, endk) in enumerate([("Con destino de Timeout", "ok", "Ring Group recepción", "ok"), ("Sin destino de Timeout", "alert", "la central corta", "alert")]):
    y = 150 + j * 210
    c.add(panel(48, y, 1104, 180, ttl, kd, title_size=19))
    for i, (a, b) in enumerate(tl):
        x = 72 + i * 250
        c.add(f'<rect x="{x}" y="{y + 56}" width="220" height="92" rx="12" fill="{WHITE}" stroke="{LINE2}" stroke-width="1.5"/>')
        c.add(text(x + 18, y + 94, a, 18, 600, INK, FB))
        c.add(text(x + 18, y + 124, b, 15, 500, INK3, FM))
        c.add(arrow((x + 224, y + 102), (x + 246, y + 102)))
    bg, fg = KC[endk]
    c.add(f'<rect x="822" y="{y + 56}" width="306" height="92" rx="12" fill="{bg}" stroke="{fg}" stroke-width="2"/>')
    c.add(text(842, y + 94, "Al terminar", 15, 600, INK3, FM))
    c.add(text(842, y + 126, end, 19, 600, fg, FB))
c.add(Step(48, 150, 5))
c.add(text(48, 600, "Para probar fuera de horario sin esperar a la noche, cambiá el horario de oficina y volvé a llamar.", 17, 500, INK2, FB))
save(c, "7-paso5.svg")
