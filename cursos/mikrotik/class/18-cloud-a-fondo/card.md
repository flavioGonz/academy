# Lección 18. Cloud a fondo

**Escuchá:** cloud-a-fondo.mp3 (2 min)

**La idea, en tres líneas**
- DDNS: `<serie>.sn.mynetname.net` con TTL de 60 segundos; detrás de NAT el router actualiza cada minuto y `/ip/cloud/force-update` lo hace ya. Con dos WAN, `public-address` es la del enlace por donde sale la ruta a la nube.
- `update-time` pone la hora desde la nube al arrancar solo si el cliente NTP está apagado, y es aproximada: para logs e IPsec, NTP.
- DDNS es un nombre, no un camino: detrás de CGNAT apunta a una IP compartida. Para entrar sin IP pública, Back To Home (lección 19) o un concentrador (lección 20).

**Impacto:** el nombre del cliente sigue a la IP aunque el PPPoE reconecte, la hora de los logs es confiable y no prometés acceso por un nombre que no lleva a ningún lado.

**Quién lo dice:** 2 de 5 fuentes coinciden (documentación de Cloud y de NAT); sobre `detect-internet`, en el foro un veterano recomienda apagarlo porque cambia las listas LAN y WAN por su cuenta, y otro usuario lo usa para registrar caídas.

**Laboratorio** · Rápido · 15 min
En un MikroTik con RouterOS 7 (los servicios cloud no están en RouterOS x86, y en CHR piden licencia paga):
1. DDNS y estado:
```routeros
/ip/cloud/set ddns-enabled=yes
/ip/cloud/print
```
Anotá `dns-name`, `public-address` y `status`.
2. Forzá una actualización y comprobá que el nombre resuelve a `public-address`:
```routeros
/ip/cloud/force-update
:put [:resolve [/ip/cloud/get dns-name]]
```
3. Hora: NTP en vez de la hora aproximada de la nube (servidores de ejemplo):
```routeros
/system/ntp/client/set enabled=yes servers=pool.ntp.org
/system/ntp/client/print
/ip/cloud/set update-time=no
```
4. ¿Hay detección de internet moviendo interfaces entre listas?
```routeros
/interface/detect-internet/print
/interface/list/member/print
```
Si `detect-interface-list` no es `none` y tus reglas dependen de las listas LAN y WAN, apagala: `/interface/detect-internet/set detect-interface-list=none`.
5. Con dos WAN: cortá la principal y mirá cómo cambia `public-address` (y con él, a dónde apunta el nombre).

⚠️ El nombre no abre nada: el firewall por defecto sigue descartando lo que llega de internet. Publicar servicios detrás del nombre es la lección 10, con sus reglas.

**Regla para quedarse**
El nombre sigue a la IP, el NTP pone la hora, y para entrar uso un túnel.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- IP Cloud en RouterOS 7.25: DDNS, hora, relays y detalles técnicos: https://manual.mikrotik.com/docs/7.25/network-management/cloud/
- El debate sobre detect-internet y la lista WAN con PPPoE: https://forum.mikrotik.com/t/trying-to-understand-defconf-firewall/267442
- Masquerade con IP dinámica: https://manual.mikrotik.com/docs/7.25/firewall-and-quality-of-service/firewall/nat
