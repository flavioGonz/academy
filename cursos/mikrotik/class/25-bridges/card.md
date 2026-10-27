# Lección 25. Un solo bridge

**Escuchá:** bridges.mp3 (2 min)

**La idea, en tres líneas**
- Un bridge es un switch dentro del router: los puertos que agregás quedan en la misma red de capa 2 y pasan a ser esclavos del bridge. La IP, el servidor DHCP y las VLAN van en el bridge, nunca en un puerto que está adentro.
- En equipos con switch chip, la marca `H` en `/interface/bridge/port/print` dice que el chip conmuta a velocidad de cable. Fuera de los CRS1xx/2xx, solo un bridge por switch chip tiene esa ayuda: el segundo bridge va por la CPU. Para separar redes, VLAN, no más bridges.
- La configuración por defecto de un hAP o un hEX deja ether1 fuera del bridge como WAN. En un CRS con configuración de switch todos los puertos están adentro: para usar uno como WAN lo sacás del bridge, lo sumás a la lista WAN y le das su cliente DHCP o su IP.

**Impacto:** el switch interno trabaja a velocidad de cable, la CPU queda libre para rutear y no hay una IP olvidada en un puerto que nunca contesta.

**Quién lo dice:** 4 de 5 fuentes coinciden en un solo bridge con la IP en el bridge (documentación de Bridging and Switching y de errores de capa 2 en 7.25, la guía de configuración manual y un veterano del foro); el matiz lo pone el mismo hilo: en routers sin switch chip, como los CCR, la cantidad de bridges casi no pesa, y en equipos con dos switch chips (RB3011) hay un bridge con offload por chip.

**Laboratorio** · Foco · 15 min
En un hAP o hEX de banco con RouterOS 7 y la configuración por defecto, la notebook en ether2 y ether1 desconectado:
1. Antes de tocar, export (lección de backup) y Safe Mode. Mirá qué armó la configuración por defecto:
```routeros
/interface/bridge/print detail
/interface/bridge/port/print
/ip/address/print
```
Los puertos con `H` están en el switch chip. La IP 192.168.88.1/24 está en `bridge`, no en ether2.
2. Mirá la MAC del bridge: la configuración por defecto trae `auto-mac=no` y una `admin-mac` fija. Si alguna vez creás un bridge a mano, fijala vos, así no cambia al sacar un puerto:
```routeros
/interface/bridge/add name=bridge-lab auto-mac=no admin-mac=02:00:00:00:00:25
/interface/bridge/remove [find name=bridge-lab]
```
3. Sacá ether5 del bridge y dale una red propia, como harías con un puerto para un equipo aparte:
```routeros
/interface/bridge/port/remove [find interface=ether5]
/ip/address/add address=10.10.50.1/24 interface=ether5 comment="lab puerto propio"
```
Pasá la notebook a ether5 con IP fija 10.10.50.2/24 y probá `ping 10.10.50.1`: contesta. WinBox por 10.10.50.1, no: ether5 no está en la lista LAN y la configuración por defecto corta en input todo lo que no viene de LAN (el ICMP lo acepta antes).
4. Si un equipo vino con ether1 dentro del bridge (un CRS con configuración de switch, o un router armado por otro), así queda como WAN:
```routeros
/interface/bridge/port/print where interface=ether1
/interface/bridge/port/remove [find interface=ether1]
/interface/list/member/add list=WAN interface=ether1
/ip/dhcp-client/add interface=ether1 disabled=no
```
En el hAP de banco el primer comando no muestra nada: ahí ether1 ya está afuera. Si en el equipo no existe la lista WAN, se crea con `/interface/list/add name=WAN`, y antes de enchufarle internet va el firewall de la lección de cerrar puertas: la página de configuraciones por defecto no le da firewall a la de switch.
5. Volvé a ether2 y dejá todo como estaba:
```routeros
/ip/address/remove [find comment="lab puerto propio"]
/interface/bridge/port/add bridge=bridge interface=ether5
/interface/bridge/port/print
```
ether5 vuelve con su `H`.

⚠️ Sacar del bridge el puerto por donde entrás te corta: la IP vive en el bridge. Y cambiar `vlan-filtering`, L2MTU o el snooping puede reiniciar el switch chip y apagar un momento todos los puertos.

**Regla para quedarse**
Un bridge por equipo, la IP en el bridge, y lo que hay que separar va por VLAN.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Bridge, admin-mac y hardware offloading en RouterOS 7.25: https://manual.mikrotik.com/docs/7.25/bridging-and-switching/
- Varios bridges en un mismo switch chip y otros errores de capa 2: https://manual.mikrotik.com/docs/7.25/bridging-and-switching/user-guides/layer2-misconfiguration
- Qué deja cada configuración por defecto (AP Router, Switch, IP Only): https://manual.mikrotik.com/docs/7.25/getting-started/configuration-management/default-configurations
- Foro: el router que "murió" al sacar ether2 del bridge, y la MAC del bridge: https://forum.mikrotik.com/t/remove-port-from-the-default-brige/125811
- Foro: un bridge o varios según el equipo: https://forum.mikrotik.com/t/one-or-more-bridges/146916
