"""Lección 8 · Túnel de gestión: principal + pasos 2 y 4."""
from _mt import *

K = "MikroTik"

# ------------------------------------------------------------------ 8.svg principal
c = Canvas(K, "A un cliente se entra por túnel, no por un puerto")
lap = c.add(Laptop(48, 196, "Notebook técnico", "10.10.10.2", hl=CYAN, w=250))
c.add(Zone(330, 140, 400, 400, "INTERNET"))
c.add(tube(298, 238, 790, 60, "WireGuard · UDP 13231"))
c.add(arrow((420, 278), (780, 278), kind="logical"))
c.add(text(440, 302, "WinBox a 10.10.10.1, por adentro", 15, 500, INK3, FB))
# router
RX, RY = 790, 150
c.add(rect(RX, RY, 362, 370, DEEP, DEEP, 2, 20))
c.add(text(RX + 22, RY + 38, "Router del cliente", 20, 600, WHITE, FD))
c.add(text(RX + 22, RY + 64, "WAN 203.0.113.10", 15, 500, "#9FC3E3", FM))
c.add(rect(RX + 18, RY + 82, 326, 42, "#0B3A66", CYAN, 1.5, 10))
c.add(text(RX + 34, RY + 109, "wg-gestion · 10.10.10.1", 15, 600, WHITE, FM))
c.add(text(RX + 22, RY + 156, "chain=input", 14, 500, CYAN, FM))
rr = [("accept udp 13231", "ok"), ("accept 8291 por wg-gestion", "ok"), ("drop all not coming from LAN", "alert")]
c.add(rows(RX + 18, RY + 170, 326, rr, h=40, gap=8, size=14))
c.add(text(RX + 22, RY + 336, "lo de arriba, arriba del drop", 14, 500, "#9FC3E3", FB))
# escáner
sc = c.add(Generic(48, 420, "Escáner", "WinBox 8291", icon="globe", hl=ALERT, w=250))
c.add(Cable(sc.right(), (RX - 4, RY + 300), kind="alert"))
c.add(mark(560, 468, ok=False))
c.add(text(470, 516, "WinBox desde internet: drop", 15, 600, ALERT, FB))
c.add(Note(48, 572, 1104, "Un peer por técnico, cada uno con su /32. Si alguien deja la empresa, borrás su peer y los demás siguen igual.", kind="info", size=16))
save(c, "8.svg")

# ------------------------------------------------------------------ 8-paso2.svg
c = Canvas(K + " · Paso 2", "Cada punta le da a la otra su clave pública")
for i, (ttl, sub, x) in enumerate([("Router del cliente", "/interface/wireguard", 48), ("Notebook del técnico", "app WireGuard", 752)]):
    c.add(rect(x, 140, 400, 300, DEEP if i == 0 else WHITE, DEEP if i == 0 else LINE2, 2, 18))
    dk = i == 0
    c.add(text(x + 24, 178, ttl, 20, 600, WHITE if dk else INK, FD))
    c.add(text(x + 24, 204, sub, 15, 500, "#9FC3E3" if dk else INK3, FM))
    c.add(rect(x + 20, 228, 360, 82, "#0B3A66" if dk else GROUND, ALERT, 2, 12, dash="6 5"))
    c.add(icon(x + 36, 252, "lock", ALERT, 1.2))
    c.add(text(x + 80, 262, "clave privada", 17, 600, WHITE if dk else INK, FB))
    c.add(text(x + 80, 288, "no sale nunca de acá", 15, 500, ALERT if not dk else "#FCA5A5", FB))
    c.add(rect(x + 20, 330, 360, 82, "#0B3A66" if dk else SOFT, OK, 2, 12))
    c.add(icon(x + 36, 354, "key", OK if not dk else GREEN_T, 1.2))
    c.add(text(x + 80, 364, "clave pública", 17, 600, WHITE if dk else INK, FB))
    c.add(text(x + 80, 390, "se copia a la otra punta", 15, 500, GREEN_T if dk else OK, FB))
c.add(arrow((452, 360), (748, 300), kind="ok"))
c.add(text(600, 290, "va a [Peer] PublicKey", 15, 600, OK, FM, anchor="middle"))
c.add(arrow((748, 400), (452, 420), kind="ok"))
c.add(text(600, 448, "va al peer, con su /32", 15, 600, OK, FM, anchor="middle"))
t, h = code(48, 470, 1104, [('/interface/wireguard/peers/add interface=wg-gestion name=notebook-lucia \\', "#D9E9F8"),
                            ('  public-key="PEGAR-CLAVE-PUBLICA-DE-LA-NOTEBOOK" allowed-address=10.10.10.2/32', CYAN_T)], title="TERMINAL · ROUTER")
c.add(t)
c.add(text(48, 470 + h + 30, "allowed-address /32: ese peer solo puede usar la 10.10.10.2. Un peer por técnico.", 16, 500, INK2, FB))
save(c, "8-paso2.svg")

# ------------------------------------------------------------------ 8-paso4.svg
c = Canvas(K + " · Paso 4", "Por el túnel, solo la red de gestión")
for i, (allowed, good) in enumerate([("AllowedIPs = 10.10.10.0/24", True), ("AllowedIPs = 0.0.0.0/0", False)]):
    x = 48 + i * 564
    col = OK if good else ALERT
    c.add(rect(x, 140, 540, 360, WHITE, col, 2, 18))
    c.add(mark(x + 34, 176, good))
    c.add(text(x + 64, 183, allowed, 17, 600, col, FM))
    c.add(mini(x + 24, 250, 170, 84, "Notebook", "", icon="laptop"))
    # destino túnel
    c.add(mini(x + 330, 216, 186, 70, "Router cliente", "10.10.10.1", dark=True, title_size=16))
    c.add(mini(x + 330, 330, 186, 70, "Mail, web", "internet", icon=None, title_size=16))
    c.add(tube(x + 196, 251, x + 328, 36, None))
    c.add(arrow((x + 196, 251), (x + 326, 251), kind="logical"))
    if good:
        c.add(arrow((x + 196, 312), (x + 326, 362), kind="flow"))
        c.add(wrap(x + 24, 448, "Solo lo que va a 10.10.10.x entra al túnel. Tu mail y tu navegación siguen saliendo por tu internet.", 492, 16, 400, INK2)[0])
    else:
        c.add(f'<path d="M{x + 196} 312C{x + 250} 312 {x + 250} 262 {x + 300} 258" fill="none" stroke="{ALERT}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#a-alert)"/>')
        c.add(f'<path d="M{x + 424} 286V328" stroke="{ALERT}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#a-alert)"/>')
        c.add(wrap(x + 24, 448, "Todo tu tráfico viaja por el túnel y sale por la conexión del cliente: le cargás su enlace y su firewall.", 492, 16, 400, INK2)[0])
    c.add(text(x + 262, 236, "túnel", 14, 600, "#0B7FA6", FM, anchor="middle"))
c.add(Note(48, 528, 1104, "PersistentKeepalive = 25 mantiene abierto el camino cuando hay NAT en el medio (el módem de tu casa, un 4G).", kind="info", size=16))
save(c, "8-paso4.svg")
