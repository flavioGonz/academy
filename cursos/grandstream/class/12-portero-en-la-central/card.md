# Lección 12. Portero en la central

**Escuchá:** portero-en-la-central.mp3 (2 min)

**La idea, en tres líneas**
- El GDS37xx se registra en la UCM como una extensión más; el timbre llama a una interna o a un grupo.
- Apertura con Remote PIN por DTMF (Enable DTMF Open Door) o con la tecla OpenDoor del GRP, que manda un mensaje SIP.
- Video según el teléfono: GRP2601 a 2604, 2612 y 2613 solo audio; GRP2614 en adelante con imagen.

**Impacto:** la puerta se atiende y se abre desde cualquier teléfono del grupo, con un PIN propio y registro en la central.

**Quién lo dice:** 3 de 3 fuentes coinciden (guía GDS37xx con GRP26xx, blog de Grandstream sobre GDS3710, manual del UCM630x); sin discrepancias. Los porteros GSC no tienen fuente propia en lo leído.

**Laboratorio** · Campo · 20 min
1. En la UCM, creá la extensión 8001 para el portero (contraseña aleatoria) y un grupo de llamada 6000 con recepción y seguridad.
2. En el GDS3710, registrá la cuenta:
```text
Account > Account 1
SIP Server: 192.168.88.20
SIP User ID / Authenticate ID: 8001
Authenticate Password: (la de la extensión 8001)
```
3. Timbre y apertura:
```text
Door System Settings > Basic Settings
Doorbell Mode: Call Doorbell Number
Number Called When Door Bell Pressed: 6000
Enable DTMF Open Door: Sí
Remote PIN to Open the Door: 4829   (de ejemplo; usá uno propio)
```
Revisá que la salida de alarma que maneja la cerradura esté en modo Open Door.
4. En el GRP (cuenta de recepción), agregá el portero como acceso con el número 8001 y el mismo PIN para la tecla OpenDoor.
5. Tocá el timbre, atendé, marcá el PIN y verificá la apertura. Probá también OpenDoor sin atender.
⚠️ Probá la cerradura con la puerta abierta o con alguien del lado de adentro: un relé mal configurado puede dejar la puerta trabada o abierta.

**Regla para quedarse**
El PIN de apertura no es el de fábrica, ni el del buzón, ni uno que adivine cualquiera.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía oficial GDS37xx con GRP26xx (peer y vía UCM): https://documentation.grandstream.com/knowledge-base/connecting-gds37xx-with-grp26xxx/
- Integración del GDS3710 con la solución Grandstream: https://blog.grandstream.com/company/news/blog/get-more-gds3710-integrating-it-your-grandstream-solution
