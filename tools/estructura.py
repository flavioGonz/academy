#!/usr/bin/env python3
"""Aplica la estructura didáctica lineal (ilustraciones/<slug>/estructura.json) a un curso.

  python3 estructura.py <curso.json> <slug> <salida.json> [--sin-avisos]

- Módulos (arcs) en el orden nuevo, con why y objetivos.
- Lecciones reordenadas según los módulos y renumeradas (n). Los ids no cambian: capturas y progreso se mantienen.
- Por lección: objetivos, conecta, sigue (o cierre en la última), requisitos.
- Curso: objetivo, recorrido y avance secuencial activado.
- Avisos: reemplaza referencias por número ("lección 10") por la sugerencia, en el texto de la lección
  (laboratorio, ideas, impacto, quién lo dice, regla, examen, charla) y regenera el html.
"""
import json, re, sys, argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from build import md, inline

ROOT = Path("/home/claude/ies-training")


UNI = "cero uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciséis diecisiete dieciocho diecinueve veinte veintiuno veintidós veintitrés veinticuatro veinticinco veintiséis veintisiete veintiocho veintinueve".split()
DEC = {3: "treinta", 4: "cuarenta", 5: "cincuenta", 6: "sesenta", 7: "setenta", 8: "ochenta", 9: "noventa"}


def palabras(n):
    if n < 30:
        return UNI[n]
    d, u = divmod(n, 10)
    return DEC[d] + (f" y {UNI[u]}" if u else "")


NUMW = r"(?:\d+|(?:cero|uno|una|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|trece|catorce|quince|dieci\w+|veinte|veinti\w+|treinta|cuarenta|cincuenta|sesenta|setenta|ochenta|noventa)(?: y (?:uno|una|dos|tres|cuatro|cinco|seis|siete|ocho|nueve))?)"
APERTURA = re.compile(r"^(Lección|Última lección|Lección número) " + NUMW + r"(?=[:,.])")


def renumerar_charla(l):
    """La charla suele abrir con 'Lección once: ...'. Tras reordenar, se ajusta al número nuevo."""
    for sl in l.get("script", [])[:3]:
        t = sl.get("t", "")
        nt = APERTURA.sub(lambda m: "Lección " + palabras(l["n"]), t, count=1)
        if nt != t:
            sl["t"] = nt
            return True
    return False


def strip_obj(x):
    x = re.sub(r"^Al terminar (el módulo |la lección |el curso )?vas a poder\s+", "", x.strip())
    return x[:1].upper() + x[1:] if x else x


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("curso"); ap.add_argument("slug"); ap.add_argument("salida"); ap.add_argument("--sin-avisos", action="store_true")
    a = ap.parse_args()
    c = json.load(open(a.curso, encoding="utf-8"))
    e = json.load(open(ROOT / "ilustraciones" / a.slug / "estructura.json", encoding="utf-8"))
    by = {str(l.get("id", l["n"])): l for l in c["lessons"]}
    # Extras en tres pasadas, para que el resultado no dependa del nombre del archivo:
    # 1) insertar y avisos, 2) modulos_nuevos (ganan sobre un insertar viejo que ubicaba la lección en otro módulo),
    # 3) lecciones, por "prioridad" (de menor a mayor, 0 por defecto) y nombre: la de más prioridad pisa los campos.
    extras = [(xf, json.load(open(xf, encoding="utf-8"))) for xf in sorted((ROOT / "ilustraciones" / a.slug).glob("estructura-extra*.json"))]
    for xf, x in extras:  # lecciones insertadas después (ej. 36 tras la 4) y textos que las enlazan
        for ins in x.get("insertar", []):
            for m in e["modulos"]:
                ls = [str(i) for i in m["lessons"]]
                if str(ins["despues_de"]) in ls and str(ins["id"]) not in ls:
                    ls.insert(ls.index(str(ins["despues_de"])) + 1, str(ins["id"])); m["lessons"] = ls
        e.setdefault("avisos", []).extend(x.get("avisos", []))
    for xf, x in extras:
        for nm in x.get("modulos_nuevos", []):  # módulo nuevo: saca sus lecciones de donde estaban y lo ubica antes de otro
            ids = [str(i) for i in nm["lessons"]]
            for m in e["modulos"]:
                m["lessons"] = [str(i) for i in m["lessons"] if str(i) not in ids]
            nuevo = {k: nm[k] for k in ("title", "why", "objetivos") if k in nm}; nuevo["lessons"] = ids
            e["modulos"] = [m for m in e["modulos"] if m["title"] != nm["title"]]
            pos = next((i for i, m in enumerate(e["modulos"]) if m["title"] == nm.get("antes_de")), len(e["modulos"]))
            e["modulos"].insert(pos, nuevo)
    for xf, x in sorted(extras, key=lambda t: (t[1].get("prioridad", 0), t[0].name)):
        for lid, v in x.get("lecciones", {}).items():
            e.setdefault("lecciones", {}).setdefault(str(lid), {}).update(v)
    rep = {"modulos": 0, "lecciones": 0, "avisos_aplicados": 0, "avisos_sin_texto": [], "faltan_en_curso": []}
    arcs, seen = [], set()
    for m in e["modulos"]:
        ls = [str(x) for x in m["lessons"] if str(x) in by]
        rep["faltan_en_curso"] += [str(x) for x in m["lessons"] if str(x) not in by]
        seen.update(ls)
        if not ls:
            continue
        arcs.append({"title": m["title"], "why": m.get("why", ""), "objetivos": [strip_obj(o) for o in m.get("objetivos", [])], "lessons": ls})
    extra = [i for i in by if i not in seen]
    if extra:  # lecciones que no están en la estructura (ej. agregadas desde el panel): al final, en su módulo de antes
        arcs.append({"title": "Más lecciones", "why": "", "objetivos": [], "lessons": extra})
    c["arcs"] = arcs
    order = [i for m in arcs for i in m["lessons"]]
    c["lessons"].sort(key=lambda l: order.index(str(l.get("id", l["n"]))))
    for i, l in enumerate(c["lessons"], 1):
        l["n"] = i
    rep["modulos"] = len(arcs)
    for lid, x in e.get("lecciones", {}).items():
        l = by.get(str(lid))
        if not l:
            continue
        l["objetivos"] = [strip_obj(o) for o in x.get("objetivos", [])]
        for f in ("conecta", "sigue"):
            if x.get(f):
                l[f] = x[f]
            else:
                l.pop(f, None)
        if x.get("cierre"):
            l["sigue"] = x["cierre"]
        if x.get("requisitos"):
            l["requisitos"] = [str(r) for r in x["requisitos"]]
        rep["lecciones"] += 1
    cur = e.get("curso", {})
    if cur.get("objetivo"):
        c["objetivo"] = strip_obj(cur["objetivo"])
    if cur.get("recorrido"):
        c["recorrido"] = cur["recorrido"]
    c["secuencial"] = True
    if not a.sin_avisos:
        for av in e.get("avisos", []):
            ids = [s.strip() for s in str(av.get("id", "")).split(",")]
            t, sug = av.get("texto", ""), av.get("sugerencia", "")
            t, sug = re.sub(r"^[AB]:\s*", "", t), re.sub(r"^[AB]:\s*", "", sug)  # avisos de la charla vienen con el hablante
            if len(ids) != 1 or not t or not sug or ids[0] not in by:
                continue
            l = by[ids[0]]
            hit = False
            def sub(s):
                nonlocal hit
                if isinstance(s, str) and t in s:
                    hit = True
                    return s.replace(t, sug)
                return s
            lab = l.get("lab", {})
            if t in lab.get("md", ""):
                lab["md"] = sub(lab["md"]); lab["html"] = md(lab["md"])
            if any(t in x for x in l.get("idea_md", [])):
                l["idea_md"] = [sub(x) for x in l["idea_md"]]; l["idea"] = [inline(x) for x in l["idea_md"]]
            for f in ("impact", "who"):
                if t in l.get(f + "_md", ""):
                    l[f + "_md"] = sub(l[f + "_md"]); l[f] = inline(l[f + "_md"])
            for f in ("rule", "summary", "theory_md"):
                if t in l.get(f, ""):
                    l[f] = sub(l[f])
                    if f == "theory_md":
                        l["theory"] = md(l[f])
            for q in l.get("quiz", []):
                q["q"] = sub(q.get("q", "")); q["why"] = sub(q.get("why", "")); q["options"] = [sub(o) for o in q.get("options", [])]
            for sl in l.get("script", []):
                sl["t"] = sub(sl.get("t", ""))
            if hit:
                rep["avisos_aplicados"] += 1
            else:
                rep["avisos_sin_texto"].append(f"{ids[0]}: {t[:60]}")
    rep["charla_renumerada"] = sum(renumerar_charla(l) for l in c["lessons"])
    json.dump(c, open(a.salida, "w", encoding="utf-8"), ensure_ascii=False)
    print(json.dumps(rep, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
