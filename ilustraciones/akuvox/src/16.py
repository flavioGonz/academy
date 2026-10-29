import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/akuvox/src")
from _cat import *

# ---------------------------------------------------------------- 16.svg: relé en la calle o adentro
c = Canvas("Akuvox", "¿Dónde conviene que esté el relé de la cerradura?")


def side(x, title, kind):
    out = [panel(x, 128, 540, 440, title, kind)]
    out.append(f'<path d="M{x + 210} 176V548" stroke="{INK3}" stroke-width="2" stroke-dasharray="6 6"/>')
    out.append(text(x + 105, 196, "CALLE", 15, 600, INK3, FM, anchor="middle", ls=2))
    out.append(text(x + 375, 196, "ADENTRO", 15, 600, INK3, FM, anchor="middle", ls=2))
    return "".join(out)


# izquierda: relé del portero
c.add(side(48, "Relé en el portero", "alert"))
c.add(portero(100, 218, "pantalla", 0.7, "Portero", None))
c.add(Lock(330, 300, "Cerradura", "puerta", w=200))
c.add(wire([(205, 330), (290, 330), (290, 342), (330, 342)], "relay"))
c.add(text(250, 318, "relé A", 15, 600, CYAN, FM, anchor="middle"))
c.add(check(78, 488, False))
c.add(wrap(102, 494, "Si rompen el portero, la cerradura queda a su alcance.", 450, 17, 500, INK)[0])

# derecha: SR01 adentro
c.add(side(612, "SR01 adentro", "ok"))
c.add(portero(664, 218, "pantalla", 0.7, "Portero", None))
c.add(Generic(880, 220, "SR01", "relé de seguridad", "shield", w=230))
c.add(Lock(880, 370, "Cerradura", "puerta", w=230))
c.add(wire([(769, 300), (880, 262)], "data"))
c.add(pill(822, 252, "RS485", BLUE, WHITE, 15))
c.add(wire([(995, 304), (995, 370)], "relay"))
c.add(check(642, 488, True))
c.add(wrap(666, 494, "Rompen el portero y la puerta sigue cerrada: el portero solo pide.", 450, 17, 500, INK)[0])
c.add(text(48, 608, "HTTP al SR01:", 16, 600, INK2, FB))
c.add(code(170, 586, 560, "/fcgi/OpenDoor?action=OpenDoor&DoorNum=SB", 16))
c.add(text(748, 612, "SA = por 12 V · SB = por RS485", 16, 500, INK2, FM))
save(c, "16.svg")

# ---------------------------------------------------------------- 16-paso1: cableado SR01
c = Canvas("Akuvox · Paso 1", "Cableá el SR01 al portero por RS485")
c.add(Zone(48, 140, 300, 420, "calle"))
c.add(Zone(390, 140, 762, 420, "adentro"))
c.add(portero(123, 180, "pantalla", 0.9, "Portero", "192.168.88.21"))
c.add(Generic(470, 200, "SR01", "relé de seguridad", "shield", w=250))
c.add(Lock(860, 200, "Cerradura de banco", "la carga", w=250))
c.add(wire([(258, 260), (470, 242)], "data"))
c.add(pill(362, 236, "RS485", BLUE, WHITE, 15))
c.add(Step(300, 196, 1))
c.add(wire([(720, 242), (860, 242)], "relay"))
c.add(pill(790, 230, "relé", CYAN, WHITE, 15))
c.add(wire([(258, 330), (430, 330), (430, 270), (470, 270)], "power+", dash="8 6", dots=False))
c.add(text(444, 322, "otra opción: salida de 12 V", 15, 600, RED, FB))
c.add(text(444, 342, "del portero → Security Relay A", 15, 400, INK2, FB))
c.add(panel(470, 400, 640, 140, None, "soft"))
c.add(text(494, 432, "Modo de conexión → qué habilitás en el portero", 16, 600, INK, FB))
c.add(text(494, 462, "RS485", 16, 700, BLUE, FM) + text(600, 462, "→ Security Relay B  (Device > RS485 = Others)", 16, 500, INK2, FM))
c.add(text(494, 490, "12 V", 16, 700, RED, FM) + text(600, 490, "→ Security Relay A  (12V Power Output)", 16, 500, INK2, FM))
c.add(text(494, 518, "Bornes exactos: video de cableado de Akuvox.", 15, 400, INK3, FB))
c.add(Note(48, 584, 1104, "El E12 no tiene RS485: su conexión especial al SR01 es la que Akuvox no recomienda por seguridad.", kind="warn", size=16))
save(c, "16-paso1.svg")

# ---------------------------------------------------------------- 16-paso2: Security Relay B + tiempos
c = Canvas("Akuvox · Pasos 2 y 3", "Habilitá Security Relay B y elegí los tiempos")
c.add(Window(48, 130, 560, 250, "Portero · web", path="Access Control > Relay > Security Relay",
             rows=[("Security Relay B", "Enabled ✓ (RS485)"), ("Trigger Delay", "0"), ("Hold Delay", "5")], hl=0))
c.add(Step(608, 130, 2))
c.add(Window(650, 130, 502, 200, "Portero · web", path="Device > RS485",
             rows=[("Apply RS485 Setting To", "Others")], hl=0))
c.add(Step(1152, 130, 3))
c.add(f'<rect x="1012" y="270" width="120" height="40" rx="10" fill="{BLUE}"/>' + text(1072, 296, "Submit", 16, 700, WHITE, FM, anchor="middle"))
# línea de tiempo
y0 = 500
c.add(text(48, 420, "Qué hace cada tiempo (Trigger Delay 0, Hold Delay 5):", 17, 600, INK, FB))
x0, k = 90, 95  # px por segundo
c.add(f'<path d="M{x0} {y0}H{x0 + k * 10}" stroke="{INK3}" stroke-width="2" marker-end="url(#a-gray)"/>')
for t in range(0, 10):
    c.add(f'<path d="M{x0 + k * t} {y0 - 6}V{y0 + 6}" stroke="{INK3}" stroke-width="2"/>' + text(x0 + k * t, y0 + 28, f"{t} s", 15, 500, INK3, FM, anchor="middle"))
c.add(f'<rect x="{x0}" y="{y0 - 50}" width="{k * 5}" height="36" rx="8" fill="{CYAN}"/>' + text(x0 + k * 2.5, y0 - 26, "relé activado: Hold Delay 5 s", 16, 600, WHITE, FB, anchor="middle"))
c.add(f'<rect x="{x0 + k * 5}" y="{y0 - 50}" width="{k * 4.6}" height="36" rx="8" fill="{SOFT}" stroke="{LINE2}"/>' + text(x0 + k * 7.3, y0 - 26, "vuelve al reposo", 16, 500, INK2, FB, anchor="middle"))
c.add(pill(x0, y0 + 66, "orden + Trigger Delay 0 = al instante", BLUE, WHITE, 15, False, anchor="start"))
c.add(Note(640, 556, 512, "Trigger Delay 5 haría esperar 5 s antes de activar. El E18 no tiene Hold Delay.", kind="info", size=15))
save(c, "16-paso2.svg")

# ---------------------------------------------------------------- 16-paso4: qué abre cada DoorNum
c = Canvas("Akuvox · Pasos 4 y 5", "¿Qué relé dispara cada DoorNum?")
c.add(Terminal(48, 130, 1104, [("PORTERO=192.168.88.21", "#9FC3E3"),
                                 "curl -s -u 'abre-lab:Ejemplo-Http-2026' \"$PORTERO/fcgi/OpenDoor?action=OpenDoor&DoorNum=SB\""], title="PC DE LABORATORIO"))
rows = [("1", "Relé A", "en el portero", "local", None),
        ("2", "Relé B", "en el portero", "local", 5),
        ("SA", "Security Relay A", "SR01 por la salida de 12 V", "adentro", None),
        ("SB", "Security Relay B", "SR01 por RS485", "adentro", 4)]
for i, (dn, rel, where, z, n) in enumerate(rows):
    y = 270 + i * 82
    on = n is not None
    c.add(f'<rect x="48" y="{y}" width="1104" height="66" rx="14" fill="{SOFT if on else WHITE}" stroke="{CYAN if on else LINE2}" stroke-width="{2.5 if on else 1.5}"/>')
    c.add(text(80, y + 42, f"DoorNum={dn}", 19, 700, BLUE, FM))
    c.add(arrow((300, y + 34), (380, y + 34), "flow"))
    c.add(text(400, y + 42, rel, 19, 600, INK, FB))
    c.add(text(640, y + 42, where, 17, 400, INK2, FB))
    c.add(Chip(1000, y + 42, z, "ok" if z == "adentro" else "dark", mono=False))
    if n:
        c.add(Step(48, y, n))
c.add(text(48, 628, "Paso 4: SB con el SR01 por RS485.  Paso 5: sin SR01, DoorNum=2 sobre el relé B con un portón o lámpara de banco.", 16, 500, INK2, FB))
save(c, "16-paso4.svg")
