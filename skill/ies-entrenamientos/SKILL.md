---
name: ies-entrenamientos
description: Mantener y ampliar el portal de cursos técnicos de IES en https://entrenamientos.ies.com.uy (IES Training): cursos y lecciones nuevas, módulos, ilustraciones y animaciones, correcciones, el editor y el panel, el repo academy y el despliegue en el CT 115 de Proxmox. USAR SIEMPRE que se hable del portal de entrenamientos, IES Training, "los cursos", "la academia", sumar un curso/lección/capítulo/módulo (MikroTik, Grandstream, UniFi, Omada, Akuvox, HikCentral, OmniAccess, Paradox, Bosch Incendio, Proxmox, VMware, Windows, Linux u otro), animaciones o fotos de lecciones, el panel de administración, o publicar/actualizar entrenamientos.ies.com.uy, aunque no se nombre el portal.
---

# IES Training · entrenamientos.ies.com.uy

Portal de cursos técnicos para los instaladores y el soporte de IES (Ingeniería en Seguridad S.R.L., Uruguay). Español rioplatense con voseo, sin audio (Nico no lo quiere, tampoco voces sintetizadas), estilo visual IES (azules #002F58 / #011E38 / #0A63B8 / #17A8D4, fondo #F3F7FB, Familjen Grotesk + Instrument Sans + JetBrains Mono) con estructura tipo Udemy/Coursera.

Al 29/10/2026: 16 cursos. MikroTik 39 lecciones, Akuvox 45, Grandstream 19 (con un módulo de líneas analógicas por FXO y la troncal SIP de Antel), UniFi, Omada, HikCentral, Proxmox, VMware, Windows y Linux 12 cada uno, Paradox y Bosch Incendio 16, OmniAccess LPR 12, Face, Intrusión y Filas 10 (los cuatro OmniAccess en borrador). Glosario de unos 900 términos.

**La documentación viva está en el doc del proyecto Entrenamientos: `claude/entrenamientos-despliegue.md`.** Leelo al empezar (estado, infraestructura, pendientes) y actualizalo al terminar.

## Dónde vive cada cosa

| Qué | Dónde |
|---|---|
| Producción | CT **115** `entrenamientos` en **pve01** (172.26.20.218), nginx + php8.4-fpm + sqlite3 (sin curl: wget). Web `/var/www/entrenamientos` (cursos en `data/*.json`, `capturas/`, `logos/`, `ilustraciones/`); datos privados en `/var/www/entrenamientos-data/` (SQLite, sesiones, `historial/<curso>/` con 60 versiones); respaldos en `/root/respaldos/` (5 de web, 20 de datos) |
| Acceso | `/data/<curso>.json` da 403 (solo `catalog.json` y `glosario.json` públicos); `/ilustraciones/` y `/capturas/` pasan por `auth_request /api/gate.php` (401 sin sesión). NPM proxy host 11, Let's Encrypt id 12, A en el cPanel |
| Código y contenido | Repo **público** https://github.com/flavioGonz/academy (rama `main`): `site/` (el sitio), `tools/`, `ilustraciones/` (fuentes .svg y scripts), `cursos/<slug>/` (workspaces claudemy sin `raw/`), `deploy/` (scripts del CT, `sync-repo.sh`), `skill/`, `docs/` |
| Trabajo en la nube | `/home/claude/ies-training/` (`site2/` = sitio, `tools/`, `ilustraciones/`, briefs) y `/home/claude/claudemy/<slug>/` (workspaces) |
| PC de Nico | `C:\Users\usuario\Claude\ies-training\`: `pvex.py` (SSH a pve0X: `run`, `cmd`, `put`, `get`), `deploy-site.sh`, `importar-curso.php`, `sync/` (JSON bajados del servidor). Clon del repo en `C:\Users\usuario\Claude\trainer` (el push sale de ahí, con Git Credential Manager) |

La red 172.26.20.x solo se alcanza desde la PC: Desktop Commander `start_process` (PowerShell) o, si se cae, `device_bash` en la VM del escritorio (`cd $HOME/mnt/ies-training && python3 pvex.py …`; paramiko con `pip --user`). Archivos de la nube a la PC con `device_commit_files` (nombre nuevo cada vez, hash verificado con `sha256sum` o `Get-FileHash`); de la PC a la nube con `device_stage_files` (aparecen en `/mnt/user-data/uploads/ies-training/…`). Límite del puente: menos de 30 MB por archivo.

## Primer paso en una sesión nueva

Si `/home/claude/ies-training/site2` no existe: `git clone https://github.com/flavioGonz/academy /home/claude/trainer` y armá las carpetas de trabajo desde ahí (`site` → `ies-training/site2`, `tools`, `ilustraciones`, `docs/brief-*.md`; `cursos/<slug>` → `claudemy/<slug>`). `site2/api/config.php` no está en el repo (hay `config.example.php`): para pruebas locales generá uno con un hash de prueba. Hace falta pandoc, Pillow, Playwright (ya instalado) y brotli (`pip install --break-system-packages brotli`) para las animaciones. La skill claudemy vive en `/root/.claude/skills/claudemy/`.

## Regla de oro: el servidor es la fuente de verdad

Nico edita en el panel (textos, fotos pegadas, pies). Antes de tocar un curso:
1. Bajalo: `python pvex.py cmd pve01 "pct pull 115 /var/www/entrenamientos/data/<slug>.json /tmp/<slug>.json"` + `python pvex.py get pve01 /tmp/<slug>.json sync/<slug>-<fecha>.json` + `device_stage_files`. Nombres nuevos, sin pisar los anteriores.
2. Compará con lo último que importaste (`/mnt/user-data/outputs/<slug>-imp-*.json`) campo por campo y respetá lo de Nico. Si su edición choca con un `estructura-extra*.json` (por ejemplo un "conecta"), corregilo también ahí.
3. Todo cambio sale de ese JSON del servidor, nunca de `build.py` solo.

## El pipeline de contenido (`/home/claude/ies-training/tools`)

- `build.py <slug>`: arma el curso desde `claudemy/<slug>/class/` (orden de catálogo en `ORDER`; un curso nuevo necesita entrada en `META` de app.js).
- `agregar-lecciones.py <servidor.json> <construido.json> <salida.json> --lecciones N-M`: suma lecciones nuevas sin pisar lo editado, con ids que no chocan.
- `enriquecer.py <curso.json> <slug> <salida.json> [--solo ids] [--campos ...]`: aplica `ilustraciones/<slug>/manifest*.json`. Campos: `fig` (ilustración principal), `concepts`, `teoria`, `teoria_figs` (figuras o animaciones dentro de la teoría, después del párrafo con `after`), `steps` (figuras del laboratorio, después del paso con `after`; un `.svg` sin `.webp` en `site2` es una animación y va tal cual), `anims` (animaciones del Resumen, bloque "Cómo se ve en la red"), `auto` (script por lección). Los `manifest-anims-*` se leen al final y suman sus pasos. **Nunca `--reemplazar-pasos` sobre un curso editado** (borra las fotos de Nico). Sobre un curso editado, aplicá solo los campos nuevos (`--campos anims,steps,teoria_figs`).
- `estructura.py <curso.json> <slug> <salida.json>`: módulos lineales, objetivos, conecta/sigue/requisitos, avisos; lee `estructura.json` y `estructura-extra*.json` (`modulos_nuevos` con `antes_de`, `lecciones`, `prioridad`); renumera la apertura de "La charla". Los `avisos_sin_texto` de avisos ya aplicados en el servidor son inofensivos.
- `prep-publicar.sh <slug> <servidor.json> [campos] [--estructura]`: enriquecer (+ estructura) y arma en `/mnt/user-data/outputs` `site-<T>.tgz` (código + ilustraciones del curso), `<slug>-imp-<T>.json`, `glosario-<T>.json` y `pub-<slug>-<T>.sh` (verifica el md5 del curso en el servidor antes de importar).
- Glosario: `glosario_check.py <slug>` para ver siglas sin entrada y `glosario_merge.py <propuesta.json>` para sumar sin duplicar.
- `sin_numero_leccion.py <slug> <curso.json> [--aplicar]`: quita "LECCIÓN N" de los rótulos de ilustraciones y animaciones y pasa las referencias "(lección N)" al número actual. Las ilustraciones nuevas van **sin número de lección en el rótulo** (el n cambia cuando se suman lecciones); si nombran otra lección, por su título.
- Ilustraciones: `ilus.py` + scripts en `ilustraciones/<slug>/src/`, render con `render_svg.py` (webp en `site2/ilustraciones/<slug>/`). Guía: `ilustraciones/GUIA.md`. Algunas lecciones tienen un script "b" que reemplaza al original (por ejemplo `11b.py` en MikroTik): editá el que genera la versión publicada.
- Animaciones: `anim.py` (SVG con CSS, sin scripts, fuentes embebidas desde `tools/fonts/`, cuadro fijo con "reducir movimiento"), revisión con `anim_preview.py` (fija cada instante por CSS en una página nueva; mirar 5 o más instantes y el cuadro fijo). No modificar ninguno de los dos desde un encargo.

## Publicar
1. Paquete y JSON a la PC con nombre nuevo, hash verificado.
2. Sitio: `deploy-site.sh` copiado a `deploy-now.sh` con el SHA y `DATOS="0"` (nunca se despliega `data/`), `python pvex.py put pve01 site-<T>.tgz /tmp/ies-entrenamientos-site.tgz` y `python pvex.py run pve01 deploy-now.sh`. Prueba `/`, catalog, auth (200) y lib/config (403).
3. Curso: `put` de `<slug>-imp-<T>.json` a `/tmp/<slug>.json`, de `importar-curso.php` a `/tmp/` y del glosario a `/tmp/glosario.json`; después `python pvex.py run pve01 pub-<slug>-<T>.sh` (corta si el curso cambió en el servidor desde que lo bajaste).
4. Si cambió JS o CSS, subí `?v=N` en `index.html`.

## El sitio (site2)
- SPA `index.html` + `assets/app.js` + `assets/styles.css`; API PHP en `api/` (`admin.php`, `auth.php`, `progress.php`, `capturas.php`, `course.php`, `gate.php`, `lib.php`).
- **`admin.php` normaliza cada curso al guardar desde el panel: un campo nuevo de lección que no esté en `normalize_course` se pierde la primera vez que Nico guarda.** Al sumar un campo (como `anims`), agregalo ahí.
- Lección: `{id, n, handle, summary, idea[], idea_md[], idea_pics[], impact(_md), who(_md), lab{energy, minutes, md, html}, rule, quiz[], sources[], script[], fig, concepts[{name, para_que, como, ejemplo, pics}], objetivos, conecta, sigue, requisitos, theory_md, theory, anims[], auto}`. `id` es estable; `n` es la posición.
- Editor de lección (`#/curso/<slug>/<n>/editar`): fotos, GIF y videos en cualquier punto (ideas, conceptos, pasos del laboratorio, párrafos de la teoría, ilustración principal) pegando con Ctrl+V, arrastrando, con los botones de cada punto o con clic derecho (menú propio; Shift + clic derecho abre el del navegador). El armador de GIF se abre desde cualquier punto. Las fotos se muestran centradas, del ancho del texto y en el mismo marco 16:9 que las ilustraciones (`figurize`).
- Prueba local antes de publicar: copia de `site2` en el scratchpad, `php -S 127.0.0.1:87xx`, usuario admin de prueba creado con `crear-admin.php`, Playwright (login por la interfaz, la función tocada, capturas de pantalla mirándolas, consola sin errores).

## Contenido: criterios de Nico
- Técnico, práctico, de obra y soporte en Uruguay (Antel, UTE, normativa local). Nada inventado: lo que no se confirma se dice en la lección ("medilo", "según lo que entregue Antel") y va a Pendientes del doc.
- Cada lección: idea en tres líneas, impacto, quién lo dice, laboratorio con comandos o menús exactos, regla, quiz de 3 con explicación, fuentes leídas, conceptos con ejemplo, teoría con "Un poco de historia" y "Cómo funciona".
- **Animaciones:** la teoría lleva ilustraciones y animaciones. En los cursos de redes e infraestructura (MikroTik, Grandstream, UniFi, Omada, Proxmox, Linux) cada lección lleva además una animación en el Resumen ("Cómo se ve en la red": el caso de obra) y 1 o 2 en los pasos del laboratorio donde hay intercambio de protocolo. Brief de referencia: `brief-anims-cursos.md`.
- Confidencialidad (el portal tiene registro abierto): sin nombres de clientes, IPs internas de IES, números de teléfono, matrículas ni usuarios reales. Las capturas reales se editan con PIL antes de publicar (ejemplo: `ilustraciones/akuvox/src/45_captura.py`). Rangos 192.0.2.x, 198.51.100.x, 203.0.113.x y 192.168.88.x.
- Lecciones nuevas en cursos grandes: un agente en segundo plano por tramo, con un brief escrito (ejemplos: `brief-omniaccess.md`, `brief-grandstream-fxo.md`, `brief-grandstream-sip-antel.md`) y la prueba de armado al final; el despliegue lo hace la sesión principal.

## Repo academy
`bash /home/claude/trainer-tools/sync.sh` (o `deploy/sync-repo.sh` del repo) rearma `/home/claude/trainer` desde las carpetas de trabajo y deja como `site/data` la última versión importada de cada curso. Después commit, `git bundle create /mnt/user-data/outputs/trainer-inc-<HHMM>.bundle <último>..HEAD`, `device_commit_files` a la PC y en PowerShell `cd C:\Users\usuario\Claude\trainer; git pull --ff-only <bundle> HEAD; git push origin HEAD`. El chequeo de secretos de `sync.sh` marca claves de ejemplo de los laboratorios: revisalas y seguí si son de ejemplo.

## Credenciales y seguridad
- No escribas contraseñas, tokens ni la clave de editor en archivos, docs, memoria ni en la línea de comando. `pvex.py` del repo lee la clave del entorno (`IES_PVE_PASSWORD`).
- No inicies sesión con credenciales de Nico ni de equipos de clientes: si hace falta entrar a una web (por ejemplo la de un portero), abrí una ventana visible y que Nico escriba el login.
- Todo HTML guardado pasa por `clean_html` (sin script, sin on*, iframes solo de youtube-nocookie y player.vimeo).

## Cerrar
1. Actualizá `claude/entrenamientos-despliegue.md` (cursos, funciones, commits, pendientes).
2. Sincronizá el repo academy.
3. Contale a Nico en español qué quedó publicado, qué no se pudo confirmar y qué queda de su lado (datos de obra, pruebas en banco), y que recargue si cambió el diseño.
