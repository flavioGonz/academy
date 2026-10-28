"""Lección 45 · Configuración de botones: ilustración principal y pasos 5, 6 y 8.
Todo sale de card.md de la lección 45 y de research/notes/g.md (Call Settings de E16, E18, E12, R20A/B, R20K,
R29 y X915; notas Configure Sequence Call y Configure Group Call; contactos de E16 y R29).
La captura real del paso 2 se arma aparte con 45_captura.py (PIL)."""
from _botones import *  # noqa
from _akv import code, panel, pill  # noqa

K = "Akuvox · Lección 45"

# ---------------------------------------------------------------- principal
c = Canvas(K, "Un botón, tres maneras de llamar")
c.add(Intercom(60, 196, "Portero E16", "botón o Recepción", screen=True))
LX, LW = 300, 860
lanes = [(124, 132, "Un destino", "IP directa o número SIP"),
         (272, 144, "Sequence Call: de a uno", "Call Timeout · When Refused"),
         (432, 144, "Group Call: todos a la vez", "When Refused")]
for (y, h, t, s) in lanes:
    c.add(lane(LX, y, LW, h, t, s))
for (y, h, _, _) in lanes:
    c.add(Arrow((214, 330), (LX - 6, y + h / 2), kind="flow"))
# carril 1
c.add(wrap(LX + 22, 124 + 86, "Direct IP: Enabled, Port 5060. Por central: la cuenta de Account > Basic.", 330, 15, 400, INK2)[0])
c.add(Arrow((700, 190), (860, 190), "una sola llamada", label_dy=-14))
c.add(dot_mon(930, 190, ".64", "ring"))
c.add(text(992, 186, "192.168.88.64", 15, 600, INK, FM))
c.add(text(992, 208, "o ext. 201", 15, 500, INK3, FM))
# carril 2
c.add(wrap(LX + 22, 272 + 86, "Rechazo: Call Next sigue con el próximo; Do Not Call Next corta.", 330, 15, 400, INK2)[0])
xs = [730, 890, 1050]
for i, x in enumerate(xs):
    c.add(dot_mon(x, 336, str(i + 1), "noanswer" if i == 0 else ("ring" if i == 1 else "idle")))
c.add(Arrow((xs[0] + 36, 336), (xs[1] - 38, 336), "20 s", label_dy=-14))
c.add(Arrow((xs[1] + 36, 336), (xs[2] - 38, 336), "20 s", label_dy=-14, kind="logical"))
c.add(text(xs[0], 386, "no atendió", 15, 600, WARN, FB, anchor="middle"))
c.add(text(xs[1], 386, "suena ahora", 15, 600, BLUE, FB, anchor="middle"))
c.add(text(xs[2], 386, "espera", 15, 600, INK3, FB, anchor="middle"))
# carril 3
c.add(wrap(LX + 22, 432 + 86, "Rechazo: End This Call Only corta solo a ese; End All Calls corta a todos.", 330, 15, 400, INK2)[0])
c.add(f'<path d="M700 466 H1100" stroke="{CYAN}" stroke-width="2" stroke-dasharray="6 6"/>')
c.add(text(900, 458, "suenan a la vez", 15, 600, CYAN, FB, anchor="middle"))
for i, x in enumerate(xs):
    c.add(dot_mon(x, 504, str(i + 1), "ok" if i == 1 else "cut"))
c.add(text(xs[0], 554, "deja de sonar", 15, 600, INK3, FB, anchor="middle"))
c.add(text(xs[1], 554, "atiende", 15, 600, OK, FB, anchor="middle"))
c.add(text(xs[2], 554, "deja de sonar", 15, 600, INK3, FB, anchor="middle"))
c.add(Note(60, 596, 1100, "Todo en la web del portero: Intercom > Basic, Intercom > Dial Plan e Intercom > Call Feature. El menú cambia por modelo.", kind="info", size=15))
save(c, "45.svg")

# ---------------------------------------------------------------- paso 5
c = Canvas(K + " · Paso 5", "Secuencia en un táctil: grupo, prioridad y tiempo")
c.add(Table(60, 124, ["Usuario", "Phone", "Group", "Priority of Call"],
            [["Living", "192.168.88.64", "Conserjeria", "Primary"], ["Cocina", "192.168.88.65", "Conserjeria", "Secondary"]],
            [130, 190, 160, 190], mono_cols=(1, 2, 3)))
c.add(text(60, 260, "Directory > User", 15, 500, BLUE, FM))
svg, h = web_panel(60, 290, 670, "Sequence Call", "Intercom > Basic > Sequence Call",
                   [("When Refused", "Call Next", "select"), ("Call Timeout (Sec)", "20", "select")], lw=220, fw=300)
c.add(svg)
c.add(Step(44, 300, 5))
# línea de tiempo a la derecha
c.add(mon_mini(800, 124, "Living", "Primary", "noanswer"))
c.add(mon_mini(800, 396, "Cocina", "Secondary", "ring"))
c.add(Arrow((900, 300), (900, 388), "20 s sin atender", label_dy=4, kind="flow"))
c.add(Note(60, 488, 520, "Con Call Next, si el living rechaza, suena la cocina enseguida.", kind="ok", size=15))
c.add(Note(60, 566, 520, "Con Do Not Call Next, el rechazo del living corta ahí: la cocina no suena.", kind="warn", size=15))
c.add(Note(1020, 140, 150, "La prioridad aparece solo con un grupo creado por vos.", kind="info", size=15))
save(c, "45-paso5.svg")

# ---------------------------------------------------------------- paso 6
c = Canvas(K + " · Paso 6", "Dial Plan: un número corto, varios destinos")
c.add(Intercom(60, 150, "Portero", "marca 100", keypad=True))
c.add(pill(135, 140, "100", BLUE, WHITE, 18))
svg, h = web_panel(300, 130, 470, "Regla de Dial Plan", "Intercom > Dial Plan > +Add",
                   [("Account", "Auto", "select"), ("Prefix", "100"), ("Replace 1", "192.168.88.64"), ("Replace 2", "192.168.88.65")],
                   lw=140, fw=270, hl=1)
c.add(svg)
c.add(Arrow((214, 280), (294, 280), kind="flow"))
c.add(mon_mini(900, 124, "Living", "192.168.88.64", "ring"))
c.add(mon_mini(900, 330, "Cocina", "192.168.88.65", "ring"))
c.add(Arrow((776, 300), (894, 190), kind="flow"))
c.add(Arrow((776, 330), (894, 396), kind="flow"))
c.add(text(838, 316, "a la vez", 15, 600, CYAN, FB, anchor="middle"))
c.add(Note(60, 520, 520, "Hasta 5 números por regla (Replace 1 a 5), IP o SIP. Reglas: 1.000 en E16 y E18, 1.500 en R29, 500 en R20K.", kind="info", size=15))
c.add(Note(620, 520, 540, "En el X915 el prefijo no acepta *. También se carga en la pantalla: Setting > Replace Rule.", kind="info", size=15))
c.add(Step(300, 120, 6))
save(c, "45-paso6.svg")

# ---------------------------------------------------------------- paso 8
c = Canvas(K + " · Paso 8", "El mismo pedido, otro menú según el portero")
rows = [["E16, E18", "táctil", "Intercom > Basic > Key Setting", "grupo + Priority of Call"],
        ["R29, X915", "táctil", "Setting > Key/Display", "grupo + Priority of Call"],
        ["R20K", "teclado", "Intercom > Basic > Speed Dial", "Manager Dial"],
        ["E12, R20A, E13", "un botón", "Intercom > Basic > Manager Dial", "Call Type: Sequence o Group"],
        ["R20B", "botones", "un número por pulsador", "Manager Dial por pulsador"]]
c.add(Table(60, 128, ["Modelo", "Frente", "Dónde va el destino", "Varios destinos"], rows, [190, 130, 410, 350], row_h=50, mono_cols=(2,)))
c.add(Note(60, 448, 530, "Grupo de los táctiles: Directory > User > Group. Rechazo y tiempo: Intercom > Basic > Sequence Call y Group Call (X915: Only Group Call Allowed).", kind="info", size=15))
c.add(Note(630, 448, 530, "E12: Direct IP está en Intercom > Call Feature. R20B y R20K suman teclas con el módulo de Device > Extension Unit (320.30.10.116 o más).", kind="info", size=15))
c.add(Note(60, 572, 1100, "Con SmartPlus, los números los carga el residente en la app: Group Call Number(Local) queda vacío y en el E12 la secuencia local no aparece.", kind="warn", size=15))
c.add(Step(44, 140, 8))
save(c, "45-paso8.svg")
