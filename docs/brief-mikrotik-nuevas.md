# Brief común: lecciones nuevas del curso MikroTik (25 a 35)

Nico (dueño de IES, integrador de seguridad electrónica en Uruguay) pidió estos capítulos que faltan en el curso MikroTik del portal IES Training:

| id | Carpeta | Tema |
|---|---|---|
| 25 | 25-bridges | Creación de bridges (puertos al bridge, por qué un bridge y no varios, hw offload, el bridge por defecto, quitar ether1 del bridge para WAN) |
| 26 | 26-asignar-ip | Asignación de IP (/ip/address, red y máscara, varias IP en una interfaz, IP en VLAN o bridge, servidor DHCP básico para la LAN) |
| 27 | 27-rutas-estaticas | Rutas estáticas para internet y para túneles (ruta por defecto, gateway, distance, check-gateway, rutas hacia redes remotas por un túnel, ruta a la IP pública del VPN por el ISP) |
| 28 | 28-l2tp-cliente | L2TP cliente: túnel saliente (el MikroTik se conecta a un servidor L2TP/IPsec remoto, use-ipsec, ipsec-secret, add-default-route sí/no, rutas por el túnel, NAT por el túnel) |
| 29 | 29-diagnostico-terminal | Diagnóstico por terminal: ping, traceroute, ping con src-address, medir saltos, saber dónde falla (LAN, gateway, ISP, destino), /tool/traceroute, ping con tamaño y do-not-fragment para MTU |
| 30 | 30-dns-mikrotik | DNS en MikroTik (/ip/dns, servers, allow-remote-requests y su riesgo de resolver abierto en WAN, cache, entradas estáticas, DoH en RouterOS 7) |
| 31 | 31-dns-transparente | MikroTik como DNS transparente (redirigir con dst-nat/redirect todo el puerto 53 de la LAN al router, por qué, excepciones, DoH que lo esquiva) |
| 32 | 32-dns-adlist | DNS address-list y bloqueo de sitios (adlist de RouterOS 7.15+ si las fuentes lo confirman, entradas estáticas NXDOMAIN o FWD, address-list por nombre de dominio en el firewall y sus límites) |
| 33 | 33-firewall-proteccion | Firewall: reglas típicas de protección (input: established/related, invalid, ICMP limitado, admins por address-list, drop final; forward: fasttrack, invalid, drop WAN no DSTNATed; listas de bloqueo por intentos: SSH/WinBox brute force con address-list y timeout; protección de DNS abierto) |
| 34 | 34-ip-neighbors | IP Neighbors para detectar vecinos: LLDP, CDP y MNDP (qué es cada uno, /ip/neighbor, discovery settings y en qué interfaces conviene apagarlo, descubrir switches, cámaras y otros MikroTik) |
| 35 | 35-netwatch | Netwatch (vigilar hosts, up-script/down-script, tipos de prueba en RouterOS 7: icmp, tcp-conn, http-get, dns; ejemplos: avisar por e-mail o Telegram si cae el NVR, failover, reiniciar un PoE) |

## Cómo trabajar
- Workspace: `/home/claude/claudemy/mikrotik/` (sources.json, raw/web/, research/notes/, class/ con 01 a 24). Antes de escribir, leé las lecciones existentes que tocan tu tema para no repetir ni contradecir: 01 (entrar), 03 (cerrar puertas), 04 (input y forward), 05 (VLAN por sistema), 08 (túnel de gestión), 11 (dos WAN), 12 (Torch y sniffer), 13-15 (IP fija, DHCP, PPPoE), 18-22 (cloud, BTH, CHR, L2TP/IPsec servidor, IPsec), 23 (Safe Mode), 24 (port forwarding, en preparación). Referite a ellas por tema ("la lección de Safe Mode"), no por número.
- Brief obligatorio de formato y tono: `/home/claude/ies-training/brief-ies.md` (script.txt, card.md, quiz.json; español rioplatense con voseo; sin exigencias; sin guiones largos). Método claudemy: `/root/.claude/skills/claudemy/`.
- Fuentes: help.mikrotik.com (documentación oficial de RouterOS 7) primero, después foro oficial y practicantes serios. Al menos 3 páginas nuevas por lección guardadas en raw/. RouterOS 7, versión vigente a octubre de 2026.
- **Archivos compartidos con otros agentes** (`sources.json`, `class/lesson-plan.md`, `research/notes/`): otros dos agentes trabajan en paralelo en el mismo workspace. Para editar sources.json o lesson-plan.md y para correr el scraper, usá siempre un lock: `flock /home/claude/claudemy/mikrotik/.lock -c '<comando>'` y releé el archivo dentro del lock antes de escribirlo (hacé la edición con un script python corto dentro del flock, nunca reescribas el archivo desde una copia vieja). Tus notas de investigación van en un archivo propio: `research/notes/n<tus ids>.md` (ej. `n25-28.md`).
- Scraper: `flock /home/claude/claudemy/mikrotik/.lock -c 'python3 /root/.claude/skills/claudemy/scripts/scrape.py /home/claude/claudemy/mikrotik web'`.
- Checker solo sobre tus carpetas: `python3 /home/claude/ies-training/tools/check_lessons_es.py /home/claude/claudemy/mikrotik <carpeta1> <carpeta2> …` (valida que toda URL citada, incluso en bloques de código, exista como `url:` en raw/; en comandos usá IPs, no `http://`).
- Cada lección: `class/<carpeta>/` con script.txt, card.md (`# Lección <id>. <Nombre de 2 a 3 palabras>`), quiz.json (3 preguntas de obra, correctas en posiciones distintas). Laboratorio de 10 a 20 min en un router de banco, con comandos exactos.
- En `lesson-plan.md` agregá cada lección con su número al final, en una sección "Lecciones agregadas (pedido de Nico, octubre 2026)" (bajo el lock). NO modifiques course.json ni lecciones ajenas.

## Enriquecimiento (en la misma tarea)
Para cada lección tuya seguí `/home/claude/ies-training/ilustraciones/GUIA.md` entera: ilustración principal `<id>.svg`, 1 a 3 de pasos `<id>-paso<N>.svg` (lo concreto: qué puerto va al bridge, la tabla de rutas, el camino del ping que falla en el salto 3, el DNS redirigido…), scripts en `/home/claude/ies-training/ilustraciones/mikrotik/src/<id>.py`, render con `/home/claude/ies-training/tools/render_svg.py` y revisión de cada PNG, y un manifest propio `/home/claude/ies-training/ilustraciones/mikrotik/manifest-<desde>-<hasta>.json` con fig, steps (anclas `after` copiadas tal cual del laboratorio), concepts (2 a 4: para qué se creó, cómo se usa, ejemplo) y teoria_md (`### Un poco de historia` y `### Cómo funciona`, 250 a 450 palabras; RFC con número y año correctos: ej. DNS RFC 1034/1035 de 1987, traceroute de 1987 por Van Jacobson, LLDP IEEE 802.1AB de 2005, CDP de Cisco, L2TP RFC 2661 de 1999 / RFC 3931). Biblioteca `/home/claude/ies-training/tools/ilus.py` (no la modifiques).

No despliegues nada. Al terminar reportá: títulos, resumen de cada lección, fuentes nuevas, checker, archivos de ilustración y lo que no pudiste confirmar.
