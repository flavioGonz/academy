# Lección 13. Paneles en red

**Escuchá:** paneles-red.mp3 (2 min)

**La idea, en tres líneas**
- Hasta 32 nodos (paneles, teclados, servidores OPC, FSI, BACnet, UGM) por Ethernet con RSTP o por CAN; la red de incendio es física y dedicada, y los switches y conversores van dentro del gabinete para cumplir EN 54.
- IP por defecto 192.168.1.x, donde x es el número de nodo físico (PNA) cargado en el panel y en RPS; usa los puertos 25001 a 25008; con más de 20 switches RSTP se ajustan parámetros.
- BMS por OPC, FSI o BACnet con licencia premium en cada panel visible; si Ethernet es solo para BMS, se desactiva la comunicación panel a panel por TCP/IP. Remoto solo por el gateway de Bosch con IPsec (UDP 500 y 4500) y subredes separadas.

**Impacto:** una red de paneles que arranca a la primera y no queda expuesta en la red del cliente.

**Quién lo dice:** 2 de 2 fuentes coinciden (Networking guide y página de servicios remotos de Bosch); evidencia escasa en número pero primaria, sin discrepancias.

**Laboratorio** · Admin · 15 min
Plan de una red de tres paneles y un servidor OPC:
```text
Nodo | Equipo                  | PNA | IP              | Licencia | Enlace
1    | AVENAR panel 8000 torre A | 1 | 192.168.1.1     | premium  | Eth anillo puerto 1-2
2    | AVENAR panel 8000 torre B | 2 | 192.168.1.2     | premium  | Eth anillo
3    | AVENAR panel 2000 torre C | 3 | 192.168.1.3     | premium  | Eth anillo
4    | Servidor OPC            |  4  | 192.168.1.4     | n/a      | switch en gabinete
Gateway por defecto: 192.168.1.254   Puertos: 25001 a 25008   Multicast: 239.192.0.1
Red del cliente (BMS): otra subred, separada por el servidor OPC
```
1. Completá la tabla con tu obra o con este ejemplo.
2. Verificá que el PNA de cada panel coincida con el último octeto de su IP y con RPS.
3. Marcá dónde van los conversores a fibra si un tramo supera los 100 m de cobre.
⚠️ La red de incendio no se conecta a la red del cliente ni a internet directamente; el acceso remoto se hace solo con el gateway seguro.

**Regla para quedarse**
La red de incendio no comparte switch con nada, y el número de nodo es el último octeto de la IP.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Topologías, IP por defecto, RSTP, BMS y Remote Services (Networking guide): https://media.boschbuildingtechnologies.com/fs/media/pb/media/extranet/fire_alarm_system/software_tools/avenar_panel_firmware/AVENAR_panel_FPA_5000_System_Networking_Guide_version_05.pdf?collection=bosch-bt-lifesafetysystems
- Servicios remotos y autotest de detectores: https://www.boschbuildingtechnologies.com/lifesafetysystems/en/products/remote-monitoring-fire-alarm-systems/
- Opciones de integración con BMS: https://www.boschbuildingtechnologies.com/lifesafetysystems/en/products/fire-alarm-control-panels/
