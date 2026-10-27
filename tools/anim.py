#!/usr/bin/env python3
"""Animaciones para la teoría de las lecciones de IES Training.

SVG animado con CSS: sin scripts (se muestra con <img>, que no ejecuta nada), con las fuentes de marca
embebidas en subconjunto (tools/fonts/*.woff2), en loop, y con un cuadro fijo para quien tiene
"reducir movimiento" activado. Lienzo 1200x675, la misma paleta que las ilustraciones (ilus.py).

Uso típico (ver ilustraciones/mikrotik/src/anim_27_rib_fib.py como ejemplo completo):

    from anim import Anim
    a = Anim(T=20, kicker="MIKROTIK · RUTAS", title="RIB y FIB: todas las rutas, y las que se usan")
    a.steps(["Paso 1 …", "Paso 2 …", "Paso 3 …"], still=1)    # leyenda numerada que avanza sola
    a.add(f'<rect x="48" y="180" width="300" height="80" rx="14" fill="{a.WHITE}" stroke="{a.LINE}" stroke-width="2"/>')
    a.add(a.text(70, 225, "Siempre visible", 18, a.INK, a.SANS, 600))
    a.add(a.group(a.text(70, 300, "Aparece en el paso 2", 18), a.show(33, 66), still=0))
    a.add(a.group('<circle cx="0" cy="0" r="10" fill="#17A8D4"/>',
                  a.move([(0, 100, 400), (40, 100, 400), (60, 700, 400), (100, 700, 400)]), still=1))
    a.save("/home/claude/ies-training/site2/ilustraciones/<slug>/<id>-t1.svg",
           title="…", desc="Descripción completa de la animación para quien no la ve")
    a.preview([10, 40, 70, 95], "/home/claude/ies-training/ilustraciones/<slug>/_anim-<id>")   # PNG por instante

Tiempos en porcentaje del ciclo (0 a 100). `still` es la opacidad del cuadro fijo (movimiento reducido).
"""
import base64, io, re, sys
from pathlib import Path

FONTS = Path(__file__).parent / "fonts"


class Anim:
    # paleta (igual a ilus.py)
    BG, INK, BLUE, CYAN, GREY, TXT, LINE = "#F7FAFD", "#04223D", "#0A63B8", "#17A8D4", "#6E88A1", "#41627F", "#DDE8F2"
    OK, OKBG, BAD, BADBG, AMB, AMBBG, SLATE, WHITE, NAVY2 = "#0E8F5E", "#E3F5EC", "#D2492F", "#FCEAE6", "#B26A00", "#FFF3DC", "#EEF3F8", "#FFFFFF", "#0B3A66"
    HEAD, SANS, MONO = "Familjen Grotesk", "Instrument Sans", "JetBrains Mono"

    def __init__(self, T=20, kicker="", title="", grid=True):
        self.T, self.css, self.body, self.n = T, [], [], 0
        self._markers = {}
        self.add(f'<rect width="1200" height="675" fill="{self.BG}"/>')
        if grid:
            self.add('<rect width="1200" height="675" fill="url(#grid)" opacity=".7"/>')
        if kicker:
            self.add(self.text(48, 56, kicker, 15, self.CYAN, self.MONO, 400, extra='letter-spacing="2.4"'))
        if title:
            self.add(self.text(48, 92, title, 32, self.INK, self.HEAD, 600))

    # ---------- piezas
    def add(self, s):
        self.body.append(s)
        return s

    @staticmethod
    def esc(s):
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def text(self, x, y, s, size=17, fill=None, fam=None, weight=400, anchor="start", extra=""):
        return (f'<text x="{x}" y="{y}" font-family="{fam or self.SANS}" font-size="{size}" font-weight="{weight}" '
                f'fill="{fill or self.TXT}" text-anchor="{anchor}" {extra}>{self.esc(s)}</text>')

    def box(self, x, y, w, h, fill=None, stroke=None, rx=14, sw=2, extra=""):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill or self.WHITE}"{st} {extra}/>'

    def pill(self, x, y, label, fg=None, bg=None, size=14, h=28, anchor="start"):
        w = int(len(label) * size * 0.62 + 26)
        x0 = x - w if anchor == "end" else (x - w / 2 if anchor == "middle" else x)
        return self.box(x0, y, w, h, bg or self.SLATE, rx=h / 2) + self.text(x0 + w / 2, y + h * 0.68, label, size, fg or self.INK, self.MONO, 600, "middle")

    def arrow(self, d, color=None, width=3, dash=""):
        c = color or self.BLUE
        mid = self._marker(c)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{width}"{da} marker-end="url(#{mid})"/>'

    def _marker(self, color):
        k = "m" + color.strip("#")
        self._markers[k] = color
        return k

    # ---------- tiempo
    def keyframes(self, points, prop="opacity", fmt="{}"):
        """points: [(porcentaje, valor)] → nombre de @keyframes."""
        self.n += 1
        name = f"k{self.n}"
        d = {}
        for p, v in points:
            d[round(float(p), 2)] = v
        steps = " ".join(f"{p}%{{{prop}:{fmt.format(v)}}}" for p, v in sorted(d.items()))
        self.css.append(f"@keyframes {name}{{{steps}}}")
        return name

    def show(self, a, b=100, fade=1.2):
        """Visible entre a% y b% del ciclo, con fundido corto. Devuelve el nombre de la animación."""
        pts = [(0, 1)] if a <= 0 else [(0, 0), (a, 0), (min(a + fade, 100), 1)]
        if b < 100:
            pts += [(max(b - fade, a + fade), 1), (b, 0), (100, 0)]
        else:
            pts += [(98.5, 1), (100, 1 if a <= 0 else 0)]
        return self.keyframes(pts)

    def pulse(self, at, dur=6, lo=0.25):
        """Resalta (opacidad lo→1→lo) alrededor de 'at'%."""
        return self.keyframes([(0, lo), (at, lo), (at + 1, 1), (at + dur, 1), (at + dur + 1, lo), (100, lo)])

    def move(self, pts):
        """pts: [(porcentaje, x, y)] → animación de transform translate."""
        return self.keyframes([(p, f"{x}px,{y}px") for p, x, y in pts], "transform", "translate({})")

    def group(self, inner, *anims, still=1, origin=None):
        """Envuelve inner en <g> con una o varias animaciones (las de opacidad y transform se combinan)."""
        if anims and not any(self._is_opacity(a) for a in anims):
            # sin animación de opacidad, la base (still) mandaría siempre: se agrega una que deja ver mientras corre
            anims = tuple(anims) + (self.keyframes([(0, 1), (100, 1)]),)
        self.n += 1
        c = f"c{self.n}"
        names = ",".join(f"{a} {self.T}s linear infinite" for a in anims)
        base = f"opacity:{still};" if still is not None else ""
        if any(self._is_move(a) for a in anims):
            base += "transform-box:view-box;"
            last = [x for x in self.css if any(x.startswith(f"@keyframes {a}{{") for a in anims if self._is_move(a))]
            if last:  # cuadro fijo: la posición del primer punto del movimiento
                m = re.search(r"0(?:\.0)?%\{transform:(translate\([^)]*\))\}", last[0])
                if m:
                    base += f"transform:{m.group(1)};"
        if origin:
            base += f"transform-origin:{origin};"
        self.css.append(f".{c}{{{base}animation:{names}}}")
        return f'<g class="{c}">{inner}</g>'

    def _is_opacity(self, name):
        return any(x.startswith(f"@keyframes {name}{{") and "opacity" in x for x in self.css)

    def _is_move(self, name):
        return any(x.startswith(f"@keyframes {name}{{") and "transform" in x for x in self.css)

    def steps(self, captions, x=48, y=118, still=0, cap_x=None, size=18):
        """Leyenda numerada (1, 2, 3…) que avanza sola; cada paso dura lo mismo. still = índice del paso que se ve fijo."""
        k = len(captions)
        span = 100 / k
        cap_x = cap_x or (x + k * 44 + 22)
        for i, cap in enumerate(captions):
            a, b = i * span, (i + 1) * span
            on = self.show(a, b, 0.6)
            cx = x + i * 44
            self.add(self.box(cx, y, 36, 36, self.WHITE, self.LINE, rx=18))
            self.add(self.text(cx + 18, y + 24, str(i + 1), 16, self.GREY, self.MONO, 600, "middle"))
            self.add(self.group(self.box(cx, y, 36, 36, self.BLUE, rx=18) + self.text(cx + 18, y + 24, str(i + 1), 16, self.WHITE, self.MONO, 600, "middle"), on, still=1 if i == still else 0))
            self.add(self.group(self.text(cap_x, y + 25, cap, size, self.INK, self.SANS, 600), on, still=1 if i == still else 0))
        return [(i * span, (i + 1) * span) for i in range(k)]

    # ---------- salida
    def _fonts(self, chars):
        try:
            from fontTools import subset
            from fontTools.ttLib import TTFont
        except ImportError:
            return ""
        out = []
        for fam, stem in ((self.HEAD, "FamiljenGrotesk"), (self.SANS, "InstrumentSans"), (self.MONO, "JetBrainsMono")):
            for sub in ("latin", "latin-ext"):
                p = FONTS / f"{stem}-{sub}.woff2"
                if not p.exists():
                    continue
                f = TTFont(str(p))
                cmap = f.getBestCmap() or {}
                need = "".join(ch for ch in chars if ord(ch) in cmap)
                if not need:
                    continue
                o = subset.Options(); o.flavor = "woff2"; o.layout_features = ["kern", "liga"]
                s = subset.Subsetter(o); s.populate(text=need); s.subset(f)
                b = io.BytesIO(); f.flavor = "woff2"; f.save(b)
                out.append(f"@font-face{{font-family:'{fam}';font-weight:400 700;src:url(data:font/woff2;base64,{base64.b64encode(b.getvalue()).decode()}) format('woff2')}}")
        return "".join(out)

    def svg(self, title, desc):
        body = "".join(self.body)
        chars = set(re.sub(r"<[^>]+>", "", body)) | set("0123456789·→")
        chars.discard("\n")
        markers = "".join(f'<marker id="{k}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{c}"/></marker>' for k, c in self._markers.items())
        style = self._fonts("".join(sorted(chars))) + "".join(self.css) + "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" width="1200" height="675" role="img" aria-labelledby="t d">'
                f'<title id="t">{self.esc(title)}</title><desc id="d">{self.esc(desc)}</desc>'
                f'<defs><style>{style}</style>{markers}'
                f'<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#E6EEF6" stroke-width="1"/></pattern></defs>'
                f'{body}</svg>')

    def save(self, path, title, desc):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        s = self.svg(title, desc)
        if "<script" in s.lower():
            raise SystemExit("una animación no puede tener scripts")
        path.write_text(s, encoding="utf-8")
        print(f"ok {path} · {len(s) // 1024} KB · ciclo {self.T}s")
        return path

    def preview(self, pcts, out_prefix, svg_path=None):
        """PNG de cada instante (porcentaje del ciclo) para revisar con Read, más el cuadro fijo.
        Cada cuadro se saca de una copia con el instante fijado en el CSS (animation-delay negativo y en pausa),
        en una página nueva: pausar por JavaScript a veces deja pintado un cuadro viejo."""
        import tempfile
        from playwright.sync_api import sync_playwright
        svg_path = Path(svg_path or self._last).resolve()
        src = svg_path.read_text(encoding="utf-8")
        outs = []
        with sync_playwright() as p, tempfile.TemporaryDirectory() as td:
            b = p.chromium.launch()
            for pct in pcts:
                t = self.T * pct / 100
                fix = f"*{{animation-delay:-{t:.3f}s!important;animation-play-state:paused!important}}"
                tmp = Path(td) / f"f{pct}.svg"
                tmp.write_text(src.replace("</style>", fix + "</style>", 1), encoding="utf-8")
                pg = b.new_page(viewport={"width": 1200, "height": 675})
                pg.goto("file://" + str(tmp)); pg.wait_for_timeout(120)
                o = f"{out_prefix}-{pct}.png"; pg.screenshot(path=o); outs.append(o); pg.close()
            ctx = b.new_context(viewport={"width": 1200, "height": 675}, reduced_motion="reduce")
            pg2 = ctx.new_page(); pg2.goto("file://" + str(svg_path)); pg2.wait_for_timeout(200)
            o = f"{out_prefix}-fijo.png"; pg2.screenshot(path=o); outs.append(o)
            b.close()
        print("cuadros:", " ".join(outs))
        return outs

    def write(self, path, title, desc, preview=None, prefix=None):
        """save + preview en un paso."""
        self._last = self.save(path, title, desc)
        if preview:
            self.preview(preview, prefix or str(Path(path).with_suffix("")))
        return self._last


if __name__ == "__main__":
    sys.exit(__doc__)
