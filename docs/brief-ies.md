# Brief: un curso técnico de IES Training con el método Claudemy

Vas a producir UN curso completo para el portal **IES Training** (training.ies.com.uy) de IES — Ingeniería en Seguridad S.R.L., integrador uruguayo de seguridad electrónica (control de acceso, CCTV, alarmas, incendio, WiFi, telefonía IP, redes y servidores). El público son técnicos instaladores y de soporte: tienen base de redes (IP, máscara, gateway, VLAN de nombre) pero no son expertos en este producto. Nivel: inicial a intermedio, práctico, orientado a obra y a soporte.

Seguís el método de la skill **claudemy** (instalada en `/root/.claude/skills/claudemy/`). Leé primero su `SKILL.md` y los archivos de `references/` (reader-brief, map-brief, writer-brief, lesson-design, lesson-example). Este brief adapta ese método a cursos técnicos en español; donde los dos difieran, manda este brief.

## Workspace
`/home/claude/claudemy/<slug>/` con la estructura de claudemy (`sources.json`, `raw/web/`, `research/`, `class/`). Scripts:
- scraper: `python3 /root/.claude/skills/claudemy/scripts/scrape.py <workspace> web`
- checker en español (usá este, no el original): `python3 /home/claude/ies-training/tools/check_lessons_es.py <workspace> [carpetas...]`
No rendericés audio: el audio lo hace el orquestador después.

## Pasos (comprimidos respecto a claudemy, mismo rigor de fuentes)
1. **Mapa del tema** → `research/topics.md`: 12 a 16 subtemas T01..T16. Buscá en la web cómo se enseña (documentación oficial, academias del fabricante, certificaciones: MTCNA, UniFi/UEWA, Omada, HikCentral, Proxmox, VCP, etc.).
2. **Lista de lectura** → `sources.json` con 18 a 30 páginas reales que viste en resultados de búsqueda o en páginas abiertas: documentación oficial y manuales del fabricante primero, después practicantes (blogs técnicos serios, foros oficiales del fabricante), y algunas voces que discrepan. Máximo 3 páginas por sitio, salvo la documentación oficial del fabricante que puede tener hasta 6 (es la fuente primaria). Corré el scraper; si guarda menos de 15 páginas, buscá reemplazos y re-corré. Páginas que solo cargan con JavaScript van a fallar: reemplazalas.
3. **Lectura y notas** → `research/notes/a.md` (y `b.md` si hace falta) siguiendo `reader-brief.md`. Lo hacés vos mismo, no lances subagentes.
4. **Mapa de acuerdos** → `research/agreement-map.md` según `map-brief.md`, versión compacta: 20 a 35 temas.
5. **Plan** → `class/lesson-plan.md`: **12 lecciones en 3 arcos de 4** (fundamentos → operación diaria → avanzado/troubleshooting), cada arco con una línea de "por qué este arco" y un título corto. Incluí la sección "Divisiones" (dónde las fuentes discrepan) y "Huecos".
6. **Lecciones** → `class/NN-<handle-slug>/` con 3 archivos: `script.txt`, `card.md`, `quiz.json`. Corré el checker sobre todo el workspace y corregí hasta que pase. Si una lección falla 3 veces, reportala.
7. **Ficha del curso** → `class/course.json` (formato abajo).

## script.txt (diálogo de 2 conductores, en español rioplatense)
- `A:` es **Lucía** (voz femenina), `B:` es **Martín** (voz masculina). Una intervención por línea, nada más en la línea. No digan sus nombres a cada rato; está bien que se nombren una vez.
- 260 a 360 palabras (unos 2 minutos). Tono de dos técnicos con experiencia charlando en la camioneta camino a una obra: cálido, concreto, con reacciones ("claro", "uf", "exacto", "¿en serio?"), voseo uruguayo natural (vos tenés, fijate, probá). Nada de clase magistral.
- Forma: gancho → la idea → cuántas fuentes coinciden y quién discrepa → una historia/número/caso real de una página leída → ejemplo concreto en obra → el laboratorio a probar → cierre con lo que cambia.
- Los comandos, rutas de menú y valores se dicen como se hablan ("barra ip barra address", "el puerto ocho mil cuatrocientos cuarenta y tres"). Nada de bloques de código en el guion: el código va en la tarjeta.
- Máximo 3 etiquetas de audio, solo `[risas]` o `[suspiro]`, al inicio de un turno.
- Sin guiones largos (—, –) ni dobles guiones en guion ni tarjeta. Sin frases de exigencia al oyente: "tenés que", "debés", "asegurate de", "no te olvides" (el checker las rechaza). Se ofrece, no se ordena: "conviene", "probá", "lo que funciona es". Las advertencias de seguridad se dicen igual de claras: "antes de actualizar, backup. Siempre."

## card.md (secciones exactas, en este orden; el checker las busca literalmente)
```
# Lección N. <Nombre de 2 a 3 palabras>

**Escuchá:** <handle-slug>.mp3 (2 min)

**La idea, en tres líneas**
- ...
- ...
- ...

**Impacto:** una línea: qué mejora en obra o en soporte cuando hacés esto.

**Quién lo dice:** N de M fuentes coinciden; quién discrepa y en qué, en una línea.

**Laboratorio** · <Rápido|Foco|Campo|Admin> · <N> min
Pasos numerados, concretos, ejecutables en 5 a 20 minutos en un equipo de laboratorio, una VM o el simulador/demo del fabricante si existe. Incluí los comandos o rutas de menú exactos en bloques de código (```routeros, ```bash, ```powershell, ```text según corresponda). Si algo es riesgoso en producción, decilo en una línea con ⚠️.

**Regla para quedarse**
Una oración para el manual de bolsillo del técnico.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- <descripción corta>: <url exacta de una página en raw/>
- <descripción corta>: <url>
```
- Toda url citada tiene que existir como línea `url:` en un archivo de `raw/`. Hacé grep antes de escribirla.
- Los números de una fuente son afirmaciones de esa fuente ("según la documentación de MikroTik...").
- Versiones: decí la versión de firmware/software a la que aplica algo cuando importe (RouterOS 7 vs 6, UniFi Network 9.x, Proxmox VE 8/9, ESXi 8, etc.) y preferí la versión actual a la fecha (octubre 2026).

## quiz.json (3 preguntas por lección)
```json
[
  {"q": "Pregunta concreta, de situación de obra si se puede", "options": ["A", "B", "C", "D"], "answer": 1, "why": "Por qué la correcta es correcta, en 1 o 2 oraciones."}
]
```
`answer` es el índice base 0. Distractores plausibles (errores reales que comete un técnico). Variá la posición de la correcta.

## class/course.json
```json
{
  "slug": "<slug>",
  "title": "<Título del curso, ej. MikroTik RouterOS para integradores>",
  "vendor": "<Fabricante>",
  "tagline": "<una línea con gancho>",
  "description": "<2 a 3 oraciones: qué vas a poder hacer al terminar>",
  "level": "Inicial a intermedio",
  "audience": "<para quién, una línea>",
  "prerequisites": ["...", "..."],
  "outcomes": ["4 a 6 cosas que el técnico va a saber hacer"],
  "version_note": "<a qué versiones aplica el curso>",
  "arcs": [{"title": "...", "why": "...", "lessons": [1,2,3,4]}, ...],
  "splits": [{"topic": "...", "sides": "...", "decide": "cómo decidir"}],
  "sources_count": <páginas en raw/web>,
  "lessons": [{"n": 1, "dir": "01-<handle-slug>", "handle": "<Nombre>", "summary": "<una línea>"}]
}
```

## Límites
- Contenido público: no incluyas datos internos de IES, nombres de clientes, IPs reales de clientes, usuarios ni contraseñas. Los ejemplos usan rangos de documentación (192.168.88.0/24, 10.10.10.0/24, 203.0.113.0/24) y contraseñas obviamente de ejemplo.
- Nada de contenido para evadir licencias, crackear o saltear protecciones del fabricante.
- No copies párrafos de las fuentes: escribí con tus palabras y citá.

## Mensaje final (corto)
Slug, páginas en raw/, lecciones que pasan el checker (N/12), títulos de las 12 lecciones en una línea, y cualquier problema abierto.
