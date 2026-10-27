# Brief común: cursos OmniAccess (LPR, Face, Intrusión, Filas)

Nico (dueño de IES, integrador de seguridad electrónica en Uruguay) pidió cuatro cursos nuevos en el portal IES Training sobre **OmniAccess**, el software de control de acceso desarrollado por **Infratec** (infratec.com.uy) que IES instala en barrios privados, edificios y empresas: **OmniAccess LPR**, **OmniAccess Face**, **OmniAccess Intrusión** y **OmniAccess Filas**.

**Público (decidido por Nico):** técnico y operador. Cada curso tiene un tramo de instalación y configuración (técnico de IES) y un tramo de operación diaria (guardia, portería, puesto de monitoreo, administrador del barrio).

## Fuente de verdad: el código y los manuales del producto
Copia de solo lectura del código vigente (rama de desarrollo más reciente, octubre de 2026) en `/home/claude/omni-src/`. **No modifiques nada ahí.**
- Manuales del producto: `docs/manual/*.md` (operador, administrador, instalador = LPR; face-*, filas-*; tablet = módulo Guardia; guia-rapida) y `docs/manual/00-meta.json`.
- `README.md` (arquitectura, modos, módulos), `INSTALL.md`, `INSTALLER.md`, `HIKVISION_SETUP.md`, `ANALISIS_PROBLEMAS_LPR.md`, `CHANGELOG.md`, `ESTADO_ACTUAL.md`, `docs/help/*`, `openspec/`.
- Código: `src/app/admin/*` (pantallas: monitor-lpr, monitor-face, monitor-intrusion, monitor-queue, filas, flujo-filas, horarios-filas, reportes-queue, notificaciones, devices, calibracion-aforo, settings, vehicles, users, units, credentials, groups, history, mapa…), `src/app/pwa/*`, `src/app/guard*`, `src/app/api/*`, `src/components/*`, `src/lib/*` (incluye `src/lib/intrusion/`), `prisma/schema.prisma` (modelos), `server.js`, `handlers/`, `hikvision-codes.js`, `dahua-events.js`, `lib-intrusion-capture.js`, `dispatch-worker.js`.
- Lo que dice el curso tiene que salir de ahí: nombres exactos de pantallas, menús, botones, campos, estados, modos (`Setting`: MODULE_LPR, MODULE_FACE, MODULE_QUEUE, MODULE_GUARD), eventos y flujos. Si el manual y el código no coinciden, manda el código y anotalo. Si algo depende de la instalación (rama del barrio, Setting), decilo así ("según cómo esté configurado tu sistema").
- Fuentes web complementarias para la teoría y el hardware (fabricantes y estándares): ONVIF (perfiles S/T/M, eventos, analíticas), Hikvision ANPR / ISAPI, Dahua, Bosch IVA Pro, Akuvox (terminales faciales), go2rtc, RTSP RFC 2326/7826, Web Push, Telegram Bot API, MinIO/S3. Guardalas con el scraper en raw/ como en los otros cursos.

## Confidencialidad (el portal tiene registro abierto)
- **Nada de datos reales de clientes ni de infraestructura**: sin nombres de barrios o clientes (no "Los Olivos", "San Nicolás", "Hospital Británico", "Sildan"), sin IPs internas de IES (172.26.x.x), sin dominios de instalaciones, sin usuarios, claves, tokens, matrículas o nombres de residentes reales, sin el repositorio. Ejemplos con datos inventados y rangos de documentación (192.0.2.x, 198.51.100.x, matrículas de ejemplo tipo `SBA 1234`, "Barrio Ejemplo", "Edificio Rambla").
- Detalles internos de implementación (Next.js, PostgreSQL, Redis, pm2) solo en lo que el técnico necesita para instalar y diagnosticar; nada de rutas de archivos con credenciales.

## Método y formato (igual que los otros cursos del portal)
- Brief de formato y tono: `/home/claude/ies-training/brief-ies.md` (script.txt, card.md, quiz.json; español rioplatense con voseo, sin exigencias, sin guiones largos). Método claudemy: `/root/.claude/skills/claudemy/` (leé SKILL.md y lo que corresponda a plan y lecciones; **no generes audio**).
- Workspace propio: `/home/claude/claudemy/omniaccess-<x>/` con `sources.json`, `raw/`, `research/notes/`, `class/course.json`, `class/lesson-plan.md`, `class/NN-tema/{card.md,script.txt,quiz.json}`. Copiá la forma de `course.json` de `/home/claude/claudemy/paradox/class/course.json` (title, vendor = "Infratec", tagline, description, level, audience, prerequisites, outcomes, version_note, arcs con title/why/lessons, splits si hay, sources_count).
- En "Para profundizar" de cada tarjeta citá páginas guardadas en raw/ (el checker lo exige). El manual del producto se nombra en el texto ("Manual del Operador, sección …") sin URL.
- Laboratorio de cada lección: 10 a 25 min, con pasos concretos sobre el sistema (en una instalación de prueba o de demo) o sobre el equipo (cámara, NVR, terminal). Para operación, laboratorios tipo práctica guiada ("abrí Monitor LPR, filtrá por…, investigá esta lectura…").
- Checker: `python3 /home/claude/ies-training/tools/check_lessons_es.py /home/claude/claudemy/omniaccess-<x>` (todas las carpetas).
- Lecciones: 8 a 12 por curso según cuánto haya de verdad en el producto. Arcos sugeridos: **Entender el sistema** (qué resuelve, arquitectura y modos, en lo que hace falta) → **Instalar y configurar** (técnico) → **Operar** (guardia/operador) → **Administrar y diagnosticar** (reglas, notificaciones, reportes, salud de dispositivos, fallas típicas).

## Enriquecimiento (en la misma tarea)
Seguí `/home/claude/ies-training/ilustraciones/GUIA.md` entera (ignorá `script_rsc`: estos cursos no llevan script de terminal): ilustración principal `<id>.svg` y 1 a 3 de pasos por lección en `/home/claude/ies-training/ilustraciones/omniaccess-<x>/`, scripts `src/<id>.py` con `/home/claude/ies-training/tools/ilus.py` (no la modifiques), render con `tools/render_svg.py` y revisión de cada PNG, `manifest.json` (fig, steps con `after`, concepts 2 a 4, teoria_md con `### Un poco de historia` y `### Cómo funciona`). El `<id>` es el número de la lección sin ceros. Las ilustraciones dibujan flujos y pantallas de forma esquemática (cámara → lectura → evento → monitor → alerta), nunca copias de la interfaz con datos.
Y `estructura.json` en la misma carpeta, con la forma de `/home/claude/ies-training/ilustraciones/akuvox/estructura.json` (curso: objetivo, recorrido; modulos: title, why, objetivos, lessons; lecciones: objetivos, conecta, sigue/cierre, requisitos; avisos si hiciera falta).

## Al terminar
1. `python3 /home/claude/ies-training/tools/check_lessons_es.py /home/claude/claudemy/omniaccess-<x>` en ok.
2. Prueba de armado: `python3 /home/claude/ies-training/tools/build.py omniaccess-<x>`, luego `python3 /home/claude/ies-training/tools/enriquecer.py /home/claude/ies-training/site2/data/omniaccess-<x>.json omniaccess-<x> /tmp/claude-0/omni-<x>-e.json` y `python3 /home/claude/ies-training/tools/estructura.py /tmp/claude-0/omni-<x>-e.json omniaccess-<x> /tmp/claude-0/omni-<x>-f.json` (faltan=[], sin_ancla=[], avisos_sin_texto=[]).
3. `python3 /home/claude/ies-training/tools/glosario_check.py omniaccess-<x>`: reportá RFC y siglas faltantes con propuesta de entrada (term, short, long, year, cat). No edites el glosario.
4. No despliegues nada. Reportá: títulos de lecciones, módulos, fuentes, archivos y lo que no pudiste confirmar (diferencias entre manual y código, funciones que dependen de la instalación).
