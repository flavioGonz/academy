# Lección 3. Probá el puerto

**Escuchá:** proba-el-puerto.mp3 (2 min)

**La idea, en tres líneas**
- El ping dice que hay alguien; Test-NetConnection con el puerto dice si el servicio atiende.
- Get-NetTCPConnection muestra qué proceso escucha un puerto y en qué placa (0.0.0.0 es en todas).
- Resolve-DnsName usa el resolvedor de Windows como las aplicaciones; nslookup consulta solo al servidor DNS y agrega sufijos a nombres sin punto final.

**Impacto:** en una alta de cámaras o un VMS que "no se ve", separás en minutos red, servicio y nombre.

**Quién lo dice:** 3 de 5 fuentes coinciden en probar el puerto concreto (Microsoft, Adam the Automator, V2 Cloud); lo de nslookup y Resolve-DnsName sale de una sola fuente, el blog de redes de Microsoft, que igual rescata nslookup para aislar fallas del resolvedor.

**Laboratorio** · Foco · 15 min
En una VM con Windows 11 o Server 2025, PowerShell como administrador:
1. Un puerto que debería estar abierto y uno cerrado:
```powershell
Test-NetConnection 192.168.88.20 -Port 554
Test-NetConnection 192.168.88.20 -Port 8443 -InformationLevel Quiet
Test-NetConnection 192.168.88.10 -CommonTCPPort RDP
```
Mirá `TcpTestSucceeded`: True o False.
2. Qué escucha en tu equipo y quién es:
```powershell
Get-NetTCPConnection -State Listen |
  Sort-Object LocalPort |
  Select-Object LocalAddress, LocalPort, OwningProcess
Get-Process -Id (Get-NetTCPConnection -State Listen -LocalPort 135).OwningProcess
```
3. Lo mismo a la vieja usanza, para comparar:
```text
netstat -ano | findstr LISTENING
```
4. DNS: compará las dos herramientas.
```powershell
Resolve-DnsName learn.microsoft.com
Resolve-DnsName learn.microsoft.com -DnsOnly -Server 1.1.1.1
nslookup learn.microsoft.com. 1.1.1.1
```
5. Agregá una línea `192.168.88.50 vms-lab` al archivo hosts (como administrador, en `C:\Windows\System32\drivers\etc\hosts`) y probá `Resolve-DnsName vms-lab` contra `nslookup vms-lab`. El primero la encuentra, el segundo no. Después borrá la línea.

**Regla para quedarse**
No digo "no hay red" hasta probar el puerto exacto del servicio.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Test-NetConnection en la documentación oficial: https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection
- Puertos en escucha con netstat y PowerShell: https://adamtheautomator.com/netstat-port/
- Resolve-DnsName contra nslookup (blog de redes de Microsoft): https://www.elevenforum.com/t/resolve-dnsname-vs-nslookup-in-windows.43640/latest
