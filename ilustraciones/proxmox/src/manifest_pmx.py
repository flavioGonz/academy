"""Genera /home/claude/ies-training/ilustraciones/proxmox/manifest.json y lo valida.

Valida: anclas de pasos (existen, únicas, fuera de código, 15-40 caracteres), teoría (250-450 palabras,
subtítulos, anclas de figuras únicas y fuera de títulos, archivos en site2), guiones largos, y los scripts
(variables declaradas y usadas, 15-60 líneas, ASCII, sintaxis con bash -n tras reemplazar las variables).
"""
import json, re, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _mbase import M
import _m1, _m2, _m3  # noqa: F401  (registran las lecciones)

ROOT = Path("/home/claude/ies-training")
OUT = ROOT / "ilustraciones/proxmox/manifest.json"
SITE = ROOT / "site2/ilustraciones/proxmox"
curso = json.load(open(ROOT / "site2/data/proxmox.json", encoding="utf-8"))
labs = {str(l["id"]): l["lab"]["md"] for l in curso["lessons"]}
order = [str(i) for i in range(1, 13)]
err = []


def lab_lines_outside_code(md):
    out, fence = [], False
    for ln in md.split("\n"):
        if ln.strip().startswith("```"):
            fence = not fence
            continue
        if not fence:
            out.append(ln)
    return out


for k in order:
    m = M[k]
    lines = lab_lines_outside_code(labs[k])
    for st in m["steps"]:
        a = st["after"]
        hits = [ln for ln in lines if a in ln]
        if len(hits) != 1 or not (15 <= len(a) <= 40):
            err.append(f"{k}: ancla de paso '{a}' aparece {len(hits)} veces o largo {len(a)}")
        elif not re.match(rf"^{st['step']}\.\s", hits[0]):
            err.append(f"{k}: ancla '{a}' no está en el paso {st['step']}: {hits[0][:50]}")
        if not (SITE / st["file"].replace(".svg", ".webp")).exists():
            err.append(f"{k}: falta {st['file']} en site2")
    if not (SITE / m["fig"]["file"].replace(".svg", ".webp")).exists():
        err.append(f"{k}: falta la figura principal")
    t = m["teoria_md"]
    w = len(re.findall(r"\w+", t))
    if not (250 <= w <= 450):
        err.append(f"{k}: teoría con {w} palabras")
    if "### Un poco de historia" not in t or "### Cómo funciona" not in t:
        err.append(f"{k}: faltan subtítulos")
    paras = t.split("\n\n")
    for f in m["teoria_figs"]:
        a = f["after"]
        if t.count(a) != 1 or not (15 <= len(a) <= 60):
            err.append(f"{k}: ancla de teoría '{a}' x{t.count(a)} largo {len(a)}")
        if any(a in p and p.startswith("###") for p in paras):
            err.append(f"{k}: ancla de teoría dentro de un título")
        if not (SITE / f["file"]).exists():
            err.append(f"{k}: falta {f['file']}")
    if not any(f["file"].endswith(".svg") for f in m["teoria_figs"]):
        err.append(f"{k}: sin animación en teoría")
    if not (2 <= len(m["concepts"]) <= 4):
        err.append(f"{k}: {len(m['concepts'])} conceptos")
    sc = m.get("script_rsc")
    if sc:
        code = sc["codigo"]
        used = set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", code))
        decl = {v["nombre"] for v in sc["variables"]}
        if used != decl:
            err.append(f"{k}: variables usadas {used} declaradas {decl}")
        n = code.count("\n") + 1
        if not (15 <= n <= 60):
            err.append(f"{k}: script de {n} líneas")
        bad = [c for c in code if ord(c) > 127]
        if bad:
            err.append(f"{k}: script con caracteres no ASCII {set(bad)}")
        if not any("Listo" in x for x in code.split("\n")[-5:]):
            err.append(f"{k}: el script no termina con Listo")
        filled = code
        for v in sc["variables"]:
            filled = filled.replace("{{" + v["nombre"] + "}}", v["valor"])
        with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as fh:
            fh.write(filled)
        r = subprocess.run(["bash", "-n", fh.name], capture_output=True, text=True)
        if r.returncode:
            err.append(f"{k}: bash -n: {r.stderr.strip()}")
    print(k, "palabras", w, "conceptos", len(m["concepts"]), "pasos", len(m["steps"]), "teoria_figs", len(m["teoria_figs"]),
          "script", (sc["codigo"].count("\n") + 1) if sc else "-")

s = json.dumps(M, ensure_ascii=False)
if "—" in s or "–" in s:
    err.append("hay guiones largos")
json.dump({k: M[k] for k in order}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", OUT, len(M), "lecciones")
print("ERRORES:" if err else "sin errores", *err, sep="\n  ")
sys.exit(1 if err else 0)
