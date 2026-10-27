import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-lpr/src")
from _lpr import *


def axis(c, x1, x2, y, ticks):
    c.add(f'<path d="M{x1} {y}H{x2}" stroke="{INK3}" stroke-width="2"/>')
    for x, lbl in ticks:
        c.add(f'<path d="M{x} {y - 6}V{y + 6}" stroke="{INK3}" stroke-width="2"/>')
        c.add(text(x, y + 28, lbl, 15, 500, INK3, FM, anchor="middle"))


# ---------------------------------------------------------------- 9.svg: permanencia y merodeo en el tiempo
c = Canvas(K(), "Permanencia y merodeo: patrones en el tiempo")
c.add(panel(48, 126, 1104, 210, "Permanencia · residente SBA 1234", "info"))
axis(c, 90, 1110, 270, [(140, "08:00"), (400, "08:45"), (660, "09:30"), (920, "10:15")])
c.add(f'<rect x="140" y="236" width="780" height="22" rx="11" fill="{OK_BG}" stroke="{OK}" stroke-width="1.5"/>')
c.add(text(530, 252, "adentro 2h 15m", 15, 700, OK, FM, anchor="middle"))
c.add(tag(140, 214, "entra · P1", "blue", size=15, anchor="middle"))
c.add(tag(920, 214, "sale · P2", "blue", size=15, anchor="middle"))
c.add(panel(48, 360, 1104, 230, "Merodeo · SCD 5678, no registrada", "alert"))
axis(c, 90, 1110, 500, [(140, "21:00"), (380, "21:10"), (620, "21:20"), (860, "21:30")])
c.add(f'<rect x="140" y="470" width="720" height="14" rx="7" fill="{ALERT}" opacity=".18"/>')
c.add(text(500, 466, "ventana de 30 min", 15, 600, ALERT, FM, anchor="middle"))
for x, cam in [(200, "P1"), (452, "P2"), (716, "P1")]:
    c.add(f'<circle cx="{x}" cy="500" r="11" fill="{ALERT}"/>')
    c.add(text(x, 432, cam, 15, 600, INK, FM, anchor="middle"))
c.add(tag(760, 560, "3.ª pasada → alerta Merodeo", "alert", size=15))
c.add(text(68, 560, "Por defecto: 3 pasadas en 30 min, por cualquier acceso; no cuenta residentes autorizados.", 15, 500, INK2, FB))
c.add(text(48, 628, "La permanencia necesita cámaras con el sentido bien puesto; el merodeo deja una entrada en la bitácora.", 16, 500, INK2, FB))
save(c, "9.svg")

# ---------------------------------------------------------------- 9-paso2: anomalías de presencia
c = Canvas(K(2), "Plazas de Parking → Anomalías de presencia")
cards = [("Autos no identificados adentro", "Entraron, no salieron y no son de ningún lote.", "alert", "SCD 5678 · desde ayer"),
         ("Vehículo del barrio adentro hace mucho", "Más de 4 días sin salir (valor por defecto).", "warn", "SBB 4321 · 6 días"),
         ("Lotes sin movimiento", "Posible casa vacía: 21 días sin lecturas.", "info", "Lote 99 · 23 días")]
for i, (t, d, kd, ex) in enumerate(cards):
    x = 48 + i * 376
    c.add(panel(x, 140, 352, 300, None, kd))
    lst, h = wrap(x + 22, 186, t, 300, 20, 700, INK)
    c.add(lst)
    lst2, _ = wrap(x + 22, 186 + h + 18, d, 300, 17, 400, INK2)
    c.add(lst2)
    c.add(pill(x + 22, 408, ex, fg=INK2, size=15, anchor="start"))
c.add(Note(48, 474, 1104, "Son datos para el guardia de la noche y para el administrador: se confirman con el historial antes de escalar.", kind="info", size=16))
save(c, "9-paso2.svg")

# ---------------------------------------------------------------- 9-paso3: simular merodeo respetando el antirrebote
c = Canvas(K(3), "Tres lecturas separadas por 30 s disparan el merodeo")
c.add(codebox(48, 128, 1104, ["for i in 1 2 3; do", "  curl -s -X POST 192.0.2.10:10000/api/webhooks/hikvision ... <licensePlate>SCD5678</licensePlate> ...", "  echo; sleep 30", "done"], size=15)[0])
axis(c, 90, 1110, 400, [(150, "0 s"), (500, "30 s"), (850, "60 s")])
for x, n in [(150, 1), (500, 2), (850, 3)]:
    c.add(f'<rect x="{x}" y="380" width="233" height="14" rx="7" fill="{AMBER}" opacity=".35"/>')
    c.add(f'<circle cx="{x}" cy="400" r="12" fill="{ALERT if n == 3 else INK}"/>')
    c.add(text(x, 364, f"pasada {n}", 15, 600, INK, FB, anchor="middle"))
c.add(text(266, 470, "20 s de antirrebote por cámara", 15, 600, WARN, FM, anchor="middle"))
c.add(card(760, 470, 392, 104, "alert", "MERODEO", "SCD 5678", "3 pasadas en 30 min · 1 acceso"))
c.add(Note(48, 500, 640, "Con menos de 20 s entre envíos, la segunda y la tercera se descartan y no hay alerta. Solo en una instalación de prueba.", kind="warn", size=16))
save(c, "9-paso3.svg")
