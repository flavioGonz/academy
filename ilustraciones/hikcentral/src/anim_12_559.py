"""Teoría de Offline de abajo arriba: la página carga por el 443, el vivo en Chrome usa el 559."""
from _anim_hc import *

caps = ["Chrome abre el Web Client por el 443: la página carga.",
        "Pide el vivo al gateway por el 559: el firewall lo bloquea.",
        "Con la matriz en mano, se habilita el 559, con autorización del cliente.",
        "El 559 pasa: el gateway reenvía el video y aparece el vivo."]
a = new(26, "Diagnóstico", "La página carga, pero el vivo necesita otro puerto", caps, still=3)

# navegador
a.add(a.box(48, 186, 330, 300, a.WHITE, a.LINE, rx=16))
a.add(a.box(48, 186, 330, 40, a.SLATE, rx=16))
a.add(a.text(68, 212, "Chrome · Web Client", 15, a.TXT, a.SANS, 600))
a.add(a.box(68, 244, 290, 28, a.SLATE, rx=6))
a.add(a.box(68, 286, 290, 180, a.INK, rx=8))
vis(a, a.text(213, 380, "sin video", 16, "#FFB4A3", a.MONO, 600, "middle"), 1, 2)
vis(a, a.box(68, 286, 290, 180, "#0B3A66", rx=8) + a.box(150, 330, 130, 90, "#17A8D4", rx=6, extra='fill-opacity="0.35"')
    + a.text(213, 450, "vivo CAM-01", 15, "#9FE0C0", a.MONO, 600, "middle"), 3)
vis(a, a.text(213, 263, "página cargada", 13, a.OK, a.MONO, 600, "middle"), 0, 3)

# firewall
a.add(a.box(470, 186, 150, 300, a.WHITE, a.LINE, rx=16))
a.add(a.text(545, 220, "Firewall", 17, a.INK, a.SANS, 600, "middle"))
a.add(a.pill(545, 244, "443 ok", a.OK, a.OKBG, anchor="middle"))
vis(a, a.pill(545, 290, "559 cerrado", a.BAD, a.BADBG, anchor="middle"), 0, 1, still=0)
vis(a, a.pill(545, 290, "559 ok", a.OK, a.OKBG, anchor="middle"), 2, 3)

# SYS y gateway, cámara
a.add(a.box(712, 186, 440, 150, a.INK, a.INK, rx=16))
a.add(a.text(736, 220, "SYS + Streaming Gateway", 18, a.WHITE, a.SANS, 600))
a.add(a.pill(736, 240, ":443 web", a.WHITE, a.NAVY2))
a.add(a.pill(736, 284, ":559 vivo web", a.WHITE, a.NAVY2))
a.add(card(a, 900, 400, 252, 86, "Cámara", "CAM-01"))
a.add(line(a, 1026, 400, 1026, 336, a.CYAN, 4, arrow=False))
stream(a, 1026, 400, 1026, 336, 0, 100, a.CYAN, tt=3, gap=3)

s0, s1 = ph(a, 0)
token(a, ":443", [(s0 + 2, 380, 258), (s0 + 12, 712, 258)], bg=a.OK)
s0, s1 = ph(a, 1)
token(a, ":559", [(s0 + 2, 380, 304), (s0 + 9, 458, 304), (s0 + 14, 458, 304)], bg=a.BAD)
vis(a, '<circle cx="470" cy="340" r="18" fill="#FCEAE6" stroke="#D2492F" stroke-width="2.5"/><path d="M463 333 L477 347 M477 333 L463 347" stroke="#D2492F" stroke-width="3"/>', 1)
s0, s1 = ph(a, 2)
vis(a, a.text(545, 400, "regla nueva", 15, a.OK, a.MONO, 600, "middle") + a.text(545, 424, "con permiso", 15, a.OK, a.MONO, 600, "middle"), 2)
s0, s1 = ph(a, 3)
token(a, ":559", [(s0 + 1, 380, 304), (s0 + 8, 712, 304)], bg=a.OK)
vis(a, line(a, 712, 318, 360, 380, a.CYAN, 4, arrow=False), 3)
stream(a, 712, 318, 360, 380, s0 + 8, 100, a.CYAN)

a.add(a.text(48, 556, "Communication Matrix: clientes al 80 y 443 del SYS; en los navegadores que no son Internet", 17, a.TXT))
a.add(a.text(48, 584, "Explorer, el Web Client toma el vivo por el 559 del gateway. Página arriba y video negro: mirá el 559.", 17, a.TXT))
write(a, "12-t1.svg", "El vivo en Chrome usa el 559", [10, 36, 62, 92])
