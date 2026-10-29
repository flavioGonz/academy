#!/usr/bin/env python3
"""Quita el número de lección de los rótulos de las ilustraciones y animaciones, y corrige las referencias a otras lecciones.

  python3 sin_numero_leccion.py <curso> <curso.json> [--aplicar]

Por qué: el id de una lección queda fijo, pero su número de orden (n) cambia cuando se suman o reordenan lecciones.
Los rótulos tipo "AKUVOX · LECCIÓN 13 · PASO 2" quedaban con el número viejo.
- Rótulo en mayúsculas "· LECCIÓN <id>" → se quita ("AKUVOX · PASO 2").
- Referencia en minúscula "(lección <id>)" → pasa al n actual de esa lección según <curso.json> (la versión vigente del servidor).
- Toca: ilustraciones/<curso>/*.svg (fuentes de los .webp), site2/ilustraciones/<curso>/*.svg (animaciones) y los scripts
  ilustraciones/<curso>/src/*.py, para que volver a generarlos no traiga el número de vuelta.
Sin --aplicar solo muestra qué cambiaría. Con --aplicar escribe y vuelve a renderizar los .webp de las fuentes que cambiaron.
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path("/home/claude/ies-training")
KICK = re.compile(r"\s*·\s*(LECCIÓN|Lección) \d+(?=\s*·|\s*[\"<])")
REF = re.compile(r"(lección )(\d+)")


def main():
    slug, cj = sys.argv[1], sys.argv[2]
    aplicar = "--aplicar" in sys.argv
    c = json.load(open(cj, encoding="utf-8"))
    nmap = {str(l.get("id", l["n"])): str(l["n"]) for l in c["lessons"]}
    fix_ref = lambda m: m.group(1) + nmap.get(m.group(2), m.group(2))
    files = sorted((ROOT / "ilustraciones" / slug).glob("*.svg")) + sorted((ROOT / "site2" / "ilustraciones" / slug).glob("*.svg")) + sorted((ROOT / "ilustraciones" / slug / "src").glob("*.py"))
    render, n = [], 0
    for p in files:
        t = p.read_text(encoding="utf-8")
        u = KICK.sub("", t)
        u = REF.sub(fix_ref, u)
        if u == t:
            continue
        n += 1
        a = set(re.findall(r"(?:LECCIÓN|Lección) \d+|lección \d+", t)); b = set(re.findall(r"(?:LECCIÓN|Lección) \d+|lección \d+", u))
        print(f"{p.relative_to(ROOT)}: {sorted(a - b)} -> {sorted(b - a)}")
        if aplicar:
            p.write_text(u, encoding="utf-8")
            if p.suffix == ".svg" and p.parent == ROOT / "ilustraciones" / slug:
                render.append(str(p.relative_to(ROOT)))
    print(f"{n} archivos {'cambiados' if aplicar else 'a cambiar'}; {len(render)} webp a renderizar")
    if aplicar and render:
        for i in range(0, len(render), 40):
            subprocess.run([sys.executable, str(ROOT / "tools" / "render_svg.py"), *render[i:i + 40]], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
