"""Teoría de Calibrar de noche: IR y patente retrorreflectiva, anti-brillo, obturador y la escritura por ISAPI."""
from _anim_lpr import *

caps = ["El IR ilumina: la patente devuelve la luz y brilla sobre una escena oscura.",
        "Con faros o IR fuerte, la patente se quema: el anti-brillo baja los brillos.",
        "Obturador: 1/1000 congela más, 1/500 deja entrar el doble de luz.",
        "El calibrador lee el XML, cambia solo un campo y lo vuelve a escribir."]
a = new(24, "Noche", "De noche: luz, obturador y un solo campo por vez", caps, still=2)
a.add('<defs><filter id="glow" x="-40%" y="-80%" width="180%" height="260%"><feGaussianBlur stdDeviation="10"/></filter>'
      '<filter id="soft" x="-10%" y="-20%" width="120%" height="140%"><feGaussianBlur stdDeviation="1.6"/></filter></defs>')

FX, FY, FW, FH = 48, 182, 560, 340
a.add(a.box(FX, FY, FW, FH, "#071526", rx=16))
a.add(a.text(FX + 20, FY + 32, "VISTA DE LA CÁMARA, DE NOCHE", 14, DARK_SUB, a.MONO, 600, extra='letter-spacing="1.5"'))
cx, cy = FX + FW / 2, FY + 210
# frente del auto, apenas visible
a.add(f'<path d="M{cx - 190} {cy + 90} L{cx - 170} {cy - 40} Q{cx - 160} {cy - 80} {cx - 110} {cy - 86} L{cx + 110} {cy - 86} Q{cx + 160} {cy - 80} {cx + 170} {cy - 40} L{cx + 190} {cy + 90} Z" fill="#12263D"/>')
lamp = lambda r, op: (f'<circle cx="{cx - 130}" cy="{cy - 10}" r="{r}" fill="#FFF6D8" opacity="{op}" filter="url(#glow)"/>'
                      f'<circle cx="{cx + 130}" cy="{cy - 10}" r="{r}" fill="#FFF6D8" opacity="{op}" filter="url(#glow)"/>')
a.add(f'<circle cx="{cx - 130}" cy="{cy - 10}" r="18" fill="#FFF6D8"/><circle cx="{cx + 130}" cy="{cy - 10}" r="18" fill="#FFF6D8"/>')
pl = lambda extra="": plate(a, cx, cy + 40, "SBA 1234", w=170, h=50, size=26, extra=extra)
# 1 · IR: patente brillante
vis(a, f'<rect x="{cx - 95}" y="{cy + 10}" width="190" height="60" rx="10" fill="#FFFFFF" opacity=".35" filter="url(#glow)"/>' + pl(), 0)
# 2 · quemada y después corregida
s0, s1 = ph(a, 1)
mid = (s0 + s1) / 2
a.add(a.group(lamp(60, .9) + f'<rect x="{cx - 110}" y="{cy}" width="220" height="80" rx="14" fill="#FFFFFF" filter="url(#glow)"/>'
              + f'<rect x="{cx - 88}" y="{cy + 14}" width="176" height="52" rx="8" fill="#FFFFFF"/>', a.show(s0, mid), still=0))
a.add(a.group(a.text(cx, FY + FH - 22, "patente quemada", 17, "#FFD28A", a.SANS, 600, "middle"), a.show(s0, mid), still=0))
a.add(a.group(pl() + a.text(cx, FY + FH - 22, "anti-brillo: vuelve a leerse", 17, "#5BE0A5", a.SANS, 600, "middle"), a.show(mid, s1), still=0))
# 3 y 4 · patente legible
vis(a, pl(), 2, 3)
vis(a, a.text(cx, FY + FH - 22, "1/500: legible y sin movido a 20 o 30 km/h", 17, "#5BE0A5", a.SANS, 600, "middle"), 2, 3)
vis(a, a.text(cx, FY + FH - 22, "IR propio: la patente brilla, el resto queda oscuro", 17, a.WHITE, a.SANS, 600, "middle"), 0)

# panel derecho
RX, RY, RW = 650, 182, 502
a.add(a.box(RX, RY, RW, FH, a.WHITE, a.LINE, rx=16))
# 1
vis(a, a.text(RX + 24, RY + 44, "Retrorreflectiva", 20, a.INK, a.SANS, 600)
    + a.text(RX + 24, RY + 74, "devuelve la luz hacia la fuente", 17, a.TXT)
    + card(a, RX + 30, RY + 120, 130, 70, "Cámara", "IR", tsize=17)
    + a.box(RX + 360, RY + 128, 110, 54, a.WHITE, a.INK, rx=8, sw=2.5) + f'<rect x="{RX + 362}" y="{RY + 130}" width="106" height="10" rx="4" fill="{a.BLUE}"/>'
    + line(a, RX + 168, RY + 140, RX + 352, RY + 140, "#B26A00", 3) + line(a, RX + 352, RY + 172, RX + 168, RY + 172, "#B26A00", 3, "7 5")
    + a.text(RX + 260, RY + 218, "va y vuelve casi entera", 16, a.AMB, a.SANS, 600, "middle")
    + a.text(RX + 24, RY + 280, "Con una cámara común pasa lo contrario:", 16, a.TXT)
    + a.text(RX + 24, RY + 304, "su IR rebota en la patente y la quema.", 16, a.TXT), 0)
# 2
vis(a, a.text(RX + 24, RY + 44, "Anti-brillo", 20, a.INK, a.SANS, 600)
    + a.text(RX + 24, RY + 74, "supresión de sobreexposición", 17, a.TXT)
    + a.box(RX + 24, RY + 120, 420, 14, a.SLATE, rx=7) + a.box(RX + 24, RY + 120, 252, 14, a.BLUE, rx=7)
    + f'<circle cx="{RX + 276}" cy="{RY + 127}" r="13" fill="{a.WHITE}" stroke="{a.BLUE}" stroke-width="3"/>'
    + a.text(RX + 24, RY + 170, "perfil barrio-noche: 60", 17, a.BLUE, a.MONO, 600)
    + a.text(RX + 24, RY + 230, "Baja los brillos para que los faros", 17, a.TXT)
    + a.text(RX + 24, RY + 256, "no quemen la patente.", 17, a.TXT), 1)
# 3
bar = lambda y, w, lab, luz, fg: (a.text(RX + 24, y + 22, lab, 20, a.INK, a.MONO, 600)
                                  + a.box(RX + 120, y, w, 32, fg, rx=8) + a.text(RX + 130 + w, y + 22, luz, 16, fg, a.SANS, 600))
vis(a, a.text(RX + 24, RY + 44, "Obturador", 20, a.INK, a.SANS, 600)
    + a.text(RX + 24, RY + 74, "cuánto tiempo entra luz en cada foto", 17, a.TXT)
    + bar(RY + 110, 110, "1/1000", "la mitad de luz", a.GREY)
    + bar(RY + 166, 220, "1/500", "el doble", a.BLUE)
    + a.text(RX + 24, RY + 250, "1/1000 congela más: conviene en accesos rápidos.", 16, a.TXT)
    + a.text(RX + 24, RY + 276, "En un barrio se anda a 20 o 30 km/h:", 16, a.TXT)
    + a.text(RX + 24, RY + 302, "el perfil elige 1/500.", 16, a.BLUE, a.SANS, 600), 2)
# 4 · leer, cambiar un campo, escribir
s0, s1 = ph(a, 3)
vis(a, a.text(RX + 24, RY + 44, "GET /ISAPI/Image/channels/1/Shutter", 15, a.BLUE, a.MONO, 600), 3)
xml = a.box(RX + 24, RY + 64, 454, 150, a.INK, rx=10) + a.text(RX + 40, RY + 96, "<?xml ...?>", 15, DARK_SUB, a.MONO) + a.text(RX + 40, RY + 124, "...", 15, DARK_SUB, a.MONO) + a.text(RX + 40, RY + 196, "...", 15, DARK_SUB, a.MONO)
vis(a, xml, 3, d0=2)
a.add(a.group(a.text(RX + 40, RY + 160, "<ShutterLevel>1/1000</ShutterLevel>", 16, a.WHITE, a.MONO, 600), a.show(s0 + 2, s0 + 10), still=0))
a.add(a.group(a.box(RX + 32, RY + 140, 438, 30, "#0B3A66", rx=6) + a.text(RX + 40, RY + 160, "<ShutterLevel>1/500</ShutterLevel>", 16, "#5BE0A5", a.MONO, 600), a.show(s0 + 10, s1), still=0))
vis(a, a.text(RX + 24, RY + 250, "cambia solo ese campo", 17, a.AMB, a.SANS, 600), 3, d0=10)
vis(a, a.text(RX + 24, RY + 300, "PUT del mismo XML a la misma ruta", 15, a.BLUE, a.MONO, 600), 3, d0=14)

a.add(a.text(48, 572, "La zona de lectura y la línea de captura van aparte, en /ISAPI/Traffic/channels/1/vehicleDetect.", 17, a.TXT))
a.add(a.text(48, 604, "Después se mide con la tasa por hora: leídas sobre total, franja por franja.", 17, a.INK, a.SANS, 600))
write(a, "6-t1.svg", "Calibración nocturna", [12, 30, 44, 62, 90])
