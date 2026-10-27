# Lección 7. Canales angostos

**Escuchá:** canales-angostos.mp3 (2 min)

**La idea, en tres líneas**
- 2.4 GHz: siempre 20 MHz y solo canales 1, 6 y 11.
- 5 GHz: cuanto más denso el lugar, más angosto (80 MHz casa, 40 MHz oficina, 20 MHz alta densidad). Mirá el espectro antes de elegir.
- Con dos o más AP, Channel AI (Network 9.5 y posteriores) propone canales; desde 10.6 puede correr de noche con las radios que elijas. Fijá el ancho antes, porque Channel AI no lo toca.

**Impacto:** menos interferencia entre AP propios y vecinos, menos cortes en horario pico.

**Quién lo dice:** 4 de 5 fuentes coinciden en 20 MHz para 2.4 GHz y en angostar 5 GHz con la densidad; discrepan en DFS (LazyAdmin los evita, std.rocks los usa) y en Auto contra manual (HostiFi desconfía de Auto).

**Laboratorio** · Foco · 20 min
1. UniFi Devices > elegí un AP > AirView > Environment: mirá qué canales usan los vecinos. Si el AP no tiene análisis en tiempo real, corré un Airtime Scan.
⚠️ El escaneo Full desconecta a los clientes de esa radio: hacelo fuera de horario.
2. Fijá anchos para todos los AP en Settings > WiFi > Default WiFi Speeds > Custom:
```text
2.4 GHz   20 MHz
5 GHz     40 MHz (oficina) / 80 MHz (casa, pocos vecinos) / 20 MHz (más de 30 clientes por AP)
6 GHz     160 MHz
```
3. Apply to All APs > Apply Changes.
4. AirView > Channel AI > elegí la banda > Optimize > revisá el resumen > Apply Changes. Repetí por banda.
5. Si los canales 36 a 48 están saturados y querés probar DFS: Settings > WiFi > Default WiFi Speeds > Custom > Extended 5 GHz Spectrum (DFS).
6. Al día siguiente, AirView > Radios > Time Machine: compará uso de airtime y eventos (cambios por radar incluidos).

**Regla para quedarse**
El ancho de canal lo elijo por la cantidad de clientes y vecinos, no por lo que dice la caja.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Channel AI, anchos y DFS paso a paso: https://www.wundertech.net/how-to-optimize-a-unifi-wi-fi-network/
- El caso de la oficina de 300 equipos, canal 64 y 20 MHz: https://std.rocks/improve-wifi-performance-guide.html
- Por qué evitar DFS y qué ancho usar: https://lazyadmin.nl/home-network/optimize-your-unifi-network/
