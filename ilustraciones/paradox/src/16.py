import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/paradox/src")
from _pdx import *

# ---------------------------------------------------------------- 16.svg: el parque y la línea M
c = Canvas(K(), "El parque cableado y la línea M, lado a lado")
c.add(NOLIG)
cols = [("Parque SP, MG y EVO", "info", [("Conexión", "bus de 4 hilos y zonas cableadas"), ("Energía", "transformador y batería de plomo o gel"), ("Programa", "teclado por secciones, BabyWare"), ("Comunica", "módulo IP o PCS, legado o MQTT"), ("Serie", "desde 7.50, solo dispositivos Paradox")]),
        ("Línea M · M25 / M25 LTE", "ok", [("Conexión", "inalámbrico M y hasta 45 por Ethernet"), ("Energía", "PoE y batería de litio interna"), ("Programa", "BlueEye o software web"), ("Comunica", "Wi-Fi, Ethernet, LTE; hasta 4 canales"), ("Capacidad", "200 zonas, 10 particiones")])]
for i, (t, kd, rows) in enumerate(cols):
    x = 48 + i * 564
    c.add(panel(x, 124, 540, 380, t, kd))
    for j, (k, v) in enumerate(rows):
        y = 200 + j * 62
        c.add(hline(x + 20, x + 520, y - 30))
        c.add(text(x + 24, y, k, 16, 600, INK3, FB))
        c.add(text(x + 140, y, v, 16, 600, INK, FB))
c.add(Note(48, 526, 540, "Desde firmware 7.50 el puerto serie trabaja solo con dispositivos Paradox. Para terceros, código de desbloqueo oficial pago: 5 USD por central.", title="La actualización que corta integraciones", kind="warn"))
c.add(Note(612, 526, 540, "Los datos de la M25 salen solo de su ficha de producto. Los servicios de app van con Swan 4G por suscripción: probala en banco antes de ofrecerla.", title="Evidencia fina", kind="info"))
save(c, "16.svg")

# ---------------------------------------------------------------- 16-paso2: decidir por sitio
c = Canvas(K(2), "Actualizar, desbloquear, migrar o dejar: por sitio")
c.add(NOLIG)
c.add(Step(48, 140, 2))
q1 = c.add(Box(80, 130, 380, 84, "¿Hay integración serie", "de terceros que el cliente usa?", icon=ICON["warn"]))
c.add(Arrow(q1.right(-14), (524, 152), kind="alert", label="sí"))
c.add(Arrow((250, 214), (250, 300), kind="ok", label="no"))
c.add(panel(530, 124, 622, 170, "Con integración serie y firmware < 7.50", "warn"))
c.add(lines(554, 190, ["No actualizar sin plan.", "Si hace falta, presupuestá el desbloqueo oficial (5 USD):", "BlueEye › menú instalador › ⋮ › Unlock Panel."], 16, 28, INK2))
c.add(panel(80, 300, 340, 110, "Sin integración serie", "ok"))
c.add(text(104, 380, "Actualizar, avisando al cliente.", 16, 600, INK, FB))
c.add(codebox(530, 318, 622, ["MG/SP+: [ENTER] + código de instalador + [300] + código", "EVO:    mantener [0] + código + [3000] + código"], 15, title="SE CARGA CON TM50, TM70, K641+ O K32LCD+ (ADMITEN LETRAS)")[0])
c.add(panel(48, 446, 540, 150, "Obra nueva sin cableado", "info"))
c.add(text(72, 512, "Evaluar M25 en banco: PoE, inalámbrico,", 16, 500, INK2, FB))
c.add(text(72, 538, "Swan 4G por suscripción, receptora compatible.", 16, 500, INK2, FB))
c.add(panel(612, 446, 540, 150, "Obra con cableado y bus", "info"))
c.add(text(636, 512, "SP+ o EVO siguen siendo la opción natural.", 16, 500, INK2, FB))
c.add(text(636, 538, "Anotá la decisión y quién la aprobó (paso 3).", 16, 500, INK2, FB))
save(c, "16-paso2.svg")
