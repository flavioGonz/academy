# Lección 22. IPsec entre marcas

**Escuchá:** ipsec-entre-marcas.mp3 (2 min)

**La idea, en tres líneas**
- Cinco piezas: fase 1 = `profile` (hash, cifrado, grupo DH, lifetime) y `peer` (IP remota, IKEv2); `identity` (clave o certificado); fase 2 = `proposal` (cifrado, PFS, lifetime) y `policy` (red local, red remota, `tunnel=yes`). Todo tiene que coincidir en las dos puntas: primero la tabla, después el túnel.
- Diagnóstico por capas: `active-peers` (fase 1), `ph2-state` en `/ip/ipsec/policy/print` (fase 2), `installed-sa` (contadores) y el log con `topics=ipsec`.
- Los dos clásicos: el masquerade cambia el origen antes de cifrar (regla de NAT `accept` arriba de todo) y FastTrack saltea las políticas (bypass en forward). Si "se arregla al prender Torch", es FastTrack.

**Impacto:** levantás túneles con firewalls de otras marcas en una sola visita y sabés en qué fase está la falla.

**Quién lo dice:** 3 de 6 fuentes coinciden en acordar los parámetros de las dos fases y diagnosticar por capas, y 4 de 6 en el bypass de NAT y FastTrack (documentación de IPsec y de firewall, MKController y una guía con pfSense). Discrepan en clave compartida o certificados (la documentación aconseja evitar la clave) y en NAT-T (la guía de pfSense lo apaga con IPs públicas). Para Fortinet, Cisco o Ubiquiti no se leyó una guía específica: vale la misma tabla.

**Laboratorio** · Foco · 20 min
Sitio A (MikroTik, RouterOS 7, defconf): pública 203.0.113.10, LAN 192.168.88.0/24. Sitio B (otro MikroTik o un pfSense): pública 198.51.100.20, LAN 10.10.10.0/24. Relojes con NTP en los dos (lección 18).
1. La tabla, para mandar al técnico del otro lado:
```text
Fase 1: IKEv2 · clave precompartida · AES-256 · SHA-256 · DH 14 (modp2048) · lifetime 1d · DPD activo · NAT-T si hay NAT
Fase 2: ESP túnel · AES-256-CBC · SHA-256 · PFS grupo 14 · lifetime 1h
Redes:  local 192.168.88.0/24  <->  remota 10.10.10.0/24
```
2. Las cinco piezas en el sitio A:
```routeros
/ip/ipsec/profile/add name=perfil-sucursal hash-algorithm=sha256 enc-algorithm=aes-256 dh-group=modp2048 lifetime=1d
/ip/ipsec/peer/add name=sucursal address=198.51.100.20/32 profile=perfil-sucursal exchange-mode=ike2
/ip/ipsec/identity/add peer=sucursal auth-method=pre-shared-key secret="Clave-Larga-De-Ejemplo-Para-El-Tunel-2026"
/ip/ipsec/proposal/add name=prop-sucursal auth-algorithms=sha256 enc-algorithms=aes-256-cbc pfs-group=modp2048 lifetime=1h
/ip/ipsec/policy/add peer=sucursal tunnel=yes src-address=192.168.88.0/24 dst-address=10.10.10.0/24 proposal=prop-sucursal action=encrypt
```
3. Puertos solo desde el otro extremo, arriba del drop:
```routeros
/ip/firewall/filter/add chain=input src-address=198.51.100.20 protocol=udp dst-port=500,4500 action=accept comment="IKE sucursal" place-before=[find comment="defconf: drop all not coming from LAN"]
/ip/firewall/filter/add chain=input src-address=198.51.100.20 protocol=ipsec-esp action=accept comment="ESP sucursal" place-before=[find comment="defconf: drop all not coming from LAN"]
```
4. Bypass de NAT y de FastTrack:
```routeros
/ip/firewall/nat/add chain=srcnat src-address=192.168.88.0/24 dst-address=10.10.10.0/24 action=accept comment="no NAT al tunel" place-before=0
/ip/firewall/filter/add chain=forward src-address=192.168.88.0/24 dst-address=10.10.10.0/24 action=accept comment="tunel fuera de FastTrack" place-before=[find action=fasttrack-connection]
/ip/firewall/filter/add chain=forward src-address=10.10.10.0/24 dst-address=192.168.88.0/24 action=accept comment="tunel fuera de FastTrack" place-before=[find action=fasttrack-connection]
```
5. Diagnóstico:
```routeros
/ip/ipsec/active-peers/print
/ip/ipsec/policy/print detail
/ip/ipsec/installed-sa/print
/system/logging/add topics=ipsec,!debug
/log/print where topics~"ipsec"
```
6. Qué significa cada síntoma:
```text
no suitable proposal / NO-PROPOSAL-CHOSEN    -> parámetros distintos: comparar la tabla con el log (local:remoto)
phase1 negotiation failed due to time up     -> comunicación: UDP 500/4500, IP del peer, NAT en el medio
Fase 1 y 2 arriba, no pasa tráfico            -> NAT bypass ausente o mal ubicado; limpiar conexiones viejas
Lento o con pérdidas, "se arregla" con Torch  -> FastTrack
Ping en un solo sentido                       -> firewall de alguno de los dos lados
```
Si probaste antes del bypass: `/ip/firewall/connection/remove [find where dst-address~"^10.10.10."]`.

⚠️ Las dos LAN no pueden tener el mismo rango (dos 192.168.88.0/24 no se rutean entre sí): renumerá una antes del túnel.

**Regla para quedarse**
Primero la tabla firmada por las dos puntas, después el túnel, y el log para no adivinar.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- IPsec en RouterOS 7.25: sitio a sitio, NAT y FastTrack, preguntas frecuentes: https://manual.mikrotik.com/docs/7.25/virtual-private-networks/ipsec/
- MikroTik con pfSense, fase 1 y fase 2 lado a lado: https://getlabsdone.com/setup-ipsec-site-to-site-vpn-tunnel-between-pfsense-and-mikrotik/
- IKEv2 sitio a sitio, bypass y ph2-state: https://mkcontroller.com/blog/remote_access/mikrotik/mikrotik-ipsec-site-to-site-vpn/
