"""Lección 2 · Usuarios propios: principal + pasos 2, 3 y 4."""
from _mt import *

K = "MikroTik"

# ------------------------------------------------------------------ 2.svg principal
c = Canvas(K, "Un usuario por técnico, un grupo por rol")
c.add(caption(48, 140, "Usuarios"))
c.add(caption(410, 140, "Grupos (qué puede hacer)"))
u1 = c.add(Person(48, 160, "lucia.tecnico", "técnica de IES", hl=CYAN, w=300))
u2 = c.add(Person(48, 276, "mesa.ayuda", "desde 192.168.88.0/24", w=300))
u3 = c.add(Person(48, 392, "admin", "deshabilitado", w=300))
c.add(rect(48, 392, 300, 84, "none", ALERT, 2, 16, dash="7 6"))
c.add(mark(330, 392, ok=False))
# grupos
c.add(rect(410, 160, 380, 84, DEEP, DEEP, 2, 16))
c.add(text(430, 194, "full", 19, 600, WHITE, FM))
c.add(text(430, 224, "todo, incluso cambiar y reiniciar", 15, 400, "#9FC3E3"))
c.add(rect(410, 276, 380, 120, WHITE, BLUE, 2, 16))
c.add(text(430, 310, "monitoreo", 19, 600, INK, FM))
c.add(pills(430, 350, ["local", "ssh", "winbox", "read", "test"], "ok", 6))
c.add(text(430, 386, "sin reboot ni write", 15, 600, ALERT, FB))
c.add(Cable(u1.right(), (410, 202), kind="flow"))
c.add(Cable(u2.right(), (410, 318), kind="flow"))
# log
lg, h = code(820, 160, 332, [("user lucia.tecnico logged in", CYAN_T), ("from 192.168.88.10 via winbox", "#D9E9F8"), "", ("filter rule added", "#D9E9F8"), ("by lucia.tecnico", CYAN_T)], title="/LOG/PRINT")
c.add(lg)
c.add(wrap(820, 196 + h, "El log dice quién entró y quién cambió qué.", 330, 16, 500, INK2)[0])
c.add(Note(48, 510, 1104, "El grupo read de fábrica puede reiniciar y ver configuración sensible. Para alguien que solo mira, armá un grupo propio como monitoreo. Para dar de baja a un técnico, deshabilitás su usuario y nadie más cambia la clave.", title="Por qué no alcanza con admin y read", kind="info", size=16))
save(c, "2.svg")

# ------------------------------------------------------------------ 2-paso2.svg
c = Canvas(K + " · Paso 2", "Probá tu usuario antes de deshabilitar admin")
c.add(mini(48, 160, 300, 96, "Entrá con lucia.tecnico", "WinBox, sesión nueva", icon="user"))
c.add(Step(48, 160, 2))
# rombo
cx, cy = 470, 208
c.add(f'<path d="M{cx} {cy - 58}L{cx + 70} {cy}L{cx} {cy + 58}L{cx - 70} {cy}z" fill="{WHITE}" stroke="{BLUE}" stroke-width="2"/>')
c.add(text(cx, cy + 6, "¿Entra?", 18, 600, INK, FD, anchor="middle"))
c.add(arrow((350, 208), (396, 208)))
# sí
c.add(arrow((542, 208), (610, 208), kind="ok"))
c.add(text(576, 196, "sí", 16, 700, OK, FB, anchor="middle"))
c.add(rect(614, 160, 538, 96, OK_BG, OK, 2, 16))
c.add(text(636, 198, "Recién ahí:", 16, 600, OK, FB))
c.add(text(636, 230, "/user/disable admin", 17, 600, INK, FM))
# no
c.add(arrow((cx, cy + 60), (cx, 330), kind="alert"))
c.add(text(cx + 14, 300, "no", 16, 700, ALERT, FB))
c.add(card(300, 334, 340, 128, "No toques admin", "Revisá nombre, grupo y contraseña desde la sesión que ya tenías.", kind="alert", icon="x"))
# user print
c.add(caption(700, 300, "/user/print después"))
c.add(Table(700, 318, ["Flags", "Name", "Group"], [[" ", "lucia.tecnico", "full"], [" ", "mesa.ayuda", "monitoreo"], ["X", "admin", "full"]],
            [80, 220, 152], hl_row=2, mono_cols=(0, 1, 2)))
c.add(text(700, 498, "X = deshabilitado: admin ya no puede entrar.", 15, 500, INK2))
c.add(Note(48, 530, 1104, "Si deshabilitás admin y tu usuario no entra, quedás afuera: la única salida es reset o Netinstall.", kind="warn", size=16))
save(c, "2-paso2.svg")

# ------------------------------------------------------------------ 2-paso3.svg
c = Canvas(K + " · Paso 3", "mesa.ayuda puede mirar, pero no reiniciar")
c.add(rect(48, 140, 520, 330, WHITE, LINE2, 2, 16))
c.add(text(72, 178, "Grupo monitoreo", 19, 600, INK, FD))
c.add(caption(72, 246, "Tiene", OK))
c.add(pills(72, 282, ["local", "ssh", "winbox", "read", "test"], "ok"))
c.add(caption(72, 338, "No tiene", ALERT))
c.add(pills(72, 374, ["reboot", "write", "policy"], "alert"))
c.add(wrap(72, 420, "Ve la configuración y diagnostica, pero no cambia ni reinicia nada.", 470, 16, 400, INK2)[0])
t, h = code(612, 140, 540, [("[mesa.ayuda@MikroTik] > /system/reboot", "#D9E9F8")], title="TERMINAL · SESIÓN DE mesa.ayuda")
c.add(t)
c.add(arrow((880, 140 + h + 4), (880, 290), kind="alert"))
c.add(card(612, 294, 540, 120, "El router lo rechaza", "Falta la política reboot en el grupo: el comando no se ejecuta.", kind="alert", icon="x"))
c.add(Note(48, 500, 1104, "Para un técnico de mesa de ayuda o un cliente curioso: puede leer el estado sin riesgo de tocar nada. Y como su cuenta tiene address=192.168.88.0/24, solo entra desde la LAN.", kind="ok", size=16))
save(c, "2-paso3.svg")

# ------------------------------------------------------------------ 2-paso4.svg
c = Canvas(K + " · Paso 4", "El signo $ dentro de comillas acorta la clave")
c.add(caption(48, 142, "Lo que escribís"))
c.add(caption(700, 142, "Lo que queda guardado"))
# mal
c.add(rect(48, 180, 560, 70, ALERT_BG, ALERT, 2, 12))
c.add(text(70, 222, 'password="Clave$Lab2026"', 18, 600, ALERT, FM))
c.add(arrow((612, 215), (692, 215), kind="alert"))
c.add(rect(700, 180, 452, 70, WHITE, ALERT, 2, 12))
c.add(text(722, 222, "Clave", 20, 600, INK, FM))
c.add(text(1130, 222, "más corta, sin aviso", 15, 600, ALERT, FB, anchor="end"))
c.add(mark(48, 180, ok=False))
# bien
c.add(rect(48, 310, 560, 70, OK_BG, OK, 2, 12))
c.add(text(70, 352, 'password="Clave\\$Lab2026"', 18, 600, OK, FM))
c.add(arrow((612, 345), (692, 345), kind="ok"))
c.add(rect(700, 310, 452, 70, WHITE, OK, 2, 12))
c.add(text(722, 352, "Clave$Lab2026", 20, 600, INK, FM))
c.add(text(1130, 352, "completa", 15, 600, OK, FB, anchor="end"))
c.add(mark(48, 310, ok=True))
c.add(Note(48, 420, 1104, "Entre comillas, RouterOS lee $Lab2026 como una variable. Como no existe, la reemplaza por nada y la clave queda en Clave. Con la barra invertida, \\$ es un signo pesos común.", title="Por qué pasa", kind="info", size=16))
c.add(Note(48, 556, 1104, "Ejemplo de clave solo para el laboratorio: en obra usá 12 caracteres o más y guardala en el gestor de claves.", kind="warn", size=15))
save(c, "2-paso4.svg")
