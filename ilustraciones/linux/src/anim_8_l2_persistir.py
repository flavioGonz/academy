#!/usr/bin/env python3
"""Lección 8 · Laboratorio, paso 3: /etc/nftables.conf, nft -c -f y systemctl enable nftables.
nft -c -f valida sin aplicar; enable engancha nftables.service al arranque; restart carga el archivo en el kernel;
una regla agregada en vivo con nft queda solo en memoria y se pierde al reiniciar, mientras el servicio vuelve a
cargar el archivo en cada arranque. Fuentes: teoría y laboratorio de la lección (lo que se hace con nft en vivo se
pierde al reiniciar; nft -c -f; systemctl enable nftables), nft(8) (-c, -f) y el nftables.service de Debian."""
from _anims_lnx_rl import *

a = nueva(28, "LINUX · FIREWALL · LABORATORIO", "En el archivo sobrevive; en vivo, hasta el reinicio")
a.steps([
    "nft -c -f valida /etc/nftables.conf sin aplicar nada.",
    "systemctl enable nftables: el servicio queda para cada arranque.",
    "restart carga el archivo en el kernel; una regla en vivo se suma solo ahí.",
    "Reinicio: el servicio vuelve a cargar el archivo; lo hecho en vivo se perdió.",
], still=3)

# archivo
a.add(a.box(48, 170, 470, 300, a.WHITE, "#C2D4E6", rx=16) + a.text(68, 202, "/etc/nftables.conf  (en disco)", 17, a.INK, a.MONO, 700))
FL = ["table inet filter {", "  chain input {", "    type filter hook input ... policy drop;", "    ct state established,related accept",
      "    iif lo accept", "    ip saddr 10.10.10.0/24 tcp dport 22 accept", "    icmp ... · meta l4proto ipv6-icmp accept", "  }  ...", "}"]
for i, l in enumerate(FL):
    a.add(mono(a, 68, 234 + i * 25, l, 14, a.INK if i not in (2,) else a.BAD, 600))
en(a, a.box(44, 166, 478, 308, "none", a.OK, rx=18, sw=3) + a.pill(330, 430, "válido: sin errores", a.OK, a.OKBG, 14, 28), 4, 25)

# servicio
a.add(a.box(48, 488, 470, 52, a.SLATE, None, rx=12) + mono(a, 66, 520, "nftables.service", 16, a.INK, 700))
en(a, a.pill(250, 500, "disabled", a.AMB, a.AMBBG, 15, 30), 0, 28)
en(a, a.pill(250, 500, "enabled: corre al arrancar", a.OK, a.OKBG, 15, 30), 28, 100, still=1)

# kernel
KX = 640
a.add(a.box(KX, 170, 512, 370, a.INK, None, rx=16) + a.text(KX + 20, 202, "Kernel: reglas activas (memoria)", 17, "#FFFFFF", a.HEAD, 600))
a.add(mono(a, KX + 20, 230, "$ sudo nft list ruleset", 15, T_PR, 600))
en(a, mono(a, KX + 20, 270, "(vacío: todavía no cargaste nada)", 15, LIGHT, 500), 0, 53)
KR = ["table inet filter {", "  chain input { ... policy drop;", "    ct state established,related accept", "    iif lo accept", "    ip saddr 10.10.10.0/24 tcp dport 22 accept", "    ... }", "}"]


def kernel_rules(t0, t1, still=0):
    en(a, "".join(mono(a, KX + 20, 270 + i * 26, l, 14, MINT, 600) for i, l in enumerate(KR)), t0, t1, still)


kernel_rules(54, 81)
kernel_rules(92, 100, still=1)
en(a, a.box(KX + 14, 444, 484, 54, "#3A2A0A", GOLD, rx=10, sw=2) + mono(a, KX + 28, 466, "+ tcp dport 8080 accept", 15, GOLD, 700)
   + a.text(KX + 28, 488, "agregada en vivo con nft add rule: no está en el archivo", 14, GOLD, a.SANS, 600), 64, 81)
en(a, a.box(KX + 14, 444, 484, 54, "none", CORAL, rx=10, sw=2, extra='stroke-dasharray="6 5"')
   + a.text(KX + 28, 476, "la regla en vivo del 8080 ya no está", 15, CORAL, a.SANS, 700), 92, 100, still=1)
# reinicio
en(a, a.box(KX + 14, 250, 484, 180, "#0B3A66", None, rx=10) + glyph(a, "bolt", KX + 230, 290, GOLD, 1.6)
   + a.text(KX + 256, 370, "reinicio: la memoria se vacía", 16, GOLD, a.SANS, 700, "middle"), 82, 91)
# carga archivo → kernel
for t0 in (54, 91):
    viaje(a, "nft -f", [(520, 330), (KX - 4, 330)], t0 - 4, t0, bg=a.OK, size=14, hold=0.5)

# terminal de comandos
TY = 556
a.add(tterm(a, 48, TY, 1104, 50))
def cmd(s, t0, t1, still=0, com=None):
    inner = trow(a, 48, TY + 32, s, 15)
    if com:
        inner += a.text(1136, TY + 32, com, 15, T_COM, a.MONO, 500, "end")
    en(a, inner, t0, t1, still)


cmd("$ sudo nft -c -f /etc/nftables.conf", 0, 25, 0, "# -c: solo revisa")
cmd("$ sudo systemctl enable nftables", 25, 50, 0, "# para el próximo arranque")
cmd("$ sudo systemctl restart nftables", 50, 75, 0, "# carga el archivo ahora")
cmd("$ sudo reboot", 75, 100, 1, "# al volver: nft list ruleset")

narr(a, [
    (0, 25, "Validar primero: una regla de SSH mal escrita te deja afuera.", None),
    (25, 50, "Sin enable, al primer reinicio el equipo queda sin firewall.", a.AMB),
    (50, 75, "nft list ruleset muestra lo que está activo, venga de donde venga.", None),
    (75, 100, "Lo que tiene que quedar va en /etc/nftables.conf; lo demás es una prueba.", a.OK),
], y=642, still_idx=3)

escribir(a, "8-l2", "En el archivo sobrevive; en vivo, hasta el reinicio",
         "Animación en cuatro tiempos. A la izquierda, /etc/nftables.conf en disco, con la tabla inet filter, la cadena input con policy drop y las reglas de la lección, y debajo nftables.service; a la derecha, las reglas activas en el kernel, que muestra nft list ruleset. "
         "1: sudo nft -c -f /etc/nftables.conf valida el archivo sin aplicar nada: válido, y el kernel sigue vacío. "
         "2: sudo systemctl enable nftables deja el servicio en enabled, para que corra al arrancar. "
         "3: sudo systemctl restart nftables carga el archivo en el kernel; además, una regla tcp dport 8080 accept agregada en vivo con nft add rule aparece en ámbar, solo en memoria. "
         "4: al reiniciar la memoria se vacía, nftables.service vuelve a cargar el archivo y las reglas de la lección vuelven, pero la del 8080 ya no está.",
         [10, 38, 70, 96])
