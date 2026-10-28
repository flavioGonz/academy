#!/usr/bin/env python3
"""Lección 30 (DNS en MikroTik) · Laboratorio paso 5: DoH en el router. Resuelve el nombre del servidor con servers, abre HTTPS al 443 y, si se cae, no hay respaldo."""
from _anim_r20_31 import *

a, _ = nuevo(26, "MIKROTIK · DNS EN MIKROTIK · PASO 5", "DoH: todo por un caño, y sin plan B",
             ["El router resuelve el nombre del servidor DoH con sus servers comunes.",
              "Abre HTTPS al 443 y, con verify-doh-cert=yes, revisa el certificado.",
              "La consulta de la notebook viaja cifrada por esa conexión y vuelve.",
              "Si el servidor DoH no responde: SERVFAIL. No vuelve a servers."], still=2)

XN, XR, XS, XD = 165, 475, 785, 1035
head(a, XN, 178, "Notebook", "192.168.88.10", w=230)
head(a, XR, 178, "Router", "use-doh-server", w=230, kind="router")
head(a, XS, 178, "servers", "1.1.1.1, 9.9.9.9 · 53", w=230, kind="isp")
head(a, XD, 178, "Servidor DoH", "cloudflare-dns.com", w=234, kind="isp")
for x in (XN, XR, XS, XD):
    lifeline(a, x, 248, 470)

# 1. resolver el nombre del servidor DoH
msg(a, XR, XS, 290, "A? cloudflare-dns.com", 3, 25)
msg(a, XS, XR, 330, "dirección del servidor DoH", 9, 25, a.OK)
# 2. HTTPS y certificado
msg(a, XR, XD, 290, "TLS · TCP 443 · queda abierta", 28, 75, a.INK, still=1)
msg(a, XD, XR, 330, "certificado", 33, 50, a.INK)
en(a, a.pill(XR + 14, 352, "verify-doh-cert=yes: válido", a.OK, a.OKBG, 13, 26), 38, 50)
en(a, f'<rect x="{XR}" y="276" width="{XD - XR}" height="28" rx="14" fill="{a.CYAN}" opacity=".14"/>', 40, 75, still=1)
# 3. la consulta de la notebook
msg(a, XN, XR, 390, "A? mikrotik.com · 53", 52, 75, still=1)
msg(a, XR, XD, 390, "cifrada por HTTPS", 56, 75, a.CYAN, still=1)
msg(a, XD, XR, 430, "respuesta cifrada", 61, 75, a.CYAN, still=1)
msg(a, XR, XN, 430, "NOERROR", 66, 75, a.OK, still=1)
en(a, a.text(XS, 470, "servers no ve la consulta", 14, a.GREY, a.SANS, 600, "middle"), 58, 75, still=1)
# 4. se cae el DoH
en(a, a.box(XD - 117, 262, 234, 120, a.BADBG, a.BAD, rx=14, sw=2) + a.text(XD, 316, "no responde", 17, a.BAD, a.HEAD, 600, "middle"), 77, 100)
msg(a, XN, XR, 390, "A? mikrotik.com", 78, 100)
msg(a, XR, XD, 400, "por HTTPS", 82, 100, a.GREY, lost=True, frac=0.78)
msg(a, XR, XN, 440, "SERVFAIL", 89, 100, a.BAD)
en(a, mark(a, XS, 420, ok=False, r=14) + a.text(XS, 452, "no usa servers de respaldo", 14, a.BAD, a.SANS, 600, "middle"), 84, 100)

# log
a.add(a.box(48, 496, 1104, 96, a.INK, rx=12))
a.add(a.text(66, 524, '/log/print follow where topics~"dns"', 14, SKY, a.MONO))
en(a, a.text(66, 556, "(sin errores)", 15, MINT, a.MONO), 0, 77, still=1)
en(a, a.text(66, 556, "DoH server connection error: timeout connecting", 15, ROSE, a.MONO, 600), 82, 100)
en(a, a.text(66, 580, "para volver atrás: /ip/dns/set use-doh-server=\"\" verify-doh-cert=no", 15, a.WHITE, a.MONO), 86, 100)

narr(a, [
    (0, 25, "Por eso servers queda cargado: el router lo necesita para encontrar al servidor DoH.", a.TXT),
    (25, 50, "Si el certificado no valida, el log lo dice con el tema dns.", a.TXT),
    (50, 75, "La LAN sigue preguntando al router por el 53; el cifrado va del router para arriba.", a.TXT),
    (75, 100, "Con DoH activo, si ese servidor se cae, toda la LAN se queda sin nombres.", a.BAD),
], still_idx=2)

escribir(a, "30-l2.svg", "DoH en el router",
         "Animación en cuatro tiempos con cuatro líneas de vida: la notebook (192.168.88.10), el router con use-doh-server, los servers comunes (1.1.1.1 y 9.9.9.9 por el puerto 53) "
         "y el servidor DoH cloudflare-dns.com. Abajo, el log con el tema dns. 1: el router pregunta a servers la dirección de cloudflare-dns.com. "
         "2: abre una conexión TLS al puerto 443 del servidor DoH y, con verify-doh-cert=yes, valida su certificado. "
         "3: la notebook le pregunta al router por el 53 como siempre; el router manda la consulta cifrada por HTTPS, recibe la respuesta y le contesta NOERROR. "
         "4: el servidor DoH deja de responder: el router no vuelve a servers, la notebook recibe SERVFAIL y el log muestra DoH server connection error: timeout connecting.",
         [12, 40, 64, 72, 94])
