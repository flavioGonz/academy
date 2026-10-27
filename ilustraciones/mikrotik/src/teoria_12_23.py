"""Textos 'Un poco de historia / Cómo funciona' (teoria_md) para MikroTik 12 a 23."""

T = {}

T["12"] = """### Un poco de historia
Las herramientas de diagnóstico de red son casi tan viejas como internet. `ping` lo escribió Mike Muuss en 1983 y usa el mensaje ICMP echo, definido en el RFC 792 de 1981. `traceroute` apareció a fines de los ochenta, de la mano de Van Jacobson, con un truco simple: mandar paquetes con TTL cada vez mayor y anotar quién avisa que se le terminó. En la misma época, en el laboratorio de Berkeley nació `tcpdump` y su biblioteca libpcap, que fijaron el formato `.pcap` que todavía usamos. Wireshark empezó en 1998 como Ethereal y cambió de nombre en 2006.

RouterOS juntó estas ideas dentro del router: ping y traceroute para preguntar, Torch para mirar en vivo y el packet sniffer para guardar un `.pcap` que se abre en Wireshark.

### Cómo funciona
**Ping y traceroute generan tráfico.** Mandan paquetes de prueba y esperan respuesta: te dicen si hay camino y hasta qué salto llega, pero no qué hace un equipo en ese momento.

**Torch no genera nada.** Lee los paquetes que recibe una interfaz y los agrupa en flujos: origen, destino, protocolo, puerto y tasa. Los ve antes del firewall, por eso muestra también lo que después se descarta. Para verlos todos, mientras corre apaga FastTrack y fast path, y la CPU trabaja más.

**Dónde mirar importa.** Del lado de la LAN cada equipo tiene su IP (192.168.88.50 es la cámara). Del lado de la WAN, el masquerade ya reescribió el origen y todo sale con la IP del router: ahí no sabés quién es quién.

**El sniffer copia paquetes enteros.** Con `ip-address=192.168.88.50/32` solo guarda los de ese equipo, y `file-limit` evita que llene el disco. Un `.pcap` vacío pesa 24 bytes: es solo la cabecera del archivo, sin paquetes.

**El log cierra el círculo.** Torch no sabe qué hace el firewall; una regla de drop con `log=yes` escribe una línea por cada paquete que descarta, con el prefijo que elijas. Por eso el orden es: preguntar, mirar, capturar y, si hace falta, registrar."""

T["13"] = """### Un poco de historia
IPv4 quedó definido en el RFC 791 de 1981. Al principio las redes se repartían en clases fijas (A, B y C), un sistema que desperdiciaba direcciones. En 1993 llegó CIDR (RFC 1519) y con él la notación de prefijo que usás hoy: `/29`, `/24`, `/27`. Gracias a eso un proveedor puede darle a una empresa un bloque chico, como las 29 IPs públicas (un `/27`) del Internet corporativo de Antel, o una sola IP fija como en Internet pyme.

El DNS es de 1987 (RFC 1034 y 1035) y reemplazó a un archivo de nombres que se copiaba a mano entre máquinas. Las IPs de los ejemplos, 203.0.113.x, 198.51.100.x y 192.0.2.x, son rangos reservados para documentación (RFC 5737): nunca aparecen en internet de verdad.

### Cómo funciona
**La máscara define el vecindario.** `203.0.113.10/29` quiere decir que los primeros 29 bits son la red. Un `/29` tiene 8 direcciones: 203.0.113.8 es la red, 203.0.113.15 es broadcast y de la .9 a la .14 son usables. El gateway .9 está en el mismo vecindario, por eso el router lo alcanza directo por ether1. Con la máscara mal puesta, el gateway queda "afuera" y el primer ping falla.

**La ruta por defecto es el plan B de todo paquete.** `0.0.0.0/0` coincide con cualquier destino. Cuando el router no tiene una ruta más específica, manda el paquete al gateway. Sin esa ruta, el router llega a su vecino pero no a internet: el segundo ping falla.

**El DNS traduce nombres a IPs.** El router pregunta a los servidores de `/ip/dns` (1.1.1.1 y 9.9.9.9 en el ejemplo). Si los pings a IPs andan pero `:resolve` no, el problema es solo de nombres.

**Masquerade y la IP fija.** La documentación de NAT explica que masquerade está pensado para IP dinámica: al caer la interfaz borra las conexiones. Con IP fija también funciona; src-nat es la alternativa que conserva las conexiones tras un corte.

Por eso la verificación va en ese orden: vecino, mundo, nombres."""

T["14"] = """### Un poco de historia
Antes de DHCP existía BOOTP (RFC 951, de 1985), pensado para que máquinas sin disco arrancaran por red: el administrador cargaba a mano una tabla con cada MAC y su IP. En 1993 apareció DHCP, y la versión que se usa hoy es el RFC 2131 de 1997. La gran novedad fue el **lease**: la dirección se presta por un tiempo y vuelve al pool si nadie la renueva.

Con los años se sumaron opciones. La opción 121 (RFC 3442, de 2002) permite mandar rutas completas y, cuando está, el cliente ignora el gateway de la opción 3. También se reservaron rangos: los privados del RFC 1918 (1996: 10.0.0.0/8, 172.16.0.0/12 y 192.168.0.0/16) y el 100.64.0.0/10 (RFC 6598, de 2012), que los proveedores usan para CGNAT cuando no les alcanzan las IPv4 públicas.

### Cómo funciona
**Cuatro mensajes.** El cliente grita *Discover* por broadcast, el servidor responde *Offer*, el cliente pide esa oferta con *Request* y el servidor confirma con *Ack*. En RouterOS ese final es el estado `bound`.

**Lo que viene en el Ack.** La dirección con su máscara, el gateway (opción 3), los DNS (opción 6), los NTP (opción 42) y el tiempo de lease. El cliente de RouterOS instala todo como dinámico; `use-peer-dns` y `use-peer-ntp` deciden si usa los DNS y NTP recibidos.

**Renovar antes de perder.** A mitad del lease el cliente pide renovar al mismo servidor; si no contesta, más adelante lo intenta con cualquiera. Si el lease vence sin renovación, la dirección y las rutas dinámicas se borran. `renew` fuerza ese pedido en el momento.

**Distancia: quién gana.** Cada ruta por defecto lleva una distancia. Gana la menor; con distancias iguales las dos quedan activas y el tráfico se reparte (ECMP). Por eso el respaldo va con `default-route-distance=2`.

**Leer el doble NAT.** Si la address recibida es privada o está en 100.64.0.0/10, hay alguien más haciendo NAT adelante. IP Cloud te muestra la `public-address` que ve internet: si no coincide con ether1, el acceso remoto directo no va a llegar."""

T["15"] = """### Un poco de historia
PPP nació para enlaces punto a punto, como los módems telefónicos: autenticaba al usuario y le entregaba una IP. La versión que se usa es el RFC 1661 de 1994. Cuando llegó la banda ancha por ADSL, los proveedores quisieron seguir cobrando y controlando por usuario y contraseña, pero sobre Ethernet. De ahí salió PPPoE, el RFC 2516 de 1999: PPP dentro de tramas Ethernet.

Con la fibra hasta el hogar, el equipo del cliente pasó a ser un ONT. Antel lo entrega en modo router o en modo puente, y el cambio se pide por MiAntel o al 121. Un instructivo de un proveedor uruguayo sugiere que Antel autentica por PPPoE (lo muestra en ADSL); para la fibra con el ONT en puente, ninguna fuente leída confirma si hace falta VLAN, y por eso el laboratorio la deja a confirmar.

### Cómo funciona
**Primero se busca al concentrador.** PPPoE arranca con una fase de descubrimiento: el cliente manda PADI por broadcast, el concentrador del proveedor contesta PADO (ahí viene el `ac-name` que ves en `scan`), el cliente pide con PADR y el concentrador confirma con PADS y un número de sesión. Si el `scan` no muestra ningún `ac-name`, ningún concentrador contestó el PADI; una causa posible es que el servicio lleve VLAN.

**Después, PPP.** Dentro de la sesión se negocia el enlace (LCP), se autentica con usuario y contraseña y se asigna la IP (IPCP). Esa IP queda en la interfaz lógica `pppoe-antel`, no en ether1. Por eso masquerade y la lista WAN tienen que apuntar a la interfaz PPPoE.

**Los 8 bytes.** Cada trama lleva 6 bytes de cabecera PPPoE y 2 de PPP. En una Ethernet de 1500 bytes de carga quedan 1492 para el paquete IP: ese es el `max-mtu`.

**MSS: el arreglo práctico.** TCP anuncia en el SYN el segmento máximo que acepta (MSS). Con MTU 1492 el MSS correcto es 1452 (1492 menos 40 de cabeceras IP y TCP). Si una PC anuncia 1460 y en el camino nadie avisa por ICMP que el paquete no entra, las conexiones se cuelgan a medias. `change-mss` con `clamp-to-pmtu` corrige el valor en el SYN y el problema desaparece.

**Al reconectar.** Cada sesión nueva puede traer otra IP; por eso el acceso remoto se resuelve con DDNS o con un túnel."""

T["16"] = """### Un poco de historia
MikroTik nació en Riga, Letonia, en 1996, y RouterOS es su sistema, basado en Linux. Desde el principio se distribuyó en paquetes `.npk` que solo MikroTik puede crear. En RouterOS 6 muchas funciones venían en paquetes separados; en RouterOS 7, que salió estable en 2021, casi todo quedó dentro del paquete principal `routeros`, y como extras quedaron cosas que no todos usan: container, zerotier, iot, user-manager y los drivers de radio.

Desde la 7.13 el WiFi se separó en dos paquetes: `wifi-qcom` para equipos 802.11ax y `wireless` para la generación anterior, que no pueden estar activos a la vez. Desde la 7.23 el chequeo de actualizaciones usa HTTPS, así que el router necesita salir por TCP 443.

### Cómo funciona
**Qué es un paquete.** Un `.npk` es un archivo con el software de una función, compilado para una arquitectura de CPU (arm, arm64, mipsbe, mmips, x86, entre otras). Un `.npk` de otra arquitectura no le sirve a tu equipo; por eso primero mirás `architecture-name` en System > Resources.

**Cómo se instala.** RouterOS no reemplaza paquetes en caliente: los deja preparados y los aplica en el arranque siguiente. Por eso actualizar, habilitar un extra o hacer downgrade siempre termina en un reinicio. Download deja la versión lista y espera; Download&Install reinicia sola. Un `.npk` soltado en la raíz de Files se toma en el próximo arranque; dentro de una carpeta, no.

**Volver atrás.** Por defecto RouterOS no instala una versión más vieja al reiniciar. `/system/package/downgrade` le indica que sí lo haga con los `.npk` anteriores que subiste, y reinicia.

**RouterBOOT, el que arranca todo.** Antes que RouterOS corre RouterBOOT, el cargador de arranque grabado en la memoria del RouterBOARD. Cada versión de RouterOS trae su RouterBOOT, pero no lo graba sola: `/system/routerboard/upgrade` lo deja listo y en el siguiente reinicio queda activo. Se actualiza el principal; el de respaldo se conserva para recuperar el equipo si algo sale mal.

**El log cuenta lo que pasó.** Si un paquete no se instaló, `/log/print` dice por qué."""

T["17"] = """### Un poco de historia
Durante años MikroTik usó otros nombres para sus ramas de RouterOS. Un distribuidor británico, LinITX, las explicaba en 2018 como *bugfix only*, *current*, *release candidate* y *legacy*, y ya entonces recomendaba la rama de solo arreglos para routers de producción y la candidata nunca. Hoy los canales se llaman **long-term**, **stable**, **testing** y **development**, y la idea de fondo es la misma: cuanto más nuevo, menos probado.

Es la misma lógica que usan muchos proyectos de software con versiones de soporte extendido: una rama que cambia poco y se arregla mucho, para quien necesita estabilidad, y otra que avanza rápido, para quien necesita funciones nuevas.

### Cómo funciona
**Cuatro ritmos.** Según la documentación de actualización: long-term sale poco y solo con arreglos críticos, sin funciones nuevas dentro de su rama; stable sale cada pocos meses con funciones nuevas ya probadas; testing sale cada pocas semanas con una prueba interna básica y no va en producción; development es para probar lo que viene.

**El canal es solo una preferencia.** Cambiar de canal no instala nada. Le dice al router qué lista de versiones consultar cuando hacés `check-for-updates`. Por eso podés pasar de long-term a stable, mirar `latest-version` y volver, sin tocar el equipo. Esa comparación es lo que hace el paso 2 del laboratorio.

**También sirve para bajar.** Si el canal elegido ofrece una versión más vieja que la instalada, Check for Updates la instala igual: es una forma de volver de stable a long-term sin subir archivos. Antes, siempre backup.

**Desde la 6, un escalón.** Un equipo con RouterOS 6 no ve directamente la última versión 7: primero aparece una intermedia (7.12.1) y recién después las nuevas.

**Automático, con cuidado.** La documentación ofrece un script de scheduler que instala solo cuando sale una versión en el canal. En un banco de pruebas está bien; en un cliente instala algo que vos no probaste. Por eso la recomendación del curso es long-term en clientes, todos los equipos del mismo cliente en el mismo canal, y lo nuevo primero en tu banco."""

T["18"] = """### Un poco de historia
El DNS se pensó para datos que cambian poco: un nombre, una IP, y caches que guardan la respuesta durante horas. Cuando las conexiones domésticas empezaron a recibir IPs dinámicas, hizo falta poder actualizar un nombre cada vez que la IP cambiaba. El estándar para eso es DNS UPDATE (RFC 2136, de 1997), y alrededor de esa idea aparecieron los servicios de DNS dinámico.

MikroTik armó el suyo dentro de IP Cloud: cada router puede registrar un nombre `<serie>.sn.mynetname.net`, hablando con sus servidores por un protocolo propio sobre UDP 15252. Con el tiempo IP Cloud sumó la hora aproximada al arrancar y, más tarde, Back To Home. La hora precisa sigue siendo trabajo de NTP, un protocolo de David Mills cuya versión actual es el RFC 5905 de 2010.

### Cómo funciona
**El router avisa, la nube mira.** Con `ddns-enabled=yes`, el router manda un mensaje a cloud2.mikrotik.com. El servidor no confía en lo que el router dice: anota la IP de origen desde la que le llegó el mensaje. Esa es la `public-address`. Si hay un NAT adelante, la IP anotada es la del equipo que hace NAT, no la de ether1.

**Por qué cada minuto.** Si la IP pública está en una interfaz del router, RouterOS ve cuando cambia y avisa. Detrás de NAT no la puede ver, así que manda una actualización por minuto. `force-update` la manda en el acto.

**TTL de 60 segundos.** Cada respuesta DNS dice cuánto tiempo puede guardarse en cache. Con 60 segundos, cuando la IP cambia, en un minuto los demás preguntan de nuevo y ven la nueva.

**Con dos WAN.** El mensaje a la nube sale por la ruta que tenga en ese momento el router hacia cloud2. Si se cae la principal, sale por la otra y la nube anota la IP nueva: el nombre la sigue.

**Nombre no es acceso.** Resolver el nombre te da una IP; llegar a un servicio depende del firewall y de que esa IP sea realmente del router. Detrás de CGNAT la IP es compartida por muchos clientes del proveedor y no lleva a tu equipo.

**La hora.** `update-time` pone una hora aproximada al arrancar solo si el cliente NTP está apagado. NTP mide la demora de ida y vuelta con el servidor y ajusta el reloj con precisión, que es lo que piden los logs y las SA de IPsec."""

T["19"] = """### Un poco de historia
WireGuard es una VPN creada por Jason Donenfeld con una idea fija: poco código, criptografía moderna sin opciones para elegir y configuración mínima. Entró al kernel de Linux en la versión 5.6, en 2020, y RouterOS 7 lo incorporó como interfaz propia.

El problema que quedaba era de red, no de cifrado: un servidor VPN necesita que el cliente pueda llegar a él, y cada vez más sitios están detrás de CGNAT o de doble NAT. MikroTik respondió con Back To Home, que arma el servidor WireGuard por vos y, si el router no es alcanzable desde internet, lo conecta a través de relays propios. Funciona en CPU ARM, ARM64 o TILE con RouterOS 7.12 o posterior; los RouterBOARD MIPS y PPC no están soportados.

### Cómo funciona
**Claves en lugar de usuarios.** En WireGuard cada punta tiene un par de claves. El servidor conoce la clave pública de cada cliente y, para cada una, qué direcciones puede usar dentro del túnel. Si llega un paquete firmado con una clave que no conoce, lo ignora sin responder. Por eso cada celular es un usuario distinto: borrar su clave es darlo de baja.

**Lo que crea RouterOS.** Al activarlo, aparece la interfaz `back-to-home-vpn` con 192.168.216.1/24, reglas dinámicas de input, masquerade y forward, y el nombre `<serie>.vpn.mynetname.net`. `show-client-config` genera la configuración del cliente y un QR con todo eso adentro.

**Directo o por relay.** Si el router tiene IP pública, el celular le habla directo. Si no, el router mantiene abierta una conexión saliente hacia el relay de MikroTik más cercano, y el celular entra por ahí. El relay solo pasa paquetes: las claves están en el router y en el celular, así que no puede leer el tráfico. Al dar una vuelta más, puede ir más lento. `vpn-relay-ipv4-status` te dice cuál de los dos caminos se usa.

**Con LAN o sin LAN.** `allow-lan=no` (por defecto) deja al usuario salir a internet a través del router, pero no tocar la red local. La restricción se apoya en la lista de interfaces LAN: si una red local tuya no está en esa lista, no queda protegida. Con `allow-lan=yes` y `client-allowed-address` acotás a qué redes llega.

**Revocar es empezar de cero.** `revoked-and-disabled` borra todas las claves; al reactivar hay claves y puerto nuevos y cada equipo se configura otra vez."""

T["20"] = """### Un poco de historia
RouterOS siempre corrió en RouterBOARD, pero MikroTik también ofreció versiones para PC. CHR (Cloud Hosted Router) es la edición pensada para máquinas virtuales: la misma configuración y los mismos comandos, sobre un hipervisor o un VPS. A diferencia de un RouterBOARD, la licencia de CHR limita la velocidad: Free sin vencimiento con 1 Mbps de subida por interfaz, y niveles pagos P1 (1 Gbps, 45 dólares), P10 (10 Gbps, 95) y P-Unlimited (250), con prueba de 60 días.

El patrón de concentrador, también llamado *hub and spoke*, es anterior a cualquier marca: un punto central con IP pública al que se conectan todas las sucursales. Con la llegada de CGNAT se volvió casi obligatorio, porque un sitio sin IP pública no puede recibir conexiones, pero sí puede iniciarlas.

### Cómo funciona
**Instalación.** En un VPS se arranca el sistema de rescate, se baja la imagen raw del CHR y se escribe con `dd` sobre el disco. Al reiniciar, el VPS ya es un MikroTik: con usuario `admin` sin contraseña y en una IP pública. Por eso el endurecimiento va primero.

**Por qué el túnel saliente atraviesa el CGNAT.** Cuando el router del sitio manda un paquete al CHR, el NAT del proveedor anota la conexión (IP interna, puerto, IP externa) y deja pasar las respuestas que vuelven por ese mismo camino. El CHR no inicia nada: responde a una conexión que el sitio abrió.

**El keepalive mantiene la puerta abierta.** Esas anotaciones del NAT vencen si no pasa tráfico por un rato. `persistent-keepalive=25s` hace que el sitio mande un paquete chico cada 25 segundos, así el camino sigue abierto y el hub puede llegar al sitio cuando quieras entrar.

**Quién lleva qué.** El sitio tiene `endpoint-address` y `endpoint-port` del CHR porque es el que llama. El hub no tiene endpoint: aprende de dónde viene cada peer. `allowed-address` funciona como tabla de ruteo del túnel: en el hub, cada sitio tiene su `/32`; en el sitio, el rango completo 10.10.10.0/24 va hacia el hub.

**Licencia y uso.** Con Free, cada interfaz sube a 1 Mbps: suficiente para WinBox y monitoreo, no para video. Clonar el CHR no reinicia la prueba, e IP Cloud pide licencia paga."""

T["21"] = """### Un poco de historia
En los noventa Microsoft popularizó PPTP para conectar notebooks a la oficina; con los años su cifrado quedó roto y hoy no se usa. En paralelo, el IETF definió L2TP (RFC 2661, de 1999), que lleva sesiones PPP por una red IP pero sin cifrar nada. La solución estándar fue meter L2TP dentro de IPsec, descrita en el RFC 3193 de 2001. Así nació la combinación L2TP/IPsec que Windows, macOS, iOS y Android traen incorporada.

Quedaba un problema: IPsec original no atravesaba bien los routers con NAT. En 2005 se publicó NAT Traversal (RFC 3947 y 3948), que encapsula IPsec dentro de UDP 4500. Windows, por defecto, no lo usa hacia servidores detrás de NAT, y de ahí sale la clave de registro AssumeUDPEncapsulationContextOnSendRule.

### Cómo funciona
**Tres capas, cada una con su trabajo.** IPsec cifra y protege; L2TP arma el túnel; PPP identifica a la persona y le da una IP. Cuando conectás, el orden es de afuera hacia adentro.

**1. IPsec negocia.** Cliente y servidor hablan por UDP 500 (IKE), se autentican con la clave precompartida (`ipsec-secret`) y acuerdan cómo cifrar. Si detectan un NAT en el medio, pasan a UDP 4500. En RouterOS, `use-ipsec=required` crea por su cuenta un peer dinámico con NAT-T activo y rechaza L2TP sin IPsec.

**2. Los datos van en ESP.** ESP es un protocolo IP propio (el número 50), no TCP ni UDP. Por eso en el firewall se abre como `protocol=ipsec-esp`. Con NAT-T, el ESP viaja dentro de UDP 4500.

**3. L2TP por UDP 1701.** Dentro del canal cifrado se arma el túnel L2TP. El puerto 1701 tiene que estar abierto en input, aunque el tráfico ya llegue protegido.

**4. PPP autentica.** Por último, el usuario y la contraseña del `/ppp/secret` (con `service=l2tp`) y la IP: `local-address` para el router y una del pool para el cliente. El perfil puede dar DNS.

**Forward y FastTrack.** El tráfico que sale del túnel hacia la LAN pasa por forward. Si FastTrack lo toma, saltea las políticas IPsec; por eso va una regla `accept` con `ipsec-policy=in,ipsec` arriba del `fasttrack-connection`.

**El caso Windows.** El valor de la clave de registro dice cuándo Windows acepta NAT-T: 0 por defecto, 1 si el servidor está detrás de NAT, 2 si servidor y cliente lo están. Después de cambiarlo, reinicio."""

T["22"] = """### Un poco de historia
IPsec nació en el IETF a mediados de los noventa, como parte del trabajo de seguridad para IPv6, y se adaptó a IPv4. La arquitectura actual es el RFC 4301 de 2005. Para acordar claves se usa IKE: la primera versión es de 1998 (RFC 2409) y la segunda, IKEv2, apareció en 2005 y hoy está en el RFC 7296 de 2014. Detrás de todo está el intercambio de Diffie y Hellman, de 1976, que permite acordar un secreto sobre una red que cualquiera puede escuchar. Los "grupos DH" son los tamaños de ese intercambio: el grupo 14 es el de 2048 bits (modp2048, RFC 3526).

Al ser un estándar, IPsec es lo que hablan casi todas las marcas: MikroTik, pfSense, Fortinet, Cisco. Lo difícil no es la tecnología sino que cada fabricante nombra distinto los mismos parámetros.

### Cómo funciona
**Fase 1: conocerse.** Los dos peers se encuentran por UDP 500 (4500 con NAT), acuerdan cifrado, hash y grupo DH, y se autentican con la clave o el certificado. El resultado es un canal seguro para seguir negociando. En RouterOS esa fase vive en `profile`, `peer` e `identity`, y se ve en `active-peers`.

**Fase 2: las SA.** Por ese canal acuerdan cómo se cifra el tráfico real: protocolo ESP, cifrado, hash, PFS y lifetime (`proposal`). El resultado son **SA**, acuerdos de un solo sentido identificados por un número (SPI). Un túnel sano tiene dos por router, una de ida y otra de vuelta: eso muestra `installed-sa`.

**Las policies deciden qué entra.** Una policy dice: el tráfico de 192.168.88.0/24 hacia 10.10.10.0/24 se cifra con tal SA. El otro extremo tiene la misma regla al revés. Si las redes no son espejo exacto, la fase 2 no se arma.

**Dónde chocan NAT y FastTrack.** El router decide si cifrar mirando la policy después del srcnat. Si el masquerade ya cambió el origen a la IP pública, el paquete no coincide y sale sin cifrar; por eso la regla `accept` de NAT va arriba de todo. FastTrack, en cambio, acelera conexiones establecidas salteando ese chequeo: de ahí el bypass en forward y el síntoma de "se arregla con Torch".

**Por qué el reloj importa.** Una guía de practicantes advierte que IPsec es sensible a la diferencia de reloj: con relojes desfasados las SA vencen y el túnel se cae. Con NTP en las dos puntas, además, los logs de los dos lados coinciden y se pueden comparar."""

T["23"] = """### Un poco de historia
Cambiar la configuración de un router a distancia siempre tuvo el mismo riesgo: un cambio que corta tu propia conexión y deja el equipo accesible solo por consola local, sin forma de deshacer nada desde lejos. Cada fabricante buscó su red de seguridad. En Cisco los técnicos programaban un reinicio con `reload in` antes de un cambio riesgoso y lo cancelaban si todo salía bien. Juniper incorporó `commit confirmed`, que vuelve atrás solo si no confirmás a tiempo.

MikroTik resolvió el problema atándolo a la sesión: Safe Mode. Se apoya en el historial de cambios de RouterOS, el mismo que usan `/undo` y los botones Undo y Redo de WinBox, que guarda las 100 acciones más recientes.

### Cómo funciona
**Una marca en el historial.** Al entrar en Safe Mode (botón de WinBox o WebFig, o `Ctrl+X` o `F4` en la terminal), RouterOS empieza a marcar cada cambio con `F` (floating-undo) en `/system/history`. Los cambios se aplican en el acto, no quedan en espera: por eso un cambio malo te corta igual.

**Lo que vigila es la sesión.** Si la sesión que tomó el Safe Mode termina de forma anormal, el router deshace todo lo marcado con `F`, también lo que se haya hecho desde otras sesiones. No hay un temporizador propio: el router se da cuenta cuando la conexión muere. La documentación toma como referencia el timeout TCP de 9 minutos; en el foro hay casos de segundos en red local y de un minuto en WebFig.

**Tres salidas.** `Ctrl+X` otra vez (o soltar el botón) confirma y sale del modo seguro. `Ctrl+D` sale y deshace todo. `/quit` cuenta como salida normal y conserva los cambios.

**El tope de 100.** Si en Safe Mode hacés más cambios de los que entran en el historial, la sesión sale sola del modo seguro y no deshace nada. Por eso conviene trabajar en pasos chicos.

**Uno por vez.** Solo una sesión puede tener el Safe Mode. Si otro técnico lo pide, RouterOS pregunta: `u` deshace lo del primero y se lo da, `r` conserva sus cambios y se lo da, `d` no toca nada.

**Lo que no cubre.** Si el cambio corta tu sesión a propósito (mover la VPN por la que entrás), se deshace igual. Y un corte de energía no es una forma de deshacer: en el foro, en 6.40.4, el cambio quedó aplicado. Para esos casos, backup y un scheduler que lo restaure si no lo cancelás."""
