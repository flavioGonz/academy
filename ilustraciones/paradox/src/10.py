import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/paradox/src")
from _pdx import *

# ---------------------------------------------------------------- 10.svg: dos generaciones que no se mezclan
c = Canvas(K(), "Dos generaciones de comunicador que no se mezclan")
c.add(NOLIG)
cols = [("Legado · TURN", "info", ["IP150 (V1 a V5)", "IP150+ (V4/V5)", "PCS250/260/265", "PCS265 LTE / V7"],
         [("Receptora", "IPR512 · IPRS-7"), ("Formato", "Contact ID o SIA (*)"), ("App", "Insite Gold, BlueEye"), ("Acceso", "Swan o IP estática")]),
        ("MQTT", "ok", ["IP180", "IP150+MQ (V6)", "IP150M (V6.50)", "PCS265 V8"],
         [("Receptora", "IPC10 · VIPC20"), ("Formato", "solo Contact ID"), ("App", "solo BlueEye"), ("Acceso", "Swan, sin IP estática")])]
for i, (t, kd, mods, props) in enumerate(cols):
    x = 48 + i * 564
    c.add(panel(x, 124, 540, 400, t, kd))
    for j, m in enumerate(mods):
        c.add(tag(x + 24 + (j % 2) * 250, 196 + (j // 2) * 44, m, "gray", 15, anchor="start"))
    for j, (k, v) in enumerate(props):
        y = 300 + j * 52
        c.add(hline(x + 20, x + 520, y - 30))
        c.add(text(x + 24, y, k, 16, 600, INK3, FB))
        c.add(text(x + 180, y, v, 17, 600, INK, FM))
c.add(Note(48, 546, 540, "Central plus: principal en el serie 1 y respaldo en el serie 2, de la misma generación. (*) SIA no va por IP ni GPRS; el IPR512 legado lo acepta.", kind="info", size=15))
c.add(Note(612, 546, 540, "Pasar un IP150 a IP150M (V6.50) es irreversible y exige sitio Swan pago para toda comunicación.", title="Sin vuelta atrás", kind="alert", size=15))
save(c, "10.svg")

# ---------------------------------------------------------------- 10-paso5: lo que el módulo MQTT necesita de salida
c = Canvas(K(5), "Lo que el IP180 y el IP150M necesitan para salir")
c.add(NOLIG)
md = c.add(Generic(48, 250, "IP180 o IP150M", "en la red del cliente", icon="server", w=290))
fw = c.add(Box(440, 210, 200, 170, "Firewall", "solo salida", dark=True, icon=ICON["shield"]))
c.add(Cable(md.right(), fw.left(), kind="data"))
ports = [("TCP 8883", "MQTT: Swan e IPC10"), ("TCP 443", "firmware"), ("UDP 53", "DNS"), ("UDP 123", "hora (NTP)"), ("UDP 5683", "según el manual"), ("465 / 587", "correo, si se usa")]
for i, (p, d) in enumerate(ports):
    y = 130 + i * 66
    c.add(Arrow((640, 295), (740, y + 22), kind="ok"))
    c.add(rect(748, y, 404, 46, OK_BG, OK, rx=12))
    c.add(text(768, y + 30, p, 17, 700, OK, FM))
    c.add(text(900, y + 30, d, 16, 500, INK, FB))
c.add(Step(48, 250, 5))
c.add(codebox(48, 420, 560, ["Resolve-DnsName paradox.com", "Test-NetConnection paradox.com -Port 443"], 15, title="POWERSHELL · DESDE UNA NOTEBOOK EN LA MISMA RED")[0])
c.add(Note(48, 556, 560, "El 8883 de salida no se prueba así: pedile al informático que confirme la regla.", kind="info", size=15))
save(c, "10-paso5.svg")

# ---------------------------------------------------------------- 10-paso6: serie 1 y serie 2
c = Canvas(K(6), "Principal en el serie 1, respaldo en el serie 2")
c.add(NOLIG)
for i, (t, a, b, ok) in enumerate([("Bien", "IP180", "PCS265 V8", True), ("Mal", "IP180", "PCS265 LTE (V7)", False)]):
    x = 48 + i * 564
    c.add(panel(x, 124, 540, 380, t, "ok" if ok else "alert"))
    c.add(board(x + 160, 180, 220, 110, "Central plus", "SP+ o MG+"))
    m1 = Generic(x + 16, 360, a, "serie 1 · principal", icon="server", w=252)
    m2 = Generic(x + 276, 360, b, "serie 2 · respaldo", icon="server", w=252)
    c.add(m1); c.add(m2)
    c.add(Cable((x + 220, 290), m1.top(), kind="data"))
    c.add(Cable((x + 320, 290), m2.top(), kind="data"))
    c.add(Mark(x + 500, 152, ok))
    c.add(text(x + 24, 480, "las dos MQTT" if ok else "MQTT con legado: no se mezclan", 17, 600, OK if ok else ALERT, FB))
c.add(Step(48, 124, 6))
c.add(Note(48, 528, 1104, "El manual del IP180 lo dice así: no mezclar dispositivos de reporte MQTT con versiones legado en la misma central.", kind="info", size=16))
save(c, "10-paso6.svg")
