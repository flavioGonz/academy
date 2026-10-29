#!/bin/bash
# Arma /home/claude/trainer desde las fuentes de trabajo, sin secretos ni datos de usuarios.
set -e
S=/home/claude/ies-training; C=/home/claude/claudemy; T=/home/claude/trainer
cd $T
rm -rf site tools ilustraciones skill docs/brief-*.md
mkdir -p site docs cursos deploy
(cd $S/site2 && tar cf - --exclude=./capturas --exclude=./logos --exclude=./api/config.php --exclude='*.sqlite*' --exclude=./db --exclude='*.log' --exclude='*.png' .) | (cd site && tar xf -)
cp $S/tools -r tools; rm -rf tools/__pycache__
(cd $S && tar cf - --exclude='*.png' ilustraciones) | tar xf -
cp -r $S/skill skill
cp $S/brief-ies.md $S/brief-mikrotik-nuevas.md docs/
for d in $C/*/; do s=$(basename $d); [ -f $d/sources.json ] || continue
  rm -rf cursos/$s; mkdir -p cursos/$s
  (cd $d && tar cf - --exclude=./raw --exclude=./audio --exclude='*.mp3' --exclude='*.wav' --exclude=.lock .) | (cd cursos/$s && tar xf -)
done
cp /home/claude/trainer-tools/config.example.php site/api/
cp /home/claude/trainer-tools/sync.sh deploy/sync-repo.sh
find . -name '__pycache__' -prune -exec rm -rf {} +
# chequeo de secretos
if grep -rIlE "(EDITOR_KEY|password|passwd|token|secret)\s*[:=]\s*['\"][^'\"\{\$]{8,}" --exclude-dir=.git . | grep -v -E 'config\.example\.php|\.md$|cursos/' ; then echo "REVISAR posibles secretos"; fi
du -sh $T
# los cursos del repo: la última versión importada al servidor (no la salida cruda de build.py)
python3 - <<'PY'
import json, glob, os
T="/home/claude/trainer/site/data"; O="/mnt/user-data/outputs"
cat=json.load(open(f"{T}/catalog.json"))
for i,e in enumerate(cat["courses"]):
    fs=sorted(glob.glob(f"{O}/{e['slug']}-imp-*.json"), key=os.path.getmtime)
    if not fs: continue
    d=json.load(open(fs[-1])); json.dump(d, open(f"{T}/{e['slug']}.json","w"), ensure_ascii=False)
    cat["courses"][i]={"slug":e["slug"],"title":d["title"],"vendor":d.get("vendor",""),"tagline":d.get("tagline",""),"level":d.get("level",""),
      "draft":bool(d.get("draft")),"logo":d.get("logo"),"lessons":[{"n":l["n"],"id":str(l.get("id",l["n"])),"handle":l["handle"]} for l in d["lessons"]],
      "lab_minutes":sum(int((l.get("lab") or {}).get("minutes") or 0) for l in d["lessons"]),"sources_count":d.get("sources_count")}
json.dump(cat, open(f"{T}/catalog.json","w"), ensure_ascii=False)
print("cursos del repo = versión publicada")
PY
