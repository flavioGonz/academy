from _akv import *

# ---------- 1.svg: idea central
c = Canvas("Akuvox", "Primero la IP, después la web, y la clave cambia")
c.add(panel(48, 140, 340, 330, "1 · Pedile la IP al equipo"))
rows = [("bell", "Botón ~5 s: la dice", "en voz alta"), ("key", "Teclado: *3258*", "o 9999 y 3888"),
        ("phone", "Pantalla ~5 s", "+ PIN de sistema"), ("laptop", "IP Scanner", "Windows 64 bits")]
for i, (ic, a, b) in enumerate(rows):
    y = 190 + i * 68
    c.add(icon(68, y, ic, BLUE, 1.25))
    c.add(text(112, y + 12, a, 17, 600, INK))
    c.add(text(112, y + 34, b, 15, 400, INK3, FM))
c.add(Window(430, 140, 340, 230, "Navegador", path="http://192.168.88.X", rows=[("Usuario", "admin"), ("Clave", "admin")], hl=1))
c.add(Chip(600, 345, "de fábrica y publicada", "alert", mono=False, anchor="middle"))
c.add(Window(812, 140, 340, 230, "Web del portero · clave", rows=[("Usuario", "admin"), ("Clave nueva", "Lab-Portero-2026!")], hl=1))
c.add(Chip(982, 345, "clave propia", "ok", mono=False, anchor="middle"))
c.add(Arrow((392, 255), (424, 255)))
c.add(Arrow((774, 255), (806, 255)))
c.add(Mark(745, 160, ok=False))
c.add(Mark(1127, 160, ok=True))
c.add(Note(430, 400, 722, "admin / admin es igual en toda la línea y figura en la documentación pública. Claroty contó unos 5.000 Akuvox expuestos a internet: la clave de fábrica no pasa de la primera visita.", title="Por qué se cambia el primer día", kind="warn"))
c.add(Note(48, 500, 340, "No todas tienen pantalla ni teclado: por eso cada familia tiene su método.", kind="info"))
save(c, "1.svg")

# ---------- 1-paso1.svg: dónde se conecta
c = Canvas("Akuvox · Paso 1", "Portero, monitor y notebook en la misma red")
sw = c.add(Router(330, 140, "Switch PoE de laboratorio", "red 192.168.88.0/24", ports=["uplink", "p2", "p3", "p4", "p5"], hl={"p2": CYAN, "p3": CYAN, "p4": BLUE}))
it = c.add(Intercom(70, 300, "Portero", "R20A / E12 / E16"))
mo = c.add(Monitor(470, 420, "Monitor", "C316 / C319 / S567"))
nb = c.add(Laptop(880, 330, "Notebook", "navegador · IP Scanner", w=270))
rt = c.add(Generic(880, 150, "Router", "DHCP · gw 192.168.88.1", icon="globe", w=270))
c.add(Cable(it.port("eth"), sw.port("p2"), kind="data", label="datos + PoE", label_at=0.42, label_dy=-6))
c.add(Cable(mo.top(-40), sw.port("p3"), kind="data"))
c.add(Cable(sw.port("p4"), nb.left(), kind="data"))
c.add(Cable(rt.left(), (sw.x + sw.w, sw.y + 60), kind="data", label="uplink", label_at=0.5))
c.add(Step(sw.port("p2")[0] - 30, sw.port("p2")[1] + 26, 1))
c.add(Note(800, 460, 350, "Con switch PoE el mismo cable alimenta al portero (802.3af en R20, E12 y E16). Sin PoE, fuente de 12 V aparte.", title="Un cable, dos cosas", kind="info"))
save(c, "1-paso1.svg")

# ---------- 1-paso2.svg: cómo pedir la IP según el modelo
c = Canvas("Akuvox · Paso 2", "Cada familia te da la IP a su manera")
c.add(Table(48, 140, ["Modelo", "Cómo pedirle la IP"], [
    ["R20A · E12 · E13 · X910", "mantener el botón de llamada ~5 s: la dice en voz alta"],
    ["R20K · R25K", "marcar *3258* en el teclado"],
    ["E16 · E18", "mantener la pantalla ~5 s, PIN de sistema"],
    ["R29 · X915", "marcar 9999, luego 3888, System Info"],
], [270, 560], row_h=56, hl_row=0, mono_cols=(0,)))
it = c.add(Intercom(990, 150, "R20A", "botón ~5 s"))
c.add(text(1065, 500, "lo dice en voz alta", 15, 500, INK3, FB, anchor="middle"))
c.add(pill(1065, 536, "“192.168.88.X”", CYAN, WHITE, 16))
c.add(Note(48, 450, 830, "PIN de sistema del E16: admin hasta el firmware 216.30.10.121; Admin321 en las versiones nuevas. Si uno no entra, probá el otro antes de resetear.", title="Ojo con el E16", kind="warn"))
save(c, "1-paso2.svg")

# ---------- 1-paso5.svg: entrar y cambiar la clave
c = Canvas("Akuvox · Paso 5", "Entrá con admin / admin y cambiá la clave web")
c.add(Window(48, 150, 400, 240, "Navegador", path="http://192.168.88.X", rows=[("User Name", "admin"), ("Password", "admin")], hl=1))
c.add(Step(48, 150, 5))
c.add(Window(530, 150, 420, 240, "Web del portero · clave web", rows=[("Clave actual", "admin"), ("Clave nueva", "Lab-Portero-2026!"), ("Confirmar", "Lab-Portero-2026!")], hl=1))
c.add(Arrow((454, 270), (522, 270), label="entrar", label_dy=-24))
c.add(Mark(975, 270, ok=True))
c.add(Table(48, 440, ["Ficha del equipo (paso 6)", "Dato"], [["Modelo · IP", "R20A · 192.168.88.X"], ["MAC · clave nueva", "anotadas en la ficha"]], [420, 480], row_h=44, mono_cols=()))
c.add(Note(1000, 440, 160, "Sin ficha, la clave nueva se pierde.", kind="info", size=15))
save(c, "1-paso5.svg")
