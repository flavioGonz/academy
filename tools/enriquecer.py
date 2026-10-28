#!/usr/bin/env python3
"""Aplica ilustraciones y conceptos (ilustraciones/<slug>/manifest*.json) a un curso.

  python3 enriquecer.py <curso.json> <slug> <salida.json> [--solo 1,2,13] [--reemplazar-pasos]

- <curso.json>: idealmente la versión vigente del servidor (respeta lo editado en el panel).
- Por cada lección del manifest:
  * fig  -> lesson.fig = {src: ilustraciones/<slug>/<id>.webp, alt, caption}
  * concepts -> lesson.concepts (reemplaza los anteriores; conserva fotos ya cargadas si el nombre coincide)
  * teoria_md -> lesson.theory_md y lesson.theory (html)
  * anims -> lesson.anims (animaciones SVG del Resumen, "Cómo se ve en la red"; suma las que faltan)
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


def rsc_ascii(code):
    """La terminal de RouterOS maneja mal lo que no es ASCII y toma '?' como pedido de ayuda: el código queda en ASCII."""
    import unicodedata
    code = code.replace("·", "-").replace("¿", "").replace("¡", "").replace("→", "->").replace("…", "...").replace("—", "-").replace("–", "-")
    code = "".join(ch for ch in unicodedata.normalize("NFKD", code) if not unicodedata.combining(ch))
    out = []
    for ln in code.split("\n"):
        if ln.lstrip().startswith("#"):
            ln = ln.replace("?", "")
        out.append(ln.encode("ascii", "replace").decode().replace("\ufffd", "?") if any(ord(c) > 127 for c in ln) else ln)
    return "\n".join(out)


def webp(slug, f):
    # el manifest nombra la fuente (.svg); en el sitio va el .webp. Si no hay .webp pero el .svg está en site2,
    # es una animación (tools/anim.py) y se usa tal cual.
    d = ROOT / "site2" / "ilustraciones" / slug
    name = Path(f).with_suffix(".webp").name
    if f.endswith(".svg") and not (d / name).exists() and (d / Path(f).name).exists():
        name = Path(f).name
    p = d / name
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
    # el paso también termina en el primer párrafo sin sangría después de una línea en blanco ("Errores típicos…")
    if True:
        fence, k = False, idx + 1
        while k < j:
            ln = lines[k]
            if ln.strip().startswith("```"):
                fence = not fence
            elif not fence and ln.strip() and not ln[0].isspace() and not lines[k - 1].strip() and not ln.startswith("<figure"):
                j = k
                break
            k += 1
    while j > idx + 1 and not lines[j - 1].strip():
        j -= 1
    return "\n".join(lines[:j] + ["", html, ""] + lines[j:])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("curso"); ap.add_argument("slug"); ap.add_argument("salida")
    ap.add_argument("--solo", default=""); ap.add_argument("--reemplazar-pasos", action="store_true")
    ap.add_argument("--campos", default="fig,auto,teoria,teoria_figs,concepts,steps,anims", help="qué aplicar (para no pisar lo editado en el panel): fig,auto,teoria,teoria_figs,concepts,steps,anims")
    ap.add_argument("--rerender", action="store_true", help="regenera con pandoc el html de idea, impacto, quién lo dice, laboratorio y teoría de todas las lecciones")
    a = ap.parse_args()
    c = json.load(open(a.curso, encoding="utf-8"))
    man = {}
    for f in sorted(glob.glob(str(ROOT / "ilustraciones" / a.slug / "manifest*.json")), key=lambda x: (Path(x).name.startswith("manifest-anims"), x)):  # los de animaciones, al final
        suma = Path(f).name.startswith("manifest-anims")  # los de animaciones suman a los pasos y figuras de teoría existentes
        for k, v in json.load(open(f, encoding="utf-8")).items():
            e = man.setdefault(k, {})
            for kk, vv in v.items():
                if suma and isinstance(vv, list) and isinstance(e.get(kk), list):
                    e[kk] = e[kk] + vv
                else:
                    e[kk] = vv  # en los demás, el manifest posterior reemplaza el campo
    solo = {x.strip() for x in a.solo.split(",") if x.strip()}
    campos = {x.strip() for x in a.campos.split(",") if x.strip()}
    by = {str(l.get("id", l["n"])): l for l in c["lessons"]}
    rep = {"fig": 0, "concepts": 0, "steps": 0, "faltan": [], "sin_ancla": []}
    for lid, m in man.items():
        if solo and lid not in solo:
            continue
        l = by.get(str(lid))
        if not l:
            rep["faltan"].append(f"lección {lid} no está en el curso"); continue
        if m.get("fig") and "fig" in campos:
            src, ok = webp(a.slug, m["fig"]["file"])
            if ok:
                l["fig"] = {"src": src, "alt": m["fig"].get("alt", ""), "caption": m["fig"].get("caption", "")}; rep["fig"] += 1
            else:
                rep["faltan"].append(src)
        if m.get("script_rsc") and "auto" in campos:
            au = dict(m["script_rsc"]); au["codigo"] = rsc_ascii(au.get("codigo", ""))
            l["auto"] = au; rep["scripts"] = rep.get("scripts", 0) + 1
        if m.get("teoria_md") and "teoria" in campos:
            l["theory_md"] = m["teoria_md"].strip()
            l["theory"] = md(l["theory_md"])
            rep["teoria"] = rep.get("teoria", 0) + 1
        for tf in (m.get("teoria_figs", []) if "teoria_figs" in campos else []):  # figuras o animaciones dentro de la teoría, después del párrafo con "after"
            src = f"ilustraciones/{a.slug}/{tf['file']}"
            if not (ROOT / "site2" / src).exists():
                rep["faltan"].append(src); continue
            th = l.get("theory_md", "")
            if not th or src in th:
                continue
            paras = th.split("\n\n")
            k = next((i for i, x in enumerate(paras) if tf["after"] in x), None)
            if k is None:
                rep["sin_ancla"].append(f"{lid}: teoría {tf['file']}"); continue
            alt = tf.get("alt", "").replace('"', "&quot;").replace("<", "&lt;")
            cap = tf.get("caption", "").replace("<", "&lt;")
            paras.insert(k + 1, f'<figure class="lab-fig th-fig"><img src="{src}" alt="{alt}" loading="lazy" width="1200" height="675"><figcaption>{cap}</figcaption></figure>')
            l["theory_md"] = "\n\n".join(paras); l["theory"] = md(l["theory_md"])
            rep["teoria_figs"] = rep.get("teoria_figs", 0) + 1
        if m.get("anims") and "anims" in campos:  # animaciones del Resumen ("Cómo se ve en la red"); suma las que falten, no quita
            cur = l.get("anims", [])
            for an in m["anims"]:
                src = f"ilustraciones/{a.slug}/{an['file']}"
                if not (ROOT / "site2" / src).exists():
                    rep["faltan"].append(src); continue
                if any(x.get("src") == src for x in cur):
                    continue
                cur.append({"src": src, "alt": an.get("alt", ""), "caption": an.get("caption", "")})
                rep["anims"] = rep.get("anims", 0) + 1
            if cur:
                l["anims"] = cur[:4]
        if m.get("concepts") and "concepts" in campos:
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
        for st in (sorted(m.get("steps", []), key=lambda s: s.get("step", 0)) if "steps" in campos else []):
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
