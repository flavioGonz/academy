"""Teoría de Grabación y hora: el pedido de video va por hora; con el NVR corrido llega otro momento."""
from _anim_lpr import *

caps = ["La lectura queda a las 14:30:00 (hora de la cámara: a menos de 10 min).",
        "Grabación: OmniAccess le pide al NVR el canal 3 a las 14:30:00.",
        "El NVR va 185 s adelantado: su 14:30:00 es otro momento, sin el auto.",
        "Sincronizar hora pone la hora del servidor (o NTP): el video coincide."]
a = new(24, "Hora", "El video se pide por hora: si el NVR está corrido, llega otro momento", caps, still=2, size=18)

# servidor
a.add(a.box(48, 182, 300, 128, a.INK, rx=14))
a.add(a.text(68, 214, "Servidor OmniAccess", 18, a.WHITE, a.SANS, 600))
a.add(a.text(68, 270, "14:30:00", 40, a.WHITE, a.MONO, 600))
a.add(a.text(68, 296, "hora de referencia", 15, DARK_SUB, a.MONO))
# NVR
a.add(a.box(450, 182, 300, 128, a.WHITE, a.LINE, rx=14))
a.add(a.text(470, 214, "NVR · canal 3", 18, a.INK, a.SANS, 600))
vis(a, a.text(470, 270, "14:33:05", 40, a.BAD, a.MONO, 600), 0, 2)
vis(a, a.text(470, 270, "14:30:00", 40, a.OK, a.MONO, 600), 3)
a.add(a.text(470, 296, "su reloj", 15, a.GREY, a.MONO))
vis(a, a.pill(650, 322, "+185 s · alerta de reloj", a.BAD, a.BADBG, size=14, anchor="middle"), 2)
# video
VX, VY, VW, VH = 852, 182, 300, 196
a.add(a.box(VX, VY, VW, VH, "#0B1E33", rx=14))
a.add(f'<path d="M{VX + 110} {VY + 30} L{VX + 20} {VY + VH - 10} M{VX + 190} {VY + 30} L{VX + 280} {VY + VH - 10}" stroke="#3A5878" stroke-width="3"/>')
a.add(f'<line x1="{VX + 60}" y1="{VY + 140}" x2="{VX + 240}" y2="{VY + 140}" stroke="#2FBF84" stroke-width="3"/>')
a.add(a.text(VX + VW / 2, VY + VH + 26, "lo que devuelve el NVR", 15, a.GREY, a.MONO, 600, "middle"))
car = (f'<rect x="{VX + 100}" y="{VY + 86}" width="100" height="70" rx="14" fill="#6E88A1"/>'
       f'<rect x="{VX + 112}" y="{VY + 96}" width="76" height="24" rx="5" fill="#A9BED2"/>'
       f'<rect x="{VX + 122}" y="{VY + 132}" width="56" height="16" rx="3" fill="#FFFFFF"/>')
vis(a, car, 3, d0=6)
vis(a, a.text(VX + VW / 2, VY + 60, "carril vacío", 17, "#FFD28A", a.SANS, 600, "middle"), 2, d0=4)
vis(a, a.text(VX + VW / 2, VY + 60, "el auto en la línea", 17, "#5BE0A5", a.SANS, 600, "middle"), 3, d0=6)

# 1 · lectura
token(a, "SBA1234 · 14:30:00", [(ph(a, 0)[0] + 2, 198, 346), (ph(a, 0)[1], 198, 346)], bg=a.CYAN)
vis(a, a.text(48, 384, "hora de la cámara: a menos de 10 min del servidor, vale", 15, a.TXT), 0)
# 2 · pedido
vis(a, line(a, 348, 236, 448, 236, a.BLUE, 3), 1, 3)
vis(a, a.pill(398, 322, "canal 3 · 14:30:00", a.WHITE, a.BLUE, size=14, anchor="middle"), 1, 2)
vis(a, line(a, 750, 236, 850, 236, a.BLUE, 3), 1, 3, d0=6)
# 4 · sincronizar
vis(a, a.pill(398, 322, "Sincronizar hora", a.WHITE, a.OK, size=14, anchor="middle"), 3)

# línea de grabación del NVR
LX0, LX1, LY = 120, 1110, 520
a.add(a.text(48, 446, "GRABACIÓN DEL CANAL 3, SEGÚN EL RELOJ DEL NVR", 14, a.GREY, a.MONO, 600, extra='letter-spacing="1.5"'))
a.add(a.box(LX0, LY - 18, LX1 - LX0, 36, a.SLATE, rx=10))
mins = ["14:29", "14:30", "14:31", "14:32", "14:33", "14:34", "14:35"]
step = (LX1 - LX0) / 6
for k, m in enumerate(mins):
    x = LX0 + k * step
    a.add(f'<line x1="{x}" y1="{LY + 18}" x2="{x}" y2="{LY + 28}" stroke="{a.GREY}" stroke-width="2"/>')
    a.add(a.text(x, LY + 50, m, 15, a.GREY, a.MONO, 600, "middle"))
xp_bad = LX0 + step * (4 + 5 / 60)
xp_ok = LX0 + step * 1
vis(a, f'<rect x="{xp_bad - 10}" y="{LY - 16}" width="20" height="32" rx="5" fill="{a.CYAN}"/>' + a.text(xp_bad, LY - 26, "pasó el auto", 15, a.BLUE, a.SANS, 600, "middle"), 0, 2)
vis(a, f'<rect x="{xp_ok - 10}" y="{LY - 16}" width="20" height="32" rx="5" fill="{a.CYAN}"/>' + a.text(xp_ok + 16, LY - 26, "pasó el auto", 15, a.BLUE, a.SANS, 600), 3)
vis(a, f'<line x1="{xp_ok}" y1="{LY - 24}" x2="{xp_ok}" y2="{LY + 24}" stroke="{a.BAD}" stroke-width="4"/>' + a.text(xp_ok, LY + 76, "pedido: 14:30:00", 15, a.BAD, a.MONO, 600, "middle"), 1, 2)
vis(a, f'<line x1="{xp_ok}" y1="{LY - 24}" x2="{xp_ok}" y2="{LY + 24}" stroke="{a.OK}" stroke-width="4"/>' + a.text(xp_ok, LY + 76, "pedido: 14:30:00", 15, a.OK, a.MONO, 600, "middle"), 3)
vis(a, a.text(xp_bad, LY + 76, "185 s después, en su reloj", 15, a.BAD, a.SANS, 600, "middle"), 2)
a.add(a.text(48, 640, "Con más de 120 s de diferencia, la salud de dispositivos abre la alerta de reloj.", 17, a.TXT))
write(a, "5-t1.svg", "Hora y pedido de video", [12, 37, 62, 90])
