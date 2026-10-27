import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/hikcentral/src")
from _hc import *

# ---------------------------------------------------------------- 1.svg: mapa de capas
c = Canvas(K(), "Cada falla vive en una capa: ubicala primero")
L = [  # (título, detalle, síntoma típico, kind)
    ("Clientes", "Web Client configura · Control Client opera · Mobile", "VSM217: Control Client de otra versión", "info"),
    ("Streaming Server", "otra máquina, solo si hace falta", "Se suma con más de 200 cámaras", "info"),
    ("SYS + Streaming Gateway", "gestión, usuarios, base de datos y video", "Puerto en rojo en Service Manager", "info"),
    ("Equipos", "cámaras, NVR, controladoras", "Cámara offline en la plataforma", "info"),
]
y0, hh, gap = 124, 92, 14
for i, (t, d, s, kd) in enumerate(L):
    y = y0 + i * (hh + gap)
    dark = i == 2
    c.add(rect(48, y, 640, hh, DEEP if dark else WHITE, DEEP if dark else LINE2, rx=16))
    c.add(text(72, y + 40, t, 21, 600, WHITE if dark else INK, FD))
    c.add(text(72, y + 70, d, 16, 400, "#9FC3E3" if dark else INK3, FM))
    c.add(f'<path d="M700 {y + hh / 2}H744" stroke="{LINE2}" stroke-width="2" stroke-dasharray="5 5"/>')
    c.add(rect(752, y + 14, 400, hh - 28, WARN_BG, WARN, rx=14, sw=1.5))
    c.add(text(774, y + hh / 2 + 6, s, 16, 500, WARN, FB))
c.add(text(752, 116, "SÍNTOMA TÍPICO DE ESA CAPA", 13, 600, INK3, FM, ls=1.5))
c.add(text(48, 560, "El Streaming Gateway viene dentro del SYS y, según el FAQ, sirve hasta 200 cámaras reenviadas.", 17, 500, INK2))
c.add(text(48, 592, "Por eso el Streaming Server va en otra máquina: nunca junto al SYS.", 17, 500, INK2))
c.add(text(48, 636, "Antes de diagnosticar: equipo, SYS, streaming o cliente.", 18, 600, BLUE, FB))
save(c, "1.svg")

# ---------------------------------------------------------------- 1-paso3: qué anotar del Service Manager
c = Canvas(K(3), "Anotá servicio, estado y puerto de cada uno")
c.add(Table(48, 128, ["Servicio", "Estado", "Puerto", "Lectura"], [
    ["SYS (web de clientes)", "Exceptional", "80 en rojo", "otro proceso tomó el puerto"],
    ["SYS (HTTPS)", "Running", "443", "bien"],
    ["Streaming Gateway (RTSP)", "Running", "554", "bien"],
    ["Streaming Gateway (vivo web)", "Running", "559", "bien"],
], [330, 190, 170, 414], hl_row=0, row_h=50, mono_cols=(1, 2)))
c.add(tag(1080, 209, "conflicto", "alert"))
c.add(text(48, 410, "Planilla de ejemplo: copiá nombres y estados tal cual los muestra tu versión.", 16, 400, INK3))
c.add(Note(48, 440, 540, "Service Manager se abre con clic derecho > Ejecutar como administrador. Un puerto en rojo es un conflicto con otro programa.", title="Cómo leerlo", kind="info"))
c.add(Note(612, 440, 540, "Service Manager permite detener servicios. En un servidor en producción, solo mirar y anotar.", title="En producción, solo mirar", kind="warn"))
save(c, "1-paso3.svg")

# ---------------------------------------------------------------- 1-paso5: misma versión SYS y Control Client
c = Canvas(K(5), "Control Client y SYS: exactamente la misma versión")
for i, (cc, ok) in enumerate([("V2.5.500", True), ("V2.4.1", False)]):
    x = 48 + i * 564
    kd = "ok" if ok else "alert"
    c.add(panel(x, 128, 540, 330, "Coinciden: entra" if ok else "No coinciden: VSM217", kd))
    s = c.add(Generic(x + 20, 180, "SYS", "V2.5.500", icon="server", w=212, dark=True))
    p = c.add(Generic(x + 308, 180, "Control Client", cc, icon="laptop", w=212, hl=None if ok else ALERT))
    c.add(Arrow(p.left(), s.right(), kind="ok" if ok else "alert", label="login"))
    c.add(Mark(x + 50, 330, ok))
    c.add(text(x + 82, 337, "Login correcto, vivo y alarmas" if ok else "El login falla con VSM217", 18, 600, OK if ok else ALERT))
    c.add(text(x + 24, 392, "Versión del SYS: Web Client, página de inicio." if ok else "Solución: instalar el Control Client", 16, 400, INK2))
    c.add(text(x + 24, 420, "Versión del cliente: en el puesto." if ok else "de la misma versión que el SYS.", 16, 400, INK2))
c.add(Note(48, 482, 1104, "Después de actualizar el SYS, el Control Client de cada puesto se actualiza también. Y recordá: el Control Client no corre en una máquina virtual.", title="Versiones de ejemplo", kind="info"))
save(c, "1-paso5.svg")
