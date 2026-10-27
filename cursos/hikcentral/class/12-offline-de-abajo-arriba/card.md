# Lección 12. Offline de abajo arriba

**Escuchá:** offline-de-abajo-arriba.mp3 (2 min)

**La idea, en tres líneas**
- Diagnosticá en orden: físico, IP y gateway, DNS, servicio habilitado, puertos.
- Validá cada puerto contra la Communication Matrix: 80 y 443 clientes, 7660 registro ISUP, 554 y 559 del Streaming Gateway (559 para vivo en Chrome y Firefox).
- No todo es red: "máximo número de streams" es el tope de conexiones del NVR, y las ONVIF offline suelen ser un puerto distinto de 80.

**Impacto:** tickets de "aparece offline" resueltos con un método repetible y no a prueba y error.

**Quién lo dice:** 4 de 8 fuentes de troubleshooting siguen el orden de abajo arriba (artículos del soporte de Hikvision USA, FAQ y Quick Start); 3 de 8 piden validar contra la matriz de puertos. Learncctv enfoca en abrir puertos del equipo en el router, útil para equipos sueltos pero no reemplaza la matriz.

**Laboratorio** · Campo · 15 min
1. Desde una PC en la red del equipo (cámara de ejemplo 192.168.88.21, gateway 192.168.88.1, SYS 192.168.88.10):
```powershell
ipconfig
ping 192.168.88.1
ping 192.168.88.21
Resolve-DnsName dev.hik-connect.com
```
2. Puertos clave:
```powershell
Test-NetConnection 192.168.88.21 -Port 8000
Test-NetConnection 192.168.88.10 -Port 7660
Test-NetConnection 192.168.88.10 -Port 559
```
3. En el Web Client buscá el registro de online y offline del equipo (Maintenance > Search for Online/Offline Logs of Device en V2.6.1) y anotá a qué hora cae.
4. Si el equipo usa Hik-Connect: casilla de Platform Access habilitada, DNS 8.8.8.8 y puertos STUN 6002, 6800, 8555, 9010 y 9020 permitidos en el firewall.
5. Si aparece "maximum number of streams": contá conexiones al NVR antes de tocar el ancho de banda; un Streaming Server reduce las conexiones directas.
6. Cámara ONVIF offline: revisá su puerto de servicio y corregilo en HikCentral si no es 80.

⚠️ Los cambios en el firewall o router del cliente los hace o autoriza el cliente.

**Regla para quedarse**
De abajo hacia arriba, y cada puerto contra la matriz.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Receta de Hik-Connect offline y puertos STUN (soporte de Hikvision USA): https://supportusa.hikvision.com/support/solutions/articles/17000146654-troubleshooting-platform-access-offline-on-device
- Matriz de puertos de HikCentral Professional (Communication Matrix V2.4.1): https://pinfo.hikvision.com/hkwsen/unzip/20230511205434_28997_doc/HikCentral%20Professional_Communication%20Matrix_V2.4.1_20230511.pdf
- Máximo número de streams en un NVR: https://supportusa.hikvision.com/support/solutions/articles/17000135582-how-to-see-the-number-of-streams-from-an-nvr-error-maximum-number-of-streams
