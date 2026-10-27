# Lección 2. Servidor a medida

**Escuchá:** servidor-a-medida.mp3 (2 min)

**La idea, en tres líneas**
- Dimensioná el SYS con la guía oficial: perfil bajo i5-8500, 8 GB de RAM, NIC gigabit y 650 GB de disco; para cargas altas, Xeon E-2314 o E-2378 con 16 GB (recomiendan 32 GB).
- Instalá como administrador: modo típico (todo menos Streaming Server) para un servidor, personalizado para separar módulos.
- El Service Manager muestra cada servicio y su puerto; un puerto en rojo es un conflicto con otro proceso.

**Impacto:** menos servidores que se arrastran a los seis meses y menos instalaciones que fallan por un puerto tomado.

**Quién lo dice:** 2 de 4 fuentes dan cifras concretas, ambas de Hikvision (guía de requisitos V2.4.510 y FAQ); discrepa VXG, un competidor de nube: el costo real está en operar y mantener el servidor. Para V3.x, confirmá las cifras en la guía de requisitos de esa versión.

**Laboratorio** · Foco · 20 min
1. Creá una VM de laboratorio con Windows Server, 4 vCPU, 8 GB de RAM y un disco de sistema amplio. IP de ejemplo: 192.168.88.10/24.
2. Verificá el instalador antes de correrlo y compará con el valor publicado en la página de descarga:
```powershell
Get-FileHash .\HikCentral_Professional.exe -Algorithm MD5
```
3. Clic derecho > Ejecutar como administrador > aceptar licencia > instalación típica > Install Now. Si el asistente pide reiniciar, reiniciá.
4. Abrí Service Manager como administrador y confirmá que todos los servicios estén en verde.
5. Si un puerto aparece en rojo, buscá quién lo ocupa:
```powershell
netstat -ano | findstr :80
tasklist | findstr 4321
```
(4321 es el PID que devolvió netstat.) Con autorización del cliente cerrás ese proceso, o cambiás el puerto del servicio en Service Manager y en el navegador entrás a 192.168.88.10:81.

⚠️ Cerrar procesos en un servidor del cliente puede cortar otro servicio: pedí permiso antes.

**Regla para quedarse**
Instalador verificado, permisos de administrador y el Control Client nunca en una VM.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Perfiles de hardware, sistemas operativos y virtualización (guía de requisitos V2.4.510): https://pinfo.hikvision.com/hkwsen/unzip/20230911113613_29615_doc/HikCentral%20Professional_System%20Requirements%20and%20Performance_V2.4.510_20230907.pdf
- Paquetes, modos de instalación y Service Manager (Quick Start Guide): https://pinfo.hikvision.com/hkwsen/unzip/20230911113416_60121_doc/pdf.pdf
- La mirada crítica sobre el costo de operar on-premises: https://www.videoexpertsgroup.com/glossary/hikcentral-professional
