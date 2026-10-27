#!/usr/bin/env python3
"""Lección 13 · teoría: dónde queda la clave con el formato viejo y cómo viaja con el formato nuevo."""
from _anim_akuvox import Anim, A, token, chip, node, appear, finish

a = Anim(T=24, kicker="AKUVOX · URL QUE ABRE", title="Clave en la URL o clave en el encabezado")
a.steps([
    "Formato viejo: la clave va como parámetro, adentro de la URL.",
    "Esa URL queda escrita en el historial, en logs de proxies y del equipo.",
    "Formato nuevo: el cliente saca usuario:clave y los manda en el encabezado.",
    "El portero valida y dispara el relé: algunos firmwares responden 0 o -1.",
], still=3)

# barra de URL
a.add(a.box(48, 176, 1104, 54, A.INK, None, rx=12))
old1 = "http://192.168.88.21/fcgi/do?action=OpenDoor&UserName=abre-lab"
old2 = "&Password=Ejemplo-Http-2026"
appear(a, a.text(66, 210, old1, 15, A.WHITE, A.MONO) + a.text(66 + len(old1) * 9.03, 210, old2, 15, "#FF8A73", A.MONO, 600)
       + a.text(66 + (len(old1) + len(old2)) * 9.03, 210, "&DoorNum=1", 15, A.WHITE, A.MONO), 0, 50, still=0)
new1 = "http://"
new2 = "abre-lab:Ejemplo-Http-2026@"
new3 = "192.168.88.21/fcgi/OpenDoor?action=OpenDoor&DoorNum=1"
appear(a, a.text(66, 210, new1, 15, A.WHITE, A.MONO) + a.text(66 + len(new1) * 9.03, 210, new2, 15, "#FFD28A", A.MONO, 600)
       + a.text(66 + (len(new1) + len(new2)) * 9.03, 210, new3, 15, A.WHITE, A.MONO), 50, 100, still=1)
appear(a, a.pill(1140, 242, "formato viejo · /fcgi/do", A.BAD, A.BADBG, 14, 28, "end"), 0, 50, still=0)
appear(a, a.pill(1140, 242, "formato nuevo · /fcgi/OpenDoor", A.OK, A.OKBG, 14, 28, "end"), 50, 100, still=1)

# equipos
Y = 290
a.add(node(a, 48, Y, 250, 96, "Cliente", "navegador o curl"))
a.add(node(a, 475, Y, 250, 96, "Proxy", "si hay uno en el medio"))
a.add(node(a, 902, Y, 250, 96, "Portero", "192.168.88.21"))
a.add(f'<line x1="298" y1="{Y + 48}" x2="475" y2="{Y + 48}" stroke="{A.BLUE}" stroke-width="3"/>')
a.add(f'<line x1="725" y1="{Y + 48}" x2="902" y2="{Y + 48}" stroke="{A.BLUE}" stroke-width="3"/>')

LOGS = [(48, "historial"), (475, "log del proxy"), (902, "log del portero")]
for x, t in LOGS:
    a.add(a.box(x, 436, 250, 116, A.WHITE, A.LINE, rx=12))
    a.add(a.text(x + 16, 462, t, 15, A.GREY, A.MONO, 600))
for i, (x, t) in enumerate(LOGS):
    appear(a, a.text(x + 16, 492, "/fcgi/do?…&UserName=", 14, A.TXT, A.MONO) + a.text(x + 16, 514, "abre-lab&Password=", 14, A.BAD, A.MONO, 600)
           + a.text(x + 16, 536, "Ejemplo-Http-2026&…", 14, A.BAD, A.MONO, 600), 27 + i * 4, 50, still=0)
    if i == 0:
        continue
    appear(a, a.text(x + 16, 492, "/fcgi/OpenDoor?action=", 14, A.TXT, A.MONO) + a.text(x + 16, 514, "OpenDoor&DoorNum=1", 14, A.TXT, A.MONO)
           + a.text(x + 16, 536, "sin la clave", 14, A.OK, A.MONO, 600), 62 + i * 3, 100, still=1)

# viaje del pedido
token(a, [(298, Y + 48), (902, Y + 48)], 5, 16, chip(a, "GET /fcgi/do?…Password=…", bg=A.BAD, size=13, h=26), hold=16.5)
token(a, [(298, Y + 48), (902, Y + 48)], 53, 63, chip(a, "GET + encabezado de autenticación", bg=A.BLUE, size=13, h=26), hold=63.5)
token(a, [(902, Y + 70), (298, Y + 70)], 77, 85, chip(a, "0", bg=A.OK, size=15, h=26), hold=85.5)
appear(a, a.pill(1027, Y + 104, "dispara el relé", A.OK, A.OKBG, 14, 28, "middle") , 77, 100, still=1)
appear(a, a.text(48, Y + 122, "respuesta: 0 = abrió · -1 = falló la credencial", 15, A.INK, A.SANS, 600), 85, 100, still=1)

a.add(a.text(48, 592, "Con la alta seguridad encendida, Akuvox ya no acepta /fcgi/do: solo /fcgi/OpenDoor.", 16, A.INK, A.SANS, 600))
a.add(a.text(48, 620, "curl -u 'abre-lab:Ejemplo-Http-2026' manda lo mismo que usuario:clave@ en la URL.", 15, A.TXT, A.SANS))

finish(a, "13-t1.svg", "Clave en la URL o clave en el encabezado",
       "Animación en cuatro tiempos con una barra de URL arriba, el cliente, un proxy si lo hay y el portero 192.168.88.21, y debajo de cada uno su registro. "
       "1: con el formato viejo la URL es http://192.168.88.21/fcgi/do?action=OpenDoor&UserName=abre-lab&Password=Ejemplo-Http-2026&DoorNum=1 y la clave viaja como parámetro. "
       "2: esa URL completa, con la clave, queda escrita en el historial del cliente, en el log del proxy y en el log del portero. "
       "3: con el formato nuevo, http://abre-lab:Ejemplo-Http-2026@192.168.88.21/fcgi/OpenDoor?action=OpenDoor&DoorNum=1, el cliente saca usuario y clave de la URL y los manda en el encabezado de autenticación; en los registros del proxy y del portero queda la ruta sin la clave. "
       "4: el portero valida la credencial y dispara el relé; algunos firmwares responden 0 si abrió y -1 si falló la credencial. "
       "Nota: con la alta seguridad encendida Akuvox ya no acepta /fcgi/do; curl -u manda lo mismo que usuario:clave@ en la URL.",
       [12, 45, 68, 92])
