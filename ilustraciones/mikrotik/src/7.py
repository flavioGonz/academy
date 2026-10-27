"""Lección 7 · Actualizar en orden: principal + pasos 3 y 4."""
from _mt import *

K = "MikroTik · Lección 7"

# ------------------------------------------------------------------ 7.svg principal
c = Canvas(K, "Backup, RouterOS, RouterBOOT: en ese orden")
st = [("Backup", "export y .backup", "save"), ("RouterOS", "update/install", "reinicia solo"), ("RouterBOOT", "routerboard/upgrade", ""),
      ("Reinicio", "/system/reboot", ""), ("Verificar", "current = upgrade", "")]
for i, (t, s, extra) in enumerate(st):
    x = 48 + i * 224
    hl = CYAN if i == 2 else (OK if i == 4 else LINE2)
    c.add(rect(x, 150, 200, 132, DEEP if i == 2 else WHITE, hl, 2.5 if i in (2, 4) else 2, 16))
    c.add(Step(x + 30, 182, i + 1, CYAN if i != 4 else OK))
    c.add(text(x + 20, 236, t, 20, 600, WHITE if i == 2 else INK, FD))
    c.add(text(x + 20, 262, s, 14, 500, "#9FC3E3" if i == 2 else BLUE, FM))
    if i < 4:
        c.add(arrow((x + 202, 216), (x + 222, 216)))
c.add(text(48 + 2 * 224, 310, "el paso que más se olvida", 15, 600, CYAN, FB))
# canales
c.add(caption(48, 362, "Canal en producción"))
ch = [("long-term", "ok"), ("stable", "ok"), ("testing", "alert"), ("development", "alert")]
x = 48
for n, k in ch:
    w = len(n) * 9.2 + 26
    c.add(pill(x, 400, n, k, anchor="start"))
    x += w + 12
c.add(text(x + 8, 400, "testing y development: nunca en un cliente", 16, 500, ALERT, FB))
c.add(Note(48, 440, 540, "No se salta directo a la última: primero 7.12.1 y recién después aparecen las nuevas en el canal.", title="Si viene de RouterOS 6", kind="warn", size=16))
c.add(Note(612, 440, 540, "Desde 7.23 el chequeo de actualizaciones usa HTTPS: el router necesita salir a internet por TCP 443.", title="Si no encuentra actualizaciones", kind="info", size=16))
c.add(Note(48, 568, 1104, "No cortes la energía mientras actualiza. En un sitio remoto: alguien en el lugar o un plan de rescate (Netinstall).", kind="alert", size=16))
save(c, "7.svg")

# ------------------------------------------------------------------ 7-paso3.svg
c = Canvas(K + " · Paso 3", "Elegí el canal antes de buscar la actualización")
chs = [("long-term", "Sale poco y trae solo arreglos críticos. Para el equipo que no se puede caer.", "ok", "producción"),
       ("stable", "Cada pocos meses, con funciones nuevas ya probadas.", "ok", "producción"),
       ("testing", "Cada pocas semanas, con prueba interna básica.", "alert", "no en clientes"),
       ("development", "Para entusiastas y laboratorio.", "alert", "no en clientes")]
for i, (n, d, k, tag) in enumerate(chs):
    y = 140 + i * 84
    bg, fg = (OK_BG, OK) if k == "ok" else (ALERT_BG, ALERT)
    c.add(rect(48, y, 700, 72, WHITE, fg if i == 0 else LINE2, 2.5 if i == 0 else 1.5, 14))
    c.add(mark(84, y + 36, k == "ok"))
    c.add(text(120, y + 30, n, 18, 600, INK, FM))
    c.add(text(120, y + 56, d, 15, 400, INK2, FB))
    c.add(pill(730, y + 42, tag, k, anchor="end") if False else "")
    w = len(tag) * 8.4 + 26
    c.add(pill(728 - w, y + 32, tag, k, anchor="start", mono=False))
lines = [("/system/package/update/set channel=long-term", "#D9E9F8"),
         ("/system/package/update/check-for-updates", "#D9E9F8"),
         ("/system/package/update/install", CYAN_T),
         ("# descarga, instala y reinicia", GRAY_T)]
t, h = code(780, 140, 372, [(s[0].replace("/system/package/update", "…/update"), s[1]) for s in lines], title="TERMINAL")
c.add(t)
c.add(text(780, 140 + h + 26, "…/update = /system/package/update", 14, 500, INK3, FM))
c.add(Note(48, 484, 1104, "Entre long-term y stable no hay un ganador: lo importante es no quedarse años sin actualizar. Según Eclypsium, unos 300.000 MikroTik seguían vulnerables a fallas que ya tenían parche.", kind="info", size=16))
save(c, "7-paso3.svg")

# ------------------------------------------------------------------ 7-paso4.svg
c = Canvas(K + " · Paso 4", "Después de RouterOS, el bootloader queda atrás")
rows_ = [["Antes de empezar", ("vieja", "pill:gray"), ("vieja", "pill:gray"), ("vieja", "pill:gray"), ("al día con su versión", OK)],
         ["Después de install", ("nueva", "pill:blue"), ("vieja", "pill:warn"), ("nueva", "pill:blue"), ("falta RouterBOOT", WARN)],
         ["Después de upgrade y reboot", ("nueva", "pill:blue"), ("nueva", "pill:ok"), ("nueva", "pill:ok"), ("listo", OK)]]
t, h = ctable(48, 140, ["Momento", "RouterOS", "current-firmware", "upgrade-firmware", "Estado"], rows_, [290, 170, 230, 230, 184], row_h=62,
              col_fonts=[FB, FM, FM, FM, FB])
c.add(t)
lines = [("/system/routerboard/print", "#D9E9F8"), ("/system/routerboard/upgrade", CYAN_T), ("/system/reboot", CYAN_T)]
tt, th = code(48, 140 + h + 26, 540, lines, title="TERMINAL")
c.add(tt)
c.add(Note(612, 140 + h + 26, 540, "current-firmware es el RouterBOOT que corre hoy. upgrade-firmware es el que trae el RouterOS instalado. Cuando no coinciden, falta el upgrade y un reinicio.", title="Cómo leerlo", kind="info", size=16))
c.add(text(48, 140 + h + 26 + th + 34, "Anotá en el legajo: versión de RouterOS, de RouterBOOT, canal y fecha.", 16, 600, INK2, FB))
save(c, "7-paso4.svg")
