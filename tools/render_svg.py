#!/usr/bin/env python3
"""Renderiza ilustraciones SVG de IES Training a WebP (para el sitio) y PNG (para revisar).

  python3 render_svg.py ilustraciones/akuvox/13.svg [más.svg ...]
  python3 render_svg.py --all            # todas las de /home/claude/ies-training/ilustraciones

Usa Chromium con las fuentes de marca (Familjen Grotesk, Instrument Sans, JetBrains Mono) desde Google Fonts,
para que el texto salga igual que en el portal. Lienzo esperado: viewBox 0 0 1200 675.
Salida:
  - /home/claude/ies-training/site2/ilustraciones/<slug>/<id>.webp  (1800x1013, calidad 86)
  - <mismo lugar del svg>/<id>.png   (vista previa para mirar con Read)
"""
import sys, asyncio, io
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image

ROOT = Path("/home/claude/ies-training/ilustraciones")
OUT = Path("/home/claude/ies-training/site2/ilustraciones")
FONTS = "https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@500;600;700&family=Instrument+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=block"


async def main(paths):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1200, "height": 675}, device_scale_factor=1.5)
        for sp in paths:
            sp = Path(sp).resolve()
            svg = sp.read_text(encoding="utf-8")
            html = f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{FONTS}"><style>html,body{{margin:0;padding:0;background:#fff}}svg{{display:block;width:1200px;height:675px}}</style></head><body>{svg}</body></html>'
            await pg.set_content(html, wait_until="networkidle")
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(150)
            png = await pg.screenshot(clip={"x": 0, "y": 0, "width": 1200, "height": 675})
            im = Image.open(io.BytesIO(png)).convert("RGB")
            slug = sp.parent.name
            (OUT / slug).mkdir(parents=True, exist_ok=True)
            im.save(OUT / slug / f"{sp.stem}.webp", "WEBP", quality=86, method=6)
            im.resize((1200, 675), Image.LANCZOS).save(sp.with_suffix(".png"), "PNG", optimize=True)
            print(f"ok {slug}/{sp.stem}: {(OUT / slug / (sp.stem + '.webp')).stat().st_size // 1024} KB")
        await b.close()


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--all"]:
        args = sorted(str(x) for x in ROOT.glob("*/*.svg"))
    if not args:
        sys.exit(__doc__)
    asyncio.run(main(args))
