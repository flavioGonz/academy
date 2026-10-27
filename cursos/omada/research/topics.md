# Subtemas: TP-Link Omada SDN Controller (nivel inicial a intermedio, técnicos de obra y soporte)

Cómo se enseña: TP-Link Academy dicta las certificaciones OCNA (Omada Certified Network Administrator) en dos tracks, Wireless y Routing & Switching, a través de distribuidores (Bluechip IT, LinITX). Los temarios públicos y la base de conocimiento de support.omadanetworks.com se ordenan igual: tipos de controlador, adopción, sitios, LAN/VLAN, WLAN, autenticación (portal), VPN, mantenimiento (firmware, backup, migración) y troubleshooting. Este mapa sigue ese orden.

- T01 Arquitectura SDN: modo standalone vs modo controlador, qué pasa con la GUI local al adoptar.
- T02 Tipos de controlador: Software, Hardware (OC200/OC220/OC300/OC400), Cloud-Based (Omada Central Essentials y Standard), gateways integrados (Fusion, ER7212PC); Cloud Access vs controlador en la nube; licencias.
- T03 Instalar el controlador software: Windows/Linux, Docker (imagen comunitaria), requisitos (Java, MongoDB, RAM, AVX).
- T04 Puertos del controlador y firewall: web 8043/8088, portal 8843, descubrimiento 29810, gestión 29811 a 29817, 27001.
- T05 Descubrimiento y adopción en capa 2: Pending, credenciales, Adopt Failed.
- T06 Adopción en capa 3 y remota: Omada Discovery Utility, Inform URL, DHCP option 138, port forwarding, VPN, Site URL de Omada Central.
- T07 Sitios, MSP y cuentas: un gateway por sitio, modo MSP, roles.
- T08 Redes LAN/VLAN y perfiles de puerto en gateway ER y switches JetStream; VLAN de gestión.
- T09 ACL y segmentación entre VLAN.
- T10 RF en EAP: canales, ancho de canal, potencia, ubicación, WLAN Optimization (RRM), región.
- T11 Roaming: fast roaming 802.11k/v, 802.11r, band steering, non-stick, AI Roaming.
- T12 Mesh en EAP: root AP, saltos, señal de uplink, auto failover.
- T13 Portal cautivo: tipos de autenticación, voucher, pre-authentication access, HTTPS.
- T14 VPN de sitio a sitio entre gateways Omada: Auto IPsec, Manual IPsec, NAT.
- T15 Firmware: controlador y dispositivos, upgrade, downgrade, ritmo de actualizaciones.
- T16 Backup, migración de controlador y troubleshooting operativo (licencias, equipos que no reconectan).
