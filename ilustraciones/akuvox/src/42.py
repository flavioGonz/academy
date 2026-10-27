from _akv import *

# ---------- 42.svg: qué anda siempre en la red local y qué se paga en la nube
c = Canvas("Akuvox · Lección 42", "¿Qué anda sin licencia y qué se paga?")
c.add(Zone(48, 140, 540, 372, "Red local · sin licencia", OK))
p = c.add(Generic(80, 180, "Portero", "SIP · relés · RTSP", icon="bell", w=230))
m = c.add(Generic(338, 180, "Monitor", "atiende y abre", icon="laptop", w=220))
c.add(Arrow(p.right(), m.left(), kind="ok"))
items = [("Llamada portero a monitor (SIP o IP directa)", "ok"),
         ("Apertura desde el monitor, PIN y tarjeta", "ok"),
         ("Relés, cerradura y RTSP al NVR", "ok"),
         ("Apertura por HTTP dentro de la LAN", "ok")]
svg, _ = bullet_list(84, 316, items, 480, size=16, gap=12)
c.add(svg)

c.add(Zone(624, 140, 528, 372, "Nube · se cobra por servicio", WARN))
cl = c.add(CloudBox(700, 180, "SmartPlus", "viviendas · Smart Access: oficinas", w=430))
c.add(Arrow((566, 222), cl.left(), kind="logical", label="internet", label_dy=-16))
chips = [("App maestra por apto", 660, 320), ("PM App", 920, 320),
         ("Familiares extra", 660, 366), ("Desvío a teléfono", 880, 366),
         ("Video en la nube", 660, 412), ("Cámaras de terceros", 880, 412),
         ("Oficinas: por puerta (1 gratis)", 660, 458)]
for s, x, y in chips:
    c.add(Chip(x, y, s, "warn", mono=False))

c.add(Note(48, 540, 540, "ACMS Pro 1.0.0.4: prueba de 180 días. SDMC: licencia USB por encima de 500 equipos.", title="Software de PC", kind="info", size=15))
c.add(Note(624, 540, 528, "Akuvox no publica precios: cotización escrita del distribuidor, con período y fecha.", title="Precios", kind="warn", size=15))
save(c, "42.svg")

# ---------- 42-paso1.svg: dónde se ve si el portero está en la nube
c = Canvas("Akuvox · Lección 42 · Paso 1", "Mirá la cuenta 1: ¿el portero está en la nube?")
c.add(Window(48, 150, 530, 200, "Portero · Account > Basic · Account 1", rows=[("Uso", "SmartPlus (nube)"), ("Register Name", "número SIP de SmartPlus"), ("Estado", "registrada")], hl=2))
c.add(Window(622, 150, 530, 200, "Portero · Account > Basic · Account 1", rows=[("Uso", "SmartPlus (nube)"), ("Register Name", "número SIP de SmartPlus"), ("Estado", "Failed")], hl=2))
c.add(Mark(548, 318, ok=True))
c.add(Mark(1122, 318, ok=False))
c.add(Chip(48, 392, "Vinculado y registrado en la nube", "ok", mono=False))
c.add(Chip(622, 392, "No registra: revisar red y Connect Setting", "alert", mono=False))
c.add(Step(48, 150, 1))
c.add(Note(48, 440, 1104, "Con SmartPlus, la cuenta 1 queda tomada por la nube y muestra su número SIP. Si dice Failed, la app no va a sonar: la Knowledge Base manda a revisar firewall, puertos salientes y el tipo de conexión en Network > Advanced (paso 2).", title="Qué te dice esta pantalla", kind="info"))
save(c, "42-paso1.svg")

# ---------- 42-paso3.svg: la planilla del edificio de ejemplo
c = Canvas("Akuvox · Lección 42 · Paso 3", "24 apartamentos: qué es local y qué se cobra")
rows = [["Llamada portero a monitor", "sí", "ninguno"],
        ["Apertura: monitor, PIN, tarjeta", "sí", "ninguno"],
        ["RTSP al NVR, HTTP local, relés", "sí", "ninguno"],
        ["Llamada a la app del residente", "no", "App maestra x24"],
        ["Familiares por encima de los gratis", "no", "Additional App"],
        ["Desvío a teléfono o celular", "no", "Landline x6"],
        ["App de la administración", "no", "PM App"]]
c.add(Table(48, 140, ["Función", "Sin licencia", "Servicio que se cobra"], rows, [470, 190, 330], row_h=50))
for i, rr in enumerate(rows):
    c.add(Mark(1100, 140 + 50 * (i + 1) + 25, ok=rr[1] == "sí"))
c.add(text(1100, 128, "LAN", 15, 600, INK3, FM, anchor="middle"))
c.add(Step(48, 140, 3))
c.add(Note(48, 556, 1104, "Verde: anda en la red local sin pagar nada. Rojo: depende de la nube y entra en la cotización.", kind="info", size=15))
save(c, "42-paso3.svg")

# ---------- 42-paso5.svg: el presupuesto en dos renglones
c = Canvas("Akuvox · Lección 42 · Paso 5", "El presupuesto: lo que se compra y lo que vence")
c.add(panel(48, 140, 520, 236, "Una vez: equipos e instalación", "ok"))
svg, _ = bullet_list(76, 210, [("Portero y monitores", "ok"), ("Fuente o PoE, cableado", "ok"), ("Mano de obra y configuración", "ok"), ("Anda en la LAN sin licencia", "ok")], 470, size=17, gap=14)
c.add(svg)
c.add(panel(612, 140, 540, 236, "Recurrente: nube SmartPlus", "warn"))
svg, _ = bullet_list(640, 210, [("Servicios de la planilla (paso 3)", "warn"), ("Período y fecha de vencimiento", "warn"), ("Renovación: automática cada 30 días o manual", "warn"), ("Paga el distribuidor o el instalador habilitado", "warn")], 490, size=17, gap=14)
c.add(svg)
c.add(Step(48, 140, 5))
c.add(Note(48, 414, 1104, "Si no se renueva: la app deja de llamar (la FAQ de la app manda a revisar la cuenta activa y paga). Portero, monitor, PIN y tarjeta siguen en la red local. Los números salen de la cotización escrita del distribuidor, nunca de un precio leído en internet.", title="Lo que conviene dejar escrito en la entrega", kind="alert"))
save(c, "42-paso5.svg")
