#!/usr/bin/env python3
"""Teoría lección 1 (Dónde vive): el controlador empuja la configuración; si desaparece, la red sigue
con lo último que recibió, pero nadie puede cambiar nada y el portal deja de autenticar.
Salida: site2/ilustraciones/omada/1-t1.svg"""
import sys
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _anim_omada import *  # noqa

a = nueva(20, "CONTROLADOR", "Si el controlador desaparece, la red sigue")
F = a.steps([
    "El controlador guarda la configuración del sitio y la empuja a cada equipo.",
    "Cada equipo se queda con lo que recibió. Los clientes navegan.",
    "Se cae el controlador: la red anda igual, con la última configuración.",
    "Pero nadie puede cambiar nada, y el portal no autentica a clientes nuevos.",
], still=3)

# --- controlador y su configuración
CX, CY, CW, CH = 48, 196, 300, 84
a.add(nodo(a, CX, CY, CW, CH, "Controlador", "local, nube o integrado"))
a.add(a.box(CX, 304, CW, 236, a.WHITE, a.LINE))
a.add(a.text(CX + 20, 340, "Configuración del sitio", 17, a.INK, a.SANS, 600))
for i, s in enumerate(["redes y VLAN", "WiFi y SSID", "puertos", "ACL", "portal"]):
    a.add(a.text(CX + 34, 378 + i * 34, s, 17, a.TXT, a.MONO))
    a.add(f'<circle cx="{CX + 22}" cy="{372 + i * 34}" r="4" fill="{a.CYAN}"/>')

# --- equipos
DX, DW, DH = 520, 250, 72
DEV = [("Gateway", "ER", 196), ("Switch", "JetStream", 316), ("EAP", "access point", 436)]
for t, s, y in DEV:
    a.add(nodo(a, DX, y, DW, DH, t, s, dark=False, tsize=19))
a.add(a.text(DX, 548, "gestión: UDP 29810 a TCP 29817", 15, a.GREY, a.MONO))

# líneas de gestión controlador → equipos (punteadas, lógicas)
for _, _, y in DEV:
    a.add(linea(a, CX + CW, CY + CH / 2, DX, y + DH / 2, a.GREY, 2, "5 7"))

# --- clientes
KX, KW = 930, 222
a.add(nodo(a, KX, 196, KW, 72, "Internet", dark=False, tsize=19))
a.add(nodo(a, KX, 380, KW, 72, "Notebook", "ya conectada", dark=False, tsize=19))
a.add(nodo(a, KX, 500, KW, 72, "Celular nuevo", "entra al portal", dark=False, tsize=19))
a.add(linea(a, DX + DW, 232, KX, 232, a.BLUE, 3))
a.add(linea(a, DX + DW, 472, KX, 416, a.BLUE, 3))
a.add(linea(a, DX + DW, 472, KX, 536, a.BLUE, 3))

# fase 1: la configuración viaja a cada equipo
for i, (_, _, y) in enumerate(DEV):
    t0 = F[0][0] + 3 + i * 4
    viaje(a, paquete(a, "config", a.BLUE, 14, 28), CX + CW + 40, CY + CH / 2, DX - 40, y + DH / 2, t0, t0 + 8, hold=2)
# equipos con config recibida (desde fase 2, también en el cuadro fijo)
for i, (_, _, y) in enumerate(DEV):
    en(a, ok(a, DX + DW - 26, y + DH / 2, 13), F[0][0] + 11 + i * 4, 100, still=1)

# tráfico de clientes: fases 2 a 4
for k in range(3):
    t0 = F[1][0] + 2 + k * 18
    viaje(a, '<circle r="7" fill="#17A8D4"/>', KX - 6, 416, DX + DW + 8, 472, t0, t0 + 5, hold=0.5)
    viaje(a, '<circle r="7" fill="#17A8D4"/>', DX + DW + 8, 232, KX - 6, 232, t0 + 6, t0 + 11, hold=0.5)
en(a, chip(a, KX + KW - 14, 456, "navega", a.OK, a.OKBG, anchor="end", h=24, size=13), F[1][0], 100, still=1)

# fase 3+: controlador caído
caido = (a.box(CX - 4, CY - 4, CW + 8, CH + 8, "none", a.BAD, rx=16, sw=3)
         + chip(a, CX + CW - 12, CY + 14, "caído", a.BAD, a.BADBG, anchor="end"))
en(a, caido, F[2][0], 100, still=1)
for _, _, y in DEV:
    en(a, bad(a, (CX + CW + DX) / 2, (CY + CH / 2 + y + DH / 2) / 2, 12), F[2][0], 100, still=1)

# fase 4: cambio que no llega y portal que no autentica
en(a, chip(a, CX, 560, "cambio nuevo: no llega a nadie", a.BAD, a.BADBG, size=14, stroke=a.BAD), F[3][0], 100, still=1)
en(a, chip(a, KX + KW - 14, 578, "no autentica", a.BAD, a.BADBG, anchor="end", h=26, size=13), F[3][0], 100, still=1)

pie(a, F, [
    "Los equipos hablan con el controlador por puertos propios de Omada.",
    "La configuración ya está en cada equipo: el tráfico no pasa por el controlador.",
    "Lo que ya estaba configurado sigue funcionando.",
    "Lo que necesita el controlador corriendo se frena hasta que vuelva.",
], still=3, colores=[a.INK, a.INK, a.OK, a.BAD])

salida(a, 1, 1, "Si el controlador desaparece, la red sigue",
       "Animación en cuatro tiempos. 1: el controlador guarda la configuración del sitio (redes y VLAN, WiFi, puertos, ACL, portal) "
       "y la empuja al gateway, al switch y al EAP por los puertos de Omada, del UDP 29810 al TCP 29817. 2: cada equipo queda con "
       "lo que recibió y los clientes navegan sin pasar por el controlador. 3: el controlador se cae y la red sigue andando con la última "
       "configuración. 4: un cambio nuevo no llega a ningún equipo y un celular nuevo no puede autenticarse en el portal.",
       [12, 37, 62, 88])
