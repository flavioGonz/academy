# Lección 5. VLAN por sistema

**Escuchá:** vlan-por-sistema.mp3 (2 min)

**La idea, en tres líneas**
- Un solo bridge con `vlan-filtering`: access entra sin etiqueta y recibe su PVID, trunk solo lleva tráfico etiquetado.
- `ingress-filtering=yes` y `frame-types` en todos los puertos, gestión por una VLAN propia (ej. 99) y nunca por la VLAN 1.
- `vlan-filtering=yes` es lo último que se activa, con un puerto de rescate fuera del bridge.

**Impacto:** una cámara infectada o un NVR que satura no se lleva puesta la red de la oficina, y el cliente ve el CCTV separado de sus datos.

**Quién lo dice:** 2 de 3 fuentes coinciden (documentación de Bridge VLAN Table y guía de VLAN del foro); no hay discrepancias de fondo. La documentación avisa que activar el filtrado antes de resolver la gestión puede dejarte afuera.

**Laboratorio** · Foco · 20 min
En un hAP o CRS de laboratorio con RouterOS 7. Plan: ether2 y ether3 cámaras (VLAN 20), ether4 trunk hacia otro switch, ether5 rescate fuera del bridge.
1. Puerto de rescate con IP propia (sacalo del bridge si estaba):
```routeros
/interface/bridge/port/remove [find interface=ether5]
/ip/address/add address=10.255.255.1/30 interface=ether5 comment="rescate"
```
Poné la notebook en ether5 con 10.255.255.2/30 y conectate por ahí.
2. Puertos, PVID y tabla VLAN (una entrada por VLAN):
```routeros
/interface/bridge/port/set [find interface=ether2] pvid=20 frame-types=admit-only-untagged-and-priority-tagged ingress-filtering=yes
/interface/bridge/port/set [find interface=ether3] pvid=20 frame-types=admit-only-untagged-and-priority-tagged ingress-filtering=yes
/interface/bridge/port/set [find interface=ether4] frame-types=admit-only-vlan-tagged ingress-filtering=yes
/interface/bridge/vlan/add bridge=bridge tagged=bridge,ether4 untagged=ether2,ether3 vlan-ids=20
/interface/bridge/vlan/add bridge=bridge tagged=bridge,ether4 vlan-ids=99
```
3. Interfaces de capa 3 para CCTV y gestión (rangos de ejemplo):
```routeros
/interface/vlan/add name=vlan20-cctv interface=bridge vlan-id=20
/interface/vlan/add name=vlan99-gestion interface=bridge vlan-id=99
/ip/address/add address=10.10.20.1/24 interface=vlan20-cctv
/ip/address/add address=10.10.99.1/24 interface=vlan99-gestion
```
4. Revisá la tabla antes de activar y después activá:
```routeros
/interface/bridge/vlan/print
/interface/bridge/set bridge vlan-filtering=yes
```
5. Con una cámara o PC en ether2, mirá con Torch que su tráfico aparece en la VLAN: `/tool/torch ether4` (columna VLAN-ID si hay tráfico hacia el trunk) o `/tool/torch vlan20-cctv`.

⚠️ No actives `vlan-filtering` por el mismo puerto que estás configurando: hacelo desde ether5 o por consola serial.

**Regla para quedarse**
`vlan-filtering` es lo último que se toca, con un camino de rescate abierto.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Bridge VLAN Table, trampas de PVID e ingress-filtering (7.25): https://manual.mikrotik.com/docs/7.25/bridging-and-switching/user-guides/bridge-vlan-table
- Guía del foro para integradores: access, trunk, híbridos y VLAN de gestión: https://forum.mikrotik.com/t/using-routeros-to-vlan-your-network/126489
