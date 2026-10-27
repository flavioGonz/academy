---
name: ies-entrenamientos
description: Mantener y ampliar el portal de cursos técnicos de IES en https://entrenamientos.ies.com.uy (IES Training) — crear un curso nuevo, sumar lecciones o secciones (partes) a un curso existente, corregir contenido, cambiar el diseño o funciones del portal, administrar usuarios y desplegar en el CT 115 de Proxmox. USAR SIEMPRE que se hable del portal de entrenamientos, IES Training, "los cursos", "la academia", agregar un curso/lección/capítulo/sección/módulo (MikroTik, Grandstream, UniFi, Omada, Akuvox, HikCentral, Paradox, Bosch Incendio, Proxmox, VMware, Windows, Linux u otro fabricante), el panel de administración de cursos, capturas, logos de cursos, o desplegar/actualizar entrenamientos.ies.com.uy — aunque no se nombre el portal explícitamente.
---

# IES Training · entrenamientos.ies.com.uy

Portal de cursos técnicos para los instaladores y el soporte de IES (Ingeniería en Seguridad S.R.L., Uruguay). Español rioplatense con voseo, sin audio (Nico no lo quiere), estilo visual IES (azules #002F58 / #011E38 / #0A63B8 / #17A8D4, fondo #F3F7FB, Familjen Grotesk + Instrument Sans + JetBrains Mono, "forma IES") con estructura tipo Udemy/Coursera.

La documentación viva de infraestructura está en el doc del proyecto **Entrenamientos**: `claude/entrenamientos-despliegue.md`. Leelo al empezar y actualizalo al terminar cualquier cambio de infraestructura, cursos o funciones.

## Dónde vive cada cosa

| Qué | Dónde |
|---|---|
| Sitio en producción | CT **115** `entrenamientos` en **pve01**, IP 172.26.20.218, nginx + php8.4-fpm. Web `/var/www/entrenamientos` (cursos en `data/*.json`, capturas en `capturas/`, logos en `logos/`) |
| Datos privados | `/var/www/entrenamientos-data/` en el CT: SQLite `ies-training.sqlite` (usuarios, progreso, auditoría), `sesiones/`, `historial/<curso>/` (últimas 60 versiones) |
| Respaldos | `/root/respaldos/` en el CT, uno por despliegue (web y datos) |
| Proxy | NPM 172.26.20.17:81, proxy host **11** → 172.26.20.218:80, cert Let's Encrypt id 12, `client_max_body_size 70m` en advanced |
| DNS | A `entrenamientos` → 200.40.182.246 en la zona ies.com.uy (skill ies-cpanel) |
| Herramientas de despliegue | PC de Nico, `C:\Users\usuario\Claude\ies-training\`: `pvex.py` (SSH a pve0X: `run`, `cmd`, `put`), `npmx.py` (API del NPM), `deploy-site.sh` y `importar.sh` (plantillas), `limites.sh`, `npm-limite.py`, `importar-curso.php`, `crear-admin.php`, `admin-user.sh` |
| Kit de fuentes | `C:\Users\usuario\Claude\ies-training\kit\ies-entrenamientos-kit.tgz` (copia también en el CT: `/root/kit/`). Trae `ies-training/site2` (código del sitio), `ies-training/tools`, `ies-training/brief-ies.md` y los workspaces `claudemy/<slug>/` de cada curso |

La PC de Nico se alcanza con las herramientas del puente (Desktop Commander `start_process` en PowerShell, `device_commit_files`, `device_stage_files`). El CT se opera siempre desde ahí con `python pvex.py ...` (el contenedor de la nube no llega a la red 172.26.20.x).

**Fuente de verdad de los cursos: el servidor.** Desde que existe el panel, los cursos se editan en producción. Nunca despliegues `data/` encima (`DATOS=0` siempre, salvo un sitio vacío) y antes de tocar un curso existente bajá su JSON actual.

## Primer paso en una sesión nueva: restaurar el kit

El contenedor de la nube es efímero. Si `/home/claude/ies-training/site2` no existe:

1. `device_stage_files` del kit (`C:\Users\usuario\Claude\ies-training\kit\ies-entrenamientos-kit.tgz`) y `tar xzf` en `/home/claude/`.
2. Si hace falta la skill claudemy (cursos o lecciones nuevas): ya suele estar en `/root/.claude/skills/claudemy/`; si no, clonar `https://github.com/assafkip/claudemy` ahí.
3. `pip install --break-system-packages markdown` si falta; `pandoc` tiene que existir (`apt-get install -y pandoc` si no).
4. Para trabajar sobre lo que hay hoy en producción, bajá los JSON vigentes desde la PC: `curl.exe -s -o <slug>.json https://entrenamientos.ies.com.uy/data/<slug>.json` (y `catalog.json`), luego `device_stage_files`.

Al terminar una sesión con cambios, regenerá el kit (ver "Cerrar") para que la próxima vez arranque de lo último.

## Arquitectura del sitio (site2)

- `index.html` + `assets/app.js` (SPA con rutas por hash) + `assets/styles.css`. Subí `?v=N` en `index.html` en cada cambio de JS/CSS para romper la caché.
- Rutas: `#/` inicio, `#/curso/<slug>`, `#/curso/<slug>/<n>` lección (pestañas resumen, laboratorio, quiz, charla, fuentes), `#/aprendizaje`, `#/buscar/<q>`, `#/constancia/<slug>`, `#/ingresar`, `#/registro`, `#/cuenta`, `#/admin` (resumen, usuarios, cursos, actividad), `#/admin/cursos/<slug>`, `#/admin/cursos/<slug>/<id>`, `#/editor`.
- `META` en app.js da a cada slug su ícono (`glyph`) y categoría (`cat`); `PATHS` arma los recorridos de la portada. **Un curso nuevo necesita su entrada en `META`** (y en un `PATHS` si corresponde) y su slug en `ORDER` de `tools/build.py`.
- API PHP (todas leen `api/lib.php`, bloqueado por nginx junto con `config.php`): `auth.php` (me, register, login, logout, password, profile), `progress.php`, `admin.php` (users, stats, user, course, history, audit; course_save con control de conflicto por `base`, course_new, catalog_order, restore, user_update/reset/create, `logo`), `capturas.php` (imagen 12 MB, GIF 30 MB, video mp4/webm 60 MB, YouTube/Vimeo; `inline=1` para medios insertados en el texto).
- Escrituras: POST con encabezado `X-IES: 1` y sesión. Roles: tecnico, editor, admin. El registro siempre crea técnicos; un admin se crea por consola (`admin-user.sh`).
- Lección = `{id, n, handle, summary, idea[], idea_md[], impact(_md), who(_md), lab{energy, minutes, md, html}, rule, quiz[], sources[], script[]}`. `id` es estable (las capturas cuelgan del id), `n` es la posición y se renumera. Partes = `arcs[{title, why, lessons:[ids]}]`.
- Panel de administración (`#/admin`, barra lateral azul): **Resumen** con indicadores, gráfico de 30 días (lecciones, activos, registros, laboratorios), tabla de cursos (empezaron, terminaron, avance medio, % de aciertos en quiz, medios, pendientes), ranking de técnicos, cuentas por empresa, preguntas que más se fallan y actividad reciente; **Usuarios** con filtros por rol, búsqueda, orden y exportación CSV; ficha de usuario con anillos de avance por curso y lecciones completadas con fecha; **Cursos** en tarjetas con salud del contenido (qué le falta a cada lección); **Actividad** agrupada por día. Endpoints: `admin.php?a=dashboard` y `?a=courses`. `progress.php` guarda `t` (lección completada) y `tl` (laboratorio) con hora del servidor desde el 27/10/2026.
- El editor de cursos ya permite: arrastrar lecciones entre partes, logo por curso, editor Markdown con vista previa, insertar imagen/GIF/video/YouTube en el laboratorio, quiz, fuentes, historial y restaurar, borrador, orden del catálogo.

## Tareas típicas

### A. Curso nuevo
1. Slug en minúsculas con guiones (ej. `bosch-incendio`). Workspace `/home/claude/claudemy/<slug>/`.
2. Producirlo con el método claudemy adaptado: leé `ies-training/brief-ies.md` (manda sobre la skill claudemy). Para cursos grandes, lanzá un agente en segundo plano por curso con el brief, el slug, el alcance (lecciones y partes) y las fuentes prioritarias; que no rendericen audio.
3. Checker: `python3 ies-training/tools/check_lessons_es.py claudemy/<slug>` hasta que pase. Revisá a mano 2 o 3 tarjetas (comandos, rutas de menú, versiones, urls que existan en `raw/`).
4. `ORDER` en `tools/build.py`, entrada en `META` (y `PATHS`) en app.js. Si el ícono no existe, agregalo al objeto de íconos (SVG de trazo, 24×24).
5. `python3 ies-training/tools/build.py <slug>` → `site2/data/<slug>.json`.
6. Si cambió app.js: probar local, empaquetar y desplegar (D). Después importar el curso (E).

### B. Sumar lecciones o una sección a un curso existente
1. Bajá el JSON vigente del servidor (paso 4 de restaurar) → `<slug>-servidor.json`.
2. Escribí las lecciones nuevas en `claudemy/<slug>/class/` con números que sigan a los existentes, con el mismo brief y checker; agregá la parte nueva en `class/course.json` (`arcs`) y en `lesson-plan.md`. Investigá con fuentes reales (documentación oficial primero) y sumalas a `sources.json` + scraper.
3. `python3 ies-training/tools/build.py <slug>` y después
   `python3 ies-training/tools/agregar-lecciones.py <slug>-servidor.json site2/data/<slug>.json <slug>-nuevo.json --lecciones 13-20 [--parte "Título" --por-que "..."]`.
   Conserva todo lo editado en el panel, da ids que no chocan y renumera. `--reemplazar` para actualizar lecciones existentes por título.
4. Importar `<slug>-nuevo.json` con `--forzar` (E). El anterior queda en el historial y se puede restaurar desde el panel.

### C. Corregir una lección puntual
Lo más simple es el panel (`#/admin/cursos/<slug>/<id>`), que guarda historial. Si lo hacés vos por API o importación, igual bajá primero el JSON vigente.

### D. Cambiar el sitio (JS, CSS, PHP) y desplegar
1. Editar en `/home/claude/ies-training/site2/`. Chequeos: `node -e "new Function(require('fs').readFileSync('assets/app.js','utf8'))"` y `php -l` de cada PHP.
2. Prueba local aislada: copiar `site2` a una carpeta del scratchpad, crear un admin con `crear-admin.php` (cambiando la ruta del `require`), `php -S 127.0.0.1:87xx` y recorrer con Playwright (login, la función tocada, vista móvil 390 px sin desborde horizontal, consola sin errores). Mirá capturas de pantalla, no solo el DOM.
3. Paquete: `cd site2 && tar czf /mnt/user-data/outputs/ies-entrenamientos-site.tgz --exclude=./capturas --exclude=./logos --exclude='*.htaccess' .` y `sha256sum`.
4. `device_commit_files` a `C:\Users\usuario\Claude\ies-training\ies-entrenamientos-site.tgz`. **Ojo:** si volvés a enviar la misma ruta de `/mnt/user-data/outputs/` en la misma sesión, el puente puede escribir la copia anterior; copiá el paquete con un nombre nuevo (ej. `site-<fecha-hora>.tgz`) antes de cada envío y verificá el hash en la PC con `Get-FileHash`. Después, en PowerShell:
   ```powershell
   cd C:\Users\usuario\Claude\ies-training
   (Get-Content deploy-site.sh -Raw).Replace('__SHA__','<sha256>').Replace('__DATOS__','0') | Set-Content -NoNewline -Encoding ascii deploy-now.sh
   python pvex.py put pve01 ies-entrenamientos-site.tgz /tmp/ies-entrenamientos-site.tgz
   python pvex.py run pve01 deploy-now.sh
   ```
   El script verifica el sha, respalda web y datos, extrae sin `data/`, ajusta permisos, recarga nginx y prueba `/`, `/data/catalog.json`, `/api/auth.php?a=me` (200) y `/api/lib.php`, `/api/config.php` (403).
5. Verificá desde la PC con `curl.exe` contra https://entrenamientos.ies.com.uy (el `?v=` nuevo en el HTML). Si tocaste la API del panel, `python pvex.py run pve01 smoke-admin.sh` crea una sesión temporal del primer admin dentro del CT, consulta `dashboard`, `courses`, `users` y `audit` (con `wget`: el CT no tiene curl) y la borra.

### E. Importar un curso al servidor
`build.py` (o `agregar-lecciones.py`) genera el JSON; para subirlo sin tocar los demás cursos, con `importar.sh` (plantilla en la carpeta de la PC):
```powershell
cd C:\Users\usuario\Claude\ies-training
python pvex.py put pve01 <slug>.json /tmp/<slug>.json
python pvex.py put pve01 importar-curso.php /tmp/importar-curso.php
(Get-Content importar.sh -Raw).Replace('__SLUG__','<slug>').Replace('__FORZAR__','') | Set-Content -NoNewline -Encoding ascii importar-now.sh
python pvex.py run pve01 importar-now.sh
```
`importar-curso.php` corre como www-data dentro del CT, se niega si el curso ya tiene historial de ediciones del panel (poné `--forzar` en `__FORZAR__` cuando el JSON salió de `agregar-lecciones.py` o revisaste que no se pierde nada), guarda la versión anterior en `historial/`, conserva el logo y actualiza `catalog.json` (un slug nuevo va al final del orden; el orden se cambia desde el panel). Los archivos se empujan con `--perms 0644` a `/tmp` del CT para que www-data los lea.

### F. Usuarios
Desde el panel. Por consola: `admin-user.sh` (corre `crear-admin.php "Nombre" correo` como www-data; imprime una contraseña temporal que obliga a cambiarla). Las contraseñas temporales se dan una sola vez en el chat y no se guardan en ningún archivo ni memoria.

## Contenido: criterios que Nico ya pidió
- Técnico, práctico, orientado a obra y soporte en Uruguay (Antel, UTE, normativa local cuando aplique). Nivel inicial a intermedio salvo que se pida otro.
- Cada lección: idea en tres líneas, impacto, quién lo dice (acuerdo entre fuentes), laboratorio con comandos o rutas de menú exactos, regla para quedarse, quiz de 3 con explicación, fuentes reales leídas. Versión de firmware/software cuando importe, la vigente a la fecha.
- Nada inventado: si un dato no se pudo confirmar (ej. VLAN de Antel), la lección lo dice y queda en "Pendientes" del doc del proyecto.
- Sin audio. Las capturas, GIF y videos los suben los técnicos desde el panel.

## Credenciales y seguridad
- No escribas contraseñas, tokens ni la clave de editor en archivos, docs, memoria ni en la línea de comando. `pvex.py` y `npmx.py` toman las credenciales por defecto documentadas en las skills ies-proxmox e ies-nginx-proxy (o variables de entorno). Para DNS usá un token de API de cPanel que Nico genere y revoque después (skill ies-cpanel).
- La clave de editor existe solo como hash bcrypt en `api/config.php`; para cambiarla, generá una nueva, poné el hash y dásela a Nico en el chat.
- Cualquier HTML guardado pasa por `clean_html` (sin script, sin on*, iframes solo de youtube-nocookie y player.vimeo).

## Cerrar
1. Actualizá `claude/entrenamientos-despliegue.md` en el proyecto (cursos y lecciones, funciones nuevas, pendientes).
2. Regenerá el kit y dejalo en la PC (y en el CT):
   ```bash
   cd /home/claude && tar czf /mnt/user-data/outputs/ies-entrenamientos-kit.tgz \
     --exclude=ies-training/site2/capturas --exclude=ies-training/site2/logos \
     ies-training/site2 ies-training/tools ies-training/brief-ies.md claudemy
   ```
   `device_commit_files` a `C:\Users\usuario\Claude\ies-training\kit\ies-entrenamientos-kit.tgz`; opcional `python pvex.py put pve01 kit\ies-entrenamientos-kit.tgz /tmp/kit.tgz` + `pct push 115 /tmp/kit.tgz /root/kit/ies-entrenamientos-kit.tgz`.
3. Contale a Nico qué cambió, qué quedó pendiente de su lado (datos de obra a confirmar, pruebas en banco) y que recargue con Ctrl+F5 si cambió el diseño.
