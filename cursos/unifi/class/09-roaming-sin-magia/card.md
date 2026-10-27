# Lección 9. Roaming sin magia

**Escuchá:** roaming-sin-magia.mp3 (2 min)

**La idea, en tres líneas**
- El roaming lo decide el cliente; el AP solo informa, acelera o empuja.
- BSS Transition (802.11v) siempre activado. Fast Roaming (802.11r) solo después de probar cada tipo de equipo del cliente. Mínimo RSSI al final, suave y con solape de cobertura comprobado.
- Equipos viejos que no toleran Fast Roaming o WPA3 (PMF obligatorio) van a un SSID aparte, idealmente en su propia VLAN.

**Impacto:** llamadas y videollamadas que no se cortan al caminar, sin dejar afuera lectores, impresoras o sensores viejos.

**Quién lo dice:** 4 de 6 fuentes coinciden en dejar BSS Transition activo; Fast Roaming está dividido: WunderTech lo activa (cita que Ubiquiti lo recomienda), LazyAdmin dice que suele hacer más mal que bien y Purple lo limita a SSID Enterprise de voz y video.

**Laboratorio** · Campo · 15 min
1. Settings > WiFi > Create New, un SSID de prueba ("Prueba-FT") en la red Staff, Advanced en Manual:
```text
BSS Transition:   On
Fast Roaming:     On
Band Steering:    On (preferir 5 GHz, no forzar)
Minimum RSSI:     Off
Security:         WPA2/WPA3 o WPA2 si hay equipos viejos
```
2. Conectá uno de cada tipo de equipo del cliente (celular, notebook, lector, impresora, terminal de pago). Anotá cuál no conecta.
3. Con un celular en llamada de voz o video, caminá de un AP a otro.
4. En UniFi Network abrí el cliente > historial de conexión y roaming: cada paso de AP tiene que verse como roam, no como desconexión y reconexión.
5. Si algún equipo no conectó: SSID aparte sin Fast Roaming para ese grupo.
⚠️ Activar Fast Roaming o WPA3 en un SSID de producción puede dejar sin conexión a equipos viejos de golpe. Probalo primero en un SSID nuevo.

**Regla para quedarse**
Ninguna función de roaming se activa en producción sin probar cada tipo de equipo del cliente.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- 802.11k, r y v en UniFi, matriz de decisión y casos: https://www.purple.ai/en-us/guides/unifi-802-11k-802-11r-fast-roaming
- Fast Roaming, BSS Transition y Handoff Suggestions en Network 10.x: https://www.wundertech.net/how-to-optimize-a-unifi-wi-fi-network/
- Por qué la mayoría de estas funciones conviene dejarlas por defecto: https://lazyadmin.nl/home-network/optimize-your-unifi-network/
