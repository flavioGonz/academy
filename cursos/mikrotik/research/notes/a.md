# Notes: batch a (documentación y avisos oficiales de MikroTik)
Pages read: 13. With notes: 13. Skipped: 0.

Páginas: manual.mikrotik.com 7.25 (securing, first-time-configuration, bridge-vlan-table, nat, cloud, torch), help.mikrotik.com congelado (Failover WAN Backup, Building Advanced Firewall, Configuration Management, Upgrading and installation, RouterBOOT, WireGuard) y mikrotik.com/supportsec (Mēris).

## T01 Acceso inicial y herramientas de gestión
- a:N1. Conectar la PC a cualquier puerto menos ether1 (ether1 es WAN por defecto), abrir WinBox, pestaña Neighbors, y conectarse por la MAC si la IP no responde o figura 0.0.0.0. Usuario admin, contraseña vacía o la de la etiqueta del equipo.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration  Quote: "Prefer the MAC address if the IP address is not reachable or shows 0.0.0.0"
  - Kind: technique
  - Level: foundation
- a:N2. Algunos equipos profesionales (serie CCR) vienen con configuración mínima o sin configuración por defecto: ahí hay que armar a mano bridge, IP de LAN y DHCP antes de seguir.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration  Quote: "some professional devices (such as the CCR series) may ship with a minimal or no default configuration"
  - Kind: rule of thumb
  - Level: foundation
  - Also: T02
- a:N3. Safe Mode: botón en WinBox, o Ctrl+X (o F4) en la CLI. Si la sesión se corta mientras está activo, el router deshace todos los cambios hechos en safe mode (tras el timeout TCP de unos 9 minutos). El historial guarda hasta 100 acciones; si se pasa, sale de safe mode sin deshacer nada, así que conviene trabajar en pasos chicos.
  - Source: https://help.mikrotik.com/docs/spaces/ROS/pages/328155/Configuration+Management  Quote: "it is best to change the configuration in small steps, while in safe mode"
  - Kind: technique
  - Level: foundation
  - Also: T13
- a:N4. Cada acción en GUI o CLI queda en /system history y se puede deshacer con /undo y /redo, incluso las hechas desde WinBox.
  - Source: https://help.mikrotik.com/docs/spaces/ROS/pages/328155/Configuration+Management  Quote: "You can undo or redo any action"
  - Kind: technique
  - Level: foundation
  - Also: T13

## T02 Configuración por defecto, reset y Netinstall
- a:N5. Para principiantes MikroTik recomienda conservar la configuración por defecto (firewall básico, DHCP, seguridad wireless) y personalizarla. Borrarla quita todas las reglas de seguridad y solo se recomienda a usuarios avanzados que configuran a mano.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration  Quote: "Removing the default configuration removes all built-in security rules and services"
  - Kind: rule of thumb
  - Level: foundation
- a:N6. /system reset-configuration acepta keep-users, no-defaults (deja el equipo vacío), skip-backup y run-after-reset (ejecuta un .rsc después del reset). Antes del reset el router guarda un backup automático, salvo skip-backup.
  - Source: https://help.mikrotik.com/docs/spaces/ROS/pages/328155/Configuration+Management  Quote: "The backup file of the existing configuration is stored before reset"
  - Kind: technique
  - Level: core
- a:N7. Botón de reset en RouterBOARD: mantenerlo al arrancar hasta que el LED titila (unos 5 s) resetea la configuración; 5 s más con LED fijo activa modo CAP; 5 s más hasta que se apaga busca un servidor Netinstall. Si se aprieta antes de dar energía, además usa el RouterBOOT de respaldo.
  - Source: https://help.mikrotik.com/docs/display/ROS/RouterBOOT  Quote: "release the button to reset the RouterOS configuration (total 5 seconds)"
  - Kind: technique
  - Level: core
  - Also: T14
- a:N8. Netinstall reinstala RouterOS cuando la instalación falló, se dañó o se perdieron las contraseñas; requiere conexión Ethernet directa y arranque por red (PXE), que se puede activar con el botón de reset.
  - Source: https://help.mikrotik.com/docs/spaces/ROS/pages/328142/Upgrading+and+installation  Quote: "where access passwords have been lost"
  - Kind: technique
  - Level: core
  - Also: T14
- a:N9. La contraseña perdida no se recupera: hay que resetear o reinstalar.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration  Quote: "If it is lost, there is no recovery option"
  - Kind: rule of thumb
  - Level: foundation
  - Also: T03

## T03 Usuarios, grupos y contraseñas
- a:N10. Crear un usuario propio con grupo full, verificar que entra, y recién ahí deshabilitar o borrar admin. Contraseña de 12 caracteres o más, con mayúsculas, minúsculas, números y símbolos.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration  Quote: "verify it works, and then disable or remove the default admin account"
  - Kind: technique
  - Level: foundation
- a:N11. Una cuenta por administrador en lugar de compartir admin, y grupos propios con las políticas justas: el grupo read que viene de fábrica puede reiniciar el router y ver configuración sensible. Con clave SSH asignada a un usuario, se deshabilita su login SSH por contraseña.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router  Quote: "the built-in read group can reboot the router and see sensitive configuration"
  - Kind: rule of thumb
  - Level: core
- a:N12. Una cuenta se puede limitar a direcciones de origen con la propiedad address (por ejemplo /user/set 0 address=192.168.88.0/24).
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router  Quote: "limit a specific user account to certain source addresses"
  - Kind: technique
  - Level: core
  - Also: T04
- a:N13. En una contraseña entre comillas, el signo $ sin escapar inicia una variable y la contraseña queda más corta sin aviso.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router  Quote: "the password silently ends up shorter"
  - Kind: mistake
  - Level: core

## T04 Servicios IP y superficie de ataque
- a:N14. No exponer servicios de gestión (WinBox, SSH) a internet: se escanean y atacan de forma automática (fuerza bruta, explotación de versiones viejas, compromiso total). Para acceso remoto, una VPN como WireGuard.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router  Quote: "use a VPN such as WireGuard"
  - Kind: rule of thumb
  - Level: foundation
  - Also: T11
- a:N15. Deshabilitar servicios no usados: /ip/service/disable telnet,ftp,www,api. available-from limita por origen, pero MikroTik prefiere el firewall porque corta la conexión antes de llegar al servicio.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router  Quote: "enforcing access control with firewall rules (above) is preferred"
  - Kind: technique
  - Level: foundation
- a:N16. En producción, cerrar MAC-Telnet, MAC-WinBox y MAC-Ping (/tool/mac-server ... allowed-interface-list=none), Neighbor Discovery, bandwidth server, proxy, SOCKS y UPnP; DNS con allow-remote-requests=no si el router no tiene que resolver para otros.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router  Quote: "should be disabled in production networks"
  - Kind: technique
  - Level: core
- a:N17. Si no hay más remedio que abrir gestión desde WAN, en un router con defconf las reglas accept van antes de "drop all not coming from LAN" (place-before), restringidas por origen, con protección de fuerza bruta y RouterOS al día.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router  Quote: "add only the accept rules for the services you need, in front of that rule"
  - Kind: technique
  - Level: advanced
  - Also: T08
- a:N18. ssh strong-crypto=yes deja de ofrecer cifrados y MAC débiles. Cambiar el puerto SSH (ej. 2200) reduce intentos automáticos.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router  Quote: "can reduce exposure to automated brute-force attempts"
  - Kind: technique
  - Level: core
- a:N19. Mēris: MikroTik dice que no hubo vulnerabilidad nueva; los atacantes usaron routers comprometidos en 2018 y los reconfiguraron con funciones propias de RouterOS. Actualizar no alcanza si robaron la contraseña en 2018: hay que cambiarla, revisar firewall y buscar scripts propios.
  - Source: https://mikrotik.com/supportsec/meris-botnet  Quote: "If somebody got your password in 2018, just an upgrade will not help"
  - Kind: story
  - Level: foundation
  - Also: T14
- a:N20. Qué buscar en un equipo sospechoso: reglas del Scheduler que ejecutan fetch, SOCKS habilitado, un cliente L2TP llamado "lvpn" o desconocido, y una regla de input que permite el puerto 5678. Tampoco confiar en la LAN: hay malware en PCs Windows que intenta reconfigurar el router desde adentro.
  - Source: https://mikrotik.com/supportsec/meris-botnet  Quote: "Don't assume your local network can be trusted"
  - Kind: test
  - Level: core

## T05 Interfaces, bridge e interface lists
- a:N21. Usar interface lists WAN y LAN (la defconf ya las trae) para que NAT y firewall no dependan del nombre de una interfaz; si el WAN pasa a PPPoE o LTE hay que agregar esa interfaz a la lista WAN.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration  Quote: "interface lists can be used for more flexible configuration"
  - Kind: technique
  - Level: foundation
  - Also: T07
- a:N22. Toda interfaz wireless que deba dar LAN tiene que estar en el bridge; si no, los clientes asocian pero no reciben DHCP ni llegan a la red.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration  Quote: "wireless clients will not receive DHCP addresses"
  - Kind: mistake
  - Level: foundation
- a:N23. Deshabilitar interfaces Ethernet/SFP que no se usan reduce la superficie de acceso.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router  Quote: "disable all unused interfaces"
  - Kind: rule of thumb
  - Level: foundation
  - Also: T04

## T06 Direccionamiento, DHCP y DNS
- a:N24. WAN por DHCP: /ip/dhcp-client/add interface=ether1 y verificar status bound. WAN estática: /ip/address + /ip/route gateway + /ip/dns servers. PPPoE: la interfaz WAN pasa a ser pppoe-out1 y todo lo de WAN se configura sobre ella.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration  Quote: "the WAN interface becomes pppoe-out1 instead of ether1"
  - Kind: technique
  - Level: foundation
  - Also: T05
- a:N25. Verificación en dos pasos: ping a una IP pública (8.8.8.8) y después a un nombre. Si la IP responde y el nombre no, el problema es DNS.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration  Quote: "If the IP ping succeeds but the domain ping fails"
  - Kind: test
  - Level: foundation
  - Also: T15
- a:N26. Con VLANs, cada VLAN lleva su propio servidor DHCP y su propio rango, lo que facilita firewall y QoS.
  - Source: https://manual.mikrotik.com/docs/7.25/bridging-and-switching/user-guides/bridge-vlan-table  Quote: "you can use different DHCP Servers"
  - Kind: rule of thumb
  - Level: core
  - Also: T09

## T07 NAT
- a:N27. NAT solo evalúa el primer paquete de la conexión; connection tracking recuerda la acción. Al cambiar reglas NAT conviene limpiar la tabla de conexiones o la regla parece no funcionar hasta que vence la entrada.
  - Source: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat  Quote: "the connection tracking table should be cleared"
  - Kind: mistake
  - Level: core
- a:N28. Masquerade es para IP pública dinámica (DHCP, PPPoE): al caer la interfaz limpia las conexiones enmascaradas. Con IP fija, src-nat. Con dos uplinks inestables pueden filtrarse IPs privadas; se mitiga con una ruta blackhole.
  - Source: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat  Quote: "when public IP is dynamic"
  - Kind: rule of thumb
  - Level: core
  - Also: T10
- a:N29. Hairpin NAT: si un equipo de la LAN entra al servidor por la IP pública, el servidor contesta directo y el cliente descarta la respuesta. Se arregla con un masquerade en srcnat desde la LAN hacia el servidor.
  - Source: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat  Quote: "it discards it because it expects a packet back from 172.16.16.1"
  - Kind: technique
  - Level: advanced
  - Also: T16
- a:N30. Un dst-nat se puede restringir con src-address a la IP pública de quien tiene que entrar; la documentación lo llama "más seguro".
  - Source: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat  Quote: "It is also considered to be more secure!"
  - Kind: technique
  - Level: core
  - Also: T16
- a:N31. Detrás de CGNAT (100.64.0.0/10) no hay port forwarding posible: nada que requiera conexiones entrantes funciona.
  - Source: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat  Quote: "CGNAT makes this impossible"
  - Kind: rule of thumb
  - Level: core
  - Also: T16
- a:N32. Ejemplo oficial de port forwarding: dst-nat de TCP 3389 a 192.168.88.254 sin filtro de origen, con la nota de que si hay firewall estricto hay que permitirlo en forward.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration  Quote: "must be allowed in the firewall filter forward chain"
  - Kind: technique
  - Level: foundation
  - Also: T16

## T08 Firewall filter
- a:N33. Estructura del firewall base de MikroTik: en input aceptar established, related, untracked, aceptar ICMP y descartar todo lo que no venga de LAN; en forward, fasttrack, aceptar established y related, descartar invalid y descartar lo que entra por WAN sin dst-nat.
  - Source: https://help.mikrotik.com/docs/spaces/ROS/pages/328513/Building+Advanced+Firewall  Quote: "dropping everything else not coming from LAN to fully protect the router"
  - Kind: template
  - Level: foundation
- a:N34. Address-lists para agrupar direcciones (no_forward_ipv4, bad_ipv4, not_global_ipv4) y referirse a ellas desde reglas; la regla queda corta y la lista se edita sin tocarla.
  - Source: https://help.mikrotik.com/docs/spaces/ROS/pages/328513/Building+Advanced+Firewall  Quote: "create a necessary address-list"
  - Kind: technique
  - Level: core
  - Also: T16
- a:N35. Si hay túneles IPsec, habilitar la regla que acepta lo que coincide con la política IPsec antes de fasttrack, y excluir ese tráfico del masquerade.
  - Source: https://help.mikrotik.com/docs/spaces/ROS/pages/328513/Building+Advanced+Firewall  Quote: "It is very important that IPsec encapsulated traffic bypass fast-track"
  - Kind: mistake
  - Level: advanced
  - Also: T11
- a:N36. No desactivar las reglas existentes del firewall por defecto; solo agregar las necesarias.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration  Quote: "Do not disable the existing rules; only add new ones if required"
  - Kind: rule of thumb
  - Level: foundation

## T09 VLANs con bridge vlan-filtering
- a:N37. Orden seguro: crear bridge, agregar puertos con PVID, cargar la tabla /interface/bridge/vlan, configurar el acceso de gestión y recién al final vlan-filtering=yes. Activarlo antes puede dejarte afuera. Recomiendan consola serial o un puerto fuera del bridge.
  - Source: https://manual.mikrotik.com/docs/7.25/bridging-and-switching/user-guides/bridge-vlan-table  Quote: "Don't enable VLAN filtering yet as you might get locked out"
  - Kind: technique
  - Level: core
- a:N38. No poner varios VLAN IDs en una entrada con puertos access como untagged: deja pasar ambas VLAN por ambos puertos. Varias VLAN por entrada solo para trunks.
  - Source: https://manual.mikrotik.com/docs/7.25/bridging-and-switching/user-guides/bridge-vlan-table  Quote: "Do NOT use multiple VLAN IDs on access ports"
  - Kind: mistake
  - Level: core
- a:N39. El bridge es también un puerto (puerto CPU). Si el trunk y el bridge comparten PVID 1, queda acceso al router por tráfico sin etiqueta desde el trunk. Revisar la tabla VLAN buscando accesos no previstos.
  - Source: https://manual.mikrotik.com/docs/7.25/bridging-and-switching/user-guides/bridge-vlan-table  Quote: "Always check the bridge VLAN table"
  - Kind: mistake
  - Level: advanced
- a:N40. ingress-filtering=yes con frame-types: admit-only-vlan-tagged en trunks y admit-only-untagged-and-priority-tagged en access. frame-types sin ingress-filtering no tiene efecto. "Usá ingress-filtering siempre que puedas".
  - Source: https://manual.mikrotik.com/docs/7.25/bridging-and-switching/user-guides/bridge-vlan-table  Quote: "Always try to use ingress-filtering wherever it is possible"
  - Kind: technique
  - Level: core
- a:N41. Gestión por una VLAN dedicada (ej. 99) en lugar de tráfico sin etiqueta: el atacante tiene que adivinar el VLAN ID y además las credenciales. Mejor acceder desde el trunk y no desde puertos access.
  - Source: https://manual.mikrotik.com/docs/7.25/bridging-and-switching/user-guides/bridge-vlan-table  Quote: "A much better way is to allow access to the device using a very specific VLAN"
  - Kind: rule of thumb
  - Level: core

## T10 Multi-WAN y failover
- a:N42. Failover con rutas recursivas: rutas /32 a dos hosts testigo (ej. 8.8.8.8 por ISP1, 8.8.4.4 por ISP2) con scope=10, y defaults con gateway=host testigo, target-scope=11, check-gateway=ping, distance 1 y 2. Así se detecta la caída de internet aguas arriba, no solo del módem.
  - Source: https://help.mikrotik.com/docs/spaces/ROS/pages/26476608/Failover+WAN+Backup  Quote: "Recursive routing occurs when a route ... has a next-hop that is not directly connected"
  - Kind: template
  - Level: advanced
- a:N43. Un solo testigo por enlace es frágil; se agrega un segundo par de testigos por enlace y el cambio total al segundo ISP ocurre solo cuando todos son inalcanzables.
  - Source: https://help.mikrotik.com/docs/spaces/ROS/pages/26476608/Failover+WAN+Backup  Quote: "Complete switchover to second link will happen only if all the gateways become unreachable"
  - Kind: technique
  - Level: advanced
- a:N44. Con dos WAN hace falta masquerade en ambas salidas.
  - Source: https://help.mikrotik.com/docs/spaces/ROS/pages/26476608/Failover+WAN+Backup  Quote: "we need to masquerade LAN traffic on both uplinks"
  - Kind: rule of thumb
  - Level: core
  - Also: T07

## T11 VPN para gestión remota
- a:N45. WireGuard en RouterOS 7: /interface/wireguard add (puerto por defecto 13231, MTU 1420), IP en la interfaz, peer con la clave pública del cliente y allowed-address /32. El firewall por defecto bloquea el túnel: aceptar UDP 13231 en input antes de los drops, y sumar la interfaz wireguard a la lista LAN si los clientes deben llegar a servicios del router.
  - Source: https://help.mikrotik.com/docs/spaces/ROS/pages/69664792/WireGuard  Quote: "The default RouterOS firewall will block the tunnel from establishing properly"
  - Kind: template
  - Level: core
- a:N46. persistent-keepalive (ej. 25 s) mantiene viva la entrada NAT cuando un extremo está detrás de NAT y casi no manda tráfico. Desde 7.21 el peer puede generar la configuración del cliente con código QR (show-client-config).
  - Source: https://help.mikrotik.com/docs/spaces/ROS/pages/69664792/WireGuard  Quote: "might benefit from having a persistent keepalive interval of 25 seconds"
  - Kind: technique
  - Level: core
- a:N47. El aviso de Mēris sugiere, si hace falta acceso remoto, abrir solo un servicio VPN seguro como IPsec en lugar de exponer el equipo.
  - Source: https://mikrotik.com/supportsec/meris-botnet  Quote: "only open a secure VPN service, like IPsec"
  - Kind: rule of thumb
  - Level: foundation
  - Also: T04

## T12 IP Cloud y DDNS
- a:N48. /ip/cloud/set ddns-enabled=yes da un nombre <serie>.sn.mynetname.net que sigue la IP pública (TTL 60 s; detrás de NAT actualiza cada minuto). El router consulta a cloud2.mikrotik.com por UDP 15252.
  - Source: https://manual.mikrotik.com/docs/7.25/network-management/cloud/  Quote: "a DNS name under sn.mynetname.net that follows its public IP address"
  - Kind: definition
  - Level: core
- a:N49. El nombre DDNS no abre ningún acceso: el firewall por defecto sigue bloqueando. Para entrar se usa Back To Home (WireGuard por relays de MikroTik, funciona sin IP pública) o reglas explícitas.
  - Source: https://manual.mikrotik.com/docs/7.25/network-management/cloud/  Quote: "The name only makes the router easier to find. It does not open any access"
  - Kind: rule of thumb
  - Level: core
  - Also: T11
- a:N50. La guía de hardening sugiere ddns-enabled=auto (DDNS solo activo con Back To Home) y update-time=no; los servicios cloud no existen en RouterOS x86.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router  Quote: "the router registers a DNS name with the MikroTik cloud only while Back To Home is enabled"
  - Kind: rule of thumb
  - Level: core
  - Also: T04

## T13 Backups, export y gestión de cambios
- a:N51. Export genera texto (.rsc) para copiar configuración entre equipos. No exporta contraseñas de usuarios, certificados ni claves SSH; show-sensitive muestra claves y secretos que por defecto oculta. Importar en la misma versión de RouterOS.
  - Source: https://help.mikrotik.com/docs/spaces/ROS/pages/328155/Configuration+Management  Quote: "System user passwords and user SSH keys can not be exported"
  - Kind: definition
  - Level: core
- a:N52. El backup de sistema (.backup) clona la configuración completa en binario. Problemas típicos al importar un export en otro equipo: interfaces renombradas, distinta cantidad de puertos. import verbose=yes y dry-run ayudan a encontrar el error.
  - Source: https://help.mikrotik.com/docs/spaces/ROS/pages/328155/Configuration+Management  Quote: "System backup is the way to completely clone router configuration in binary format"
  - Kind: mistake
  - Level: core
- a:N53. Hacer un /export file=... después de cada etapa grande de la configuración inicial.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration  Quote: "After completing each major configuration section, it is recommended to create a backup"
  - Kind: rule of thumb
  - Level: foundation

## T14 Actualización de RouterOS y RouterBOOT
- a:N54. Canales: long-term (pocas veces, solo arreglos críticos), stable (cada pocos meses), testing (no para producción) y development. Desde 7.23 el chequeo usa HTTPS: el router necesita salir por TCP 443.
  - Source: https://help.mikrotik.com/docs/spaces/ROS/pages/328142/Upgrading+and+installation  Quote: "should not be used in production"
  - Kind: definition
  - Level: core
- a:N55. Desde v6 no se salta directo a la última: primero a una intermedia (7.12.1) y recién después aparecen las nuevas en el canal.
  - Source: https://help.mikrotik.com/docs/spaces/ROS/pages/328142/Upgrading+and+installation  Quote: "you will only see v7.12.1 as the available version"
  - Kind: rule of thumb
  - Level: core
- a:N56. Después de actualizar RouterOS, actualizar el bootloader: /system routerboard upgrade y reiniciar. Cada versión de RouterOS trae su RouterBOOT. Solo se actualiza el RouterBOOT principal; el de respaldo queda para recuperar.
  - Source: https://help.mikrotik.com/docs/display/ROS/RouterBOOT  Quote: "once you perform a ROS upgrade we always recommend upgrading RouterBoot also"
  - Kind: technique
  - Level: core
- a:N57. La guía de hardening empieza por actualizar RouterOS porque versiones viejas tuvieron vulnerabilidades ya corregidas, y sugiere seguir el blog de anuncios de seguridad.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router  Quote: "Start by upgrading your RouterOS version"
  - Kind: rule of thumb
  - Level: foundation

## T15 Troubleshooting
- a:N58. Torch muestra en vivo los flujos que pasan por una interfaz (direcciones, puertos, protocolo, DSCP, tasas). Ve lo recibido antes del firewall, así que muestra tráfico que luego se descarta. Mientras corre apaga fast path y FastTrack: sube la CPU.
  - Source: https://manual.mikrotik.com/docs/7.25/diagnostics-monitoring-and-troubleshooting/torch  Quote: "Torch sees received packets before the firewall filters them"
  - Kind: definition
  - Level: core
- a:N59. Para encontrar quién consume, mirar Torch en la interfaz LAN (bridge), no en la WAN: después del src-nat todo aparece con la IP pública del router. Filtrar con src-address=IP/32 y port.
  - Source: https://manual.mikrotik.com/docs/7.25/diagnostics-monitoring-and-troubleshooting/torch  Quote: "Watch the LAN interface, not the WAN interface"
  - Kind: technique
  - Level: core
- a:N60. Torch en el puerto padre muestra la columna VLAN-ID y el DSCP: sirve para verificar que una cámara o un teléfono llega en la VLAN correcta. Para ver el contenido o guardar a archivo, packet sniffer.
  - Source: https://manual.mikrotik.com/docs/7.25/diagnostics-monitoring-and-troubleshooting/torch  Quote: "To see the contents of packets or save them to a file, use the packet sniffer instead"
  - Kind: technique
  - Level: advanced
  - Also: T09
- a:N61. Si el router no actualizó bien, mirar el log: /log print without-paging.
  - Source: https://help.mikrotik.com/docs/spaces/ROS/pages/328142/Upgrading+and+installation  Quote: "make sure you check the log"
  - Kind: technique
  - Level: foundation
  - Also: T14

## Disagreements seen
- Configuración por defecto: https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration recomienda conservarla para principiantes; la guía del foro https://forum.mikrotik.com/t/using-routeros-to-vlan-your-network/126489 arma todo desde cero con su propia VLAN de gestión.
- Port forwarding: el ejemplo de https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration publica RDP sin filtrar el origen; https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router y https://mikrotik.com/supportsec/meris-botnet empujan a VPN en lugar de abrir puertos.
- Restringir servicios: available-from en /ip service existe, pero https://manual.mikrotik.com/docs/7.25/getting-started/securing-your-router prefiere hacerlo en el firewall.
- VPN recomendada: securing-your-router nombra WireGuard; el aviso de Mēris nombra IPsec.

## Best stories
- Mēris: la mayoría de los bots eran routers comprometidos en 2018 que se actualizaron pero no cambiaron la contraseña. https://mikrotik.com/supportsec/meris-botnet
- El bridge como puerto CPU: con PVID 1 en el trunk y en el bridge queda una puerta sin etiqueta al router. https://manual.mikrotik.com/docs/7.25/bridging-and-switching/user-guides/bridge-vlan-table
- Safe Mode deshace todo si se corta la sesión, salvo que pases las 100 acciones. https://help.mikrotik.com/docs/spaces/ROS/pages/328155/Configuration+Management
- Hairpin: el servidor contesta directo y el cliente tira la respuesta porque esperaba otra IP. https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat
