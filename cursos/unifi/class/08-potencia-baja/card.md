# Lección 8. Potencia baja

**Escuchá:** potencia-baja.mp3 (2 min)

**La idea, en tres líneas**
- Potencia al máximo deja a los clientes pegados a un AP lejano: el AP los escucha mal, hay reintentos y se consume el airtime de todos.
- Con varios AP, punto de partida: 2.4 GHz baja, 5 GHz entre baja y media, 6 GHz alta. Con un solo AP, alta.
- Si queda una zona débil, un AP más es mejor que subirle la potencia a todos.

**Impacto:** los clientes se pasan al AP más cercano y el WiFi rinde parejo en todo el local.

**Quién lo dice:** 5 de 5 fuentes coinciden en que la potencia alta perjudica con varios AP; WunderTech nota que la guía residencial de Ubiquiti sugiere alta salvo AP muy juntos, así que los valores son un punto de partida a ajustar por AP.

**Laboratorio** · Campo · 20 min
1. Elegí tres puntos del local (cerca del AP 1, entre AP 1 y AP 2, cerca del AP 2). Con la app WiFiman en el celular anotá en cada punto la señal (dBm) y a qué AP estás conectado.
2. En UniFi Network: AirView > Radios (o UniFi Devices > AP > Settings) y ajustá:
```text
2.4 GHz   Low
5 GHz     Medium (Low si hay un AP por ambiente)
6 GHz     High
```
3. Apply Changes y esperá un par de minutos.
4. Repetí la caminata. Buscá que en el punto cercano al AP 2 el celular ya esté en el AP 2 y con -65 dBm o mejor.
5. Si algún punto queda por debajo de -70 dBm, anotalo como candidato a AP adicional o subí un nivel solo ese AP.
⚠️ Bajar potencia en producción puede dejar rincones sin cobertura: hacelo AP por AP y caminando.

**Regla para quedarse**
Más AP con menos potencia antes que pocos AP a todo volumen.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- La potencia como causa número uno y valores sugeridos: https://lazyadmin.nl/home-network/optimize-your-unifi-network/
- Por qué un cliente con señal pobre frena a todos: https://std.rocks/improve-wifi-performance-guide.html
- Valores por banda y la excepción de un solo AP: https://www.wundertech.net/how-to-optimize-a-unifi-wi-fi-network/
