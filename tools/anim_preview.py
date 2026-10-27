#!/usr/bin/env python3
"""Vista previa confiable de animaciones ya generadas: PNG por instante y cuadro fijo.

  python3 anim_preview.py <archivo.svg> [más.svg] [--pct 10,35,60,85] [--out <carpeta>]

Fija cada instante por CSS (animation-delay negativo, en pausa) en una página nueva; la duración del ciclo
se lee del propio SVG. Por defecto deja los PNG en ilustraciones/<slug>/_rev-<nombre>-<pct>.png.
"""
import re, sys, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path("/home/claude/ies-training/ilustraciones")


def main(args):
    pcts, out, files = [10, 35, 60, 85], None, []
    it = iter(args)
    for a in it:
        if a == "--pct": pcts = [float(x) for x in next(it).split(",")]
        elif a == "--out": out = Path(next(it))
        else: files.append(Path(a).resolve())
    if not files: sys.exit(__doc__)
    with sync_playwright() as p, tempfile.TemporaryDirectory() as td:
        b = p.chromium.launch()
        for f in files:
            src = f.read_text(encoding="utf-8")
            m = re.search(r"([\d.]+)s linear infinite", src)
            T = float(m.group(1)) if m else 20
            dest = out or (ROOT / f.parent.name)
            dest.mkdir(parents=True, exist_ok=True)
            outs = []
            for pct in pcts:
                fix = f"*{{animation-delay:-{T * pct / 100:.3f}s!important;animation-play-state:paused!important}}"
                tmp = Path(td) / "f.svg"; tmp.write_text(src.replace("</style>", fix + "</style>", 1), encoding="utf-8")
                pg = b.new_page(viewport={"width": 1200, "height": 675}); pg.goto("file://" + str(tmp)); pg.wait_for_timeout(120)
                o = dest / f"_rev-{f.stem}-{int(pct)}.png"; pg.screenshot(path=str(o)); outs.append(o.name); pg.close()
            ctx = b.new_context(viewport={"width": 1200, "height": 675}, reduced_motion="reduce")
            pg = ctx.new_page(); pg.goto("file://" + str(f)); pg.wait_for_timeout(150)
            o = dest / f"_rev-{f.stem}-fijo.png"; pg.screenshot(path=str(o)); outs.append(o.name); ctx.close()
            print(f"{f.name} (ciclo {T}s): {' '.join(outs)}")
        b.close()


if __name__ == "__main__":
    main(sys.argv[1:])
