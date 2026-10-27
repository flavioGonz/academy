#!/usr/bin/env python3
"""Lección 3 · teoría: option 43 llega con cada arranque; set-inform vive en la memoria del equipo."""
from _anim_unifi import *  # noqa

a = new(22, "Inform remoto", "Después de un reinicio, ¿quién le recuerda el inform?", [
    "Arranque: A recibe la IP del controlador en option 43; B la tiene por set-inform.",
    "Los dos informan a http://10.10.10.5:8080/inform.",
    "Reinician: A recibe otra vez option 43; B puede volver a unifi:8080/inform.",
    "A vuelve solo al controlador. B queda pendiente hasta otro set-inform.",
], still=3)

# controlador
CX, CY, CW, CH = 900, 270, 252, 220
a.add(a.box(CX, CY, CW, CH, A.INK, None, rx=16))
a.add(a.text(CX + 22, CY + 46, "Controlador", 21, A.WHITE, A.HEAD, 600))
a.add(a.text(CX + 22, CY + 74, "10.10.10.5", 16, SUB_DARK, A.MONO))
a.add(a.text(CX + 22, CY + 98, "TCP 8080", 16, SUB_DARK, A.MONO))

# carriles
LA, LB = 220, 440
a.add(a.text(48, LA - 18, "A · OPTION 43", 14, A.BLUE, A.MONO, 600, extra='letter-spacing="1.5"'))
a.add(a.text(48, LB - 18, "B · SET-INFORM", 14, A.AMB, A.MONO, 600, extra='letter-spacing="1.5"'))
a.add(node(a, 48, LA, 250, 76, "DHCP del sitio", "option 43", ssize=14))
a.add(node(a, 48, LB, 250, 76, "Notebook", "SSH · set-inform", ssize=14))
AP = 380
for y, n in ((LA, "AP A"), (LB, "AP B")):
    a.add(a.box(AP, y, 300, 76, A.WHITE, A.LINE, rx=14))
    a.add(ap_icon(a, AP + 40, y + 38, 20))
    a.add(a.text(AP + 74, y + 45, n, 20, A.INK, A.HEAD, 600))
a.add(line(a, [(298, LA + 38), (AP, LA + 38)], A.LINE, 2.5))
a.add(line(a, [(298, LB + 38), (AP, LB + 38)], A.LINE, 2.5, "6 6"))

# memoria de cada AP
MEMY_A, MEMY_B = LA + 90, LB + 90
a.add(a.text(AP, MEMY_A + 19, "recibe:", 14, A.GREY, A.MONO))
a.add(a.text(AP, MEMY_B + 19, "memoria:", 14, A.GREY, A.MONO))
GOOD = "10.10.10.5:8080/inform"
vis(a, pill(a, AP + 70, MEMY_A, GOOD, "info"), 0, 1)
vis(a, pill(a, AP + 70, MEMY_A, "esperando DHCP…", "grey"), 2)
s0, s1 = ph(a, 2)
at(a, pill(a, AP + 70, MEMY_A, GOOD, "info"), s0 + 14, 100, still=1)
vis(a, pill(a, AP + 80, MEMY_B, GOOD, "amb"), 0, 1)
vis(a, pill(a, AP + 80, MEMY_B, "unifi:8080/inform", "bad"), 2, 3)

# 1: arranque
s0, s1 = ph(a, 0)
token(a, [(298, LA + 38), (AP + 150, LA + 38)], s0 + 2, s0 + 10, "0x01040A0A0A05", bg=A.BLUE, hold=s0 + 11)
token(a, [(298, LB + 38), (AP + 150, LB + 38)], s0 + 8, s0 + 16, "set-inform", bg=A.AMB, hold=s0 + 17)

# líneas al controlador
EA, EB = (AP + 300, LA + 38), (AP + 300, LB + 38)
TA, TB = (CX, CY + 60), (CX, CY + CH - 50)
vis(a, line(a, [EA, TA], A.OK, 3, arrow=True), 1)
vis(a, line(a, [EB, TB], A.OK, 3, arrow=True), 1)
s0, s1 = ph(a, 1)
for k in range(2):
    token(a, [EA, (CX - 20, TA[1])], s0 + 2 + k * 10, s0 + 8 + k * 10, "inform", bg=A.CYAN, hold=s0 + 8.3 + k * 10)
    token(a, [EB, (CX - 20, TB[1])], s0 + 4 + k * 10, s0 + 10 + k * 10, "inform", bg=A.CYAN, hold=s0 + 10.3 + k * 10)

# 3: reinicio
for y in (LA, LB):
    vis(a, pill(a, AP + 290, y - 14, "reinicia", "amb", anchor="end"), 2)
s0, s1 = ph(a, 2)
token(a, [(298, LA + 38), (AP + 150, LA + 38)], s0 + 6, s0 + 13, "0x01040A0A0A05", bg=A.BLUE, hold=s0 + 14)

# 4: resultado
vis(a, line(a, [EA, TA], A.OK, 3, arrow=True), 3)
s0, s1 = ph(a, 3)
token(a, [EA, (CX - 50, TA[1] - 10)], s0 + 2, s0 + 9, "inform", bg=A.CYAN, hold=s1 - 1, still=1)
vis(a, check(a, CX - 50, TA[1] - 44, 14), 3)
token(a, [EB, (EB[0] + 120, EB[1])], s0 + 2, s0 + 8, "unifi:8080", bg=A.BAD, hold=s1 - 1, still=1)
vis(a, xmark(a, EB[0] + 195, EB[1], 14), 3)
vis(a, pill(a, EB[0] + 130, MEMY_B, "pendiente: set-inform otra vez", "bad", anchor="middle"), 3)

a.add(note(a, 48, 600, 1104, "DHCP del sitio tuyo: option 43 o DNS. Si no, set-inform y control después de cada actualización.", "info", size=16))

write(a, "3-t1.svg", "Option 43 contra set-inform después de un reinicio", mid_pcts(a))
