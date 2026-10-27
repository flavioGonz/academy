"""Figuras de la Teoría del curso OmniAccess LPR: archivo, ancla, alt y leyenda.
Lo usan los scripts anim_* (el alt es la descripción del SVG) y manifest_teoria.py (escribe manifest-teoria-1-12.json)."""

FIGS = {
    "1": [{
        "file": "1-t1.svg",
        "after": "entre 1 y 3 segundos desde la línea hasta la pantalla",
        "alt": "Animación en cinco tiempos sobre una fila de cinco tramos: cámara, red, servidor, base y almacenamiento, y Monitor LPR. "
               "1: la cámara ve el auto en la línea de captura, lee la patente SBA 1234 y arma el XML con licensePlate, confianza, MAC, hora y dos fotos. "
               "2: el mensaje viaja como POST multipart por HTTP al puerto 10000. 3: el receptor separa el XML de las imágenes, reconoce la cámara por la MAC o la IP, descarta repeticiones y decide Autorizado. "
               "4: la foto va al bucket lpr y el evento a la base de datos. 5: el evento aparece en el Monitor LPR. Abajo, un cronómetro se llena de 0 a 3 segundos; más de 10 segundos habituales marcan un tramo degradado. "
               "Al costado, el NVR graba aparte y solo entrega video cuando alguien toca Grabación, Clip o Exportar.",
        "caption": "Seguí la ficha de tramo en tramo y mirá el cronómetro: de la línea a la pantalla, 1 a 3 segundos.",
    }],
    "2": [{
        "file": "2-t1.svg",
        "after": "la lista negra siempre le gana a un pase",
        "alt": "Animación en cinco tiempos: una lectura atraviesa cinco controles del servidor, de izquierda a derecha: antirrebote, hora, lista de la cámara, padrón y modo, vigilancia y pases. "
               "1: SBA1234 llega dos veces en 2 segundos; la segunda queda descartada por el antirrebote (5 s por matrícula, 20 s por cámara). "
               "2: la hora de la cámara se usa si está a menos de 10 minutos de la del servidor; si no, se usa la del servidor. "
               "3: si el XML trae whiteList o blackList, manda la cámara y sale Autorizado. "
               "4: sin lista en el XML, la matrícula SBA-1234 se normaliza a SBA1234, se encuentra en el padrón y con Modo LPR en Lista Blanca sale Autorizado, en verde. "
               "5: SAB2024 no está en el padrón y tiene un pase de invitado, pero está en lista negra: sale Lista negra, en rojo con sonido.",
        "caption": "Cada lectura pasa por los controles en orden; mirá en cuál se decide.",
    }],
    "3": [{
        "file": "3-t1.svg",
        "after": "Leer donde frena reduce el problema",
        "alt": "Animación en cuatro tiempos que muestra el recorte de una patente SBD 1080 tal como le llega al OCR y, al lado, los siete caracteres leídos. "
               "1: patente de frente, de 150 a 200 píxeles de ancho, con el auto frenando: los siete caracteres salen en verde. "
               "2: perspectiva de más de 30 grados: la patente se ve aplastada e inclinada y varios caracteres quedan dudosos. "
               "3: pocos píxeles, unos 40 de ancho: la patente se ve borrosa y el OCR duda entre B y 8 y entre D y 0. "
               "4: auto rápido: la patente sale movida en horizontal y los caracteres se mezclan; leer donde el auto frena lo evita.",
        "caption": "El mismo OCR, cuatro imágenes: lo que arruina la lectura es la perspectiva, el tamaño y el movimiento.",
    }],
    "4": [{
        "file": "4-t1.svg",
        "after": "evita el problema clásico de las cámaras detrás de NAT",
        "alt": "Animación en cuatro tiempos, diagrama de mensajes entre el servidor OmniAccess (192.0.2.10) y la cámara P1 - Entrada (21) (192.0.2.21). "
               "1: el servidor manda PUT /ISAPI/System/time con su hora y PUT /ISAPI/Event/notification/httpHosts/1 con el destino 192.0.2.10:10000/api/webhooks/hikvision; la cámara responde ok. "
               "2: GET VCAResource; si la respuesta no dice roadDetection, la tarea queda en error y no se fuerza, porque cambiarlo pide reiniciar. "
               "3: PUT Streaming/channels/101 y 102 con H.264, registro del video en vivo y carga de matrículas. "
               "4: la cámara manda su primer evento por POST al puerto 10000; pasa por un router con NAT y llega con la IP del router, pero el XML trae la MAC y el receptor la reconoce como P1 - Entrada (21).",
        "caption": "La puesta a punto son pedidos ISAPI del servidor a la cámara; el primer evento hace el camino inverso.",
    }],
    "5": [{
        "file": "5-t1.svg",
        "after": "Si el NVR está corrido, el video no coincide",
        "alt": "Animación en cuatro tiempos con tres piezas: el servidor con su reloj, el NVR con su reloj y la vista del video. "
               "1: una lectura queda registrada a las 14:30:00; la hora de la cámara vale porque está a menos de 10 minutos de la del servidor. "
               "2: al tocar Grabación, OmniAccess le pide al NVR el canal 3 a las 14:30:00. "
               "3: el reloj del NVR va 185 segundos adelantado: su 14:30:00 es un momento anterior y el video muestra el carril vacío; con más de 120 segundos se abre la alerta de reloj. "
               "4: Sincronizar hora pone la hora del servidor en el NVR, sin internet, o configura NTP; el mismo pedido trae el video con el auto en la línea.",
        "caption": "El pedido de video va por hora: si el reloj del NVR está corrido, llega otro momento.",
    }],
    "6": [{
        "file": "6-t1.svg",
        "after": "cambiando solo el campo necesario",
        "alt": "Animación en cuatro tiempos sobre la vista nocturna de una cámara ANPR. "
               "1: el IR de la cámara ilumina; la patente retrorreflectiva devuelve la luz y se ve brillante sobre una escena oscura. "
               "2: con faros de frente o IR muy fuerte la patente se quema en blanco; el anti-brillo baja los brillos y vuelve a leerse. "
               "3: obturador: 1/1000 congela más pero entra la mitad de luz que con 1/500; a 20 o 30 km/h, el perfil barrio-noche elige 1/500. "
               "4: el calibrador hace GET de /ISAPI/Image/channels/1/Shutter, cambia solo ShutterLevel de 1/1000 a 1/500 y hace PUT del mismo XML.",
        "caption": "Luz, obturador y una escritura por ISAPI que toca un solo campo.",
    }],
    "7": [{
        "file": "7-t1.svg",
        "after": "redibuja unas cuatro veces por segundo",
        "alt": "Animación en cuatro tiempos: a la izquierda el receptor de eventos, en el medio el navegador del puesto con una cola, a la derecha el Monitor LPR. "
               "1: el receptor emite cada lectura por WebSocket (Socket.io) a los navegadores abiertos. "
               "2: llega una ráfaga de lecturas; el monitor las junta en la cola y redibuja unas cuatro veces por segundo, en tandas. "
               "3: cada tarjeta se pinta con tres datos: decisión, si la matrícula está en vigilancia y si vino sin chapa; verde Autorizado, ámbar Denegado, rojo lista negra, amarillo sin lectura. "
               "4: llega una lectura de lista negra: tarjeta roja con sonido, que sigue hasta abrir el evento, y una ventana chica abajo a la izquierda.",
        "caption": "Las lecturas llegan sueltas, la pantalla se pinta en tandas y el color sale de tres datos.",
    }],
    "8": [{
        "file": "8-t1.svg",
        "after": "es una limitación del hardware",
        "alt": "Animación en cuatro tiempos. 1: en Búsqueda inteligente, modo Accesos, se escribe camioneta blanca ayer a la tarde. "
               "2: un analizador, sin inteligencia artificial ni internet, convierte cada palabra en un filtro: camioneta pasa a tipo SUV o camioneta, blanca a color blanco, ayer a la fecha de ayer y a la tarde a la franja de 12 a 20 horas. "
               "3: los filtros se aplican sobre la tabla de eventos propios del sistema y quedan solo las filas que coinciden, al instante, incluidas las de los portones. "
               "4: la búsqueda por imagen va por otro camino: se la pide al NVR, que busca en índices de analítica alimentados solo por cámaras de contexto; la cámara de matrícula no alimenta ese índice.",
        "caption": "La frase se vuelve filtros sobre tus eventos; la búsqueda por imagen depende del NVR.",
    }],
    "9": [{
        "file": "9-t1.svg",
        "after": "no vuelve a avisar por esa matrícula durante 30 minutos",
        "alt": "Animación en cinco tiempos sobre una línea de tiempo de 21:00 a 21:40 para la matrícula SCD5678, no registrada, con una ventana de 30 minutos que acompaña a cada lectura y un contador. "
               "1: pasada a las 21:00 por P1: el contador marca 1. "
               "2: pasada a las 21:10 por P2: el contador marca 2; una lectura sin chapa a las 21:15 aparece en gris y no cuenta. "
               "3: pasada a las 21:25 por P1: el contador llega a 3 y se abre la alerta Merodeo, que queda anotada en la bitácora. "
               "4: pasada a las 21:32 por P2: siguen siendo 3 en la ventana, pero no hay aviso nuevo hasta las 21:55. "
               "5: en otra fila, un residente autorizado pasa cinco veces en media hora y no abre alerta.",
        "caption": "La ventana de 30 minutos acompaña cada lectura; la tercera pasada abre la alerta una sola vez.",
    }],
    "10": [{
        "file": "10-t1.svg",
        "after": "Al sacarla, vuelve a la lista blanca si tiene credencial",
        "alt": "Animación en cuatro tiempos: el servidor OmniAccess arriba y tres lectoras Hikvision, P1, P2 y P3, cada una con dos listas: blanca y de bloqueo. "
               "1: la matrícula SAB2024, con credencial, está en la lista blanca de cada lectora; en P1 la cámara cierra su relé y sube la barrera. "
               "2: se carga en lista negra: el servidor la marca Denegada y un PUT la mueve a la lista de bloqueo en P1 y P2; P3 no responde y el resumen lo informa; la barrera la deniega igual por servidor. "
               "3: nueva lectura en P1: la cámara no cierra el relé, el servidor la deniega y el monitor la muestra en rojo con sonido. "
               "4: al sacarla de la lista negra vuelve a la lista blanca porque tiene credencial; una matrícula sin credencial se borra de la cámara.",
        "caption": "La lista negra vive en el servidor y se copia a la lista de bloqueo de cada lectora.",
    }],
    "11": [{
        "file": "11-t1.svg",
        "after": "mientras tanto la cámara no abre sola",
        "alt": "Animación en cuatro tiempos con dos columnas: a la izquierda las matrículas de la base y a la derecha las listas de la cámara P1, lista blanca y lista de bloqueo. "
               "1: Analizar compara las dos columnas: falta SAC1010, sobra SDE9090 y SAB2024 está en lista negra pero sigue en la lista blanca de la cámara. "
               "2: Incremental agrega SAC1010 y quita SDE9090. 3: mueve SAB2024 a la lista de bloqueo. "
               "4: en cambio, Reemplazo total vacía la lista de la cámara y la recarga entera; mientras recarga, la cámara no abre sola.",
        "caption": "Incremental toca solo las diferencias; Reemplazo total deja la cámara sin lista un rato.",
    }, {
        "file": "11-t2.svg",
        "after": "uno o dos caracteres según el largo",
        "alt": "Animación en tres tiempos sobre un pase de invitado. "
               "1: hay un pase activo y vigente para la patente SBA1234. "
               "2: la cámara lee SBA1Z34, con un carácter distinto; como la patente tiene 6 o más caracteres, se toleran hasta 2 diferencias (con menos de 6, una) y el pase coincide. "
               "3: si la patente leída está en lista negra, gana la lista negra y la lectura queda denegada aunque coincida con el pase.",
        "caption": "El pase tolera errores de lectura; la lista negra no cede.",
    }],
    "12": [{
        "file": "12-t1.svg",
        "after": "reloj abre con más de 120 segundos",
        "alt": "Animación en cuatro tiempos sobre la salud de una cámara. "
               "1: cada sondeo deja una muestra en una fila de puntos; las muestras se guardan 14 días. "
               "2: un sondeo sin respuesta queda en ámbar y no abre nada; con dos seguidos se abre la alerta Sin respuesta, y al volver a contestar se cierra. "
               "3: un gráfico de memoria sube: al pasar 95 % se abre la alerta y no se cierra a 94 %, recién al bajar de 90 %. "
               "4: el desfase del reloj contra el servidor crece y al pasar 120 segundos se abre la alerta de reloj.",
        "caption": "Cada alerta tiene un umbral para abrir y otro para cerrar: así no parpadea.",
    }],
}
