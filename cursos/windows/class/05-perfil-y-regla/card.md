# Lección 5. Perfil y regla

**Escuchá:** perfil-y-regla.mp3 (2 min)

**La idea, en tres líneas**
- Cada placa cae en un perfil (Dominio, Privado, Público) y una regla solo actúa cuando su perfil está activo.
- Se abre por puerto o por programa, y con origen limitado (LocalSubnet o IP concretas), nunca "todo a todos".
- Antes de tocar, se exporta la configuración; para ver qué abre una regla hay que pedir sus filtros.

**Impacto:** reglas que funcionan a la primera y un firewall que queda encendido después de la puesta en marcha.

**Quién lo dice:** 3 de 5 fuentes coinciden (documentación de Microsoft, woshub, TheITBros); nadie discrepa.

**Laboratorio** · Foco · 15 min
En una VM, PowerShell como administrador:
1. Perfil de cada placa y estado del firewall:
```powershell
Get-NetConnectionProfile | Select-Object InterfaceAlias, NetworkCategory
Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction
```
2. Respaldo antes de tocar:
```powershell
New-Item -ItemType Directory C:\Lab -Force
netsh advfirewall export "C:\Lab\firewall-antes.wfw"
```
3. Si la red de laboratorio quedó como Pública y es una red tuya, pasala a Privada:
```powershell
Set-NetConnectionProfile -InterfaceAlias 'Ethernet' -NetworkCategory Private
```
4. Regla por puerto, solo desde la subred local y solo en perfiles Privado y Dominio:
```powershell
New-NetFirewallRule -DisplayName 'LAB VMS web 8443' -Direction Inbound -Action Allow `
  -Protocol TCP -LocalPort 8443 -RemoteAddress LocalSubnet -Profile Private,Domain
```
5. Ver qué abre de verdad:
```powershell
Get-NetFirewallRule -DisplayName 'LAB VMS web 8443' | Get-NetFirewallPortFilter
Get-NetFirewallRule -DisplayName 'LAB VMS web 8443' | Get-NetFirewallAddressFilter
```
6. Probar desde otro equipo con `Test-NetConnection IP -Port 8443` (con algo escuchando en ese puerto) y después borrar la regla:
```powershell
Remove-NetFirewallRule -DisplayName 'LAB VMS web 8443'
```
Para una regla por programa, el parámetro es `-Program` con la ruta completa del ejecutable.

⚠️ `netsh advfirewall reset` borra todas las reglas propias; en producción, solo con el export a mano.

**Regla para quedarse**
Perfil primero, regla después, y siempre con origen limitado.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Firewall de Windows con PowerShell, perfiles y respaldo: https://woshub.com/manage-windows-firewall-powershell/
- Referencia de New-NetFirewallRule (en español): https://learn.microsoft.com/es-es/powershell/module/netsecurity/new-netfirewallrule
