# Lección 40. Software y nube

**Escuchá:** software-y-nube.mp3 (2 min)

**La idea, en tres líneas**
- Nube y apps: SmartPlus App (residente: ver, hablar, abrir, llaves virtuales; lección 10) y My MobileKey (credencial Bluetooth con AES256, abre acercando la mano o con un botón, se integra con ACMS).
- PC y local: ACMS (control de acceso para pymes), ACMS Pro (empresa: estado de puertas, grupos, varios puestos, B/S y C/S), SDMC (gestión local de comunidades: despliegue por lotes, video, acceso, mensajes).
- Installer Kit Tool: sobre hardware S563W con PoE y Wi-Fi, junta la red de los equipos y sube el proyecto a la nube. El segundo bloque del firmware en `30` indica versión Akuvox con nube, SDMC y modo descubrimiento.

**Impacto:** cada obra arranca con el software que le corresponde, y no se descubre tarde que un equipo tiene firmware a medida.

**Quién lo dice:** 1 de 7 fuentes describe el software (la página de software de Akuvox); la guía de firmware de Akuvox explica el bloque B. Sin opiniones de terceros sobre ACMS o SDMC.

**Laboratorio** · Admin · 15 min
1. Elegí el software para tres casos y justificá en una línea:
```text
Casa con portero y monitor         : ________ (y plan B local, lección 10)
Edificio sin internet confiable    : ________
Oficina de 40 personas, 6 puertas  : ________
```
2. En un equipo de laboratorio, `Status > Basic > Product Information`: leé el firmware A.B.C.D.
```text
B = 30  -> versión Akuvox con nube, SDMC y descubrimiento
B = 31  -> sin logo, mismas funciones
otro    -> versión a medida: consultar antes de integrarla
```
3. Anotá en la ficha qué software administra cada equipo.
⚠️ Un equipo administrado por la nube y por un software local a la vez termina con dos fuentes de verdad: definí uno.

**Regla para quedarse**
Antes de elegir software, leo el bloque B del firmware y decido quién administra cada equipo.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Software de Akuvox para intercom y acceso: https://www.akuvox.com/productsSoftwareForIntercom
- Qué significa cada bloque del firmware: https://knowledge.akuvox.com/docs/upgrade-devices
- SmartPlus en la tienda y sus reseñas: https://play.google.com/store/apps/details?id=com.akuvox.mobile.smartplus&hl=en&gl=US&pli=1
