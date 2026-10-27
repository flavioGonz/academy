# Lección 6. RDP sin exponer

**Escuchá:** rdp-sin-exponer.mp3 (2 min)

**La idea, en tres líneas**
- El 3389 nunca abierto a internet: acceso remoto por VPN o gateway de RDP, y adentro la regla limitada a la subred de gestión.
- NLA autentica antes de abrir la sesión y viene activada; cambiar el puerto solo baja el ruido de los escaneos.
- El error "requiere NLA" casi siempre es DNS, controlador de dominio, relación de confianza u hora; y conectar por IP en vez de nombre rompe Kerberos.

**Impacto:** el servidor del VMS deja de ser la puerta de entrada de un ransomware.

**Quién lo dice:** 2 de 4 fuentes coinciden en lo central (TechTarget y woshub, con TheITBros en NLA); V2 Cloud discrepa en parte y suma cambiar el puerto como capa extra, pero ninguna defiende exponer el 3389.

**Laboratorio** · Foco · 15 min
En una VM con escritorio remoto habilitado, PowerShell como administrador:
1. ¿NLA activa? (1 es sí)
```powershell
(Get-CimInstance -ClassName Win32_TSGeneralSetting -Namespace root\cimv2\terminalservices `
  -Filter "TerminalName='RDP-tcp'").UserAuthenticationRequired
```
En Windows 11 también se ve en Configuración > Sistema > Escritorio remoto.
2. Qué reglas de RDP hay y desde dónde aceptan:
```powershell
Get-NetFirewallRule -DisplayGroup 'Remote Desktop' -ErrorAction SilentlyContinue |
  Select-Object DisplayName, Enabled, Profile
```
(En Windows en español el grupo puede figurar como 'Escritorio remoto'.)
3. Limitar las reglas de RDP a la subred de gestión del laboratorio (ejemplo 10.10.10.0/24):
```powershell
Get-NetFirewallRule -DisplayGroup 'Remote Desktop' |
  Set-NetFirewallRule -RemoteAddress 10.10.10.0/24
```
4. Desde un equipo de esa subred, `Test-NetConnection IP -CommonTCPPort RDP` da True; desde otra subred, False.
5. Revisá en el router del laboratorio que no exista ningún reenvío de puerto al 3389.

⚠️ Si tocás estas reglas por escritorio remoto desde fuera de la subred elegida, te cortás. Hacelo por consola o desde la subred de gestión.

**Regla para quedarse**
RDP solo por VPN, con NLA y desde la subred de gestión.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Diez prácticas de seguridad para RDP: https://www.techtarget.com/cybersecurity/tip/10-RDP-security-best-practices-to-prevent-cyberattacks
- Errores de NLA y cómo encontrar la causa: https://theitbros.com/remote-computer-requires-network-level-authentication-nla/
- Cambiar el puerto de RDP y sus límites: https://v2cloud.com/tutorials/change-rdp-port
