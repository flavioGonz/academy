#!/usr/bin/env python3
"""Aplica ilustraciones y conceptos (ilustraciones/<slug>/manifest*.json) a un curso.

  python3 enriquecer.py <curso.json> <slug> <salida.json> [--solo 1,2,13] [--reemplazar-pasos]

- <curso.json>: idealmente la versión vigente del servidor (respeta lo editado en el panel).
- Por cada lección del manifest:
  * fig  -> lesson.fig = {src: ilustraciones/<slug>/<id>.webp, alt, caption}
  * concepts -> lesson.concepts (reemplaza los anteriores; conserva fotos ya cargadas si el nombre coincide)
  * teoria_md -> lesson.theory_md y lesson.theory (html)
  * steps -> inserta <figure class="lab-fig"> en lab.md al final del paso que contiene "after"
             (antes del paso siguiente), y regenera lab.html con pandoc (mismo md() que build.py).
- Verifica que cada imagen exista en site2/ilustraciones/<slug>/<archivo>.webp.
- Es idempotente: no vuelve a insertar una imagen de paso que ya está en el laboratorio.
"""
import argparse, glob, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from build import md  # pandoc GFM con los mismos ajustes del sitio

ROOT = Path("/home/claude/ies-training")
NUM = re.compile(r"^\d+\.\s")


def webp(slug, f):
    name = Path(f).with_suffix(".webp").name
    p = ROOT / "site2" / "ilustraciones" / slug / name
    return f"ilustraciones/{slug}/{name}", p.exists()


def insert_step(lab, anchor, html):
    lines = lab.split("\n")
    fence, idx = False, None
    for i, ln in enumerate(lines):
        if ln.strip().startswith("```"):
            fence = not fence
            continue
        if not fence and anchor in ln:
            idx = i
            break
    if idx is None:
        return None
    # avanzar hasta el próximo paso numerado, una advertencia o el final (saltando bloques de código)
    fence, j = False, idx + 1
    while j < len(lines):
        ln = lines[j]
        if ln.strip().startswith("```"):
            fence = not fence
        elif not fence and (NUM.match(ln) or ln.startswith("⚠️")):
            break
        j += 1
    while j > idx + 1 and not lines[j - 1].strip():
        j -= 1
    return "\n".join(lines[:j] + ["", html, ""] + lines[j:])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("curso"); ap.add_argument("slug"); ap.add_argument("salida")
    ap.add_argument("--solo", default=""); ap.add_argument("--reemplazar-pasos", action="store_true")
    ap.add_argument("--rerender", action="store_true", help="regenera con pandoc el html de idea, impacto, quién lo dice, laboratorio y teoría de todas las lecciones")
    a = ap.parse_args()
    c = json.load(open(a.curso, encoding="utf-8"))
    man = {}
    for f in sorted(glob.glob(str(ROOT / "ilustraciones" / a.slug / "manifest*.json"))):
        for k, v in json.load(open(f, encoding="utf-8")).items():
            man.setdefault(k, {}).update(v)  # varios manifests pueden aportar campos a la misma lección
    solo = {x.strip() for x in a.solo.split(",") if x.strip()}
    by = {str(l.get("id", l["n"])): l for l in c["lessons"]}
    rep = {"fig": 0, "concepts": 0, "steps": 0, "faltan": [], "sin_ancla": []}
    for lid, m in man.items():
        if solo and lid not in solo:
            continue
        l = by.get(str(lid))
        if not l:
            rep["faltan"].append(f"lección {lid} no está en el curso"); continue
        if m.get("fig"):
            src, ok = webp(a.slug, m["fig"]["file"])
            if ok:
                l["fig"] = {"src": src, "alt": m["fig"].get("alt", ""), "caption": m["fig"].get("caption", "")}; rep["fig"] += 1
            else:
                rep["faltan"].append(src)
        if m.get("script_rsc"):
            l["auto"] = m["script_rsc"]; rep["scripts"] = rep.get("scripts", 0) + 1
        if m.get("teoria_md"):
            l["theory_md"] = m["teoria_md"].strip()
            l["theory"] = md(l["theory_md"])
            rep["teoria"] = rep.get("teoria", 0) + 1
        if m.get("concepts"):
            prevpics = {k.get("name", "").strip().lower(): k.get("pics") for k in l.get("concepts", []) if k.get("pics")}
            l["concepts"] = [{k: x.get(k, "") for k in ("name", "para_que", "como", "ejemplo")} for x in m["concepts"] if x.get("name")]
            for k in l["concepts"]:
                if prevpics.get(k["name"].strip().lower()):
                    k["pics"] = prevpics[k["name"].strip().lower()]
            rep["concepts"] += len(l["concepts"])
        lab = l.get("lab", {}).get("md", "")
        if a.reemplazar_pasos:
            lab = re.sub(r'\n*<figure class="lab-fig">.*?</figure>\n*', "\n\n", lab, flags=re.S)
        changed = False
        for st in sorted(m.get("steps", []), key=lambda s: s.get("step", 0)):
            src, ok = webp(a.slug, st["file"])
            if not ok:
                rep["faltan"].append(src); continue
            if src in lab:
                continue
            cap = st.get("caption", "").replace("<", "&lt;")
            alt = st.get("alt", "").replace('"', "&quot;").replace("<", "&lt;")
            html = f'<figure class="lab-fig"><img src="{src}" alt="{alt}" loading="lazy" width="1200" height="675"><figcaption><b>Paso {st.get("step", "")}.</b> {cap}</figcaption></figure>'
            new = insert_step(lab, st.get("after", ""), html) if st.get("after") else None
            if new is None:
                rep["sin_ancla"].append(f"{lid}: {st['file']} (ancla: {st.get('after', '')[:40]})"); continue
            lab, changed = new, True
            rep["steps"] += 1
        if changed or a.reemplazar_pasos:
            l["lab"]["md"] = lab.strip()
            l["lab"]["html"] = md(lab)
    if a.rerender:
        from build import inline
        for l in c["lessons"]:
            if l.get("idea_md"): l["idea"] = [inline(x) for x in l["idea_md"]]
            if l.get("impact_md"): l["impact"] = inline(l["impact_md"])
            if l.get("who_md"): l["who"] = inline(l["who_md"])
            if l.get("lab", {}).get("md"): l["lab"]["html"] = md(l["lab"]["md"])
            if l.get("theory_md"): l["theory"] = md(l["theory_md"])
        rep["rerender"] = len(c["lessons"])
    json.dump(c, open(a.salida, "w", encoding="utf-8"), ensure_ascii=False)
    print(json.dumps(rep, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
