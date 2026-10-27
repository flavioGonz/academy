import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/bosch-incendio/src")
from _bi import *


def battery(x, y, w=110, h=60, label="12 V", sub=None):
    return (rect(x, y, w, h, WHITE, INK2, rx=8, sw=2.5) + rect(x + 16, y - 9, 18, 9, INK2, INK2, rx=2, sw=0) + rect(x + w - 34, y - 9, 18, 9, RED, RED, rx=2, sw=0)
            + mid(x + w / 2, y + h / 2 + 7, label, 18, 700, INK, FM) + (mid(x + w / 2, y + h + 22, sub, 14, 500, INK3, FM) if sub else ""))


def rail(x, y, mods, zone, col):
    out = [rect(x - 14, y - 40, 14 + len(mods) * 150 + 10, 196, "none", col, rx=18, sw=2.5, dash="8 6"),
           text(x, y - 14, zone, 15, 600, col, FM)]
    out.append(rect(x, y, len(mods) * 150 - 10, 12, "#C9D6E3", "#C9D6E3", rx=6, sw=0))
    for i, (m, kd) in enumerate(mods):
        mx = x + i * 150
        c_ = {"bcm": WARN, "hi": CYAN, "lsn": BLUE}[kd]
        out.append(rect(mx, y + 18, 140, 92, WHITE, c_, rx=10, sw=2.5))
        out.append(mid(mx + 70, y + 58, m, 15, 600, INK, FM))
        out.append(mid(mx + 70, y + 84, {"bcm": "baterías", "hi": "alto consumo", "lsn": "lazo"}[kd], 14, 500, c_))
    return "".join(out)


# ---------------------------------------------------------------- 8.svg: zonas de energía
c = Canvas(K(), "Zonas de energía: si cae una, la otra sigue")
c.add(rail(70, 170, [("FPE-8000-BCM", "bcm"), ("ENO 0000 B", "hi"), ("NZM 0002 A", "hi"), ("LSN 1500 A", "lsn")], "ZONA DE ENERGÍA 1", OK))
c.add(rail(70, 400, [("FPE-8000-BCM", "bcm"), ("LSN 1500 A", "lsn"), ("LSN 1500 A", "lsn")], "ZONA DE ENERGÍA 2", CYAN))
c.add(text(56, 600, "Cada FPE-8000-BCM tiene sus baterías: si falla uno, o sus baterías,", 16, 500, INK2))
c.add(text(56, 626, "las otras zonas siguen funcionando.", 16, 500, INK2))
c.add(rect(560, 360, 34, 30, ALERT_BG, ALERT, rx=6, sw=1.5))
c.add(f'<path d="M566 366l22 18M588 366l-22 18" stroke="{ALERT}" stroke-width="3"/>')
c.add(text(604, 382, "cable rojo entre rieles quitado: zonas separadas", 15, 600, ALERT))
c.add(box(760, 130, 392, 190, "Orden en el riel", ["Al lado del BCM, primero los de alto", "consumo o sensibles a la tensión:", "ENO 0000 B, CZM 0004 A, NZM 0002 A,", "RML 0008 A, IOS 0020 A, RMH 0002 A"], size=15))
c.add(box(760, 440, 392, 180, "Obra nueva desde el 02/05/2026", ["FPE-8000-BCM, sin mezclar con BCM-0000-B", "firmware 4.7.0 o más · RPS 5.14.17 o más", "SSD 3.6 o más para planificar"], kind="warn", size=15))
save(c, "8.svg")

# ---------------------------------------------------------------- 8-paso1: dos variantes de cálculo
c = Canvas(K(1), "Dos variantes: misma fórmula, distinta exigencia")
s, h = codebox(48, 130, 1104, ["Variante A (guía NFPA 72): (0,6 x 24 + 2,5 x 5/60)  x 1,20 = 17,5 Ah",
                               "Variante B (más exigente): (0,6 x 30 + 2,5 x 15/60) x 1,25 = 23,3 Ah"], size=17, lh=34, title="DATOS: I REPOSO 0,6 A · I ALARMA 2,5 A")
c.add(s)
X0, k = 300, 30
for i, (lab, rep, al, tot, col) in enumerate([("A", 0.6 * 24 * 1.2, 2.5 * 5 / 60 * 1.2, 17.5, BLUE), ("B", 0.6 * 30 * 1.25, 2.5 * 15 / 60 * 1.25, 23.3, WARN)]):
    y = 290 + i * 100
    c.add(text(X0 - 20, y + 38, f"Variante {lab}", 18, 600, INK, FD, anchor="end"))
    c.add(rect(X0, y + 10, rep * k, 44, col, col, rx=8, sw=0, op=.85))
    c.add(rect(X0 + rep * k, y + 10, max(al * k, 6), 44, ALERT, ALERT, rx=4, sw=0))
    c.add(text(X0 + 14, y + 39, "reposo con factor", 15, 600, WHITE))
    c.add(text(X0 + (rep + al) * k + 14, y + 40, f"{tot:.1f} Ah".replace(".", ","), 20, 700, col, FM))
c.add(f'<rect x="{X0}" y="500" width="16" height="16" fill="{ALERT}"/>')
c.add(text(X0 + 26, 514, "alarma: chica en Ah, pero es la que tiene que funcionar al final", 15, 500, INK2))
c.add(Note(48, 548, 1104, "Redondeá hacia arriba a una capacidad comercial y anotá cuál variante pide el proyecto firmado. Al montar las baterías, rotulalas con su fecha de fabricación.", title="Después de la cuenta", kind="info"))
save(c, "8-paso1.svg")

# ---------------------------------------------------------------- 8-paso3: medir y probar por separado
c = Canvas(K(3), "Medí cada batería y probá red y batería por separado")
c.add(battery(80, 180, 150, 80, "B1 12 V")); c.add(battery(290, 180, 150, 80, "B2 12 V"))
c.add(f'<path d="M230 220H290" stroke="{INK2}" stroke-width="3"/>')
c.add(mid(260, 310, "en serie: 24 a 28,2 V", 16, 600, INK2, FM))
c.add(rect(80, 340, 360, 76, OK_BG, OK, rx=14, sw=2))
c.add(mid(260, 374, "cada una: 12,0 a 14,1 V", 19, 700, OK, FM))
c.add(mid(260, 400, "rango de la puesta en marcha", 15, 400, INK2))
c.add(panel(520, 140, 632, 140, "Prueba 1: falta de red", "info"))
c.add(text(544, 210, "Cortás la alimentación de red: el panel sigue con baterías", 16, 400, INK2))
c.add(text(544, 240, "y tiene que avisar la falla de red.", 16, 400, INK2))
c.add(panel(520, 300, 632, 160, "Prueba 2: falta de batería", "warn"))
c.add(text(544, 370, "Con red presente, desconectás las baterías.", 16, 400, INK2))
c.add(text(544, 400, "El aviso de batería puede demorar hasta 15 minutos:", 16, 600, WARN))
c.add(text(544, 428, "esperá antes de dar la prueba por fallida.", 16, 400, INK2))
c.add(Note(48, 490, 1104, "Medir tensión no alcanza: la práctica que cita Security Sales es probar con carga, fechar por fabricación y contar con una vida típica de 3 a 5 años.", title="Y la batería, con carga", kind="info"))
save(c, "8-paso3.svg")
