# trainer · IES Training

Portal de capacitación técnica de IES (Uruguay): **entrenamientos.ies.com.uy**.
Cursos de Akuvox, MikroTik, Grandstream, UniFi, Omada, HikCentral, Paradox, Bosch Incendio, Proxmox, VMware, Windows y Linux, con lecciones cortas, laboratorio, teoría, examen, ilustraciones, glosario con tooltips y scripts listos para pegar.

## Estructura

| Carpeta | Qué hay |
|---|---|
| `site/` | El sitio: SPA estática (`index.html`, `assets/app.js`, `assets/styles.css`) + API PHP 8 con SQLite (`api/`). `data/` tiene los cursos construidos, `catalog.json` y `glosario.json`. `ilustraciones/` las WebP publicadas. |
| `cursos/<slug>/` | Workspaces de investigación y guion de cada curso (método claudemy): `sources.json`, `research/notes/`, `class/<NN-tema>/` con `card.md`, `script.txt`, `quiz.json`. Sin `raw/` (páginas descargadas). |
| `tools/` | `build.py` (cursos → JSON del sitio), `agregar-lecciones.py`, `enriquecer.py` (ilustraciones, conceptos, teoría, scripts), `estructura.py` (módulos y avance lineal), `ilus.py` + `render_svg.py` (ilustraciones SVG → WebP), `check_lessons_es.py`, `glosario_check.py`, `rsc_check.py`, `importar-curso.php`. |
| `ilustraciones/<slug>/` | Fuentes de las ilustraciones (SVG + scripts `src/`), `manifest*.json` (fig, pasos, conceptos, teoría, script_rsc), `estructura*.json`. `GUIA.md` es la especificación. |
| `deploy/` | Scripts de despliegue en Proxmox (CT 115) detrás de Nginx Proxy Manager. Leen las credenciales del entorno; ninguna está en el repo. |
| `skill/` | Skill `ies-entrenamientos` para Claude. |
| `docs/` | Briefs de contenido y tono. |

## Flujo para actualizar un curso

1. Bajar la versión del servidor (respeta lo editado desde el panel).
2. `python3 tools/build.py <slug>`
3. `python3 tools/agregar-lecciones.py servidor.json site/data/<slug>.json a.json --lecciones N-M [--reemplazar]`
4. `python3 tools/enriquecer.py a.json <slug> b.json`
5. `python3 tools/estructura.py b.json <slug> final.json`
6. Subir e importar con `importar-curso.php <slug> final.json --forzar` (guarda la versión anterior en el historial).

## Puesta en marcha

- `site/api/config.example.php` → `config.php` con el hash de la clave de editor.
- nginx: `/data/<slug>.json` bloqueado (salvo `catalog.json` y `glosario.json`); `/capturas/` e `/ilustraciones/` con `auth_request /api/gate.php`. Ver `deploy/nginx-acceso.sh`.
- `gifenc` (MIT) va incluido en `site/assets/vendor/`.
