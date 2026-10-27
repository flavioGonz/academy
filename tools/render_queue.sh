#!/bin/sh
# Renders every finished course (has class/course.json); serialized with flock; render_es skips done lessons.
exec 9>/home/claude/ies-training/render.lock
flock 9
for c in /home/claude/claudemy/*/; do
  [ -f "$c/class/course.json" ] || continue
  python3 /home/claude/ies-training/tools/render_es.py "$c"class/[0-9][0-9]-* >> /home/claude/ies-training/render-$(basename $c).log 2>&1
done
