#!/usr/bin/env python3
"""Lección 3 · Teoría · Qué hace Configurar OmniAccess como alarma.
Sale de teoria_md (Cómo funciona): el servidor lee la lista de hosts de la cámara (/ISAPI/Event/notification/httpHosts);
si ya hay uno con su IP y puerto, no hace nada; si no, elige un lugar libre (IP 0.0.0.0) o el siguiente número y escribe
uno nuevo con HTTP, XML, sin autenticación, al host de eventos (puerto 10000, ruta /api/webhooks/hikvision).
Si el host de eventos no está cargado, lo dice y no escribe nada."""
from _anim_omni import new, out, when, travel, seq, box, check, card

a = new(22, "SERVIDOR DE ALARMA", "Configurar OmniAccess como alarma, por dentro")
a.steps([
    "El servidor lee la lista de hosts de la cámara.",
    "¿Ya hay uno con su IP y puerto? No: busca un lugar libre (IP 0.0.0.0).",
    "Escribe el host nuevo: HTTP, XML, sin autenticación, puerto 10000.",
    "Si lo tocás otra vez, lo encuentra en la lista y no escribe nada.",
], still=2)

a.add(box(48, 182, 300, 84, "OmniAccess", "host de eventos 192.0.2.10", "server"))
a.add(box(852, 182, 300, 84, "Cámara", "Hikvision", "camera"))
for t0, t1 in ((1, 50), (77, 100)):
    seq(a, "M356 210 H842", t0, t1, a.BLUE, "GET …/Event/notification/httpHosts", 600, 200, still=0)
    travel(a, (380, 210), (820, 210), t0, t0 + 6, dot=8)
    seq(a, "M842 246 H356", t0 + 7, t1, a.CYAN, "lista de hosts", 600, 238, still=0)

# tabla de hosts
TX, TY, TW = 48, 292, 1104
COLS = [("id", 20), ("IP", 90), ("puerto", 300), ("ruta", 420), ("formato", 760)]
a.add(a.box(TX, TY, TW, 206, a.WHITE, a.LINE, rx=12))
a.add(a.text(TX + 20, TY + 28, "httpHosts de la cámara", 15, a.GREY, a.MONO, 600))
for name, x in COLS:
    a.add(a.text(TX + x, TY + 58, name, 15, a.GREY, a.MONO, 600))
R1, R2 = TY + 72, TY + 124
a.add(a.box(TX + 12, R1, TW - 24, 46, a.SLATE, rx=8))
a.add(a.text(TX + 20, R1 + 29, "1", 16, a.INK, a.MONO, 600)
      + a.text(TX + 90, R1 + 29, "198.51.100.20", 16, a.INK, a.MONO, 600)
      + a.text(TX + 300, R1 + 29, "8080", 16, a.INK, a.MONO, 600)
      + a.text(TX + 420, R1 + 29, "(otro sistema)", 16, a.GREY, a.SANS))
a.add(a.box(TX + 12, R2, TW - 24, 46, a.SLATE, rx=8))
a.add(a.text(TX + 20, R2 + 29, "2", 16, a.INK, a.MONO, 600))
# fila 2 libre -> escrita
a.add(a.group(a.text(TX + 90, R2 + 29, "0.0.0.0", 16, a.GREY, a.MONO, 600) + a.text(TX + 300, R2 + 29, "libre", 16, a.GREY, a.SANS),
              a.keyframes([(0, 1), (50, 1), (51, 0), (99, 0), (100, 1)]), still=0))
written = (a.text(TX + 90, R2 + 29, "192.0.2.10", 16, a.BLUE, a.MONO, 600)
           + a.text(TX + 300, R2 + 29, "10000", 16, a.BLUE, a.MONO, 600)
           + a.text(TX + 420, R2 + 29, "/api/webhooks/hikvision", 16, a.BLUE, a.MONO, 600)
           + a.text(TX + 760, R2 + 29, "HTTP · XML · sin auth", 16, a.BLUE, a.MONO, 600))
when(a, written, 51, 100, still=1)

# tiempo 2: revisa filas
when(a, check(a, TX + TW - 44, R1 + 23, ok=False) + a.text(TX + TW - 70, R1 + 29, "no es OmniAccess", 15, a.BAD, a.MONO, 600, "end"), 27, 50, still=0)
when(a, f'<rect x="{TX + 8}" y="{R2 - 4}" width="{TW - 16}" height="54" rx="10" fill="none" stroke="{a.AMB}" stroke-width="3" stroke-dasharray="8 6"/>'
     + a.text(TX + TW - 30, R2 + 29, "lugar libre", 15, a.AMB, a.MONO, 600, "end"), 30, 50, still=0)
# tiempo 3: escribe
seq(a, "M356 226 H842", 51, 76, a.BLUE, "PUT: escribe el host 2", 600, 214, still=1)
travel(a, (380, 226), (820, 226), 51, 60, label="host 2", bg=a.BLUE, hold=2)
when(a, check(a, TX + TW - 44, R2 + 23), 58, 100, still=1)
a.add(a.text(TX + 20, TY + 192, "Si no hay lugar con IP 0.0.0.0, usa el siguiente número.", 15, a.GREY, a.SANS))

# tiempo 4: segunda vez
when(a, a.pill(48, 524, "segunda vez: ya está en la lista (IP y puerto) → no escribe nada", a.OK, a.OKBG, 15, 32), 77, 100, still=0)

a.add(card(a, 48, 590, 1104, ["El host de eventos es un dato del servidor, cargado al instalarlo. Si falta, el sistema lo avisa y no escribe nada."], "amb", size=16, lh=22))

out(a, 3, 1, "Configurar OmniAccess como alarma, por dentro",
    "Animación en cuatro tiempos entre el servidor OmniAccess, con su host de eventos 192.0.2.10, y una cámara Hikvision. "
    "Tiempo 1: el servidor pide la lista de hosts de la cámara con GET /ISAPI/Event/notification/httpHosts y la cámara la devuelve; "
    "la tabla tiene el host 1, de otro sistema, en 198.51.100.20 puerto 8080, y el host 2 libre, con IP 0.0.0.0. "
    "Tiempo 2: el servidor busca uno con su IP y puerto; el host 1 no es OmniAccess y el host 2 se marca como lugar libre. "
    "Tiempo 3: escribe el host 2 con 192.0.2.10, puerto 10000, ruta /api/webhooks/hikvision, HTTP, XML y sin autenticación. "
    "Tiempo 4: si se toca el botón otra vez, el servidor lo encuentra en la lista y no escribe nada. "
    "Nota: si no hay lugar con IP 0.0.0.0, usa el siguiente número; el host de eventos es un dato del servidor y, si falta, el sistema lo avisa y no escribe nada.",
    [10, 38, 62, 90])
