from _oai import *

# ---------- 5.svg
c = Canvas("OmniAccess Intrusión · Lección 5", "Dónde suena una intrusión en esta versión")
tiles = [("Monitor Intrusión", "el canal se pone rojo y sube arriba", "laptop", True),
         ("Mapa", "pitido y voz: «Persona en Perímetro Norte 12»", "globe", True),
         ("Pantalla de pared", "Sin sonido · Un tono · Repetir hasta que se acepte", "bell", True),
         ("Celular", "Telegram, WhatsApp o push: no hay regla de intrusión", "phone", False)]
for i, (t, d, ic, ok) in enumerate(tiles):
    x = 48 + (i % 2) * 562
    y = 140 + (i // 2) * 170
    kd = "ok" if ok else "alert"
    c.add(panel(x, y, 542, 150, None, kind=kd))
    c.add(icon(x + 24, y + 30, ic, OK if ok else ALERT, 1.5))
    c.add(text(x + 76, y + 52, t, 21, 600, INK, FD))
    s, _ = wrap(x + 76, y + 86, d, 420, 16, 400, INK2)
    c.add(s)
    c.add(Mark(x + 500, y + 44, ok=ok))
c.add(Note(48, 490, 542, "Telegram sí avisa la salud de los equipos: ALERTA y NORMALIZADO cuando una cámara deja de responder.", kind="info", size=15))
c.add(Note(610, 490, 542, "Por WhatsApp sale el clip que manda el operador desde la grabación, no la alarma automática.", kind="info", size=15))
save(c, "5.svg")

# ---------- 5-paso3.svg: pantalla de pared en kiosco
c = Canvas("OmniAccess Intrusión · Lección 5 · Paso 3", "La PC de la pared abre el enlace en modo kiosco")
c.add(Generic(48, 150, "PC de la pared", "Chrome en kiosco", "laptop", w=300))
c.add(Arrow((352, 192), (430, 192), kind="flow"))
c.add(Generic(434, 150, "Vista Intrusión", "/monitor/intrusion", "shield", w=300, dark=True))
c.add(Arrow((738, 192), (816, 192), kind="flow"))
c.add(Generic(820, 150, "Suena", "Repetir hasta que se acepte", "bell", w=332))
c.add(Terminal(48, 280, 1104, [("chrome.exe --kiosk --autoplay-policy=no-user-gesture-required", "#D9E9F8"),
                               ("  \"https://<servidor>/monitor/intrusion?pantalla=<token>\"", "#8FE3B5")], title="ACCESO DIRECTO EN INICIO"))
c.add(Note(48, 400, 540, "--kiosk abre a pantalla completa y --autoplay-policy deja sonar sin el primer toque.", title="Por qué esas opciones", kind="info", size=15))
c.add(Note(612, 400, 540, "Sin kiosco también anda: la pantalla pide un toque para habilitar sonido y pantalla completa.", title="Sin kiosco", kind="warn", size=15))
c.add(Note(48, 540, 1104, "El enlace es de solo lectura: la pared muestra la alarma; se decide desde el panel o con una sesión con permiso.", kind="ok", size=15))
save(c, "5-paso3.svg")

# ---------- 5-paso4.svg: dibujar la línea en el mapa
c = Canvas("OmniAccess Intrusión · Lección 5 · Paso 4", "Dibujá la línea de la cámara sobre el cerco del mapa")
c.add('<rect x="48" y="140" width="760" height="440" rx="16" fill="#25352A"/>')
# calles y lotes
c.add('<path d="M48 400H808" stroke="#55626B" stroke-width="26"/>')
c.add('<path d="M420 140V580" stroke="#55626B" stroke-width="22"/>')
for (x, y) in [(80, 180), (230, 180), (480, 180), (630, 180), (80, 440), (230, 440), (480, 440), (630, 440)]:
    c.add(f'<rect x="{x}" y="{y}" width="120" height="{90 if y < 400 else 100}" rx="6" fill="#33463A" stroke="#4E6355"/>')
# cerco perimetral arriba
c.add('<path d="M60 160H796" stroke="#8FA3B5" stroke-width="3" stroke-dasharray="10 6"/>')
c.add(text(796, 152, "cerco", 14, 600, "#C9D6E2", FB, anchor="end"))
# cámara
c.add('<circle cx="560" cy="300" r="12" fill="#60a5fa" stroke="#fff" stroke-width="3"/>')
c.add('<path d="M560 300L470 175L650 175z" fill="rgba(96,165,250,0.18)" stroke="rgba(96,165,250,0.6)"/>')
c.add(text(578, 326, "Perímetro Norte 12", 15, 600, WHITE, FB))
# línea dibujada
c.add('<path d="M480 168L640 168" stroke="#3b82f6" stroke-width="6" stroke-linecap="round"/>')
for x in (480, 640):
    c.add(f'<circle cx="{x}" cy="168" r="8" fill="#fff" stroke="#3b82f6" stroke-width="3"/>')
c.add(Step(470, 205, 4))
# barra de dibujo
c.add('<rect x="180" y="510" width="500" height="50" rx="12" fill="#fff" stroke="#C2D4E6"/>')
c.add(text(200, 541, "Cruce · Perímetro Norte 12 · 2 pts", 15, 600, INK, FB))
c.add(button(560, 518, 104, "Finalizar", "dark", 15, 34))
c.add(panel(840, 140, 312, 200, "Mapa → Editar mapa", kind="info", sub="video → Cruces de línea", title_size=17))
s, _ = bullet_list(860, 225, ["Dibujar: dos puntos", "Sugerir: según el rumbo de la cámara", "Horario: aviso del mapa"], 280, 15, 10)
c.add(s)
c.add(Note(840, 360, 312, "Sin esta línea, el recuadro «Dónde fue el cruce» del análisis no tiene qué mostrar.", kind="warn", size=15))
save(c, "5-paso4.svg")
