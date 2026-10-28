<p align="center">
  <img src="docs/readme/banner.svg" alt="IES Training: lo que hay que saber antes de llegar a la obra. 16 cursos, 251 lecciones, más de 280 animaciones y 860 términos de glosario." width="100%">
</p>

<p align="center">
  <a href="https://entrenamientos.ies.com.uy"><img alt="Portal en línea" src="https://img.shields.io/badge/portal-entrenamientos.ies.com.uy-0A63B8?style=for-the-badge"></a>
  <img alt="16 cursos" src="https://img.shields.io/badge/cursos-16-04223D?style=for-the-badge">
  <img alt="251 lecciones" src="https://img.shields.io/badge/lecciones-251-04223D?style=for-the-badge">
  <img alt="Más de 280 animaciones" src="https://img.shields.io/badge/animaciones-280%2B-17A8D4?style=for-the-badge">
  <img alt="864 términos de glosario" src="https://img.shields.io/badge/glosario-864%20términos-17A8D4?style=for-the-badge">
</p>

<p align="center">
  <img alt="PHP 8.4" src="https://img.shields.io/badge/PHP-8.4-777BB4?logo=php&logoColor=white">
  <img alt="SQLite" src="https://img.shields.io/badge/SQLite-WAL-003B57?logo=sqlite&logoColor=white">
  <img alt="JavaScript sin frameworks" src="https://img.shields.io/badge/JavaScript-sin%20frameworks-F7DF1E?logo=javascript&logoColor=black">
  <img alt="nginx" src="https://img.shields.io/badge/nginx-auth__request-009639?logo=nginx&logoColor=white">
  <img alt="Proxmox LXC" src="https://img.shields.io/badge/Proxmox-LXC-E57000?logo=proxmox&logoColor=white">
  <img alt="Python" src="https://img.shields.io/badge/herramientas-Python%203-3776AB?logo=python&logoColor=white">
</p>

# IES Training · academia técnica de IES

**IES Training** es la academia de formación técnica de **IES – Ingeniería en Seguridad** (Uruguay). Forma técnicos de redes, telefonía IP, seguridad electrónica y servidores con cursos cortos y prácticos. Cada lección tiene:

- una **idea en tres líneas**;
- la **teoría** (historia y cómo funciona) con **animaciones**;
- un **laboratorio** con los comandos exactos;
- un **examen** con casos de obra;
- donde hay terminal, un **script listo para pegar**.

Este repositorio tiene todo lo que hace funcionar la academia:

- **El portal:** front sin frameworks y API PHP con SQLite.
- **Los 16 cursos:** investigación, guion, tarjetas y exámenes.
- **El enriquecimiento:** más de 770 ilustraciones y más de 280 animaciones de teoría.
- **Las herramientas** que construyen, enriquecen y publican cada curso.
- **Los scripts de despliegue** en Proxmox detrás de Nginx Proxy Manager.

> **En línea:** <https://entrenamientos.ies.com.uy>. Sin cuenta se ven los títulos y el recorrido; registrándose (gratis) se ve todo y se rinden los exámenes.

---

## Índice

1. [Recorrido en imágenes](#recorrido-en-imágenes)
2. [Los cursos](#los-cursos)
3. [Anatomía de una lección](#anatomía-de-una-lección)
4. [Teoría animada](#teoría-animada)
5. [Ilustraciones de paso](#ilustraciones-de-paso)
6. [Editor y administración](#editor-y-administración)
7. [Arquitectura](#arquitectura)
8. [Cómo se construye un curso](#cómo-se-construye-un-curso)
9. [Cómo se publica](#cómo-se-publica)
10. [Estructura del repositorio](#estructura-del-repositorio)
11. [Herramientas](#herramientas)
12. [Probarlo en tu máquina](#probarlo-en-tu-máquina)
13. [Criterios de contenido](#criterios-de-contenido)
14. [Créditos](#créditos)

---

## Recorrido en imágenes

<table>
  <tr>
    <td width="50%"><img src="docs/readme/portal-inicio.webp" alt="Portada del portal con el buscador, los temas frecuentes y el contador de cursos, lecciones y horas de laboratorio"><br><sub><b>Portada.</b> Buscador por tema, equipo o protocolo, y lo que te falta para seguir.</sub></td>
    <td width="50%"><img src="docs/readme/curso.webp" alt="Página del curso MikroTik con módulos, objetivos y lecciones"><br><sub><b>Curso.</b> Objetivo, recorrido y módulos en orden: cada lección se abre al completar la anterior.</sub></td>
  </tr>
  <tr>
    <td><img src="docs/readme/leccion-resumen.webp" alt="Lección de Akuvox con la ilustración principal y el índice del curso a la derecha"><br><sub><b>Lección.</b> Ilustración principal, ideas, de dónde venimos y qué sigue.</sub></td>
    <td><img src="docs/readme/teoria-animada.webp" alt="Pestaña Teoría con la animación de RIB y FIB en la lección de rutas estáticas"><br><sub><b>Teoría animada.</b> La animación va después del párrafo que explica (acá, RIB y FIB en MikroTik).</sub></td>
  </tr>
  <tr>
    <td><img src="docs/readme/laboratorio.webp" alt="Laboratorio con pasos numerados, comandos y una ilustración del paso"><br><sub><b>Laboratorio.</b> Pasos numerados con comandos exactos y la figura justo después del paso que ilustra.</sub></td>
    <td><img src="docs/readme/script.webp" alt="Recuadro de script con variables editables y el código de RouterOS listo para copiar"><br><sub><b>Script para automatizar.</b> Completás tus datos, se reemplazan en el código y lo copiás o descargás (<code>.rsc</code>, <code>.sh</code> o <code>.ps1</code>).</sub></td>
  </tr>
  <tr>
    <td><img src="docs/readme/glosario-tooltip.webp" alt="Tooltip del glosario sobre la palabra OSPF dentro de la teoría"><br><sub><b>Glosario en contexto.</b> Cada término técnico y cada RFC explica qué es y para qué se creó, sin salir de la lección.</sub></td>
    <td><img src="docs/readme/conceptos.webp" alt="Tarjetas de conceptos con para qué se creó, cómo se usa y un ejemplo"><br><sub><b>Conceptos.</b> Para qué se creó, cómo se usa y un ejemplo de obra.</sub></td>
  </tr>
  <tr>
    <td><img src="docs/readme/admin.webp" alt="Panel de administración con indicadores, gráfico de 30 días y tabla de cursos"><br><sub><b>Administración.</b> Técnicos activos, lecciones completadas, cursos, preguntas que más se fallan y actividad.</sub></td>
    <td><img src="docs/readme/editor-ilustracion.webp" alt="Editor de lección con la ilustración principal seleccionada y los botones Pegar, Subir y Quitar"><br><sub><b>Edición en el lugar.</b> Se pega una captura con Ctrl+V y se guarda sola.</sub></td>
  </tr>
  <tr>
    <td><img src="docs/readme/glosario.webp" alt="Página del glosario con buscador y categorías"><br><sub><b>Glosario.</b> 864 términos, 76 RFC con número, año y qué resolvieron.</sub></td>
    <td><img src="docs/readme/celular.webp" alt="Dos capturas de celular: una lección de Paradox y su teoría animada"><br><sub><b>En el celular.</b> El técnico lo usa en la obra.</sub></td>
  </tr>
</table>

---

## Los cursos

| | Curso | Lecciones | Módulos | Script | Qué se aprende |
|---|---|:-:|:-:|:-:|---|
| 🛜 | **MikroTik RouterOS para integradores** | 39 | 9 | `.rsc` | Entrar sin perder el acceso, VLAN, firewall input/forward y zonas, dos WAN (PPPoE, DHCP, IP fija), túneles WireGuard, L2TP e IPsec, DNS, Netwatch, Safe Mode |
| ☎️ | **Grandstream UCM** | 12 | 4 | | Central cerrada, extensiones, troncal, rutas, IVR, colas, NAT y portero SIP |
| 📶 | **UniFi** | 12 | 4 | | Adopción, VLAN y zonas, WiFi bien hecho, roaming, sitios y backups |
| 📡 | **Omada** | 12 | 4 | | Controlador, option 138, ACL, portal cautivo, mesh, VPN entre sedes |
| 🚪 | **Porteros IP Akuvox** | 42 | 9 | | SIP y DTMF, relés y cerraduras, apertura por HTTP, catálogo por modelo, licencias |
| 🎥 | **HikCentral Professional** | 12 | 4 | | Servidor, licencias, ISUP, grabación, alarmas, roles y control de acceso |
| 🚗 | **OmniAccess LPR** <sup>borrador</sup> | 12 | 4 | | Lectura de matrículas: cámara, calibración, monitor, merodeo, lista de vigilancia |
| 🙂 | **OmniAccess Face** <sup>borrador</sup> | 10 | 4 | | Reconocimiento facial, sincronización con terminales, enrolamiento y privacidad |
| 🚨 | **OmniAccess Intrusión** <sup>borrador</sup> | 10 | 4 | | Analítica de cámara, horario de armado, atender una alarma, falsas alarmas |
| 👥 | **OmniAccess Filas** <sup>borrador</sup> | 10 | 3 | | Conteo por ONVIF, aforo, tiempo de espera (ley de Little), alertas y reportes |
| 🔔 | **Alarmas Paradox** | 16 | 4 | | Bus, zonas con EOL, programación, BabyWare, Contact ID, MQTT, diagnóstico |
| 🔥 | **Bosch Incendio** | 16 | 4 | | Lazo LSN, aisladores, cálculos, programación con FSP-5000-RPS, red y mantenimiento |
| 🖥️ | **Proxmox VE** | 12 | 4 | `.sh` | KVM y LXC, almacenamiento, bridges VLAN, backups con PBS, clúster, HA |
| 🧊 | **VMware vSphere** | 12 | 4 | `.sh` | ESXi, vSwitch, datastores, snapshots, vMotion y HA, licencias |
| 🪟 | **Windows para técnicos** | 12 | 3 | `.ps1` | Red y SMB, firewall, RDP con NLA, servicios, UPS, eventos, BitLocker |
| 🐧 | **Linux para técnicos** | 12 | 4 | `.sh` | Archivos y permisos, systemd, procesos, red, SSH con llaves, firewall, mantenimiento |

Hay 68 horas de laboratorio en total. Los OmniAccess (software de [Infratec](https://infratec.com.uy)) se escribieron a partir del producto y están en borrador en el portal hasta su revisión.

---

## Anatomía de una lección

```mermaid
flowchart LR
    A["🧭 Ruta<br/><sub>de dónde venimos · objetivos · qué sigue</sub>"] --> B["📌 Resumen<br/><sub>ilustración principal · idea en 3 líneas · quién lo dice</sub>"]
    B --> C["📖 Teoría<br/><sub>un poco de historia · cómo funciona · conceptos · animaciones</sub>"]
    C --> D["🧪 Laboratorio<br/><sub>pasos con comandos · figuras por paso · fotos de obra</sub>"]
    D --> E["⌨️ Script<br/><sub>variables · copiar · descargar</sub>"]
    D --> F["✅ Examen<br/><sub>3 casos de obra</sub>"]
    F --> G["🔓 Siguiente lección"]
    style C fill:#E3F5EC,stroke:#0E8F5E
    style E fill:#EEF3F8,stroke:#0A63B8
```

Las pestañas de cada lección son: **Resumen · Teoría · Laboratorio · Examen · La charla · Fuentes**. Las palabras técnicas y las RFC muestran un tooltip del glosario. Cada lección y cada curso se pueden bajar en **PDF**.

---

## Teoría animada

Cada lección tiene en su teoría al menos una animación del mecanismo que explica. Son SVG animados con CSS: sin JavaScript, con las fuentes de la marca embebidas, en loop, con leyenda numerada y un **cuadro fijo** para quien tiene "reducir movimiento" activado. Pesan alrededor de 50 KB cada una.

<table>
  <tr>
    <td width="50%"><img src="docs/readme/anim/mikrotik-rib-fib.svg" alt="Animación: las rutas entran a la RIB, gana la de menor distancia, la FIB busca la máscara más larga, cae el ISP A y vuelve"><br><sub><b>MikroTik · RIB y FIB.</b> Todas las rutas y las que se usan; qué pasa cuando cae un proveedor.</sub></td>
    <td width="50%"><img src="docs/readme/anim/akuvox-sip.svg" alt="Animación de una llamada SIP directa del portero al monitor y la apertura por DTMF"><br><sub><b>Akuvox · SIP directo.</b> INVITE, 180, 200 OK, ACK, audio RTP y el DTMF que abre el relé.</sub></td>
  </tr>
  <tr>
    <td><img src="docs/readme/anim/paradox-eol.svg" alt="Animación de una zona con resistencia de fin de línea: normal, abierta, en corto y sin EOL"><br><sub><b>Paradox · zona con EOL.</b> Lo que mide la central en cada estado del lazo.</sub></td>
    <td><img src="docs/readme/anim/bosch-aislador.svg" alt="Animación de un lazo LSN alimentado por ambos extremos que aísla un cortocircuito"><br><sub><b>Bosch · aisladores.</b> El lazo sigue funcionando con un corto entre dos aisladores.</sub></td>
  </tr>
  <tr>
    <td><img src="docs/readme/anim/proxmox-quorum.svg" alt="Animación del clúster Proxmox con corosync y quórum"><br><sub><b>Proxmox · quórum.</b> Votos, mayoría y por qué un nodo solo no decide.</sub></td>
    <td><img src="docs/readme/anim/filas-little.svg" alt="Animación de la ley de Little para estimar el tiempo de espera de una fila"><br><sub><b>OmniAccess Filas · ley de Little.</b> Cómo se estima la espera a partir del aforo y las salidas.</sub></td>
  </tr>
</table>

---

## Ilustraciones de paso

Más de 770 ilustraciones dibujan lo que el técnico tiene que hacer o ver: qué cable va a qué borne, qué menú abrir o qué le pasa al paquete. No son decoración: cada figura sale de la tarjeta de la lección, con los mismos puertos, menús y valores de ejemplo.

<table>
  <tr>
    <td width="33%"><img src="docs/readme/ilus-mikrotik.webp" alt="MikroTik: input y forward"><br><sub>MikroTik · ¿va al router o pasa por el router?</sub></td>
    <td width="33%"><img src="docs/readme/ilus-akuvox.webp" alt="Akuvox: ilustración de relés"><br><sub>Akuvox · relés y cerraduras</sub></td>
    <td width="33%"><img src="docs/readme/ilus-paradox.webp" alt="Paradox: cableado de zona"><br><sub>Paradox · cableado de zona</sub></td>
  </tr>
  <tr>
    <td><img src="docs/readme/ilus-bosch.webp" alt="Bosch Incendio: lazo"><br><sub>Bosch · lazo y aisladores</sub></td>
    <td><img src="docs/readme/ilus-unifi.webp" alt="UniFi: roaming"><br><sub>UniFi · roaming</sub></td>
    <td><img src="docs/readme/ilus-omniaccess.webp" alt="OmniAccess LPR: recorrido de una lectura"><br><sub>OmniAccess LPR · recorrido de una lectura</sub></td>
  </tr>
</table>

---

## Editor y administración

<table>
  <tr><td>

**Para el alumno**
- Registro libre; sin cuenta solo se ven los títulos.
- Avance lineal por módulos, con progreso sincronizado.
- Examen por lección y marcado de laboratorio hecho.
- Glosario con tooltips y página propia.
- PDF por lección y por curso.

  </td><td>

**Para el staff (editar desde el frente)**
- Textos editables en el lugar, con barra de formato.
- Fotos pegadas con <kbd>Ctrl</kbd>+<kbd>V</kbd> en cada idea, concepto o paso.
- Ilustración principal que se pega, se arrastra o se sube y **se guarda sola**.
- Constructor de **GIF** con capturas pegadas.
- Módulos, objetivos, teoría y script editables.
- Historial: las últimas 60 versiones de cada curso.

  </td><td>

**Panel de administración**
- Indicadores y gráfico de 30 días.
- Fichas de usuarios con avance por curso.
- Salud del contenido de cada curso.
- Preguntas que más se fallan.
- Actividad y exportación a CSV.

  </td></tr>
</table>

---

## Arquitectura

```mermaid
flowchart LR
    U["👤 Navegador<br/><sub>SPA sin frameworks</sub>"] -->|HTTPS| NPM["🔐 Nginx Proxy Manager<br/><sub>Let's Encrypt</sub>"]
    NPM --> NG["nginx · CT 115<br/><sub>Debian 13 en Proxmox</sub>"]
    subgraph CT["Contenedor LXC"]
      NG -->|/ y /assets| SPA["index.html · app.js · styles.css"]
      NG -->|/api/*.php| PHP["PHP 8.4-FPM<br/><sub>auth · progress · course · admin · capturas</sub>"]
      NG -.->|auth_request| GATE["gate.php<br/><sub>¿hay sesión?</sub>"]
      GATE -.-> ILU["/ilustraciones · /capturas"]
      PHP --> DB[("SQLite WAL<br/><sub>usuarios · progreso · auditoría</sub>")]
      PHP --> JSON[("data/*.json<br/><sub>cursos · historial</sub>")]
    end
    NG -->|público| CAT["catalog.json · glosario.json"]
```

- **Contenido protegido:** `/data/<curso>.json` responde 403. El curso completo sale por `api/course.php`: con sesión devuelve todo y sin sesión solo el esquema. Las ilustraciones y las capturas pasan por `auth_request`.
- **Sesiones** con cookie `HttpOnly`, `Secure` y `SameSite=Lax`. Las escrituras exigen un encabezado propio, y hay bloqueo por intentos fallidos.
- **Sin build:** el front es un único `app.js`. El único vendor es [gifenc](https://github.com/mattdesl/gifenc) (MIT), para el constructor de GIF.

---

## Cómo se construye un curso

```mermaid
flowchart TB
    subgraph R["1 · Investigación (método claudemy)"]
      S["Fuentes web<br/><sub>documentación oficial, foros, normas</sub>"] --> N["Notas citadas<br/><sub>research/notes</sub>"] --> P["Plan de lecciones<br/><sub>acuerdos y discrepancias</sub>"]
    end
    subgraph L["2 · Lecciones"]
      P --> K["card.md · script.txt · quiz.json<br/><sub>cursos/&lt;slug&gt;/class/NN-tema</sub>"]
      K --> CH["check_lessons_es.py<br/><sub>toda URL citada existe en raw/</sub>"]
    end
    subgraph E["3 · Enriquecimiento"]
      CH --> B["build.py → site/data/&lt;slug&gt;.json"]
      I1["ilus.py + render_svg.py<br/><sub>ilustraciones → WebP</sub>"] --> M
      A1["anim.py<br/><sub>animaciones de teoría</sub>"] --> M
      M["manifest*.json<br/><sub>fig · steps · concepts · teoria_md · teoria_figs · script_rsc</sub>"]
      B --> EN["enriquecer.py"]
      M --> EN
      EN --> ES["estructura.py<br/><sub>módulos · objetivos · conecta/sigue · avisos</sub>"]
      G["glosario_check.py / glosario_merge.py"] --> GL["glosario.json"]
    end
    ES --> PUB["4 · Publicación"]
```

---

## Cómo se publica

El servidor es la fuente de verdad: lo que el staff edita en el panel nunca se pisa.

```mermaid
sequenceDiagram
    participant W as Contenedor de trabajo
    participant PC as PC de IES
    participant PVE as Proxmox (pve01)
    participant CT as CT 115 entrenamientos
    W->>PC: pedido de la versión vigente
    PC->>PVE: pvex.py cmd "pct pull 115 …/data/CURSO.json"
    PVE-->>W: CURSO-servidor.json
    W->>W: prep-publicar.sh: enriquecer --campos … + estructura
    W->>PC: site-T.tgz · CURSO-imp-T.json · pub-CURSO.sh (hash verificado)
    PC->>PVE: deploy-site.sh (sha256, sin tocar data/)
    PVE->>CT: tar → /var/www/entrenamientos + respaldo
    PC->>PVE: pub-CURSO.sh
    PVE->>CT: ¿md5 igual al que se bajó? → importar-curso.php (guarda la versión anterior)
    CT-->>PC: catálogo · glosario 200 · ilustración 401 sin sesión · curso 200
```

---

## Estructura del repositorio

```text
.
├── site/                    el portal tal como se publica
│   ├── index.html
│   ├── assets/              app.js · styles.css · vendor/gifenc
│   ├── api/                 auth · course · progress · admin · capturas · gate · lib (config.example.php)
│   ├── data/                catalog.json · glosario.json · <curso>.json (versión publicada)
│   └── ilustraciones/       <curso>/<id>.webp · <id>-paso<N>.webp · <id>-t<N>.svg (animadas)
├── cursos/<slug>/           método claudemy: sources.json · research/ · class/NN-tema/{card.md,script.txt,quiz.json}
├── ilustraciones/<slug>/    fuentes SVG, src/*.py, manifest*.json, estructura.json, glosario-propuesta.json
│   └── GUIA.md              especificación de ilustraciones, conceptos, teoría, animaciones y scripts
├── tools/                   construir, enriquecer, estructurar, animar, validar y publicar
├── deploy/                  creación del CT, nginx, NPM, despliegue e importación (sin credenciales)
├── skill/                   skill ies-entrenamientos para Claude
└── docs/                    briefs de contenido y tono · imágenes de este README
```

---

## Herramientas

| Herramienta | Qué hace |
|---|---|
| `tools/build.py <slug>` | Arma `site/data/<slug>.json` y el catálogo desde las tarjetas del curso |
| `tools/agregar-lecciones.py` | Suma o reemplaza lecciones sobre la versión del servidor sin pisar lo editado |
| `tools/enriquecer.py` | Aplica ilustraciones, pasos, conceptos, teoría, figuras de teoría y scripts (`--campos` para aplicar solo una parte) |
| `tools/estructura.py` | Módulos, orden lineal, objetivos, conecta/sigue, avisos y renumeración de la charla |
| `tools/ilus.py` · `tools/render_svg.py` | Biblioteca de ilustraciones SVG y render a WebP con las fuentes de la marca |
| `tools/anim.py` · `tools/anim_preview.py` | Animaciones SVG con CSS y vista previa por instante y cuadro fijo |
| `tools/glosario_check.py` · `tools/glosario_merge.py` | Valida el glosario y detecta RFC y siglas sin entrada; suma propuestas sin duplicar |
| `tools/check_lessons_es.py` | Verifica formato, tono y que toda URL citada exista en las fuentes guardadas |
| `tools/rsc_check.py` | Revisa los scripts RouterOS: variables, llaves, ASCII, comentarios `ies-` |
| `tools/prep-publicar.sh` | Prepara paquete, curso, glosario y script de publicación con verificación de md5 |
| `tools/importar-curso.php` | Importa un curso en el servidor y guarda la versión anterior en el historial |

---

## Probarlo en tu máquina

```bash
git clone https://github.com/flavioGonz/academy.git && cd academy
cp site/api/config.example.php site/api/config.php      # hash de la clave de editor (opcional)
mkdir -p entrenamientos-data                             # la base SQLite se crea sola al primer uso
php -S 127.0.0.1:8080 -t site
# abrí http://127.0.0.1:8080, registrate y hacete administrador:
sqlite3 entrenamientos-data/ies-training.sqlite "UPDATE users SET role='admin' WHERE email='vos@ejemplo.com';"
```

Hace falta PHP 8.x con `pdo_sqlite` y `mbstring`. Con el servidor de desarrollo de PHP no hay `auth_request`: las ilustraciones se sirven sin pedir sesión. En producción eso lo hace nginx (`deploy/nginx-acceso.sh`).

Para regenerar ilustraciones y animaciones hace falta Python 3 con Playwright (Chromium), Pillow y fontTools con brotli.

---

## Criterios de contenido

- **Exactitud:** todo sale de fuentes guardadas (documentación oficial primero) o del propio producto. Lo que no se pudo confirmar se dice en la lección.
- **Dibujar lo concreto:** qué cable, qué borne, qué menú, qué pasa con el paquete. Si un detalle no está confirmado, se dibuja genérico y rotulado.
- **Tono:** español rioplatense con voseo, cálido y directo, sin exigencias ni guiones largos.
- **Datos de ejemplo:** rangos de documentación (`192.0.2.x`, `198.51.100.x`, `203.0.113.x`), matrículas y personas inventadas. Sin datos de clientes.
- **Scripts:** se pueden pegar dos veces sin duplicar, no cortan el acceso de quien los pega y dejan comentados los pasos riesgosos. Conviene probarlos en un equipo de banco antes de usarlos en obra.

---

## Créditos

- **IES – Ingeniería en Seguridad**, Uruguay · [ies.com.uy](https://ies.com.uy) · contenido, revisión y uso en obra.
- **OmniAccess** es software de **Infratec** · [infratec.com.uy](https://infratec.com.uy).
- **Fuentes tipográficas:** Familjen Grotesk, Instrument Sans y JetBrains Mono (Google Fonts, SIL OFL).
- **Vendor:** [gifenc](https://github.com/mattdesl/gifenc) (MIT).
- Las marcas y los productos mencionados (MikroTik, Grandstream, Ubiquiti UniFi, TP-Link Omada, Akuvox, Hikvision, Paradox, Bosch, Proxmox, VMware, Microsoft Windows y otros) pertenecen a sus dueños. Este material es formación técnica independiente.
