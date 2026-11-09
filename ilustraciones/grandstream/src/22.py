"""Caso de estudio · Video de un lado (id 22): ilustración principal y pasos 1 y 6.

Caso armado para enseñar (sin datos de clientes): GXV3350 de un depósito detrás de un router 4G con poca subida,
recepción con un GXV3480. Recepción ve negro o congelado. Causa: 720P a 2048 kbps (de fábrica en el GXV3350)
por una subida chica; arreglo recomendado por Grandstream: VGA y 384 kbps.
Fuentes: manual del GXV3350, FAQ del GDS371x, FAQ de los GXV34x0, guía de Wave, RFC 3264 y 6184. Datos de ejemplo.
"""
import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _gs import *


def KC(paso=None):
    return "Grandstream · Caso de estudio" + (f" · Paso {paso}" if paso else "")


# ---------------------------------------------------------------- 22.svg: tres lugares
c = Canvas(KC(), "Video de un lado: tres lugares, en orden")
c.add(Generic(48, 128, "GXV3350", "depósito · 1004", icon="camera", w=230))
c.add(Generic(338, 128, "Router 4G", "subida chica", icon="wifi", w=220))
c.add(Generic(618, 128, "UCM6300", "captura acá", icon="server", w=220, dark=True))
c.add(Generic(898, 128, "GXV3480", "recepción · 1003", icon="user", w=254))
c.add(arrow((278, 170), (332, 170)))
c.add(arrow((558, 170), (612, 170), kind="alert"))
c.add(arrow((838, 170), (892, 170)))
c.add(text(585, 236, "pierde", 15, 600, ALERT, FM, anchor="middle"))
c.add(text(600, 266, "el video del depósito hacia recepción", 16, 500, INK3, FB, anchor="middle"))

cards = [("1 · ¿Se manda?", ["cámara, obturador, permiso", "video apagado o solo audio", "SDP: sendonly, recvonly, m=video 0"], "info"),
         ("2 · ¿Llega entero?", ["RTP Streams: Lost de ese flujo", "un solo sentido con pérdida", "subida, puertos, ALG"], "alert"),
         ("3 · ¿Se decodifica?", ["solo si llega entero", "profile-level-id", "packetization-mode"], "info")]
for i, (t, ls, k) in enumerate(cards):
    x = 48 + i * 372
    c.add(panel(x, 296, 352, 196, t, k, title_size=20))
    lst, _ = bullet_list(x + 20, 360, ls, 312, size=16, gap=10)
    c.add(lst)
c.add(text(48 + 372 + 20, 476, "el caso: 720P a 2048 kbps por un 4G", 15, 600, ALERT, FB))
c.add(Note(48, 516, 1104, "Antes de capturar: ¿ese equipo puede mandar video? Un portero GDS371x manda y no recibe, y muchos GRP muestran solo audio o una foto JPEG. Ahí que uno vea y el otro no es lo normal.", kind="warn", size=16))
save(c, "22.svg")

# ---------------------------------------------------------------- 22-paso1: ¿puede mandar?
c = Canvas(KC(1), "Primera pregunta: ¿ese equipo puede mandar video?")
devs = [("Portero GDS371x", "camera", ["Manda video al que atiende", ("No recibe video del otro lado", "warn"), "Que no vea a recepción es lo normal"]),
        ("Teléfono GRP o GXP", "phone", ["GRP2601 a 2604: solo audio", "GRP2614 en adelante: foto JPEG del portero", ("No es un flujo H.264", "warn")]),
        ("GXV34x0", "user", ["Obturador de privacidad: tapa el sensor", ("Se puede atender solo con audio", "warn"), "Video deshabilitado: solo audio"]),
        ("Wave en el celular", "phone", ["Pide permiso de cámara: Allow", ("Video: invitación que el otro acepta", "warn"), "Sin permiso, no hay cámara"])]
for i, (t, ic, ls) in enumerate(devs):
    x, y = 48 + (i % 2) * 560, 124 + (i // 2) * 236
    c.add(panel(x, y, 544, 220, None, "info"))
    c.add(icon(x + 20, y + 22, ic, BLUE, 1.35))
    c.add(text(x + 64, y + 46, t, 20, 600, INK, FD))
    lst, _ = bullet_list(x + 24, y + 98, ls, 500, size=17, gap=14)
    c.add(lst)
c.add(Step(48, 124, 1))
c.add(text(48, 628, "Si el equipo puede mandar y del otro lado no se ve, recién ahí la captura en la UCM.", 16, 500, INK3, FB))
save(c, "22-paso1.svg")

# ---------------------------------------------------------------- 22-paso6: lo que entra por la subida
c = Canvas(KC(6), "Lo que entra por una subida de 768 kbps")
X0, PX = 300, 820 / 2400          # escala: 0 a 2400 kbps
c.add(text(48, 160, "Subida del 4G", 17, 600, INK, FB))
c.add(f'<rect x="{X0}" y="138" width="{768 * PX:.0f}" height="34" rx="8" fill="{LINE2}"/>')
c.add(text(X0 + 768 * PX + 14, 162, "768 kbps (simulada en el banco)", 15, 500, INK3, FM))
c.add(text(48, 234, "De fábrica", 17, 600, INK, FB))
c.add(text(48, 256, "720P", 15, 500, INK3, FM))
c.add(f'<rect x="{X0}" y="212" width="{2048 * PX:.0f}" height="34" rx="8" fill="{ALERT}"/>')
c.add(f'<rect x="{X0 + 2048 * PX:.0f}" y="212" width="{90 * PX:.0f}" height="34" rx="4" fill="{BLUE}"/>')
c.add(text(X0 + 16, 235, "video 2048 kbps", 15, 600, WHITE, FM))
c.add(f'<path d="M{X0 + 768 * PX:.0f} 126V268" stroke="{INK}" stroke-width="2" stroke-dasharray="6 5"/>')
c.add(text(48, 318, "Con el arreglo", 17, 600, INK, FB))
c.add(text(48, 340, "VGA", 15, 500, INK3, FM))
c.add(f'<rect x="{X0}" y="296" width="{384 * PX:.0f}" height="34" rx="8" fill="{OK}"/>')
c.add(f'<rect x="{X0 + 384 * PX + 3:.0f}" y="296" width="{90 * PX:.0f}" height="34" rx="4" fill="{BLUE}"/>')
c.add(text(X0 + 16, 319, "384 kbps", 15, 600, WHITE, FM))
c.add(f'<path d="M{X0 + 768 * PX:.0f} 284V346" stroke="{INK}" stroke-width="2" stroke-dasharray="6 5"/>')
c.add(text(X0 + 2140 * PX - 70, 196, "audio G.711 ≈ 90 kbps", 15, 600, BLUE, FM, anchor="middle"))
c.add(Window(48, 384, 540, 196, "GXV3350 del depósito", path="Account > Codec Settings",
             rows=[("H.264 Image Size", "VGA  (720P de fábrica)"), ("Video Bit Rate", "384 kbps  (2048)"), ("H.264 Profile Type", "BP/MP/HP (igual)")], hl=1))
c.add(Step(48, 384, 6))
c.add(Note(620, 384, 532, "Grandstream lo dice en el manual del GXV3350: en algunas redes 720P es demasiado y deja sin video o con mala imagen; conviene VGA o CIF y 384 kbps o menos.", kind="ok", size=16))
c.add(Note(620, 520, 532, "Más bit rate mejora la imagen solo si la red lo deja pasar; si no, la pérdida la empeora.", kind="info", size=16))
save(c, "22-paso6.svg")
