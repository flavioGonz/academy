"""Teoría de Tres formas de alta: ISUP da vuelta la dirección de la conexión y pasa el NAT."""
from _anim_hc import *

caps = ["Por IP, el SYS intenta entrar al 8000 de la cámara y el NAT lo corta.",
        "Con ISUP, la cámara sale hacia el 7660 del SYS: el router la deja salir.",
        "El SYS valida Device ID y clave: la cámara queda registrada.",
        "Por esa sesión viajan pedidos y eventos, sin puertos abiertos en el sitio."]
a = new(26, "ISUP", "ISUP: la cámara llama y el NAT deja de ser un problema", caps, still=3)

a.add(a.box(48, 196, 560, 300, None, "#C2D4E6", rx=22, extra='fill-opacity="0" stroke-dasharray="7 7"'))
a.add(a.text(70, 190, "SITIO SIN IP FIJA", 14, a.GREY, a.MONO, 600))
a.add(a.box(784, 196, 368, 300, None, "#C2D4E6", rx=22, extra='fill-opacity="0" stroke-dasharray="7 7"'))
a.add(a.text(806, 190, "CENTRO", 14, a.GREY, a.MONO, 600))
a.add(card(a, 72, 300, 220, 92, "Cámara", "LAB-CAM-01"))
a.add(card(a, 364, 300, 220, 92, "Router", "con NAT"))
a.add(card(a, 820, 300, 300, 92, "SYS", "escucha el 7660", dark=True))
a.add(line(a, 292, 346, 364, 346, a.LINE, 3, arrow=False))
a.add(line(a, 584, 346, 820, 346, a.LINE, 3, arrow=False))

# 1: entrada bloqueada
s0, s1 = ph(a, 0)
token(a, "SYS → :8000", [(s0 + 2, 960, 270), (s0 + 12, 640, 270), (s0 + 20, 640, 270)], bg=a.BAD)
vis(a, '<circle cx="600" cy="300" r="20" fill="#FCEAE6" stroke="#D2492F" stroke-width="2.5"/><path d="M592 292 L608 308 M608 292 L592 308" stroke="#D2492F" stroke-width="3"/>', 0)
vis(a, a.text(474, 430, "entrada nueva: no pasa", 16, a.BAD, a.SANS, 600, "middle"), 0)
# 2: la cámara sale
s0, s1 = ph(a, 1)
token(a, "registro → :7660", [(s0 + 2, 182, 270), (s0 + 10, 474, 270), (s0 + 18, 960, 270), (s1, 960, 270)], bg=a.OK)
vis(a, a.text(474, 430, "salida: pasa, como navegar", 16, a.OK, a.SANS, 600, "middle"), 1)
# sesión abierta, del tiempo 2 en adelante
vis(a, line(a, 292, 346, 364, 346, a.OK, 4, "8 6", arrow=False) + line(a, 584, 346, 820, 346, a.OK, 4, "8 6", arrow=False)
    + a.box(364, 300, 220, 92, "none", a.OK, rx=14, sw=3), 1, 3)
vis(a, a.text(474, 456, "sesión abierta por la cámara", 15, a.OK, a.MONO, 600, "middle"), 2, 3)
# 3: validación
vis(a, a.pill(970, 230, "Device ID + clave: ok", a.OK, a.OKBG, anchor="middle"), 2, 3)
vis(a, a.pill(182, 230, "online", a.WHITE, a.OK, anchor="middle"), 2, 3)
# 4: tráfico por la sesión
s0, s1 = ph(a, 3)
for k in range(2):
    t = s0 + 2 + k * 11
    token(a, "pedido", [(t, 800, 346), (t + 8, 310, 346)], bg=a.BLUE, size=13)
    token(a, "evento", [(t + 4, 310, 346), (t + 11, 800, 346)], bg=a.AMB, size=13)

a.add(a.text(48, 556, "Solo el centro publica puertos: 7660 para el registro, y los de video y archivos según la", 17, a.TXT))
a.add(a.text(48, 584, "Communication Matrix (16000 y 16001 para stream, 8555 para archivos).", 17, a.TXT))
a.add(a.text(48, 628, "Con IP fija y ruta, por IP. Sin IP fija, ISUP.", 18, a.BLUE, a.SANS, 600))
write(a, "5-t1.svg", "ISUP pasa el NAT", [10, 36, 62, 88])
