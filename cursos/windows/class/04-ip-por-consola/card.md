# Lección 4. IP por consola

**Escuchá:** ip-por-consola.mp3 (2 min)

**La idea, en tres líneas**
- IP fija de un servidor en cuatro pasos: ver la placa, limpiar IP y gateway viejos, asignar con New-NetIPAddress, poner el DNS aparte. Y verificar.
- New-NetIPAddress toma PrefixLength (24), no la máscara; si no se limpia la ruta vieja quedan dos gateways.
- El rol DHCP de Windows Server pide IP fija, se autoriza en Active Directory si hay dominio y reparte reservas por MAC para cámaras y controladoras.

**Impacto:** configuraciones repetibles, que se pegan en el informe de obra y funcionan igual en Server Core.

**Quién lo dice:** 2 de 2 fuentes coinciden (evidencia fina): la guía de OneUptime para IP estática y el quickstart de DHCP de Microsoft para Server 2025; no encontramos discrepancias.

**Laboratorio** · Foco · 15 min
En una VM, desde la consola de la VM (no por escritorio remoto), PowerShell como administrador:
1. Ver la placa:
```powershell
Get-NetAdapter | Select-Object Name, InterfaceIndex, Status, MacAddress
```
2. Limpiar y asignar (cambiá "Ethernet" por el nombre que viste):
```powershell
$if = 'Ethernet'
Remove-NetIPAddress -InterfaceAlias $if -AddressFamily IPv4 -Confirm:$false
Remove-NetRoute -InterfaceAlias $if -DestinationPrefix '0.0.0.0/0' -Confirm:$false
New-NetIPAddress -InterfaceAlias $if -IPAddress 10.10.10.20 -PrefixLength 24 -DefaultGateway 10.10.10.1
Set-DnsClientServerAddress -InterfaceAlias $if -ServerAddresses 10.10.10.1
```
3. Verificar:
```powershell
Get-NetIPAddress -InterfaceAlias $if -AddressFamily IPv4
Get-NetRoute -DestinationPrefix '0.0.0.0/0'
Get-DnsClientServerAddress -InterfaceAlias $if -AddressFamily IPv4
```
4. Volver a DHCP:
```powershell
Set-NetIPInterface -InterfaceAlias $if -Dhcp Enabled
Set-DnsClientServerAddress -InterfaceAlias $if -ResetServerAddresses
```
5. Opcional, en un Windows Server 2025 de prueba sin dominio:
```powershell
Install-WindowsFeature DHCP -IncludeManagementTools
Add-DhcpServerv4Scope -Name 'Lab CCTV' -StartRange 10.10.10.100 -EndRange 10.10.10.200 -SubnetMask 255.255.255.0
Set-DhcpServerv4OptionValue -ScopeId 10.10.10.0 -Router 10.10.10.1 -DnsServer 10.10.10.20 -Force
Add-DhcpServerv4Reservation -ScopeId 10.10.10.0 -IPAddress 10.10.10.150 -ClientId '00-11-22-33-44-55' -Description 'Camara acceso'
```
Si hay dominio, falta autorizarlo con `Add-DhcpServerInDC`.

⚠️ Cambiar la IP por escritorio remoto te desconecta. Y un DHCP de laboratorio conectado a la red del cliente puede repartir direcciones: hacelo en una red aislada.

**Regla para quedarse**
La IP de un servidor se pone por consola, se verifica y se documenta.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- IP estática con New-NetIPAddress paso a paso: https://oneuptime.com/blog/post/2026-03-20-set-static-ipv4-powershell-new-netipaddress/view
- Instalar y configurar DHCP en Windows Server: https://learn.microsoft.com/en-us/windows-server/networking/technologies/dhcp/quickstart-install-configure-dhcp-server
