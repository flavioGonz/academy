import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-lpr/src")
from _lpr import *

# ---------------------------------------------------------------- 5.svg: hora y grabación
c = Canvas(K(), "Misma hora en cámara, NVR y servidor")
srv = c.add(Server(440, 134, "Servidor OmniAccess", "hora de referencia", w=320, hl=CYAN))
c.add(text(600, 254, "14:30:00", 30, 700, INK, FM, anchor="middle"))
cam = c.add(Camera(60, 330, "P1 - Entrada (21)", "cámara ANPR", w=300))
nvr = c.add(Generic(840, 330, "NVR de prueba", "graba 24/7", icon="server", w=300))
c.add(Arrow((srv.x + 60, srv.y + srv.h), cam.top(), label="Sincronizar hora", label_at=0.55, label_dy=-6))
c.add(Arrow((srv.x + srv.w - 60, srv.y + srv.h), nvr.top(), label="Sincronizar hora", label_at=0.55, label_dy=-6))
c.add(tag(210, 452, "+2 s · bien", "ok", anchor="middle"))
c.add(tag(990, 452, "+185 s · alerta de reloj", "alert", anchor="middle"))
c.add(Cable(cam.right(), nvr.left(), kind="data", label="grabación · canal 3", label_dy=-14))
c.add(Note(60, 500, 520, "Con más de 120 s de diferencia se abre la alerta. Si la cámara está corrida más de 10 min, el evento usa la hora del servidor.", kind="warn", size=16))
c.add(Note(620, 500, 520, "Sin el vínculo cámara → NVR → canal no hay Grabación, Clip ni ZIP con video: el historial dice «sin NVR».", kind="info", size=16))
save(c, "5.svg")

# ---------------------------------------------------------------- 5-paso3: leer los desfases antes de corregir
c = Canvas(K(3), "Sincronizar hora: mirá el desfase y después confirmá")
c.add(Table(48, 140, ["Equipo", "Hora del equipo", "Desfase", "Estado"],
            [["P1 - Entrada (21)", "14:30:02", "+2 s", "bien"], ["P2 - Salida (22)", "14:33:05", "+185 s", "alerta"], ["NVR de prueba", "14:29:59", "-1 s", "bien"]],
            [330, 300, 200, 274], hl_row=1, row_h=52, mono_cols=(1, 2)))
c.add(panel(48, 380, 540, 170, "Hora del servidor", "ok", sub="modo por defecto"))
lst, _ = wrap(68, 476, "La empuja por la red local en Montevideo. No necesita internet ni un servidor NTP. Pregunta antes de tocar.", 490, 16, 400, INK2)
c.add(lst)
c.add(panel(612, 380, 540, 170, "NTP", "info", sub="si hay un servidor de hora en la red"))
lst, _ = wrap(632, 476, "La cámara pide la hora a ese servidor cada cierto tiempo. Solo anda si el equipo lo alcanza.", 490, 16, 400, INK2)
c.add(lst)
save(c, "5-paso3.svg")

# ---------------------------------------------------------------- 5-paso5: la cuenta del disco
c = Canvas(K(5), "Hacé la cuenta del disco antes de prometer días")
for d in range(30):
    x = 48 + (d % 10) * 62
    y = 150 + (d // 10) * 70
    c.add(f'<rect x="{x}" y="{y}" width="54" height="56" rx="8" fill="{SOFT}" stroke="{BLUE}" stroke-width="1.5"/>')
    c.add(text(x + 27, y + 34, str(d + 1), 15, 600, BLUE, FM, anchor="middle"))
c.add(text(48, 392, "30 días de fotos · 8 cámaras con tráfico normal", 17, 600, INK, FB))
c.add(code(48, 412, 610, "3,5 GB/día x 30 días = 105 GB (el manual redondea a 120 GB)", size=16, color="#7EE2B8"))
c.add(code(48, 464, 610, "clips: 7 días de retención (valor típico)", size=16))
c.add(panel(700, 140, 452, 200, "Dónde se ajusta", "info"))
c.add(code(720, 196, 412, "Configuración → Sistema → Almacenamiento", size=15))
lst, _ = wrap(720, 270, "Retención de fotos (típico 30 días) y de clips (típico 7 días), por bucket.", 410, 16, 400, INK2)
c.add(lst)
c.add(Note(700, 366, 452, "Bajar la retención para que entre en el disco es perder evidencia. Si falta espacio, se agranda el disco.", kind="warn", size=16))
c.add(text(48, 560, "Según el Manual del Instalador: hasta 4 cámaras, 250 GB SSD; 8 a 16 cámaras, 500 GB SSD.", 16, 500, INK2, FB))
save(c, "5-paso5.svg")
