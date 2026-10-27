# Lección 12. Mirar primero

**Escuchá:** mirar-primero.mp3 (2 min)

**La idea, en tres líneas**
- Ante "el WiFi anda mal", primero el historial del cliente (conexión y roaming, Network 10.5 en adelante) y el Time Machine de radios y puertos (10.6.101).
- Patrones: roam en el borde de celda está bien; desconexión y reconexión es hueco de cobertura; ping-pong entre dos AP es potencia pareja de más.
- Después, un cambio por vez y probar. Si algo se rompió, mirá lo último que tocaste o volvé a los valores por defecto.

**Impacto:** soporte más corto, sin cambios a ciegas que generan un problema nuevo.

**Quién lo dice:** 4 de 4 fuentes empujan a mirar historial y eventos antes de tocar, y 4 de 5 piden un cambio por vez; nadie discrepa. std.rocks recuerda que ninguna optimización reemplaza al cable donde se puede tender.

**Laboratorio** · Rápido · 10 min
1. UniFi Network > Client Devices > elegí un cliente WiFi con quejas o uno cualquiera.
2. Abrí su historial de conexión y roaming. Anotá:
```text
Cliente:              <nombre / MAC>
AP y banda actuales:  <AP-xx, 5 GHz>
Señal promedio:       <dBm>  (Ubiquiti trata -70 dBm como mínimo y recomienda -65 dBm o mejor, según WunderTech)
Eventos 24 h:         <roams / desconexiones / ping-pong>
```
3. UniFi Devices > el AP de ese cliente > AirView > Radios > Time Machine: ¿hubo cambio de canal, de potencia o de configuración en las últimas 24 horas?
4. Port Manager > Time Machine del puerto del AP: ¿el uplink flapeó?
5. Escribí en tres líneas qué pasó y cuál es el único cambio que vas a probar primero. Recién ahí tocás algo.

**Regla para quedarse**
Primero el historial, después la teoría, y un cambio por vez.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Cómo leer el historial del cliente y los tres patrones: https://www.purple.ai/en-us/guides/unifi-802-11k-802-11r-fast-roaming
- Time Machine de radios y puertos en Network 10.6.101: https://community.ui.com/releases/UniFi-Network-Application-10-6-101/05283624-0980-4dd7-b8d6-9fa5c4e28da4
- Un cambio por vez y los sospechosos habituales: https://www.wundertech.net/how-to-optimize-a-unifi-wi-fi-network/
