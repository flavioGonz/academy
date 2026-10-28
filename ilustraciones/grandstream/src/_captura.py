"""Ayudas para editar capturas de la web de la UCM (Lato, fondo blanco) sin dejar datos reales.

reemplazar(im, caja, nuevo, align): tapa la caja del texto original con el color de fondo y escribe
el texto nuevo con Lato, con la misma altura de mayúsculas, el mismo borde superior y el color más
oscuro del texto original (el resto son píxeles de suavizado). align: "left" (mismo borde izquierdo)
o "center" (mismo centro).
"""
from collections import Counter
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

LATO = str(Path(__file__).parent / "fonts" / "Lato-Regular.ttf")  # la fuente de la web de la UCM
CAPT = Path("/home/claude/ies-training/ilustraciones/grandstream/capturas")
SITE = Path("/home/claude/ies-training/site2/ilustraciones/grandstream")
PREV = Path("/home/claude/ies-training/ilustraciones/grandstream")


def medir(im, caja, umbral=170):
    """Caja ajustada de los píxeles de texto (más oscuros que umbral) dentro de caja, color del texto y del fondo."""
    x0, y0, x1, y1 = caja
    px = im.load()
    pts = [(x, y) for y in range(y0, y1) for x in range(x0, x1) if sum(px[x, y]) / 3 < umbral]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    oscuros = sorted((px[x, y] for x, y in pts), key=lambda c: sum(c))
    color = oscuros[max(0, len(oscuros) // 10)]
    fondo = Counter(px[x, y] for y in range(y0, y1) for x in range(x0, x1)).most_common(1)[0][0]
    return (min(xs), min(ys), max(xs), max(ys)), color, fondo


def reemplazar(im, caja, viejo, nuevo, align="left", umbral=170):
    (bx0, by0, bx1, by1), color, fondo = medir(im, caja, umbral)
    ancho = bx1 - bx0 + 1
    # tamaño de letra que reproduce el ancho del texto original
    size = 10
    for s10 in range(80, 260):
        f = ImageFont.truetype(LATO, s10 / 10)
        l, t, r, b = f.getbbox(viejo, anchor="ls")
        if r - l <= ancho:
            size = s10 / 10
    f = ImageFont.truetype(LATO, size)
    gris = round(sum(color) / 3)
    color = (gris, gris, gris + 3)  # el texto de la UCM es gris neutro; el tinte viene de la compresión
    d = ImageDraw.Draw(im)
    d.rectangle((bx0 - 2, by0 - 2, bx1 + 2, by1 + 2), fill=fondo)
    # alrededor, la compresión deja un halo casi blanco: se limpia sin tocar líneas divisorias (más oscuras)
    px = im.load()
    for y in range(by0 - 7, by1 + 8):
        for x in range(bx0 - 8, bx1 + 9):
            if sum(px[x, y]) / 3 > 236:
                px[x, y] = fondo
    l, t, r, b = f.getbbox(nuevo, anchor="ls")
    cap_top = f.getbbox("A", anchor="ls")[1]
    base = by0 - cap_top
    if align == "center":
        cx = (bx0 + bx1) / 2
        x = cx - (r + l) / 2
    else:
        x = bx0 - l
    d.text((x, base), nuevo, font=f, fill=color, anchor="ls")
    return {"viejo": viejo, "nuevo": nuevo, "size": size, "color": color, "caja": (bx0, by0, bx1, by1)}


def guardar(im, nombre, escala=2):
    """Vista previa PNG (para revisar con Read) y webp para el sitio, escalado para que no se vea chico."""
    PREV.joinpath(nombre + ".png").parent.mkdir(parents=True, exist_ok=True)
    im.save(PREV / f"{nombre}.png")
    w, h = im.size
    im.resize((w * escala, h * escala), Image.LANCZOS).save(SITE / f"{nombre}.webp", "WEBP", quality=90, method=6)
    print("ok", SITE / f"{nombre}.webp", (w * escala, h * escala))
