"""Lección 33 · Reglas de protección: principal, paso 3 (DNS cerrado desde WAN) y paso 4 (listas por etapas)."""
from _mt import *

K = "MikroTik · Lección 33"

# ------------------------------------------------------------------ 33.svg
c = Canvas(K, "Qué frena cada regla de protección")
rows_ = [
    [("input", "pill:blue"), "accept established,related,untracked", "las respuestas de lo que ya aceptaste"],
    [("input", "pill:blue"), ("drop invalid", ALERT), "paquetes que no son de ninguna conexión"],
    [("input", "pill:blue"), "accept ICMP (ping WAN a 5/s)", "ping y avisos de error; el de afuera, limitado"],
    [("input", "pill:blue"), ("accept src-address-list=admins", OK), "tu gestión, siempre antes de cualquier drop"],
    [("input", "pill:blue"), ("drop all not coming from LAN", ALERT), "todo lo demás que llega al router de afuera"],
    [("forward", "pill:cyan"), "fasttrack + accept established", "velocidad para lo que ya está aceptado"],
    [("forward", "pill:cyan"), ("drop invalid", ALERT), "basura y paquetes sin conexión conocida"],
    [("forward", "pill:cyan"), ("drop WAN not DSTNATed", ALERT), "de afuera hacia la LAN sin port forwarding"],
    [("extra", "pill:warn"), ("drop UDP/TCP 53 desde WAN", ALERT), "el DNS del router usado para amplificar"],
    [("extra", "pill:warn"), "listas SSH por etapas", "fuerza bruta, solo si SSH quedó expuesto"],
]
svg, h = ctable(48, 124, ["cadena", "regla", "qué frena"], rows_, [150, 470, 484], row_h=40,
                col_colors=[INK, INK, INK2], col_fonts=[FM, FM, FB], size=15)
c.add(svg)
c.add(Note(48, 124 + h + 16, 1104, "Se lee de arriba abajo y manda la primera que coincide. Lo permitido va arriba del drop; lo extra no reemplaza a no exponer gestión ni DNS.", kind="info", size=16))
save(c, "33.svg")

# ------------------------------------------------------------------ 33-paso3.svg
c = Canvas(K + " · Paso 3", "Cerrá el 53: tu router no es DNS de internet")
net = c.add(Internet(48, 190, "Internet", "cualquier IP", w=250))
rt = c.add(Box(470, 170, 270, 124, "Router", "DNS · allow-remote-requests", dark=True))
lan = c.add(Laptop(902, 190, "PC de la LAN", "192.168.88.10", w=250))
c.add(Cable(net.right(), rt.left(), "alert", label="consulta :53", label_dy=-36))
c.add(Cable(lan.left(), rt.right(), "ok", label="DNS de la LAN", label_dy=-36))
c.add(Mark(420, 232, False))
c.add(Mark(790, 232, True))
c.add(pill(330, 330, "ether1 · WAN", "warn"))
c.add(pill(860, 330, "bridge · LAN", "gray"))
c.add(rect(48, 372, 540, 150, ALERT_BG, ALERT, 2, 16))
c.add(text(68, 406, "Abierto", 19, 600, ALERT, FD))
c.add(wrap(68, 438, "Responde a cualquiera y lo usan para amplificar ataques. En el foro: 409 GB de subida en una semana hasta que avisó el proveedor.", 500, 16, 400, INK)[0])
c.add(rect(612, 372, 540, 150, OK_BG, OK, 2, 16))
c.add(text(632, 406, "Cerrado", 19, 600, OK, FD))
c.add(wrap(632, 438, "Drop de UDP y TCP 53 que entra por la WAN, arriba de todo. La LAN sigue usando el DNS del router.", 500, 16, 400, INK)[0])
s, _ = code(48, 548, 1104, [("nslookup mikrotik.com <IP WAN del router>   # desde la notebook WAN: sin respuesta", "#D9E9F8")], title="PRUEBA", lh=26)
c.add(s)
save(c, "33-paso3.svg")

# ------------------------------------------------------------------ 33-paso4.svg
c = Canvas(K + " · Paso 4", "Cada conexión SSH nueva sube un escalón")
steps = [("connection1", "5 min", "1.ª conexión", "plain"), ("connection2", "15 min", "2.ª, dentro de 5 min", "plain"),
         ("connection3", "1 h", "3.ª, dentro de 15 min", "warn"), ("bruteforce_blacklist", "1 día", "4.ª, dentro de 1 h: drop", "alert")]
x0, wcol, gap = 48, 252, 32
for i, (lst, t, cond, k) in enumerate(steps):
    x = x0 + i * (wcol + gap)
    hgt = 150 + i * 60
    y = 560 - hgt
    fill, st = {"plain": (WHITE, LINE2), "warn": (WARN_BG, WARN), "alert": (ALERT_BG, ALERT)}[k]
    c.add(rect(x, y, wcol, hgt, fill, st, 2, 16))
    c.add(text(x + 18, y + 34, cond, 15, 600, INK2, FB))
    c.add(text(x + 18, y + 70, lst if len(lst) < 16 else "bruteforce_", 16, 600, ALERT if k == "alert" else INK, FM))
    if len(lst) >= 16:
        c.add(text(x + 18, y + 92, "blacklist", 16, 600, ALERT, FM))
    c.add(pill(x + 18, y + hgt - 26, "timeout " + t, {"plain": "gray", "warn": "warn", "alert": "alert"}[k], anchor="start"))
    if i < 3:
        c.add(arrow((x + wcol + 3, y + 40), (x + wcol + gap - 3, y + 40), kind="flow", bend="straight"))
c.add(rect(48, 132, 470, 96, OK_BG, OK, 2, 16))
c.add(text(68, 166, "src-address-list=admins → accept", 16, 600, OK, FM))
c.add(text(68, 196, "Va primero: tu oficina no cuenta conexiones.", 16, 400, INK, FB))
c.add(Note(48, 584, 1104, "Cuenta conexiones nuevas, no logins fallidos: un login exitoso también suma. Sin el drop final, la lista negra no bloquea nada.", kind="warn", size=16))
save(c, "33-paso4.svg")
