#!/usr/bin/env python3
"""Lección 10 · Teoría · Que llegue, y que llegue completo.
Sale de teoria_md (Cómo funciona) y de la tarjeta: el servidor tiene que reconocer la cámara por su MAC o su IP (si no,
la detección entra sin cámara y no pinta ningún canal); la foto la pide a la cámara con su propia clave por el puerto 80;
la grabación necesita el vínculo con el NVR y el canal; con relojes corridos el clip del NVR no coincide con el evento."""
from _anim_omni import new, out, when, travel, seq, box, check

a = new(26, "DIAGNÓSTICO", "Que llegue, y que llegue completo")
a.steps([
    "Llega el evento con la IP y la MAC: el servidor encuentra la cámara en Dispositivos.",
    "Si la cámara no está con esa IP o MAC, la detección entra sin cámara.",
    "Foto: el servidor la pide por el puerto 80 con la clave propia de la cámara.",
    "Grabación: con NVR y canal pide el clip; con el reloj corrido, no coincide.",
], still=2)

a.add(box(48, 186, 300, 84, "Cámara", "192.0.2.31", "camera"))
a.add(a.text(64, 292, "MAC 00:00:5E:00:53:31", 15, a.GREY, a.MONO))
a.add(box(48, 440, 300, 84, "NVR", "canal D5", "server"))

# servidor
SX, SY, SW = 420, 182, 380
a.add(a.box(SX, SY, SW, 390, a.WHITE, a.LINE, rx=16))
a.add(a.text(SX + 20, SY + 32, "Servidor OmniAccess", 18, a.INK, a.SANS, 600))
a.add(a.text(SX + 20, SY + 64, "Dispositivos", 15, a.GREY, a.MONO, 600))
a.add(a.box(SX + 16, SY + 76, SW - 32, 64, a.SLATE, rx=10))
a.add(a.text(SX + 32, SY + 102, "Perímetro Norte 12", 16, a.INK, a.SANS, 600))
a.add(a.group(a.text(SX + 32, SY + 126, "192.0.2.31 · …:53:31", 15, a.TXT, a.MONO), a.keyframes([(0, 1), (25, 1), (26, 0), (49, 0), (50, 1), (100, 1)]), still=1))
a.add(a.group(a.text(SX + 32, SY + 126, "192.0.2.99 · sin MAC", 15, a.BAD, a.MONO, 600), a.keyframes([(0, 0), (25, 0), (26, 1), (49, 1), (50, 0), (100, 0)]), still=0))

# monitor
MX, MW = 852, 300
a.add(a.box(MX, SY, MW, 166, a.INK, rx=14))
a.add(a.text(MX + 20, SY + 32, "Monitor Intrusión", 17, a.WHITE, a.SANS, 600))
when(a, a.box(MX + 16, SY + 54, MW - 32, 40, a.BAD, rx=8) + a.text(MX + 32, SY + 80, "Perímetro Norte 12", 16, a.WHITE, a.SANS, 600), 8, 25, still=1)
when(a, a.box(MX + 16, SY + 54, MW - 32, 40, a.BAD, rx=8) + a.text(MX + 32, SY + 80, "Perímetro Norte 12", 16, a.WHITE, a.SANS, 600), 50, 100, still=1)
when(a, a.text(MX + 20, SY + 82, "ningún canal en rojo", 16, "#FFD28A", a.SANS, 600)
     + a.text(MX + 20, SY + 108, "detección sin cámara", 15, "#9FC3E3", a.MONO), 30, 49, still=0)
# ficha: foto y clip
a.add(a.box(MX, SY + 186, MW, 204, a.WHITE, a.LINE, rx=14))
a.add(a.text(MX + 20, SY + 216, "Ficha de la detección", 17, a.INK, a.SANS, 600))
a.add(a.text(MX + 20, SY + 250, "foto", 15, a.GREY, a.MONO) + a.text(MX + 20, SY + 330, "clip", 15, a.GREY, a.MONO))
when(a, check(a, MX + 120, SY + 245) + a.text(MX + 146, SY + 251, "foto propia", 16, a.OK, a.SANS, 600), 58, 64, still=1)
when(a, check(a, MX + 120, SY + 245) + a.text(MX + 146, SY + 251, "foto propia", 16, a.OK, a.SANS, 600), 76, 100, still=0)
when(a, check(a, MX + 120, SY + 245, False) + a.text(MX + 146, SY + 251, "sin foto propia", 16, a.BAD, a.SANS, 600), 66, 75, still=0)
when(a, a.text(MX + 20, SY + 282, "clave equivocada: la cámara rechaza", 15, a.BAD, a.SANS), 66, 75, still=0)
when(a, check(a, MX + 120, SY + 325, False) + a.text(MX + 146, SY + 331, "otro momento", 16, a.BAD, a.SANS, 600)
     + a.text(MX + 20, SY + 362, "reloj del NVR corrido 2 min", 15, a.BAD, a.SANS), 88, 100, still=0)

# 1: evento
seq(a, f"M356 214 C390 214 390 {SY + 108} {SX - 8} {SY + 108}", 1, 100, a.BLUE, still=1)
when(a, a.pill(356, 238, "evento · IP y MAC", a.BLUE, a.WHITE, 15, 28), 1, 25, still=0)
travel(a, (360, 214), (SX - 20, SY + 108), 1, 6, dot=8)
seq(a, f"M{SX + SW + 6} {SY + 74} H{MX - 8}", 6, 25, a.BAD, still=0)
when(a, check(a, SX + SW - 40, SY + 108), 6, 25, still=0)
when(a, check(a, SX + SW - 40, SY + 108), 50, 100, still=1)
# 2: no la encuentra
when(a, check(a, SX + SW - 40, SY + 108, False), 27, 49, still=0)
when(a, a.text(SX + 20, SY + 172, "no coincide con lo que trae el evento", 15, a.BAD, a.SANS, 600), 27, 49, still=0)

# 3: foto
seq(a, f"M{SX - 8} {SY + 200} C390 {SY + 200} 390 262 356 262", 51, 75, a.CYAN, still=1)
when(a, a.text(SX + 20, SY + 206, "pide la foto · puerto 80", 15, a.BLUE, a.MONO, 600)
     + a.text(SX + 20, SY + 230, "usuario y clave de la cámara", 15, a.BLUE, a.MONO, 600), 51, 75, still=1)
travel(a, (370, 262), (SX - 20, SY + 200), 56, 61, label="foto", bg=a.CYAN, hold=1)
seq(a, f"M{SX + SW + 6} {SY + 250} H{MX - 8}", 58, 75, a.CYAN, still=1)
when(a, a.pill(SX + 20, SY + 246, "con la clave del NVR: no", a.BAD, a.BADBG, 15, 28), 66, 75, still=0)

# 4: grabación y reloj
seq(a, f"M{SX - 8} {SY + 300} C390 {SY + 300} 390 470 356 470", 76, 100, a.AMB, still=0)
when(a, a.text(SX + 20, SY + 306, "clip de las 02:11:40 · NVR, D5", 15, a.AMB, a.MONO, 600), 76, 100, still=0)
when(a, a.text(SX + 20, SY + 340, "hora del servidor", 15, a.INK, a.MONO, 600) + a.text(SX + 220, SY + 340, "02:11:40", 15, a.INK, a.MONO, 600)
     + a.text(SX + 20, SY + 364, "hora del NVR", 15, a.BAD, a.MONO, 600) + a.text(SX + 220, SY + 364, "02:13:40", 15, a.BAD, a.MONO, 600), 82, 100, still=0)
seq(a, f"M{SX + SW + 6} {SY + 330} H{MX - 8}", 86, 100, a.AMB, still=0)

a.add(a.text(48, 618, "Para que llegue completo: foto con la clave propia, grabación con NVR y canal, y relojes en hora.", 16, a.TXT, a.SANS, 600))
a.add(a.text(48, 644, "Y antes que nada, la cámara dada de alta con la IP o la MAC que manda en el evento.", 16, a.TXT, a.SANS, 600))

out(a, 10, 1, "Que llegue, y que llegue completo",
    "Animación en cuatro tiempos. A la izquierda, la cámara 192.0.2.31 con MAC 00:00:5E:00:53:31 y el NVR con el canal D5; en el centro, el servidor OmniAccess con la lista de Dispositivos; "
    "a la derecha, el Monitor Intrusión y la ficha de la detección con foto y clip. "
    "Tiempo 1: llega el evento con la IP y la MAC; el servidor encuentra Perímetro Norte 12 en Dispositivos y el canal se pinta de rojo. "
    "Tiempo 2: si en Dispositivos la cámara figura con otra IP (192.0.2.99) y sin MAC, no coincide: la detección entra sin cámara y no hay ningún canal en rojo. "
    "Tiempo 3: el servidor pide la foto a la cámara por el puerto 80 con el usuario y la clave de la cámara y la ficha muestra la foto propia; con la clave del NVR la cámara rechaza y no hay foto propia. "
    "Tiempo 4: el servidor pide al NVR el clip de las 02:11:40 en el canal D5; el reloj del NVR está corrido 2 minutos (02:13:40) y el clip muestra otro momento. "
    "Al pie: para que llegue completo hacen falta la foto con la clave propia, la grabación con NVR y canal y los relojes en hora; y antes que nada, la cámara dada de alta con la IP o la MAC que manda en el evento.",
    [12, 38, 60, 70, 94])
