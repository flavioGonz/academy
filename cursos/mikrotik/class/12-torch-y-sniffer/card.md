# Lección 12. Torch y sniffer

**Escuchá:** torch-y-sniffer.mp3 (2 min)

**La idea, en tres líneas**
- Ping y traceroute preguntan; Torch mira en vivo los flujos de una interfaz; el sniffer guarda paquetes en `.pcap` para Wireshark; `log=yes` en una regla dice qué se descarta.
- Torch y sniffer en la interfaz LAN (bridge), no en la WAN: del lado de afuera, después del NAT, todo tiene la IP del router.
- Torch ve los paquetes antes del firewall y apaga FastTrack mientras corre: prendelo, mirá y apagalo.

**Impacto:** pasás de "no anda" a "el paquete llega y nadie contesta" en cinco minutos, con evidencia para el ticket.

**Quién lo dice:** las fuentes de troubleshooting coinciden en el uso combinado (2 de 6 lo detallan: documentación de Torch y un caso de packet sniffer); ninguna discrepa.

**Laboratorio** · Campo · 15 min
En RouterOS 7, con una cámara o PC de ejemplo en 192.168.88.50:
1. Preguntar: ¿hay camino?
```routeros
/ping 8.8.8.8 count=5
/tool/traceroute 8.8.8.8
```
2. Mirar: ¿qué hace la cámara ahora?
```routeros
/tool/torch bridge src-address=192.168.88.50/32 duration=20s
/tool/torch bridge ip-protocol=tcp port=554
```
Si el tráfico de la cámara cae a cero a ratos, mirá cámara y cable; si fluye parejo, mirá el NVR.
3. Capturar: 30 segundos a archivo.
```routeros
/tool/sniffer/set file-name=camara.pcap file-limit=10000KiB
/tool/sniffer/start interface=bridge ip-address=192.168.88.50/32
/tool/sniffer/stop
/file/print where name~"pcap"
```
Si el archivo pesa 24 bytes, no capturó nada. Bajalo y abrilo en Wireshark (filtro `dns` o `rtsp`).
4. Registrar: log temporal en una regla de drop que sospeches.
```routeros
/ip/firewall/filter/set [find comment="defconf: drop invalid"] log=yes log-prefix="DROP-INV"
/log/print follow where message~"DROP-INV"
```
Cortá con `Ctrl+C` y volvé a dejar `log=no`.

⚠️ Torch y sniffer suben la CPU (apagan FastTrack) y una captura llena el disco rápido: en producción, duración corta, filtro y `file-limit`.

**Regla para quedarse**
No adivino: miro con Torch, y si no alcanza, capturo.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Torch en RouterOS 7.25: filtros, VLAN, DSCP y límites: https://manual.mikrotik.com/docs/7.25/diagnostics-monitoring-and-troubleshooting/torch
- Packet sniffer a Wireshark, con el caso del portal cautivo: https://admiralplatform.com/tips4tiks-packet-capture-with-mikrotik/
- Traceroute y Torch juntos: https://www.wirelessnetware.ca/blog/traceroute-torch-powerful-troubleshooting-duo/
