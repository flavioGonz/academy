from _akv import *

# ---------- 12.svg: la carpeta del ticket
c = Canvas("Akuvox · Lección 12", "Antes de tocar nada, juntá la evidencia")
c.add(Table(48, 140, ["Archivo", "De dónde sale", "Qué responde"], [
    ["firmware.txt", "Status > Product Information", "¿qué versión corre?"],
    ["config-export.tgz", "exportar configuración", "¿cómo está configurado?"],
    ["syslog-nivel7.log", "log level 7 + reproducir", "¿qué dice el equipo?"],
    ["captura.pcap", "PCAP Start · Stop · Export", "¿qué pasó en la red?"],
    ["topologia.png", "dibujo de la obra", "¿por dónde pasa todo?"],
], [270, 340, 300], row_h=56, mono_cols=(0,)))
c.add(f'<rect x="990" y="140" width="162" height="336" rx="16" fill="{DEEP}"/>')
c.add(icon(1046, 200, "check", CYAN, 2.2, 2.2))
svg, _ = wrap(1071, 290, "Ticket que soporte no rebota", 130, 17, 600, WHITE, FB, anchor="middle")
c.add(svg)
c.add(Note(48, 510, 1104, "Si cambiás cosas antes de capturar, borrás la pista. Primero la foto del problema; después el arreglo.", title="Por qué en este orden", kind="info"))
save(c, "12.svg")

# ---------- 12-paso4.svg: la PCAP de 1 MB
c = Canvas("Akuvox · Lección 12 · Paso 4", "La captura guarda 1 MB: arrancala justo antes")
for i, (lab, kd, start, fail_in) in enumerate((("Arrancada temprano", "alert", 0.05, False), ("Arrancada justo antes", "ok", 0.55, True))):
    y = 170 + i * 190
    x0, x1 = 300, 1120
    X = lambda t: x0 + (x1 - x0) * t
    c.add(text(48, y + 30, lab, 19, 600, INK, FD))
    c.add(Mark(260, y + 24, ok=fail_in))
    c.add(f'<path d="M{x0} {y + 24}H{x1}" stroke="{LINE2}" stroke-width="3"/>')
    end = min(start + 0.3, 1)
    c.add(f'<rect x="{X(start):.0f}" y="{y + 6}" width="{X(end) - X(start):.0f}" height="36" rx="8" fill="{OK_BG if fail_in else ALERT_BG}" stroke="{OK if fail_in else ALERT}" stroke-width="2"/>')
    c.add(text((X(start) + X(end)) / 2, y + 30, "1 MB capturado", 15, 600, OK if fail_in else ALERT, FM, anchor="middle"))
    c.add(text(X(start), y + 70, "PCAP Start", 15, 600, INK2, FM, anchor="middle"))
    fx = X(0.8)
    c.add(f'<path d="M{fx:.0f} {y - 6}V{y + 54}" stroke="{WARN}" stroke-width="3" stroke-dasharray="5 4"/>')
    c.add(text(fx, y - 14, "falla", 15, 700, WARN, FM, anchor="middle"))
    if not fail_in:
        c.add(text(X(0.35) + 12, y + 70, "se llenó antes de la falla", 15, 600, ALERT, FB))
    else:
        c.add(text(X(end), y + 70, "Stop · Export", 15, 600, INK2, FM, anchor="middle"))
c.add(Step(48, 520, 4))
c.add(Note(80, 500, 1072, "Secuencia: log level 7, PCAP Start, reproducís la falla (reiniciás la cuenta SIP), PCAP Stop y Export.", kind="info"))
save(c, "12-paso4.svg")

# ---------- 12-paso5.svg: leer el REGISTER en Wireshark
c = Canvas("Akuvox · Lección 12 · Paso 5", "Qué buscar en la captura cuando no registra")
c.add("<style>text{font-variant-ligatures:none;font-feature-settings:'calt' 0,'liga' 0}</style>")
xa, xb = 240, 820
c.add(lifeline(xa, 130, 440, "Portero", "10.10.10.21"))
c.add(lifeline(xb, 130, 440, "Central", "Asterisk / FreePBX"))
c.add(msg(xa, xb, 240, "REGISTER"))
c.add(msg(xb, xa, 300, "401 · pide credencial", "logical"))
c.add(msg(xa, xb, 360, "REGISTER con clave (mal)"))
c.add(msg(xb, xa, 420, "401 o 403 · rechazo", "alert"))
c.add(Chip(xb + 90, 420, "Failed to authenticate", "alert"))
c.add(text(xb + 90, 380, "log de la central:", 15, 500, INK3, FB))
svg, spans = code_parts(48, 480, [("sip.Method == \"REGISTER\" || sip.Status-Code == 401 || sip.Status-Code == 403", "#D9E9F8")], 15)
c.add(svg)
c.add(text(48, 560, "Filtro de Wireshark del paso 5", 15, 500, INK3, FM))
c.add(Note(640, 540, 512, "Un 401 al principio es normal: es la central pidiendo la clave. El problema es el segundo rechazo.", kind="warn", size=15))
save(c, "12-paso5.svg")
