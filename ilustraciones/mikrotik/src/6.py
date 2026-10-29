"""Lección 6 · Backup primero: principal + pasos 3 y 5."""
from _mt import *

K = "MikroTik"

# ------------------------------------------------------------------ 6.svg principal
c = Canvas(K, "¿.backup o export? Cada uno sirve para otra cosa")
for i, (ttl, cmd, kind, items, use) in enumerate([
    (".backup · binario", "/system/backup/save", "bin",
     ["Clona el equipo completo, usuarios incluidos.", "No se puede leer ni comparar.", "En otro modelo puede traer problemas de interfaces y MAC."],
     "Para volver atrás en el mismo equipo"),
    ("export · texto .rsc", "/export file=antes", "text",
     ["Se lee con cualquier editor y se compara con diff.", "No lleva contraseñas de usuarios ni certificados.", "Con show-sensitive suma claves WiFi, PPPoE y VPN."],
     "Para leer, comparar y migrar")]):
    x = 48 + i * 564
    c.add(rect(x, 140, 540, 350, WHITE, NAVY if kind == "bin" else BLUE, 2, 18))
    c.add(fileicon(x + 28, 166, "", kind))
    c.add(text(x + 116, 196, ttl, 22, 600, INK, FD))
    c.add(text(x + 116, 226, cmd, 15, 500, BLUE, FM))
    b, _ = bullets(x + 30, 290, items, 480, 17)
    c.add(b)
    c.add(rect(x + 20, 406, 500, 60, OK_BG, OK_BG, 0, 12))
    c.add(mark(x + 48, 436, True))
    c.add(text(x + 78, 442, use, 17, 600, OK, FB))
c.add(Note(48, 520, 1104, "En obra se hacen los dos: el .backup para restaurar rápido, el export para el legajo y para saber qué cambió.", kind="info", size=16))
save(c, "6.svg")

# ------------------------------------------------------------------ 6-paso3.svg
c = Canvas(K + " · Paso 3", "Compará antes y después: el diff muestra el cambio")
fa = ["# <fecha> by RouterOS 7.x", "/interface bridge", "add name=bridge", "…"]
fb = ["# <fecha> by RouterOS 7.x", "/interface bridge", "add name=bridge", "…", "/system identity", "set name=LAB-MT01"]
for i, (nm, ls) in enumerate([("antes.rsc", fa), ("despues.rsc", fb)]):
    x = 48 + i * 300
    c.add(rect(x, 140, 280, 250, WHITE, LINE2, 2, 14))
    c.add(text(x + 18, 172, nm, 16, 600, INK, FM))
    c.add(line(x + 12, 186, x + 268, 186, LINE, 1.5))
    for j, s in enumerate(ls):
        yy = 214 + j * 28
        new = i == 1 and j >= 4
        dat = j == 0
        if new:
            c.add(rect(x + 8, yy - 19, 264, 26, OK_BG, OK_BG, 0, 6))
        c.add(text(x + 18, yy, s, 13.5, 500, OK if new else (WARN if dat else INK2), FM))
t, h = code(660, 140, 492, [("$ diff antes.rsc despues.rsc", "#D9E9F8"),
                            ("< # <fecha 10:02> by RouterOS 7.x", AMBER_T),
                            ("> # <fecha 10:09> by RouterOS 7.x", AMBER_T),
                            ("> /system identity", GREEN_T),
                            ("> set name=LAB-MT01", GREEN_T)], title="NOTEBOOK · LINUX O MAC", lh=30)
c.add(t)
c.add(text(660, 140 + h + 30, "En Windows: fc antes.rsc despues.rsc", 16, 500, INK2, FM))
c.add(Note(48, 430, 540, "< es lo que estaba en el archivo de antes, > lo que aparece en el de después. Lo verde es tu cambio.", title="Cómo se lee", kind="ok", size=16))
c.add(Note(612, 430, 540, "La primera línea trae la fecha del export: siempre cambia. No es un cambio de configuración.", title="La línea ámbar no cuenta", kind="warn", size=16))
save(c, "6-paso3.svg")

# ------------------------------------------------------------------ 6-paso5.svg
c = Canvas(K + " · Paso 5", "Los archivos con secretos se guardan bajo llave")
c.add(fileicon(110, 160, "antes-sensible.rsc", "secret", 72, 90))
c.add(fileicon(330, 160, "antes.backup", "bin", 72, 90))
c.add(text(48, 318, "Tienen claves WiFi, PPPoE, VPN o el equipo entero.", 16, 500, INK2, FB))
c.add(card(612, 140, 540, 120, "Lugar con acceso restringido", "Carpeta del cliente con permisos, gestor de claves o almacenamiento cifrado.", kind="ok", icon="lock"))
c.add(card(612, 280, 540, 120, "Nunca en un chat ni en un mail sin cifrar", "Un archivo reenviado una vez ya no se controla.", kind="alert", icon="x"))
c.add(arrow((450, 210), (604, 200), kind="ok"))
c.add(fileicon(110, 400, "antes.rsc", "text", 72, 90))
c.add(text(230, 440, "Sin show-sensitive: no trae secretos.", 16, 500, INK2, FB))
c.add(text(230, 466, "Va al legajo del cliente, junto al de después.", 16, 500, INK2, FB))
c.add(Note(48, 560, 1104, "El .backup se guardó con contraseña en el paso 1: anotala en el gestor de claves, no al lado del archivo.", kind="info", size=16))
save(c, "6-paso5.svg")
