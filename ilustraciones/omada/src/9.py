import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _om import *

# ---------------------------------------------------------------- 9.svg: roaming
c = Canvas(K(), "Roaming: decide el cliente, el EAP lo ayuda")
c.add(cell(210, 300, 150, BLUE, 0.07))
c.add(cell(520, 300, 150, OK, 0.07))
c.add(APNode(210, 286, "EAP 1", "Roaming-Lab", r=32))
c.add(APNode(520, 286, "EAP 2", "Roaming-Lab", r=32, led=OK))
c.add(f'<path d="M150 478C260 430 430 430 590 478" fill="none" stroke="{INK3}" stroke-width="3" stroke-dasharray="8 8" marker-end="url(#a-gray)"/>')
c.add(icon(130, 470, "phone", INK, 1.4))
c.add(text(260, 512, "el celular camina de un EAP al otro", 15, 500, INK3, FM))
for i, (k_, d, kd) in enumerate([("802.11k", "le pasa la lista de vecinos", "ok"), ("802.11v", "le sugiere un EAP mejor", "ok"), ("802.11r", "claves por adelantado: con prueba", "warn")]):
    y = 554 + i * 36
    c.add(tag(48, y, k_, kd, anchor="start"))
    c.add(text(160, y - 1, d, 16, 500, INK2, FB))
c.add(panel(724, 124, 428, 500, "Para que haya roaming", "info"))
chk = [("SSID idéntico: nombre, seguridad,", True), ("cifrado y clave", None), ("Los dos EAP en el mismo sitio", True),
       ("Fast Roaming (k y v) encendido", True), ("802.11r solo si los clientes", True), ("lo soportan, probado", None),
       ("Sin Lock to AP en el cliente", True), ("EAP no tan juntos: si no, el", True), ("cliente nunca suelta al primero", None)]
y = 186
for s, mk in chk:
    if mk is not None:
        y += 14
        c.add(Mark(760, y - 6, ok=True))
    c.add(text(792, y, s, 16, 500, INK2, FB))
    y += 26
save(c, "9.svg")

# ---------------------------------------------------------------- 9-paso5: caminar con ping continuo
c = Canvas(K(5), "Caminá con ping continuo y contá los cortes")
c.add(Terminal(48, 124, 600, [
    "C:\\> ping -t 192.168.88.1",
    "Respuesta desde 192.168.88.1: tiempo=3ms",
    "Respuesta desde 192.168.88.1: tiempo=4ms",
    ("Tiempo de espera agotado para esta solicitud.", "#F4A592"),
    "Respuesta desde 192.168.88.1: tiempo=5ms",
    "Respuesta desde 192.168.88.1: tiempo=3ms"], title="NOTEBOOK · ILUSTRATIVO"))
c.add(Step(48, 124, 5))
c.add(Table(48, 368, ["Prueba", "Cortes", "AP al final"], [
    ["Fast Roaming (k y v)", "____", "____"], ["+ 802.11r en el SSID", "____", "____"]], [300, 140, 160], row_h=46))
c.add(Note(684, 124, 468, "Cada línea de Tiempo de espera agotado es un corte. Al volver, mirá en Clients a qué EAP quedó asociada la notebook.", title="Qué anotar", kind="info"))
c.add(Note(684, 290, 468, "Paso 6: activá 802.11r en Edit SSID > Advanced Settings y repetí el mismo recorrido.", title="Después, con 802.11r", kind="info"))
c.add(Note(684, 432, 468, "Si algún equipo pierde internet al cambiar de EAP con 802.11r, dejalo apagado en ese SSID.", title="Si algo se corta", kind="warn"))
save(c, "9-paso5.svg")

# ---------------------------------------------------------------- 9-paso7: mesh
c = Canvas(K(7), "Mesh: cobertura, no capacidad")
c.add(Box(48, 128, 230, 72, "Switch", "cable al root"))
root = c.add(APNode(163, 300, "Root AP", "con cable", r=32))
c.add(Cable((163, 200), (163, 268), kind="data"))
pos = [(420, 200, "1 salto"), (420, 400, "1 salto"), (660, 200, "2 saltos")]
for x, y, lab in pos:
    c.add(APNode(x, y, "Mesh AP", lab, r=28, led=OK))
c.add(Cable((195, 292), (392, 208), kind="wifi"))
c.add(Cable((195, 308), (392, 392), kind="wifi"))
c.add(Cable((448, 200), (632, 200), kind="wifi"))
c.add(tag(560, 316, "señal del uplink: -40 a -62 dBm", "ok", mono=False))
c.add(text(48, 520, "Estrella mejor que cadena: cada salto resta rendimiento.", 17, 600, INK, FB))
c.add(Step(48, 128, 7))
c.add(panel(772, 124, 380, 230, "Límites del mesh", "info"))
c.add(lines(796, 196, ["Hasta 3 saltos.", "Hasta 4 downlinks por uplink.", "Uplink entre -40 y -62 dBm.", "EAP225-Outdoor: 50 a 60", "clientes en toda la red mesh."], 16, 30))
c.add(Note(772, 374, 380, "Un EAP que se manejó por su web local tiene el mesh apagado hasta un reset.", title="Antes de armarlo", kind="warn"))
c.add(Note(48, 556, 700, "Mucha gente en un lugar: cable. El mesh lleva señal donde no llega el cable; no suma clientes.", kind="ok"))
c.add(Note(772, 506, 380, "Auto Failover viene apagado y necesita el controlador corriendo.", kind="info"))
save(c, "9-paso7.svg")
