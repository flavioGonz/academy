import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/linux/src")
from _lnx import *

# ---------------------------------------------------------------- 10.svg: available, no free
c = new(None, "free -h: la columna que importa es available")
svg, h = term(48, 124, 1104, ["$ free -h",
                              ("               total     used     free   shared  buff/cache available", T_COM),
                              ("Mem:           7,8Gi    2,1Gi    0,9Gi    40Mi       4,8Gi      5,4Gi", "#FFFFFF"),
                              ("Swap:          2,0Gi       0B    2,0Gi", T_OUT)], "TERMINAL · EJEMPLO", size=17, lh=30)
c.add(svg)
cw = 17 * 0.6
X = 64
yl = 124 + 32 + 4 + 2.6 * 30
c.add(f'<rect x="{X + cw * 33 - 4}" y="{yl - 23}" width="{cw * 5 + 8}" height="31" rx="6" fill="none" stroke="{T_ERR}" stroke-width="2.5"/>')
c.add(f'<rect x="{X + cw * 64 - 4}" y="{yl - 23}" width="{cw * 5 + 8}" height="31" rx="6" fill="none" stroke="{T_OK}" stroke-width="2.5"/>')
# barra de memoria
y = 330
c.add(text(48, y - 14, "Los 7,8 GB de RAM, por dentro", 19, 600, INK, FD))
W = 1104
parts = [("usada por programas", 2.1, BLUE, WHITE), ("caché de disco (buff/cache)", 4.8, "#9FD3EA", INK), ("libre", 0.9, WHITE, INK2)]
x = 48
tot = 7.8
for lb, v, col, tc in parts:
    w = W * v / tot
    c.add(rect(x, y, w, 70, col, BLUE if col == WHITE else col, rx=8))
    c.add(mid(x + w / 2, y + 32, lb, 16, 600, tc, FB))
    c.add(mid(x + w / 2, y + 56, f"{v:.1f} GB".replace(".", ","), 15, 600, tc, FM))
    x += w
xa = 48 + W * 2.1 / tot + W * 0.3 / tot
c.add(f'<path d="M{xa} {y + 86}V{y + 100}H{48 + W}V{y + 86}" fill="none" stroke="{OK}" stroke-width="3"/>')
c.add(mid((xa + 48 + W) / 2, y + 126, "available ≈ 5,4 GB: lo que se le puede dar a un programa sin ir a swap", 17, 600, OK, FB))
c.add(Note(48, 494, 540, "free bajo es normal: Linux usa la RAM que sobra como caché y la suelta apenas un programa la pide.", title="free bajo no es un problema", kind="ok"))
c.add(Note(612, 494, 540, "Muchas herramientas de monitoreo alertan mirando free: un servidor sano puede figurar en presión de memoria.", title="Ojo con las alertas", kind="warn"))
save(c, "10.svg")

# ---------------------------------------------------------------- 10-paso1: carga contra núcleos
c = new(1, "La carga se compara con la cantidad de núcleos")
svg, h = term(48, 124, 700, ["$ uptime", (" 10:42:07 up 153 days,  2 users,  load average: 0,52, 0,61, 0,70", "#FFFFFF"),
                             "$ nproc", ("4", "#FFFFFF")], "TERMINAL · EJEMPLO", size=15, lh=30)
c.add(svg)
c.add(Note(776, 124, 376, "Los tres números son promedios de 1, 5 y 15 minutos: procesos corriendo o esperando turno.", title="load average", kind="info"))
y = 330
c.add(text(48, y, "Con 4 núcleos", 19, 600, INK, FD))
scale = [(0, 4, OK_BG, OK, "por debajo de 4: hay lugar"), (4, 6, WARN_BG, WARN, "cerca o arriba de 4: llena"), (6, 8, ALERT_BG, ALERT, "sostenida arriba: saturación")]
X0, SW = 48, 1104 / 8
for a0, a1, bg, fg, lb in scale:
    c.add(rect(X0 + a0 * SW, y + 24, (a1 - a0) * SW, 64, bg, fg, rx=8))
    c.add(mid(X0 + (a0 + a1) / 2 * SW, y + 62, lb, 16, 600, fg, FB))
for k in range(9):
    c.add(mid(X0 + k * SW, y + 116, str(k), 16, 600, INK3, FM))
for v, lab in [(0.52, "1 min"), (0.70, "15 min")]:
    xx = X0 + v * SW
    c.add(f'<path d="M{xx} {y + 14}V{y + 96}" stroke="{INK}" stroke-width="3"/>')
c.add(text(X0, y + 150, "Las rayas son 0,52 (1 min) y 0,70 (15 min): tranquilo.", 16, 700, INK, FB))
c.add(box(48, 500, 540, 110, "Carga alta y available bajo", ["Falta memoria o un proceso se la come:", "top con Shift+M para ver quién."], kind="warn"))
c.add(box(612, 500, 540, 110, "Carga alta y available alto", ["Es CPU o disco, no RAM:", "top con Shift+P ordena por CPU."], kind="info"))
save(c, "10-paso1.svg")

# ---------------------------------------------------------------- 10-paso3: señales con un proceso de prueba
c = new(3, "Terminar un proceso: primero se pide, después se fuerza")
svg, h = term(48, 124, 560, ["$ sleep 600 &", ("[1] 12345", "#FFFFFF"), "$ pgrep -a sleep", ("12345 sleep 600", "#FFFFFF"),
                             "$ kill 12345", "$ pgrep -a sleep", ("(nada: terminó)", T_OK)], "TERMINAL · EJEMPLO", size=16, lh=30)
c.add(svg)
c.add(text(64 + 16 * 0.6 * 18, 124 + 32 + 4 + 3.6 * 30, "<- el PID para kill", 16, 600, T_WARN, FM))
c.add(text(640, 150, "De menos a más, según quién consume", 19, 600, INK, FD))
lad = [("systemctl restart servicio", "Si es un servicio: systemd lo baja y lo levanta.", "ok"),
       ("kill PID", "SIGTERM (15): le pide terminar; cierra y guarda.", "info"),
       ("kill -9 PID", "SIGKILL: el kernel lo saca; nada se guarda. Último recurso.", "alert")]
for i, (cmd, d, k) in enumerate(lad):
    y = 176 + i * 132
    bg, fg = {"ok": (OK_BG, OK), "info": (WHITE, BLUE), "alert": (ALERT_BG, ALERT)}[k]
    c.add(rect(640, y, 512, 112, bg, fg if k != "info" else LINE2, rx=14))
    c.add(text(664, y + 40, cmd, 19, 700, fg, FM))
    svg, _ = wrap(664, y + 74, d, 464, 16, 400, INK2)
    c.add(svg)
c.add(Note(48, 440, 560, "El & deja el sleep corriendo en segundo plano y te devuelve la terminal: así lo practicás sin riesgo.", kind="info"))
save(c, "10-paso3.svg")
