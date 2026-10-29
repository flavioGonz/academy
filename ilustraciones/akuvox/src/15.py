import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/akuvox/src")
from _cat import *

# ---------------------------------------------------------------- 15.svg: el monitor abre un portero que no llamó
c = Canvas("Akuvox", "¿Cómo abre el monitor un portero que no llamó?")
c.add(Zone(48, 140, 300, 330, "en llamada"))
c.add(portero(123, 175, "pantalla", 0.85, "Portero hall", "192.168.88.21"))
c.add(Zone(852, 140, 300, 330, "sin llamada"))
c.add(portero(927, 175, "pantalla", 0.85, "Portero portón", "192.168.88.22", hl=CYAN))
c.add(monitor(470, 190, 260, 170, "Monitor", "192.168.88.31", hl=CYAN, screen_txt="monitoreo · portón", keys=[("Hall", False), ("Portón", True)]))
c.add(arrow((470, 250), (252, 250), "logical", "llamada SIP + DTMF", label_dy=-14))
c.add(arrow((730, 250), (925, 250), "flow", "HTTP", label_dy=-14))
c.add(text(48, 520, "Lo que manda la tecla Portón (usuario propio del monitor):", 16, 600, INK2, FB))
s, _ = code_parts(48, 536, [("monitor-porton:•••••@", "#9FC3E3"), ("192.168.88.22", "#7FD6F2"), ("/fcgi/OpenDoor?action=OpenDoor&", "#D9E9F8"), ("DoorNum=1", "#F2C94C")], size=16)
c.add(s)
c.add(f'<g>{check(64, 618, False)}</g>' + text(88, 624, "DTMF: solo llega al portero que está en la llamada.", 16, 500, INK2, FB))
c.add(f'<g>{check(64, 652, True)}</g>' + text(88, 658, "HTTP: llega a cualquier portero por su IP, con o sin llamada.", 16, 500, INK2, FB))
save(c, "15.svg")

# ---------------------------------------------------------------- 15-paso2: Remote Relay By HTTP or HTTPS
c = Canvas("Akuvox · Pasos 1 a 3", "Apuntá el monitor al portero del portón")
w = c.add(Window(48, 130, 660, 320, "Monitor · web", path="Phone > Relay > Remote Relay By HTTP or HTTPS",
                 rows=[("IP / número SIP", "192.168.88.22"), ("Formato", "/fcgi/OpenDoor (nuevo)"), ("Usuario", "monitor-porton"),
                       ("Clave", "Ejemplo-Mon-2026"), ("DoorNum", "1")], hl=0))
c.add(Step(48 + 660, 130, 2))
c.add(f'<rect x="568" y="470" width="140" height="44" rx="10" fill="{BLUE}"/>' + text(638, 498, "+Add", 17, 700, WHITE, FM, anchor="middle"))
c.add(Step(568, 470, 3))
c.add(portero(860, 140, "pantalla", 0.8, "Portero portón", "192.168.88.22", hl=CYAN))
c.add(Step(860, 140, 1))
c.add(panel(800, 418, 352, 110, None, "soft"))
c.add(text(820, 450, "En el portón (lección 14):", 16, 600, INK, FB))
c.add(text(820, 476, "Open Relay via HTTP", 15, 600, BLUE, FM))
c.add(text(820, 502, "monitor-porton / Ejemplo-Mon-2026", 15, 500, INK2, FM))
c.add(arrow((710, 220), (850, 220), "flow", "HTTP", label_dy=-12))
c.add(Note(48, 540, 660, "El formato lo decide el portero: si su firmware tiene alta seguridad (tercer bloque 10 o más) y el modo está encendido, solo acepta /fcgi/OpenDoor.", title="Formato nuevo o viejo", kind="info", size=15))
c.add(Note(800, 550, 352, "DoorNum=1 es el relé A del portón; 2 sería el relé B.", kind="ok", size=15))
save(c, "15-paso2.svg")

# ---------------------------------------------------------------- 15-paso4: las tres pantallas con tecla
c = Canvas("Akuvox · Pasos 4 a 6", "La tecla Portón puede ir en tres pantallas")
cols = [("Monitoreo", "Softkey In Monitor Page", True, 4, "sin llamada: el cliente mira y abre"),
        ("En llamada", "Softkey in Talking Page", True, 6, "hablando con el hall"),
        ("Vista previa", "Softkey In Call-Preview Page", False, None, "antes de atender")]
for i, (t, menu, on, n, why) in enumerate(cols):
    x = 48 + i * 376
    c.add(monitor(x + 25, 140, 300, 190, None, None, hl=CYAN if on else None, screen_txt=t.lower(), keys=[("Portón", True)]))
    c.add(text(x + 175, 362, t, 19, 600, INK, FB, anchor="middle"))
    c.add(text(x + 175, 388, menu, 15, 500, BLUE, FM, anchor="middle"))
    c.add(text(x + 175, 412, why, 15, 400, INK3, FB, anchor="middle"))
    if n:
        c.add(Step(x + 25, 140, n))
    else:
        c.add(pill(x + 175, 448, "opcional", INK3, WHITE, 15, False))
c.add(text(48, 488, "En cada pantalla, la misma tecla:", 16, 600, INK2, FB))
c.add(Table(48, 500, ["Campo", "Valor"], [["Enabled", "sí"], ["Type", "Remote Relay By HTTP or HTTPS"], ["Label", "Portón"]], [200, 420], mono_cols=(1,), row_h=36))
c.add(Note(720, 500, 432, "Monitoreo y vista previa piden que el monitor ya vea el video del portón: confirmalo antes de probar la tecla (paso 5).", kind="warn", size=15))
save(c, "15-paso4.svg")
