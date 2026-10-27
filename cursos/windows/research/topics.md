# Mapa del tema: Windows para técnicos de campo (cliente y Server)

Nivel: inicial a intermedio. Público: técnicos instaladores y de soporte de seguridad electrónica que montan servidores de VMS, controladoras de acceso y puestos de monitoreo sobre Windows 11 y Windows Server 2025.

Cómo se enseña (lo que se miró): el temario del examen AZ-800 (Windows Server Hybrid Administrator: AD DS, DNS, DHCP, redes, almacenamiento, servicios), las guías de post-instalación de Microsoft Learn (sconfig, IP, actualizaciones), la referencia de comandos de Windows (ipconfig, pathping, tracert, netsh, manage-bde, wbadmin, sc, schtasks), la documentación de PowerShell (NetTCPIP, NetSecurity, DnsClient, ScheduledTasks) y las guías de "mejores prácticas de Windows" de fabricantes de VMS (Milestone, Genetec, Bosch BVMS). El orden típico: instalación y versión, red, firewall, acceso remoto, servicios y tareas, logs y rendimiento, actualizaciones, almacenamiento, identidad, roles de Server, backup.

- T01 Versiones y canales vigentes: Windows 11 (24H2/25H2), Windows Server 2025, ediciones, LTSC, ciclo de vida, qué cambió en 2025.
- T02 Diagnóstico de red básico: ipconfig, ping, tracert, pathping, arp. Leer la salida y ubicar el fallo por capas.
- T03 Diagnóstico de puertos y DNS: Test-NetConnection, nslookup y Resolve-DnsName, netstat y Get-NetTCPConnection, qué proceso escucha un puerto.
- T04 Configurar IP por PowerShell: New-NetIPAddress, Set-DnsClientServerAddress, Remove-NetIPAddress, volver a DHCP, varias IP en una placa.
- T05 Firewall de Windows: perfiles (Dominio, Privado, Público), reglas por puerto y por programa, New-NetFirewallRule, netsh advfirewall, categoría de red.
- T06 Escritorio remoto seguro: RDP, NLA, no exponer el 3389, VPN o gateway, cambiar puerto, bloqueo de fuerza bruta, MFA.
- T07 Servicios: tipos de inicio, inicio retrasado, recuperación ante fallas (sc failure), cuentas de servicio, dependencias.
- T08 Tareas programadas: Register-ScheduledTask, disparadores al inicio, correr como SYSTEM, sin sesión iniciada, errores típicos.
- T09 Visor de eventos y Monitor de confiabilidad: logs System/Application, IDs clave (41, 6008, 1074, 7031/7034), Get-WinEvent, perfmon /rel.
- T10 Rendimiento: Administrador de tareas, Monitor de recursos, perfmon y contadores (disco, CPU, memoria), typeperf/logman, IOPS y latencia de disco para grabación.
- T11 Windows Update y servicio: horas activas, reinicios forzados, políticas, pausas, PSWindowsUpdate, sconfig, riesgos de actualizaciones (caso Server 2025 instalado solo), validación con el fabricante del VMS.
- T12 Energía y arranque para equipos 24/7: plan de energía, suspensión y disco, powercfg, BIOS "restore on AC power loss", arranque automático tras corte, UPS.
- T13 Discos y BitLocker: estado, protectores, clave de recuperación (dónde guardarla), BitLocker en servidores de grabación, TPM, exclusiones de antivirus para carpetas de video.
- T14 Cuentas y permisos: local vs dominio, UAC, administrador local, LAPS, mínimo privilegio, cuentas de servicio.
- T15 Roles de Server: nociones de Active Directory (bosque, dominio, DC), DNS y DHCP en Windows Server, reservas, puertos de DC.
- T16 Backups: Windows Server Backup y wbadmin, estado del sistema, backup de configuración del VMS, regla de probar la restauración.
