"""Lección 4 · Input y forward: pasos 1, 2 y 3 (la principal 4.svg está hecha a mano y se mantiene)."""
from _mt import *

K = "MikroTik · Lección 4"

# ------------------------------------------------------------------ 4-paso1.svg
c = Canvas(K + " · Paso 1", "Ubicá las dos reglas que protegen")
cols = [("chain=input", "protege al router", BLUE,
         [("accept established,related,untracked", "plain"), ("drop invalid", "plain"), ("accept ICMP", "plain"), ("…", "dim"),
          ("drop all not coming from LAN", "alert")]),
        ("chain=forward", "protege a la LAN", CYAN,
         [("fasttrack", "plain"), ("accept established,related,untracked", "plain"), ("drop invalid", "plain"), ("…", "dim"),
          ("drop all from WAN not DSTNATed", "alert")])]
for i, (ch, sub, col, items) in enumerate(cols):
    x = 48 + i * 564
    c.add(rect(x, 140, 540, 340, WHITE, LINE2, 2, 16))
    c.add(pill(x + 20, 180, ch, "blue" if i == 0 else "cyan", anchor="start"))
    c.add(text(x + 200, 180, sub, 17, 600, INK, FD))
    c.add(text(x + 20, 222, "defconf:", 14, 500, INK3, FM))
    c.add(rows(x + 20, 236, 500, items, h=38, gap=8, size=15))
c.add(Note(48, 506, 540, "Si el destino es una IP del router (también 192.168.88.1), el paquete entra por input y llega a esta regla.", kind="info", size=16))
c.add(Note(612, 506, 540, "Lo que entra por la WAN hacia la LAN se descarta, salvo que tenga un dst-nat (lección 10).", kind="info", size=16))
save(c, "4-paso1.svg")

# ------------------------------------------------------------------ 4-paso2.svg
c = Canvas(K + " · Paso 2", "La regla apunta a la lista, no a cada IP")
c.add(rect(48, 150, 420, 250, WHITE, BLUE, 2, 16))
c.add(text(72, 188, "address-list", 15, 500, INK3, FM))
c.add(text(72, 218, "admins", 22, 600, INK, FM))
for i, (ip, cm) in enumerate([("192.168.88.10", "notebook lab"), ("203.0.113.25", "oficina ejemplo")]):
    yy = 246 + i * 62
    c.add(rect(68, yy, 380, 50, SOFT, LINE2, 1.5, 10))
    c.add(text(86, yy + 31, ip, 16, 600, BLUE, FM))
    c.add(text(430, yy + 31, cm, 14, 400, INK3, FB, anchor="end"))
c.add(arrow((472, 275), (560, 275), kind="flow"))
c.add(rect(568, 210, 584, 130, DEEP, DEEP, 2, 16))
c.add(text(592, 244, "chain=input  action=accept", 15, 500, "#9FC3E3", FM))
c.add(text(592, 274, "protocol=tcp  dst-port=8291", 15, 500, WHITE, FM))
c.add(text(592, 304, "src-address-list=admins", 16, 600, CYAN, FM))
c.add(text(592, 330, "winbox solo admins", 14, 400, "#9FC3E3", FB))
c.add(card(48, 432, 540, 150, "¿Cambió la IP de la oficina?",
           "Editás la entrada en la lista. La regla del firewall no se toca y no corrés riesgo de desordenarla.", kind="ok", icon="check"))
c.add(card(612, 432, 540, 150, "Lo mismo con interfaces",
           "Las interface lists (WAN, LAN) hacen lo mismo con puertos: si la WAN pasa a PPPoE, la sumás a la lista WAN.", kind="info", icon="server"))
save(c, "4-paso2.svg")

# ------------------------------------------------------------------ 4-paso3.svg
c = Canvas(K + " · Paso 3", "Arriba del drop, no al final")
heads = [("Con place-before", OK, True), ("Sin place-before (al final)", ALERT, False)]
for i, (ttl, col, good) in enumerate(heads):
    x = 48 + i * 564
    c.add(mark(x + 18, 154, ok=good))
    c.add(text(x + 46, 161, ttl, 19, 600, INK, FD))
    if good:
        items = [("accept established,related,untracked", "plain"), ("accept ICMP", "plain"), ("accept dst-port=8291 admins", "ok"),
                 ("drop all not coming from LAN", "alert")]
        cnt = ["", "", "contador sube", ""]
    else:
        items = [("accept established,related,untracked", "plain"), ("accept ICMP", "plain"), ("drop all not coming from LAN", "alert"),
                 ("accept dst-port=8291 admins", "dim")]
        cnt = ["", "", "corta a 203.0.113.25", "contador en 0"]
    c.add(rows(x + 44, 190, 470, items, h=44, gap=10, size=15))
    # flecha del paquete
    stop = 2
    yy0, yy1 = 190 + 22, 190 + stop * 54 + 22
    c.add(f'<path d="M{x + 22} {yy0}V{yy1}" stroke="{col}" stroke-width="3" fill="none" marker-end="url(#a-{"ok" if good else "alert"})"/>')
    for j, s in enumerate(cnt):
        if s:
            c.add(text(x + 500, 190 + j * 54 + 28, s, 14, 600, OK if good else (ALERT if j == 2 else INK3), FB, anchor="end"))
c.add(text(48, 470, "El paquete baja regla por regla y se queda en la primera que coincide.", 17, 500, INK2, FB))
lines = [('/ip/firewall/filter/add chain=input protocol=tcp dst-port=8291 \\', "#D9E9F8"),
         ('  src-address-list=admins action=accept comment="winbox solo admins" \\', "#D9E9F8"),
         ('  place-before=[find comment="defconf: drop all not coming from LAN"]', CYAN_T)]
t, h = code(48, 494, 1104, lines, title="TERMINAL · EN SAFE MODE")
c.add(t)
save(c, "4-paso3.svg")
