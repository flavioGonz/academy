import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _gs import *

# ---------------------------------------------------------------- 6.svg: una ruta, muchos DID
c = Canvas(K(), "Una sola ruta lleva cada DID a su interna")
nums = [("29001007", "1007"), ("29001012", "1012"), ("29001020", "1020")]
for i, (n_, ext) in enumerate(nums):
    y = 170 + i * 130
    c.add(Generic(48, y, n_, "llega del troncal", icon="phone", w=250))
    c.add(arrow((304, y + 42), (404, 330), kind="flow"))
    c.add(Arrow((800, 330), (896, y + 42), kind="ok"))
    c.add(Generic(904, y, "Interna " + ext, "suena acá", icon="phone", w=248, hl=OK))
c.add(f'<rect x="410" y="200" width="380" height="270" rx="18" fill="{DEEP}"/>')
c.add(text(434, 240, "Ruta entrante", 21, 600, WHITE, FD))
c.add(text(434, 266, "Inbound Routes · Proveedor_Lab", 14, 400, "#9FC3E3", FM))
for i, (k, v) in enumerate([("Pattern", "_2900XXXX"), ("Destino", "By DID"), ("Strip", "4")]):
    y = 310 + i * 48
    c.add(f'<rect x="430" y="{y - 26}" width="340" height="38" rx="8" fill="#0B3A66"/>')
    c.add(text(446, y, k, 16, 500, "#9FC3E3", FB))
    c.add(text(756, y, v, 17, 600, WHITE, FM, anchor="end"))
c.add(text(600, 520, "2900 se saca · queda 1007", 17, 600, OK, FM, anchor="middle"))
c.add(Note(48, 566, 1104, "Diez o cien números directos se mantienen con un patrón: el número que llega, menos lo que saca el Strip, es la interna que suena.", kind="ok", size=16))
save(c, "6.svg")

# ---------------------------------------------------------------- 6-paso2: DID Mode, de dónde se lee el número
c = Canvas(K(2), "DID Mode: en qué línea del INVITE está tu número")
lines = [("INVITE sip:29001007@203.0.113.10 SIP/2.0", "#7FD6F2"),
         ("Via: SIP/2.0/UDP ...", "#7FA6C9"),
         ("From: <sip:099xxxxxx@sip.proveedor.example>", "#7FA6C9"),
         ("To: <sip:21000000@sip.proveedor.example>", "#FFD18A"),
         ("...", "#7FA6C9")]
svg, h = codebox(48, 140, 700, lines, size=16, lh=34, title="INVITE QUE MANDA EL PROVEEDOR (EJEMPLO)")
c.add(svg)
c.add(arrow((760, 194), (820, 194), kind="ok"))
c.add(text(832, 186, "Request-line", 18, 600, OK, FM))
c.add(text(832, 210, "acá viene el DID 29001007", 15, 500, INK2, FB))
c.add(arrow((760, 296), (820, 296), kind="flow"))
c.add(text(832, 288, "To-header", 18, 600, WARN, FM))
c.add(text(832, 312, "acá viene la cuenta 21000000", 15, 500, INK2, FB))
c.add(Window(48, 360, 520, 150, "UCM · troncal", path="VoIP Trunks > Advanced Settings", rows=[("DID Mode", "Request-line")], hl=0))
c.add(Step(48, 360, 2))
c.add(Note(612, 360, 540, "Con DID Mode en To-header, este INVITE se leería como 21000000: no matchea _2900XXXX y la llamada no llega a la interna.", title="Leer el lugar equivocado", kind="alert", size=16))
c.add(Note(48, 540, 1104, "Request-line viene de fábrica. Cada proveedor manda el DID donde quiere: si las entrantes no matchean, es lo primero que se mira.", kind="info", size=16))
save(c, "6-paso2.svg")

# ---------------------------------------------------------------- 6-paso3: Strip para tres formatos
c = Canvas(K(3), "El Strip cuenta caracteres hasta la interna")
rows = [("29001007", 4, "Strip 4"), ("59829001007", 7, "Strip 7"), ("+59829001007", 8, "Strip 8 · el + cuenta")]
for r, (num, k, lab) in enumerate(rows):
    y = 150 + r * 130
    for i, ch in enumerate(num):
        x = 48 + i * 52
        cut = i < k
        bg, fg = (WHITE, ALERT) if cut else (OK_BG, OK)
        dash = ' stroke-dasharray="5 4"' if cut else ""
        c.add(f'<rect x="{x}" y="{y}" width="46" height="58" rx="8" fill="{bg}" stroke="{fg}" stroke-width="2"{dash}/>')
        c.add(text(x + 23, y + 39, ch, 24, 600, ALERT if cut else INK, FM, anchor="middle"))
    c.add(f'<path d="M48 {y + 74}H{48 + k * 52 - 6}" stroke="{ALERT}" stroke-width="3"/>')
    c.add(text(48, y + 100, f"se sacan {k}", 15, 600, ALERT, FM))
    c.add(Chip(760, y + 38, lab, "warn" if r == 2 else "blue", mono=True))
    c.add(arrow((1000, y + 29), (1040, y + 29), kind="ok"))
    c.add(text(1056, y + 38, "1007", 22, 700, OK, FM))
c.add(Step(48, 150, 3))
c.add(Note(48, 540, 1104, "El Strip sale del número que llega en la primera llamada de prueba (miralo en el CDR), no del que figura en la factura. Y cada formato necesita además su propio patrón.", kind="warn", size=16))
save(c, "6-paso3.svg")
