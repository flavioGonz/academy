"""Lección 22 · IPsec entre marcas."""
from _comun_12_22 import *

K = "MikroTik"

# ---------------------------------------------------------------- principal: fases y policies espejo
c = Canvas(K, "IPsec: dos fases y policies que se espejan")
a = c.add(Box(48, 150, 250, 124, "Sitio A · MikroTik", "203.0.113.10", dark=True))
b = c.add(Box(902, 150, 250, 124, "Sitio B · otra marca", "198.51.100.20", dark=True))
X1, X2 = 318, 882
c.add(pipe(X1, 136, X2 - X1, 152, BLUE, None, None, .07))
c.add(text(600, 166, "Fase 1 · IKE: profile + peer + identity", 16, 600, BLUE, FM, anchor="middle"))
c.add(text(600, 274, "UDP 500 / 4500 · se ve en active-peers", 14, 500, INK3, FM, anchor="middle"))
c.add(pipe(X1 + 40, 186, X2 - X1 - 80, 62, OK, None, None, .14))
c.add(text(600, 223, "Fase 2 · SA ESP: proposal + policy", 16, 600, OK, FM, anchor="middle"))
c.add(Cable(a.right(), (X1, 212), "data", arrow=False))
c.add(Cable((X2, 212), b.left(), "data", arrow=False))

# policies espejo
c.add(Label(48, 336, "POLICY EN A", 14, 600, INK3, FM))
c.add(Label(1152, 336, "POLICY EN B", 14, 600, INK3, FM, anchor="end"))
rowsA = [("src-address", "192.168.88.0/24"), ("dst-address", "10.10.10.0/24")]
rowsB = [("local", "10.10.10.0/24"), ("remota", "192.168.88.0/24")]
for i in range(2):
    y = 352 + i * 74
    c.add(panel(48, y, 420, 60, None, "info"))
    c.add(mono(68, y + 37, rowsA[i][0], 15, INK3, 500))
    c.add(mono(448, y + 37, rowsA[i][1], 17, INK, 600, anchor="end"))
    c.add(panel(732, y, 420, 60, None, "info"))
    c.add(mono(752, y + 37, rowsB[i][0], 15, INK3, 500))
    c.add(mono(1132, y + 37, rowsB[i][1], 17, INK, 600, anchor="end"))
c.add(Cable((474, 382), (726, 456), "ok", arrow=False))
c.add(Cable((474, 456), (726, 382), "ok", arrow=False))
c.add(Chip(600, 425, "= espejo", "ok", anchor="middle"))
c.add(Note(48, 520, 1104, "Cifrado, hash, grupo DH, lifetimes y redes tienen que coincidir en las dos puntas. Primero la tabla firmada por los dos técnicos, después el túnel.", kind="warn"))
save(c, "22.svg")

# ---------------------------------------------------------------- paso 1: la tabla
c = Canvas(K + " · Paso 1", "La tabla que firman las dos puntas")
c.add(Table(48, 130, ["fase", "parámetro", "valor acordado", "pieza en RouterOS"], [
    ["1", "intercambio", "IKEv2", "peer (exchange-mode=ike2)"],
    ["1", "autenticación", "clave precompartida", "identity"],
    ["1", "cifrado · hash", "AES-256 · SHA-256", "profile"],
    ["1", "grupo DH · lifetime", "14 (modp2048) · 1d", "profile"],
    ["2", "cifrado · hash", "AES-256-CBC · SHA-256", "proposal"],
    ["2", "PFS · lifetime", "grupo 14 · 1h", "proposal"],
    ["2", "redes", "192.168.88.0/24 ↔ 10.10.10.0/24", "policy (tunnel=yes)"],
], [80, 250, 400, 374], mono_cols=(0, 2, 3), row_h=48))
c.add(Note(48, 532, 540, "La otra punta (pfSense u otra marca) carga los mismos valores con las redes al revés.", kind="ok", size=15))
c.add(Note(612, 532, 540, "DPD activo y NAT-T si hay NAT. Relojes con NTP en los dos lados.", kind="info", size=15))
save(c, "22-paso1.svg")

# ---------------------------------------------------------------- paso 4: NAT y FastTrack
c = Canvas(K + " · Paso 4", "Que el tráfico al túnel no pase por NAT ni FastTrack")


def lane(y, kind, title, boxes, result, res_kind):
    c.add(panel(48, y, 1104, 136, None, kind))
    c.add(text(68, y + 30, title, 17, 600, {"alert": ALERT, "ok": OK, "warn": WARN}[kind], FD))
    x = 68
    for i, (t, s) in enumerate(boxes):
        w = 236
        c.add(f'<rect x="{x}" y="{y + 50}" width="{w}" height="66" rx="12" fill="{WHITE}" stroke="{LINE2}" stroke-width="1.5"/>')
        c.add(text(x + 16, y + 77, t, 15, 600, INK, FM))
        c.add(text(x + 16, y + 101, s, 14, 400, INK3, FB))
        if i < len(boxes) - 1:
            c.add(Arrow((x + w + 4, y + 83), (x + w + 22, y + 83), bend="straight"))
        x += w + 26
    c.add(pill(x, y + 50, 1132 - x, 66, result, {"ok": OK, "alert": ALERT, "warn": WARN}[res_kind], WHITE, 15, FB, 600))


lane(130, "alert", "Sin bypass de NAT", [("PC 192.168.88.x", "va a 10.10.10.x"), ("masquerade", "cambia el origen"),
                                          ("policy", "origen ya no es 192.168.88.0/24")], "no se cifra", "alert")
lane(286, "ok", "Con accept arriba de todo en srcnat", [("PC 192.168.88.x", "va a 10.10.10.x"), ("nat: accept", "no NAT al túnel"),
                                                        ("policy coincide", "action=encrypt")], "entra al túnel", "ok")
lane(442, "warn", "FastTrack sin bypass en forward", [("conexión", "ya establecida"), ("fasttrack", "saltea las policies"),
                                                      ("síntoma", "lento o con pérdidas")], "se arregla con Torch", "warn")
c.add(Label(48, 620, "Si probaste antes del bypass, borrá las conexiones viejas: /ip/firewall/connection/remove", 16, 500, INK2))
save(c, "22-paso4.svg")

# ---------------------------------------------------------------- paso 6: diagnóstico
c = Canvas(K + " · Paso 6", "Diagnosticá por capas y leé el síntoma")
ladder = [("Fase 1", "/ip/ipsec/active-peers/print"), ("Fase 2", "/ip/ipsec/policy/print detail  (ph2-state)"),
          ("Contadores", "/ip/ipsec/installed-sa/print"), ("Mensajes", "/log/print where topics~\"ipsec\"")]
c.add(Label(48, 140, "DÓNDE MIRAR, EN ORDEN", 14, 600, INK3, FM))
for i, (t, cmd) in enumerate(ladder):
    y = 156 + i * 70
    c.add(panel(48, y, 470, 58, None, "info"))
    c.add(badge(80, y + 29, i + 1))
    c.add(text(110, y + 25, t, 16, 600, INK, FD))
    c.add(mono(110, y + 47, cmd, 13, INK2, 500))
c.add(Label(560, 140, "QUÉ SIGNIFICA CADA SÍNTOMA", 14, 600, INK3, FM))
syms = [
    ("no suitable proposal / NO-PROPOSAL-CHOSEN", "parámetros distintos: tabla vs log (local:remoto)", "alert"),
    ("phase1 negotiation failed due to time up", "comunicación: UDP 500/4500, IP del peer, NAT", "alert"),
    ("fases arriba, sin tráfico", "falta el bypass de NAT o está mal ubicado", "warn"),
    ("se arregla con Torch", "FastTrack", "warn"),
    ("ping en un solo sentido", "firewall de alguno de los dos lados", "warn"),
]
for i, (s, m, k) in enumerate(syms):
    y = 156 + i * 70
    bg, fg = {"alert": (ALERT_BG, ALERT), "warn": (WARN_BG, WARN)}[k]
    c.add(f'<rect x="560" y="{y}" width="592" height="58" rx="12" fill="{bg}"/>')
    c.add(text(578, y + 25, s, 15, 600, fg, FM))
    c.add(text(578, y + 47, "→ " + m, 15, 500, INK, FB))
c.add(Note(48, 530, 470, "Túnel sano: un peer activo, ph2-state established y dos SA por router.", kind="ok", size=15))
c.add(Note(560, 530, 592, "Para ver cada algoritmo rechazado en el log: /system/logging/add topics=ipsec,!debug", kind="info", size=15))
save(c, "22-paso6.svg")
