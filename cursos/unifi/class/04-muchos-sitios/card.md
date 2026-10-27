# Lección 4. Muchos sitios

**Escuchá:** muchos-sitios.mp3 (2 min)

**La idea, en tres líneas**
- Site Manager (unifi.ui.com) muestra todas las consolas y servidores que tu cuenta administra; la configuración sigue en cada controlador.
- Para aparecer, la consola necesita Remote Management activo y salida TCP 443 y 8883, DNS (UDP 53) y NTP (UDP 123). No hace falta abrir puertos de entrada.
- Para muchos clientes: Fabrics y MSP Groups ordenan administradores y roles; Blueprints con Drift Inspector (Network 10.6.101) muestran qué sitio se apartó de la plantilla.

**Impacto:** sabés qué sitios tenés, quién entra a cada uno y qué cambió, sin depender de la cuenta de un técnico.

**Quién lo dice:** 3 de 4 fuentes coinciden en que Site Manager conecta y no guarda configuración; la lista de puertos sale de una sola fuente (UniHosted, que cita el artículo oficial de Ubiquiti), así que conviene confirmarla en cada sitio.

**Laboratorio** · Admin · 10 min
1. En la consola o UniFi OS Server de laboratorio: Settings > Control Plane > Console, verificá que Remote Management esté activo y la consola asociada a la cuenta UI de la empresa.
2. Si no aparece en Site Manager, desde una PC de esa red probá la salida:
```powershell
Test-NetConnection unifi.ui.com -Port 443
Resolve-DnsName unifi.ui.com
```
y revisá en el firewall que estén permitidos TCP 443 y 8883, UDP 53 y UDP 123 de salida.
3. Entrá a unifi.ui.com con la cuenta de la empresa y confirmá que la consola figura con su versión.
4. Invitá a un compañero como administrador con rol limitado (por ejemplo solo ver, o solo ese sitio).
5. Abrí una planilla de sitios con una fila por cliente:
```text
Cliente | Host (UCG/UDM/CloudKey/UOS Server) | Versión UniFi OS | Versión Network | Dueño de la cuenta | Admins | Último backup
```
⚠️ Una consola de cliente asociada a la cuenta personal de un técnico se pierde el día que esa persona se va.

**Regla para quedarse**
Cada consola de cliente queda en la cuenta de la empresa y los técnicos entran como administradores con su rol.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Site Manager: qué hace, puertos y Fabrics: https://www.unihosted.com/blog/unifi-site-management
- Notas de Network 10.6.101, Blueprints y Drift Inspector: https://community.ui.com/releases/UniFi-Network-Application-10-6-101/05283624-0980-4dd7-b8d6-9fa5c4e28da4
