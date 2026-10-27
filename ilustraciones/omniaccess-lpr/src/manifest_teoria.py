"""Escribe manifest-teoria-1-12.json (solo teoria_figs) y valida las anclas contra el teoria_md combinado."""
import glob, json, sys
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-lpr/src")
from teoria_figs_lpr import FIGS

D = "/home/claude/ies-training/ilustraciones/omniaccess-lpr/"
OUT = D + "manifest-teoria-1-12.json"
json.dump({k: {"teoria_figs": v} for k, v in FIGS.items()}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
m = {}
for f in sorted(glob.glob(D + "manifest*.json")):
    for k, v in json.load(open(f, encoding="utf-8")).items():
        if isinstance(v, dict):
            m.setdefault(k, {}).update(v)
bad = 0
for k, figs in FIGS.items():
    th = m[k].get("teoria_md", "")
    for tf in figs:
        n = th.count(tf["after"])
        heading = any(tf["after"] in l for l in th.splitlines() if l.startswith("#"))
        ok = n == 1 and not heading and 15 <= len(tf["after"]) <= 60
        bad += not ok
        print(("ok " if ok else "MAL"), k, tf["file"], n, len(tf["after"]), tf["after"])
print("escrito", OUT, "· problemas:", bad)
