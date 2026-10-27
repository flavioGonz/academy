import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-lpr/src")
from _lpr import *

# ---------------------------------------------------------------- 7.svg: el Monitor LPR, esquemático
c = Canvas(K(), "Monitor LPR: entradas, foco y salidas")
c.add(f'<rect x="48" y="122" width="1104" height="530" rx="16" fill="{WHITE}" stroke="{LINE2}" stroke-width="2"/>')
c.add(f'<path d="M48 186H1152" stroke="{LINE}" stroke-width="1.5"/>')
c.add(text(68, 162, "Monitor LPR", 19, 700, INK, FD))
c.add(f'<rect x="200" y="138" width="236" height="34" rx="8" fill="{GROUND}" stroke="{LINE2}"/>')
c.add(text(212, 161, "Buscar matrícula e investigar...", 15, 400, INK3, FB))
c.add(pill(452, 162, "En casa 212/240", fg=BLUE, size=15, anchor="start"))
c.add(pill(621, 162, "Hoy 1304", fg=INK2, size=15, anchor="start"))
c.add(tag(727, 162, "1190", "ok", size=15))
c.add(tag(797, 162, "114", "alert", size=15))
c.add(pill(870, 162, "Todos · Permitidos · Denegados", fg=INK2, size=14, mono=False, anchor="start"))
cols = [(64, "ENTRADAS"), (432, "FOCO"), (800, "SALIDAS")]
for x, t in cols:
    c.add(text(x, 214, t, 14, 700, INK3, FM, ls=1.5))
c.add(card(64, 228, 336, 96, "ok", "AUTORIZADO", "SBA 1234", "P1 - Entrada (21)"))
c.add(card(64, 336, 336, 96, "warn", "DENEGADO", "SCD 5678", "verificar con el residente"))
c.add(card(64, 444, 336, 96, "yellow", "SIN LECTURA", "sin chapa", "Cargar matrícula"))
# foco
c.add(f'<rect x="432" y="228" width="336" height="250" rx="14" fill="#14222F"/>')
c.add(plate(600, 270, "SBA 1234", w=220, size=30))
c.add(text(600, 380, "auto · blanco · P1 - Entrada (21)", 15, 500, "#C2D4E6", FM, anchor="middle"))
c.add(text(600, 406, "hace 2 s", 15, 500, "#9FC3E3", FM, anchor="middle"))
c.add(pill(530, 452, "Investigar", fg=CYAN, bg="#14222F", mono=False, size=16))
c.add(pill(670, 452, "Registrar", fg=OK, bg="#14222F", mono=False, size=16))
c.add(text(432, 512, "Capturas recientes debajo del foco", 15, 500, INK3, FB))
c.add(card(800, 228, 336, 96, "ok", "AUTORIZADO", "SBB 4321", "P2 - Salida (22)"))
c.add(card(800, 336, 336, 96, "alert", "LISTA NEGRA", "SAB 2024", "suena hasta abrir el evento"))
c.add(text(68, 620, "Verde pasa · ámbar se verifica · rojo con sonido es la alarma real · amarillo: la cámara vio el auto pero no leyó", 16, 500, INK2, FB))
save(c, "7.svg")

# ---------------------------------------------------------------- 7-paso3: qué hace el guardia con cada color
c = Canvas(K(3), "Qué hacés con cada tarjeta")
rows = [("ok", "AUTORIZADO", "SBA 1234", "Nada. Pasa solo si la barrera está automatizada."),
        ("warn", "DENEGADO", "SCD 5678", "Verificás con el residente antes de abrir. Casi siempre es una visita o un auto nuevo."),
        ("alert", "LISTA NEGRA", "SAB 2024", "Mirás el recorte y seguís el protocolo del cliente. No se abre por las dudas."),
        ("yellow", "SIN LECTURA", "sin chapa", "Mirás la foto. Si la patente se ve, Cargar matrícula y el servidor vuelve a decidir.")]
for i, (kd, lbl, pl, act) in enumerate(rows):
    y = 128 + i * 124
    c.add(card(48, y, 400, 104, kd, lbl, pl))
    lst, _ = wrap(480, y + 44, act, 660, 18, 500, INK)
    c.add(lst)
save(c, "7-paso3.svg")

# ---------------------------------------------------------------- 7-paso6: cargar a mano una sin lectura
c = Canvas(K(6), "Cargá a mano la patente de una lectura sin chapa")
c.add(card(48, 150, 330, 104, "yellow", "SIN LECTURA", "sin chapa", "P1 - Entrada (21)"))
w = c.add(Window(440, 132, 330, 210, "Cargar matrícula", rows=[("Matrícula", "SBA1234")], hl=0))
c.add(text(460, 260, "sin espacios ni guiones", 15, 500, INK3, FM))
c.add(pill(605, 312, "Listo", fg=OK, mono=False, size=16))
c.add(Arrow((378, 202), (436, 202)))
c.add(panel(832, 132, 320, 210, "El servidor re-evalúa", "info"))
for i, s in enumerate(["¿es de un residente?", "decisión nueva", "¿está en vigilancia?"]):
    c.add(text(852, 200 + i * 34, "· " + s, 17, 500, INK2, FB))
c.add(Arrow((770, 236), (828, 236)))
c.add(card(48, 400, 520, 104, "ok", "AUTORIZADO", "SBA 1234", "Residente · Lote 99 (prueba)"))
c.add(card(632, 400, 520, 104, "warn", "DENEGADO", "SCD 5678", "La matrícula no figura registrada"))
c.add(Note(48, 540, 1104, "Una matrícula que se lee mal siempre igual no se corrige una por una: se avisa al técnico con el nombre exacto de la cámara.", kind="info", size=16))
save(c, "7-paso6.svg")
