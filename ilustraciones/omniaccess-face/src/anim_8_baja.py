"""Teoría de Visitas y bloqueos: tres lugares, cada acción toca uno; la baja va primero en el terminal."""
from _anim_face import *

caps = ["Ana vive en tres lugares: el terminal, la ficha con sus eventos y las fotos.",
        "Cambiar el Modo Face cambia el registro: la cara sigue y la puerta abre.",
        "Eliminar en Memoria Flash saca la cara del terminal: deja de abrir.",
        "Recién ahí se decide la ficha. Las fotos siguen su retención."]
a = new(24, "Baja", "Dar de baja: primero el terminal, después la ficha", caps, still=3, size=17)
S = [sp[0] for sp in a.spans]

cols = [(48, "Memoria del terminal", "es lo que abre"), (340, "Ficha y eventos", "en OmniAccess"), (632, "Fotos", "almacenamiento")]
W, Y, H = 276, 180, 300
for x, t, s in cols:
    a.add(a.box(x, Y, W, H, a.WHITE, a.LINE) + a.text(x + 20, Y + 32, t, 18, a.INK, a.SANS, 600) + a.text(x + 20, Y + 56, s, 15, a.GREY, a.MONO))
# terminal
X0 = 48
term = (a.box(X0 + 20, Y + 76, W - 40, 118, a.SLATE, rx=10) + person(a, X0 + 62, Y + 104, .5, fill="#9DB2C6")
        + a.text(X0 + 104, Y + 108, "Ana Ejemplo", 16, a.INK, a.SANS, 600) + a.text(X0 + 104, Y + 132, "cara · tarjetas", 14, a.GREY, a.MONO)
        + a.text(X0 + 104, Y + 152, "PIN", 14, a.GREY, a.MONO))
vis(a, term, 0, 1)
a.add(a.group(term, a.keyframes([(0, 0), (S[2], 0), (S[2] + .5, 1), (S[2] + 6, 1), (S[2] + 8, 0), (100, 0)]), still=0))
vis(a, a.box(X0 + 20, Y + 76, W - 40, 118, "none", a.LINE, rx=10, extra='stroke-dasharray="6 5"') + a.text(X0 + W / 2, Y + 142, "sin Ana", 17, a.GREY, a.SANS, 600, "middle"), 2, 3, d0=8)
vis(a, a.pill(X0 + 20, Y + 214, "Memoria Flash → eliminar", a.WHITE, a.BAD, size=14), 2, d0=2)
# ficha y eventos
X1 = 340
a.add(a.box(X1 + 20, Y + 76, W - 40, 54, a.SLATE, rx=10) + a.text(X1 + 36, Y + 109, "Ficha · Ana Ejemplo", 16, a.INK, a.SANS, 600))
ev_ok = "".join(a.box(X1 + 20, Y + 142 + k * 40, W - 40, 32, a.OKBG, rx=8) + a.text(X1 + 34, Y + 164 + k * 40, f"evento {k + 1}", 15, a.INK, a.MONO) + a.text(X1 + W - 34, Y + 164 + k * 40, "Permitido", 14, a.OK, a.MONO, 600, "end") for k in range(2))
vis(a, ev_ok, 0)
vis(a, a.box(X1 + 20, Y + 142, W - 40, 32 + 80, "none", None) + "".join(a.box(X1 + 20, Y + 142 + k * 40, W - 40, 32, a.OKBG, rx=8) + a.text(X1 + 34, Y + 164 + k * 40, f"evento {k + 1}", 15, a.INK, a.MONO) + a.text(X1 + W - 34, Y + 164 + k * 40, "Permitido", 14, a.OK, a.MONO, 600, "end") for k in range(2))
    + a.box(X1 + 20, Y + 222, W - 40, 32, a.BADBG, rx=8) + a.text(X1 + 34, Y + 244, "evento 3", 15, a.INK, a.MONO) + a.text(X1 + W - 34, Y + 244, "Denegado", 14, a.BAD, a.MONO, 600, "end"), 1, 3, d0=6)
vis(a, a.pill(X1 + 20, Y + 268, "Modo Face → Lista Negra", a.WHITE, a.INK, size=14), 1, d0=2)
# fotos
X2 = 632
fotos = "".join(a.box(X2 + 20 + (k % 3) * 80, Y + 80 + (k // 3) * 80, 70, 70, a.SLATE, rx=8) + person(a, X2 + 55 + (k % 3) * 80, Y + 104 + (k // 3) * 80, .4, fill="#9DB2C6") for k in range(6))
a.add(fotos)
a.add(a.text(X2 + 20, Y + 262, "foto de alta y capturas", 15, a.GREY, a.MONO))

# prueba en la puerta
PX = 930
a.add(a.box(PX, Y, 222, H, a.WHITE, a.LINE) + a.text(PX + 20, Y + 32, "Prueba en la puerta", 17, a.INK, a.SANS, 600))
a.add(terminal(a, PX + 63, Y + 60, w=96, h=140))
vis(a, a.pill(PX + 111, Y + 226, "abre", a.WHITE, a.OK, size=16, h=34, anchor="middle"), 0, 1, d0=4)
vis(a, a.pill(PX + 111, Y + 226, "no abre", a.WHITE, a.BAD, size=16, h=34, anchor="middle") + a.text(PX + 111, Y + 284, "rostro desconocido", 15, a.BAD, a.SANS, 600, "middle"), 2, 3, d0=10)

# decisión sobre la ficha
a.add(a.box(48, 504, 1104, 132, a.SLATE, None, rx=14))
vis(a, a.text(72, 540, "Orden de la baja", 18, a.INK, a.SANS, 600) + a.text(72, 574, "1 · terminal (Memoria Flash)   2 · probar que no abre   3 · decidir la ficha", 17, a.TXT, a.MONO), 0, 2)
vis(a, a.text(72, 540, "La ficha, después:", 18, a.INK, a.SANS, 600)
    + a.pill(72, 556, "conservarla sin terminales: queda el historial", a.OK, a.OKBG, size=15, h=32)
    + a.pill(570, 556, "borrarla: se van también sus eventos", a.BAD, a.BADBG, size=15, h=32)
    + a.text(72, 618, "Las fotos quedan en el almacenamiento y se van con su retención (lección 9). Borrar la ficha no saca la cara del terminal.", 15, a.TXT), 3, d0=3)
write(a, "8-t1.svg", "Baja ordenada", [12, 40, 66, 92])
