# Lección 21. L2TP con IPsec

**Escuchá:** l2tp-con-ipsec.mp3 (2 min)

**La idea, en tres líneas**
- L2TP con IPsec es para cuando del otro lado solo hay el cliente nativo (Windows, macOS, iOS, Android). En el servidor, `use-ipsec=required`: L2TP solo no cifra.
- Servidor: pool, perfil PPP (`local-address` y `remote-address`), un `secret` por persona con `service=l2tp`. En input: UDP 500, UDP 4500 (NAT-T), UDP 1701 y protocolo ESP.
- Si el MikroTik está detrás de NAT (IP privada detrás del módem, con los puertos reenviados) y Windows no conecta pero el celular sí, es NAT-T: la clave de registro `AssumeUDPEncapsulationContextOnSendRule` en 2 y reinicio. Con el MikroTik en IP pública, el valor de fábrica alcanza aunque la notebook esté detrás de NAT.

**Impacto:** le das acceso al encargado o a la central de monitoreo sin instalar nada en su equipo, y sabés por qué falla cuando falla.

**Quién lo dice:** 2 de 3 fuentes coinciden en el servidor con IPsec obligatorio y los cuatro puertos (documentación de IPsec y una guía de un proveedor de VPS, en alemán); Microsoft documenta la clave de NAT-T. La documentación de IPsec aconseja evitar la clave compartida, que L2TP usa igual; ninguna fuente defiende PPTP.

**Laboratorio** · Foco · 20 min
En un router de laboratorio con RouterOS 7, configuración por defecto, LAN 192.168.88.0/24 y una IP pública de ejemplo 203.0.113.10:
1. Pool, perfil y servidor:
```routeros
/ip/pool/add name=pool-l2tp ranges=192.168.89.10-192.168.89.50
/ppp/profile/add name=perfil-l2tp local-address=192.168.89.1 remote-address=pool-l2tp dns-server=192.168.88.1
/interface/l2tp-server/server/set enabled=yes use-ipsec=required ipsec-secret="Secreto-IPsec-Largo-De-Ejemplo-2026" default-profile=perfil-l2tp
```
2. Un usuario por persona:
```routeros
/ppp/secret/add name=encargado password="Clave-Usuario-Ejemplo-1" service=l2tp profile=perfil-l2tp
```
3. Input, arriba del drop de la configuración por defecto:
```routeros
/ip/firewall/filter/add chain=input protocol=udp dst-port=500,4500,1701 action=accept comment="L2TP IPsec" place-before=[find comment="defconf: drop all not coming from LAN"]
/ip/firewall/filter/add chain=input protocol=ipsec-esp action=accept comment="ESP" place-before=[find comment="defconf: drop all not coming from LAN"]
```
4. Para que el tráfico del túnel hacia la LAN no pase por FastTrack, buscá en forward una regla `accept` con `ipsec-policy=in,ipsec` arriba del `fasttrack-connection`. Si no está (o está deshabilitada), agregala:
```routeros
/ip/firewall/filter/print where chain=forward
/ip/firewall/filter/add chain=forward ipsec-policy=in,ipsec action=accept comment="IPsec fuera de FastTrack" place-before=[find action=fasttrack-connection]
```
5. En una notebook Windows, VPN nueva de tipo L2TP/IPsec con clave precompartida, servidor 203.0.113.10, usuario `encargado`. Si conecta, seguí. Si el MikroTik estuviera detrás de NAT (IP privada en ether1 detrás del módem, con UDP 500 y 4500 reenviados) y Windows no conecta, falta NAT-T: en PowerShell como administrador:
```powershell
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\PolicyAgent" -Name AssumeUDPEncapsulationContextOnSendRule -PropertyType DWord -Value 2 -Force
Restart-Computer
```
6. Diagnóstico en el router:
```routeros
/ip/ipsec/active-peers/print
/ppp/active/print
/log/print where topics~"ipsec|l2tp"
```

⚠️ Nunca `use-ipsec=no` en un servidor expuesto: el usuario y la contraseña viajan dentro de un túnel sin cifrar. Y PPTP, nunca.

**Regla para quedarse**
L2TP siempre con IPsec obligatorio, un usuario por persona y cuatro puertos claros en input.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- L2TP/IPsec básico y diagnóstico en la documentación de IPsec 7.25: https://manual.mikrotik.com/docs/7.25/virtual-private-networks/ipsec/
- Clave de registro de Windows para NAT-T: https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/configure-l2tp-ipsec-server-behind-nat-t-device
- Guía práctica con puertos y FastTrack (en alemán, de un proveedor de VPS): https://cloudzy.com/de/blog/mikrotik-l2tp-vpn/
