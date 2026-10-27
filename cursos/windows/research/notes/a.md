# Notes: batch a
Pages read: 30. With notes: 30. Skipped: 0 (tres páginas de la primera tanda se reemplazaron antes de leer: woshub block-rdp-brute-force por ser un script largo sin enseñanza aplicable a obra, y el post de 2013 del Scripting Guy por estar superado por el artículo de 2026 del Microsoft Networking Blog, y CSO Online por repetir lo de TechTarget; entró una plantilla de recuperación de servicios).

## T01 Versiones y canales vigentes
- a:N1. Windows Server 2025 permite upgrade en sitio salteando hasta cuatro versiones, desde Windows Server 2012 R2 en adelante. Trae escritorio con estilo Windows 11, Terminal, WinGet y OpenSSH servidor instalados por defecto.
  - Source: https://learn.microsoft.com/en-us/windows-server/get-started/whats-new-windows-server-2025  Quote: "You can upgrade directly to Windows Server 2025 from Windows Server 2012 R2 and later."
  - Kind: definition
  - Level: foundation
  - Bias: none (documentación oficial)
- a:N2. Server 2025: Credential Guard viene activado por defecto en equipos que cumplen requisitos; hotpatch (parches sin reinicio) existe pero en vista previa y atado a Azure Arc.
  - Source: https://learn.microsoft.com/en-us/windows-server/get-started/whats-new-windows-server-2025  Quote: "Credential Guard is now enabled by default on devices that meet the requirements."
  - Kind: definition
  - Level: core
  - Also: T11
  - Bias: none
- a:N3. Server 2025 exige firma SMB en todas las conexiones SMB salientes por defecto (antes solo SYSVOL y NETLOGON) y las reglas de firewall nuevas de compartir archivos ya no abren NetBIOS 137 a 139.
  - Source: https://learn.microsoft.com/en-us/windows-server/get-started/whats-new-windows-server-2025  Quote: "SMB signing is now required by default for all SMB outbound connections."
  - Kind: rule of thumb
  - Level: core
  - Also: T05, T11
  - Bias: none
- a:N4. Windows 11 24H2 exige firma SMB en todas las conexiones y deshabilita el acceso invitado (guest fallback) en Pro; NAS viejos o pendrives en routers pueden dejar de abrir. Microsoft recomienda actualizar o reemplazar el equipo antes que bajar la seguridad.
  - Source: https://www.theregister.com/2024/05/30/windows_11_24h2_security_tweaks/  Quote: "SMB signing is now required by default on all connections, and guest fallback has been disabled"
  - Kind: story
  - Level: core
  - Also: T11
  - Bias: none

## T02 Diagnóstico de red básico
- a:N5. Pathping combina ping y tracert: primero traza la ruta y después mide pérdida y latencia en cada salto, lo que muestra dónde se pierde el paquete. Por defecto manda 100 consultas por salto y resuelve nombres; con -n, -q 10 y -h se acelera.
  - Source: https://lazyadmin.nl/it/pathping-command/  Quote: "it will first trace the route to the destination and then performs a ping to each node"
  - Kind: technique
  - Level: foundation
- a:N6. Pathping usa ICMP; si un router o firewall bloquea ICMP, el trazado se corta ahí aunque el servicio funcione. Un ping fallido no prueba que el equipo esté caído.
  - Source: https://lazyadmin.nl/it/pathping-command/  Quote: "some server, routers or firewalls have blocked the ICMP protocol"
  - Kind: mistake
  - Level: foundation
  - Also: T03
- a:N7. El autor de LazyAdmin dice que dejó de usar tracert desde que aprendió pathping (su opinión).
  - Source: https://lazyadmin.nl/it/pathping-command/  Quote: "I have never used tracert again"
  - Kind: story
  - Level: foundation

## T03 Diagnóstico de puertos y DNS
- a:N8. Test-NetConnection hace ping, prueba de puerto TCP (-Port), traza (-TraceRoute) y diagnóstico de ruta; -CommonTCPPort acepta HTTP, RDP, SMB y WINRM; -InformationLevel Quiet devuelve solo verdadero o falso, útil en scripts.
  - Source: https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection  Quote: "It supports ping test, TCP test, route tracing, and route selection diagnostics."
  - Kind: technique
  - Level: foundation
  - Also: T02
- a:N9. netstat -a muestra escuchas y conexiones; -n evita resolver nombres; -b muestra el proceso y exige consola elevada. Get-NetTCPConnection devuelve objetos con OwningProcess y se filtra por -State Listen o -LocalPort; con Get-Process -Id se obtiene el nombre del programa.
  - Source: https://adamtheautomator.com/netstat-port/  Quote: "Using the -b switch requires an elevated command prompt"
  - Kind: technique
  - Level: foundation
- a:N10. Una dirección local 0.0.0.0 en netstat significa que el servicio escucha en todas las placas; si muestra la IP de una placa, solo escucha en esa.
  - Source: https://adamtheautomator.com/netstat-port/  Quote: "this will be 0.0.0.0 for the IP part, meaning it is listening on all network interfaces"
  - Kind: definition
  - Level: foundation
- a:N11. nslookup no usa el resolvedor de Windows: ignora el archivo hosts, la caché, mDNS, LLMNR y las políticas NRPT; consulta solo servidores DNS. Resolve-DnsName sí usa el resolvedor de Windows, así que reproduce lo que ve una aplicación.
  - Source: https://www.elevenforum.com/t/resolve-dnsname-vs-nslookup-in-windows.43640/latest  Quote: "nslookup only uses DNS servers for name resolution"
  - Kind: rule of thumb
  - Level: core
  - Bias: none (reposteo del Microsoft Networking Blog, enero 2026)
- a:N12. nslookup agrega cada sufijo DNS de búsqueda a un nombre sin punto final; con muchos sufijos da timeout. El ejemplo: "nslookup bing.com" consultó bing.com.contoso.com, .fabrikam.com, etc., antes del nombre real. Con punto final ("bing.com.") se evita.
  - Source: https://www.elevenforum.com/t/resolve-dnsname-vs-nslookup-in-windows.43640/latest  Quote: "nslookup expects FQDNs to be dot terminated"
  - Kind: story
  - Level: core
- a:N13. Resolve-DnsName tiene -DnsOnly, -NoHostsFile, -CacheOnly, -Server y -Type; Microsoft lo recomienda para probar cómo resuelve un programa en Windows. nslookup sigue siendo útil para sospechar del resolvedor o de políticas.
  - Source: https://www.elevenforum.com/t/resolve-dnsname-vs-nslookup-in-windows.43640/latest  Quote: "Microsoft recommends using Resolve-DnsName"
  - Kind: technique
  - Level: core

## T04 Configurar IP por PowerShell
- a:N14. Secuencia para IP fija: Get-NetAdapter para el nombre e índice, quitar la IP y la ruta por defecto existentes (Remove-NetIPAddress, Remove-NetRoute), New-NetIPAddress con -PrefixLength y -DefaultGateway, después Set-DnsClientServerAddress, y verificar con Get-NetIPAddress y Get-DnsClientServerAddress.
  - Source: https://oneuptime.com/blog/post/2026-03-20-set-static-ipv4-powershell-new-netipaddress/view  Quote: "Remove existing IPv4 address on the interface"
  - Kind: template
  - Level: foundation
  - Bias: blog de una empresa de monitoreo (OneUptime), contenido técnico sin venta directa
- a:N15. PrefixLength 24 equivale a máscara 255.255.255.0; New-NetIPAddress no toma máscara en notación decimal.
  - Source: https://oneuptime.com/blog/post/2026-03-20-set-static-ipv4-powershell-new-netipaddress/view  Quote: "PrefixLength 24 is equivalent to subnet mask 255.255.255.0"
  - Kind: definition
  - Level: foundation
- a:N16. El servidor DHCP de Windows exige IPv4 estática como prerrequisito.
  - Source: https://learn.microsoft.com/en-us/windows-server/networking/technologies/dhcp/quickstart-install-configure-dhcp-server  Quote: "A static IPv4 address."
  - Kind: rule of thumb
  - Level: foundation
  - Also: T15

## T05 Firewall de Windows
- a:N17. Hay tres perfiles (Dominio, Privado, Público); por defecto se permite todo lo saliente y se bloquea todo lo entrante salvo reglas. Get-NetConnectionProfile muestra qué perfil tiene cada placa; si la red se detecta mal, se cambia la categoría.
  - Source: https://woshub.com/manage-windows-firewall-powershell/  Quote: "allows all outbound connections and blocks all inbound connections"
  - Kind: definition
  - Level: foundation
- a:N18. Una regla de New-NetFirewallRule solo actúa cuando su perfil está activo; el valor por defecto de -Profile es Any. -RemoteAddress acepta IP, rangos, subredes y palabras clave como LocalSubnet.
  - Source: https://learn.microsoft.com/es-es/powershell/module/netsecurity/new-netfirewallrule  Quote: "The rule is active on the local computer only when the specified profile is currently active."
  - Kind: definition
  - Level: core
- a:N19. Las reglas pueden ser por puerto (-Protocol, -LocalPort) o por programa (-Program con ruta completa); el ejemplo oficial permite un programa solo desde la subred local con -RemoteAddress LocalSubnet.
  - Source: https://learn.microsoft.com/es-es/powershell/module/netsecurity/new-netfirewallrule  Quote: "only from computers on the same subnet as the local computer"
  - Kind: technique
  - Level: core
- a:N20. Antes de tocar reglas, exportar la configuración con netsh advfirewall export a un .wfw; se restaura con import. netsh advfirewall reset borra las reglas propias.
  - Source: https://woshub.com/manage-windows-firewall-powershell/  Quote: "Before resetting the firewall rules, you can export the current settings to a file."
  - Kind: technique
  - Level: core
- a:N21. Get-NetFirewallRule no muestra puertos ni IP; hay que encadenar Get-NetFirewallPortFilter y Get-NetFirewallAddressFilter para ver qué abre cada regla.
  - Source: https://woshub.com/manage-windows-firewall-powershell/  Quote: "the Get-NetFirewallRule cmdlet doesn't show network ports and IP addresses"
  - Kind: mistake
  - Level: core
- a:N22. Si la placa de un controlador de dominio queda en perfil Public o Private en vez de DomainAuthenticated, fallan autenticaciones (NLA); deshabilitar y habilitar la placa suele corregirlo.
  - Source: https://theitbros.com/remote-computer-requires-network-level-authentication-nla/  Quote: "If it returns Public or Private instead of DomainAuthenticated, try disabling and enabling the NIC."
  - Kind: mistake
  - Level: advanced
  - Also: T06

## T06 Escritorio remoto seguro
- a:N23. No exponer el 3389 a internet: RDP detrás de VPN o Remote Desktop Gateway; aun con MFA y contraseñas fuertes, expuesto queda sujeto a fuerza bruta, bloqueos de cuenta y denegación de servicio. Ataques de ransomware (Baltimore, Atlanta) empezaron por RDP (su afirmación).
  - Source: https://www.techtarget.com/cybersecurity/tip/10-RDP-security-best-practices-to-prevent-cyberattacks  Quote: "RDP should never be open to the internet"
  - Kind: rule of thumb
  - Level: foundation
- a:N24. Lista de prácticas de RDP: parches al día, contraseñas fuertes con segundo factor, bloqueo de cuentas, VPN, gateway de RDP y solo conexiones con NLA sobre TLS, que protege contra robo de credenciales en el medio.
  - Source: https://www.techtarget.com/cybersecurity/tip/10-RDP-security-best-practices-to-prevent-cyberattacks  Quote: "Only allow connections from computers running Remote Desktop with Network Level Authentication (NLA) over TLS."
  - Kind: rule of thumb
  - Level: foundation
- a:N25. NLA viene activado por defecto en todas las versiones soportadas; el error "requiere NLA" suele ser DNS, DC inalcanzable, canal seguro roto o reloj desfasado, no un problema de RDP en sí. Desactivar NLA es parche temporal; después se vuelve a activar.
  - Source: https://theitbros.com/remote-computer-requires-network-level-authentication-nla/  Quote: "NLA is enabled by default in all supported versions of Windows."
  - Kind: mistake
  - Level: core
- a:N26. Conectar por IP en vez de FQDN puede impedir Kerberos y forzar NTLM, y eso rompe NLA en dominio. El estado de NLA se consulta con Win32_TSGeneralSetting, propiedad UserAuthenticationRequired.
  - Source: https://theitbros.com/remote-computer-requires-network-level-authentication-nla/  Quote: "using an IP address instead of an FQDN may prevent Kerberos authentication"
  - Kind: mistake
  - Level: advanced
- a:N27. Cambiar el puerto de RDP (registro PortNumber en RDP-Tcp, rango 49152 a 65535) reduce escaneos automáticos pero no frena amenazas; hay que abrir el puerto nuevo en el firewall y limitar IP de origen.
  - Source: https://v2cloud.com/tutorials/change-rdp-port  Quote: "changing the port won't stop all potential threats"
  - Kind: technique
  - Level: core
  - Also: T03 (verifica el puerto nuevo con netstat -an)
  - Bias: vende escritorios virtuales (V2 Cloud)
- a:N28. Restringir el puerto de RDP a una lista de IP confiables y monitorear intentos fallidos; aplicar mínimo privilegio a quién tiene RDP.
  - Source: https://www.techtarget.com/cybersecurity/tip/10-RDP-security-best-practices-to-prevent-cyberattacks  Quote: "Restrict access to the Remote Desktop port to an individual or group of trusted IP addresses"
  - Kind: technique
  - Level: core
  - Also: T05, T14
- a:N29. Permitir RDP desde una sola IP con -RemoteAddress en una regla de firewall.
  - Source: https://woshub.com/manage-windows-firewall-powershell/  Quote: "allow an incoming RDP connection on the default TCP\3389 port from only one IP address"
  - Kind: template
  - Level: core
  - Also: T05

## T07 Servicios
- a:N30. sc failure configura qué hace Windows cuando un servicio se cae: restart, run o reboot con demoras en milisegundos y un reset del contador en segundos; sc qfailure lo consulta. failureflag 1 dispara las acciones también si el servicio se detiene con error.
  - Source: https://ss64.com/nt/sc.html  Quote: "Change the actions taken by a service upon failure"
  - Kind: technique
  - Level: core
- a:N30b. Plantilla de recuperación de servicio: reiniciar en la primera, segunda y tercera falla con 180000 ms (3 minutos) de espera y reset del contador a 86400 segundos (un día), aplicada con sc.exe failure nombre actions= restart/180000/restart/180000/restart/180000 reset= 86400.
  - Source: https://octopus.com/integrations/windows/windows-service-set-recovery-on-failure-actions  Quote: "Specifies the length of time (in seconds) with no failures after which the failure count should be reset to 0."
  - Kind: template
  - Level: core
  - Bias: plantilla de una herramienta de despliegue (Octopus), sin venta en el contenido
- a:N31. sc config acepta start= auto, demand, disabled y delayed-auto; el espacio después del igual es obligatorio. En PowerShell, "sc" es alias de Set-Content: hay que escribir sc.exe.
  - Source: https://ss64.com/nt/sc.html  Quote: "A space is required between the equal sign and the value."
  - Kind: mistake
  - Level: foundation

## T08 Tareas programadas
- a:N32. Una tarea con disparador AtStartup y "ejecutar aunque el usuario no haya iniciado sesión" corre sin nadie logueado; con -RunLevel Highest corre elevada. Conviene carpeta propia (-TaskPath), -NoProfile y límite de duración.
  - Source: https://lazyadmin.nl/powershell/how-to-create-a-powershell-scheduled-task/  Quote: "make sure that the script runs even when we are not logged on"
  - Kind: template
  - Level: core
- a:N33. Si no se define "Iniciar en", el script deja sus archivos en C:\Windows\System32.
  - Source: https://lazyadmin.nl/powershell/how-to-create-a-powershell-scheduled-task/  Quote: "Otherwise, the output will be saved in C:\Windows\System32"
  - Kind: mistake
  - Level: foundation

## T09 Visor de eventos y Confiabilidad
- a:N34. Evento 1074 en System registra quién o qué proceso pidió el reinicio (usuario, servicio de Windows Update como SYSTEM, VMware Tools); el 6008 marca un apagado inesperado (corte de luz, pantallazo azul).
  - Source: https://woshub.com/check-shutdown-reboot-logs-windows/  Quote: "you have to search for an EventID 6008"
  - Kind: technique
  - Level: core
  - Also: T11, T12
- a:N35. Get-WinEvent con -FilterHashtable (LogName, ID, StartTime) es mucho más rápido que filtrar con Where-Object; Get-EventLog no existe en PowerShell 7.
  - Source: https://theitbros.com/get-windows-event-logs-powershell/  Quote: "This log search command is many times faster"
  - Kind: technique
  - Level: core
- a:N36. El Monitor de confiabilidad (perfmon /rel) grafica un índice de 1 a 10 por día con fallas de aplicaciones, de Windows, instalaciones y updates; sirve para responder "qué cambió desde ayer" y se puede exportar a XML.
  - Source: https://www.techtarget.com/it-infrastructure/tip/How-to-use-Reliability-Monitor-to-manage-servers  Quote: "the first troubleshooting step is to find out what changed"
  - Kind: technique
  - Level: foundation
- a:N37. Si los registros se borraron o se sobrescribieron, no hay forma de saber quién reinició; conviene agrandar el tamaño máximo del log.
  - Source: https://woshub.com/check-shutdown-reboot-logs-windows/  Quote: "it is recommended to increase the max size of event logs"
  - Kind: mistake
  - Level: core

## T10 Rendimiento
- a:N38. Para disco: Administrador de tareas (velocidad y tiempo medio de respuesta), Monitor de recursos (longitud de cola) y perfmon con contadores de PhysicalDisk: Avg. Disk sec/Transfer (latencia), Disk Transfers/sec (IOPS), Disk Bytes/sec, Avg. Disk Queue Length.
  - Source: https://woshub.com/how-to-measure-disk-iops-using-powershell/  Quote: "Avg. Disk Sec./Transfer (latency)"
  - Kind: technique
  - Level: core
- a:N39. Umbrales según el autor: latencia de disco sobre 25 ms indica que el arreglo no da abasto; en sistemas exigidos, no pasar de 10 ms; cola de un disco no mayor a 2 (8 para RAID de 4).
  - Source: https://woshub.com/how-to-measure-disk-iops-using-powershell/  Quote: "If the delay is more than 25 ms (0.25), then the disk array cannot handle the I/O operation on time."
  - Kind: number
  - Level: core
- a:N40. DiskSpd genera carga real; el autor advierte no correrlo en producción en horario de uso. IOPS de referencia del autor: disco de 7200 rpm entre 50 y 75.
  - Source: https://woshub.com/how-to-measure-disk-iops-using-powershell/  Quote: "it is not recommended to start tests on productive systems during peak or working hours"
  - Kind: number
  - Level: advanced
- a:N41. Milestone: no escanear con antivirus las carpetas de base de grabación (por defecto C:\mediadatabase) ni archivos .blk, .idx, .pic; el escaneo consume recursos y puede bloquear archivos, cortar grabación o corromper la base.
  - Source: https://doc.milestonesys.com/2025R1/en-US/standard_features/sf_mc/sf_considerationsrequirements/mc_virusscanningexclusionsexplained.htm  Quote: "could result in a disruption in the recording process or even corruption of databases"
  - Kind: rule of thumb
  - Level: core
  - Also: T13
  - Bias: fabricante de VMS

## T11 Windows Update y servicio
- a:N42. Las horas activas por defecto son de 8 a 17; Windows reinicia fuera de ellas; el rango máximo es de 18 horas. Para servidores, Microsoft sugiere la opción 7 de Configure Automatic Updates: avisar para instalar y avisar para reiniciar.
  - Source: https://learn.microsoft.com/en-us/windows/deployment/update/waas-restart  Quote: "For server devices, leverage Configure Automatic Updates options 7 - notify to install and notify to reboot."
  - Kind: rule of thumb
  - Level: core
- a:N43. Solo las sesiones RDP activas cuentan como usuario conectado: un equipo sin nadie logueado se reinicia. Varias políticas viejas de reinicio no aplican a Windows 11.
  - Source: https://learn.microsoft.com/en-us/windows/deployment/update/waas-restart  Quote: "Devices that don't have locally signed-in users, or active RDP sessions, are restarted."
  - Kind: mistake
  - Level: core
- a:N44. Bosch recomienda mantener actualizado el sistema operativo del VMS con un ciclo máximo de 6 meses y una actualización mayor cada dos años.
  - Source: https://knowledge.keenfinity-group.com/video-systems/article/what-is-the-recommendation-regarding-the-windows-u  Quote: "with a maximum update cycle of 6 months"
  - Kind: number
  - Level: core
  - Bias: fabricante de VMS
- a:N45. Noviembre 2024: servidores Windows Server 2022 amanecieron actualizados a 2025 sin licencia porque la API de Windows Update clasificó mal el upgrade (KB5044284) y herramientas de parches de terceros lo instalaron como actualización de seguridad. No había vuelta atrás simple: restaurar backup, reinstalar o comprar licencia.
  - Source: https://windowslatest.com/2024/11/06/windows-server-2022-auto-upgraded-to-windows-server-2025-due-to-api-error  Quote: "all of our Windows 2022 Servers had either upgraded themselves to 2025 overnight"
  - Kind: story
  - Level: core

## T12 Energía y arranque 24/7
- a:N46. powercfg /change con standby-timeout-ac, hibernate-timeout-ac, disk-timeout-ac y monitor-timeout-ac en 0 significa "nunca". powercfg /hibernate off desactiva hibernación y Fast Startup; powercfg /a lista estados de suspensión; /requests y /lastwake ayudan a diagnosticar.
  - Source: https://ss64.com/nt/powercfg.html  Quote: "Setting any value to 0 will set the timeout=Never"
  - Kind: technique
  - Level: foundation
- a:N47. Con Fast Startup activo, Wake on LAN puede fallar y las actualizaciones pueden no instalarse bien.
  - Source: https://ss64.com/nt/powercfg.html  Quote: "Wake-on-LAN may fail to work (or work reliably) when fast startup is enabled."
  - Kind: mistake
  - Level: core
- a:N48. BIOS "Restore on AC Power Loss": Last State vuelve a encender solo si estaba prendido; si una UPS lo apagó ordenadamente, no vuelve. Power On lo enciende siempre que vuelve la energía (contra: también enciende equipos que estaban apagados a propósito).
  - Source: https://www.servethehome.com/keeping-servers-bios-setup-availability/  Quote: "if a UPS has sent a shutdown signal to the server ... it will likely not come up"
  - Kind: story
  - Level: core

## T13 Discos y BitLocker
- a:N49. BitLocker pide la clave de recuperación ante cambios de hardware, BIOS, firmware, componentes de arranque o actualización de Windows; la clave no se puede guardar en el disco cifrado y si se pierde los datos no se recuperan, ni Microsoft puede.
  - Source: https://lazyadmin.nl/it/bitlocker-recovery-key/  Quote: "Even Microsoft support can't recover the key for you."
  - Kind: rule of thumb
  - Level: foundation
- a:N50. Antes de cambios de hardware o BIOS, suspender BitLocker, hacer el cambio y reanudar; la clave se puede guardar en cuenta Microsoft, Entra ID, Active Directory, archivo o impresa.
  - Source: https://lazyadmin.nl/it/bitlocker-recovery-key/  Quote: "first disable or suspend Bitlocker, make the changes, and then re-enable Bitlocker"
  - Kind: technique
  - Level: core

## T14 Cuentas y permisos
- a:N51. Windows LAPS genera una contraseña única y aleatoria para el administrador local de cada equipo unido a dominio y la guarda en AD o Entra ID; evita que una contraseña repetida permita saltar de equipo en equipo. Viene integrado en Windows 11 y Server 2019 a 2025 con updates de abril 2023; el LAPS heredado está deprecado.
  - Source: https://theitbros.com/enable-windows-laps-in-active-directory/  Quote: "mitigates the risk of lateral movement"
  - Kind: definition
  - Level: core
- a:N52. En Windows 11 24H2 y Server 2025, LAPS suma gestión automática de la cuenta, frases de contraseña y detección de rollback de imagen.
  - Source: https://learn.microsoft.com/en-us/windows-server/get-started/whats-new-windows-server-2025  Quote: "automatically generates unique passwords for each computer's local administrator account"
  - Kind: definition
  - Level: advanced
- a:N53. Ante NLA fallando en dominio, entrar con la cuenta de administrador local o por consola (iLO, iDRAC, consola de VM): por eso el admin local tiene que ser recuperable.
  - Source: https://theitbros.com/remote-computer-requires-network-level-authentication-nla/  Quote: "Log on to the RDP host remotely using the local administrator account"
  - Kind: technique
  - Level: core
  - Also: T06
- a:N54. Dar acceso RDP y permisos solo a quien lo necesita (mínimo privilegio).
  - Source: https://www.techtarget.com/cybersecurity/tip/10-RDP-security-best-practices-to-prevent-cyberattacks  Quote: "principle of least privilege"
  - Kind: rule of thumb
  - Level: foundation
  - Also: T06

## T15 Roles de Server
- a:N55. Install-WindowsFeature AD-Domain-Services -IncludeManagementTools e Install-ADDSForest crean el primer DC; el DNS se instala por defecto con el bosque. Cada cmdlet de despliegue tiene un Test- que solo verifica prerrequisitos. La contraseña DSRM no se escribe en texto plano.
  - Source: https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/install-active-directory-domain-services--level-100-  Quote: "The DNS server is installed by default when you run Install-ADDSForest."
  - Kind: technique
  - Level: advanced
- a:N56. DHCP en Server: instalar el rol (sin reinicio), autorizarlo en AD si hay dominio (un DHCP no autorizado no entrega direcciones), crear el ámbito con Add-DhcpServerv4Scope, opciones con Set-DhcpServerv4OptionValue (opción 6 DNS) y reservas por MAC con Add-DhcpServerv4Reservation.
  - Source: https://learn.microsoft.com/en-us/windows-server/networking/technologies/dhcp/quickstart-install-configure-dhcp-server  Quote: "Unauthorized DHCP servers that are installed in Active Directory domains can't function properly"
  - Kind: template
  - Level: core

## T16 Backups
- a:N57. wbadmin start backup con -backupTarget, -include, -allCritical (volúmenes críticos para restaurar el sistema) y -systemState; wbadmin get versions lista los backups; start systemstatebackup para el estado del sistema; -recreateDisks borra datos al restaurar.
  - Source: https://ss64.com/nt/wbadmin.html  Quote: "Include all critical volumes in the backups."
  - Kind: technique
  - Level: core
- a:N58. Ante el upgrade accidental a Server 2025 las opciones fueron restaurar desde backup, reconstruir o pagar licencia: el backup es la única marcha atrás real.
  - Source: https://windowslatest.com/2024/11/06/windows-server-2022-auto-upgraded-to-windows-server-2025-due-to-api-error  Quote: "restore servers from backups, rebuild them, or purchase new licenses"
  - Kind: story
  - Level: core
  - Also: T11

## Disagreements seen
- Cambiar el puerto 3389: v2cloud (https://v2cloud.com/tutorials/change-rdp-port) y TechTarget (https://www.techtarget.com/cybersecurity/tip/10-RDP-security-best-practices-to-prevent-cyberattacks) lo recomiendan como capa extra; woshub (https://woshub.com/manage-windows-firewall-powershell/) prefiere restringir por IP de origen en el firewall. El mismo TechTarget dice que RDP nunca debe quedar abierto a internet aunque se cambie el puerto.
- Actualizar o no los servidores de VMS: Bosch (https://knowledge.keenfinity-group.com/video-systems/article/what-is-the-recommendation-regarding-the-windows-u) pide actualizar con ciclo máximo de 6 meses; TechTarget recomienda actualizaciones automáticas; Microsoft (https://learn.microsoft.com/en-us/windows/deployment/update/waas-restart) sugiere para servidores avisar antes de instalar y reiniciar; el caso de Windows Latest muestra que la automatización ciega también rompe.
- nslookup vs Resolve-DnsName: el artículo del Networking Blog (https://www.elevenforum.com/t/resolve-dnsname-vs-nslookup-in-windows.43640/latest) prefiere Resolve-DnsName para reproducir aplicaciones pero rescata nslookup para aislar el resolvedor.
- pathping vs tracert: LazyAdmin (https://lazyadmin.nl/it/pathping-command/) dice que dejó tracert; Test-NetConnection -TraceRoute (https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection) ofrece traza integrada en PowerShell.
- BIOS Last State vs Power On: ServeTheHome (https://www.servethehome.com/keeping-servers-bios-setup-availability/) muestra que Last State falla tras apagado ordenado por UPS; Power On enciende también equipos apagados a propósito.

## Best stories
- Servidores 2022 que amanecieron en 2025 sin licencia por una mala etiqueta en la API de Windows Update (KB5044284): https://windowslatest.com/2024/11/06/windows-server-2022-auto-upgraded-to-windows-server-2025-due-to-api-error
- El NAS viejo que deja de abrir con Windows 11 24H2 por firma SMB obligatoria y fin del acceso invitado: https://www.theregister.com/2024/05/30/windows_11_24h2_security_tweaks/
- nslookup bing.com que consulta cuatro sufijos inventados antes del nombre real y da timeout: https://www.elevenforum.com/t/resolve-dnsname-vs-nslookup-in-windows.43640/latest
- El servidor que no vuelve después del corte porque la UPS lo apagó prolijo y el BIOS estaba en Last State: https://www.servethehome.com/keeping-servers-bios-setup-availability/
- Antivirus que bloquea archivos de la base de grabación y corta la grabación o corrompe la base: https://doc.milestonesys.com/2025R1/en-US/standard_features/sf_mc/sf_considerationsrequirements/mc_virusscanningexclusionsexplained.htm
