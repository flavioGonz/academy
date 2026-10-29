#!/usr/bin/env python3
"""Lección 1 · Resumen, "Cómo se ve en la red": qué servidor contesta cada línea de apt update en un host recién
instalado. Debian base y security contestan con su InRelease firmado; enterprise.proxmox.com, sin clave de
suscripción, contesta 401; con enterprise en Enabled: no y proxmox.sources (no-subscription) contesta
download.proxmox.com, y apt full-upgrade baja los paquetes.
Fuentes: wiki Package_Repositories (URIs, Suites, Components, Signed-By, Enabled: no, SecureApt) y anuncio de 9.x."""
from _anim_pmx_red import *

a = new(24, "Repos en orden", "Quién contesta cada línea de apt update")
a.steps([
    "apt update pide el InRelease de cada repositorio: Debian contesta, firmado.",
    "enterprise.proxmox.com pide la clave de suscripción: sin clave, 401.",
    "Con enterprise en Enabled: no, contesta download.proxmox.com.",
    "apt full-upgrade baja los paquetes y pveversion queda en la ficha.",
], still=2)

# ---------- host
HX, HY, HW, HH = 48, 186, 300, 100
a.add(dev(a, HX, HY, HW, HH, "pve1", "host recién instalado", icon="server", dark=True, sub2="/etc/apt/sources.list.d/", ssize=15))

# ---------- servidores
SX, SW, SH = 744, 408, 62
SYS = [182, 254, 326]
a.add(dev(a, SX, SYS[0], SW, SH, "deb.debian.org", "", icon="globe", tsize=18))
a.add(a.text(SX + 62, SYS[0] + 52, "trixie · trixie-updates", 15, a.GREY, a.MONO))
a.add(dev(a, SX, SYS[1], SW, SH, "security.debian.org", "", icon="globe", tsize=18))
a.add(a.text(SX + 62, SYS[1] + 52, "trixie-security", 15, a.GREY, a.MONO))
at(a, dev(a, SX, SYS[2], SW, SH, "enterprise.proxmox.com", "", icon="lock", tsize=18, stroke=a.BAD) +
   a.text(SX + 62, SYS[2] + 52, "pve-enterprise · pide clave", 15, a.BAD, a.MONO), 0, 50)
at(a, dev(a, SX, SYS[2], SW, SH, "download.proxmox.com", "", icon="globe", tsize=18, stroke=a.OK) +
   a.text(SX + 62, SYS[2] + 52, "pve-no-subscription", 15, a.OK, a.MONO), 50, 100, still=1)

# cables (líneas finas fijas)
X1, X2 = HX + HW, SX
for y in SYS:
    a.add(path(f"M{X1} {HY + 50} C{X1 + 160} {HY + 50} {X2 - 160} {y + 31} {X2} {y + 31}", a.LINE, 2.5))


def curve(y, f):
    """Punto a la fracción f del cable hacia el servidor en y (Bezier cúbica)."""
    p0, p1, p2, p3 = (X1, HY + 50), (X1 + 160, HY + 50), (X2 - 160, y + 31), (X2, y + 31)
    u = 1 - f
    return (u ** 3 * p0[0] + 3 * u * u * f * p1[0] + 3 * u * f * f * p2[0] + f ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * f * p1[1] + 3 * u * f * f * p2[1] + f ** 3 * p3[1])


def ida(y, t0, t1, label="GET InRelease", color=None):
    go(a, label, [curve(y, f / 10) for f in range(1, 10)], t0, t1, color or a.BLUE, hold=0.6)


def vuelta(y, t0, t1, label, color):
    go(a, label, [curve(y, f / 10) for f in range(9, 2, -1)], t0, t1, color, hold=2.5)


# 1 · Debian contesta
ida(SYS[0], 2, 6)
vuelta(SYS[0], 7, 11, "200 · firmado", a.OK)
ida(SYS[1], 9, 13)
vuelta(SYS[1], 14, 18, "200 · firmado", a.OK)
at(a, chip(a, HX + 20, HY + 112, "firma OK · debian-archive-keyring", "ok"), 12, 25)
# 2 · enterprise sin clave
ida(SYS[2], 28, 33)
vuelta(SYS[2], 34, 39, "401 Unauthorized", a.BAD)
at(a, xmark(a, SX - 26, SYS[2] + 31), 34, 50)
at(a, chip(a, HX + 20, HY + 112, "sin clave de suscripción", "bad"), 38, 50)
# 3 · no-subscription
ida(SYS[2], 53, 58)
vuelta(SYS[2], 59, 64, "200 · firmado", a.OK)
at(a, chip(a, HX + 20, HY + 112, "firma OK · proxmox-archive-keyring", "ok"), 62, 75, still=1)
# 4 · full-upgrade
ida(SYS[2], 77, 81, "GET .deb", a.BLUE)
vuelta(SYS[2], 81, 86, "pve-manager", a.CYAN)
ida(SYS[0], 79, 83, "GET .deb", a.BLUE)
vuelta(SYS[0], 83, 88, "paquetes base", a.CYAN)
at(a, chip(a, HX + 20, HY + 112, "pve-manager 9.2.3 · a la ficha", "info"), 88, 100)

# ---------- terminal (abajo, ancho completo)
TX, TY, TW, TH = 48, 404, 1104, 206
a.add(a.box(TX, TY, TW, TH, a.INK, rx=14))
a.add(a.text(TX + 20, TY + 28, "TERMINAL DE PVE1", 13, SKY, a.MONO, 400, extra='letter-spacing="1.8"'))
L = [TY + 58 + i * 26 for i in range(6)]
at(a, tline(a, TX + 20, L[0], "# apt update", MINT), 0, 75, still=1)
at(a, tline(a, TX + 20, L[1], "Hit:1 http://deb.debian.org/debian trixie InRelease"), 8, 75, still=1)
at(a, tline(a, TX + 20, L[2], "Hit:2 http://deb.debian.org/debian trixie-updates InRelease"), 10, 75, still=1)
at(a, tline(a, TX + 20, L[3], "Hit:3 http://security.debian.org/debian-security trixie-security InRelease"), 15, 75, still=1)
at(a, tline(a, TX + 20, L[4], "Err:4 https://enterprise.proxmox.com/debian/pve trixie InRelease", CORAL), 35, 50)
at(a, tline(a, TX + 20, L[5], "  401  Unauthorized", CORAL), 36, 50)
at(a, tline(a, TX + 20, L[4], "Get:4 http://download.proxmox.com/debian/pve trixie InRelease", MINT), 60, 75, still=1)
at(a, tline(a, TX + 20, L[5], "Reading package lists... Done", SKY), 63, 75, still=1)
# paso 4
at(a, tline(a, TX + 20, L[0], "# apt full-upgrade", MINT), 75, 100)
at(a, tline(a, TX + 20, L[1], "Get:1 http://download.proxmox.com/debian/pve trixie/pve-no-subscription ... pve-manager"), 82, 100)
at(a, tline(a, TX + 20, L[2], "Get:2 http://deb.debian.org/debian trixie/main ..."), 85, 100)
at(a, tline(a, TX + 20, L[3], "# pveversion -v | head -3", MINT), 89, 100)
at(a, tline(a, TX + 20, L[4], "proxmox-ve: ... (running kernel: ...)", SKY), 91, 100)
at(a, tline(a, TX + 20, L[5], "pve-manager: 9.2.3 (running version: 9.2.3/...)"), 92, 100)

status(a, 646, [
    (0, 25, "Cada bloque de los .sources es una pregunta: el InRelease firmado dice qué paquetes hay.", a.INK, 0),
    (25, 50, "El 401 no es un problema de red: enterprise solo contesta a hosts con suscripción.", a.BAD, 0),
    (50, 75, "Un solo repositorio de Proxmox habilitado, más los de Debian: apt update sin errores.", a.OK, 1),
    (75, 100, "Los paquetes vienen de los mismos servidores; full-upgrade deja todo en una versión.", a.BLUE, 0),
])

write(a, 1, "r1", "Quién contesta cada línea de apt update",
      "Animación en cuatro tiempos con el host pve1 recién instalado, tres servidores de paquetes y la terminal. "
      "1: apt update pide el archivo InRelease a cada repositorio de los .sources; deb.debian.org (trixie y trixie-updates) y security.debian.org (trixie-security) contestan con su InRelease firmado, apt verifica la firma con debian-archive-keyring y la terminal muestra Hit:1, Hit:2 y Hit:3. "
      "2: enterprise.proxmox.com, el repositorio pve-enterprise que viene habilitado, pide la clave de suscripción; sin clave contesta 401 Unauthorized y la terminal muestra Err:4 con 401 Unauthorized. "
      "3: con enterprise en Enabled: no y el archivo proxmox.sources con pve-no-subscription, contesta download.proxmox.com, la firma se verifica con proxmox-archive-keyring y apt update termina sin errores. "
      "4: apt full-upgrade baja pve-manager de download.proxmox.com y los paquetes base de deb.debian.org; pveversion -v muestra pve-manager 9.2.3 y ese dato va a la ficha del cliente.",
      [8, 22, 40, 66, 92])
