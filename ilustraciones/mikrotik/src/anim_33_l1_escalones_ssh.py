#!/usr/bin/env python3
"""Lección 33 (Reglas de protección) · Laboratorio paso 5: cuatro conexiones SSH seguidas suben los escalones de las listas hasta la lista negra."""
from _anim_r20_31 import *

a, _ = nuevo(26, "MIKROTIK · REGLAS DE PROTECCIÓN · PASO 5", "Cuatro conexiones SSH, cuatro escalones",
             ["Conexión 1: no está en ninguna lista. Entra a connection1 y se acepta.",
              "Conexión 2: estaba en connection1, sube a connection2. Se acepta.",
              "Conexión 3: sube a connection3. Se acepta, con 9 claves más para probar.",
              "Conexión 4: pasa a bruteforce_blacklist por 1 día. El accept ya no la deja: drop."], still=3)

dev(a, 48, 196, 230, 96, "Notebook WAN", "192.0.2.50", "ssh admin@IP-WAN", ssize=14)

# listas
LX, LW = 340, 470
a.add(a.box(LX, 186, LW, 300, a.INK, rx=18))
a.add(a.text(LX + 20, 218, "/ip/firewall/address-list", 15, SKY, a.MONO))
LST = [("connection1", "5m"), ("connection2", "15m"), ("connection3", "1h"), ("bruteforce_blacklist", "1d")]
ly = []
for i, (n, to) in enumerate(LST):
    y = 236 + i * 58
    ly.append(y + 23)
    a.add(a.box(LX + 16, y, LW - 32, 46, a.NAVY2, rx=9))
    a.add(a.text(LX + 32, y + 29, n, 15, a.WHITE, a.MONO, 600))
    a.add(a.text(LX + LW - 32, y + 29, f"timeout {to}", 14, SKY, a.MONO, 400, "end"))
ENTRY = [(8, a.CYAN), (33, a.CYAN), (58, GOLD), (83, ROSE)]
for i, (t, c) in enumerate(ENTRY):
    en(a, a.pill(LX + 224, ly[i] - 13, "192.0.2.50", a.INK, c, 13, 26), t, 100, still=1)
    en(a, ring(a, LX + 13, ly[i] - 26, LW - 26, 52, c, rx=11, sw=3), t, t + 14)

# conexiones
def conn(k, t0, ok):
    go(a, f"SSH #{k}", [(278, 244), (LX - 8, 244)], t0, t0 + 4, hold=3, bg=a.BLUE if ok else a.BAD, size=14)
for k, t0, ok in [(1, 2, True), (2, 27, True), (3, 52, True), (4, 77, False)]:
    conn(k, t0, ok)

# resultados
a.add(a.box(850, 186, 302, 300, a.WHITE, a.LINE, rx=16))
a.add(a.text(870, 218, "Resultado", 16, a.INK, a.SANS, 600))
RES = [("#1 aceptada", "hasta 9 claves", a.OK, 9), ("#2 aceptada", "9 más", a.OK, 34),
       ("#3 aceptada", "9 más: 27 en total", a.OK, 59), ("#4 drop", "lista negra, 1 día", a.BAD, 84)]
for i, (r, s_, c, t) in enumerate(RES):
    y = 252 + i * 58
    en(a, a.text(870, y + 6, r, 16, c, a.MONO, 600) + a.text(870, y + 30, s_, 15, a.TXT, a.SANS), t, 100, still=1)
en(a, mark(a, 1120, 252 + 3 * 58 + 12, ok=False), 84, 100, still=1)

# nota de admins y regla
a.add(note(a, 48, 506, 560, 92, "La lista admins va primero", ["198.51.100.7 se acepta antes de todo esto: si", "probás desde la oficina, no te bloqueás."], "amb"))
a.add(note(a, 628, 506, 524, 92, "Las reglas de lista no frenan", ["Anotan y dejan seguir: por eso van en orden", "inverso y al final hace falta el drop."], "info"))

narr(a, [
    (0, 25, "La regla de la primera etapa no pide lista: cualquier conexión nueva al 22 la cumple.", a.TXT),
    (25, 50, "Cada conexión nueva en menos de 5 minutos sube un escalón.", a.TXT),
    (50, 75, "SSH acepta 9 intentos por conexión: el atacante rápido llega a 27.", a.AMB),
    (75, 100, "Cuenta conexiones, no logins fallidos: un login bueno también suma.", a.BAD),
], y=636, still_idx=3)

escribir(a, "33-l1.svg", "Listas SSH por etapas",
         "Animación en cuatro tiempos con la notebook WAN (192.0.2.50) que abre conexiones SSH al router, las cuatro address-lists con su timeout (connection1 5m, connection2 15m, "
         "connection3 1h y bruteforce_blacklist 1d) y una columna de resultado. 1: la primera conexión no está en ninguna lista, entra a connection1 y se acepta, con hasta 9 intentos de clave. "
         "2: la segunda, como ya estaba en connection1, sube a connection2 y se acepta. 3: la tercera sube a connection3 y se acepta; van 27 intentos posibles. "
         "4: la cuarta pasa a bruteforce_blacklist por un día y el accept ya no la deja pasar: la descarta el drop. Abajo, dos notas: la lista admins va primero para no bloquearte, "
         "y las reglas de lista anotan y dejan seguir, por eso van en orden inverso y terminan en un drop.",
         [12, 38, 64, 80, 94])
