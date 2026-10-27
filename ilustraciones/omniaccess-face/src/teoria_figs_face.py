"""Figuras de la Teoría del curso OmniAccess Face: archivo, ancla, alt y leyenda.
Lo usan los scripts anim_* (el alt es la descripción del SVG) y manifest_teoria.py (escribe manifest-teoria-1-10.json)."""

FIGS = {
    "1": [{
        "file": "1-t1.svg",
        "after": "si se corta la red, la puerta sigue funcionando",
        "alt": "Animación en cuatro tiempos con dos zonas: a la izquierda la puerta, con la persona, el terminal facial y la cerradura; a la derecha el servidor, con el servidor de eventos en el puerto 10000, el Modo Face y el Monitor Facial. "
               "1: Ana se para frente al terminal, que la compara con las caras de su memoria, la reconoce y dispara el relé: la cerradura se abre. "
               "2: el terminal manda el aviso por Action URL al puerto 10000; el servidor busca la foto en el registro del terminal y, con Modo Face en Lista Blanca, el monitor muestra Permitido. "
               "3: con el Modo Face en Lista Negra, la misma persona: el terminal abre igual y OmniAccess registra Denegado, con la puerta ya abierta. "
               "4: se corta la red entre los dos lados: la puerta sigue abriendo y el aviso no llega al servidor.",
        "caption": "El terminal decide y abre; OmniAccess recibe el aviso, lo clasifica y lo guarda.",
    }],
    "2": [{
        "file": "2-t1.svg",
        "after": "ubicación y luz primero, ajustes del equipo después",
        "alt": "Animación en cuatro tiempos. A la izquierda, el cuadro que ve la cámara del terminal; a la derecha, una vista de costado con la persona y el terminal, y una barra de similitud contra el umbral. "
               "1: la persona a unos 50 cm: la cara ocupa buena parte del cuadro, se detecta y la similitud con su plantilla queda por encima del umbral. "
               "2: más lejos: la cara queda chica y no se detecta un rostro, así que no hay comparación. "
               "3: más cerca: la cara se sale del cuadro y tampoco se detecta. "
               "4: a 50 cm pero con una ventana atrás: la cámara ajusta la exposición a la ventana, la cara queda en sombra, los rasgos salen distintos y la similitud cae por debajo del umbral.",
        "caption": "Primero hay que detectar la cara y después compararla: las dos cosas dependen de la imagen.",
    }],
    "3": [{
        "file": "3-t1.svg",
        "after": "Guarda el evento con su foto y lo empuja en tiempo real",
        "alt": "Animación en cuatro tiempos. 1: en el terminal, la Action URL es una plantilla: GET /api/webhooks/akuvox?event=face_valid con mac=$mac, user=$user_name y userid=$userid. "
               "2: al reconocer a alguien, el terminal reemplaza cada variable por el dato real: la MAC 00:00:5E:00:53:21, el nombre Ana%20Ejemplo y el ID 000482193, y manda el pedido al puerto 10000. "
               "3: el servidor lee el tipo de evento y lo normaliza; por ejemplo, relay_open pasa a puerta abierta. "
               "4: busca el equipo por la MAC en Dispositivos y encuentra Portería peatonal; con un aviso de una MAC que no está cargada, no hay evento. Con el equipo encontrado, va a buscar la foto y empuja el evento al monitor.",
        "caption": "La URL viaja con los datos adentro; la MAC es la que une el aviso con el equipo.",
    }, {
        "file": "3-t2.svg",
        "after": "cuál de los dos caminos está cortado",
        "alt": "Animación en tres tiempos con el terminal a la izquierda, el servidor a la derecha y dos caminos de red: arriba, del terminal al servidor, el aviso por Action URL al puerto 10000; abajo, del servidor al terminal, la foto del registro y el botón Relé, con el usuario y la clave de la API. "
               "1: los dos caminos andan y el monitor muestra el evento con foto. "
               "2: se corta el camino del aviso: no llega nada, ni evento ni foto; se revisa la URL, el firewall y la MAC. "
               "3: se corta el camino de vuelta: el evento llega sin foto y el botón Relé no responde; se revisa el usuario y la clave de la API y la red hacia el terminal.",
        "caption": "Cada síntoma apunta a un camino: sin evento es el aviso; evento sin foto es la vuelta.",
    }],
    "4": [{
        "file": "4-t1.svg",
        "after": "la verdad está en el terminal",
        "alt": "Animación en cuatro tiempos entre la ficha de Ana Ejemplo en OmniAccess y la memoria del terminal Portería peatonal. "
               "1: a partir del identificador interno de la persona se calcula un ID numérico de 9 dígitos, 000482193, que siempre da el mismo número. "
               "2: OmniAccess crea o actualiza el usuario en el terminal con nombre, tarjetas y PIN. "
               "3: manda la foto codificada en base64 al módulo de rostros; el terminal guarda una plantilla de rasgos, o rechaza la foto si no tiene una cara usable y el error aparece en el cajón. "
               "4: un reenvío usa el mismo ID y actualiza la misma fila en vez de duplicarla; Memoria Flash hace el camino inverso y lee lo que el terminal tiene.",
        "caption": "El ID estable evita duplicados; Memoria Flash muestra lo que el equipo tiene de verdad.",
    }],
    "5": [{
        "file": "5-t1.svg",
        "after": "puede volver a siempre sin que nadie lo note",
        "alt": "Animación en cuatro tiempos con OmniAccess a la izquierda y el terminal a la derecha. "
               "1: el Grupo de Acceso cruza personas y equipos y queda en OmniAccess: ordena y documenta, no viaja al terminal. "
               "2: la copia por A qué equipos se manda lleva al terminal la cara, el nombre, las tarjetas y el PIN de Ana, con el horario siempre (1001). "
               "3: un técnico carga en el terminal un horario de lunes a viernes de 8 a 17 para Ana; a las 7:30 el terminal la reconoce pero no abre. "
               "4: alguien reenvía la ficha: crear falla porque Ana ya existe, entonces se actualiza con todos sus datos y el horario vuelve a siempre; a las 7:30 abre otra vez.",
        "caption": "El horario lo decide el terminal, y un reenvío lo puede pisar.",
    }],
    "6": [{
        "file": "6-t1.svg",
        "after": "cuenta una historia distinta que Desconocido",
        "alt": "Animación en cuatro tiempos sobre el Monitor Facial, con sus columnas Entrada, centro y Salida. "
               "1: al abrir, el monitor carga los eventos de rostro de las últimas 24 horas. "
               "2: el servidor de eventos emite un evento nuevo por WebSocket; el monitor lo pone arriba, en Entrada porque el terminal es de entrada, y lo muestra grande en el centro. "
               "3: para la foto prueba en orden la captura del momento, la foto de la ficha y la imagen del evento, y usa la primera que existe. "
               "4: para el nombre prueba la ficha vinculada, el nombre que mandó el terminal y, si no hay ninguno, Desconocido; el color sale de la decisión registrada, verde Permitido y rojo Denegado.",
        "caption": "Cada evento llega en vivo y cada dato tiene un orden de respaldo.",
    }],
    "7": [{
        "file": "7-t1.svg",
        "after": "Que pase y salga Permitido con su nombre",
        "alt": "Animación en cuatro tiempos sobre un recorrido con una bifurcación. "
               "1: una persona nueva llega a portería; se le lee un texto corto y se deja constancia de quién, cuándo y quién leyó. "
               "2: si acepta, se saca la foto de frente, con una sola cara y luz pareja. "
               "3: se carga la ficha con nombre, unidad y el terminal en A qué equipos se manda, y se prueba: pasa y sale Permitido con su nombre. "
               "4: si no acepta, toma el otro camino: entra con tarjeta, PIN o por portería, sin castigo. "
               "Al costado, las tareas del responsable de la base: evaluación de impacto, inscripción de la base y texto definitivo.",
        "caption": "El consentimiento va antes de la foto, y siempre hay una alternativa.",
    }],
    "8": [{
        "file": "8-t1.svg",
        "after": "primero el terminal, probar que no abre",
        "alt": "Animación en cuatro tiempos con tres lugares donde vive algo de Ana: la memoria del terminal, la ficha con sus eventos en OmniAccess y el almacenamiento de fotos; a la derecha, la prueba en la puerta. "
               "1: Ana está en los tres lugares y la puerta abre. "
               "2: se cambia el Modo Face: cambia el registro, la cara sigue en el terminal y la puerta sigue abriendo. "
               "3: se elimina en Memoria Flash: la cara sale del terminal y en la prueba ya no abre. "
               "4: recién ahí se decide la ficha: conservarla sin terminales o borrarla, que borra también sus eventos; las fotos quedan y siguen la retención del almacenamiento.",
        "caption": "Solo sacar la cara del terminal impide que abra; la ficha se decide después.",
    }],
    "9": [{
        "file": "9-t1.svg",
        "after": "sea captura o foto de alta",
        "alt": "Animación en tres tiempos sobre una línea de 0 a 40 días del Bucket FACE, con la retención en 30 días. "
               "1: al bucket entran la foto de alta de Ana el día 0 y las capturas de cada evento, día a día. "
               "2: el día de hoy avanza y cada objeto vence a los 30 días de creado: las capturas más viejas se borran solas. "
               "3: el día 30 vence también la foto de alta de Ana, porque la regla se aplica a todo el bucket; por eso la retención se decide con el responsable y con un plan para resguardar las fotos de alta.",
        "caption": "La regla de días no distingue capturas de fotos de alta.",
    }, {
        "file": "9-t2.svg",
        "after": "comparando la hora con una tolerancia de unos segundos",
        "alt": "Animación en cuatro tiempos con dos columnas: el registro del terminal (doorlog) y los eventos en OmniAccess. "
               "1: con red, los accesos de las 10:00 y 10:05 llegan por aviso y quedan en las dos columnas. "
               "2: se corta la red: el terminal sigue abriendo y anota las 10:12 y las 10:20 solo en su registro. "
               "3: Auditoría Hardware lee los últimos registros del terminal y crea los que faltan, marcados SINCRO_HW. "
               "4: los que ya estaban, con la misma hora dentro de 2 segundos, no se duplican.",
        "caption": "El terminal guarda su propio registro; la sincronización trae solo lo que falta.",
    }],
    "10": [{
        "file": "10-t1.svg",
        "after": "Lo que sí lo reduce es mejorar las imágenes",
        "alt": "Animación en cuatro tiempos. 1: una pasada se compara con cada plantilla de la memoria; la mejor similitud supera el umbral y el terminal identifica y abre. "
               "Después, un gráfico con dos curvas de similitud: a la izquierda las de personas ajenas, a la derecha las de la persona correcta, y una línea vertical para el umbral. "
               "2: con el umbral bajo, casi no hay rechazos legítimos pero una parte de los ajenos queda a la derecha de la línea: suben las falsas coincidencias (FMR). "
               "3: con el umbral alto, casi ningún ajeno pasa, pero una parte de los legítimos queda a la izquierda: suben los falsos rechazos (FNMR). "
               "4: con mejor luz y mejor foto de alta las curvas se separan y, con el umbral en el medio, bajan los dos errores.",
        "caption": "Mover el umbral cambia el error de lado; mejorar la imagen lo achica.",
    }],
}
