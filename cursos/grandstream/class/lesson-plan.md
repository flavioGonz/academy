# Plan de lecciones: Telefonía IP Grandstream: UCM y terminales

Nivel: inicial a intermedio. Público: técnicos instaladores y de soporte. 12 lecciones de unos 2 minutos, en 3 arcos de 4.
Base: 24 páginas leídas (6 de documentation.grandstream.com, 3 del blog de Grandstream, 4 guías de proveedores de troncales y SIP ALG, foros de FreePBX, Netgate, 3CX y Wazo, un CVE). Mapa de acuerdos: research/agreement-map.md.
Versiones: UCM6300/6300A con el firmware oficial vigente a octubre de 2026 (manual del UCM630x actualizado el 27/10/2026). En UCM6200 y UCM6510 los menús cambian un poco.

## Arco 1. La central en pie
Por qué este arco: antes de rutas y menús, la central tiene que quedar con la red bien elegida, cerrada, con extensiones sólidas, teléfonos aprovisionados solos y un troncal registrado. Al terminar, la UCM hace y recibe llamadas.

### Lección 1. Primer arranque
- 3 de 4 fuentes coinciden (TH01, TH02, TH04); Telnyx todavía cita admin/admin.
- Idea: elegir el modo de red (Switch por defecto, Route, Dual) antes de nada, entrar por HTTPS 8089 con la contraseña de la etiqueta, cambiarla y hacer backup antes de actualizar firmware.
- Por qué importa: Route habilita DHCP opción 66 y Dynamic Defense; cambiar el modo después rompe lo armado.
- Historia: CVE-2025-28172, UCM6510 hasta 1.0.20.52 sin límite de intentos de login (https://www.tenable.com/cve/CVE-2025-28172). Simtex: admin/admin es de las causas más comunes de centrales comprometidas (https://www.simtex.com.au/support/kb/pbx-setup-guides/grandstream-ucm-sip-trunk-configuration).
- Laboratorio: Foco, 15 min. Modo de red, contraseña, versión de firmware, backup descargado.
- Regla: antes de actualizar, backup; y la contraseña de la etiqueta no sobrevive al primer día.

### Lección 2. Extensión sólida
- 2 de 2 fuentes (evidencia delgada en cantidad, oficial).
- Idea: contraseña SIP aleatoria, registros concurrentes acotados (3 por defecto, hasta 10), NAT activado, Direct Media apagado, DTMF RFC4733.
- Por qué: la mayoría de los audios cortados y fraudes empiezan en una extensión floja.
- Ejemplo: Direct Media apagado por defecto: el audio pasa por la central (https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/).
- Laboratorio: Rápido, 10 min. Crear 3 extensiones con contraseña aleatoria y revisar la pestaña Media.
- Regla: la contraseña de la extensión la genera la central, nunca la cliente.

### Lección 3. Zero Config
- 2 de 2 fuentes (oficiales); GDMS como alternativa en la nube (https://blog.grandstream.com/company/news/blog/gdms-is-a-game-changer).
- Idea: descubrir teléfonos por SIP SUBSCRIBE u opción 66, plantillas con prioridad Global Policy, Global Template, Model Template; lo configurado a mano en el teléfono no lo pisa la plantilla.
- Historia: escaneo por SIP Message a la dirección de broadcast cuando faltan equipos (https://documentation.grandstream.com/knowledge-base/zero-config-guide/).
- Laboratorio: Foco, 20 min. Descubrir un GRP, asignarle extensión y sincronizar.
- Regla: el teléfono que se aprovisiona no se toca a mano.

### Lección 4. Troncal registrado
- 3 de 3 fuentes coinciden.
- Idea: Register SIP Trunk con host, usuario, Auth ID y contraseña; ver estado en el Dashboard; heartbeat; codecs recortados; no abrir puertos para el troncal.
- Historia: "Rejected" es alcance o credenciales (https://documentation.grandstream.com/knowledge-base/sip-trunks-guide/); Simtex: 99,9 % de los casos sin reenvío de puertos.
- Laboratorio: Foco, 15 min. Troncal de laboratorio, heartbeat 60 s, codecs PCMA y PCMU.
- Regla: el troncal se prueba con llamada saliente, entrante, caller ID y una tecla en el buzón.

## Arco 2. Las llamadas van donde tienen que ir
Por qué este arco: con la central en pie, el trabajo diario es rutear: quién puede marcar qué, a dónde entra cada número, qué escucha el que llama y quién atiende. Al terminar, un cliente tipo pyme queda funcionando.

### Lección 5. Patrón y privilegio
- 4 de 5 fuentes coinciden en privilegios y PIN; Simtex y el manual difieren en el orden de rutas.
- Idea: patrones con guion bajo (X, Z, N, punto), Strip para el prefijo, privilegio Internal a International, PIN en internacionales, failover.
- Historia: _9NXXXXXXXXX con Strip 1 (https://support.telnyx.com/en/articles/5748258-grandstream-configuring-sip-trunks-on-your-grandstream-ucm6xxx-series); failover a los 32 s o ante 403, 407, 408, 503, 603.
- Laboratorio: Foco, 15 min. Ruta nacional y ruta internacional con PIN.
- Regla: la ruta internacional nace con PIN y privilegio International.

### Lección 6. Cada DID
- 2 de 2 fuentes (oficiales).
- Idea: ruta entrante con patrón DID, destino ByDID, Strip; DID Mode del troncal; horarios y lista negra.
- Historia: 0655441007 con Strip 6 llega a la 1007 (https://documentation.grandstream.com/knowledge-base/sip-trunks-guide/).
- Laboratorio: Rápido, 10 min. Simular DID con troncal peer de laboratorio o calcular strips en papel.
- Regla: el Strip se calcula con el número completo que manda el proveedor, no con el que figura en la factura.

### Lección 7. IVR con horario
- 2 de 2 fuentes; el blog habla de 5 niveles, el manual de 64 IVR anidados.
- Idea: cada tecla con destino por horario, timeout y opción inválida con destino, prompts propios, lista blanca de internas.
- Laboratorio: Foco, 15 min.
- Regla: todo IVR tiene destino para el que no marca nada.

### Lección 8. Grupo o cola
- 2 de 2 fuentes.
- Idea: grupo de llamada para "que suene en todos"; cola cuando hay espera, agentes, estrategia y desborde; buzón con PIN no trivial y a correo.
- Historia: devolución de llamada sin perder el lugar en la cola (https://blog.grandstream.com/company/news/blog/how-to-use-the-ucm-ip-pbxs-call-center-features).
- Laboratorio: Foco, 15 min.
- Regla: ninguna cola sin destino de desborde.

## Arco 3. Fuera de la oficina y cuando algo falla
Por qué este arco: internos remotos, routers ajenos, ataques y porteros son donde se gana o se pierde el soporte. Al terminar, el técnico diagnostica audio de un lado, cierra la central y conecta un portero.

### Lección 9. Interno remoto
- 3 de 3 fuentes.
- Idea: External Host, Use IP address in SDP, Local Network Address, puertos 5060 y 10000 a 20000 reenviados, STUN en el teléfono; el puerto se cambia en la central, no solo en el router.
- Historia: sin Local Network Address la IP externa no se arma bien (https://documentation.grandstream.com/knowledge-base/ucm-remote-extensions-guide/); 5555 a 5060 no funciona (https://community.freepbx.org/t/fail2ban-securing-pbx-behind-router-with-port-forwarding/70943).
- Laboratorio: Campo, 20 min.
- Regla: External Host sin Local Network Address es medio trabajo.

### Lección 10. Audio de un lado
- 6 de 7 fuentes coinciden en NAT y puertos primero; 5 de 5 en apagar SIP ALG; Plexatalk y SureVoIP admiten excepciones.
- Idea: orden de diagnóstico: NAT y puertos, ALG, captura en la UCM leyendo el SDP.
- Historia: corte a los 32 s por ACK perdido (https://didlogic.com/learn/sip-alg-explained/); GXP que oye pero no es oído (https://www.3cx.com/community/threads/grandstream-phone-receiver-cant-hear-me.116955/).
- Laboratorio: Campo, 20 min. Ethernet Capture y lectura de la línea c= del SDP.
- Regla: no se toca un router sin una captura antes.

### Lección 11. Central cerrada
- 4 de 7 fuentes en cerrar la administración; 3 de 7 en Fail2ban.
- Idea: Fail2ban activo con Allowlist, lista blanca web, sin 80 ni 443, SSH y AMI apagados, Geo-IP, privilegios; VPN o lista blanca por IP para remotos.
- Historia: varios INVITE maliciosos por segundo y más de 50 IPs baneadas (https://wazo-platform.discourse.group/t/fail2ban-guide-for-servers-on-the-internet/399); VPN caída 2 a 4 veces por año por certificados (https://community.freepbx.org/t/vpn-or-tls/91126).
- Laboratorio: Admin, 15 min.
- Regla: cada puerto abierto tiene nombre, motivo y Fail2ban mirando.

### Lección 12. Portero en la central
- 3 de 3 fuentes.
- Idea: el GDS37xx se registra como extensión, el timbre llama a una interna o grupo, apertura con PIN remoto por DTMF o tecla OpenDoor; video solo en ciertos GRP.
- Historia: GRP2601 a 2604 solo audio, GRP2614 en adelante con imagen (https://documentation.grandstream.com/knowledge-base/connecting-gds37xx-with-grp26xxx/).
- Laboratorio: Campo, 20 min.
- Regla: el PIN de apertura no es el de fábrica ni el del buzón.

## Divisiones
- VPN o puertos abiertos para internos remotos. VPN primero (https://community.freepbx.org/t/vpn-or-tls/91126); lista blanca por IP para sedes con IP fija (https://community.freepbx.org/t/cloud-hosted-pbx-direct-sip-or-vpn/47641); VPN que se cae y pierde llamadas (https://community.freepbx.org/t/fail2ban-securing-pbx-behind-router-with-port-forwarding/70943). Cómo decidir: pocos remotos con IP fija, lista blanca; muchos móviles y alguien que mantenga certificados, VPN; si no hay ninguna de las dos, puertos no estándar con Fail2ban, Geo-IP y PIN en rutas caras.
- SIP ALG siempre apagado o depende. Cómo decidir: con UCM y teléfonos Grandstream, que ya manejan NAT, apagado; si no se puede apagar, TLS o cambiar el router (https://didlogic.com/learn/sip-alg-explained/, https://www.plexatalk.co.uk/?p=17613).
- Login de fábrica. Cómo decidir: mirar la etiqueta; equipos desde enero de 2017 traen contraseña aleatoria.
- Orden de rutas salientes. Cómo decidir: mirar Outgoing Routing Priority en el equipo y probar con un número que matchee dos rutas.

## Huecos
- GDMS sin guía técnica leída (las páginas cargan con JavaScript); se menciona en lecciones 1 y 3 sin pasos detallados.
- GSC3570 y altavoces GSC35xx sin fuente propia; la lección 12 se centra en GDS37xx.
- WP8xx sin guía propia leída; se tratan como terminal SIP aprovisionable.
- QoS, VLAN de voz y jitter casi sin cobertura.
- El foro oficial de Grandstream no se pudo leer desde el entorno; los casos de foro vienen de 3CX, FreePBX, Netgate y Wazo.

## Entrega
Guion, tarjeta y quiz por lección en class/NN-handle/. El audio lo renderiza el orquestador.
