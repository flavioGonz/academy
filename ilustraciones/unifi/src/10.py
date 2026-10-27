import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/unifi/src")
from _uf import *

# ---------------------------------------------------------------- 10.svg: el invitado sale a internet y nada más
c = Canvas(K(), "El invitado sale a internet y no llega a nada interno")
ph = c.add(Phone(48, 262, "Celular invitado", "192.168.20.x", w=290))
c.add(Zone(30, 230, 330, 140, "zona Hotspot · VLAN 20", color=WARN))
gw = c.add(Generic(430, 262, "Gateway UniFi", "zonas", icon="shield", w=260, dark=True))
inet = c.add(Internet(840, 140, "Internet", "Allow Internet Access", w=312))
c.add(Zone(800, 300, 352, 214, "zona Internal", color=BLUE))
c.add(Generic(830, 330, "Impresora", "10.10.10.50", icon="server", w=292))
c.add(Generic(830, 420, "NVR y cajas", "red Staff", icon="camera", w=292))
c.add(arrow(ph.right(), gw.left()))
c.add(wire([(690, 290), (760, 290), (760, 182), (836, 182)], kind="ok", arrow=True))
c.add(wire([(690, 320), (760, 320), (760, 420), (796, 420)], kind="alert", arrow=True))
c.add(Mark(760, 372, ok=False))
c.add(text(48, 452, "Post-Authorization Restrictions, de fábrica:", 17, 600, INK, FB))
for i, s in enumerate(["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]):
    c.add(tag(48 + i * 196, 494, s, "alert", anchor="start"))
c.add(Note(48, 540, 1104, "Con firewall por zonas (Network 9.0 en adelante) una red es de invitados al ponerla en la zona Hotspot. Nada de esto vale hasta probarlo desde un celular: el paso 5.", kind="info"))
save(c, "10.svg")

# ---------------------------------------------------------------- 10-paso2: Standard u Hotspot
c = Canvas(K(2), "Standard o Hotspot: ¿hace falta un portal?")
c.add(panel(48, 130, 540, 330, "Solo contraseña", "info", sub="WiFi tipo Standard"))
lst, _ = bullet_list(72, 220, ["El invitado entra con la clave del WiFi, como en cualquier red.", ("La zona Hotspot trae la landing page activada: desmarcá Show Landing Page en el Hotspot Portal.", "warn"), "Si no, aparece un portal que nadie pidió."], 490, size=17, gap=14)
c.add(lst)
c.add(panel(612, 130, 540, 330, "Portal cautivo", "ok", sub="WiFi tipo Hotspot > Captive Portal"))
lst, _ = bullet_list(636, 220, ["Vouchers con vencimiento, usos y límite de velocidad.", "Contraseña, pago con Stripe, Facebook o RADIUS.", "Portal externo, con Pre-Authorization Allowances para sus dominios."], 490, size=17, gap=14)
c.add(lst)
c.add(Step(612, 130, 2))
c.add(Note(48, 486, 1104, "Los dos van en la red Invitados (zona Hotspot). Lo que cambia es cómo entra el invitado, no lo que puede tocar: el aislamiento lo da la zona.", kind="ok"))
save(c, "10-paso2.svg")

# ---------------------------------------------------------------- 10-paso3: el voucher
c = Canvas(K(3), "Un voucher: un día, un uso, velocidad acotada")
flow = [("phone", "Se conecta", "al SSID Invitados"), ("door", "Ve el portal", "landing page"), ("key", "Ingresa el voucher", "código de un uso"), ("globe", "Navega", "con su límite")]
for i, (ic, a, b) in enumerate(flow):
    x = 48 + i * 280
    c.add(panel(x, 140, 248, 130, None, "ok" if i == 3 else "info"))
    c.add(icon(x + 22, 162, ic, OK if i == 3 else BLUE, 1.4))
    c.add(text(x + 22, 228, a, 19, 600, INK, FD))
    c.add(text(x + 22, 254, b, 15, 400, INK3, FM))
    if i < 3:
        c.add(arrow((x + 252, 205), (x + 276, 205)))
c.add(rect(48, 310, 520, 220, WHITE, CYAN, rx=16, sw=2.5, dash="8 6"))
c.add(text(76, 350, "VOUCHER DE LABORATORIO", 15, 600, CYAN, FM, ls=1.6))
for i, (k, v) in enumerate([("Vencimiento", "1 día"), ("Usos", "1"), ("Límite", "10 Mbps bajada / 5 Mbps subida")]):
    c.add(text(76, 396 + i * 40, k, 17, 500, INK2, FB))
    c.add(text(240, 396 + i * 40, v, 17, 600, INK, FM))
c.add(Step(48, 310, 3))
c.add(Note(600, 310, 552, "Hotspot Portal > Authentication: activá Vouchers y generá uno. Los vouchers pueden llevar vencimiento, límite de ancho de banda y cuota de datos.", title="Dónde se crea", kind="info"))
c.add(Note(600, 440, 552, "Un voucher de un uso y un día no queda dando vueltas: se usa y se vence.", kind="ok"))
save(c, "10-paso3.svg")

# ---------------------------------------------------------------- 10-paso5: la prueba del celular
c = Canvas(K(5), "La prueba: desde el celular, nada interno responde")
c.add(rect(60, 128, 250, 470, "#26323F", DEEP, rx=34))
c.add(rect(78, 168, 214, 390, WHITE, WHITE, rx=12))
c.add(rect(92, 184, 186, 38, SOFT, LINE2, rx=10, sw=1.5))
c.add(text(104, 209, "10.10.10.50", 16, 600, INK, FM))
c.add(f'<circle cx="185" cy="330" r="34" fill="none" stroke="{LINE2}" stroke-width="6"/><path d="M185 296a34 34 0 0 1 34 34" fill="none" stroke="{BLUE}" stroke-width="6" stroke-linecap="round"/>')
c.add(mid(185, 410, "Esperando...", 16, 500, INK3))
c.add(mid(185, 470, "se vence el tiempo", 17, 600, OK))
c.add(Step(60, 128, 5))
c.add(panel(360, 128, 792, 150, None, "ok"))
c.add(Mark(398, 176, ok=True))
c.add(text(430, 170, "Navega por internet y la impresora no responde", 19, 600, OK, FB))
lst, _ = bullet_list(430, 210, ["Aislado: la zona Hotspot y las restricciones hacen su trabajo.", "Probalo igual con el NAS o el NVR: http a su IP, puerto 80."], 700, size=16, gap=8)
c.add(lst)
c.add(panel(360, 300, 792, 150, None, "alert"))
c.add(Mark(398, 348, ok=False))
c.add(text(430, 342, "La página de la impresora abre", 19, 600, ALERT, FB))
lst, _ = bullet_list(430, 382, ["Revisá que la red esté en zona Hotspot y no en Internal.", ("Revisá las Post-Authorization Restrictions (paso 4).", "alert")], 700, size=16, gap=8)
c.add(lst)
c.add(Note(360, 474, 792, "Esta prueba va en cada entrega, no solo en el laboratorio. Repetila después de cada actualización grande de Network.", kind="info"))
save(c, "10-paso5.svg")
