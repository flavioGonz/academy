import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/windows/src")
from _win import *

# ---------------------------------------------------------------- 12.svg: tres llaves fuera del equipo
c = Canvas(K(), "Tres llaves, y ninguna vive solo dentro del equipo")
c.add(NOLIG)
keys_ = [("Administrador local", "único por equipo", ["Windows LAPS si hay dominio", "guardado en AD o Entra ID", "la puerta si el dominio no responde"], "key"),
         ("Clave de BitLocker", "48 dígitos de recuperación", ["fuera del disco cifrado", "gestor de contraseñas o AD", "sin ella no hay recuperación"], "lock"),
         ("Contraseña DSRM", "del controlador de dominio", ["nunca en texto plano", "ni en un script ni en un ticket", "se pide de forma segura"], "shield")]
for i, (t, s, items, ic) in enumerate(keys_):
    x = 48 + i * 372
    c.add(panel(x, 128, 352, 270, None, "info"))
    c.add(icon(x + 24, 150, ic, CYAN, 1.6))
    c.add(text(x + 74, 172, t, 20, 600, INK, FD))
    c.add(text(x + 74, 198, s, 15, 500, INK3, FB))
    sv, _ = bullet_list(x + 24, 250, [(it, "ok" if k < 2 else "warn") for k, it in enumerate(items)], 310, 16, gap=18)
    c.add(sv)
c.add(Note(48, 424, 1104, "Ninguna llave vive solo dentro del equipo que protege: la clave de recuperación no va en el mismo disco cifrado y las contraseñas no se pegan en scripts ni tickets.", title="Regla", kind="ok"))
save(c, "12.svg")

# ---------------------------------------------------------------- 12-paso2: anotar la clave de recuperación
c = Canvas(K(2), "La clave de recuperación sale del equipo")
c.add(NOLIG)
c.add(Step(65, 141, 2))
c.add(text(94, 147, "manage-bde -protectors -get C: (dibujo abreviado)", 17, 600, INK2, FM))
sv, h = console(48, 172, 640, [
    ("TPM:", "#D9E9F8"),
    ("  ID: {…}", "#7FA6C9"),
    ("Contraseña numérica:", "#9FE3F7"),
    ("  ID: {AAAAAAAA-…}", "#9FE3F7"),
    ("  Contraseña:", "#9FE3F7"),
    ("  ######-######-######-######-…", "#FFB020"),
], title="Protectores del volumen C:", prompt="C:\\> ")
c.add(sv)
c.add(crow(48, 172, 640, 3))
pm = c.add(Generic(800, 200, "Gestor de contraseñas", "de la empresa", icon="key", w=352, hl=OK))
c.add(Arrow((690, 300), pm.left(), label="copiar", kind="ok"))
c.add(Window(800, 316, 352, 150, "Entrada nueva", rows=[("Equipo", "SRV-VMS-01"), ("ID protector", "{AAAAAAAA-…}")], hl=None))
c.add(Note(48, 430, 640, "Anotá el ID del protector \"Contraseña numérica\" y copiá la clave con el nombre del equipo. Si hay dominio y la directiva lo permite, también va a Active Directory (paso 3).", kind="info"))
c.add(Note(48, 560, 1104, "Nunca la guardes solo en el mismo disco cifrado: ni el soporte de Microsoft la puede recuperar. Datos del dibujo de ejemplo.", kind="alert"))
save(c, "12-paso2.svg")

# ---------------------------------------------------------------- 12-paso4: suspender antes del BIOS
c = Canvas(K(4), "Antes de actualizar el BIOS, suspendé BitLocker")
c.add(NOLIG)
c.add(Step(65, 141, 4))
c.add(code(94, 122, 560, "Suspend-BitLocker -MountPoint C: -RebootCount 1", 15))
lane = [("Suspender", "por un reinicio", "info"), ("Actualizar BIOS", "o firmware", "info"), ("Reinicio", "arranca sin pedir clave", "ok"), ("Se reanuda solo", "vuelve a proteger", "ok")]
for i, (t, s, kd) in enumerate(lane):
    x = 48 + i * 284
    c.add(panel(x, 190, 252, 110, None, kd))
    c.add(text(x + 20, 232, t, 18, 600, OK if kd == "ok" else INK, FD))
    c.add(text(x + 20, 262, s, 15, 400, INK2, FB))
    if i < 3:
        c.add(arrow((x + 256, 245), (x + 280, 245), "flow"))
c.add(panel(48, 336, 1104, 150, None, "alert"))
c.add(Mark(86, 376, ok=False))
c.add(text(118, 383, "Sin suspender", 20, 600, ALERT, FD))
svg, _ = wrap(72, 424, "Un cambio de BIOS, firmware o hardware puede hacer que al arrancar aparezca la pantalla de recuperación de BitLocker. Ahí solo sirve la clave guardada fuera del equipo.", 1050, 16, 400, INK2)
c.add(svg)
c.add(Note(48, 512, 1104, "-RebootCount 1: la protección vuelve sola después del primer reinicio. Tené la clave de recuperación a mano igual.", kind="info"))
save(c, "12-paso4.svg")

# ---------------------------------------------------------------- 12-paso5: quién es administrador
c = Canvas(K(5), "¿Quién es administrador local en este equipo?")
c.add(NOLIG)
c.add(Step(65, 141, 5))
c.add(text(94, 147, "S-1-5-32-544 es el grupo Administradores en cualquier idioma", 17, 600, INK2, FB))
sv, h = console(48, 172, 1104, [
    ">Get-LocalGroupMember -SID S-1-5-32-544",
    ("ObjectClass  Name                        PrincipalSource", "#7FA6C9"),
    ("Usuario      SRV-VMS-01\\Administrador    Local", "#D9E9F8"),
    ("Grupo        EMPRESA\\Admins. del dominio  ActiveDirectory", "#D9E9F8"),
    ("Usuario      SRV-VMS-01\\soporte2         Local", "#FFB020"),
])
c.add(sv)
c.add(crow(48, 172, 1104, 4, color=WARN))
c.add(Note(48, 386, 540, "Si aparece una cuenta que nadie reconoce, anotala y consultá antes de borrarla: puede ser la de un software o de otro proveedor.", title="Cuenta desconocida", kind="warn"))
c.add(Note(612, 386, 540, "Cada equipo con su administrador local único y recuperable, y el resto de las cuentas con lo mínimo que necesitan.", title="Mínimo privilegio", kind="ok"))
c.add(text(48, 560, "Nombres de ejemplo.", 15, 400, INK3, FB))
save(c, "12-paso5.svg")

# ---------------------------------------------------------------- 12-t2: movimiento lateral (fija, teoría)
c = Canvas("Windows · Teoría", "La misma clave en todos los equipos abre todos")
c.add(NOLIG)
c.add(panel(48, 128, 540, 420, "Sin LAPS: una clave para todos", "alert"))
c.add(panel(612, 128, 540, 420, "Con Windows LAPS: una por equipo", "ok"))
pcs = [(80, 200), (330, 200), (80, 370), (330, 370)]
for k, (x, y) in enumerate(pcs):
    c.add(Generic(x, y, f"Puesto {k + 1}", "admin: ••••", icon="laptop", w=220, hl=ALERT if k else WARN))
for a_, b_ in ((0, 1), (0, 2), (0, 3)):
    (x1, y1), (x2, y2) = pcs[a_], pcs[b_]
    c.add(Cable((x1 + 110, y1 + 84), (x2 + 110, y2), kind="alert") if b_ == 2 else Cable((x1 + 220, y1 + 42), (x2, y2 + 42), kind="alert") if b_ == 1 else Cable((x1 + 200, y1 + 84), (x2 + 20, y2), kind="alert"))
c.add(text(72, 520, "Quien la saca de uno, entra a todos.", 16, 600, ALERT, FB))
for k, (x, y) in enumerate(pcs):
    c.add(Generic(x + 564, y, f"Puesto {k + 1}", f"admin: clave {k + 1}", icon="laptop", w=220, hl=OK))
c.add(text(636, 520, "Única, aleatoria, rotada y guardada en AD o Entra ID.", 16, 600, OK, FB))
c.add(text(48, 600, "Las fuentes lo llaman movimiento lateral: saltar de equipo en equipo con la misma credencial.", 16, 400, INK2, FB))
save(c, "12-t2.svg")
