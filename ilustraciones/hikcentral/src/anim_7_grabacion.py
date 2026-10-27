"""Teoría de Dónde graba: grabar en el sitio contra grabar en el centro cuando se corta el enlace."""
from _anim_hc import *

caps = ["Graban las dos: CAM-A en el NVR del sitio, CAM-B en pStor, en el centro.",
        "Se corta el enlace: el NVR sigue grabando; en el centro queda un hueco.",
        "Vuelve el enlace: la grabación central sigue, con el hueco marcado.",
        "Para reproducir CAM-A, el video viaja desde el NVR solo mientras se mira."]
a = new(28, "Grabación", "Grabar en el sitio o en el centro: qué pasa si se corta el enlace", caps, still=2)

a.add(a.box(48, 182, 520, 240, None, "#C2D4E6", rx=22, extra='fill-opacity="0" stroke-dasharray="7 7"'))
a.add(a.text(70, 176, "SUCURSAL", 14, a.GREY, a.MONO, 600))
a.add(a.box(812, 182, 340, 240, None, "#C2D4E6", rx=22, extra='fill-opacity="0" stroke-dasharray="7 7"'))
a.add(a.text(834, 176, "CENTRO", 14, a.GREY, a.MONO, 600))
a.add(card(a, 72, 204, 200, 76, "CAM-A", "graba en el sitio"))
a.add(card(a, 72, 322, 200, 76, "NVR", "del sitio"))
a.add(card(a, 344, 204, 200, 76, "CAM-B", "graba en el centro"))
a.add(card(a, 836, 204, 292, 76, "pStor", "almacenamiento central", dark=True))
a.add(card(a, 836, 322, 292, 76, "Control Client", "operador"))
a.add(line(a, 172, 280, 172, 322, a.LINE, 3, arrow=False))
a.add(line(a, 544, 242, 836, 242, a.LINE, 3, arrow=False))
a.add(a.text(620, 230, "enlace", 14, a.GREY, a.MONO, 600, "middle"))
a.add(line(a, 272, 360, 836, 360, a.LINE, 3, arrow=False, dash="4 6"))

# flujos de grabación
a.add(line(a, 172, 280, 172, 322, a.OK, 4, arrow=False))
vis(a, line(a, 544, 242, 836, 242, a.CYAN, 4, arrow=False), 0)
vis(a, line(a, 544, 242, 836, 242, a.CYAN, 4, arrow=False), 2, 3)
vis(a, line(a, 544, 242, 836, 242, a.BAD, 3, "6 6", arrow=False), 1)
stream(a, 172, 280, 172, 322, 0, 100, a.OK, tt=3, gap=2.4, r=6)
s0, s1 = ph(a, 0); stream(a, 544, 242, 836, 242, 1, s1, a.CYAN)
s0, s1 = ph(a, 2); stream(a, 544, 242, 836, 242, s0 + 1, 100, a.CYAN)
s0, s1 = ph(a, 1); stream(a, 544, 242, 700, 242, s0, s1, a.CYAN, tt=2.5)
vis(a, '<circle cx="740" cy="242" r="20" fill="#FCEAE6" stroke="#D2492F" stroke-width="2.5"/><path d="M732 234 L748 250 M748 234 L732 250" stroke="#D2492F" stroke-width="3"/>', 1)
vis(a, a.text(740, 290, "enlace cortado", 15, a.BAD, a.SANS, 600, "middle"), 1)
# reproducción de CAM-A
s0, s1 = ph(a, 3)
token(a, "reproducir CAM-A", [(s0 + 1, 980, 400), (s0 + 6, 980, 400)], bg=a.BLUE)
stream(a, 272, 360, 836, 360, s0 + 6, 100, a.BLUE)
vis(a, a.text(554, 386, "video de CAM-A, solo mientras se reproduce", 15, a.BLUE, a.SANS, 600, "middle"), 3)

# líneas de tiempo
X0, X1 = 280, 1150
W = (X1 - X0) / 3
for r, (nm, y) in enumerate((("CAM-A · NVR del sitio", 470), ("CAM-B · pStor central", 530))):
    a.add(a.text(48, y + 21, nm, 15, a.INK, a.MONO, 600))
    a.add(a.box(X0, y, X1 - X0, 30, a.SLATE, a.LINE, rx=8))
    for i in range(3):
        gap = r == 1 and i == 1
        seg = a.box(X0 + i * W + 2, y + 3, W - 4, 24, a.BADBG if gap else a.OKBG, a.BAD if gap else a.OK, rx=6, sw=1.5)
        seg += a.text(X0 + i * W + W / 2, y + 21, "hueco: no grabó" if gap else "grabado", 14, a.BAD if gap else a.OK, a.MONO, 600, "middle")
        vis(a, seg, i, 3)
a.add(a.text(48, 610, "La grabación en el sitio no depende del enlace. La central necesita ancho de banda", 17, a.TXT))
a.add(a.text(48, 638, "sostenido las 24 horas, y cada corte deja un hueco en el centro.", 17, a.TXT))
write(a, "7-t1.svg", "Grabar en el sitio o en el centro", [12, 38, 62, 90])
