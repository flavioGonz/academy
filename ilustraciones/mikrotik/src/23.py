"""Ilustraciones de la lección 2 (Safe Mode) del curso MikroTik.
Fuentes: class/23-safe-mode/card.md, research/notes/d.md
(manual 7.25 Configuration Management y WinBox, foro oficial)."""
import sys; sys.path.insert(0, "/home/claude/ies-training/tools")
from ilus import *

OUT = "/home/claude/ies-training/ilustraciones/mikrotik/"


def pill(x, y, s, w, kind="gray"):
    bg, fg, st = {"gray": (WHITE, INK2, LINE2), "cyan": (CYAN, WHITE, CYAN)}[kind]
    return (f'<rect x="{x}" y="{y}" width="{w}" height="40" rx="10" fill="{bg}" stroke="{st}" stroke-width="2"/>'
            + text(x + w / 2, y + 26, s, 15, 600, fg, FB, anchor="middle"))


# ------------------------------------------------------------ principal
c = Canvas("MikroTik", "Safe Mode: un punto de vuelta para tus cambios")
c.add(Terminal(48, 130, 490, [
    "[admin@MikroTik] >   Ctrl+X o F4",
    ("[Safe Mode taken]", "#7FD3F0"),
    "[admin@MikroTik] <SAFE>",
], title="NEW TERMINAL"))
c.add(Label(48, 300, "/system/history mientras estás en Safe Mode", 15, 600, BLUE, FM))
c.add(Table(48, 316, ["", "acción"], [
    ["F", "regla de firewall agregada"],
    ["F", "IP de gestión cambiada"],
    ["F", "ruta por defecto cambiada"],
], [70, 420]))
c.add(Note(48, 492, 490, "Entran 100 acciones. Si te pasás, sale solo del modo seguro y no deshace nada: pasos chicos.", title="Tope del historial", kind="warn"))
ok = c.add(Note(680, 150, 470, "Los cambios quedan y el prompt pierde el <SAFE>. Salir con /quit también los deja.", title="Confirmás: Ctrl+X otra vez o soltás el botón", kind="ok"))
bad = c.add(Note(680, 350, 470, "RouterOS deshace todo lo marcado con F. Si se cortó la conexión, lo hace cuando da la sesión por muerta (la documentación toma 9 minutos de timeout TCP).", title="Se corta tu sesión o salís con Ctrl+D", kind="alert"))
c.add(Arrow((548, 380), (670, 205), kind="ok", label="todo bien", label_at=0.5, label_dy=-4))
c.add(Arrow((548, 410), (670, 430), kind="alert", label="algo falló", label_at=0.55, label_dy=-26))
c.save(OUT + "23.svg")

# ------------------------------------------------------------ paso 2: dónde se activa
c = Canvas("MikroTik · Paso 2", "Activá Safe Mode: el botón o Ctrl+X")
# ventana WinBox genérica
x, y, w, h = 48, 140, 560, 250
c.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{WHITE}" stroke="{LINE2}" stroke-width="2"/>'
      f'<path d="M{x} {y + 14}a14 14 0 0 1 14 -14h{w - 28}a14 14 0 0 1 14 14v26h-{w}z" fill="{SOFT}"/>'
      f'<circle cx="{x + 20}" cy="{y + 20}" r="5" fill="{LINE2}"/><circle cx="{x + 38}" cy="{y + 20}" r="5" fill="{LINE2}"/><circle cx="{x + 56}" cy="{y + 20}" r="5" fill="{LINE2}"/>'
      + text(x + 76, y + 26, "WinBox · admin@192.168.88.1", 15, 600, INK2, FB))
c.add(f'<rect x="{x + 10}" y="{y + 52}" width="{w - 20}" height="60" rx="10" fill="{GROUND}" stroke="{LINE}" stroke-width="1.5"/>')
c.add(pill(x + 24, y + 62, "Undo", 96))
c.add(pill(x + 130, y + 62, "Redo", 96))
c.add(pill(x + 250, y + 62, "Safe Mode", 150, "cyan"))
c.add(pill(x + 420, y + 62, "Disconnect", 116))
c.add(Step(x + 250 + 150, y + 62, 2))
c.add(Label(x + 24, y + 150, "Barra de arriba de WinBox 4 (esquema, no captura):", 15, 500, INK3))
c.add(Label(x + 24, y + 176, "Undo, Redo y el interruptor Safe Mode.", 15, 500, INK3))
c.add(Label(x + 24, y + 214, "En WebFig también hay botón Safe Mode.", 15, 500, INK3))
t = c.add(Terminal(660, 140, 490, [
    "[admin@MikroTik] >      Ctrl+X",
    ("[Safe Mode taken]", "#7FD3F0"),
    "[admin@MikroTik] <SAFE>",
], title="NEW TERMINAL"))
c.add(Chip(660, 330, "Ctrl+X otra vez: confirma", "ok"))
c.add(Chip(660, 378, "Ctrl+D: descarta todo", "alert"))
c.add(Note(48, 440, 1102, "En un enlace malo, el botón puede quedar apretado sin que el router haya entrado en modo seguro. El aviso [Safe Mode taken] y el <SAFE> en la terminal son la confirmación de que sí entró.", title="Cuándo mirar la terminal", kind="warn"))
c.save(OUT + "23-paso2.svg")

# ------------------------------------------------------------ paso 3: corte a propósito
c = Canvas("MikroTik · Paso 3", "Cortate a propósito y mirá cómo vuelve solo")
panels = [
    ("1 · Safe Mode activo", "data", None, "<SAFE>", "cyan"),
    ("2 · /interface/disable ether2", "alert", False, "sesión cortada", "alert"),
    ("3 · el router deshace", "ok", True, "ether2 vuelve", "ok"),
]
for i, (lbl, kind, mark, chip, ck) in enumerate(panels):
    px = 48 + i * 390
    c.add(Zone(px, 140, 330, 330, lbl, {"data": LINE2, "alert": ALERT, "ok": OK}[kind]))
    lp = c.add(Laptop(px + 50, 178, "Notebook", "WinBox", w=230))
    rt = c.add(Generic(px + 50, 340, "hAP de banco", "RouterOS 7", icon="server", dark=True, w=230))
    a, b = lp.bottom(), rt.top()
    if kind == "data":
        c.add(Cable(a, b, kind="data"))
    elif kind == "alert":
        c.add(Cable(a, b, kind="alert", arrow=False))
    else:
        c.add(Cable(a, b, kind="data"))
    if mark is not None:
        c.add(Mark(px + 290, 302, ok=mark))
    c.add(Chip(px + 165, 312, chip, ck, anchor="middle"))
    if i < 2:
        c.add(Arrow((px + 336, 300), (px + 384, 300), kind="flow"))
c.add(Note(48, 500, 1102, "Esperá sin tocar nada. Puede tardar de segundos a varios minutos: la documentación toma como referencia el timeout TCP de 9 minutos y en el foro se ve volver en segundos o al minuto.", title="El tiempo de la vuelta", kind="info"))
c.save(OUT + "23-paso3.svg")
print("ok")
