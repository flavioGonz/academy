# Lección 9. Roaming y mesh

**Escuchá:** roaming-y-mesh.mp3 (2 min)

**La idea, en tres líneas**
- Roaming: SSID idéntico en todos los APs (nombre, seguridad, cifrado, clave), todos en el mismo sitio, Fast Roaming (802.11k/v) encendido; 802.11r solo si los clientes lo soportan.
- Controlador 6.2 suma Non-Stick Roaming, Ping-Pong Roaming Suppression, AI Roaming y Band Steering en Site Settings > Wireless Features.
- Mesh extiende cobertura, no capacidad: hasta 3 saltos, 4 downlinks por uplink, señal del uplink entre -40 y -62 dBm; un EAP que pasó por su web local necesita reset para hacer mesh.

**Impacto:** tablets, lectores y teléfonos WiFi que se mueven sin cortes, y mesh solo donde realmente conviene.

**Quién lo dice:** evidencia fina: roaming se apoya en 1 de 1 fuente (guía oficial de troubleshooting de roaming) y mesh en 1 de 2 (FAQ oficial de mesh). No se encontró discrepancia, pero tampoco mediciones de practicantes.

**Laboratorio** · Campo · 15 min
Con dos EAP en el mismo sitio y una notebook:
1. **Network Config > WLAN**: un solo SSID `Roaming-Lab`, WPA2-Personal, clave de ejemplo `Lab-Roaming-2026`, aplicado a los dos EAP.
2. **Site Settings > Wireless Features**: activá **Fast Roaming**.
3. Separá los EAP lo suficiente para que haya una zona de transición.
4. Conectá la notebook y dejá un ping continuo al gateway:
```powershell
ping -t 192.168.88.1
```
5. Caminá de un AP al otro y volvé. Anotá cuántos "Tiempo de espera agotado" aparecen y verificá en **Clients** a qué AP quedó asociada.
6. Repetí con **802.11r** activado en el SSID (**Edit SSID > Advanced Settings**) y compará. Si algún equipo pierde internet al roamear con 802.11r, dejalo apagado.
7. Para mesh: verificá en el EAP sin cable que la señal del uplink quede entre -40 y -62 dBm.

**Regla para quedarse**
Mismo SSID, mismo sitio, k y v siempre, r con prueba; mesh para cobertura, cable para capacidad.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía oficial de troubleshooting de roaming (incluye funciones de v6.2): https://support.omadanetworks.com/en/document/13229/
- Preguntas frecuentes de mesh en EAP (saltos, señal, capacidad): https://www.omadanetworks.com/cz/support/faq/2283/
