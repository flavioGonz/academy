# Lección 2. Capa por capa

**Escuchá:** capa-por-capa.mp3 (2 min)

**La idea, en tres líneas**
- Orden de diagnóstico: tu propia IP, el gateway, la tabla ARP y recién después la ruta.
- Un ping que falla no prueba que el equipo esté apagado: ICMP puede estar bloqueado.
- pathping combina tracert y ping, y muestra en qué salto se pierden paquetes.

**Impacto:** menos viajes al sitio para encontrar una cámara que estaba viva y solo bloqueaba el ping.

**Quién lo dice:** 2 de 2 fuentes coinciden (evidencia fina): LazyAdmin y la referencia de Test-NetConnection de Microsoft; nadie discrepa, aunque Test-NetConnection -TraceRoute da la ruta sin la estadística por salto.

**Laboratorio** · Rápido · 10 min
En tu notebook o una VM en la red de laboratorio (ejemplo 192.168.88.0/24):
1. Tu configuración:
```text
ipconfig /all
```
Anotá IP, máscara, puerta de enlace y DNS de la placa activa.
2. Gateway y un equipo de la misma subred:
```text
ping 192.168.88.1
ping 192.168.88.20
arp -a
```
Si la MAC de 192.168.88.20 aparece en la tabla, respondió a ARP aunque el ping falle.
3. Un destino en otra red, rápido:
```text
pathping -n -q 10 -h 5 203.0.113.10
```
`-n` no resuelve nombres, `-q 10` baja de 100 a 10 consultas por salto, `-h 5` corta a 5 saltos.
4. La misma ruta desde PowerShell:
```powershell
Test-NetConnection 203.0.113.10 -TraceRoute
```
5. Opcional: en un equipo de prueba con el ping entrante bloqueado, repetí el paso 2 y mirá que la MAC aparece igual.

**Regla para quedarse**
Antes de declarar caído un equipo, miro ARP en su subred y pathping si hay saltos.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Pathping y cómo acelerarlo: https://lazyadmin.nl/it/pathping-command/
- Referencia de Test-NetConnection: https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection
