"""Caso de estudio · Audio en un sentido (id 21): ilustración principal y pasos 1 y 5.

Caso armado para enseñar (sin datos de clientes): troncal SIP de Antel en modo Dual (lección Troncal SIP de Antel);
se suman internos remotos con External Host y Local Network Address queda sin las redes de Antel.
La UCM le anuncia a Antel la IP pública en la c= y el audio de Antel se pierde: la oficina no oye al de afuera.
Campos del manual del UCM630x vigente (PBX Settings > SIP Settings > NAT). Datos de ejemplo.
"""
import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _gs import *


def KC(paso=None):
    return "Grandstream · Caso de estudio" + (f" · Paso {paso}" if paso else "")


# ---------------------------------------------------------------- 21.svg: la c= equivocada
c = Canvas(KC(), "El de afuera la oye, ella a él no: la c= equivocada")
c.add(Zone(36, 118, 312, 150, "red privada de Antel", CYAN))
c.add(Generic(56, 150, "Antel", "203.0.113.0/24", icon="phone", w=272))
u = c.add(UCMBox(430, 124, w=340, name="UCM6300 · Dual", sub="External Host 192.0.2.10", ports=("LAN1", "LAN2"), hl={"LAN1": CYAN}, h=140))
c.add(Generic(882, 150, "Router del cliente", "remotos e internet", icon="globe", w=270))
c.add(wire([(328, 192), (430, 192)]))
c.add(wire([(770, 192), (882, 192)]))
c.add(text(379, 180, "LAN1", 14, 600, BLUE, FM, anchor="middle"))
c.add(text(826, 180, "LAN2", 14, 600, BLUE, FM, anchor="middle"))

# los dos sentidos del audio
c.add(arrow((430, 300), (334, 300), kind="ok"))
c.add(text(600, 306, "RTP de la oficina a Antel: llega", 16, 600, OK, FB, anchor="middle"))
c.add(f'<path d="M334 344H560" stroke="{ALERT}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#a-alert)"/>')
c.add(Mark(588, 344, ok=False))
c.add(text(618, 350, "RTP de Antel a 192.0.2.10: se pierde", 16, 600, ALERT, FB))

box_svg, _ = codebox(48, 384, 520, [("INVITE de la UCM hacia Antel (SDP)", "#7FA6C9"),
                                     ("c=IN IP4 192.0.2.10      <- External Host", "#FFB4A8"),
                                     ("c=IN IP4 198.51.100.2    <- con el arreglo", "#9BE7C4")], size=16, lh=30)
c.add(box_svg)
c.add(Window(600, 384, 552, 230, "UCM · NAT", path="PBX Settings > SIP Settings > NAT",
             rows=[("External Host", "192.0.2.10"), ("Use IP address in SDP", "Sí"),
                   ("Local Network Address", "192.168.88.0/24"), ("+ las de Antel", "198.51.100.0/30 · 203.0.113.0/24")], hl=3))
c.add(Note(48, 520, 520, "El sentido que falta dice dónde mirar: si la oficina no oye, la c= que anunció la central; si no oye el de afuera, el camino por donde sale su audio.", kind="info", size=16))
save(c, "21.svg")

# ---------------------------------------------------------------- 21-paso1: el síntoma exacto
c = Canvas(KC(1), "El síntoma exacto, antes de tocar nada")
qs = [("¿Quién no oye a quién?", "La oficina al de afuera, o el de afuera a la oficina."),
      ("¿En qué llamadas?", "Troncal, internas entre sí, internos remotos."),
      ("¿Desde cuándo y qué cambió?", "Firmware, router, External Host, una VLAN nueva."),
      ("¿Desde el primer segundo?", "Si además corta a los 30 y pico: lección Audio de un lado.")]
for i, (q, a) in enumerate(qs):
    x, y = 48 + (i % 2) * 560, 124 + (i // 2) * 132
    c.add(panel(x, y, 544, 116, q, "info", title_size=19))
    svg, _ = wrap(x + 20, y + 72, a, 504, 17, 400, INK2)
    c.add(svg)
c.add(Step(48, 124, 1))
c.add(panel(48, 404, 544, 176, "La oficina no oye al de afuera", "alert", title_size=19))
lst, _ = bullet_list(68, 470, ["El audio de afuera va adonde dijo la central.", ("Mirá la c= del SDP que sale de la UCM.", "alert"), "En el caso: External Host sin las redes de Antel."], 504, size=17, gap=12)
c.add(lst)
c.add(panel(608, 404, 544, 176, "El de afuera no oye a la oficina", "warn", title_size=19))
lst, _ = bullet_list(628, 470, ["El audio de la central sale mal.", ("Mirá por qué interfaz sale y hacia qué IP.", "warn"), "En la troncal: una red de Antel sin ruta estática."], 504, size=17, gap=12)
c.add(lst)
save(c, "21-paso1.svg")

# ---------------------------------------------------------------- 21-paso5: hipótesis en orden
c = Canvas(KC(5), "Hipótesis en orden, cada una con su prueba")
rows = [["H1", "La UCM anuncia otra IP en c=", "c= del INVITE o 200 OK por LAN1"],
        ["H2", "Su audio sale por otra interfaz", "captura en LAN2: RTP hacia Antel"],
        ["H3", "Algo en el medio filtra o reescribe", "c= sale bien y llega distinto"],
        ["H4", "Codec", "Active Calls y la m= de cada lado"]]
c.add(Table(48, 124, ["", "Hipótesis", "La prueba que la separa"], rows, [80, 480, 544], row_h=56, hl_row=0, mono_cols=()))
c.add(Step(48, 124, 5))
box_svg, _ = codebox(48, 432, 560, [("Wireshark · sip || sdp", "#7FA6C9"),
                                     ("INVITE  c=IN IP4 192.0.2.10", "#FFB4A8"),
                                     ("RTP Streams: 1 flujo, 198.51.100.2 -> .1", "#D9E9F8"),
                                     ("Ctrl+R: flujo sin vuelta", "#FFB4A8")], size=16, lh=30)
c.add(box_svg)
c.add(Note(640, 432, 512, "H1 confirmada con la primera prueba: no hace falta seguir con H2. El orden ahorra tiempo porque va de lo más probable a lo menos.", kind="ok", size=17))
save(c, "21-paso5.svg")
