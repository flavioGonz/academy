"""Genera /home/claude/ies-training/ilustraciones/paradox/estructura.json."""
import json

E = {
 "curso": {
  "objetivo": "Al terminar el curso vas a poder identificar y cablear centrales Paradox SP, MG y EVO con el bus, la EOL y la energía bien resueltos, programarlas por teclado con método y con una copia en BabyWare, dejarlas reportando en Contact ID con el comunicador y la receptora correctos, explicarle al cliente la app y Swan, diagnosticar con TBL y [935], y entregar cada central sin ninguna llave de fábrica.",
  "recorrido": "Arrancás por la central física: qué familia es, cómo se arma el bus, cómo se supervisa una zona con la resistencia al final y cuánta energía aguanta. Después programás con método: entrar sin romper, sacar una copia con BabyWare y recién ahí zonas, particiones, usuarios y salidas. Con la central programada, la conectás a monitoreo: el comunicador según su generación, el abonado y la receptora, y la app con Swan. Cerrás con lo que pasa después de la entrega: leer las fallas, encontrar por qué no reporta, cerrar todas las llaves y decidir qué hacer con cada sitio del parque."
 },
 "modulos": [
  {"title": "La central bien parada",
   "why": "Antes de programar, la central tiene que estar identificada, con el bus armado, las zonas bien cableadas y la energía calculada. Va de lo que se ve al abrir el gabinete a lo que se mide con el tester. Termina con una central de banco energizada, con un teclado, un expansor y zonas supervisadas.",
   "objetivos": [
    "Al terminar el módulo vas a poder identificar la familia y la versión de una central Paradox y abrir el manual correcto.",
    "Al terminar el módulo vas a poder armar el bus de a grupos y cablear zonas con EOL de 1 kΩ y, en la SP6000+ o EVO, con ATZ.",
    "Al terminar el módulo vas a poder sumar el consumo del auxiliar, calcular la autonomía de batería y resolver la salida de campana."
   ],
   "lessons": ["1", "2", "3", "4"]},
  {"title": "Programar con método",
   "why": "Es el trabajo de cada obra. Primero se aprende a entrar sin romper y a sacar una copia de la central con BabyWare; recién con esa copia se programan zonas, particiones, usuarios y salidas. Termina con una casa tipo programada y probada como la usaría el cliente.",
   "objetivos": [
    "Al terminar el módulo vas a poder entrar a programación, mirar una sección antes de escribirla y cambiar los códigos de fábrica.",
    "Al terminar el módulo vas a poder conectar BabyWare por cable y guardar una copia completa de la central antes de cambiar nada.",
    "Al terminar el módulo vas a poder programar zonas, particiones, usuarios y PGM con relé, y probarlos con el recorrido del cliente."
   ],
   "lessons": ["5", "9", "6", "7", "8"]},
  {"title": "Comunicación y monitoreo",
   "why": "Una alarma que no avisa no sirve. Primero se decide el comunicador según su generación, después se programa el reporte a la receptora y al final la app, que va por otro camino. Termina con un evento de prueba confirmado por el operador y el sitio Swan anotado en la ficha.",
   "objetivos": [
    "Al terminar el módulo vas a poder distinguir módulos legado y MQTT, y pedir la salida de red que necesitan.",
    "Al terminar el módulo vas a poder programar Contact ID, abonados por partición y canal, receptor IP y perfil de supervisión.",
    "Al terminar el módulo vas a poder dar de alta un sitio Swan en BlueEye y explicar al cliente qué paga y qué pasa si vence."
   ],
   "lessons": ["10", "11", "12"]},
  {"title": "Diagnóstico y cuidado",
   "why": "Fallas y comunicación caída son las llamadas de todos los días, y las llaves de fábrica el riesgo más grande. Va del diagnóstico en el teclado al de la cadena de reporte, y cierra con la seguridad de la central y el futuro del parque.",
   "objetivos": [
    "Al terminar el módulo vas a poder leer TBL y el LED de estado, y saber qué fallas se van solas y cuáles se borran en [955].",
    "Al terminar el módulo vas a poder diagnosticar una central que no reporta con [935], de la central hacia afuera.",
    "Al terminar el módulo vas a poder entregar una central sin llaves de fábrica y decidir por sitio qué hacer ante el firmware 7.50 y la línea M."
   ],
   "lessons": ["13", "14", "15", "16"]}
 ],
 "lecciones": {
  "1": {"objetivos": [
         "Al terminar vas a poder reconocer en la placa si la central es SP, MG, EVO o de la línea M.",
         "Al terminar vas a poder leer la versión de firmware de una SP o MG en la sección [980].",
         "Al terminar vas a poder completar la ficha de la obra con modelo, versión, teclados, módulos y StayD."],
        "sigue": "Con la central identificada, la próxima arma el bus que une teclados y expansores, de a un grupo por vez.",
        "requisitos": []},
  "2": {"objetivos": [
         "Al terminar vas a poder conectar teclados y expansores al bus de 4 hilos respetando la serigrafía.",
         "Al terminar vas a poder poner en marcha el bus de a grupos y saber qué fallas son esperables en una central nueva.",
         "Al terminar vas a poder asignar la zona de un teclado y evitar que un inalámbrico la pise."],
        "conecta": "En Leer la central identificaste familia y versión. Acá le sumás a esa central sus teclados y expansores.",
        "sigue": "Con el bus andando, la próxima cablea las zonas con la resistencia al final para que la central vea un corte o un corto.",
        "requisitos": ["1"]},
  "3": {"objetivos": [
         "Al terminar vas a poder explicar qué ve la central con una EOL de 1 kΩ: normal, abierta y en corto.",
         "Al terminar vas a poder cablear la resistencia en el extremo del detector y activar EOL en [706].",
         "Al terminar vas a poder cablear dos detectores en un par con ATZ en una SP6000+ o EVO."],
        "conecta": "En Bus de a grupos usaste TBL para encontrar fallas de módulos. Acá TBL muestra también el grupo 5, tamper y cableado de zona.",
        "sigue": "Con zonas y bus cableados, la próxima suma lo que todo eso consume y cuánto aguanta la batería.",
        "requisitos": ["2"]},
  "4": {"objetivos": [
         "Al terminar vas a poder sumar el consumo del AUX con la tabla de la guía y compararlo con el límite de la central.",
         "Al terminar vas a poder calcular la autonomía aproximada de la batería.",
         "Al terminar vas a poder resolver la salida de campana sin sirena y conocer los umbrales de batería de la SP+."],
        "conecta": "En Bus de a grupos viste que cada módulo cuelga de la alimentación del bus. Acá sumás todo eso contra el límite del AUX.",
        "sigue": "La central quedó bien parada. El próximo módulo entra a programarla, empezando por cómo entrar sin romper nada.",
        "requisitos": ["2"]},
  "5": {"objetivos": [
         "Al terminar vas a poder entrar a programación en SP y MG y reconocer los tres tipos de dato.",
         "Al terminar vas a poder mirar una sección con ENTER antes de escribirla y salir con CLEAR sin guardar.",
         "Al terminar vas a poder cambiar los códigos de instalador y maestro, y saber qué no toca el de mantenimiento."],
        "conecta": "En Leer la central viste cómo se entra a cada familia. Acá entrás en serio a una SP o MG y aprendés a no pisar nada.",
        "sigue": "Antes de cambiar una sola zona, la próxima saca una copia completa de la central con BabyWare.",
        "requisitos": ["1"]},
  "9": {"objetivos": [
         "Al terminar vas a poder conectar BabyWare por el cable 307USB al conector serie de la central.",
         "Al terminar vas a poder cambiar el ID de panel y la contraseña de PC y crear la cuenta con los mismos valores.",
         "Al terminar vas a poder guardar una copia completa de la central y explicar por qué una sesión abierta ocupa el módulo IP."],
        "conecta": "En Entrar con método cambiaste las llaves del teclado. Acá aparecen las dos llaves del software, [910] y [911], y la copia antes de programar.",
        "sigue": "Con la copia guardada, la próxima programa las zonas de una casa tipo según el recorrido de entrada.",
        "requisitos": ["5"]},
  "6": {"objetivos": [
         "Al terminar vas a poder programar una zona con definición, partición y opciones en [001] a [032].",
         "Al terminar vas a poder elegir entre retardo, seguimiento, instantánea, fuego y 24 h según el recorrido de entrada.",
         "Al terminar vas a poder probar la casa como el cliente y usar el retardo de transmisión contra falsas alarmas."],
        "conecta": "En BabyWare primero guardaste la copia de la central. Ahora sí cambiás zonas, y en Resistencia al final ya dejaste esas zonas bien cableadas.",
        "sigue": "Con una partición programada, la próxima suma una segunda partición y los usuarios que arman cada una.",
        "requisitos": ["9", "3"]},
  "7": {"objetivos": [
         "Al terminar vas a poder activar el particionado y asignar zonas a cada partición con el tercer dígito.",
         "Al terminar vas a poder dejar a un usuario solo con la partición y las opciones que necesita.",
         "Al terminar vas a poder decidir el largo de código antes de cargar usuarios."],
        "conecta": "En Cada zona su tipo el tercer dígito de cada zona fue 1. Acá ese dígito separa la casa del taller.",
        "sigue": "Con zonas y usuarios en orden, la próxima saca salidas útiles de la central: el portón y la luz de falla.",
        "requisitos": ["6"]},
  "8": {"objetivos": [
         "Al terminar vas a poder conectar una PGM a un relé externo y manejar un portón con un pulso.",
         "Al terminar vas a poder programar eventos de activación y desactivación, o un tiempo, en cada PGM.",
         "Al terminar vas a poder hacer una luz de falla de AC que se prenda y se apague sola."],
        "conecta": "En Cuentas de energía viste que todo lo que cuelga del AUX suma. Acá la bobina del relé entra en esa cuenta.",
        "sigue": "La central quedó programada. El próximo módulo la conecta a monitoreo, empezando por elegir el comunicador según su generación.",
        "requisitos": ["7", "4"]},
  "10": {"objetivos": [
          "Al terminar vas a poder distinguir un módulo legado (TURN) de uno MQTT por su modelo y firmware.",
          "Al terminar vas a poder elegir receptora y app según la generación del módulo.",
          "Al terminar vas a poder pedir la lista de salida de red y ubicar principal y respaldo en serie 1 y serie 2."],
         "conecta": "En BabyWare primero usaste el conector serie con un cable. Acá el módulo IP o PCS ocupa ese mismo lugar para comunicar.",
         "sigue": "Con el comunicador elegido, la próxima programa el reporte: formato, abonados y receptor IP.",
         "requisitos": ["9"]},
  "11": {"objetivos": [
          "Al terminar vas a poder programar Contact ID y el abonado en cada partición y canal.",
          "Al terminar vas a poder cargar el receptor IP con IP, puerto, contraseña y perfil, y registrar el módulo.",
          "Al terminar vas a poder dejar una prueba automática diaria y confirmar un evento con el operador."],
         "conecta": "En Comunicador por generación elegiste la receptora según el módulo. Acá le cargás a la central los datos que esa receptora te da.",
         "sigue": "El monitoreo ya recibe. La próxima suma la app del cliente, que va por otro camino.",
         "requisitos": ["10", "7"]},
  "12": {"objetivos": [
          "Al terminar vas a poder dar de alta un sitio Swan en BlueEye y entrar con el código de PC.",
          "Al terminar vas a poder decidir cuándo usar IP estática sin Swan y qué riesgos tiene.",
          "Al terminar vas a poder explicarle al cliente qué paga, qué pasa si vence y por qué el monitoreo no depende de la app."],
         "conecta": "En BabyWare primero cargaste la contraseña de PC. BlueEye pide ese mismo código, con cada 0 escrito como A.",
         "sigue": "La obra está entregada y reportando. El último módulo trata lo que viene después: fallas, comunicación caída y seguridad.",
         "requisitos": ["10", "9"]},
  "13": {"objetivos": [
          "Al terminar vas a poder leer los grupos de TBL y sus submenús más frecuentes.",
          "Al terminar vas a poder borrar la falla de un módulo quitado con [955] y resolver la pérdida de reloj.",
          "Al terminar vas a poder interpretar el LED de estado de la placa."],
         "conecta": "En Bus de a grupos, Resistencia al final y Cuentas de energía ya usaste TBL. Acá lo recorrés entero.",
         "sigue": "TBL muestra la falla de comunicación; la próxima sigue esa falla hasta la receptora.",
         "requisitos": ["4", "8"]},
  "14": {"objetivos": [
          "Al terminar vas a poder diagnosticar un reporte caído en orden: serie, red, puertos y receptora.",
          "Al terminar vas a poder leer la tabla de estados de [935] y provocar cada error en el banco.",
          "Al terminar vas a poder resolver un abonado atado a la MAC de un módulo anterior."],
         "conecta": "En Abonado y receptora registraste el módulo con ARM en [935]. Acá esa misma sección te dice por qué no registra.",
         "sigue": "Con la central diagnosticada, la próxima cierra todas las llaves que todavía tengan su valor de fábrica.",
         "requisitos": ["11", "13"]},
  "15": {"objetivos": [
          "Al terminar vas a poder listar todas las llaves de una SP+ con su sección y su valor de fábrica.",
          "Al terminar vas a poder configurar el bloqueo de teclado y decidir si corresponde el bloqueo de instalador.",
          "Al terminar vas a poder actuar ante una central ajena bloqueada sin buscar atajos."],
         "conecta": "En Entrar con método, BabyWare primero y Abonado y receptora fuiste cambiando llaves de a una. Acá las revisás todas juntas.",
         "sigue": "Con la central cerrada, la última mira el parque completo: qué actualizar, qué desbloquear y cuándo pensar en la línea M.",
         "requisitos": ["5", "9", "11"]},
  "16": {"objetivos": [
          "Al terminar vas a poder explicar qué cambia en el puerto serie desde el firmware 7.50 y cómo se desbloquea.",
          "Al terminar vas a poder describir la M25 según su ficha y cuándo evaluarla.",
          "Al terminar vas a poder decidir por sitio entre actualizar, desbloquear, migrar o dejar."],
         "conecta": "En Leer la central anotaste la versión de firmware. Acá esa versión decide si una integración serie sigue andando.",
         "cierre": "Con esto recorriste Paradox completo: de la placa al operador de monitoreo. La ficha de la obra, la copia en BabyWare, el abonado en cada partición y canal, TBL y [935] para diagnosticar y ninguna llave de fábrica son tu kit para la próxima central.",
         "requisitos": ["1", "10"]}
 },
 "avisos": [
  {"id": "9,6,7,8", "archivo": "card.md y script.txt",
   "texto": "El título \"# Lección N.\" de las tarjetas y la primera línea de la charla usan el número de carpeta. BabyWare primero pasa del 9 al 6, al lado de Entrar con método.",
   "sugerencia": "Si el portal muestra la posición y no el id, renumerar: 9→6, 6→7, 7→8, 8→9. Las lecciones 1 a 5 y 10 a 16 conservan su número, así que las referencias \"(lección 5)\", \"(lección 15)\" y \"(lección 11)\" de los laboratorios siguen correctas."},
  {"id": "5", "archivo": "script.txt",
   "texto": "A: Arco dos, programar. Lección cinco: entrar con método.",
   "sugerencia": "A: Módulo dos, programar. Lección cinco: entrar con método."},
  {"id": "9", "archivo": "script.txt",
   "texto": "A: Arco tres, comunicación. Lección nueve: BabyWare primero.",
   "sugerencia": "A: Lección seis: BabyWare primero."},
  {"id": "6", "archivo": "script.txt",
   "texto": "A: Lección seis: cada zona, su tipo.",
   "sugerencia": "A: Lección siete: cada zona, su tipo."},
  {"id": "7", "archivo": "script.txt",
   "texto": "A: Lección siete: particiones y usuarios.",
   "sugerencia": "A: Lección ocho: particiones y usuarios."},
  {"id": "8", "archivo": "script.txt",
   "texto": "A: Lección ocho: las PGM.",
   "sugerencia": "A: Lección nueve: las PGM."},
  {"id": "10", "archivo": "script.txt",
   "texto": "A: Lección diez: el comunicador.",
   "sugerencia": "A: Módulo tres, comunicación. Lección diez: el comunicador."},
  {"id": "13", "archivo": "script.txt",
   "texto": "A: Arco cuatro, diagnóstico. Lección trece: primero el TBL.",
   "sugerencia": "A: Módulo cuatro, diagnóstico. Lección trece: primero el TBL."}
 ]
}
out = "/home/claude/ies-training/ilustraciones/paradox/estructura.json"
json.dump(E, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
s = json.dumps(E, ensure_ascii=False)
print("ok", out, "guiones largos:", "—" in s or "–" in s)
