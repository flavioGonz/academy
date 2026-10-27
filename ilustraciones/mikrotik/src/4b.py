"""Lección 4 (versión ampliada, octubre 2026) · Input y forward: pasos 2, 4 y 9.

La principal 4.svg (hecha a mano) se mantiene. Usa tools/ilus.py y los ayudantes de _mt.py, sin modificarlos.
Regenerar:
  python3 /home/claude/ies-training/ilustraciones/mikrotik/src/4b.py
  python3 /home/claude/ies-training/tools/render_svg.py /home/claude/ies-training/ilustraciones/mikrotik/4-paso2.svg ...
"""
import sys
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/mikrotik/src")
from _mt import *  # noqa: F401,F403
from _mt import rect, line, text, wrap, rows, caption, code, save, arrow, mark, pill, GRAY_T, CYAN_T, AMBER_T, GREEN_T, RED_T

K = "MikroTik · Lección 4"


def stage(x, y, w, h, title, lines, hl_line=None, kind="dark"):
    """Etapa del camino del paquete: caja oscura con título y líneas mono."""
    out = [rect(x, y, w, h, DEEP if kind == "dark" else WHITE, DEEP if kind == "dark" else LINE2, 2, 16),
           text(x + 18, y + 32, title, 19, 600, WHITE if kind == "dark" else INK, FD)]
    for i, s in enumerate(lines):
        col = AMBER_T if i == hl_line else (GRAY_T if kind == "dark" else INK2)
        out.append(text(x + 18, y + 60 + i * 24, s, 15, 600 if i == hl_line else 500, col, FM))
    return "".join(out)


def chainbox(x, y, w, h, name, sub, color):
    return (rect(x, y, w, h, WHITE, color, 3, 16)
            + text(x + w / 2, y + h / 2 - 2, name, 22, 700, color, FM, anchor="middle")
            + text(x + w / 2, y + h / 2 + 22, sub, 15, 400, INK3, FB, anchor="middle"))


# ------------------------------------------------------------------ paso 2: el camino del paquete
c = Canvas(K + " · paso 2", "¿Por qué cadena pasa cada paquete?")
# entrada
c.add(rect(48, 300, 140, 84, WHITE, LINE2, 2, 14))
c.add(text(118, 336, "entra por", 15, 500, INK3, FB, anchor="middle"))
c.add(text(118, 362, "una interfaz", 15, 600, INK, FB, anchor="middle"))
# prerouting
c.add(stage(222, 272, 230, 140, "prerouting", ["raw", "connection tracking", "dst-nat"], hl_line=2))
# decisión
c.add(rect(486, 278, 170, 128, SOFT, BLUE, 2, 16))
c.add(text(571, 310, "decisión", 17, 600, INK, FD, anchor="middle"))
c.add(text(571, 332, "de ruteo", 17, 600, INK, FD, anchor="middle"))
c.add(text(571, 364, "¿el destino es", 15, 500, INK2, FB, anchor="middle"))
c.add(text(571, 386, "IP del router?", 15, 500, INK2, FB, anchor="middle"))
# input / forward
c.add(chainbox(700, 140, 190, 92, "input", "filter: al router", BLUE))
c.add(chainbox(700, 470, 190, 92, "forward", "filter: pasa a través", CYAN))
# router y output
c.add(rect(932, 140, 220, 92, DEEP, DEEP, 2, 16))
c.add(text(1042, 178, "el router", 19, 600, WHITE, FD, anchor="middle"))
c.add(text(1042, 204, "WinBox · DNS · ping", 15, 500, GRAY_T, FM, anchor="middle"))
c.add(chainbox(932, 296, 220, 84, "output", "lo que genera el router", NAVY))
c.add(stage(932, 448, 220, 118, "postrouting", ["src-nat", "(masquerade)", "y sale"], hl_line=0))
# flechas
c.add(arrow((188, 342), (222, 342)))
c.add(arrow((452, 342), (486, 342)))
c.add(arrow((600, 278), (700, 190), label="sí", kind="flow", label_at=0.78))
c.add(arrow((600, 406), (700, 512), label="no", kind="flow", label_at=0.78))
c.add(arrow((890, 186), (932, 186)))
c.add(arrow((1042, 232), (1042, 296)))
c.add(arrow((1042, 380), (1042, 448)))
c.add(arrow((890, 516), (932, 516)))
# nota dst-nat
c.add(Note(48, 128, 560, "El dst-nat cambia el destino antes de la decisión: un port forwarding hacia el NVR cae en forward, nunca en input.", kind="warn", size=15))
# ejemplos del laboratorio
y0 = 600
for i, (s, k) in enumerate([("ping 192.168.88.1 → input", "blue"), ("ping 1.1.1.1 → forward", "cyan"), ("/ping desde el router → output", "dark")]):
    c.add(pill([48, 380, 700][i], y0 + 20, s, k, anchor="start"))
save(c, "4-paso2.svg")


# ------------------------------------------------------------------ paso 4: cadena propia con jump
c = Canvas(K + " · paso 4", "Una cadena propia para la gestión desde WAN")
c.add(caption(48, 150, "chain=input · de arriba abajo"))
c.add(rows(48, 166, 560, [
    ("accept established,related,untracked", "plain"),
    ("drop invalid", "plain"),
    ("accept ICMP", "plain"),
    ("jump gestion-wan · WAN tcp 22,8291", "hl"),
    ("drop all not coming from LAN", "alert"),
], h=40, gap=10, size=15))
c.add(caption(700, 150, "chain=gestion-wan"))
c.add(rect(690, 166, 462, 160, WHITE, CYAN, 2, 16))
c.add(rows(706, 184, 430, [
    ("accept src-address-list=admins", "ok"),
    ("drop log-prefix=GESTION-WAN", "alert"),
], h=40, gap=12, size=15))
c.add(text(706, 304, "si ninguna decide: vuelve a input", 15, 500, INK3, FB))
c.add(arrow((608, 336), (690, 246), label="jump", kind="flow"))
c.add(Cable((690, 296), (608, 386), kind="logical", arrow=True))
# resultados
c.add(rect(48, 440, 520, 84, OK_BG, OK, 2, 14))
c.add(mark(86, 482, True))
c.add(text(120, 474, "203.0.113.25 (en admins)", 17, 600, INK, FM))
c.add(text(120, 500, "entra por WinBox", 15, 500, OK, FB))
c.add(rect(48, 540, 520, 84, ALERT_BG, ALERT, 2, 14))
c.add(mark(86, 582, False))
c.add(text(120, 574, "198.51.100.7 (fuera de la lista)", 17, 600, INK, FM))
c.add(text(120, 600, "queda en el log y se descarta", 15, 500, ALERT, FB))
t, _ = code(620, 440, 532, [
    '/log/print where message~"GESTION-WAN"',
    ("GESTION-WAN input: in:ether1 ...", AMBER_T),
    ("proto TCP (SYN), 198.51.100.7:51234", AMBER_T),
    ("->203.0.113.10:8291", AMBER_T),
], title="TERMINAL", lh=28)
c.add(t)
save(c, "4-paso4.svg")


# ------------------------------------------------------------------ paso 9: contadores y orden
c = Canvas(K + " · paso 9", "El contador dice qué regla se lleva el tráfico")
t, _ = code(48, 128, 1104, ['/ip/firewall/filter/print stats where chain=forward   (números de ejemplo)'], title="TERMINAL", lh=28)
c.add(t)


def stats_table(x, y, title, title_col, data):
    out = [text(x, y, title, 19, 600, title_col, FD)]
    tb, _ = ctable(x, y + 16, ["regla", "acción", "paquetes"], data, [250, 140, 128], row_h=46,
                   col_fonts=[FM, FM, FM], size=15)
    out.append(tb)
    return "".join(out)


c.add(stats_table(48, 248, "Bien ordenado", OK, [
    ["lab: NVR a NTP", "accept", ("12", OK)],
    ["lab: NVR a su nube", "accept", ("340", OK)],
    ["lab: NVR resto", "reject", ("25", WARN)],
]))
c.add(stats_table(634, 248, "Reject arriba (error a propósito)", ALERT, [
    ["lab: NVR resto", "reject", ("377", ALERT)],
    ["lab: NVR a NTP", "accept", ("0", ALERT)],
    ["lab: NVR a su nube", "accept", ("0", ALERT)],
]))
c.add(Note(48, 492, 520, "Manda la primera regla que coincide: la de abajo queda en 0 aunque esté bien escrita. move la devuelve a su lugar.", title="Contador en 0", kind="alert", size=15))
c.add(Note(634, 492, 518, "Si no sube ninguna, el tráfico no llega: mirá con Torch (mientras corre, FastTrack se apaga).", title="¿Llega el paquete?", kind="info", size=15))
save(c, "4-paso9.svg")
