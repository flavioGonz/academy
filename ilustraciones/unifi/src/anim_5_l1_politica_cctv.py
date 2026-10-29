#!/usr/bin/env python3
"""Lección 5 · Laboratorio, paso 4: CCTV en zona propia con una política que permite solo del NVR hacia las cámaras
y bloquea el resto. El NVR pasa; una PC de Staff no; la cámara no inicia hacia Internal.
Fuentes: lab.md de la lección (paso 4) y theory_md (WunderTech: una zona propia no llega a las otras zonas salvo
que escribas políticas)."""
from _anim_red_unifi import *  # noqa

a = new(24, "VLAN por función", "Zona CCTV: solo el NVR llega a las cámaras", [
    "La política de la zona CCTV: permitir desde el NVR y bloquear el resto.",
    "El NVR abre la conexión a la cámara: coincide con la primera regla y pasa.",
    "Una PC de Staff intenta lo mismo: no es el NVR y cae en el bloqueo.",
    "La cámara tampoco inicia hacia Staff: la zona propia no sale a otras zonas.",
], still=1, paso=4)

a.add(dev(a, 48, 225, 290, 90, "NVR", "10.10.10.20 · Staff", icon="server"))
a.add(dev(a, 48, 400, 290, 90, "PC de Staff", "10.10.10.30", icon="laptop"))
a.add(dev(a, 862, 225, 290, 90, "Cámara", "192.168.30.11 · CCTV", icon="camera"))
a.add(pill(a, 48, 186, "zona Internal", "ok"))
a.add(pill(a, 1152, 186, "zona CCTV", "info", anchor="end"))

GX, GY, GW, GH = 420, 186, 360, 380
a.add(a.box(GX, GY, GW, GH, a.INK, None, rx=14))
a.add(glyph(a, "shield", GX + 18, GY + 16, a.CYAN))
a.add(a.text(GX + 62, GY + 40, "Gateway · Policy Engine", 18, a.WHITE, a.HEAD, 600))
a.add(wire(338, 270, 420, 270, a.BLUE, 4))
a.add(wire(780, 270, 862, 270, a.CYAN, 4))
a.add(wire(338, 445, 420, 445, a.BLUE, 4))
a.add(poly([(193, 490), (193, 528), (420, 528)], a.LINE, 2, "3 7"))
a.add(f'<line x1="{GX + 10}" y1="270" x2="{GX + GW - 10}" y2="270" stroke="{SKY}" stroke-width="2" stroke-dasharray="3 7"/>')

PY = 330
a.add(a.text(GX + 20, PY, "Políticas hacia la zona CCTV", 15, SKY, a.MONO))
R1 = (a.box(GX + 16, PY + 16, GW - 32, 82, a.NAVY2, None, rx=10)
      + a.pill(GX + 30, PY + 30, "Allow", a.OK, a.OKBG, 15, 28)
      + a.text(GX + 124, PY + 50, "origen 10.10.10.20", 15, a.WHITE, a.MONO, 600)
      + a.text(GX + 30, PY + 84, "destino: cámaras de CCTV", 15, SKY, a.MONO))
R2 = (a.box(GX + 16, PY + 112, GW - 32, 82, a.NAVY2, None, rx=10)
      + a.pill(GX + 30, PY + 126, "Block", a.BAD, a.BADBG, 15, 28)
      + a.text(GX + 124, PY + 146, "el resto", 15, a.WHITE, a.MONO, 600)
      + a.text(GX + 30, PY + 180, "hacia CCTV y desde CCTV", 15, SKY, a.MONO))
a.add(R1 + R2)
HL1 = a.box(GX + 14, PY + 14, GW - 28, 86, "none", GOLD, rx=11, sw=3)
HL2 = a.box(GX + 14, PY + 110, GW - 28, 86, "none", GOLD, rx=11, sw=3)
vis(a, HL1 + HL2, 0)
vis(a, HL1, 1)
vis(a, HL2, 2, 3)

# 2 · NVR → cámara
s0, s1 = ph(a, 1)
go(a, [(338, 270), (790, 270)], s0 + 2, s0 + 11, "NVR → cámara", a.BLUE, hold=s0 + 12, still=1)
go(a, [(862, 290), (338, 290)], s0 + 13, s0 + 21, "video", a.CYAN, hold=s1 - 0.5)
during(a, check(a, 821, 236, 14), s0 + 11, s1, still=1)

# 3 · PC → cámara, bloqueada
s0, s1 = ph(a, 2)
go(a, [(193, 490), (193, 528), (330, 528)], s0 + 2, s0 + 7, "PC → cámara", a.BLUE, hold=s1 - 0.5)
during(a, xmark(a, 420, 528, 17) + poly([(398, 528), (408, 528)], a.BAD, 3), s0 + 7, s1)

# 4 · cámara → Staff, bloqueada
s0, s1 = ph(a, 3)
go(a, [(1000, 315), (1000, 345), (884, 345)], s0 + 2, s0 + 7, "cámara → Staff", a.CYAN, hold=s1 - 0.5)
during(a, xmark(a, 792, 345, 17), s0 + 7, s1)

status(a, 610, [
    (0, 25, "Primero lo permitido, puntual; después el bloqueo para todo lo demás.", a.INK, 0),
    (25, 50, "El NVR graba: el permiso es por origen, no por toda la red Staff.", a.OK, 1),
    (50, 75, "Estar en la misma VLAN que el NVR no alcanza: la política mira el origen.", a.BAD, 0),
    (75, 100, "Si alguien toma una cámara, desde ahí no llega a las PCs.", a.OK, 0),
])

write(a, 5, "l1", "Política de la zona CCTV",
      "Animación en cuatro tiempos del paso 4 con el NVR (10.10.10.20) y una PC de Staff (10.10.10.30) en la zona Internal, el gateway con el Policy Engine "
      "y una cámara (192.168.30.11) en la zona propia CCTV. "
      "1: las políticas hacia la zona CCTV: Allow con origen 10.10.10.20 hacia las cámaras, y Block para el resto, hacia CCTV y desde CCTV. "
      "2: el NVR abre la conexión hacia la cámara, coincide con la primera regla, pasa y el video llega al NVR. "
      "3: la PC de Staff intenta lo mismo, no es el NVR y cae en el bloqueo: la política mira el origen, no toda la red Staff. "
      "4: la cámara intenta iniciar hacia Staff y también se bloquea: la zona propia no llega a otras zonas sin una política.",
      [12, 40, 62, 90])
