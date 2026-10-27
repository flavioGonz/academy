# Mapa de acuerdos: Windows para técnicos de campo

Fuente: research/notes/a.md (30 páginas, 59 notas). M = páginas con al menos una nota en el subtema del tema (incluye líneas Also). N = cuántas de esas M apoyan el tema. M menor a 3 se marca "evidencia fina".

M por subtema: T01 2 · T02 2 · T03 5 · T04 2 · T05 5 · T06 4 · T07 2 · T08 1 · T09 3 · T10 2 · T11 6 · T12 3 · T13 2 · T14 4 · T15 2 · T16 2.

## TH01 Identificá versión, edición y build antes de instalar: Windows 11 24H2 y Server 2025 exigen firma SMB y cortan el acceso invitado
- Sub-topic: T01 (also T11)
- Agree: 2 of 2 (evidencia fina). Notes: a:N3, a:N4. Urls: https://learn.microsoft.com/en-us/windows-server/get-started/whats-new-windows-server-2025, https://www.theregister.com/2024/05/30/windows_11_24h2_security_tweaks/
- Disagree: none found
- Level: foundation
- Best story: el NAS viejo que deja de abrir tras pasar a 24H2; Microsoft pide actualizar o reemplazar el NAS antes que bajar la seguridad, https://www.theregister.com/2024/05/30/windows_11_24h2_security_tweaks/

## TH02 Server 2025 trae de serie OpenSSH, Terminal, WinGet y Credential Guard; el hotpatch sin reinicio está en vista previa y atado a Azure Arc, así que no se cuenta con él
- Sub-topic: T01
- Agree: 1 of 2 (evidencia fina). Notes: a:N1, a:N2. Urls: https://learn.microsoft.com/en-us/windows-server/get-started/whats-new-windows-server-2025
- Disagree: none found
- Level: core
- Best story: none

## TH03 Diagnosticá por capas y usá pathping para ubicar el salto donde se pierde el paquete
- Sub-topic: T02
- Agree: 2 of 2 (evidencia fina). Notes: a:N5, a:N7, a:N8. Urls: https://lazyadmin.nl/it/pathping-command/, https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection
- Disagree: none found (Test-NetConnection -TraceRoute es la alternativa en PowerShell)
- Level: foundation
- Best story: el autor de LazyAdmin dice que no volvió a usar tracert después de pathping, https://lazyadmin.nl/it/pathping-command/

## TH04 Un ping que falla no prueba que el equipo esté caído: ICMP puede estar bloqueado; probá el puerto del servicio
- Sub-topic: T02 (also T03)
- Agree: 2 of 2 (evidencia fina). Notes: a:N6, a:N8. Urls: https://lazyadmin.nl/it/pathping-command/, https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection
- Disagree: none found
- Level: foundation
- Best story: none

## TH05 Probá el puerto concreto del servicio con Test-NetConnection -Port en vez de suponer
- Sub-topic: T03
- Agree: 3 of 5. Notes: a:N8, a:N9, a:N27. Urls: https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection, https://adamtheautomator.com/netstat-port/, https://v2cloud.com/tutorials/change-rdp-port
- Disagree: none found
- Level: foundation
- Best story: none

## TH06 Para saber qué programa escucha un puerto, usá Get-NetTCPConnection con OwningProcess o netstat -ano en consola elevada
- Sub-topic: T03
- Agree: 2 of 5. Notes: a:N9, a:N10, a:N27. Urls: https://adamtheautomator.com/netstat-port/, https://v2cloud.com/tutorials/change-rdp-port
- Disagree: none found
- Level: foundation
- Best story: none

## TH07 Para reproducir lo que ve una aplicación usá Resolve-DnsName; nslookup consulta solo servidores DNS y agrega sufijos a nombres sin punto final
- Sub-topic: T03
- Agree: 1 of 5. Notes: a:N11, a:N12, a:N13. Urls: https://www.elevenforum.com/t/resolve-dnsname-vs-nslookup-in-windows.43640/latest
- Disagree: none found (la misma fuente rescata nslookup para aislar fallas del resolvedor)
- Level: core
- Best story: "nslookup bing.com" que consulta cuatro sufijos inventados antes del nombre real y da timeout, https://www.elevenforum.com/t/resolve-dnsname-vs-nslookup-in-windows.43640/latest

## TH08 A un servidor que da servicio ponele IP fija por PowerShell: limpiar IP y ruta vieja, New-NetIPAddress con PrefixLength, DNS aparte, verificar
- Sub-topic: T04 (also T15)
- Agree: 2 of 2 (evidencia fina). Notes: a:N14, a:N15, a:N16. Urls: https://oneuptime.com/blog/post/2026-03-20-set-static-ipv4-powershell-new-netipaddress/view, https://learn.microsoft.com/en-us/windows-server/networking/technologies/dhcp/quickstart-install-configure-dhcp-server
- Disagree: none found
- Level: foundation
- Best story: none

## TH09 Antes de crear reglas, mirá qué perfil de red tiene cada placa: una regla solo actúa en su perfil
- Sub-topic: T05 (also T06)
- Agree: 3 of 5. Notes: a:N17, a:N18, a:N22. Urls: https://woshub.com/manage-windows-firewall-powershell/, https://learn.microsoft.com/es-es/powershell/module/netsecurity/new-netfirewallrule, https://theitbros.com/remote-computer-requires-network-level-authentication-nla/
- Disagree: none found
- Level: foundation
- Best story: placa de un DC que queda en perfil Public y rompe la autenticación de RDP, https://theitbros.com/remote-computer-requires-network-level-authentication-nla/

## TH10 Abrí por puerto o por programa y limitá el origen (LocalSubnet o IP concretas), no "todo a todos"
- Sub-topic: T05 (also T06)
- Agree: 3 of 5. Notes: a:N19, a:N28, a:N29. Urls: https://learn.microsoft.com/es-es/powershell/module/netsecurity/new-netfirewallrule, https://woshub.com/manage-windows-firewall-powershell/, https://www.techtarget.com/cybersecurity/tip/10-RDP-security-best-practices-to-prevent-cyberattacks
- Disagree: none found
- Level: core
- Best story: none

## TH11 Exportá la configuración del firewall antes de tocarla y revisá puertos con los filtros, porque Get-NetFirewallRule no los muestra
- Sub-topic: T05
- Agree: 1 of 5. Notes: a:N20, a:N21. Urls: https://woshub.com/manage-windows-firewall-powershell/
- Disagree: none found
- Level: core
- Best story: none

## TH12 Nunca dejes el 3389 abierto a internet: RDP detrás de VPN o gateway, y limitado por IP
- Sub-topic: T06
- Agree: 2 of 4. Notes: a:N23, a:N24, a:N28, a:N29. Urls: https://www.techtarget.com/cybersecurity/tip/10-RDP-security-best-practices-to-prevent-cyberattacks, https://woshub.com/manage-windows-firewall-powershell/
- Disagree: https://v2cloud.com/tutorials/change-rdp-port: si el equipo es accesible desde internet, cambiar el puerto y limitar IP como capas extra (no dice "nunca")
- Level: foundation
- Best story: ataques de ransomware a Baltimore y Atlanta que empezaron por RDP (afirmación de TechTarget), https://www.techtarget.com/cybersecurity/tip/10-RDP-security-best-practices-to-prevent-cyberattacks

## TH13 Mantené NLA activa; si da error, arreglá DNS, controlador de dominio, canal seguro u hora, y apagarla es solo temporal
- Sub-topic: T06 (also T14)
- Agree: 2 of 4. Notes: a:N24, a:N25, a:N53. Urls: https://theitbros.com/remote-computer-requires-network-level-authentication-nla/, https://www.techtarget.com/cybersecurity/tip/10-RDP-security-best-practices-to-prevent-cyberattacks
- Disagree: none found
- Level: core
- Best story: none

## TH14 Cambiar el puerto de RDP baja el ruido de escaneos pero no reemplaza VPN ni NLA
- Sub-topic: T06
- Agree: 2 of 4. Notes: a:N27. Urls: https://v2cloud.com/tutorials/change-rdp-port, https://www.techtarget.com/cybersecurity/tip/10-RDP-security-best-practices-to-prevent-cyberattacks
- Disagree: https://woshub.com/manage-windows-firewall-powershell/: pone el foco en restringir por IP de origen en el puerto por defecto
- Level: core
- Best story: none

## TH15 En dominio conectá por nombre completo (FQDN) y no por IP, para que Kerberos funcione con NLA
- Sub-topic: T06
- Agree: 1 of 4. Notes: a:N26. Urls: https://theitbros.com/remote-computer-requires-network-level-authentication-nla/
- Disagree: none found
- Level: advanced
- Best story: none

## TH16 Configurá la recuperación del servicio (reiniciar ante falla, con demora y reset del contador) y verificala con sc qfailure
- Sub-topic: T07
- Agree: 2 of 2 (evidencia fina). Notes: a:N30, a:N30b. Urls: https://ss64.com/nt/sc.html, https://octopus.com/integrations/windows/windows-service-set-recovery-on-failure-actions
- Disagree: none found
- Level: core
- Best story: none

## TH17 En PowerShell escribí sc.exe (sc es alias de Set-Content) y dejá un espacio después del igual
- Sub-topic: T07
- Agree: 1 of 2 (evidencia fina). Notes: a:N31. Urls: https://ss64.com/nt/sc.html
- Disagree: none found
- Level: foundation
- Best story: none

## TH18 Lo que tiene que correr al arrancar va como tarea AtStartup, sin sesión iniciada, con privilegios altos, en carpeta propia y con "Iniciar en" definido
- Sub-topic: T08 (also T07)
- Agree: 1 of 1 (evidencia fina). Notes: a:N32, a:N33. Urls: https://lazyadmin.nl/powershell/how-to-create-a-powershell-scheduled-task/
- Disagree: none found
- Level: core
- Best story: el script que deja sus archivos en System32 porque nadie definió "Iniciar en", https://lazyadmin.nl/powershell/how-to-create-a-powershell-scheduled-task/

## TH19 Filtrá el Visor de eventos por log, ID y fecha con Get-WinEvent -FilterHashtable, no con Where-Object
- Sub-topic: T09
- Agree: 2 of 3. Notes: a:N34, a:N35. Urls: https://theitbros.com/get-windows-event-logs-powershell/, https://woshub.com/check-shutdown-reboot-logs-windows/
- Disagree: none found
- Level: core
- Best story: none

## TH20 Ante un reinicio sin explicación buscá el 1074 (quién lo pidió) y el 6008 (apagado inesperado)
- Sub-topic: T09 (also T11, T12)
- Agree: 1 of 3. Notes: a:N34, a:N37. Urls: https://woshub.com/check-shutdown-reboot-logs-windows/
- Disagree: none found
- Level: core
- Best story: el 1074 que muestra NT AUTHORITY\SYSTEM y el proceso de Windows Update como autor del reinicio, https://woshub.com/check-shutdown-reboot-logs-windows/

## TH21 Empezá por "qué cambió": el Monitor de confiabilidad (perfmon /rel) cruza fallas con instalaciones y updates por día
- Sub-topic: T09
- Agree: 1 of 3. Notes: a:N36. Urls: https://www.techtarget.com/it-infrastructure/tip/How-to-use-Reliability-Monitor-to-manage-servers
- Disagree: none found
- Level: foundation
- Best story: la caída del índice el día que se instaló una aplicación nueva, https://www.techtarget.com/it-infrastructure/tip/How-to-use-Reliability-Monitor-to-manage-servers

## TH22 Medí el disco con latencia, IOPS y cola en perfmon, no a ojo
- Sub-topic: T10
- Agree: 1 of 2 (evidencia fina). Notes: a:N38, a:N39, a:N40. Urls: https://woshub.com/how-to-measure-disk-iops-using-powershell/
- Disagree: none found
- Level: core
- Best story: umbrales del autor: más de 25 ms de latencia es un disco que no da abasto, https://woshub.com/how-to-measure-disk-iops-using-powershell/

## TH23 Excluí del antivirus la base de grabación del VMS, sus extensiones y procesos
- Sub-topic: T10 (also T13)
- Agree: 1 of 2 (evidencia fina). Notes: a:N41. Urls: https://doc.milestonesys.com/2025R1/en-US/standard_features/sf_mc/sf_considerationsrequirements/mc_virusscanningexclusionsexplained.htm
- Disagree: none found
- Level: core
- Best story: el escaneo que bloquea archivos de la base y corta la grabación o la corrompe, https://doc.milestonesys.com/2025R1/en-US/standard_features/sf_mc/sf_considerationsrequirements/mc_virusscanningexclusionsexplained.htm

## TH24 En servidores, que Windows avise antes de instalar y de reiniciar; un equipo sin nadie logueado se reinicia solo
- Sub-topic: T11
- Agree: 3 of 6. Notes: a:N42, a:N43, a:N34, a:N45. Urls: https://learn.microsoft.com/en-us/windows/deployment/update/waas-restart, https://woshub.com/check-shutdown-reboot-logs-windows/, https://windowslatest.com/2024/11/06/windows-server-2022-auto-upgraded-to-windows-server-2025-due-to-api-error
- Disagree: https://www.techtarget.com/cybersecurity/tip/10-RDP-security-best-practices-to-prevent-cyberattacks: habilitar actualizaciones automáticas
- Level: core
- Best story: servidores 2022 que amanecieron en 2025 sin licencia por una mala etiqueta en la API de Windows Update, https://windowslatest.com/2024/11/06/windows-server-2022-auto-upgraded-to-windows-server-2025-due-to-api-error

## TH25 Actualizá igual, con un ciclo definido: congelar el servidor tampoco es seguro
- Sub-topic: T11
- Agree: 3 of 6. Notes: a:N44, a:N3, a:N4. Urls: https://knowledge.keenfinity-group.com/video-systems/article/what-is-the-recommendation-regarding-the-windows-u, https://learn.microsoft.com/en-us/windows-server/get-started/whats-new-windows-server-2025, https://www.theregister.com/2024/05/30/windows_11_24h2_security_tweaks/
- Disagree: none found
- Level: core
- Best story: Bosch pide un ciclo máximo de 6 meses y una actualización mayor cada dos años, https://knowledge.keenfinity-group.com/video-systems/article/what-is-the-recommendation-regarding-the-windows-u

## TH26 Antes de un cambio grande, un backup que sepas restaurar: es la única marcha atrás real
- Sub-topic: T16 (also T11)
- Agree: 2 of 2 (evidencia fina). Notes: a:N57, a:N58. Urls: https://ss64.com/nt/wbadmin.html, https://windowslatest.com/2024/11/06/windows-server-2022-auto-upgraded-to-windows-server-2025-due-to-api-error
- Disagree: none found
- Level: core
- Best story: restaurar, reconstruir o pagar licencia: las tres salidas tras el upgrade accidental, https://windowslatest.com/2024/11/06/windows-server-2022-auto-upgraded-to-windows-server-2025-due-to-api-error

## TH27 En un equipo 24/7, suspensión e hibernación en "nunca" con powercfg y Fast Startup apagado
- Sub-topic: T12
- Agree: 1 of 3. Notes: a:N46, a:N47. Urls: https://ss64.com/nt/powercfg.html
- Disagree: none found
- Level: foundation
- Best story: none

## TH28 Configurá en el BIOS el encendido tras corte, sabiendo que "Last State" no vuelve si la UPS apagó el equipo en orden
- Sub-topic: T12
- Agree: 2 of 3. Notes: a:N48, a:N34. Urls: https://www.servethehome.com/keeping-servers-bios-setup-availability/, https://woshub.com/check-shutdown-reboot-logs-windows/
- Disagree: none found (ServeTheHome marca la contra de "Power On": enciende también lo que estaba apagado a propósito)
- Level: core
- Best story: el servidor que la UPS apagó prolijo y no volvió solo con el BIOS en Last State, https://www.servethehome.com/keeping-servers-bios-setup-availability/

## TH29 Guardá la clave de BitLocker fuera del equipo y suspendé BitLocker antes de tocar BIOS, firmware o hardware
- Sub-topic: T13
- Agree: 1 of 2 (evidencia fina). Notes: a:N49, a:N50. Urls: https://lazyadmin.nl/it/bitlocker-recovery-key/
- Disagree: none found
- Level: core
- Best story: sin clave no hay recuperación, ni siquiera el soporte de Microsoft puede, https://lazyadmin.nl/it/bitlocker-recovery-key/

## TH30 Cada equipo con su administrador local único y recuperable (LAPS en dominio), y el resto de las cuentas con lo mínimo
- Sub-topic: T14
- Agree: 4 of 4. Notes: a:N51, a:N52, a:N53, a:N54. Urls: https://theitbros.com/enable-windows-laps-in-active-directory/, https://learn.microsoft.com/en-us/windows-server/get-started/whats-new-windows-server-2025, https://theitbros.com/remote-computer-requires-network-level-authentication-nla/, https://www.techtarget.com/cybersecurity/tip/10-RDP-security-best-practices-to-prevent-cyberattacks
- Disagree: none found
- Level: core
- Best story: entrar con el admin local o por iLO cuando el dominio no responde, https://theitbros.com/remote-computer-requires-network-level-authentication-nla/

## TH31 En Server: el DC instala DNS con el bosque, el DHCP lleva IP fija y en dominio se autoriza, y las cámaras van con reserva por MAC
- Sub-topic: T15
- Agree: 2 of 2 (evidencia fina). Notes: a:N55, a:N56. Urls: https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/install-active-directory-domain-services--level-100-, https://learn.microsoft.com/en-us/windows-server/networking/technologies/dhcp/quickstart-install-configure-dhcp-server
- Disagree: none found
- Level: advanced
- Best story: none

## TH32 Antes de promover un DC, corré el Test- del cmdlet y no escribas la contraseña DSRM en texto plano
- Sub-topic: T15
- Agree: 1 of 2 (evidencia fina). Notes: a:N55. Urls: https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/install-active-directory-domain-services--level-100-
- Disagree: none found
- Level: advanced
- Best story: none

## The big splits
- Actualizar servidores de VMS: automático (https://www.techtarget.com/cybersecurity/tip/10-RDP-security-best-practices-to-prevent-cyberattacks) vs avisar y decidir en servidores (https://learn.microsoft.com/en-us/windows/deployment/update/waas-restart) vs ciclo máximo de 6 meses del fabricante (https://knowledge.keenfinity-group.com/video-systems/article/what-is-the-recommendation-regarding-the-windows-u). Gira en quién controla el momento del reinicio y si hay backup.
- Cambiar el puerto de RDP: capa útil (https://v2cloud.com/tutorials/change-rdp-port, https://www.techtarget.com/cybersecurity/tip/10-RDP-security-best-practices-to-prevent-cyberattacks) vs restringir origen en el puerto por defecto (https://woshub.com/manage-windows-firewall-powershell/). Todos coinciden en que no reemplaza la VPN.
- BIOS "Last State" vs "Power On" (https://www.servethehome.com/keeping-servers-bios-setup-availability/): gira en si hay UPS con apagado ordenado.
- nslookup vs Resolve-DnsName (https://www.elevenforum.com/t/resolve-dnsname-vs-nslookup-in-windows.43640/latest): reproducir a la aplicación vs aislar el resolvedor.
- pathping vs tracert (https://lazyadmin.nl/it/pathping-command/): rapidez vs estadística por salto.

## Coverage gaps
- Evidencia fina: T01, T02, T04, T07, T08, T10, T13, T15, T16 (M menor a 3).
- Sin fuente leída: UAC en detalle (tokens filtrados, cuándo pide elevación), Administrador de tareas y Monitor de recursos fuera del disco (CPU, memoria, red), Windows 11 IoT Enterprise LTSC como opción para puestos de monitoreo, Windows Server Backup como rol instalado (Install-WindowsFeature Windows-Server-Backup), arp en profundidad, eventos 41 (Kernel-Power) y 7031/7034 (servicio que se cayó), DNS de Windows Server más allá de "se instala con el bosque".
- Lo que un técnico esperaría y no está en las fuentes: guía oficial de Microsoft para equipos 24/7 sin usuario, recomendaciones de energía de otros VMS (Genetec, Hikvision), y procedimiento de restauración probado paso a paso.
