# Lección 10. Invitados aislados

**Escuchá:** invitados-aislados.mp3 (2 min)

**La idea, en tres líneas**
- Con firewall por zonas (Network 9.0 en adelante), una red es de invitados al ponerla en la zona Hotspot; el WiFi elige entre Standard (solo contraseña) y Hotspot (portal cautivo).
- La zona Hotspot trae la landing page activada: si no querés portal, desmarcá Show Landing Page.
- Post-Authorization Restrictions bloquean por defecto 10.0.0.0/8, 172.16.0.0/12 y 192.168.0.0/16. Probalo siempre desde un celular.

**Impacto:** el WiFi de invitados sale a internet y no llega a cajas, NVR ni impresoras.

**Quién lo dice:** 3 de 4 fuentes coinciden en zona Hotspot más prueba de aislamiento; nadie discrepa. Las rutas de menú cambiaron varias veces entre Network 10.0 y 10.6, así que guiate por los nombres de las opciones.

**Laboratorio** · Foco · 20 min
1. Settings > Networks > Create New: nombre "Invitados", Router = gateway UniFi, Zone = Hotspot, VLAN 20, subred 192.168.20.0/24, Allow Internet Access.
2. Settings > WiFi > Create New: nombre "Invitados", Network = Invitados, tipo Hotspot > Captive Portal.
3. Hotspot Portal (desde el aviso bajo Zone o en Client Devices) > Authentication: activá Vouchers. Generá un voucher:
```text
Vencimiento:   1 día
Usos:          1
Límite:        10 Mbps bajada / 5 Mbps subida
```
4. Revisá que en Authorization Access estén las Post-Authorization Restrictions 10.0.0.0/8, 172.16.0.0/12 y 192.168.0.0/16.
5. Desde un celular: conectate, ingresá el voucher, navegá. Después intentá abrir la IP de una impresora o NAS de la red Staff (por ejemplo la impresora en 10.10.10.50, puerto 80). Tiene que vencer el tiempo.
6. Settings > Policy Engine > Zones > Zone Matrix: fila Hotspot hacia Internal en Allow Return, el resto Block All.
⚠️ Si el WiFi de invitados va solo con contraseña (Standard) en zona Hotspot, desmarcá Show Landing Page o les aparece un portal que nadie pidió.

**Regla para quedarse**
No entrego una red de invitados sin probar desde un celular que no llega a nada interno.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guest network con zona Hotspot y la prueba de aislamiento: https://www.wundertech.net/how-to-set-up-a-guest-network-vlan-in-unifi/
- Métodos del portal, vouchers y pre y post autorización: https://help.cloudunifi.com/unifi/setting-up-hotspot/
- Portal externo y pre-autorización paso a paso: https://help.ironwifi.com/configuration-guides/ubiquiti/unifi-hotspot
