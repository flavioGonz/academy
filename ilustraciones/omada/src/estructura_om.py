"""Genera /home/claude/ies-training/ilustraciones/omada/estructura.json."""
import json

E = {
 "curso": {
  "objetivo": "Al terminar el curso vas a poder elegir y levantar el controlador Omada adecuado para cada obra, adoptar equipos en la misma subred y a distancia, ordenar sitios y usuarios, segmentar la red con VLAN y ACL, dejar un WiFi con canales, potencia, roaming y portal bien resueltos, unir sedes con IPsec y mantener el controlador con backups, upgrades y migraciones sin perder la configuración.",
  "recorrido": "Arrancás por el controlador: dónde vive, cómo se levanta en un host propio y cómo lo encuentran los equipos, primero en la misma subred y después desde otra. Con los equipos adoptados, ordenás la red del cliente: un sitio por sede y un usuario por persona, VLAN completas de punta a punta y ACL que aíslan de verdad. Después pasás al WiFi: canales y potencia, roaming y mesh, y el portal para invitados sobre la red aislada. Cerrás con lo que sostiene la instalación en el tiempo: un túnel entre sedes y el backup antes de cada cambio."
 },
 "modulos": [
  {"title": "El controlador y la adopción",
   "why": "Antes de configurar una sola VLAN hay que decidir dónde vive el controlador, levantarlo bien y lograr que los equipos lo encuentren. Va de la decisión a la instalación, y de la adopción en la misma subred a la adopción desde otra. Termina con un controlador andando y un EAP adoptado en cada caso.",
   "objetivos": [
    "Al terminar el módulo vas a poder elegir entre controlador local, Omada Central o gateway integrado según la obra y la capacidad recomendada.",
    "Al terminar el módulo vas a poder levantar el controlador en Docker con red host y CPU con AVX, y adoptar un EAP en la misma subred leyendo el mensaje de Adopt Failed.",
    "Al terminar el módulo vas a poder adoptar equipos de otra subred o sede con Discovery Utility, Inform URL u option 138, y armar el port forwarding cuando hay NAT."
   ],
   "lessons": ["1", "2", "3", "4"]},
  {"title": "Ordenar y segmentar la red",
   "why": "Con los equipos adoptados, la red del cliente se ordena de arriba hacia abajo: primero sitios y usuarios, después las VLAN y al final las ACL que las aíslan. El orden importa porque la VLAN se crea dentro de un sitio y la ACL se apoya en las VLAN. Termina con una red de cámaras y una de invitados separadas y probadas.",
   "objetivos": [
    "Al terminar el módulo vas a poder crear un sitio por sede con gateway y usuarios con el rol justo, incluido un Viewer limitado a su sitio.",
    "Al terminar el módulo vas a poder armar una VLAN completa, con red y DHCP en el gateway, uplink tagueado y puerto con la VLAN nativa.",
    "Al terminar el módulo vas a poder aislar una VLAN con una Gateway ACL ordenada y demostrarlo con tres pings."
   ],
   "lessons": ["5", "6", "7"]},
  {"title": "WiFi que funciona",
   "why": "Sobre la red ya segmentada va el plan de radio. Primero canal, ancho y potencia, porque roaming y mesh dependen de celdas bien dimensionadas; al final el portal, que usa la VLAN de invitados del módulo anterior. Termina con un WiFi medido, un roaming probado caminando y un portal con vouchers.",
   "objetivos": [
    "Al terminar el módulo vas a poder fijar canal, ancho y potencia por EAP, medir antes y después, y programar WLAN Optimization fuera de horario.",
    "Al terminar el módulo vas a poder dejar el roaming andando con SSID idéntico y Fast Roaming, probar 802.11r con ping continuo y decidir cuándo usar mesh.",
    "Al terminar el módulo vas a poder configurar un portal Hotspot con vouchers y sus excepciones, sabiendo que depende del controlador corriendo."
   ],
   "lessons": ["8", "9", "10"]},
  {"title": "Sedes y mantenimiento",
   "why": "Lo último es lo que hace que la instalación se sostenga en el tiempo. El túnel entre sedes usa los sitios y la option 138 de módulos anteriores; el backup y la migración cuidan todo lo configurado. Termina con dos sedes unidas y un procedimiento de backup, upgrade y migración.",
   "objetivos": [
    "Al terminar el módulo vas a poder unir dos sedes con Auto IPsec, o con Manual IPsec cuando hay NAT adelante, con subredes que no se solapan.",
    "Al terminar el módulo vas a poder adoptar los equipos de una sucursal por el túnel con option 138, sin abrir puertos de gestión a internet.",
    "Al terminar el módulo vas a poder programar backups fuera del controlador, actualizar de a una versión mayor y migrar el controlador en orden."
   ],
   "lessons": ["11", "12"]}
 ],
 "lecciones": {
  "1": {
   "objetivos": [
    "Al terminar vas a poder distinguir las tres familias de controlador: local, en la nube e integrado en el gateway.",
    "Al terminar vas a poder explicar por qué Cloud Access no es un controlador en la nube y qué pasa cuando vence una licencia de Central Standard.",
    "Al terminar vas a poder elegir el controlador de una obra por dónde corre el servicio y por la capacidad recomendada, con margen."
   ],
   "sigue": "Si la obra pide controlador propio, la próxima lo levanta en un host dedicado con Docker, con los tres detalles que evitan que los equipos nunca aparezcan.",
   "requisitos": []
  },
  "2": {
   "objetivos": [
    "Al terminar vas a poder verificar AVX y elegir la imagen correcta del controlador.",
    "Al terminar vas a poder levantar el controlador en Docker con red host, reinicio automático y sesenta segundos para cerrar.",
    "Al terminar vas a poder completar el asistente con cuenta local y región Uruguay, y ver un EAP en Pending."
   ],
   "conecta": "En Dónde vive elegiste el tipo de controlador. Si fue Software propio, acá lo instalás en un host que no se duerma.",
   "sigue": "Con el controlador andando, la próxima mira de cerca qué pasa entre el EAP y el controlador al adoptar, y cómo leer un Adopt Failed.",
   "requisitos": ["1"]
  },
  "3": {
   "objetivos": [
    "Al terminar vas a poder explicar el descubrimiento por broadcast al UDP 29810 y por qué pide la misma VLAN.",
    "Al terminar vas a poder adoptar un EAP y resolver un Adopt Failed con las credenciales de la web local.",
    "Al terminar vas a poder leer los mensajes de adopción fallida y saber cuándo, y cómo, resetear."
   ],
   "conecta": "En Host dedicado viste que la red host existe para que llegue el broadcast. Acá ese broadcast se ve paso a paso, hasta que el equipo queda Connected.",
   "sigue": "En la misma subred el equipo encuentra solo al controlador. La próxima resuelve el caso de la sucursal o la VLAN de cámaras, donde el broadcast no llega.",
   "requisitos": ["2"]
  },
  "4": {
   "objetivos": [
    "Al terminar vas a poder elegir entre Discovery Utility, Inform URL y option 138 para un equipo en otra subred.",
    "Al terminar vas a poder cargar la option 138 en un gateway Omada o en un MikroTik, con la IP en hexadecimal.",
    "Al terminar vas a poder armar el port forwarding del 29810 al 29817 cuando hay NAT, y saber por qué conviene una VPN."
   ],
   "conecta": "En Adopción limpia viste que el broadcast no cruza routers. Acá alguien le dice al equipo dónde está el controlador.",
   "sigue": "Los equipos ya llegan al controlador desde cualquier lado. El próximo módulo ordena la red del cliente, empezando por los sitios y los usuarios.",
   "requisitos": ["3"]
  },
  "5": {
   "objetivos": [
    "Al terminar vas a poder crear un sitio por cada sede con gateway, con región y zona horaria.",
    "Al terminar vas a poder decidir cuándo activar el modo MSP y en qué controladores existe.",
    "Al terminar vas a poder crear usuarios con el rol justo, como un Viewer limitado a un sitio."
   ],
   "conecta": "En el módulo anterior adoptaste equipos en el sitio por defecto. Acá cada sede pasa a tener su sitio, antes de que llegue el segundo gateway.",
   "sigue": "Con los sitios en orden, la próxima arma la primera red dentro de uno: una VLAN de cámaras completa, de punta a punta.",
   "requisitos": ["3"]
  },
  "6": {
   "objetivos": [
    "Al terminar vas a poder crear una red con su VLAN y DHCP en el gateway desde el controlador.",
    "Al terminar vas a poder asignar perfiles de puerto: All en el uplink y la red de la VLAN en el puerto del equipo.",
    "Al terminar vas a poder diagnosticar una VLAN que no da IP revisando gateway, uplink y puerto, en ese orden."
   ],
   "conecta": "En Sitios y clientes cada sede quedó en su sitio. Acá se crea la primera red de un sitio: la VLAN 20 de cámaras.",
   "sigue": "La VLAN quedó andando, pero todavía se ve con las demás. La próxima explica por qué y la aísla con una ACL.",
   "requisitos": ["5"]
  },
  "7": {
   "objetivos": [
    "Al terminar vas a poder explicar por qué dos VLAN se ven si el gateway rutea entre ellas.",
    "Al terminar vas a poder crear una Gateway ACL con un IP Group y ordenarla de arriba hacia abajo.",
    "Al terminar vas a poder probar el aislamiento de una red de invitados con tres pings."
   ],
   "conecta": "En VLAN completa la red de cámaras quedó andando. Acá se agrega la de invitados y se corta su paso hacia las redes internas.",
   "sigue": "La red está segmentada y probada. El próximo módulo pasa a la radio: canales, ancho y potencia de los EAP.",
   "requisitos": ["6"]
  },
  "8": {
   "objetivos": [
    "Al terminar vas a poder elegir canal y ancho por banda: 1, 6 u 11 a 20 MHz en 2.4 GHz y 40 MHz para empezar en 5 GHz.",
    "Al terminar vas a poder bajar la potencia de EAP cercanos y validarla midiendo antes y después en dBm.",
    "Al terminar vas a poder programar WLAN Optimization de madrugada, lejos del reinicio programado."
   ],
   "conecta": "En el módulo anterior cada red quedó en su VLAN. Ahora se decide cómo salen los SSID al aire: por qué canal, con qué ancho y con cuánta potencia.",
   "sigue": "Con celdas del tamaño justo, el cliente ya puede cambiar de EAP. La próxima lo ayuda con roaming y decide cuándo conviene mesh.",
   "requisitos": ["3"]
  },
  "9": {
   "objetivos": [
    "Al terminar vas a poder dejar las condiciones del roaming: SSID idéntico, mismo sitio y Fast Roaming encendido.",
    "Al terminar vas a poder probar 802.11r caminando con ping continuo y decidir si queda encendido.",
    "Al terminar vas a poder decidir cuándo usar mesh y verificar la señal del uplink entre -40 y -62 dBm."
   ],
   "conecta": "En Menos potencia achicaste las celdas. Recién con eso el roaming funciona, y en Sitios y clientes viste por qué todos los EAP van en el mismo sitio.",
   "sigue": "El WiFi interno quedó resuelto. La próxima arma el WiFi de los invitados con un portal y vouchers.",
   "requisitos": ["8", "5"]
  },
  "10": {
   "objetivos": [
    "Al terminar vas a poder crear un portal Hotspot con vouchers sobre el SSID de invitados.",
    "Al terminar vas a poder configurar Pre-Authentication Access y Authentication-Free Client.",
    "Al terminar vas a poder explicar por qué el portal depende del controlador corriendo y probarlo con un celular."
   ],
   "conecta": "En VLAN no aísla dejaste la red de invitados separada de la interna. Acá ese SSID recibe su portal.",
   "sigue": "Un sitio quedó completo. El último módulo une sedes con un túnel y cuida todo lo configurado.",
   "requisitos": ["7"]
  },
  "11": {
   "objetivos": [
    "Al terminar vas a poder planificar subredes que no se solapen entre sedes.",
    "Al terminar vas a poder crear un Auto IPsec entre dos ER de sitios distintos y verificarlo.",
    "Al terminar vas a poder pasar a Manual IPsec con UDP 500 y 4500 cuando hay NAT adelante."
   ],
   "conecta": "En Sitios y clientes cada sede quedó en su sitio, y en Tres caminos viste la option 138. Acá el túnel une los sitios y la option 138 viaja por adentro.",
   "sigue": "Con todo configurado, queda cuidarlo. La última lección arma el backup, el upgrade y la migración.",
   "requisitos": ["5", "4"]
  },
  "12": {
   "objetivos": [
    "Al terminar vas a poder programar un backup semanal guardado fuera del controlador y exportar uno con la versión en el nombre.",
    "Al terminar vas a poder actualizar de a una versión mayor y explicar por qué el downgrade es reinstalar.",
    "Al terminar vas a poder restaurar en un controlador nuevo y migrar equipos en orden, con Forget al final."
   ],
   "conecta": "En Host dedicado viste dónde vive la configuración en Docker. Acá se respalda, junto con todo lo que armaste en el curso.",
   "cierre": "Con esto recorriste Omada completo: de elegir y levantar el controlador a unir sedes y cuidar la configuración. La tabla de decisión, el orden de las tres patas de la VLAN, la prueba de los tres pings y el backup antes de cada cambio son tu kit para la próxima obra.",
   "requisitos": ["2"]
  }
 },
 "avisos": [
  {"id": "1,2,3,4,5,6,7,8,9,10,11,12", "archivo": "card.md y script.txt",
   "texto": "El orden de las lecciones no cambia: los títulos \"# Lección N.\" de las tarjetas, las aperturas \"Lección cinco...\" de la charla y las referencias \"(Lección 7)\" de los laboratorios siguen correctos.",
   "sugerencia": "No hace falta renumerar. Solo cambian las aperturas que hablan de \"arco\", porque el curso pasa de tres arcos a cuatro módulos."},
  {"id": "5", "archivo": "script.txt",
   "texto": "A: Arranca el segundo arco. Lección cinco: sitios.",
   "sugerencia": "A: Arranca el segundo módulo. Lección cinco: sitios."},
  {"id": "8", "archivo": "script.txt",
   "texto": "A: Lección ocho, la del WiFi.",
   "sugerencia": "A: Arranca el tercer módulo. Lección ocho, la del WiFi."},
  {"id": "9", "archivo": "script.txt",
   "texto": "A: Arranca el último arco. Lección nueve: roaming y mesh.",
   "sugerencia": "A: Lección nueve: roaming y mesh."},
  {"id": "11", "archivo": "script.txt",
   "texto": "A: Lección once. Un cliente con central y sucursal",
   "sugerencia": "A: Arranca el último módulo. Lección once. Un cliente con central y sucursal"}
 ]
}
out = "/home/claude/ies-training/ilustraciones/omada/estructura.json"
json.dump(E, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
s = json.dumps(E, ensure_ascii=False)
print("ok", out, "dashes:", "—" in s or "–" in s)
