#!/usr/bin/env python3
"""Animación RIB y FIB (lección Rutas estáticas, teoría "Cómo funciona").

SVG animado con CSS (sin scripts, se muestra con <img>), con las fuentes de marca embebidas
en subconjunto para que se vea igual que el portal aunque la imagen no pueda cargar fuentes.
Ciclo de 25 s en cinco tiempos:
  1. Todas las rutas entran a la RIB.
  2. Por destino gana la de menor distancia; las ganadoras pasan a la FIB.
  3. Llega un paquete: la FIB busca la máscara más larga.
  4. Cae el ISP A: check-gateway deja la ruta inactiva y la FIB pasa al ISP B.
  5. Vuelve el ISP A: la ruta recupera su lugar.
Con prefers-reduced-motion se ve un cuadro fijo (tiempo 3).

  python3 anim_27_rib_fib.py            -> site2/ilustraciones/mikrotik/27-rib-fib.svg
  python3 anim_27_rib_fib.py --frames   -> además PNG de cada tiempo para revisar
"""
import base64, io, re, sys, urllib.request
from pathlib import Path

OUT = Path("/home/claude/ies-training/site2/ilustraciones/mikrotik/27-rib-fib.svg")
PREV = Path("/home/claude/ies-training/ilustraciones/mikrotik")
T = 25  # segundos del ciclo

# ---- paleta (la de las ilustraciones del curso)
BG, INK, BLUE, CYAN, GREY, TXT, LINE = "#F7FAFD", "#04223D", "#0A63B8", "#17A8D4", "#6E88A1", "#41627F", "#DDE8F2"
OK, OKBG, BAD, BADBG, AMB, AMBBG, SLATE = "#0E8F5E", "#E3F5EC", "#D2492F", "#FCEAE6", "#B26A00", "#FFF3DC", "#EEF3F8"

css, body = [], []
kf_n = [0]


def anim(points, prop="opacity", fmt="{}"):
    """points: [(porcentaje, valor)] -> nombre de animación nueva."""
    kf_n[0] += 1
    name = f"k{kf_n[0]}"
    steps = " ".join(f"{p}%{{{prop}:{fmt.format(v)}}}" for p, v in points)
    css.append(f"@keyframes {name}{{{steps}}}")
    return name


def show(a, b, fade=1.2):
    """visible entre a% y b% del ciclo (con fundido corto)."""
    pts = [(0, 0)] if a > 0 else [(0, 1)]
    if a > 0:
        pts += [(a, 0), (min(a + fade, 100), 1)]
    if b < 100:
        pts += [(max(b - fade, 0), 1), (b, 0), (100, 0)]
    else:
        pts += [(98.5, 1), (100, 0 if a > 0 else 1)]
    # quitar duplicados de porcentaje conservando el último
    d = {}
    for p, v in pts:
        d[round(p, 2)] = v
    return anim(sorted(d.items()))


def cls(name, base_opacity):
    """clase con animación; base_opacity es el cuadro fijo (movimiento reducido)."""
    kf_n[0] += 1
    c = f"c{kf_n[0]}"
    css.append(f".{c}{{opacity:{base_opacity};animation:{name} {T}s linear infinite}}")
    return c


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=17, fill=TXT, fam="Instrument Sans", weight=400, anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{esc(s)}</text>'


MONO, HEAD = "JetBrains Mono", "Familjen Grotesk"

# ---------------- fondo y encabezado
body.append(f'<rect width="1200" height="675" fill="{BG}"/>')
body.append(text(48, 56, "MIKROTIK · RUTAS", 15, CYAN, MONO, 400, extra='letter-spacing="2.4"'))
body.append(text(48, 92, "RIB y FIB: todas las rutas, y las que se usan", 32, INK, HEAD, 600))

# ---------------- leyenda de tiempos (barra de pasos)
PH = [(0, 20), (20, 40), (40, 60), (60, 80), (80, 100)]
CAP = [
    "Todas las rutas entran a la RIB: conectadas, estáticas, de DHCP, de PPP.",
    "Para cada destino gana una: la de menor distancia. Las ganadoras pasan a la FIB.",
    "Llega un paquete a 10.20.5.7: la FIB busca la máscara más larga. Gana la /24.",
    "Cae el ISP A: check-gateway deja su ruta inactiva y la FIB pasa al ISP B.",
    "Vuelve el ISP A: su ruta recupera el lugar y la FIB vuelve a usarla.",
]
for i, (a, b) in enumerate(PH):
    x = 48 + i * 44
    on = cls(show(a, b, 0.6), 1 if i == 2 else 0)
    body.append(f'<rect x="{x}" y="118" width="36" height="36" rx="18" fill="#FFFFFF" stroke="{LINE}" stroke-width="2"/>')
    body.append(f'<g class="{on}"><rect x="{x}" y="118" width="36" height="36" rx="18" fill="{BLUE}"/></g>')
    body.append(text(x + 18, 142, str(i + 1), 16, GREY, MONO, 600, "middle"))
    body.append(f'<g class="{on}">' + text(x + 18, 142, str(i + 1), 16, "#FFFFFF", MONO, 600, "middle") + "</g>")
    body.append(f'<g class="{on}">' + text(282, 143, CAP[i], 18, INK, "Instrument Sans", 600) + "</g>")

# ---------------- paneles
RX, RY, RW, RH = 48, 176, 610, 392
FX, FY, FW, FH = 752, 176, 400, 392
body.append(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="18" fill="#FFFFFF" stroke="{LINE}" stroke-width="2"/>')
body.append(text(RX + 24, RY + 40, "RIB", 22, INK, HEAD, 600))
body.append(text(RX + 76, RY + 40, "todas las candidatas · /routing/route", 15, GREY, MONO))
body.append(f'<rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" rx="18" fill="{INK}"/>')
body.append(text(FX + 24, FY + 40, "FIB", 22, "#FFFFFF", HEAD, 600))
body.append(text(FX + 76, FY + 40, "la que reenvía · activas", 15, "#9FC3E3", MONO))

# columnas RIB
body.append(text(RX + 24, RY + 74, "destino", 13, GREY, MONO))
body.append(text(RX + 196, RY + 74, "gateway", 13, GREY, MONO))
body.append(text(RX + 392, RY + 74, "dist", 13, GREY, MONO))
body.append(text(RX + RW - 24, RY + 74, "estado", 13, GREY, MONO, anchor="end"))

ROWS = [  # dst, gw, dist, tipo
    ("0.0.0.0/0", "203.0.113.1  ISP A", "1", "estática"),
    ("0.0.0.0/0", "198.51.100.1 ISP B", "2", "estática"),
    ("192.168.88.0/24", "bridge", "0", "conectada"),
    ("10.20.0.0/16", "l2tp-central", "1", "estática"),
    ("10.20.5.0/24", "192.168.88.254", "1", "estática"),
]
ROW_H, ROW_Y0 = 54, RY + 88


def pill(x, y, label, fg, bg, w=None, anchor_end=True):
    w = w or (len(label) * 9 + 26)
    x0 = x - w if anchor_end else x
    return (f'<rect x="{x0}" y="{y}" width="{w}" height="28" rx="14" fill="{bg}"/>'
            + text(x0 + w / 2, y + 19, label, 14, fg, MONO, 600, "middle"))


for i, (dst, gw, dist, tipo) in enumerate(ROWS):
    y = ROW_Y0 + i * ROW_H
    appear = 2 + i * 3
    row = cls(show(appear, 100), 1)
    body.append(f'<g class="{row}">')
    body.append(f'<rect x="{RX + 12}" y="{y}" width="{RW - 24}" height="{ROW_H - 8}" rx="10" fill="{SLATE}"/>')
    body.append(text(RX + 24, y + 30, dst, 17, INK, MONO, 600))
    body.append(text(RX + 196, y + 30, gw, 16, TXT, MONO))
    body.append(text(RX + 392, y + 30, dist, 17, INK, MONO, 600))
    body.append(text(RX + 414, y + 30, tipo, 12, GREY, "Instrument Sans"))
    body.append("</g>")
    py = y + 9
    end = RX + RW - 24
    if i == 0:   # ISP A: activa, inactiva al caer, activa de nuevo
        body.append(f'<g class="{cls(show(21, 61), 1)}">' + pill(end, py, "activa", OK, OKBG) + "</g>")
        body.append(f'<g class="{cls(show(61, 81), 0)}">' + pill(end, py, "inactiva", BAD, BADBG) + "</g>")
        body.append(f'<g class="{cls(show(81, 100), 0)}">' + pill(end, py, "activa", OK, OKBG) + "</g>")
        # tachado del gateway caído
        body.append(f'<g class="{cls(show(61, 81), 0)}"><line x1="{RX + 192}" y1="{y + 25}" x2="{RX + 372}" y2="{y + 25}" stroke="{BAD}" stroke-width="2.5"/>'
                    + text(RX + 196, y + 50, "check-gateway: 2 timeouts", 12, BAD, MONO) + "</g>")
    elif i == 1:  # ISP B: en espera, activa cuando cae A
        body.append(f'<g class="{cls(show(21, 61), 1)}">' + pill(end, py, "en espera", GREY, "#E6EDF4") + "</g>")
        body.append(f'<g class="{cls(show(61, 81), 0)}">' + pill(end, py, "activa", OK, OKBG) + "</g>")
        body.append(f'<g class="{cls(show(81, 100), 0)}">' + pill(end, py, "en espera", GREY, "#E6EDF4") + "</g>")
    else:
        body.append(f'<g class="{cls(show(21, 100), 1)}">' + pill(end, py, "activa", OK, OKBG) + "</g>")

# resaltado del duelo por 0.0.0.0/0 en el tiempo 2
duel = cls(anim([(0, 0), (21, 0), (22.5, 1), (37, 1), (39, 0), (100, 0)]), 0)
body.append(f'<g class="{duel}"><rect x="{RX + 8}" y="{ROW_Y0 - 4}" width="{RW - 16}" height="{ROW_H * 2}" rx="12" fill="none" stroke="{AMB}" stroke-width="3" stroke-dasharray="8 6"/>'
            + f'<rect x="{RX + 250}" y="{ROW_Y0 + ROW_H * 2 - 17}" width="300" height="26" rx="13" fill="{AMBBG}" stroke="{AMB}" stroke-width="1.5"/>'
            + text(RX + 400, ROW_Y0 + ROW_H * 2 + 1, "mismo destino: gana distancia 1", 13, AMB, MONO, 600, "middle") + "</g>")

# flecha RIB -> FIB
arr = cls(anim([(0, 0.25), (21, 0.25), (23, 1), (31, 1), (33, 0.25), (61, 0.25), (62.5, 1), (67, 1), (69, 0.25), (81, 0.25), (82.5, 1), (87, 1), (89, 0.25), (100, 0.25)]), 1)
body.append(f'<g class="{arr}"><path d="M{RX + RW + 10} {RY + 196} H{FX - 14}" stroke="{BLUE}" stroke-width="4" marker-end="url(#ah)"/>'
            + text((RX + RW + FX) / 2, RY + 166, "la mejor", 12, BLUE, MONO, 600, "middle")
            + text((RX + RW + FX) / 2, RY + 182, "por destino", 12, BLUE, MONO, 600, "middle") + "</g>")

# filas FIB
FROWS = [("0.0.0.0/0", "ISP A"), ("192.168.88.0/24", "bridge"), ("10.20.0.0/16", "l2tp-central"), ("10.20.5.0/24", "192.168.88.254")]
FROW_Y0 = FY + 70
for i, (dst, via) in enumerate(FROWS):
    y = FROW_Y0 + i * 62
    g = cls(show(24 + i * 1.5, 100), 1)
    body.append(f'<g class="{g}"><rect x="{FX + 16}" y="{y}" width="{FW - 32}" height="52" rx="10" fill="#0B3A66"/>'
                + text(FX + 32, y + 22, dst, 17, "#FFFFFF", MONO, 600) + "</g>")
    if i == 0:
        body.append(f'<g class="{cls(show(24, 61), 1)}">' + text(FX + 32, y + 43, "→ 203.0.113.1  ISP A", 14, "#9FC3E3", MONO) + "</g>")
        body.append(f'<g class="{cls(show(61, 81), 0)}">' + text(FX + 32, y + 43, "→ 198.51.100.1 ISP B", 14, "#FFD28A", MONO, 600) + "</g>")
        body.append(f'<g class="{cls(show(81, 100), 0)}">' + text(FX + 32, y + 43, "→ 203.0.113.1  ISP A", 14, "#9FC3E3", MONO) + "</g>")
        flash = cls(anim([(0, 0), (61, 0), (62, 1), (66, 0), (81, 0), (82, 1), (86, 0), (100, 0)]), 0)
        body.append(f'<g class="{flash}"><rect x="{FX + 16}" y="{y}" width="{FW - 32}" height="52" rx="10" fill="none" stroke="#FFD28A" stroke-width="3"/></g>')
    else:
        body.append(f'<g class="{g}">' + text(FX + 32, y + 43, "→ " + via, 14, "#9FC3E3", MONO) + "</g>")

# coincidencias del paquete (tiempo 3)
m16 = cls(anim([(0, 0), (45, 0), (46.5, 1), (59, 1), (60, 0), (100, 0)]), 1)
m24 = cls(anim([(0, 0), (49, 0), (50.5, 1), (59, 1), (60, 0), (100, 0)]), 1)
y16, y24 = FROW_Y0 + 2 * 62, FROW_Y0 + 3 * 62
body.append(f'<g class="{m16}"><rect x="{FX + 16}" y="{y16}" width="{FW - 32}" height="52" rx="10" fill="none" stroke="#FFD28A" stroke-width="3" stroke-dasharray="7 5"/>'
            + text(FX + FW - 30, y16 + 22, "coincide /16", 13, "#FFD28A", MONO, 600, "end") + "</g>")
body.append(f'<g class="{m24}"><rect x="{FX + 16}" y="{y24}" width="{FW - 32}" height="52" rx="10" fill="none" stroke="#5BE0A5" stroke-width="3.5"/>'
            + text(FX + FW - 30, y24 + 22, "/24 gana", 13, "#5BE0A5", MONO, 600, "end") + "</g>")

# ---------------- carril del paquete
LY = 600
body.append(text(48, LY + 6, "PAQUETE", 13, GREY, MONO, extra='letter-spacing="2"'))
body.append(f'<line x1="140" y1="{LY}" x2="1152" y2="{LY}" stroke="{LINE}" stroke-width="2" stroke-dasharray="4 6"/>')
mv = anim([(0, 0), (40, 0), (47, 820), (60, 820), (60.1, 0), (100, 0)], "transform", "translateX({}px)")
op = anim([(0, 0), (40, 0), (41, 1), (59, 1), (60, 0), (100, 0)])
kf_n[0] += 1
pk = f"c{kf_n[0]}"
css.append(f".{pk}{{opacity:1;transform:translateX(820px);animation:{mv} {T}s linear infinite,{op} {T}s linear infinite}}")
body.append(f'<g class="{pk}"><rect x="150" y="{LY - 20}" width="180" height="40" rx="20" fill="{CYAN}"/>'
            + text(240, LY + 6, "→ 10.20.5.7", 16, "#FFFFFF", MONO, 600, "middle") + "</g>")
res = cls(show(51, 60), 1)
body.append(f'<g class="{res}">' + text(140, LY + 50, "sale por 192.168.88.254: la máscara más larga manda, antes que la distancia", 16, INK, "Instrument Sans", 600) + "</g>")
fo = cls(show(62, 80), 0)
body.append(f'<g class="{fo}">' + text(140, LY + 50, "Las conexiones nuevas salen por el ISP B. Las rutas de la RIB no se borran: esperan.", 16, BAD, "Instrument Sans", 600) + "</g>")
bk = cls(show(82, 99), 0)
body.append(f'<g class="{bk}">' + text(140, LY + 50, "El gateway vuelve a contestar: la ruta de distancia 1 gana otra vez.", 16, OK, "Instrument Sans", 600) + "</g>")
idle = cls(show(0, 40), 0)
body.append(f'<g class="{idle}">' + text(140, LY + 50, "La RIB guarda todo; la FIB es la lista corta que el router mira con cada paquete.", 16, TXT, "Instrument Sans", 600) + "</g>")

# ---------------- fuentes embebidas (subconjunto)
svg_text = "".join(body)
chars = set(re.sub(r"<[^>]+>", "", svg_text)) | set("0123456789")
chars = "".join(sorted(chars))


def font_face(family, weights, css_url):
    from fontTools import subset
    from fontTools.ttLib import TTFont
    ua = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"}
    cssx = urllib.request.urlopen(urllib.request.Request(css_url, headers=ua)).read().decode()
    blocks = re.findall(r"/\* (latin(?:-ext)?) \*/\s*@font-face\s*\{([^}]*)\}", cssx)
    out = []
    for name, blk in blocks:
        if name != "latin":
            continue
        w = re.search(r"font-weight:\s*(\d+)", blk).group(1)
        url = re.search(r"url\((https://[^)]+\.woff2)\)", blk).group(1)
        raw = urllib.request.urlopen(urllib.request.Request(url, headers=ua)).read()
        f = TTFont(io.BytesIO(raw))
        opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = ["kern", "liga"]
        s = subset.Subsetter(opts); s.populate(text=chars + "·→–"); s.subset(f)
        b = io.BytesIO(); f.flavor = "woff2"; f.save(b)
        data = base64.b64encode(b.getvalue()).decode()
        out.append(f"@font-face{{font-family:'{family}';font-weight:{weights};src:url(data:font/woff2;base64,{data}) format('woff2')}}")
        break  # fuentes variables: un archivo cubre todos los pesos
    return "".join(out)


G = "https://fonts.googleapis.com/css2?family="
fonts = (font_face("Familjen Grotesk", "400 700", G + "Familjen+Grotesk:wght@600&display=block")
         + font_face("Instrument Sans", "400 700", G + "Instrument+Sans:wght@400;600&display=block")
         + font_face("JetBrains Mono", "400 700", G + "JetBrains+Mono:wght@400;600&display=block"))

style = fonts + "".join(css) + "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" width="1200" height="675" role="img" aria-labelledby="t d">'
       f'<title id="t">RIB y FIB en RouterOS 7</title>'
       f'<desc id="d">Animación en cinco tiempos: todas las rutas entran a la RIB; por destino gana la de menor distancia y pasa a la FIB; '
       f'un paquete a 10.20.5.7 coincide con la /16 y la /24 y gana la /24 por máscara más larga; cae el ISP A, check-gateway deja su ruta inactiva '
       f'y la FIB pasa al ISP B; vuelve el ISP A y recupera su lugar.</desc>'
       f'<defs><style>{style}</style>'
       f'<marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{BLUE}"/></marker></defs>'
       + svg_text + "</svg>")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(svg, encoding="utf-8")
print("ok", OUT, len(svg) // 1024, "KB")

if "--frames" in sys.argv:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1200, "height": 675})
        pg.goto("file://" + str(OUT)); pg.wait_for_timeout(400)
        for pct in (10, 30, 52, 70, 90):
            pg.evaluate(f"document.getAnimations().forEach(a=>{{a.pause();a.currentTime={T * 1000 * pct / 100}}})")
            pg.wait_for_timeout(80)
            pg.screenshot(path=str(PREV / f"_anim27-{pct}.png"))
        b.close()
        print("cuadros en", PREV)
