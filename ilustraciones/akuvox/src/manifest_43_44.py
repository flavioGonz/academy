import json, re
T43 = """### Un poco de historia
Los primeros monitores de portero eran teléfonos de pared con pantalla: un botón para atender, otro para abrir y, a veces, uno para mirar la cámara. Cuando pasaron a Android y a pantallas táctiles de 7 a 10 pulgadas, el monitor se volvió una pequeña tableta fija, y cada obra empezó a pedir otra cosa en la pantalla: el edificio quiere conserjería, la casa con alarma quiere el botón de armado, la oficina no quiere nada que distraiga.

Akuvox ordenó esa variedad en tres capas que se configuran desde la web: el theme (la forma de la pantalla de inicio), las áreas (qué botón va en cada lugar) y el aspecto (protector, fondo, logos, idioma). En las guías vigentes en 2026, los Android de las series C, S, IT y X ofrecen Default y Call List; el C313 Linux los llama Classic y Call List Simple; y el S567 suma un estilo visual para todas las pantallas y fondos que cambian solos en fechas festivas.

Para muchos equipos se usa el mismo camino que para cualquier otro ajuste: el aprovisionamiento con comandos AutoP, enviados desde la nube SmartPlus.

### Cómo funciona
**Theme.** Es una plantilla. Default muestra la hora y una fila de áreas con íconos; Call List pone a la izquierda la lista de contactos para llamar con un toque y deja unos botones al costado. Cambiar de theme no borra lo que hay en las áreas.

**Áreas.** Cada área guarda tres datos: el tipo (la función: Intercom, Message, DND, Arming, SOS, Unlock, Monitor, Browser y otras), una etiqueta y, si querés, un ícono propio de hasta 100x100. Un botón de alarma es un área con tipo Arming; para sacarlo se cambia el tipo. Unlock puede disparar un Remote Relay HTTP, el mismo de Botón del monitor. Settings Page Display hace algo parecido con el menú de configuración: decide qué entradas ve el residente.

**Reposo y protector.** Sin uso durante el Sleep Time (de 15 segundos a 30 minutos), el monitor muestra el protector si está activo (fotos, videos o reloj, con horario) o apaga la pantalla. Un toque lo despierta, y en el S567 también acercarse.

**AutoP.** Cada ajuste tiene su comando, como `Config.Wallpaper.Url01` para el fondo. El monitor lo recibe, baja lo que haga falta y lo aplica; el fondo recién se ve después del reinicio. Los valores son por modelo: la pantalla de inicio es `4` o `5` en el S567 y `0` o `1` en el S562."""

T44 = """### Un poco de historia
El portero de calle fue durante décadas una botonera: un pulsador por apartamento y una placa con nombres. Los porteros con teclado cambiaron los botones por un número a marcar, y los táctiles cambiaron la placa por una pantalla que puede ser botonera, teclado, directorio o cartelera, según cómo se configure.

Esa libertad trae una pregunta que antes no existía: qué ve la visita al llegar. Akuvox la contesta con themes pensados por escenario: Villa para una casa, Building para un edificio (el de fábrica en S539, X915 y R29), Office para buscar empleados, Alphanumeric para apartamentos con letras y números, Speed Dial y QR Code para accesos simples, y Directory o Customized Text en los Linux más chicos. Los más nuevos se apoyan en la nube: Gate Mode y Parking Lot muestran lo cargado en una comunidad de SmartPlus, y VMS separa visitas con cita y sin cita. La nota de themes por modelo es de junio de 2026, y las guías de septiembre y octubre ya suman Parking Lot al R29 y al S539: la lista crece con el firmware.

### Cómo funciona
**Theme.** Es la plantilla de la pantalla de inicio y del recorrido de la visita. Se elige en la web del portero (`Setting > Key/Display > Theme` en la mayoría, `Device > LCD > Theme` en E18 y E16) y cambia qué íconos aparecen y a dónde lleva cada uno.

**Página de inicio.** Dentro de Building se elige con qué pantalla arranca: la de íconos con el recuadro de rostro, o directo al directorio, al teclado del PIN o a la llamada. Cada tecla tiene etiqueta y tipo (incluso Relay, con horario), y hay un texto propio para cuando la apertura falla.

**Idioma.** El idioma general de pantalla se elige aparte (en el R29, `Setting > Time/Lang > LCD Language`), y el theme Building puede mostrar hasta cuatro idiomas para que la visita cambie con un toque.

**Reposo y publicidad.** Sin nadie enfrente, el portero pasa al protector después del Sleep: imágenes que rotan con su Play Time, o video en S539, S538 y X915 V2.0. Se despierta por detección infrarroja, por video, por rostro o al tocarlo, según el modelo.

**Themes de nube.** Gate Mode y Parking Lot no tienen lista propia: muestran edificios, apartamentos y accesos del proyecto en SmartPlus. En una obra local la pantalla queda sin nada para elegir; ahí van Villa, Building o Default."""

for t in (T43, T44):
    body = re.sub(r"[#*`]", "", t)
    print(len(body.split()), "palabras")

M = {
 "43": {
  "fig": {"file": "43.svg",
          "alt": "Dos monitores interiores esquemáticos. A la izquierda, theme Default: la hora y cuatro áreas con íconos (Llamar, Mensajes, DND y Alarma), con el área de alarma marcada en ámbar. A la derecha, theme Call List: lista de contactos (Portero calle, Portón, Conserjería, Apto 302) y botones Monitor, DND y Más. A la derecha, tres tarjetas: Theme (forma del inicio), Áreas (tipo, etiqueta e ícono) y Aspecto (protector, fondo, logo e idioma). Abajo, las rutas: C319, S567, IT88, X933 y S562 en Device > Display Setting > Theme con Default o Call List; C313 Linux en Device > Key/Display > Home Page Mode con Classic o Call List Simple. Nota: el botón de alarma es un área, no un theme.",
          "caption": "El theme da la forma; el botón de alarma es el tipo Arming de un área y se cambia ahí."},
  "steps": [
   {"file": "43-paso2.svg", "step": 2,
    "alt": "Dos tablas de Home Page Display en Device > Display Setting. Antes: área 4 con Type Arming y Label Alarma, marcada en ámbar. Después: área 4 con Type Unlock y Label Portón, en verde. Debajo, el monitor antes con el botón Alarma y después con el botón Portón. Nota: en S567 y X933, Value toma un Remote Relay HTTP de Botón del monitor.",
    "caption": "Se cambia el tipo del área 4 y en la pantalla aparece Portón en lugar de Alarma.",
    "after": "sección Home Page Display, buscá el área"},
   {"file": "43-paso6.svg", "step": 6,
    "alt": "SmartPlus manda al monitor dos comandos AutoP: Config.Wallpaper.Url01 con la URL del JPG y Config.Settings.PICTURE.Wallpaper en 1. Un servidor de imágenes por HTTPS, FTP o TFTP entrega el archivo, que el monitor baja; el fondo cambia después del reinicio. Ejemplo de la guía con un S562. Nota de advertencia: la pantalla de inicio (IdleStyle) vale 4 o 5 en el S567 y 0 o 1 en el S562 y el C313.",
    "caption": "Dos comandos, la imagen en un servidor y un reinicio; y cuidado al copiar líneas entre modelos.",
    "after": "Si el monitor está en SmartPlus"}
  ],
  "concepts": [
   {"name": "Theme de la pantalla de inicio",
    "para_que": "El mismo monitor se instala en casas, edificios y oficinas, y no todos quieren la misma pantalla. El theme deja elegir la forma del inicio sin tocar firmware: íconos grandes para quien usa pocas funciones, o una lista de contactos para quien llama seguido a la conserjería o a otro apartamento.",
    "como": "En C319, S567, IT88, X933 y S562 se elige en Device > Display Setting > Theme (Default o Call List); en el C313 Linux, en Device > Key/Display > Home Page Mode (Classic o Call List Simple). Conviene probar los dos con el residente adelante: cambiarlo no borra lo que está configurado en las áreas.",
    "ejemplo": "En un edificio de Pocitos con conserje 24 horas, los monitores van en Call List con Conserjería primera en la lista; en las casas de un barrio de Carrasco, Default con cuatro íconos grandes."},
   {"name": "Áreas de inicio y su tipo",
    "para_que": "Cada botón de la pantalla de inicio es un área con una función asignada. Así se resuelve el pedido más común de soporte: sacar, cambiar o renombrar un botón, sin tocar el theme.",
    "como": "En Device > Display Setting, secciones Home Page Display y More Page Display: Type (Intercom, Message, DND, Arming, SOS, Unlock, Monitor, Browser, Custom APK y otros según modelo), Label y un ícono propio de hasta 100x100 en JPG o PNG. Unlock puede tomar un Remote Relay HTTP. Settings Page Display oculta entradas del menú de configuración.",
    "ejemplo": "Una señora mayor en un apartamento de Punta Carretas toca sin querer el botón de alarma. Se cambia el área 4 de Arming a Unlock con la etiqueta Portón, que abre el portón del garaje con el Remote Relay HTTP ya armado."},
   {"name": "Protector y reposo",
    "para_que": "La pantalla prendida todo el día gasta y molesta; apagada del todo, parece rota. El protector ocupa ese tiempo con la hora o con imágenes del edificio, y la pantalla vuelve con un toque.",
    "como": "Device > Display Setting > Screen Saver Setting: Local Pictures, Local Videos o Clock (en el C313, Local Pictures o Clock), con horario. El Sleep Time en Display Settings marca cuándo entra. El formato depende del modelo: C319 hasta 2 MP a 1280x800, C313 JPG de 600K a 800x480, S562 JPG de 256K.",
    "ejemplo": "Una cooperativa de vivienda pide que los monitores muestren el reloj cuando nadie los usa, en vez de quedar en negro: protector Clock y Sleep Time de 1 minuto, en todos los apartamentos igual."},
   {"name": "AutoP para muchos monitores",
    "para_que": "Configurar 40 monitores a mano es lento y siempre queda uno distinto. El aprovisionamiento manda el mismo ajuste a todos y deja registro de qué se cambió.",
    "como": "Desde SmartPlus, en el proyecto, AutoP y el equipo: Config.Wallpaper.Url01 con la URL de la imagen y Config.Settings.PICTURE.Wallpaper en 1, y reinicio. Antes de copiar líneas de un modelo a otro, conviene mirar la planilla AutoP de ese modelo: la pantalla de inicio vale 4 o 5 en el S567 y 0 o 1 en el S562.",
    "ejemplo": "La administración de un edificio en el Centro cambia el logo del fondo: se sube el JPG al servidor, se mandan los dos comandos a los 40 monitores desde SmartPlus y se programa el reinicio en la madrugada."}
  ],
  "teoria_md": T43,
  "teoria_figs": [
   {"file": "43-t1.svg", "after": "Un toque lo despierta, y en el S567 también acercarse.",
    "alt": "Animación con un monitor esquemático y, al lado, los ajustes de la web. Tiempo 1: theme Default con la hora y cuatro áreas (Llamar, Mensajes, DND y Alarma); el área 4 tiene Arming y se marca en ámbar. Tiempo 2: el theme pasa a Call List y la pantalla muestra la lista de contactos; las áreas siguen como estaban. Tiempo 3: otra vez Default, y el área 4 cambia a Unlock con la etiqueta Portón, en verde. Tiempo 4: después de un minuto sin uso entra el protector con una imagen del edificio, y un toque lo despierta. Abajo, las rutas de C319, S567, IT88, X933 y S562 y la del C313 Linux.",
    "caption": "Mirá qué cambia en la pantalla con cada ajuste: el theme mueve la forma, el área cambia el botón."}
  ]
 },
 "44": {
  "fig": {"file": "44.svg",
          "alt": "Tres porteros táctiles esquemáticos en vertical. Villa (una casa): tres íconos redondos, Contacto, PIN y Llamar. Building (edificio, el de fábrica), resaltado: recuadro de rostro y cuatro botones, PIN, Llamar, Directorio y Recepción. Office (oficinas): buscador y lista de sectores. A la derecha, dónde se elige: S539, S538, S535, S532, X915, X912 y R29 en Setting > Key/Display > Theme; X916 en Intercom > Key/Display > Theme; E18 y E16 en Device > LCD > Theme. En ámbar, los que necesitan la nube: Gate Mode y Parking Lot (área pública de una comunidad en SmartPlus) y el Office del S539 (Smart Access Cloud). Nota: la lista depende del modelo y del firmware.",
          "caption": "Villa, Building u Office según quién llega, y los themes de nube solo si hay SmartPlus."},
  "steps": [
   {"file": "44-paso3.svg", "step": 3,
    "alt": "Ruta Setting > Key/Display > Key In Homepage Of The Building Theme y tres pantallas del portero según la página de inicio elegida: Home Page con íconos y recuadro de rostro, Tenants o Contacts con el directorio de apartamentos (101 García, 102 Pereira, 201 Rodríguez, 202 Silva, 301 Méndez) y PIN con el teclado numérico. Notas: en el X915 se llama Default Page y en el R29 Display Type; directorio para edificios con visitas y teclado para accesos de personal.",
    "caption": "La misma pantalla del theme Building puede arrancar en íconos, directorio o teclado.",
    "after": "cambiá la página de inicio"},
   {"file": "44-paso6.svg", "step": 6,
    "alt": "Tres estados del portero R29: en uso con la pantalla Building; después de 30 segundos sin nadie (Sleep), el protector con una imagen del edificio; y al detectar a alguien por infrarrojo (IR Detection), de vuelta a la pantalla de inicio. Abajo, hasta 5 imágenes con Play Time de 0 a 120 segundos y las rutas Device > LCD > Standby Interface Display y Device > Import/Export > Upload Screensaver Picture. Notas: JPG hasta 2 MP, 800x1280 recomendado; en el X915, Device > LCD > Upload Screensaver con video sin sonido.",
    "caption": "Reposo, cartelera y despertar: tres ajustes que se prueban parado frente al portero.",
    "after": "Protector del R29:"}
  ],
  "concepts": [
   {"name": "Theme del portero",
    "para_que": "Una pantalla táctil puede ser botonera, teclado o directorio. El theme elige cuál según el lugar, para que la visita entienda qué hacer sin leer nada: una casa no necesita un directorio y un edificio no se arregla con un solo botón.",
    "como": "En la web del portero: Setting > Key/Display > Theme en S539, S538, S535, S532, X915, X912 y R29; Intercom > Key/Display > Theme en el X916; Device > LCD > Theme en E18 y E16. La lista cambia por modelo y por firmware: lo que muestra la web de tu equipo es lo que vale.",
    "ejemplo": "Un R29 en el portón de una casa en Carrasco va en Villa; el X915 de la entrada de un edificio de 30 apartamentos en Pocitos queda en Building, que es el de fábrica."},
   {"name": "Página de inicio dentro del theme",
    "para_que": "Dentro de un mismo theme, la primera pantalla define cuántos toques hacen falta. Arrancar directo en el directorio o en el teclado ahorra un paso y evita que la visita se pierda entre íconos.",
    "como": "En Building: Setting > Key/Display > Key In Homepage Of The Building Theme, con Default Page (X915, S539) o Display Type (R29). Opciones: la página de íconos, directorio (Tenants o Contacts), PIN, llamada y, según modelo, Delivery o Temp Key. En la misma pantalla se renombra cada tecla.",
    "ejemplo": "En un edificio con mucha visita, el portero arranca en el directorio; en la puerta de servicio de un depósito, donde solo entra personal con código, arranca en el teclado."},
   {"name": "Themes que dependen de la nube",
    "para_que": "Algunos themes muestran información que vive en SmartPlus: los edificios y apartamentos de una comunidad o los accesos de un estacionamiento. Así un solo portero de entrada sirve para varias torres sin cargar nada a mano.",
    "como": "Gate Mode (S532, X912) y Parking Lot (R29 y S539 en sus guías más nuevas) necesitan el portero en el Public Area de un proyecto de comunidad en SmartPlus. El Office del S539 funciona con Smart Access Cloud. En una obra local, conviene Villa, Building o Default.",
    "ejemplo": "En un complejo de tres torres en Malvín con SmartPlus, el portero del acceso principal va en Gate Mode y muestra Torre A, B y C. El mismo portero en una obra sin nube quedaría con la pantalla vacía."},
   {"name": "Protector como cartelera",
    "para_que": "El portero pasa la mayor parte del día sin nadie enfrente. El protector apaga el brillo o muestra imágenes útiles: el nombre del edificio, horarios de la administración, avisos.",
    "como": "En el R29, Device > LCD > Standby Interface Display (Sleep, tiempo de protector, Wake Mode por infrarrojo, video o toque, horario) y hasta 5 imágenes en Device > Import/Export > Upload Screensaver Picture con su Play Time. El formato recomendado sale de la tabla de especificaciones: 800x1280 en R29 y X915 V2.0.",
    "ejemplo": "Un edificio en la rambla de Punta del Este muestra en temporada el horario de la conserjería en español y portugués, y vuelve a la pantalla de inicio cuando alguien se acerca."}
  ],
  "teoria_md": T44,
  "teoria_figs": [
   {"file": "44-t1.svg", "after": "al teclado del PIN o a la llamada",
    "alt": "Animación con un portero táctil esquemático y los ajustes de la web. Tiempo 1: theme Building con la página de inicio Home Page, recuadro de rostro y cuatro botones. Tiempo 2: la página de inicio pasa a Tenants y el portero arranca en el directorio; la visita toca el apartamento 201 y aparece Llamando a 201. Tiempo 3: la página de inicio pasa a PIN y el portero arranca en el teclado; con el código correcto, el relé A abre. Tiempo 4: el theme pasa a Gate Mode en una obra sin SmartPlus y la pantalla queda sin edificios para mostrar, en ámbar; un recuadro verde explica que con el portero en el área pública de una comunidad de SmartPlus aparecen los edificios, y que en obra local conviene Villa, Building o Default.",
    "caption": "Mirá cómo cambia el recorrido de la visita según la página de inicio, y qué pasa con un theme de nube sin nube."}
  ]
 }
}
# chequeos de anclas
for lid, folder in (("43", "43-theme-monitores"), ("44", "44-theme-porteros")):
    card = open(f"/home/claude/claudemy/akuvox/class/{folder}/card.md", encoding="utf-8").read()
    lab = card.split("**Laboratorio**")[1].split("**Regla para quedarse**")[0]
    nocode = re.sub(r"```.*?```", "", lab, flags=re.S)
    for st in M[lid]["steps"]:
        n = nocode.count(st["after"])
        print(lid, st["file"], "ancla", n, len(st["after"]))
    t = M[lid]["teoria_md"]
    for tf in M[lid]["teoria_figs"]:
        print(lid, tf["file"], "ancla teoria", t.count(tf["after"]), len(tf["after"]))
    s = json.dumps(M[lid], ensure_ascii=False)
    print("guiones largos:", bool(re.search("—|–", s)), "exigencias:", re.findall(r"tenés que|debés|asegurate de|no te olvides", s))
json.dump(M, open("/home/claude/ies-training/ilustraciones/akuvox/manifest-43-44.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
