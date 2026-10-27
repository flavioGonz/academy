from _fil import *

# ---------- 1.svg: quién cuenta y por dónde pasa el número
c = Canvas("OmniAccess Filas · Lección 1", "Quién cuenta: la cámara, no el servidor")
cam = c.add(Camera(48, 200, "Cámara Bosch", "IVA Pro · cuenta", w=240))
srv = c.add(Server(430, 200, "OmniAccess", "Modo Cola", w=230))
mon = c.add(Generic(780, 130, "Monitor en Vivo", "aforo y estado", icon="laptop", w=330))
alt = c.add(Generic(780, 280, "Alerta", "Telegram · WhatsApp · push", icon="bell", w=372))
c.add(Arrow(cam.right(), srv.left(), label="evento ONVIF", label_dy=-16))
c.add(Arrow(srv.right(-12), mon.left(), kind="flow"))
c.add(Arrow(srv.right(12), alt.left(), kind="flow"))
c.add(Step(48, 200, 1))
c.add(Step(430, 200, 2))
c.add(Step(780, 130, 3))
c.add(Step(780, 280, 4))
c.add(text(168, 330, "zona de la fila", 15, 500, INK3, FM, anchor="middle"))
c.add(text(168, 352, "Aforo · Entrada · Salida", 15, 600, BLUE, FM, anchor="middle"))
c.add(text(545, 330, "pregunta cada 5 s", 15, 500, INK3, FM, anchor="middle"))
c.add(text(545, 352, "guarda y compara", 15, 600, BLUE, FM, anchor="middle"))
c.add(text(966, 392, "si pasa el umbral", 15, 500, INK3, FM, anchor="middle"))
c.add(Note(48, 440, 540, "El número nace en la cámara. Si está mal, se revisa la cámara (ubicación, zona, calibración).", title="Número equivocado", kind="warn"))
c.add(Note(612, 440, 540, "Si el número no llega, se revisa el camino: ONVIF, red, suscripción, procesos del servidor.", title="Número que no llega", kind="info"))
save(c, "1.svg")

# ---------- 1-paso2.svg: activar el Modo Cola
c = Canvas("OmniAccess Filas · Lección 1 · Paso 2", "Activá el Modo Cola: los modos son exclusivos")
w = c.add(Window(48, 140, 620, 330, "Configuración · Modos (LPR / Face / Cola)", rows=[("Modo LPR", "apagado"), ("Modo Face", "apagado"), ("Modo Cola", "Activar"), ("Confirmación", "Sí, cambiar")], hl=2, path="Configuración → Modos"))
c.add(Step(668, 290, 2))
c.add(Arrow((690, 300), (790, 300), kind="flow"))
c.add(panel(800, 140, 352, 330, "Después de recargar", kind="ok"))
items = ["Monitor en Vivo", "Flujo de Filas", "Filas · Despachos", "Reportes", "Horarios de Filas", "Pantalla / Kiosko", "Calibración"]
for i, s in enumerate(items):
    c.add(text(826, 210 + i * 36, "· " + s, 17, 500, INK))
c.add(Note(48, 500, 1104, "Al activar Cola se apagan LPR y Face para todos los usuarios y la aplicación se recarga con el menú nuevo. En un sistema en uso, se coordina con el cliente.", title="Ojo en producción", kind="alert"))
save(c, "1-paso2.svg")

# ---------- 1-paso4.svg: los cuatro pasos y su pantalla
c = Canvas("OmniAccess Filas · Lección 1 · Paso 4", "Cada paso del aforo tiene su pantalla")
c.add(Table(48, 150, ["Paso", "Qué pasa", "Dónde lo ves"], [
    ["1 · Cámara", "cuenta personas en la zona", "Filas · Analíticas ONVIF"],
    ["2 · Evento", "OmniAccess lo recibe y guarda", "Filas · Detección por fila"],
    ["3 · Monitor", "se muestra el aforo y el estado", "Monitor en Vivo · Kiosko"],
    ["4 · Alerta", "pasa el umbral y avisa", "Despachos · Telegram · app"],
], [220, 420, 464], hl_row=None, row_h=58))
c.add(Note(48, 470, 1104, "Dibujalo en una hoja con estas cuatro cajas. Cuando haya un reclamo, ubicá en qué paso se cortó antes de tocar nada.", kind="info"))
save(c, "1-paso4.svg")
