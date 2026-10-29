# Mapa del tema: Telefonía IP Grandstream (UCM y terminales)

Nivel: inicial a intermedio. Público: técnicos instaladores y de soporte con base de redes.

Cómo se enseña (lo que miré antes de armar el mapa):
- Bootcamp de certificación UCM (Grandstream Certified Specialist) de NTS Direct: hardware, web UI, quick setup y Zero Config, troncales SIP y red, reportes, mantenimiento y troubleshooting, más GDS3710 el segundo día (https://ntsdirect.com/?p=4104).
- Entrenamiento GWN y UC 2026 de Streakwave con instructores de Grandstream: configuración inicial, extensiones y buzón, gestión de dispositivos, ruteo y caller ID, funciones de llamada y seguridad, administración y troubleshooting; kit con UCM6301 y GRP2604P (https://streakwave.focuspointsap.com/grandstream-training-certification).
- El índice del manual oficial del UCM630x (actualizado el 27/10/2026) y las guías de la base de conocimiento de documentation.grandstream.com (Zero Config, SIP Trunks, Remote Extensions, Security Manual, GDS37xx con GRP26xx).

## Subtemas
- T01 Plataforma UCM6300/6300A: modelos, puertos FXS/FXO, modo de red (Route/Switch/Dual), primer acceso web, firmware y backup
- T02 Extensiones: contraseña SIP, registros concurrentes, NAT, Direct Media, DTMF, SRTP
- T03 Provisioning local con Zero Config: descubrimiento, plantillas y prioridades, asignación de extensiones
- T04 Gestión en la nube con GDMS (y RemoteConnect)
- T05 Troncales SIP con proveedores: Register, Peer y Account trunk, parámetros, estado de registro, codecs del troncal
- T06 Rutas salientes: patrones, strip/prepend, privilegios, failover, DOD
- T07 Rutas entrantes: DID, ByDID, strip, condiciones de horario, lista negra
- T08 IVR: eventos de tecla, horarios, prompts, anidado
- T09 Grupos de llamada y colas: estrategias, tiempos, desborde
- T10 Buzón de voz: acceso, PIN, envío a correo, operador
- T11 Extensiones remotas y NAT: External Host, red local, puertos 5060 y 10000 a 20000, STUN en el teléfono
- T12 SIP ALG: qué hace, síntomas, cómo apagarlo y qué hacer si no se puede
- T13 Seguridad de la central: contraseñas, acceso web, Fail2ban, defensa estática y dinámica, Geo-IP, fraude de peaje, firmware
- T14 Exponer SIP o usar VPN: puertos abiertos, TLS, listas blancas por IP
- T15 Porteros GDS37xx y GSC conectados a la UCM: cuenta SIP, botón de timbre, PIN remoto por DTMF, video en el teléfono
- T16 Troubleshooting: audio unidireccional, captura Ethernet, syslog, codecs, pruebas de troncal

## Módulo agregado en octubre de 2026: Líneas analógicas por FXO
Cómo se enseña: la guía "Manage Analog Lines" de Grandstream (troncal, rutas, ACIM, PSTN Detection, Analog Record Trace, SLA), el manual del UCM630x y del UCM630xA, la lista de tonos nacionales de la UIT (E.180) y la documentación de Asterisk/DAHDI, que es el motor analógico de la UCM.
- T17 La línea analógica: FXS y FXO, tensión en reposo y descolgado, timbre, RJ11, equipos en paralelo, qué ofrece Antel
- T18 Troncal analógica en el UCM: canales FXO, una troncal por línea o grupo, selección de línea saliente, estados en el Dashboard, Opermode y PCMA
- T19 Tonos de Uruguay y detección de corte: tonos E.180, Tone Country y Custom, busy detection, polaridad, current disconnect, ring timeout, PSTN Detection
- T20 Identificador de llamadas, ganancias y eco: esquemas FSK y DTMF, Antel, ACIM, RX y TX, cancelador de eco, fax
- T21 De la línea al destino: extensión s, ruta entrante por troncal, extensión, grupo o IVR, ruta saliente con varias líneas, numeración de Uruguay, desvíos de Antel
- T22 Diagnóstico de líneas analógicas: Dashboard, Active Calls, CDR, Analog Record Trace, syslog chan_dahdi, multímetro, teléfono de prueba, cambio de par, reclamo a Antel

## Lección agregada en octubre de 2026: Troncal SIP de Antel
Cómo se enseña: la página comercial de Antel (planes TSIP), la guía de implementación que publicó un integrador uruguayo, hilos de técnicos que la instalaron con 3CX y FreePBX, el manual del UCM630x (Peer SIP Trunk, modo Dual, Static Routes, SIP Settings) y el plan de numeración de Uruguay notificado a la UIT. Notas: research/notes/c.md.
- T23 Troncal SIP de Antel: planes, qué entrega Antel, red privada, número de servicio, migración de números, reclamos
- T24 La troncal por IP en la UCM: Peer SIP Trunk, OPTIONS de Antel, modo Dual, rutas estáticas, topologías y NAT
- T25 Numeración de Uruguay y caller ID con Antel: patrones salientes, formato entrante, número de salida
- T26 Diagnóstico de la troncal SIP: captura, respuestas 401, 403, 404, 408 y 484, pruebas de entrega

## Lección agregada en octubre de 2026: IVR que solo anuncia
Cómo se enseña: el manual del UCM630x y del UCM630xA (IVR, Announcement, Custom Prompt, CDR), la guía de IVR de Grandstream, la documentación de Asterisk sobre Background(), WaitExten() y las extensiones i y t, y casos de foro de DTMF detectado de más o de menos en líneas analógicas. Notas: research/notes/d.md.
- T27 El IVR por dentro: Prompt, Digit Timeout, Response Timeout, repeticiones, Timeout e Invalid, Key Pressing Events
- T28 Marcar internos desde el IVR (Dial Other Extensions) y la alternativa Announcement
- T29 DTMF falso en líneas analógicas: talk-off, eco, detección en el FXO, inband y RFC 4733
- T30 Medir y verificar: llamada de prueba, CDR (Action Type, Call Time, Talk Time), Analog Record Trace
