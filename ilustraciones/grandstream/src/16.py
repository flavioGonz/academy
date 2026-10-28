import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _fxo import *

X0, SEC = 330, 120


def ring(x, w, y, label=None):
    """Timbre: ráfaga de alterna."""
    d = "".join(f"M{x + j * 5:.1f} {y - 18}V{y + 18}" for j in range(int(w / 5)))
    s = f'<path d="{d}" stroke="{INK3}" stroke-width="2"/>'
    if label:
        s += text(x + w / 2, y - 26, label, 15, 600, INK3, FB, anchor="middle")
    return s


def burst(x, w, y, label, color):
    return (f'<rect x="{x}" y="{y - 16}" width="{w}" height="32" rx="6" fill="{color}"/>'
            + text(x + w / 2, y + 6, label, 15, 700, WHITE, FM, anchor="middle"))


# ---------------------------------------------------------------- 16.svg: cuándo viaja el número
c = Canvas(K(), "¿Cuándo viaja el número del que llama?")
filas = [
    ("Bellcore/Telcordia", "de fábrica en la UCM", [("ring", 0.0, 1.2, "timbre 1"), ("fsk", 1.8, 1.6, "FSK"), ("ring", 4.2, 1.2, "timbre 2")]),
    ("ETSI-FSK During Ringing", "después del primer timbre", [("ring", 0.0, 1.2, "timbre 1"), ("fsk", 1.8, 1.6, "FSK"), ("ring", 4.2, 1.2, "timbre 2")]),
    ("ETSI Prior to Ringing", "con aviso: LR, DTAS o RP", [("alert", 0.0, 0.7, "aviso"), ("fsk", 1.0, 1.6, "FSK o DTMF"), ("ring", 3.2, 1.2, "timbre 1")]),
    ("ETSI-DTMF", "en tonos de teclado, antes o durante", [("dtmf", 0.0, 2.4, "2 9 0 0 …"), ("ring", 3.2, 1.2, "timbre 1")]),
]
for i, (n, sub, evs) in enumerate(filas):
    y = 190 + i * 92
    c.add(text(48, y - 4, n, 18, 600, INK, FB))
    c.add(text(48, y + 20, sub, 15, 500, INK3, FB))
    c.add(f'<path d="M{X0} {y}H{X0 + 6.6 * SEC}" stroke="{LINE2}" stroke-width="2"/>')
    for kind, t0, dur, lab in evs:
        x, w = X0 + t0 * SEC, dur * SEC
        if kind == "ring":
            c.add(ring(x, w, y, lab if i == 0 or kind == "ring" else None))
        elif kind == "fsk":
            c.add(burst(x, w, y, lab, BLUE))
        elif kind == "alert":
            c.add(burst(x, w, y, lab, WARN))
        else:
            c.add(burst(x, w, y, lab, CYAN))
c.add(Note(48, 556, 1104, "En Bellcore el número viaja entre el primer y el segundo timbre: si la central atiende antes, no llega. Qué esquema usa Antel no está publicado: se prueba.", kind="warn", size=16))
save(c, "16.svg")

# ---------------------------------------------------------------- 16-paso4: probar esquemas de a uno
c = Canvas(K(4), "Probá los esquemas de a uno y anotá el que anda")
items = [("Auto-Detect", "probalo primero"), ("Bellcore/Telcordia", "el de fábrica"), ("ETSI-FSK During Ringing", ""),
         ("ETSI-DTMF During Ringing", ""), ("ETSI-FSK Prior to Ringing with LR", "también DTAS y RP"), ("ETSI-DTMF Prior to Ringing with LR", "también DTAS y RP")]
c.add(panel(48, 132, 640, 440, "Caller ID Scheme, en este orden", "info"))
for i, (s, n) in enumerate(items):
    y = 196 + i * 60
    c.add(f'<rect x="72" y="{y - 20}" width="26" height="26" rx="6" fill="{WHITE}" stroke="{BLUE}" stroke-width="2"/>')
    c.add(text(114, y, s, 17, 600, INK, FM))
    if n:
        c.add(text(114, y + 22, n, 15, 400, INK3, FB))
c.add(Step(48, 132, 4))
c.add(panel(730, 132, 422, 180, "En cada prueba", "ok"))
lst, _ = bullet_list(750, 196, ["Llamá desde un celular.", "Dejá sonar al menos dos timbres.", "Mirá el número en CDR y en el teléfono que atiende."], 392, size=16, gap=8)
c.add(lst)
c.add(Note(730, 332, 422, "Antes, un teléfono con pantalla en el par: si no muestra el número, la línea no tiene la facilidad de Antel.", kind="warn", size=16))
c.add(Note(48, 594, 1104, "El que funciona va a la ficha de la línea, junto con la tensión y los tonos.", kind="ok", size=16))
save(c, "16-paso4.svg")

# ---------------------------------------------------------------- 16-paso6: RX y TX
c = Canvas(K(6), "RX es lo que escuchás; TX, lo que escucha el otro")
c.add(dev(48, 250, "Línea de Antel", "el que llama", icon="central", w=270, dark=True))
c.add(f'<rect x="460" y="200" width="280" height="184" rx="18" fill="{DEEP}"/>')
c.add(text(600, 244, "UCM · FXO1", 20, 600, WHITE, FD, anchor="middle"))
c.add(text(600, 270, "Antel_Linea1", 15, 500, "#9FC3E3", FM, anchor="middle"))
c.add(pill(600, 316, "RX Gain", CYAN, DEEP, size=15))
c.add(pill(600, 360, "TX Gain", WARN, DEEP, size=15))
c.add(DeskPhone(930, 222, "Interna 1001", "la que atiende", w=200))
c.add(Arrow((318, 290), (460, 290), kind="flow", label="entra: RX"))
c.add(Arrow((740, 290), (930, 290), kind="flow"))
c.add(Arrow((930, 346), (740, 346), kind="flow"))
c.add(Arrow((460, 346), (318, 346), kind="flow", label="sale: TX", label_dy=26))
c.add(Step(460, 200, 6))
c.add(text(600, 440, "De -13,5 a +12 dB, 0 de fábrica.", 17, 600, INK, FB, anchor="middle"))
c.add(Note(48, 480, 540, "Si vos escuchás bajo al que llama, subí RX de a poco. Si al otro lado te escuchan bajo, subí TX.", kind="info", size=16))
c.add(Note(612, 480, 540, "Eco, ruido o volumen raro: primero la impedancia (ACIM, Detect en Analog Hardware); recién después las ganancias.", kind="warn", size=16))
save(c, "16-paso6.svg")
