# Lección 19. Troncal SIP de Antel

**Escuchá:** troncal-sip-antel.mp3 (2 min)

**La idea, en tres líneas**
- La Troncal SIP de Antel (planes TSIP8 a TSIP180, sobre FTTH o fibra dedicada) llega en un puerto RJ45 con IP fija y sin usuario ni contraseña: en la UCM es un Peer SIP Trunk, no un Register.
- Antel manda OPTIONS para ver si la central está viva y espera un 200 OK: la UCM lo contesta si la IP de Antel es el Host Name del troncal y si el camino vuelve por el puerto de la troncal (modo Dual y ruta estática).
- Toda saliente lleva como caller ID un número de la troncal; si no, Antel la rechaza o la saca con el número por defecto del servicio.

**Impacto:** la troncal queda andando el día de la instalación, sin puertos abiertos a internet ni ALG en el medio, y los reclamos se hacen con el número de servicio y una captura.

**Quién lo dice:** 3 de 3 fuentes que describen la troncal de Antel (Simpletech, un hilo de 3CX de 2017 y uno de FreePBX de 2022) coinciden en que va por IP, sin registro y con OPTIONS de Antel; la página de Antel no publica datos técnicos, y ninguna fuente dice en qué formato llega el número entrante.

**Laboratorio** · Foco · 25 min
Con la troncal real o, si todavía no la tenés, con otra UCM o un Asterisk de laboratorio que haga de Antel (al final). Todos los datos son de ejemplo: los reales salen de la planilla de Antel.
1. Juntá la planilla antes de ir a la obra y pedí por escrito lo que falte:
```text
Número de servicio:  P00000 (de ejemplo; es el que pide el 0800 2599)
Plan:                TSIP8 = 8 llamadas simultáneas
IP del cliente:      198.51.100.2   máscara 255.255.255.252
Gateway de Antel:    198.51.100.1
Servidor SIP:        203.0.113.10   puerto 5060 UDP   (no contesta ping)
Redes de Antel a rutear (señalización y audio): 203.0.113.0/24
IP de prueba que sí contesta ping: la que indique Antel
Números:             2900 1001 a 2900 1008 (de ejemplo)   número por defecto: 2900 1001
Codecs: G.711 y T.38   DTMF: RFC 2833 o inband   Session Expire: 600
Formato del número entrante y del saliente (8 cifras, 598, 09): pedilo o miralo en la primera llamada
```
2. Pasá la UCM a modo Dual. La red del cliente queda en el puerto WAN (LAN2, con su gateway) y la troncal de Antel va al puerto LAN (LAN1), sin gateway:
```text
System Settings > Network Settings > Basic Settings
Method: Dual   Default Interface: LAN2
LAN1 (puerto LAN):  Static  198.51.100.2 / 255.255.255.252  (sin gateway)
LAN2 (puerto WAN):  la IP de la central en la red del cliente, con su gateway
```
⚠️ Cambiar el modo de red reinicia la central y puede dejarte sin acceso web: backup antes, hacelo en sitio, y desenchufá antes lo que estuviera colgado del puerto LAN.
3. Agregá la ruta estática hacia las redes de Antel, así lo que va a Antel sale por el puerto de la troncal y no por el router del cliente:
```text
System Settings > Network Settings > Static Routes > Add IPv4 Static Route
Destination: 203.0.113.0   Subnet Mask: 255.255.255.0
Gateway: 198.51.100.1      Interface: LAN (eth0)
```
Para probar el camino sin la central: una notebook con 198.51.100.2/30 y gateway 198.51.100.1 en el cable de Antel, y ping a la IP de prueba (el servidor SIP no contesta ping).
4. Creá el troncal por IP:
```text
Extension/Trunk > VoIP Trunks > Add
Type: Peer SIP Trunk     Provider Name: Antel_Troncal
Host Name: 203.0.113.10  Transport: UDP     NAT: No
Keep Trunk CID: Sí       CallerID Number: 29001001
Codec Preference: PCMA, PCMU   (sacá el resto)
Advanced: DTMF Mode RFC4733   DID Mode: Request-line
          Enable Heartbeat Detection: Sí (60 s)
          Max Concurrent Calls: 8   Response to Blocked Call: 486
```
Con Keep Trunk CID en Sí todas las salientes muestran el 2900 1001; si cada interna sale con su número directo, DOD por interna y Keep Trunk CID en No. Sumá 203.0.113.0/24 a la Allowlist de Fail2ban (lección Central cerrada), así un error de configuración no banea a Antel. Si la central ya tiene External Host por internos remotos (lección Interno remoto), sumá 203.0.113.0/24 y 198.51.100.0/30 a Local Network Address en PBX Settings > SIP Settings > NAT: así a Antel le habla con 198.51.100.2 y no con la IP pública.
5. Mirá el estado y el OPTIONS de Antel. En System Status > Dashboard > Trunks el troncal no tiene que quedar Unreachable. Después, una captura de dos o tres minutos en Maintenance > Network Troubleshooting > Ethernet Capture sobre la interfaz LAN: tienen que aparecer los OPTIONS de Antel y el 200 OK de la UCM.
```text
sip.Method == "OPTIONS" || sip.Status-Code
```
Si al OPTIONS de Antel la UCM contesta 401 o 404, o no contesta, ese OPTIONS vino de una IP que no es el Host Name: pedile a Antel todas sus IP de señalización. Si el troncal queda Unreachable pero los OPTIONS de Antel tienen su 200 OK, Antel no está contestando los de la UCM: apagá el heartbeat y anotalo en la ficha.
6. Armá la entrada en dos tiempos. Primero una ruta que agarre todo y mande a una interna de prueba; llamá desde un celular al 2900 1001 y mirá en CDR, o en la captura (Request-URI y To), qué número llegó:
```text
Extension/Trunk > Inbound Routes > Antel_Troncal > Add
Pattern: _X.   Default Destination: Extension 1001
```
Con el formato a la vista, la ruta definitiva (lección Cada DID): si llega 29001001, patrón `_2900100X` con By DID y Strip 4 (suena la 1001); si llega 59829001001, patrón `_5982900100X` con Strip 7. El número principal, al grupo o al IVR.
7. Armá la salida con el plan de Uruguay y una ruta internacional aparte con PIN (lección Patrón y privilegio):
```text
Outbound Routes > Add   Calling Rule Name: Uruguay   Use Trunk: Antel_Troncal
Pattern:  _2XXXXXXX   fijos de Montevideo
          _4XXXXXXX   fijos del interior
          _09XXXXXXX  celulares (0 más el número)
          _0800XXXX   sin cargo
          _911        emergencias (sin PIN, privilegio Internal)
          _10X        104 Bomberos, 105 Salud Pública, 109 Policía
Internacional: _00.  en otra ruta, privilegio International y PIN
0900 a 0908: valor agregado; con PIN o sin ruta
```
8. Probá como lo entrega Antel: saliente a un fijo y a celulares de Antel y de otra compañía (el celular tiene que mostrar 2900 1001, o el DOD de la interna si lo usás), entrante desde un celular, una tecla en el buzón, dos llamadas a la vez y una de más de 10 minutos. Si Antel contesta 403 a una saliente, mirá el From en la captura: casi siempre sale el número de la interna y no uno de la troncal. Si contesta 404 o 484, mirá el número del Request-URI.
⚠️ El 911 no se prueba llamando: se revisa que el patrón exista, no pida PIN y salga por la troncal.

Sin troncal de Antel: armá el mismo escenario con una segunda UCM (o un Asterisk) que hace de Antel. Dale 198.51.100.1/30, conectala con un cable al puerto LAN de la tuya y, en tu UCM, usá 198.51.100.1 como Host Name (sin ruta estática: es la red conectada). En la otra central, un Peer SIP Trunk hacia 198.51.100.2 con heartbeat, que manda OPTIONS como Antel; una ruta saliente `_2900100X` hacia ese troncal y una entrante `_X.` a una interna para lo que mande la tuya. Lo que cambia con la real: con Antel no controlás el otro lado, así que el formato del número, las IP de origen y la respuesta a tus OPTIONS se confirman con la captura de la primera llamada.

**Regla para quedarse**
La troncal de Antel se pide por escrito, se conecta directo a la central y se da por terminada con una captura donde se ve el OPTIONS de Antel con su 200 OK y una saliente con el número de la troncal.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Planes y condiciones de la Troncal SIP de Antel: https://antel.com.uy/empresas/internet-y-fija/planes/troncal-sip
- Guía de implementación de un integrador uruguayo (datos, topologías, pruebas): https://www.simpletech.uy/en/troncal-sip-empresarial-antel-uruguay/
- El 401 a los OPTIONS de Antel en un caso real: https://community.freepbx.org/t/antel-sip-trunk-only-options/84614
- Peer SIP Trunk entre dos UCM, para el laboratorio: https://documentation.grandstream.com/knowledge-base/how-to-interconnect-multiple-ucm/
- Plan de numeración de Uruguay notificado a la UIT: https://www.itu.int/dms_pub/itu-t/oth/02/02/T02020000E00001PDFS.pdf
