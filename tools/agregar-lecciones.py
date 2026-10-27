#!/usr/bin/env python3
"""Suma lecciones nuevas a un curso que ya está en el servidor, sin pisar lo editado desde el panel.

  python3 agregar-lecciones.py <curso-servidor.json> <curso-construido.json> <salida.json> \
      --lecciones 13-20 [--parte "Título de la parte" --por-que "una línea"] [--reemplazar]

- <curso-servidor.json>: el curso tal como está hoy en producción (bajarlo con bajar-curso.sh).
- <curso-construido.json>: lo que sale de build.py (site2/data/<slug>.json) con las lecciones nuevas.
- --lecciones: números (n) de las lecciones del construido a sumar: "13-20", "13,15,17".
- --parte: si se da, las lecciones van a esa parte (se crea al final si no existe, se busca por título).
           Si no, cada lección va a la parte que le asigna el construido (por título de parte), creándola si falta.
- --reemplazar: si una lección con el mismo título (handle) ya existe, se reemplaza su contenido y conserva su id.
Las lecciones nuevas reciben ids que no chocan con los existentes. n se renumera según el orden de las partes.
Después: importar-curso.php <slug> salida.json --forzar  (guarda la versión anterior en el historial).
"""
import argparse, json, sys


def rango(txt):
    out = []
    for p in txt.split(","):
        p = p.strip()
        if "-" in p:
            a, b = p.split("-"); out += list(range(int(a), int(b) + 1))
        elif p:
            out.append(int(p))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("servidor"); ap.add_argument("construido"); ap.add_argument("salida")
    ap.add_argument("--lecciones", required=True); ap.add_argument("--parte"); ap.add_argument("--por-que", default="")
    ap.add_argument("--reemplazar", action="store_true")
    a = ap.parse_args()
    srv = json.load(open(a.servidor, encoding="utf-8")); new = json.load(open(a.construido, encoding="utf-8"))
    if srv.get("slug") != new.get("slug"):
        sys.exit(f"slug distinto: {srv.get('slug')} vs {new.get('slug')}")
    lid = lambda l: str(l.get("id", l.get("n")))
    srv.setdefault("arcs", [])
    used = {lid(l) for l in srv["lessons"]}
    by_handle = {l["handle"].strip().lower(): l for l in srv["lessons"]}
    arc_of_new = {}
    for arc in new.get("arcs", []):
        for r in arc["lessons"]:
            arc_of_new[str(r)] = arc
    wanted = set(rango(a.lecciones))
    added, replaced = [], []
    for l in new["lessons"]:
        if l["n"] not in wanted:
            continue
        old = by_handle.get(l["handle"].strip().lower())
        if old and a.reemplazar:
            keep = lid(old); old.clear(); old.update(l); old["id"] = keep; replaced.append(keep); continue
        if old:
            sys.exit(f"Ya existe una lección '{l['handle']}' (id {lid(old)}). Usá --reemplazar o cambiale el título.")
        src_arc = arc_of_new.get(lid(l))
        nid = str(l["n"]); k = 1
        while nid in used:
            nid = f"{l['n']}-{k}"; k += 1
        used.add(nid)
        l = dict(l, id=nid); srv["lessons"].append(l)
        title = a.parte or (src_arc["title"] if src_arc else "Lecciones nuevas")
        why = a.por_que if a.parte else (src_arc.get("why", "") if src_arc else "")
        arc = next((x for x in srv["arcs"] if x["title"].strip().lower() == title.strip().lower()), None)
        if not arc:
            arc = {"title": title, "why": why, "lessons": []}; srv["arcs"].append(arc)
        arc["lessons"].append(nid); added.append(nid)
    order = [x for arc in srv["arcs"] for x in arc["lessons"]]
    order += [lid(l) for l in srv["lessons"] if lid(l) not in order]
    srv["lessons"].sort(key=lambda l: order.index(lid(l)))
    for i, l in enumerate(srv["lessons"], 1):
        l["n"] = i
    srv["sources_count"] = max(srv.get("sources_count") or 0, new.get("sources_count") or 0)
    json.dump(srv, open(a.salida, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"ok {srv['slug']}: {len(added)} nuevas {added}, {len(replaced)} reemplazadas, {len(srv['lessons'])} en total, {len(srv['arcs'])} partes")


if __name__ == "__main__":
    main()
