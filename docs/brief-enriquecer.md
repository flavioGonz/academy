# Brief: enriquecer un curso completo (ilustraciones, conceptos, teoría con animaciones, módulos)

Nico (dueño de IES, integrador de seguridad electrónica en Uruguay) pidió para cada curso del portal IES Training:
ilustraciones que ayuden a entender cada paso concreto; una reflexión de cada concepto (para qué se creó, cómo se usa,
ejemplo claro); un poco de historia y teoría; la teoría con ilustraciones y animaciones; y que el curso sea una línea
de aprendizaje lineal en módulos, no lecciones sueltas.

1. Leé entera `/home/claude/ies-training/ilustraciones/GUIA.md` (ignorá `script_rsc` salvo que tu curso tenga una
   terminal donde pegar comandos: para Linux, un script bash de verificación o configuración por lección sigue las
   mismas reglas, campo `script_rsc` con variables `{{…}}`; para Windows, PowerShell; para Proxmox y VMware, shell del host).
2. Copiá el esquema de trabajo del ejemplo más completo, Paradox: `/home/claude/ies-training/ilustraciones/paradox/`
   (src/_pdx.py y _apdx.py de ayudantes, 1.py…, anim_*.py, manifest_pdx.py, estructura_pdx.py, glosario_pdx.py).
   `tools/ilus.py` y `tools/anim.py` no se modifican; tus ayudantes van en tu `src/`.
3. Fuentes: `/home/claude/claudemy/<slug>/` (class/<NN>/card.md, script.txt, quiz.json; research/notes; raw/) y el JSON
   publicado `/home/claude/ies-training/site2/data/<slug>.json` (ids = campo `id`; laboratorio en `lab.md`).
   Nada inventado; fechas y estándares solo si están en fuentes o son conocimiento técnico estable.
4. Render de fijas con `tools/render_svg.py` bajo `flock /home/claude/ies-training/render.lock`; animaciones con
   `tools/anim.py`; revisión de TODO con Read (PNG de fijas, `tools/anim_preview.py` para animaciones y su cuadro fijo).
5. Entregables en `/home/claude/ies-training/ilustraciones/<slug>/`: SVG + PNG; WebP y animaciones en
   `site2/ilustraciones/<slug>/` (sin PNG ahí); `manifest.json` (fig, steps, concepts, teoria_md, teoria_figs con al
   menos una animación por lección, script_rsc si corresponde); `estructura.json`; `glosario-propuesta.json`
   (`{"terms":[…], "alias_agregar":{}, "modificar":{}}`, validada sobre una copia de `site2/data/glosario.json`, que ya
   tiene más de 600 entradas: no dupliques; agregá alias si hace falta).
6. Pruebas limpias: `python3 tools/enriquecer.py site2/data/<slug>.json <slug> /tmp/claude-0/<slug>-e.json` y
   `python3 tools/estructura.py /tmp/claude-0/<slug>-e.json <slug> /tmp/claude-0/<slug>-f.json`.
7. No edites card.md, quiz.json, script.txt, course.json ni el glosario; no despliegues; no corras con glob scripts
   que no son tuyos; no toques carpetas de otros cursos.
8. Tono rioplatense con voseo, sin exigencias, sin guiones largos. Reportá módulos, archivos, pruebas y lo no confirmado.
