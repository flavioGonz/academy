# Plan de lecciones: Windows para técnicos de campo, cliente y Server

Público: técnicos instaladores y de soporte de seguridad electrónica que montan servidores de VMS, controladoras de acceso y puestos de monitoreo. Nivel inicial a intermedio. Versiones: Windows 11 24H2 en adelante y Windows Server 2025 (vigentes a octubre de 2026). Fuentes: 30 páginas en raw/web, mapa en research/agreement-map.md.

12 lecciones en 3 arcos de 4. Cada lección: unos 2 minutos de audio (Lucía y Martín), una tarjeta y un laboratorio de 5 a 20 minutos en una VM o PC de banco.

## Arco 1. Red y punto de partida (lecciones 1 a 4)
Por qué este arco: antes de tocar un servidor hay que saber qué Windows es y si la red llega; el 80 por ciento de las llamadas de "no veo las cámaras" se resuelven acá.

### Lección 1 · Versión primero
- Acuerdo: 2 de 2 fuentes (evidencia fina), TH01 y TH02.
- Idea: antes de instalar, anotá edición, versión y build. Windows 11 24H2 y Server 2025 exigen firma SMB y cortan el acceso invitado, así que un NAS o grabador viejo puede dejar de abrir.
- Por qué importa: evita culpar a la red por un cambio de seguridad del sistema.
- Historia: Ned Pyle de Microsoft avisando que el NAS "bajo la escalera" puede dejar de funcionar con 24H2, https://www.theregister.com/2024/05/30/windows_11_24h2_security_tweaks/
- Laboratorio: Rápido · 10 min. winver, versión por registro, Get-SmbClientConfiguration.
- Regla: lo primero que anoto de un Windows es edición, versión y build.

### Lección 2 · Capa por capa
- Acuerdo: 2 de 2 (evidencia fina), TH03 y TH04.
- Idea: ipconfig, ping, arp y pathping en ese orden; pathping muestra en qué salto se pierde el paquete. Un ping que falla no prueba que el equipo esté apagado.
- Historia: el autor de LazyAdmin dice que no volvió a usar tracert, https://lazyadmin.nl/it/pathping-command/
- Laboratorio: Rápido · 10 min.
- Regla: si hay MAC en la tabla ARP, el equipo está vivo aunque no responda ping.

### Lección 3 · Probá el puerto
- Acuerdo: 3 de 5, TH05, TH06 y TH07.
- Idea: Test-NetConnection con el puerto del servicio, Get-NetTCPConnection para ver qué programa escucha, Resolve-DnsName para ver lo que ve la aplicación.
- Historia: nslookup sin punto final que prueba cuatro sufijos antes del nombre real, https://www.elevenforum.com/t/resolve-dnsname-vs-nslookup-in-windows.43640/latest
- Laboratorio: Foco · 15 min.
- Regla: no digo "no hay red" hasta probar el puerto exacto del servicio.

### Lección 4 · IP por consola
- Acuerdo: 2 de 2 (evidencia fina), TH08 y TH31.
- Idea: servidor con IP fija por PowerShell en cuatro pasos (limpiar, asignar, DNS, verificar); en Windows Server, el DHCP lleva IP fija, se autoriza si hay dominio y las cámaras van con reserva por MAC.
- Historia: el DHCP no autorizado en un dominio que no entrega direcciones, https://learn.microsoft.com/en-us/windows-server/networking/technologies/dhcp/quickstart-install-configure-dhcp-server
- Laboratorio: Foco · 15 min.
- Regla: la IP de un servidor se pone por consola, se verifica y se documenta.

## Arco 2. Un servidor que no se cae solo (lecciones 5 a 8)
Por qué este arco: un VMS o una controladora viven años encendidos; firewall, acceso remoto, servicios y energía bien puestos son lo que evita la visita a las tres de la mañana.

### Lección 5 · Perfil y regla
- Acuerdo: 3 de 5, TH09, TH10 y TH11.
- Idea: mirá el perfil de red de cada placa antes de abrir nada; una regla solo actúa en su perfil. Abrí por puerto o programa, con origen limitado, y exportá antes de tocar.
- Historia: la placa de un controlador de dominio que queda en perfil Público y rompe RDP, https://theitbros.com/remote-computer-requires-network-level-authentication-nla/
- Laboratorio: Foco · 15 min.
- Regla: perfil primero, regla después, y siempre con origen limitado.

### Lección 6 · RDP sin exponer
- Acuerdo: 2 de 4, TH12, TH13 y TH14. Discrepa en parte https://v2cloud.com/tutorials/change-rdp-port (cambiar puerto como capa).
- Idea: el 3389 nunca abierto a internet; RDP por VPN, con NLA activa y la regla limitada a la subred de gestión.
- Historia: ataques de ransomware a Baltimore y Atlanta que empezaron por RDP, según TechTarget, https://www.techtarget.com/cybersecurity/tip/10-RDP-security-best-practices-to-prevent-cyberattacks
- Laboratorio: Foco · 15 min.
- Regla: RDP solo por VPN, con NLA y desde la subred de gestión.

### Lección 7 · Que se levante
- Acuerdo: 2 de 2 (evidencia fina), TH16, TH17 y TH18.
- Idea: el servicio del VMS en automático (o retrasado) con recuperación ante fallas; lo que corre al arrancar va como tarea AtStartup, como SYSTEM y sin sesión.
- Historia: la plantilla de Octopus que reinicia el servicio a los 3 minutos y resetea el contador al día, https://octopus.com/integrations/windows/windows-service-set-recovery-on-failure-actions
- Laboratorio: Foco · 15 min.
- Regla: todo servicio crítico tiene recuperación configurada y probada.

### Lección 8 · Nunca dormir
- Acuerdo: 2 de 3, TH27 y TH28.
- Idea: suspensión, hibernación y apagado de disco en "nunca", Fast Startup apagado, y el BIOS en encendido tras corte; con UPS que apaga en orden, "Last State" no alcanza.
- Historia: el servidor que la UPS apagó prolijo y no volvió solo, https://www.servethehome.com/keeping-servers-bios-setup-availability/
- Laboratorio: Rápido · 10 min.
- Regla: un equipo 24/7 no duerme y vuelve solo cuando vuelve la luz.

## Arco 3. Cuando algo falla (lecciones 9 a 12)
Por qué este arco: con lo anterior en su lugar, toca diagnosticar, actualizar sin romper y cuidar las llaves; es la parte que separa al que cambia piezas del que encuentra la causa.

### Lección 9 · Qué cambió
- Acuerdo: 2 de 3, TH19, TH20 y TH21.
- Idea: arrancá por el Monitor de confiabilidad, seguí con Get-WinEvent filtrado por log, ID y fecha; 1074 dice quién reinició y 6008 marca el apagado inesperado.
- Historia: el índice que se desploma el día que se instaló una aplicación nueva, https://www.techtarget.com/it-infrastructure/tip/How-to-use-Reliability-Monitor-to-manage-servers
- Laboratorio: Rápido · 10 min.
- Regla: ante una falla, primero pregunto qué cambió y lo busco en Confiabilidad.

### Lección 10 · Disco que graba
- Acuerdo: 2 de 2 en partes distintas (evidencia fina), TH22 y TH23.
- Idea: medí latencia, IOPS y cola del disco de grabación; más de 25 ms sostenidos es un disco que no da abasto, según woshub. Y excluí del antivirus la base de grabación.
- Historia: Milestone avisa que el escaneo puede cortar la grabación o corromper la base, https://doc.milestonesys.com/2025R1/en-US/standard_features/sf_mc/sf_considerationsrequirements/mc_virusscanningexclusionsexplained.htm
- Laboratorio: Foco · 15 min.
- Regla: el disco de grabación se mide y se excluye del antivirus según el fabricante.

### Lección 11 · Actualizar con red
- Acuerdo: 3 de 6, TH24, TH25 y TH26. Discrepa https://www.techtarget.com/cybersecurity/tip/10-RDP-security-best-practices-to-prevent-cyberattacks (actualizaciones automáticas).
- Idea: actualizar sí, con ciclo definido, aviso antes de instalar y reiniciar en servidores, y un backup restaurable antes de cada cambio grande.
- Historia: servidores 2022 que amanecieron en 2025 sin licencia por una mala etiqueta en la API de Windows Update, https://windowslatest.com/2024/11/06/windows-server-2022-auto-upgraded-to-windows-server-2025-due-to-api-error
- Laboratorio: Admin · 20 min.
- Regla: antes de actualizar, backup. Siempre.

### Lección 12 · Llaves en orden
- Acuerdo: 4 de 4, TH30, con TH29 y TH32.
- Idea: cada equipo con su administrador local único y recuperable (LAPS si hay dominio), la clave de BitLocker guardada fuera del equipo y la contraseña DSRM de un controlador de dominio nunca en texto plano.
- Historia: sin la clave de recuperación de BitLocker no hay vuelta, ni el soporte de Microsoft la recupera, https://lazyadmin.nl/it/bitlocker-recovery-key/
- Laboratorio: Admin · 15 min.
- Regla: ninguna llave vive solo dentro del equipo que protege.

## Divisiones (decisiones, no lecciones)
- Actualizaciones automáticas o controladas en servidores de VMS. Lados: TechTarget pide automáticas; Microsoft sugiere para servidores avisar antes de instalar y de reiniciar; Bosch pide un ciclo máximo de 6 meses. Cómo decidir: si el cliente tiene ventana de mantenimiento y backup, controladas con calendario; si nadie va a mirar el equipo, automáticas con horas activas bien puestas, y siempre validando la compatibilidad con el fabricante del VMS.
- Cambiar el puerto 3389. Lados: v2cloud y TechTarget lo suman como capa; woshub prefiere limitar el origen en el puerto por defecto. Cómo decidir: no decide nada si hay VPN; si no hay VPN, el problema es otro.
- BIOS "Last State" o "Power On". Lados: Last State respeta lo que estaba apagado; Power On asegura el arranque aunque la UPS haya apagado el equipo. Cómo decidir: con UPS que apaga en orden, Power On.
- nslookup o Resolve-DnsName. Lados: Resolve-DnsName reproduce a la aplicación; nslookup aísla al resolvedor de Windows. Cómo decidir: empezar con Resolve-DnsName y usar nslookup para comparar.
- pathping o tracert. Lados: tracert es rápido; pathping da pérdida por salto. Cómo decidir: tracert para ver la ruta, pathping cuando hay pérdida intermitente.

## Huecos
- Evidencia fina (menos de 3 fuentes): versiones, diagnóstico básico, IP por PowerShell, servicios, tareas, rendimiento, BitLocker, roles de Server y backups. Las lecciones lo dicen en "Quién lo dice".
- Sin fuente leída: UAC en detalle (se menciona solo de pasada), Administrador de tareas y Monitor de recursos para CPU, memoria y red, Windows 11 IoT Enterprise LTSC para puestos de monitoreo, eventos 41 Kernel-Power y 7031/7034, DNS de Windows Server más allá de que se instala con el bosque, recomendaciones de energía de otros VMS.
- El presupuesto de búsqueda web de la sesión se agotó a mitad de la investigación; las fuentes se completaron con sitemaps y enlaces de páginas ya abiertas.

## Entrega
12 carpetas class/NN-handle con script.txt, card.md y quiz.json; class/course.json con la ficha. El audio lo renderiza el orquestador.
