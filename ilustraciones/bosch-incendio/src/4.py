import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/bosch-incendio/src")
from _bi import *


def cut(x, y):
    return (f'<rect x="{x - 16}" y="{y - 16}" width="32" height="32" rx="8" fill="{GROUND}"/>'
            f'<path d="M{x - 11} {y - 11}L{x + 11} {y + 11}M{x + 11} {y - 11}L{x - 11} {y + 11}" stroke="{ALERT}" stroke-width="4" stroke-linecap="round"/>')


def mod(x, y, w=210, two=True, ret_open=False):
    s = rect(x, y, w, 70, DEEP, DEEP, rx=12) + text(x + 18, y + 30, "Módulo LSN", 17, 600, WHITE, FD)
    s += text(x + 30, y + 58, "LSN1", 14, 600, "#9FC3E3", FM, anchor="middle")
    if two:
        s += text(x + w - 30, y + 58, "LSN2", 14, 600, ALERT if ret_open else "#9FC3E3", FM, anchor="middle")
    return s


def det(x, y, state, lab=None, col=None):
    s = rect(x - 30, y - 30, 60, 60, GROUND, GROUND, rx=10, sw=0) + detector(x, y, 25, state=state)
    if lab:
        s += mid(x, y + 50, lab, 15, 600, col or INK2, FM)
    return s


# ---------------------------------------------------------------- 4.svg: lazo contra ramal
c = Canvas(K(), "Un corte en el cable: el lazo sigue, el ramal no")
# lazo
c.add(panel(48, 120, 540, 440, "Lazo (clase A; clase X por los aisladores)", "ok"))
c.add(mod(80, 168))
c.add(f'<path d="M110 238V470H548V280H260V238" fill="none" stroke="{BLUE}" stroke-width="4" stroke-linejoin="round"/>')
c.add(f'<path d="M110 470H395" stroke="{OK}" stroke-width="7" stroke-opacity=".35"/>')
c.add(f'<path d="M395 470H548V280H260V238" fill="none" stroke="{CYAN}" stroke-width="7" stroke-opacity=".35" stroke-linejoin="round"/>')
for x, l in [(200, "1"), (320, "2"), (470, "3")]:
    c.add(det(x, 470, "ok", l))
c.add(det(548, 375, "ok", None)); c.add(mid(548 - 44, 380, "4", 15, 600, INK2, FM))
c.add(det(400, 280, "ok", None)); c.add(mid(400, 254, "5", 15, 600, INK2, FM))
c.add(cut(395, 470))
c.add(text(72, 536, "1 y 2 quedan con LSN1; 3, 4 y 5 con LSN2. Avería, todos detectan.", 15, 600, OK))
# ramal
c.add(panel(612, 120, 540, 440, "Ramal (clase B)", "alert"))
c.add(mod(644, 168, two=False))
c.add(f'<path d="M674 238V470H1110" fill="none" stroke="{BLUE}" stroke-width="4" stroke-linejoin="round"/>')
for x, l, st in [(760, "1", "ok"), (880, "2", "ok"), (1000, "3", "off"), (1110, "4", "off")]:
    c.add(det(x, 470, st, l, ALERT if st == "off" else None))
c.add(cut(940, 470))
c.add(rect(960, 340, 180, 64, ALERT_BG, ALERT, rx=12, sw=1.5))
c.add(mid(1050, 366, "sin detección", 16, 600, ALERT))
c.add(mid(1050, 390, "detrás del corte", 15, 400, ALERT))
c.add(text(636, 536, "Se pierde todo lo que queda detrás de la falla.", 15, 600, ALERT))
c.add(text(48, 600, "Cada elemento LSN trae aislador entre b1 y b2: ante un corte o un corto, el panel parte el lazo en dos.", 17, 500, INK2))
c.add(text(48, 630, "La clase la decide el proyecto: Bosch recomienda lazo siempre que se pueda.", 17, 600, BLUE))
save(c, "4.svg")

# ---------------------------------------------------------------- 4-paso2: corte en banco
c = Canvas(K(2), "Cortá entre el 1 y el 2: los tres siguen respondiendo")
c.add(mod(470, 140, 260))
c.add(f'<path d="M500 210V330H160V470H1040V330H700V210" fill="none" stroke="{BLUE}" stroke-width="4" stroke-linejoin="round"/>')
c.add(f'<path d="M500 210V330H160V470H385" fill="none" stroke="{OK}" stroke-width="8" stroke-opacity=".3" stroke-linejoin="round"/>')
c.add(f'<path d="M455 470H1040V330H700V210" fill="none" stroke="{CYAN}" stroke-width="8" stroke-opacity=".3" stroke-linejoin="round"/>')
for x, l in [(240, "Detector 1"), (600, "Detector 2"), (900, "Detector 3")]:
    c.add(det(x, 470, "ok", l))
c.add(cut(420, 470))
c.add(text(420, 432, "conductor desconectado", 15, 600, ALERT, FB, anchor="middle"))
c.add(tag(250, 300, "alimentado por LSN1", "ok", size=14))
c.add(tag(900, 300, "alimentado por LSN2", "cyan", size=14))
c.add(rect(820, 150, 330, 92, WARN_BG, WARN, rx=14, sw=1.5))
c.add(text(842, 186, "En el panel: avería del lazo", 17, 600, WARN, FB))
c.add(text(842, 214, "anotá el mensaje tal cual", 15, 400, INK2))
c.add(Note(48, 556, 1104, "Con la zona en modo revisión, aerosol a los tres: los tres dan alarma. El lazo se partió en dos ramales, uno desde cada extremo.", title="Qué tenés que ver", kind="ok"))
save(c, "4-paso2.svg")

# ---------------------------------------------------------------- 4-paso5: retorno abierto, ahora es ramal
c = Canvas(K(5), "Sin retorno es un ramal: el mismo corte pierde dos")
c.add(mod(470, 140, 260, ret_open=True))
c.add(f'<path d="M500 210V330H160V470H1040V330H760" fill="none" stroke="{BLUE}" stroke-width="4" stroke-linejoin="round"/>')
c.add(f'<path d="M700 210V262" stroke="{BLUE}" stroke-width="4"/>')
c.add(f'<path d="M500 210V330H160V470H385" fill="none" stroke="{OK}" stroke-width="8" stroke-opacity=".3" stroke-linejoin="round"/>')
c.add(cut(730, 300))
c.add(text(760, 270, "retorno desconectado en LSN2", 15, 600, ALERT))
for x, l, st in [(240, "Detector 1", "ok"), (600, "Detector 2", "off"), (900, "Detector 3", "off")]:
    c.add(det(x, 470, st, l, ALERT if st == "off" else None))
c.add(cut(420, 470))
c.add(text(600, 420, "sin alimentación", 15, 600, ALERT, FB, anchor="middle"))
c.add(text(900, 420, "sin alimentación", 15, 600, ALERT, FB, anchor="middle"))
c.add(codebox(48, 540, 660, ["Lazo con corte:   avería, detectores activos: 3 de 3", "Ramal con corte:  avería, detectores activos: 1 de 3"], title="PASO 6: RESULTADO ESPERADO")[0])
c.add(Note(740, 540, 412, "Volvé a cerrar el lazo y reponé. En obra real, abrir el lazo pide aviso al monitoreo.", title="Paso 7", kind="warn"))
save(c, "4-paso5.svg")

# ---------------------------------------------------------------- 4-t2: el ramal de un elemento no aísla (teoría, fija)
c = Canvas("Bosch Incendio · Aisladores", "Un ramal de un elemento no aísla nada")
c.add(f'<path d="M80 300H1120" stroke="{BLUE}" stroke-width="4"/>')
for x in (200, 1000):
    c.add(rect(x - 60, 260, 120, 80, WHITE, OK, rx=12, sw=2.5))
    c.add(iso(x - 17, 300, True))
    c.add(mid(x, 365, "aísla", 15, 600, OK))
for x in (420, 600, 780):
    c.add(f'<path d="M{x} 300V420" stroke="{BLUE}" stroke-width="4"/>')
    c.add(rect(x - 30, 420, 60, 60, GROUND, GROUND, rx=8, sw=0))
    c.add(detector(x, 450, 26))
    c.add(text(x + 34, 418, "solo b1", 14, 600, INK3, FM))
c.add(rect(260, 230, 680, 290, "none", WARN, rx=18, sw=2.5, dash="8 6"))
c.add(text(282, 256, "Zona entre dos aisladores: un corto adentro la tira entera", 16, 600, WARN))
c.add(Note(48, 548, 540, "El elemento conectado solo a b1 toma corriente pero no la deja pasar por su aislador: no corta nada si hay un corto.", title="Por qué no aísla", kind="warn"))
c.add(Note(612, 548, 540, "Las mallas dentro de un lazo o un ramal están prohibidas, y la autoridad puede limitar cuántos elementos caen por una falla.", title="Y además", kind="alert"))
save(c, "4-t2.svg")
