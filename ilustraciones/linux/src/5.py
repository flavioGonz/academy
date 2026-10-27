import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/linux/src")
from _lnx import *

# ---------------------------------------------------------------- 5.svg: start no es enable + el método
c = new(None, "start lo levanta hoy; enable, después de cada corte")
c.add(panel(48, 124, 540, 300, "Dos órdenes distintas"))
c.add(rect(72, 178, 492, 104, SOFT, CYAN, rx=12))
c.add(text(92, 212, "systemctl start ssh", 18, 700, BLUE, FM))
c.add(text(92, 240, "Lo arranca ahora. Si se corta la luz,", 16, 400, INK2, FB))
c.add(text(92, 262, "al volver no arranca solo.", 16, 400, INK2, FB))
c.add(rect(72, 296, 492, 104, OK_BG, OK, rx=12))
c.add(text(92, 330, "systemctl enable ssh", 18, 700, OK, FM))
c.add(text(92, 358, "Lo engancha al arranque (multi-user.target):", 16, 400, INK2, FB))
c.add(text(92, 380, "vuelve solo después de cada reinicio.", 16, 400, INK2, FB))
c.add(Note(48, 446, 540, "Un servicio que tiene que volver tras un corte (accesos, grabación, SSH) lleva start y enable. Se revisa con systemctl is-enabled.", kind="info"))
# método
c.add(panel(612, 124, 540, 466, "Servicio caído: el método", "ok"))
st = [("1", "systemctl status ssh", "¿activo, caído, desde cuándo?"), ("2", "journalctl -u ssh -n 20", "el error real, con archivo y línea"),
      ("3", "Arreglo", "corregís lo que dice el log"), ("4", "systemctl status ssh", "confirmás que quedó active (running)")]
for i, (n, cmd, d) in enumerate(st):
    y = 186 + i * 96
    c.add(badge(650, y + 22, n, OK if i == 3 else CYAN))
    c.add(text(684, y + 18, cmd, 18, 700, INK, FM if i != 2 else FB))
    c.add(text(684, y + 44, d, 16, 400, INK2, FB))
    if i < 3:
        c.add(vline(650, y + 44, y + 92, LINE2, 2))
c.add(text(636, 566, "Reiniciar a ciegas borra la pista: primero se lee.", 16, 600, OK, FB))
save(c, "5.svg")

# ---------------------------------------------------------------- 5-paso2: status y journal de un servicio roto
c = new(2, "Servicio roto: status dice qué, journal dice por qué")
svg, h = term(48, 124, 1104, ["$ systemctl status ssh",
                              ("● ssh.service - OpenBSD Secure Shell server", "#FFFFFF"),
                              ("     Loaded: loaded (/usr/lib/systemd/system/ssh.service; enabled)", T_OUT),
                              ("     Active: failed (Result: exit-code) since mar 2026-10-27 10:12:03", T_ERR),
                              "$ sudo journalctl -u ssh -n 20",
                              ("sshd[1188]: /etc/ssh/sshd_config.d/99-roto.conf line 1: unsupported option \"yess\".", T_WARN)],
            "TERMINAL · CONSOLA DE LA VM · EJEMPLO", size=15, lh=29)
c.add(svg)
cw = 15 * 0.6
X = 64
def ly(k): return 124 + 32 + 4 + (k + 0.6) * 29
c.add(f'<rect x="{X + cw * 58 - 3}" y="{ly(2) - 20}" width="{cw * 7 + 6}" height="27" rx="5" fill="none" stroke="{T_PR}" stroke-width="2"/>')
c.add(f'<rect x="{X + cw * 13 - 3}" y="{ly(3) - 20}" width="{cw * 6 + 6}" height="27" rx="5" fill="none" stroke="{T_ERR}" stroke-width="2"/>')
yb = 124 + h
c.add(callout(X + cw * 61, yb, 820, yb + 40, "arranca al bootear", "cyan"))
c.add(callout(X + cw * 16, yb, 200, yb + 40, "está caído", "alert"))
c.add(box(48, yb + 74, 352, 150, "Loaded", ["Si encontró la unidad y si", "está habilitada (enabled)."]))
c.add(box(424, yb + 74, 352, 150, "Active", ["active (running), inactive", "o failed, y desde cuándo."], kind="alert"))
c.add(box(800, yb + 74, 352, 150, "journalctl -u", ["El mensaje del propio sshd:", "archivo, línea y opción mala."], kind="warn"))
save(c, "5-paso2.svg")

# ---------------------------------------------------------------- 5-paso4: filtros de journalctl
c = new(4, "Filtros de journalctl para obra")
cards = [("sudo journalctl -b -1 -p err", "Errores del arranque anterior", "Qué pasó antes del corte o del reinicio."),
         ("sudo journalctl -u ssh -S \"1 hour ago\"", "Un servicio, la última hora", "Lo de esa unidad desde un momento."),
         ("sudo journalctl -f", "En vivo", "Como tail -f: ves llegar cada línea. Ctrl+C sale."),
         ("sudo du -sh /var/log/journal", "Cuánto ocupa", "El journal crece: en Disco lleno se le pone tope.")]
for i, (cmd, t, d) in enumerate(cards):
    x, y = 48 + (i % 2) * 564, 124 + (i // 2) * 166
    c.add(panel(x, y, 540, 148, t))
    c.add(code(x + 20, y + 50, 500, cmd, 15))
    c.add(text(x + 20, y + 124, d, 16, 400, INK2, FB))
# escala de prioridades
y = 470
c.add(text(48, y, "Prioridades: -p err muestra err y todo lo más grave", 18, 600, INK, FD))
pr = ["0 emerg", "1 alert", "2 crit", "3 err", "4 warning", "5 notice", "6 info", "7 debug"]
for i, p in enumerate(pr):
    x = 48 + i * 139
    on = i <= 3
    c.add(rect(x, y + 20, 128, 50, ALERT_BG if on else WHITE, ALERT if on else LINE2, rx=10))
    c.add(mid(x + 64, y + 52, p, 16, 600, ALERT if on else INK3, FM))
c.add(f'<path d="M48 {y + 84}H{48 + 4 * 139 - 11}" stroke="{ALERT}" stroke-width="3"/>')
c.add(text(48, y + 110, "lo que ves con -p err", 16, 600, ALERT, FB))
save(c, "5-paso4.svg")
