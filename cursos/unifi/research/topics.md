# Mapa del tema: UniFi Network, controlador y sitios multi-cliente

Nivel: inicial a intermedio. Técnicos instaladores y de soporte con base de redes (IP, máscara, gateway, VLAN de nombre).
Versión de referencia: UniFi Network 10.6 / 11.0 sobre UniFi OS 5.x / 6.x (octubre 2026).

Cómo se enseña: el temario oficial del curso Ubiquiti Enterprise Wireless Admin (UEWA), según el resumen de LinITX, va de fundamentos de WLAN y planificación RF (canales, potencia, ancho, airtime) a adopción básica (multi-sitio, adopción L2, SSID, seguridad y VLAN) y adopción avanzada e invitados (hosting en la nube, adopción L3 con descubrimiento, SSH, DNS y DHCP, mínimo RSSI, portal de invitados). Los practicantes (LazyAdmin, WunderTech, HostiFi, UniHosted, Deluisio) suman lo operativo: dónde correr el controlador, Site Manager, backups, firmware y troubleshooting. El mapa sigue ese orden.

Fuente: https://blog.linitx.com/ubiquiti-uewa-training-course/

| Id | Subtema |
|----|---------|
| T01 | Arquitectura: UniFi OS, Network Application, consola y "host" de cada dispositivo |
| T02 | Dónde corre el controlador: Cloud Gateway (UCG/UDM), CloudKey, UniFi OS Server, hosting |
| T03 | Site Manager (unifi.ui.com) y gestión de muchos sitios: acceso remoto, Fabrics, roles, Blueprints |
| T04 | Adopción en capa 2: descubrimiento, reset, versiones de firmware |
| T05 | Adopción en capa 3: set-inform, DHCP option 43, DNS "unifi", inform host |
| T06 | Backups, restauración y migración de controlador |
| T07 | Redes y VLANs: networks, VLAN ID, DHCP por VLAN, zonas del firewall |
| T08 | Puertos de switch: VLAN nativa, VLANs etiquetadas, perfiles, trunk a AP, seguridad de puerto |
| T09 | Plan de RF: bandas, canales, ancho de canal, DFS, Channel AI |
| T10 | Potencia de transmisión y tamaño de celda |
| T11 | Roaming y steering: band steering, BSS Transition (802.11v), Fast Roaming (802.11r), mínimo RSSI |
| T12 | Seguridad WiFi: WPA2/WPA3, PMF, Enterprise/RADIUS, compatibilidad de dispositivos viejos |
| T13 | Redes de invitados y portal cautivo: zona Hotspot, vouchers, pre y post autorización |
| T14 | Firmware y actualizaciones: canales de release, despliegue escalonado, revert |
| T15 | Monitoreo y alertas: Alarm Manager, Time Machine, historial de clientes, observabilidad |
| T16 | Troubleshooting de clientes WiFi: método, herramientas, señal mínima, un cambio por vez |
