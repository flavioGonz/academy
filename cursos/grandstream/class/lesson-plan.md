# Plan de lecciones: Telefonía IP Grandstream: UCM y terminales

Nivel: inicial a intermedio. Público: técnicos instaladores y de soporte. 12 lecciones de unos 2 minutos, en 3 arcos de 4, más un arco de 6 lecciones sobre líneas analógicas por FXO (13 a 18) agregado en octubre de 2026.
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

### Lección 19. Troncal SIP de Antel (agregada en octubre de 2026)
- Va después de Troncal registrado y antes de Patrón y privilegio: en el portal queda en el módulo "Hablar con el mundo" (orden 4, 19, 5, 6).
- 3 de 3 fuentes que describen la troncal de Antel coinciden en que va por IP, sin registro y con OPTIONS de Antel (TH46); 2 de 2 en lo que entrega (TH47); la página de Antel da planes y condiciones, no datos técnicos (TH48). Notas: research/notes/c.md.
- Idea: Peer SIP Trunk con el servidor de Antel en Host Name; la UCM contesta 200 OK a los OPTIONS de Antel; modo Dual con la troncal en su propio puerto y ruta estática a las redes de Antel; caller ID de la troncal en toda saliente; patrones de Uruguay.
- Por qué importa: es la troncal que más instala IES en clientes nuevos, y el error típico es buscar usuario y contraseña o colgarla del switch del cliente detrás de un NAT.
- Historia: el FreePBX que contestaba 401 a cada OPTIONS de Antel (https://community.freepbx.org/t/antel-sip-trunk-only-options/84614); el técnico de 3CX con ping a la IP de prueba recién al agregar rutas (https://www.3cx.com/community/threads/troncal-sip-antel-and-3cx.50040/); datos, topologías y pruebas en la guía de Simpletech (https://www.simpletech.uy/en/troncal-sip-empresarial-antel-uruguay/); planes TSIP8 a TSIP180 (https://antel.com.uy/empresas/internet-y-fija/planes/troncal-sip); plan de numeración (https://www.itu.int/dms_pub/itu-t/oth/02/02/T02020000E00001PDFS.pdf).
- Laboratorio: Foco, 25 min. Planilla, modo Dual, ruta estática, Peer trunk, captura del OPTIONS, entrante en dos tiempos, saliente con el plan de Uruguay, pruebas de entrega. Sin troncal real: una segunda UCM o un Asterisk hace de Antel (https://documentation.grandstream.com/knowledge-base/how-to-interconnect-multiple-ucm/).
- Regla: la troncal de Antel se pide por escrito, se conecta directo a la central y se da por terminada con una captura del OPTIONS de Antel con su 200 OK y una saliente con el número de la troncal.

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

## Arco agregado (octubre de 2026). Líneas analógicas por FXO
Por qué este arco: muchos comercios siguen con líneas de cobre de Antel, y es donde la UCM se parece menos a una central SIP: no hay mensajes de corte, no llega número llamado y el identificador depende de la línea. Va después de "Las llamadas van donde tienen que ir" porque usa las rutas, el IVR y los grupos ya armados. Al terminar, una línea de Antel suena en un teléfono, un grupo o un IVR, y el técnico tiene un método cuando no anda.
Base: 25 páginas (manual del UCM630x y del UCM630xA, guía Manage Analog Lines, guía del HT80x V2, lista de tonos UIT E.180, 5 páginas de Antel, documentación y foros de Asterisk y FreePBX, Wikipedia, innovaphone, Patton, Sandman, Yeastar y AudioCodes). Notas: research/notes/b.md. Mapa: TH32 a TH45 en research/agreement-map.md.

### Lección 13. Qué trae el par
- 4 de 4 fuentes coinciden en FXS y FXO (TH32); en valores difieren y ninguna da los de Antel (TH33).
- Idea: la línea de Antel es un FXS (tensión, timbre, tono) y el FXO de la UCM descuelga y cuelga; se mide antes de enchufar y se anota lo que cuelga del mismo par.
- Por qué importa: la ficha de la línea sana es la vara de cualquier diagnóstico y de cualquier reclamo.
- Historia: el panel de alarma que entra en falla cuando alguien descuelga la línea compartida (https://www.sandman.com/firealarm-bul.html); 48 V en reposo y 4 a 18 V descolgado, según Sandman.
- Laboratorio: Campo, 20 min. Medir reposo y descolgado, teléfono de prueba, recorrer el par, ficha, enchufar al FXO1.
- Regla: ninguna línea se enchufa al FXO sin su ficha.

### Lección 14. Troncal analógica
- 3 de 3 fuentes en ruta por troncal porque no llega número llamado (TH34); 2 de 2 en los estados del Dashboard (TH35).
- Idea: Analog Trunks con canales FXO y nombre sin número real; una troncal por línea si entran distinto, una para varias si son iguales (Ascend, Poll, Descend); FXO Opermode y PCMA Override.
- Historia: Ascend toma siempre el puerto 1 si está libre (https://documentation.grandstream.com/knowledge-base/manage-analog-lines/); PCMA fuera de Norteamérica (https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/).
- Laboratorio: Foco, 15 min. Dos troncales, colores del Dashboard, cable desconectado, teléfono en paralelo descolgado.
- Regla: una troncal por línea si cada línea entra a un lugar distinto.

### Lección 15. Tonos y corte
- 5 de 7 fuentes en los tres métodos de corte y en medirlo (TH38); 2 de 2 en los tonos de Uruguay (TH37, evidencia delgada y de 2010).
- Idea: el corte se adivina por tono, polaridad o corriente; en Uruguay todo es 425 Hz y cambia la cadencia; la UCM viene con tonos de Estados Unidos; PSTN Detection mide.
- Historia: ocupado 425 Hz 0,5/0,5 (https://www.itu.int/dms_pub/itu-t/opb/sp/T-SP-E.180-2010-PDF-S.pdf); busy detection que corta salientes a los tres timbres (https://community.asterisk.org/t/asterisk-hangsup-when-busydetect-yes/44836).
- Laboratorio: Foco, 20 min. Tonos Custom, Busy Tone Count 4, PSTN Detection, prueba de corte, Analog Record Trace y Audacity si no corta.
- Regla: los tonos se cargan o se miden, nunca se dejan en Estados Unidos.

### Lección 16. Identificador y audio
- 5 de 6 fuentes en confirmar el servicio y probar esquemas (TH39); 2 de 3 en impedancia antes que ganancias (TH40).
- Idea: sin la facilidad de Antel no hay número; con ella, Auto-Detect y probar esquemas; eco y volumen se arreglan primero con ACIM.
- Historia: Bellcore manda el número entre el primer y el segundo timbre (https://en.wikipedia.org/wiki/Caller_ID); Uruguay no figura en la tabla de países; "Failed to decode CallerID" con el teléfono mostrando el número (https://lists.digium.com/pipermail/asterisk-users/2010-July/251933.html).
- Laboratorio: Foco, 20 min. Teléfono con pantalla, Auto-Detect, esquemas uno por uno, ACIM, ganancias, eco y fax.
- Regla: el esquema que funciona va a la ficha de la línea.

### Lección 17. Hasta que suene
- 4 de 4 fuentes en que no hay DID y la ruta va por troncal (TH41); 3 de 3 en salida con orden, failover y número de la línea (TH42).
- Idea: la llamada analógica entra a `s`; ruta entrante por troncal con `_.` y destino (grupo 6000, IVR 7000, fax); ruta saliente con patrones de Uruguay y failover; el que recibe ve el número de la línea.
- Historia: "When an analog call comes into Asterisk, the call is sent to the s extension" (https://docs.asterisk.org/Configuration/Dialplan/Special-Dialplan-Extensions/); Outbound Route CID no aplica a analógicas.
- Laboratorio: Foco, 25 min. Dos entrantes, una saliente con failover, pruebas con celular, cable desconectado.
- Regla: toda troncal analógica tiene ruta entrante con destino, y ninguna prueba vale si quedó en `s`.

### Lección 18. Diagnóstico de línea
- 6 de 8 fuentes en piezas del método (TH44); el caso real no está en ninguna fuente y se presenta como hipótesis.
- Idea: de la ficha a la configuración: medir, teléfono de prueba, desconectar lo que está en paralelo, cambiar el par de puerto, revisar ruta y detección, grabar, reclamar con datos.
- Historia: el caso del comercio con FXO2 en loop cada 10 s (capturas editadas); el FXO "In Use" sin tensión (https://community.asterisk.org/t/functioning-pstn-line-with-red-alarm/65892); entrantes fantasma por polaridad (https://community.freepbx.org/t/polarity-switch-causing-false-call-backs/35199); reclamos al 121 (https://antel.com.uy/atencion-telefonica).
- Laboratorio: Campo, 25 min. Foto del estado, medición, paralelo, cambio de pares, ruta, Analog Record Trace, syslog chan_dahdi, reclamo.
- Regla: antes de culpar a la central o a Antel, cambiá el par de puerto.

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
- Lección 19: Antel no publica servidor, puertos, codecs, formato del número entrante ni del saliente, ni cómo entrega la troncal en FTTH (puerto del ONT, VLAN o equipo aparte); tampoco si su servidor contesta los OPTIONS de la central ni desde cuántas IP manda señalización y audio. La lección enseña a pedirlo en la planilla y a confirmarlo en la primera captura. La guía técnica más completa es de un integrador (2018, actualizada en 2025).
- Módulo FXO: Antel no publica tensión, frecuencia de timbre, esquema de identificador ni método de corte de su línea; las lecciones 13, 15 y 16 enseñan a medirlo y probarlo. La lista de tonos de la UIT es de 2010. No se encontró norma técnica pública de URSEC sobre la interfaz analógica.
- GDMS sin guía técnica leída (las páginas cargan con JavaScript); se menciona en lecciones 1 y 3 sin pasos detallados.
- GSC3570 y altavoces GSC35xx sin fuente propia; la lección 12 se centra en GDS37xx.
- WP8xx sin guía propia leída; se tratan como terminal SIP aprovisionable.
- QoS, VLAN de voz y jitter casi sin cobertura.
- El foro oficial de Grandstream no se pudo leer desde el entorno; los casos de foro vienen de 3CX, FreePBX, Netgate y Wazo.

- Módulo FXO, corte de llamada: Busy Tone Count alto (Grandstream) contra el aviso de que muy alto no detecta (Yeastar) y los falsos cortes de Asterisk. Cómo decidir: PSTN Detection y una prueba colgando del otro lado. Inversión de polaridad: solo si la detección la encuentra (https://community.freepbx.org/t/polarity-switch-causing-false-call-backs/35199).

## Entrega
Guion, tarjeta y quiz por lección en class/NN-handle/. El audio lo renderiza el orquestador.
