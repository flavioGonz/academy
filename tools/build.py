#!/usr/bin/env python3
"""Build the IES Training static site data from claudemy workspaces.

Reads /home/claude/claudemy/<slug>/class/{course.json, NN-*/card.md, script.txt, quiz.json, *.mp3, timings.json}
Writes  /home/claude/ies-training/site/data/catalog.json, data/<slug>.json, audio/<slug>/NN.mp3

Usage: python3 build.py [slug ...]   (default: every course in ORDER that has a course.json)
"""
import json, re, shutil, subprocess, sys
from pathlib import Path
import markdown

WS = Path("/home/claude/claudemy")
SITE = Path("/home/claude/ies-training/site2")
ORDER = ["mikrotik", "grandstream", "unifi", "omada", "akuvox", "hikcentral", "paradox", "bosch-incendio", "proxmox", "vmware", "windows", "linux"]
SECTIONS = {"**Escuchá:**": "listen", "**La idea, en tres líneas**": "idea", "**Impacto:**": "impact",
            "**Quién lo dice:**": "who", "**Laboratorio**": "lab", "**Regla para quedarse**": "rule",
            "**Saltear**": "skip", "**Para profundizar (opcional)**": "deeper"}
TAG = re.compile(r"\[[^\]]*\]")
URL = re.compile(r"https?://\S+")


def prep(text):
    out, prev = [], ""
    for line in text.strip().splitlines():
        if re.match(r"^\d+\.\s", line) and prev.strip() and not re.match(r"^\s*(\d+\.|[-*])\s", prev):
            out.append("")
        out.append(line); prev = line
    return "\n".join(out)


def md(text):
    text = prep(text)
    r = subprocess.run(["pandoc", "-f", "gfm", "-t", "html", "--no-highlight", "--wrap=none"], input=text.strip(), capture_output=True, text=True)
    html = r.stdout.strip()
    html = re.sub(r'<pre class="([\w+-]+)"><code>', r'<pre><code class="language-\1">', html)
    html = re.sub(r'<(ol|ul)( start="\d+")? type="1"', r'<\1\2', html)
    html = html.replace('<tr class="odd">', '<tr>').replace('<tr class="even">', '<tr>').replace('<tr class="header">', '<tr>')
    return html.replace("<a href=", '<a target="_blank" rel="noopener" href=')


def inline(text):
    h = md(text)
    return re.sub(r"^<p>(.*)</p>$", r"\1", h, flags=re.S)


def parse_card(text):
    lines = text.splitlines()
    title = next((l for l in lines if l.startswith("# ")), "# Lección")[2:].strip()
    parts, cur = {}, None
    for l in lines:
        hit = next((k for k in SECTIONS if l.strip().startswith(k)), None)
        if hit:
            cur = SECTIONS[hit]
            parts[cur] = [l.strip()[len(hit):]]
        elif cur:
            parts[cur].append(l)
    out = {"title": title}
    idea = "\n".join(parts.get("idea", []))
    out["idea_md"] = [re.sub(r"^\s*[-*]\s+", "", l).strip() for l in idea.splitlines() if re.match(r"^\s*[-*]\s+", l)]
    out["idea"] = [inline(x) for x in out["idea_md"]]
    out["impact_md"] = "\n".join(parts.get("impact", [])).strip()
    out["who_md"] = "\n".join(parts.get("who", [])).strip()
    out["impact"] = inline(out["impact_md"])
    out["who"] = inline(out["who_md"])
    lab = parts.get("lab", [""])
    head = lab[0]
    m = re.search(r"·\s*([^·]+?)\s*·\s*(\d+)\s*min", head)
    out["lab"] = {"energy": m.group(1).strip() if m else "", "minutes": int(m.group(2)) if m else None,
                  "md": "\n".join(lab[1:]).strip(), "html": md("\n".join(lab[1:]))}
    out["rule"] = " ".join(l.strip() for l in parts.get("rule", []) if l.strip()).strip()
    srcs = []
    for l in parts.get("deeper", []):
        u = URL.search(l)
        if not u:
            continue
        url = u.group(0).rstrip(").,;*")
        label = l[:u.start()].strip().lstrip("-* ").rstrip(": ").strip() or url
        label = re.sub(r"[*_`]", "", label)
        srcs.append({"label": label, "url": url})
    out["sources"] = srcs
    return out


def script_lines(text):
    res = []
    for l in text.splitlines():
        m = re.match(r"^([AB]):\s*(.+)$", l.strip())
        if not m:
            continue
        t = TAG.sub("", m.group(2)).strip()
        if t:
            res.append({"s": m.group(1), "t": t})
    return res


def duration(mp3):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)],
                       capture_output=True, text=True)
    try:
        return round(float(r.stdout.strip()))
    except ValueError:
        return None


def build(slug):
    cls = WS / slug / "class"
    course = json.loads((cls / "course.json").read_text(encoding="utf-8"))
    lessons = []
    dirs = sorted(p for p in cls.glob("[0-9][0-9]-*") if p.is_dir())
    meta = {l.get("n"): l for l in course.get("lessons", [])}
    for d in dirs:
        n = int(d.name[:2])
        card = d / "card.md"
        if not card.exists():
            continue
        c = parse_card(card.read_text(encoding="utf-8"))
        handle = re.sub(r"^Lecci[oó]n\s*\d+\.\s*", "", c["title"]).strip()
        lines = script_lines((d / "script.txt").read_text(encoding="utf-8")) if (d / "script.txt").exists() else []
        quiz = json.loads((d / "quiz.json").read_text(encoding="utf-8")) if (d / "quiz.json").exists() else []
        lessons.append({"n": n, "id": str(n), "handle": handle, "summary": meta.get(n, {}).get("summary", ""),
                        "idea": c["idea"], "idea_md": c["idea_md"], "impact": c["impact"], "impact_md": c["impact_md"],
                        "who": c["who"], "who_md": c["who_md"], "lab": c["lab"],
                        "rule": c["rule"], "sources": c["sources"], "script": lines, "quiz": quiz,
                        })
    course["lessons"] = lessons
    for a in course.get("arcs", []):
        a["lessons"] = [str(x) for x in a.get("lessons", [])]
    for k in ("splits",):
        for s in course.get(k, []):
            for f in ("topic", "sides", "decide"):
                if f in s:
                    s[f] = inline(s[f])
    (SITE / "data").mkdir(parents=True, exist_ok=True)
    (SITE / "data" / f"{slug}.json").write_text(json.dumps(course, ensure_ascii=False), encoding="utf-8")
    labmin = sum(l["lab"]["minutes"] or 0 for l in lessons)
    return {"slug": slug, "title": course.get("title"), "vendor": course.get("vendor"),
            "tagline": course.get("tagline"), "level": course.get("level"),
            "lessons": [{"n": l["n"], "id": l["id"], "handle": l["handle"]} for l in lessons], "draft": False,
            "lab_minutes": labmin,
            "sources_count": course.get("sources_count")}


def main(slugs):
    cat_path = SITE / "data" / "catalog.json"
    catalog = {c["slug"]: c for c in json.loads(cat_path.read_text())["courses"]} if cat_path.exists() else {}
    for s in slugs:
        if (WS / s / "class" / "course.json").exists():
            catalog[s] = build(s)
            print(f"built {s}: {len(catalog[s]['lessons'])} lecciones, {catalog[s]['lab_minutes']} min de laboratorio")
        else:
            print(f"skip {s}: no course.json yet")
    courses = [catalog[s] for s in ORDER if s in catalog]
    cat_path.parent.mkdir(parents=True, exist_ok=True)
    cat_path.write_text(json.dumps({"courses": courses, "order": ORDER}, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1:] or ORDER)
