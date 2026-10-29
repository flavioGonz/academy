#!/usr/bin/env python3
"""Lección 1 · Laboratorio, paso 4: apt modernize-sources. La línea vieja de un .list se reparte en los campos
de un bloque deb822 (.sources): Types, URIs, Suites, Components. apt update lee el bloque igual, sin la queja de
formato, y para apagar un repositorio alcanza con Enabled: no.
Fuentes: wiki Package_Repositories (formato de una línea, deb822, apt modernize-sources, Enabled: no)."""
from _anim_pmx_red import *

a = new(24, "Repos en orden", "apt modernize-sources: de una línea a un bloque", lab=True)
a.steps([
    "Un .list viejo: todo el repositorio en una línea. Debian 13 se queja.",
    "modernize-sources reparte cada parte en un campo con nombre.",
    "apt update lee el .sources: el mismo repositorio, sin la queja.",
    "Para apagar un repositorio sin borrarlo: Enabled: no en su bloque.",
], still=1)

CW = 10.2  # ancho de un carácter mono a 17 px
OX, OY = 48, 178
a.add(a.box(OX, OY, 1104, 108, a.WHITE, a.LINE, rx=14))
a.add(a.text(OX + 22, OY + 32, "/etc/apt/sources.list.d/repo.list", 15, a.GREY, a.MONO))
LINE1 = "deb http://download.proxmox.com/debian/pve trixie pve-no-subscription"
LX, LY = OX + 22, OY + 76
parts = [("deb", 0, a.BLUE), ("http://download.proxmox.com/debian/pve", 4, a.CYAN), ("trixie", 43, a.OK), ("pve-no-subscription", 50, a.AMB)]
a.add(during(a, a.text(LX, LY, LINE1, 17, a.INK, a.MONO, 600), 0, 28, still=0))
a.add(during(a, a.text(LX, LY, LINE1, 17, a.GREY, a.MONO, 600), 27, 100, still=1))
for w, c0, col in parts:  # subrayado de color de cada parte
    a.add(during(a, line(LX + c0 * CW, LY + 10, LX + (c0 + len(w)) * CW - 3, LY + 10, col, 4), 26, 50, still=1))
at(a, a.text(OX + 1080, OY + 32, "formato viejo", 15, a.AMB, a.MONO, 600, "end"), 4, 50, still=1)
a.add(during(a, a.text(OX + 1080, OY + 32, "repo.list ya no se usa", 15, a.GREY, a.MONO, 600, "end"), 50, 100))

# bloque deb822
BX, BY, BW, BH = 48, 334, 620, 214
a.add(a.box(BX, BY, BW, BH, a.WHITE, a.LINE, rx=14))
a.add(a.text(BX + 22, BY + 32, "/etc/apt/sources.list.d/repo.sources", 15, a.GREY, a.MONO))
FY = [BY + 70 + i * 32 for i in range(5)]
fields = [("Types:", "deb", a.BLUE), ("URIs:", "http://download.proxmox.com/debian/pve", a.CYAN),
          ("Suites:", "trixie", a.OK), ("Components:", "pve-no-subscription", a.AMB)]
for i, (k, v, col) in enumerate(fields):
    a.add(during(a, a.text(BX + 22, FY[i], k, 16, a.INK, a.MONO, 600), 28, 100, still=1))
    a.add(during(a, a.text(BX + 152, FY[i], v, 16, col, a.MONO, 600), 32 + i * 4, 100, still=1))
# las partes viajan de la línea al campo
for i, (w, c0, col) in enumerate(parts):
    x0 = LX + (c0 + len(w) / 2) * CW
    x1 = BX + 152 + len(w) * 9.6 / 2
    a.add(travel(a, a.text(0, 6, w, 16, col, a.MONO, 600, "middle"), [(x0, LY - 6), (x1, FY[i] - 6)], 28 + i * 4, 32 + i * 4, hold=0.2, fade=0.3))
# paso 4: Enabled: no
a.add(during(a, a.box(BX + 12, FY[4] - 24, 300, 34, a.AMBBG, rx=8) + a.text(BX + 22, FY[4], "Enabled: no", 16, a.AMB, a.MONO, 700), 80, 100))

# terminal a la derecha
TX, TY, TW, TH = 700, 334, 452, 214
a.add(a.box(TX, TY, TW, TH, a.INK, rx=14))
a.add(a.text(TX + 20, TY + 28, "TERMINAL DE PVE1", 13, SKY, a.MONO, 400, extra='letter-spacing="1.8"'))
TL = [TY + 60 + i * 27 for i in range(6)]
at(a, tline(a, TX + 20, TL[0], "# apt update", MINT), 2, 25)
at(a, tline(a, TX + 20, TL[1], "aviso: repo.list está en el", GOLD), 8, 25)
at(a, tline(a, TX + 20, TL[2], "formato viejo de una línea", GOLD), 8, 25)
at(a, tline(a, TX + 20, TL[0], "# apt modernize-sources", MINT), 25, 50, still=1)
at(a, tline(a, TX + 20, TL[1], "queda repo.sources", SKY), 46, 50, still=1)
at(a, tline(a, TX + 20, TL[0], "# apt update", MINT), 50, 75)
at(a, tline(a, TX + 20, TL[1], "Hit:4 http://download.proxmox", MINT), 55, 75)
at(a, tline(a, TX + 20, TL[2], "  .com/debian/pve trixie", MINT), 55, 75)
at(a, tline(a, TX + 20, TL[3], "  InRelease", MINT), 55, 75)
at(a, tline(a, TX + 20, TL[4], "sin avisos de formato", SKY), 60, 75)
at(a, tline(a, TX + 20, TL[0], "# apt update", MINT), 84, 100)
at(a, tline(a, TX + 20, TL[1], "este repositorio no se consulta", SKY), 88, 100)
at(a, tline(a, TX + 20, TL[2], "y el bloque queda escrito", SKY), 88, 100)
at(a, tline(a, TX + 20, TL[3], "para volver a habilitarlo", SKY), 88, 100)
# lectura del bloque en el paso 3
a.add(during(a, a.box(BX - 3, BY - 3, BW + 6, BH + 6, "none", a.OK, rx=16, sw=3), 52, 75))
go(a, "lee el bloque", [(BX + BW - 40, BY + 110), (TX + 40, BY + 110)], 52, 56, a.OK, hold=3)

status(a, 600, [
    (0, 25, "Desde Debian 13, apt avisa cuando encuentra repositorios en el formato viejo de una línea.", a.AMB, 0),
    (25, 50, "Cada parte de la línea va a un campo con nombre: más fácil de leer y de revisar.", a.BLUE, 1),
    (50, 75, "Para apt es el mismo repositorio: cambia la forma de escribirlo, no de dónde bajan los paquetes.", a.OK, 0),
    (75, 100, "Enabled: no apaga el bloque y lo deja escrito: así se deshabilita enterprise sin borrarlo.", a.AMB, 0),
], size=17)

write(a, 1, "l1", "apt modernize-sources: de una línea a un bloque",
      "Animación en cuatro tiempos con un archivo viejo /etc/apt/sources.list.d/repo.list, el archivo nuevo repo.sources y la terminal de pve1. "
      "1: repo.list tiene todo el repositorio en una línea, deb http://download.proxmox.com/debian/pve trixie pve-no-subscription, y apt update avisa que es el formato viejo. "
      "2: apt modernize-sources reparte cada parte en un campo con nombre del bloque deb822: Types: deb, URIs: http://download.proxmox.com/debian/pve, Suites: trixie y Components: pve-no-subscription; repo.list ya no se usa. "
      "3: apt update lee el bloque de repo.sources y consulta el mismo repositorio, sin avisos de formato. "
      "4: para apagar un repositorio sin borrarlo se agrega Enabled: no en su bloque; apt update deja de consultarlo y el bloque queda escrito para volver a habilitarlo, como se hace con pve-enterprise sin suscripción.",
      [10, 36, 48, 64, 92])
