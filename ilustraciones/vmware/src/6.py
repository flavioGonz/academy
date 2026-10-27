import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/vmware/src")
from _vmw import *

# ---------------------------------------------------------------- 6.svg: la cadena de snapshots
c = Canvas(K(), "Un snapshot no es una copia: es un delta que depende")
c.add(NOLIG)
c.add(vm(48, 140, 260, 70, "vm-prueba", "VM encendida"))
c.add(filebox(48, 270, 330, "vm-prueba-flat.vmdk", "disco base: congelado"))
c.add(filebox(430, 270, 330, "vm-prueba-000001.vmdk", "delta 1: recibe lo escrito", "warn"))
c.add(filebox(812, 270, 340, "vm-prueba-000002.vmdk", "delta 2: si sacás otro", "warn"))
c.add(arrow((428, 292), (380, 292), "logical"))
c.add(arrow((810, 292), (762, 292), "logical"))
c.add(text(404, 340, "depende de", 14, 500, INK3, FB, anchor="middle"))
c.add(text(786, 340, "depende de", 14, 500, INK3, FB, anchor="middle"))
c.add(arrow((300, 186), (560, 266), "flow", label="escrituras nuevas", label_at=0.55))
c.add(icon(330, 300, "lock", INK3, 0.9))
# reglas
reglas = [("2 o 3", "por VM en la práctica (32 es el tope técnico)", "info"),
          ("72 h", "como máximo; mejor borrarlo apenas validás", "warn"),
          ("fecha en el nombre", "borrar-2026-10-30-antes-update", "info")]
for i, (t, s, k) in enumerate(reglas):
    x = 48 + i * 376
    c.add(panel(x, 380, 352, 110, None, k))
    c.add(text(x + 20, 420, t, 22, 700, WARN if k == "warn" else BLUE, FD))
    sv, _ = wrap(x + 20, 452, s, 312, 15, 500, INK2, FM if i == 2 else FB)
    c.add(sv)
c.add(Note(48, 514, 540, "Si se pierde o se rompe el disco base, el delta solo no restaura nada.", title="Por qué no es backup", kind="alert"))
c.add(Note(612, 514, 540, "No agrandes un disco con snapshots vivos ni canceles una consolidación en curso.", title="Dos cosas que no", kind="warn"))
save(c, "6.svg")

# ---------------------------------------------------------------- 6-paso1: el delta en el datastore
c = Canvas(K(1), "Mirá el delta en el datastore y que no quede nada")
c.add(NOLIG)
c.add(Step(48, 140, 1))
cols = [("Antes", ["vm-prueba.vmx", "vm-prueba.vmdk", "vm-prueba-flat.vmdk"], "info", None),
        ("Con el snapshot", ["vm-prueba.vmx", "vm-prueba.vmdk", "vm-prueba-flat.vmdk", "vm-prueba-000001.vmdk"], "warn", "snapshot.create 1 \"borrar-2026-10-30…\""),
        ("Después de removeall", ["vm-prueba.vmx", "vm-prueba.vmdk", "vm-prueba-flat.vmdk"], "ok", "snapshot.removeall 1")]
for i, (t, fs, k, cmd) in enumerate(cols):
    x = 48 + i * 376
    c.add(panel(x, 170, 352, 330, t, k))
    c.add(text(x + 20, 226, "ls -lh …/vm-prueba/", 14, 600, INK3, FM))
    for j, f in enumerate(fs):
        nuevo = "000001" in f
        c.add(filebox(x + 20, 244 + j * 56, 312, f, None, "warn" if nuevo else "info", h=44, size=14.5))
    if cmd:
        c.add(text(x + 20, 480, cmd, 13.5, 600, BLUE, FM))
    if i < 2:
        c.add(arrow((x + 354, 330), (x + 374, 330), "flow"))
c.add(code(48, 524, 700, 'find /vmfs/volumes/datastore1/ -name "*-0000*.vmdk"'))
c.add(text(48, 600, "Al final no tiene que devolver nada: ni deltas de tu prueba ni de backups fallidos.", 17, 600, OK, FB))
c.add(Note(780, 524, 372, "Un snapshot que dejó un backup puede no verse en el Snapshot Manager: por eso el find.", kind="warn", size=15))
save(c, "6-paso1.svg")
