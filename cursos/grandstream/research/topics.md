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
