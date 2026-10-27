# Lección 29. E21 y E20S

**Escuchá:** e21-y-e20s.mp3 (2 min)

**La idea, en tres líneas**
- E21 ("intercomunicador de emergencia SIP con video"): acero inoxidable, sin pantalla, Linux, cámara, ONVIF e IP65 según la guía; sin PIN, tarjeta ni Wiegand (versiones E21V y E21A). Relé 30 V 3 A; PoE 802.3af o 12 V 1 A; sin salida de 12 V; tres versiones de hardware.
- E20S ("intercomunicador de emergencia SIP"): solo PoE 802.3af según la tabla, sin fuente opcional ni salida de 12 V; no figura en la guía de selección, así que cámara y protección no se afirman.
- IP: E21 manteniendo el pulsador 5 s; E20S se enciende y conecta, y la IP se busca con IP Scanner o en el DHCP.

**Impacto:** el punto de emergencia queda registrado en la central, con destino de respaldo y la cámara del E21 grabando en el NVR.

**Quién lo dice:** 2 de 10 fuentes coinciden en sacar la IP por el método de la familia y leer el firmware; las tablas de métodos, alimentación y 12 V completan. Sin ficha propia leída de E21 ni E20S.

**Laboratorio** · Rápido · 10 min
1. Conectá el E21 a PoE 802.3af y mantené el pulsador 5 s para escuchar la IP.
2. Registralo como extensión en la central de laboratorio (lección 5): `Account > Basic`, extensión `801`.
3. Configurá el botón para llamar al interno de guardia y probá la llamada.
4. En la central, armá el respaldo si nadie atiende:
```text
801 (E21 estacionamiento) -> interno 200 guardia
  sin respuesta en 20 s  -> cola o celular de guardia
```
5. Sumá la cámara del E21 al NVR por ONVIF o RTSP con credenciales propias (lección 9).
⚠️ Un botón de emergencia sin destino de respaldo es peor que no tenerlo: probá también el caso sin respuesta.

**Regla para quedarse**
Todo botón de emergencia tiene un destino que atiende y un respaldo si no atiende.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía de selección de porteros (fila del E21): https://www.akuvox.com/productSelectionGuide?cid=3
- Alimentación por modelo (E21 y E20S): https://knowledge.akuvox.com/docs/power-supply-for-intercom-devices
- Registro SIP en una central, ejemplo con Yeastar: https://help.yeastar.com/en/p-series-appliance-edition/integrations/akuvox/manually-register-akuvox-intercom-device-with-yeastar-p-series-pbx-system.html
