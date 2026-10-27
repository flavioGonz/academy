import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-lpr/src")
from _lpr import *

# ---------------------------------------------------------------- 11.svg: la cadena del padrón y la sincronización
c = Canvas(K(), "Padrón completo: unidad, usuario, matrícula y grupo")
chain = [("Unidad", "Lote 99 (prueba)", "door"), ("Usuario", "Residente Prueba", "user"), ("Credencial", "SBA1234 · SCD5678", "card"), ("Grupo de acceso", "Residentes · 24/7", "key")]
for i, (t, s, ic) in enumerate(chain):
    x = 48 + i * 282
    c.add(Generic(x, 140, t, s, icon=ic, w=262))
    if i:
        c.add(Arrow((x - 18, 182), (x - 2, 182)))
c.add(panel(48, 270, 540, 250, "Vehículos / Matrículas", "info", sub="la vista por vehículo"))
c.add(Table(68, 340, ["Matrícula", "Dueño", "Última"], [["SBA1234", "Residente Prueba", "hoy 08:02"], ["SCD5678", "Residente Prueba", "ayer"]], [150, 210, 140], row_h=40, mono_cols=(0, 2)))
c.add(panel(612, 270, 540, 250, "Sincronizar matrículas a las cámaras", "dark"))
c.add(text(632, 336, "Incremental", 19, 700, CYAN, FD))
c.add(text(632, 364, "solo diferencias; nunca quedan sin lista", 16, 500, WHITE, FB))
c.add(text(632, 420, "Reemplazo total", 19, 700, "#FFB4A6", FD))
c.add(text(632, 448, "borra y recarga; solo para reparar", 16, 500, WHITE, FB))
c.add(text(632, 496, "Dispositivos → vista Cámaras LPR", 15, 500, "#9FC3E3", FM))
c.add(text(48, 566, "Matrícula suelta sin usuario ni unidad: abre igual, pero no se puede responder «¿qué autos tiene el lote 99?».", 16, 500, INK2, FB))
c.add(text(48, 600, "Baja temporal: Suspendido, no Eliminado. Visitas: Invitados. Reporte del mes: Historial → Exportar.", 16, 500, INK2, FB))
save(c, "11.svg")

# ---------------------------------------------------------------- 11-paso4: incremental contra reemplazo total
c = Canvas(K(4), "Analizar, leer las diferencias y sincronizar en Incremental")
c.add(Table(48, 130, ["Cámara", "En la base", "Tiene", "A agregar", "A quitar"],
            [["P1 - Entrada (21)", "122", "120", "+2", "0"], ["P2 - Salida (22)", "122", "121", "+1", "0"], ["P3 - Servicio (23)", "122", "123", "0", "-1"]],
            [300, 190, 170, 200, 244], hl_row=0, row_h=48, mono_cols=(1, 2, 3, 4)))
c.add(panel(48, 350, 540, 150, "Incremental · recomendado", "ok"))
lst, _ = wrap(68, 420, "Aplica solo lo que falta y lo que sobra. La cámara sigue abriendo a los de siempre mientras tanto.", 500, 17, 400, INK)
c.add(lst)
c.add(panel(612, 350, 540, 150, "Reemplazo total · solo para reparar", "alert"))
lst, _ = wrap(632, 420, "Borra la lista de cada cámara y recarga todo. Mientras recarga, la cámara no abre sola: fuera del horario pico.", 500, 17, 400, INK)
c.add(lst)
save(c, "11-paso4.svg")

# ---------------------------------------------------------------- 11-paso6: el reporte del mes
c = Canvas(K(6), "Historial → Exportar (Excel / PDF) para el cierre de mes")
c.add(Window(48, 130, 520, 230, "Exportar reporte", rows=[("Período", "mes pasado"), ("Qué eventos", "todos"), ("Columnas", "matrícula, persona, lote, punto, sentido, resultado"[:24] + "…"), ("Formato", "PDF")], hl=3))
c.add(Arrow((568, 250), (640, 250)))
c.add(f'<rect x="650" y="130" width="250" height="330" rx="8" fill="{WHITE}" stroke="{LINE2}" stroke-width="2"/>')
c.add(f'<rect x="650" y="130" width="250" height="90" rx="8" fill="{DEEP}"/>')
c.add(text(670, 172, "Barrio Ejemplo", 18, 700, WHITE, FD))
c.add(text(670, 198, "Accesos del mes", 15, 500, "#9FC3E3", FM))
for k in range(6):
    c.add(f'<rect x="670" y="{244 + k * 26}" width="{210 - (k % 3) * 30}" height="10" rx="5" fill="{LINE}"/>')
c.add(text(670, 436, "Realizado por · Autorizado por", 13, 500, INK3, FB))
c.add(panel(930, 130, 222, 330, "Portada", "info"))
lst, _ = wrap(950, 196, "Logo, colores y firmas en Configuración → Branding → Reportes Exportables.", 180, 16, 400, INK2)
c.add(lst)
c.add(Note(48, 494, 1104, "En esta versión, con el sistema en modo LPR, el reporte de accesos sale del Historial de Acceso; el menú Reportes aparece en el modo Filas.", kind="info", size=16))
save(c, "11-paso6.svg")
