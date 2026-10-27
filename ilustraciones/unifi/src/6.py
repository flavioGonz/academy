import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/unifi/src")
from _uf import *


def frame(x, y, s, kind="gray", w=None):
    """Trama dibujada como etiqueta: sin etiqueta (gris) o con número de VLAN."""
    bg, fg = {"gray": (WHITE, INK3), "cyan": (WHITE, CYAN), "ok": (OK_BG, OK), "alert": (ALERT_BG, ALERT)}[kind]
    w = w or len(s) * 9.2 + 26
    return rect(x - w / 2, y - 20, w, 30, bg, fg, rx=8, sw=2) + mid(x, y, s, 15, 600, fg, FM)


def switch_body(x, y, w, ports, title="Switch UniFi"):
    out = [rect(x, y, w, 110, DEEP, DEEP, rx=18), text(x + 20, y + 34, title, 20, 600, WHITE, FD)]
    for px, lab, col in ports:
        out.append(rect(px - 50, y + 50, 100, 46, col or "#0B3A66", col or "#4E7396", rx=8))
        out.append(mid(px, y + 80, lab, 15, 600, WHITE, FM))
    return "".join(out)


# ---------------------------------------------------------------- 6.svg: puerto troncal contra puerto de equipo final
c = Canvas(K(), "Puerto troncal o puerto de equipo final")
cx = [200, 560, 900]
c.add(switch_body(48, 120, 1104, [(cx[0], "uplink", None), (cx[1], "AP", None), (cx[2], "cámara", CYAN)]))
for i, x in enumerate(cx):
    c.add(wire([(x, 216), (x, 420)], kind="data"))
for x in cx[:2]:
    c.add(frame(x + 90, 262, "sin etiqueta"))
    c.add(frame(x + 90, 312, "20", "cyan", 56))
    c.add(frame(x + 90, 362, "30", "cyan", 56))
c.add(frame(cx[2] + 130, 280, "sin etiqueta: VLAN 30", "ok"))
c.add(frame(cx[2] + 95, 350, "10 etiquetada", "alert"))
c.add(Mark(cx[2] + 196, 350, ok=False))
c.add(Generic(cx[0] - 150, 422, "Gateway u otro switch", "", icon="server", w=300))
c.add(APNode(cx[1], 466, "", ""))
c.add(Camera(cx[2] - 140, 422, "Cámara", "VLAN 30", w=280))
cfg = [("Nativa: Staff o gestión", "Etiquetadas: Allow All", "info"),
       ("Nativa: gestión del AP", "Etiquetadas: Allow All", "info"),
       ("Nativa: CCTV (VLAN 30)", "Etiquetadas: Block All", "ok")]
for x, (a, b, kd) in zip(cx, cfg):
    c.add(text(x - 150, 548, a, 16, 600, INK, FM))
    c.add(text(x - 150, 574, b, 16, 600, OK if kd == "ok" else BLUE, FM))
c.add(text(48, 630, "Por defecto un puerto UniFi acepta todas las VLAN etiquetadas: bien para uplinks y AP, no para equipos finales.", 16, 400, INK2, FB))
save(c, "6.svg")

# ---------------------------------------------------------------- 6-paso1: el puerto de la cámara en Port Manager
c = Canvas(K(1), "Puerto de cámara: nativa CCTV y Block All")
c.add(Window(48, 130, 620, 250, "UniFi Network", path="Port Manager > switch > puerto de la cámara", rows=[("Native VLAN / Network", "CCTV (VLAN 30)"), ("Tagged VLAN Management", "Block All"), ("PoE", "Power Cycle en el paso 3")], hl=1))
c.add(text(48, 398, "Los valores van en el paso 2.", 15, 500, INK3, FB))
c.add(Step(48, 130, 1))
c.add(Camera(760, 150, "Cámara", "recibe su red sin etiqueta", w=392))
c.add(arrow((710, 262), (750, 262), kind="ok"))
c.add(panel(760, 270, 392, 110, None, "ok"))
c.add(text(784, 312, "Toma IP de 192.168.30.0/24", 18, 600, OK, FB))
c.add(text(784, 344, "y no puede pedir otra VLAN.", 16, 400, INK2, FB))
c.add(Note(48, 420, 540, "Native VLAN dice en qué red caen las tramas sin etiqueta: lo que manda la cámara entra a CCTV.", title="Qué hace cada campo", kind="info"))
c.add(Note(612, 420, 540, "Block All descarta cualquier trama que llegue con etiqueta de otra VLAN. El puerto queda en una sola red.", kind="info"))
save(c, "6-paso1.svg")

# ---------------------------------------------------------------- 6-paso5: switch de terceros en el medio
c = Canvas(K(5), "Con un switch de terceros: gestión sin etiqueta")
g = c.add(Generic(48, 170, "Gateway UniFi", "", icon="server", w=260, dark=True))
s3 = c.add(Generic(430, 170, "Switch de terceros", "administrable", icon="server", w=300))
ap = c.add(APNode(980, 212, "AP", ""))
c.add(Cable(g.right(), s3.left(), kind="data"))
c.add(Cable(s3.right(), (938, 212), kind="data"))
c.add(Step(840, 212, 5))
c.add(panel(430, 300, 722, 150, "Puerto del switch de terceros hacia el AP", "ok"))
c.add(frame(610, 380, "gestión del AP: sin etiqueta", "ok"))
c.add(frame(960, 380, "VLAN de los SSID: etiquetadas", "cyan"))
c.add(text(454, 430, "Ejemplo: gestión sin etiqueta, 20 y 30 etiquetadas.", 16, 400, INK2, FB))
c.add(Note(48, 300, 350, "Un lector de LazyAdmin tenía la VLAN del AP etiquetada en el switch del medio: el AP no anduvo hasta dejarla sin etiqueta.", title="El caso", kind="alert"))
c.add(Note(48, 490, 1104, "Un switch no administrable en el camino descarta o pierde las etiquetas: con VLANs, todo lo que está entre el gateway y el AP tiene que ser administrable y llevar las mismas VLAN.", kind="warn"))
save(c, "6-paso5.svg")

# ---------------------------------------------------------------- 6-paso6: la prueba de la notebook
c = Canvas(K(6), "Probá con tu notebook en el puerto de la cámara")
sw = c.add(switch_body(48, 130, 420, [(258, "cámara", CYAN)], title="Switch"))
nb = c.add(Laptop(128, 330, "Notebook", "en lugar de la cámara", w=260))
c.add(wire([(258, 226), (258, 330)], kind="data"))
c.add(Step(296, 280, 6))
c.add(panel(520, 130, 632, 96, None, "ok"))
c.add(Mark(556, 178, ok=True))
c.add(text(588, 170, "Recibe 192.168.30.x", 19, 600, OK, FB))
c.add(text(588, 198, "cae en la VLAN de cámaras", 16, 400, INK2, FB))
c.add(panel(520, 244, 632, 96, None, "alert"))
c.add(Mark(556, 292, ok=False))
c.add(text(588, 284, "No llega a Staff 10.10.10.0/24", 19, 600, ALERT, FB))
c.add(text(588, 312, "ni a las PCs ni al resto de la red", 16, 400, INK2, FB))
c.add(text(48, 470, "Para puertos expuestos (exterior, estacionamiento), una capa más:", 18, 600, INK, FD))
c.add(Note(48, 492, 540, "Fijá la MAC de la cámara en el puerto: otro equipo enchufado ahí no entra (lo que hace The Hook Up).", title="Cámaras de terceros", kind="info"))
c.add(Note(612, 492, 540, "Lock Port to UniFi Device en Port Manager (Network 10.6.101, switch con firmware 7.6 o superior).", title="Cámaras UniFi", kind="info"))
save(c, "6-paso6.svg")
