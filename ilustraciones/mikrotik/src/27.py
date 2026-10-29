"""Lección 27 · Rutas estáticas."""
from _mt import *  # noqa

K = "MikroTik"

# ---------------------------------------------------------------- principal
c = Canvas(K, "¿Por dónde sale el paquete? Decide la tabla")
c.add(pill(48, 152, "paquete a 192.168.20.15", "dark", anchor="start"))
t, h = ctable(48, 180, ["destino", "gateway", "dist.", ""], [
    ["0.0.0.0/0", "192.168.1.1 (ISP)", "1", ("coincide", "pill:gray")],
    ["192.168.20.0/24", "l2tp-central", "1", ("gana: /24", "pill:ok")],
    ["192.168.88.0/24", "bridge (conectada)", "0", ("no coincide", "pill:gray")],
    ["203.0.113.10/32", "192.168.1.1 (ISP)", "1", ("no coincide", "pill:gray")],
], [220, 250, 90, 170], row_h=50, col_fonts=[FM, FM, FM, FB])
c.add(t)
c.add(rect(52, 283, 722, 44, "none", OK, 2.5, 10))
c.add(card(820, 180, 332, 124, "1 · La más específica",
           "Máscara más larga: una /24 le gana a 0.0.0.0/0.", kind="ok", title_size=18, body_size=15))
c.add(card(820, 322, 332, 124, "2 · Menor distancia",
           "Solo entre rutas al mismo destino: conectada 0, estática 1, OSPF 110.", kind="info", title_size=18, body_size=15))
c.add(card(820, 464, 332, 124, "3 · Gateway vivo",
           "Una ruta con gateway inalcanzable queda inactiva.", kind="warn", title_size=18, body_size=15))
c.add(Note(48, 470, 726, "La ruta por defecto se usa cuando nada más coincide. Y cada ruta hacia una red remota necesita su ruta de vuelta en la otra punta.", kind="info", size=15))
save(c, "27.svg")

# ---------------------------------------------------------------- paso 3: check-gateway
c = Canvas(K + " · Paso 3", "check-gateway: dos pings perdidos y la ruta se apaga")
X0, Y = 120, 260
c.add(line(X0, Y, 1080, Y, LINE2, 3))
ticks = [(0, "0 s", True), (1, "10 s", False), (2, "20 s", False)]
for i, lbl, ok in ticks:
    x = X0 + 120 + i * 300
    c.add(line(x, Y - 12, x, Y + 12, INK3, 2))
    c.add(text(x, Y + 40, lbl, 16, 600, INK2, FM, anchor="middle"))
    c.add(pill(x, Y - 40, "ping al gateway", "gray"))
c.add(mark(X0 + 120, Y - 92, True))
c.add(text(X0 + 150, Y - 85, "contesta", 16, 600, OK, FB))
c.add(mark(X0 + 420, Y - 92, False))
c.add(text(X0 + 450, Y - 85, "1 s sin respuesta", 16, 600, ALERT, FB))
c.add(mark(X0 + 720, Y - 92, False))
c.add(text(X0 + 750, Y - 85, "2.º timeout", 16, 600, ALERT, FB))
c.add(pill(X0 + 900, Y - 40, "ruta inactiva", "alert"))
c.add(Table(48, 350, ["ruta a 10.20.30.0/24", "gateway", "estado"], [
    ["lab principal", "192.168.88.250 · ping", "sin A: inactiva"],
    ["lab respaldo", "192.168.88.251 · dist. 2", "A: activa"],
], [300, 420, 380], hl_row=1, row_h=50, mono_cols=(1,)))
c.add(Note(48, 520, 1104, "Según la documentación: prueba cada 10 s, timeout de 1 s, dos timeouts y el gateway queda inalcanzable. Mira solo el próximo salto, no internet: para eso, rutas recursivas.", kind="warn", size=15))
save(c, "27-paso3.svg")

# ---------------------------------------------------------------- paso 5: túnel + /32
c = Canvas(K + " · Paso 5", "El túnel y su ruta /32: que no se coma su camino")
s, a, w = port_router(48, 160, ["ether1", "bridge"], {"ether1": BLUE, "bridge": CYAN}, "Sucursal", "", pw=90)
c.add(s)
isp = c.add(Generic(400, 160, "ISP", "gateway 192.168.1.1", icon="globe", w=250))
srv = c.add(Box(860, 150, 292, 110, "Servidor VPN", "203.0.113.10", dark=True))
c.add(Cable((48 + w, 225), isp.left(), "data"))
c.add(Cable(isp.right(), srv.left(), "data"))
c.add(f'<path d="M{48 + w} 300 C 600 360, 760 360, 1006 262" fill="none" stroke="{INK3}" stroke-width="3" stroke-dasharray="8 8"/>')
c.add(pill(640, 352, "túnel l2tp-central", "gray"))
t, h = ctable(48, 400, ["ruta", "gateway", "para qué"], [
    ["192.168.20.0/24", "l2tp-central", "la LAN de la central, por adentro del túnel"],
    ["203.0.113.10/32", "192.168.1.1", "el túnel mismo sale por el ISP"],
], [230, 200, 674], row_h=50, col_fonts=[FM, FM, FB])
c.add(t)
c.add(Note(48, 570, 1104, "La /32 hace falta cuando la ruta por defecto va por el túnel. Sin ella, los paquetes del túnel intentan entrar al túnel.", kind="warn", size=15))
save(c, "27-paso5.svg")
