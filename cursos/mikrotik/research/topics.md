# Subtemas: MikroTik RouterOS 7 para integradores

Nivel: inicial a intermedio. Público: técnicos instaladores y de soporte de seguridad electrónica (CCTV, control de acceso, alarmas) que ya saben IP, máscara, gateway y qué es una VLAN, pero no son expertos en RouterOS.

Cómo se enseña: el temario de MTCNA (MikroTik Certified Network Associate) arranca por acceso al equipo (Winbox, WebFig, CLI), configuración por defecto, actualización de RouterOS y RouterBOOT, bridge, DHCP, firewall y NAT, ruteo estático, y cierra con túneles y herramientas (torch, ping, traceroute, sniffer, logs). La documentación oficial de MikroTik (manual.mikrotik.com, versión 7.25, y el sitio congelado help.mikrotik.com) sigue el mismo orden: First Time Configuration, Securing your router, Configuration Management, Bridging, Firewall, Routing, VPN, Diagnostics.

- T01 Acceso inicial y herramientas de gestión: Winbox (por IP y por MAC), WebFig, SSH, Neighbor Discovery.
- T02 Configuración por defecto, reset y Netinstall: cuándo conservar la defconf, cuándo `no-defaults=yes`, botón de reset, recuperación.
- T03 Usuarios, grupos y contraseñas: un usuario por técnico, deshabilitar admin, grupos con políticas mínimas, address por usuario.
- T04 Servicios IP y superficie de ataque: `/ip service`, MAC server, SOCKS, UPnP, DNS remoto, bandwidth server.
- T05 Interfaces, bridge e interface lists (LAN/WAN).
- T06 Direccionamiento, DHCP cliente y servidor, DNS.
- T07 NAT: masquerade, src-nat, dst-nat, hairpin.
- T08 Firewall filter: input vs forward, estados de conexión, orden de reglas, address-lists, drop por defecto.
- T09 VLANs con bridge vlan-filtering: trunk, access, PVID, ingress-filtering, frame-types, VLAN de gestión.
- T10 Multi-WAN y failover: distancias, rutas recursivas, check-gateway, scope/target-scope, Netwatch.
- T11 VPN para gestión remota: WireGuard (road warrior y sitio a sitio), L2TP/IPsec, túnel saliente a un VPS.
- T12 IP Cloud y DDNS: nombre sn.mynetname.net, Back To Home, qué abre y qué no.
- T13 Backups, export y gestión de cambios: .backup vs export .rsc, show-sensitive, safe mode, undo.
- T14 Actualización de RouterOS y RouterBOOT: canales, orden, bootloader.
- T15 Troubleshooting: ping, traceroute, torch, packet sniffer, logs.
- T16 Port forwarding para NVR y cámaras con criterio de seguridad: dst-nat restringido, address-lists, alternativas.

## Ampliación (octubre 2026, lecciones 13 a 22)
Cómo se enseña: la documentación de RouterOS 7.25 separa la conexión a internet (First Time Configuration: DHCP, IP estática, PPPoE; páginas propias de DHCP Client y PPPoE), el software (Upgrade, Packages, canales) y el acceso remoto (Cloud, Back To Home, IPsec, L2TP, licencias CHR). El temario MTCNA cubre DHCP cliente, PPPoE y actualización; IPsec y CHR quedan en MTCRE/MTCSE y en la práctica de integradores. Para Antel se buscaron fuentes uruguayas (antel.com.uy, foros de usuarios y de proveedores).

- T17 IP fija en la WAN: dirección, ruta por defecto, DNS estáticos, verificación, IP fija de Antel o de otro ISP.
- T18 DHCP cliente en la WAN: add-default-route, distancia, DNS y NTP del proveedor, script de lease, doble NAT.
- T19 PPPoE y el caso Antel: ONT en modo puente, credenciales, VLAN, MTU y MSS, IP dinámica al reconectar.
- T20 Paquetes y canales de RouterOS: Check for Updates, paquetes extra, .npk sin internet, downgrade, canales long-term, stable, testing y development.
- T21 CHR en un VPS como concentrador de VPN: instalación, licencias, endurecimiento, sitios que llaman al hub.
- T22 L2TP con IPsec: servidor, perfiles PPP, clientes nativos, puertos, NAT-T, diagnóstico.
- T23 IPsec puro entre marcas: profile, peer, identity, proposal, policy, diagnóstico de SA y políticas, bypass de NAT y FastTrack.
- T24 Back To Home: VPN WireGuard gestionada por la nube de MikroTik, usuarios, relay y límites.
