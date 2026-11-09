"""Caso de estudio · Cuelga y no corta (id 23): ilustración principal y pasos 1 y 4.

Caso armado para enseñar (sin datos de clientes): comercio con UCM6304A, dos líneas de Antel por FXO y dos vendedores
con teléfono en la casa. Dos mundos con el mismo síntoma: en FXO la UCM no detecta el corte (lección Tonos y corte);
en SIP el BYE no llega (NAT del router del remoto). Redes de seguridad: RTP Timeout, Session Timer, máximos de llamada.
Campos del manual del UCM630x vigente y del GXV3350. Datos de ejemplo.
"""
import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _gs import *


def KC(paso=None):
    return "Grandstream · Caso de estudio" + (f" · Paso {paso}" if paso else "")


# ---------------------------------------------------------------- 23.svg: dos mundos
c = Canvas(KC(), "Cuelga y no corta: dos mundos, dos causas")
for x, t, k in ((48, "FXO · línea de Antel", "warn"), (612, "SIP · vendedor en la casa", "alert")):
    c.add(panel(x, 118, 540, 400, t, k, title_size=20))
# FXO
c.add(Generic(68, 170, "Línea de Antel", "el cliente colgó", icon="phone", w=230))
c.add(Generic(348, 170, "UCM · FXO1", "troncal tomada", icon="server", w=220, dark=True))
c.add(arrow((298, 212), (342, 212), kind="flow"))
c.add(text(68, 316, "Por el par llega ocupado de 425 Hz, polaridad o", 16, 400, INK2, FB))
c.add(text(68, 340, "corte de corriente, y la UCM no lo reconoce.", 16, 400, INK2, FB))
lst, _ = bullet_list(68, 384, [("La interna queda con el tu tu tu", "warn"), "Arreglo: tonos de Uruguay, Busy Detection, PSTN Detection",
                               ("Red: Maximum Call Duration y Max Message Length", "ok")], 500, size=16, gap=10)
c.add(lst)
# SIP
c.add(Generic(632, 170, "UCM", "manda el BYE", icon="server", w=190, dark=True))
c.add(Generic(942, 170, "Teléfono", "no cortó", icon="phone", w=190))
c.add(f'<path d="M822 212H862" stroke="{BLUE}" stroke-width="3"/>')
c.add(f'<path d="M902 212H936" stroke="{ALERT}" stroke-width="3" stroke-dasharray="6 5"/>')
c.add(Mark(882, 212, ok=False))
c.add(pill(882, 276, "router: NAT vencido", ALERT, ALERT_BG, size=14))
c.add(text(842, 200, "BYE", 14, 600, BLUE, FM, anchor="middle"))
c.add(text(632, 316, "El corte se manda, pero el BYE no llega: el router", 16, 400, INK2, FB))
c.add(text(632, 340, "se olvidó del puerto, o el Contact tiene otra IP.", 16, 400, INK2, FB))
lst, _ = bullet_list(632, 384, [("El teléfono corta solo a los 30 s: su RTP timeout", "alert"), "Arreglo: Enable Keep-alive y NAT en la extensión",
                                ("Red: RTP Timeout y Session Timer en la UCM", "ok")], 500, size=16, gap=10)
c.add(lst)
c.add(Note(48, 540, 1104, "El CDR y Active Calls dicen por dónde entró la llamada colgada: eso separa los mundos antes de tocar un solo campo.", kind="info", size=17))
save(c, "23.svg")

# ---------------------------------------------------------------- 23-paso1: separar los mundos
c = Canvas(KC(1), "Separar los mundos con el CDR y Active Calls")
rows = [["1001 y un celular", "Antel_Linea1 · FXO1", "ocupado 425 Hz", "FXO"],
        ["1001 y 1002", "extensión remota 1002", "silencio", "SIP"],
        ["portero 8001 y 6000", "extensión del GDS", "calle", "portero"]]
c.add(Table(48, 124, ["Llamada colgada", "Por dónde entró", "Qué se oye", "Mundo"], rows, [300, 340, 260, 204], row_h=52, mono_cols=(1,)))
c.add(Step(48, 124, 1))
c.add(panel(48, 352, 540, 196, "¿Cuánto dura lo colgado?", "info", title_size=19))
lst, _ = bullet_list(68, 410, [("Siempre lo mismo: corta un timer, no el BYE", "warn"), "30 s: RTP timeout de un GXV3350", "1800 s: Session Expiration de la UCM",
                               "Cualquier cosa: no lo corta nadie"], 500, size=16, gap=8)
c.add(lst)
c.add(panel(612, 352, 540, 196, "System Status > Active Calls", "info", title_size=19))
for i, (lab, col, d) in enumerate((("gris", LINE2, "menos de media hora"), ("naranja", WARN, "de media hora a una hora"), ("roja", ALERT, "más de una hora: puede ser anormal"))):
    y = 404 + i * 40
    c.add(f'<rect x="632" y="{y}" width="64" height="26" rx="6" fill="{col}"/>')
    c.add(text(712, y + 19, f"{lab}: {d}", 16, 400, INK2, FB))
c.add(text(632, 534, "Desde ahí se ve la troncal o la extensión y se puede colgar.", 15, 400, INK3, FB))
c.add(text(48, 590, "Ejemplo armado para la lección: números e internos de ejemplo.", 15, 400, INK3, FB))
save(c, "23-paso1.svg")

# ---------------------------------------------------------------- 23-paso4: la red de seguridad
c = Canvas(KC(4), "La red de seguridad, puesta y probada")
c.add(Window(48, 124, 540, 196, "UCM · ToS", path="PBX Settings > SIP Settings > ToS",
             rows=[("RTP Timeout", "60   (sin timeout de fábrica)"), ("RTP Hold Timeout", "300  (más largo)")], hl=0))
c.add(Window(612, 124, 540, 196, "UCM · Session Timer", path="PBX Settings > SIP Settings > Session Timer",
             rows=[("Timer", "Sí (de fábrica)"), ("Session Expiration (s)", "1800"), ("Min SE (s)", "90")], hl=None))
c.add(Step(48, 124, 4))
# línea de tiempo: el teléfono que desaparece
X0, PX = 220, 900 / 120
c.add(text(48, 372, "Teléfono desenchufado en plena llamada (segundos)", 17, 600, INK, FB))
c.add(text(48, 424, "Sin RTP Timeout", 16, 600, INK, FB))
c.add(f'<rect x="{X0}" y="402" width="{120 * PX:.0f}" height="34" rx="8" fill="{ALERT}" opacity=".85"/>')
c.add(text(X0 + 16, 425, "silencio hasta que alguien cuelga", 15, 600, WHITE, FB))
c.add(text(48, 484, "RTP Timeout 60", 16, 600, INK, FB))
c.add(f'<rect x="{X0}" y="462" width="{60 * PX:.0f}" height="34" rx="8" fill="{LINE2}"/>')
c.add(text(X0 + 16, 485, "silencio", 15, 600, INK2, FB))
c.add(f'<rect x="{X0 + 60 * PX + 4:.0f}" y="462" width="150" height="34" rx="8" fill="{OK}"/>')
c.add(text(X0 + 60 * PX + 79, 485, "la UCM corta", 15, 600, WHITE, FB, anchor="middle"))
for s in (0, 30, 60, 90, 120):
    x = X0 + s * PX
    c.add(f'<path d="M{x:.0f} 506V514" stroke="{INK3}" stroke-width="1.5"/>')
    c.add(text(x, 534, str(s), 14, 500, INK3, FM, anchor="middle"))
c.add(Note(48, 560, 1104, "RTP Timeout corta también a los equipos que dejan de mandar audio en mute: probalo con los teléfonos y la troncal del cliente. Session Timer solo actúa si el otro lado lo negocia.", kind="warn", size=16))
save(c, "23-paso4.svg")
