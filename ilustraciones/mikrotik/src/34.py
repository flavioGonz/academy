"""Lección 34 · Descubrir vecinos: principal (tres protocolos), paso 1 (leer la tabla) y paso 4 (lista de descubrimiento)."""
from _mt import *

K = "MikroTik · Lección 34"

# ------------------------------------------------------------------ 34.svg
c = Canvas(K, "Tres protocolos, una sola tabla de vecinos")
cols = [
    ("MNDP", "de MikroTik", ["UDP 5678, por broadcast", "lo usa WinBox en Neighbors", "entre equipos MikroTik"], "blue"),
    ("CDP", "de Cisco, 1994", ["multicast 01:00:0c:cc:cc:cc", "anuncio cada 60 s", "solo si hay equipos Cisco"], "gray"),
    ("LLDP", "IEEE 802.1AB", ["EtherType 0x88CC", "habla casi cualquier marca", "switches, teléfonos IP"], "cyan"),
]
x0, wcol, gap = 48, 352, 24
for i, (name, sub, items, k) in enumerate(cols):
    x = x0 + i * (wcol + gap)
    c.add(rect(x, 130, wcol, 250, WHITE, LINE2, 2, 16))
    c.add(text(x + 22, 172, name, 26, 700, {"blue": BLUE, "gray": INK2, "cyan": "#0B7FA6"}[k], FD))
    c.add(text(x + 22, 200, sub, 15, 500, INK3, FM))
    b, _ = bullets(x + 22, 246, items, wcol - 44, 16, INK2, 14, dot={"blue": BLUE, "gray": INK3, "cyan": CYAN}[k])
    c.add(b)
    c.add(arrow((x + wcol / 2, 384), (x + wcol / 2, 440), kind="flow", bend="straight"))
c.add(rect(48, 448, 1104, 92, DEEP, DEEP, 2, 16))
c.add(text(72, 486, "/ip/neighbor", 20, 600, CYAN, FM))
c.add(text(72, 518, "identidad · plataforma · versión · IP · MAC · puerto físico donde lo ve", 16, 400, "#D9E9F8", FB))
c.add(Note(48, 560, 1104, "Lo que el router aprende de los vecinos, los vecinos lo aprenden de él: nombre, modelo, versión e IP salen por cada puerto de la lista.", kind="warn", size=16))
save(c, "34.svg")

# ------------------------------------------------------------------ 34-paso1.svg
c = Canvas(K + " · Paso 1", "Leé la tabla: el puerto real está en INTERFACE")
s, _ = code(48, 128, 1104, ["/ip/neighbor/print"], title="TERMINAL · ROUTEROS 7", lh=26)
c.add(s)
rows_ = [
    [("ether3,bridge", BLUE), "192.168.88.2", "sw-rack", "switch (otra marca)", ("lldp", "pill:cyan")],
    [("ether4,bridge", INK), "192.168.88.3", "hap-oficina", "MikroTik", ("mndp", "pill:blue")],
    [("ether1", ALERT), "192.0.2.1", "router-proveedor", "?", ("lldp", "pill:alert")],
]
svg, h = ctable(48, 222, ["interface", "address", "identity", "platform", "por"], rows_, [210, 200, 220, 300, 174], row_h=48,
                col_colors=[INK, INK2, INK, INK2, INK2], col_fonts=[FM, FM, FM, FB, FM], size=16)
c.add(svg)
c.add(Note(48, 222 + h + 24, 540, "ether3 es el puerto físico; bridge es la interfaz que lo contiene. Ahí está el switch del rack, sin seguir el cable.", title="Puerto físico + bridge", kind="ok"))
c.add(Note(612, 222 + h + 24, 540, "Si ves vecinos en ether1, el router también se está anunciando hacia la WAN: eso se corrige en el paso 4.", title="Vecinos en la WAN", kind="alert"))
save(c, "34-paso1.svg")

# ------------------------------------------------------------------ 34-paso4.svg
c = Canvas(K + " · Paso 4", "Anunciate solo en los puertos que son tuyos")
cols_ = {"ether1": ALERT, "ether2": OK, "ether3": OK, "ether4": "#6E88A1", "ether5": "#6E88A1"}
svg, anc, w = port_router(145, 128, ["ether1", "ether2", "ether3", "ether4", "ether5"], cols_, name="Router", sub="lista: descubrir", pw=150, gap=30)
c.add(svg)
devs = [("ether1", "Internet", "WAN", "globe", "alert", "no se anuncia"),
        ("ether2", "Notebook", "WinBox", "laptop", "ok", "se anuncia"),
        ("ether3", "Switch", "rack", "server", "ok", "se anuncia"),
        ("ether5", "Cámara", "PoE", "camera", "gray", "no se anuncia")]
for p, t, sub, ic, k, lab in devs:
    px, py = anc[p]
    bx = px - 75
    c.add(Cable((px, py), (px, 372), "data" if k != "alert" else "alert", arrow=False))
    c.add(mini(bx, 372, 150, 76, t, sub, icon=ic, title_size=17))
    c.add(pill(px, 478, lab, k))
s, _ = code(48, 512, 1104, ["/interface/list/member/add list=descubrir interface=ether2   # y ether3, sueltos, sin el bridge",
                              "/ip/neighbor/discovery-settings/set discover-interface-list=descubrir protocol=lldp,mndp"], title="LISTA PROPIA", lh=28)
c.add(s)
save(c, "34-paso4.svg")
