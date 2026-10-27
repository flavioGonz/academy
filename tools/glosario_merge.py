#!/usr/bin/env python3
"""Suma una propuesta de glosario ({"terms":[…], "alias_agregar":{}, "modificar":{}}) a site2/data/glosario.json sin duplicar."""
import json, sys
p = "/home/claude/ies-training/site2/data/glosario.json"
d = json.load(open(p)); g = json.load(open(sys.argv[1]))
ex = {t["id"] for t in d["terms"]}; terms = {t["term"].lower() for t in d["terms"]}
al = {a.lower() for t in d["terms"] for a in t.get("aliases", [])}
n = 0
for t in g.get("terms", []):
    if t["id"] in ex or t["term"].lower() in terms or t["term"].lower() in al:
        print("ya", t["term"]); continue
    t["aliases"] = [a for a in t.get("aliases", []) if a.lower() not in al and a.lower() not in terms]
    al.update(a.lower() for a in t["aliases"]); d["terms"].append(t); n += 1
by = {t["id"]: t for t in d["terms"]}
for k, v in (g.get("alias_agregar") or {}).items():
    for a in (v if isinstance(v, list) else [v]):
        if k in by and a.lower() not in al:
            by[k]["aliases"].append(a); al.add(a.lower())
for k, v in (g.get("modificar") or {}).items():
    if k in by: by[k].update(v)
json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)
print(f"{n} nuevas, {len(d['terms'])} en total")
