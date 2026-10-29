#!/usr/bin/env python3
"""Lección 2 · Laboratorio, paso 5: el puerto del switch que va al host tiene que estar en trunk con la VLAN 10
permitida. La VM 100 (tag 10) pregunta por ARP por su gateway: la trama sale de eno1 con tag 10; si el puerto está
en access, el switch la descarta y el ping falla; en trunk con la 10 permitida llega al gateway y vuelve.
Fuentes: tarjeta de la lección (paso 5, trunk), 802.1Q, comportamiento de ARP y ping en Linux."""
from _anim_pmx_red import *

a = new(24, "Puente VLAN-aware", "El puerto del switch: access no, trunk sí", lab=True)
a.steps([
    "La VM 100 busca su gateway: el ARP sale de eno1 con tag 10.",
    "Puerto en access: el switch no tiene la 10 ahí y descarta la trama.",
    "Puerto en trunk con la 10 permitida: el ARP llega al gateway.",
    "Vuelve la respuesta con tag 10 y el ping de la VM contesta.",
], still=3)

# host
HX, HY, HW, HH = 48, 182, 380, 230
a.add(a.box(HX, HY, HW, HH, a.WHITE, a.LINE, rx=18))
a.add(glyph(a, "server", HX + 18, HY + 16))
a.add(a.text(HX + 60, HY + 36, "pve1", 19, a.INK, a.SANS, 600))
a.add(dev(a, HX + 20, HY + 62, 196, 76, "VM 100", "192.168.10.20", tsize=18))
a.add(a.text(HX + 20, HY + 166, "net0 · VLAN Tag: 10", 15, a.OK, a.MONO, 600))
a.add(a.box(HX + 250, HY + 62, 108, 150, a.NAVY2, rx=12) + a.text(HX + 304, HY + 92, "vmbr0", 15, a.WHITE, a.MONO, 600, "middle"))
a.add(a.box(HX + 262, HY + 172, 84, 30, a.SLATE, rx=8) + a.text(HX + 304, HY + 192, "eno1", 15, a.INK, a.MONO, 600, "middle"))
a.add(line(HX + 216, HY + 100, HX + 250, HY + 100, a.BLUE, 3))
# switch
SX, SY, SW, SH = 548, 190, 250, 214
a.add(a.box(SX, SY, SW, SH, a.INK, rx=16))
a.add(a.text(SX + 20, SY + 34, "Switch", 19, a.WHITE, a.SANS, 600))
a.add(a.text(SX + 20, SY + 62, "puerto del host", 15, SKY, a.MONO))
a.add(during(a, a.box(SX + 20, SY + 80, SW - 40, 64, "#3A1F1A", rx=10) + a.text(SX + 36, SY + 106, "modo: access", 15, CORAL, a.MONO, 600)
             + a.text(SX + 36, SY + 130, "VLAN 1", 15, CORAL, a.MONO, 600), 0, 50))
a.add(during(a, a.box(SX + 20, SY + 80, SW - 40, 64, "#0F3A2C", rx=10) + a.text(SX + 36, SY + 106, "modo: trunk", 15, MINT, a.MONO, 600)
             + a.text(SX + 36, SY + 130, "permitidas: 10, 20", 15, MINT, a.MONO, 600), 50, 100, still=1))
a.add(a.text(SX + 20, SY + 180, "VLAN 10 → gateway", 15, SKY, a.MONO))
# gateway
GX, GY = 900, 220
a.add(dev(a, GX, GY, 252, 92, "Router", "gateway VLAN 10", icon="globe", sub2="192.168.10.1"))
# cables
ENO = (HX + 346, HY + 187)
SPI = (SX, SY + 112)
SPO = (SX + SW, SY + 112)
GWI = (GX, GY + 46)
a.add(path(f"M{ENO[0]} {ENO[1]} C{ENO[0] + 70} {ENO[1]} {SPI[0] - 70} {SPI[1]} {SPI[0]} {SPI[1]}", a.BLUE, 5))
a.add(path(f"M{SPO[0]} {SPO[1]} C{SPO[0] + 50} {SPO[1]} {GWI[0] - 50} {GWI[1]} {GWI[0]} {GWI[1]}", a.BLUE, 3))
VMO = (HX + 216, HY + 100)
BR = (HX + 304, HY + 140)


def mid(p, q, f):
    return (p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f)


# 1 · ARP sale con tag 10
go(a, "ARP ¿.1?", [VMO, BR], 3, 7, a.GREY, hold=0.3)
go(a, "ARP · tag 10", [BR, ENO, mid(ENO, SPI, .5)], 8, 14, a.OK, hold=8)
# 2 · descartado en access
go(a, "ARP · tag 10", [mid(ENO, SPI, .5), (SPI[0] - 10, SPI[1])], 28, 32, a.OK, hold=1)
at(a, xmark(a, SPI[0] - 6, SPI[1] - 44), 33, 50)
at(a, chip(a, SPI[0] - 20, SPI[1] + 40, "descartada", "bad", anchor="end"), 33, 50)
# 3 · trunk: pasa al gateway
go(a, "ARP · tag 10", [mid(ENO, SPI, .5), SPI, SPO], 53, 59, a.OK, hold=0.3)
go(a, "ARP ¿.1?", [SPO, GWI], 60, 64, a.GREY, hold=2)
# 4 · vuelve
go(a, "ARP: .1 es mía", [GWI, SPO], 77, 81, a.GREY, hold=0.3)
go(a, "respuesta · tag 10", [SPO, SPI, ENO, BR], 82, 89, a.OK, hold=0.3)
go(a, "ping OK", [BR, VMO], 90, 93, a.OK, hold=6)

# terminal de la VM
TX, TY, TW, TH = 48, 448, 560, 150
a.add(a.box(TX, TY, TW, TH, a.INK, rx=14))
a.add(a.text(TX + 20, TY + 28, "CONSOLA DE LA VM 100", 13, SKY, a.MONO, 400, extra='letter-spacing="1.8"'))
at(a, tline(a, TX + 20, TY + 60, "$ ping 192.168.10.1", MINT), 2, 100, still=1)
at(a, tline(a, TX + 20, TY + 88, "From 192.168.10.20 icmp_seq=1", CORAL), 36, 50)
at(a, tline(a, TX + 20, TY + 114, "  Destination Host Unreachable", CORAL), 36, 50)
at(a, tline(a, TX + 20, TY + 88, "64 bytes from 192.168.10.1: icmp_seq=1", MINT), 92, 100, still=1)
at(a, tline(a, TX + 20, TY + 114, "64 bytes from 192.168.10.1: icmp_seq=2", MINT), 95, 100, still=1)
# nota a la derecha
a.add(during(a, note(a, 640, 448, 512, 150, "Síntoma típico", ["El host y las otras VM andan; la VM con tag", "no llega ni al gateway. bridge vlan show está", "bien: el problema está en el puerto del switch."], "bad"), 25, 50))
a.add(during(a, note(a, 640, 448, 512, 150, "Cómo se confirma", ["En el switch, la MAC de la VM 100 aparece", "aprendida en la VLAN 10 del puerto del host.", "Sumar una VLAN nueva es permitirla en el trunk."], "ok"), 50, 100, still=1))
a.add(during(a, note(a, 640, 448, 512, 150, "Lo que sale del host", ["La VM manda tramas comunes; el bridge les pone", "el tag 10 al salir por eno1. El switch tiene que", "aceptar ese tag en el puerto del host."], "info"), 0, 25))

status(a, 640, [
    (0, 25, "Del host sale bien: el tag lo pone vmbr0 en la placa física.", a.INK, 0),
    (25, 50, "Un puerto access no espera etiquetas de otra VLAN: la trama no pasa.", a.BAD, 0),
    (50, 75, "En trunk, el switch lee el tag y la trama entra a la VLAN 10.", a.OK, 0),
    (75, 100, "Ida y vuelta con tag 10: la VM tiene red sin saber nada de VLAN.", a.OK, 1),
])

write(a, 2, "l2", "El puerto del switch: access no, trunk sí",
      "Animación en cuatro tiempos con el host pve1 (VM 100 en 192.168.10.20 con VLAN Tag 10, vmbr0 y eno1), el switch con el puerto que va al host y el router gateway de la VLAN 10 en 192.168.10.1, más la consola de la VM. "
      "1: la VM hace ping a 192.168.10.1 y primero pregunta por ARP por su gateway; el bridge le pone tag 10 a la trama al salir por eno1. "
      "2: si el puerto del switch está en access con la VLAN 1, no tiene la VLAN 10 y descarta la trama; el ping muestra Destination Host Unreachable. "
      "3: con el puerto en trunk y las VLAN 10 y 20 permitidas, el switch lee el tag, la trama entra a la VLAN 10 y el ARP llega al gateway. "
      "4: la respuesta vuelve con tag 10 hasta eno1, el bridge la entrega sin tag a la VM y el ping contesta 64 bytes from 192.168.10.1. "
      "Para confirmarlo en el switch, la MAC de la VM 100 aparece aprendida en la VLAN 10 del puerto del host.",
      [10, 40, 62, 90, 97])
