import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/windows/src")
from _win import *

# ---------------------------------------------------------------- 8.svg: no dormir y volver solo
c = Canvas(K(), "Un equipo 24/7 no duerme y vuelve solo tras un corte")
c.add(NOLIG)
c.add(panel(48, 128, 620, 400, "En Windows: powercfg", "info"))
rows = [("standby-timeout-ac 0", "suspensión: nunca", "ok"), ("hibernate-timeout-ac 0", "hibernación: nunca", "ok"),
        ("disk-timeout-ac 0", "apagar disco: nunca", "ok"), ("monitor-timeout-ac 15", "el monitor sí se apaga", "info"),
        ("/hibernate off", "sin hibernación ni inicio rápido", "ok")]
for i, (cmd, s, kd) in enumerate(rows):
    y = 178 + i * 66
    c.add(code(72, y, 300, cmd, 15))
    c.add(text(392, y + 26, s, 16, 500, OK if kd == "ok" else INK2, FB))
c.add(text(72, 510, "0 quiere decir \"nunca\".", 15, 400, INK3, FB))
c.add(panel(692, 128, 460, 400, "En el BIOS o UEFI", "info"))
c.add(text(716, 196, "Restore on AC Power Loss", 17, 600, INK, FM))
c.add(text(716, 222, "o After Power Failure", 15, 400, INK3, FM))
opts_ = [("Power On", "vuelve siempre que vuelve la luz", "ok"), ("Last State", "solo si estaba prendido", "warn"), ("Power Off", "queda apagado", "alert")]
for i, (o, s, kd) in enumerate(opts_):
    y = 256 + i * 80
    c.add(rect(716, y, 412, 64, {"ok": OK_BG, "warn": WARN_BG, "alert": ALERT_BG}[kd], {"ok": OK, "warn": WARN, "alert": ALERT}[kd], rx=12))
    c.add(text(736, y + 28, o, 17, 600, {"ok": OK, "warn": WARN, "alert": ALERT}[kd], FM))
    c.add(text(736, y + 52, s, 15, 400, INK2, FB))
c.add(Note(48, 552, 1104, "Con una UPS que apaga el equipo en orden, \"Last State\" recuerda \"apagado\" y no vuelve: con UPS conviene Power On.", title="Last State y la UPS", kind="warn"))
save(c, "8.svg")

# ---------------------------------------------------------------- 8-paso5: dónde está en el BIOS
c = Canvas(K(5), "Buscá la vuelta tras corte en el BIOS de banco")
c.add(NOLIG)
c.add(Step(65, 141, 5))
c.add(text(94, 147, "Menú genérico: el nombre y la pestaña cambian según la marca", 17, 600, INK2, FB))
c.add(rect(48, 176, 700, 400, "#0B3A66", "#0B3A66", rx=16))
tabs = ["Main", "Advanced", "Power", "Chipset", "Boot"]
for i, t in enumerate(tabs):
    x = 68 + i * 134
    hl = t == "Power"
    c.add(rect(x, 192, 120, 40, CYAN if hl else "#03213C", CYAN if hl else "#4E7396", rx=8, sw=1.5))
    c.add(mid(x + 60, 218, t, 15, 600, WHITE, FM))
items = [("(otras opciones)", "…", False), ("Restore on AC Power Loss", "[Power On]", True), ("(otras opciones)", "…", False)]
for i, (k, v, hl) in enumerate(items):
    y = 270 + i * 60
    if hl:
        c.add(rect(64, y - 8, 668, 46, "#1E5A8C", CYAN, rx=8, sw=2))
    c.add(text(84, y + 22, k, 16, 600 if hl else 500, WHITE if hl else "#9FC3E3", FM))
    c.add(text(712, y + 22, v, 16, 600, "#FFFFFF" if hl else "#9FC3E3", FM, anchor="end"))
c.add(text(84, 470, "Opciones:  Power On  ·  Last State  ·  Power Off".replace("  ", "\u00a0\u00a0"), 16, 500, "#FFFFFF", FM))
c.add(text(84, 520, "Menú dibujado, no copiado de una marca.", 15, 400, "#9FC3E3", FB))
c.add(panel(776, 176, 376, 260, "Cómo puede llamarse", "info"))
for i, s in enumerate(["Restore on AC Power Loss", "After Power Failure", "", "Según la marca, en Power,", "Advanced, Chipset o ACPI."]):
    c.add(text(800, 236 + i * 34, s, 16, 500 if i < 2 else 400, BLUE if i < 2 else INK2, FM if i < 2 else FB))
c.add(Note(776, 456, 376, "Anotá cómo se llama en esa marca y ponela en Power On.", kind="ok"))
save(c, "8-paso5.svg")

# ---------------------------------------------------------------- 8-paso6: probar el corte
c = Canvas(K(6), "Probá el corte y confirmalo en el registro")
c.add(NOLIG)
c.add(Step(65, 141, 6))
c.add(text(94, 147, "Solo en un equipo de banco", 17, 600, INK2, FB))
steps_ = [("Encendido", "funcionando", "info"), ("Corte", "unos segundos sin luz", "alert"), ("Vuelve la luz", "Power On: arranca solo", "ok"), ("Confirmá", "evento 6008", "info")]
for i, (t, s, kd) in enumerate(steps_):
    x = 48 + i * 284
    c.add(panel(x, 176, 252, 120, None, kd))
    c.add(badge(x + 32, 214, str(i + 1), {"info": CYAN, "alert": ALERT, "ok": OK}[kd]))
    c.add(text(x + 60, 221, t, 18, 600, {"info": INK, "alert": ALERT, "ok": OK}[kd], FD))
    c.add(text(x + 20, 266, s, 16, 400, INK2, FB))
    if i < 3:
        c.add(arrow((x + 256, 236), (x + 280, 236), "flow"))
sv, h = console(48, 330, 1104, [
    ">Get-WinEvent -FilterHashtable @{LogName='System'; Id=6008} -MaxEvents 3",
    ("TimeCreated            Id    Mensaje", "#7FA6C9"),
    ("(fecha y hora)         6008  el apagado anterior fue inesperado", "#9FE3F7"),
])
c.add(sv)
c.add(Note(48, 500, 1104, "El 6008 marca un apagado inesperado: corte de luz o pantallazo azul. Nunca hagas esta prueba en un servidor en producción con discos girando.", kind="warn"))
save(c, "8-paso6.svg")
