"""Genera /home/claude/ies-training/ilustraciones/unifi/estructura.json."""
import json

E = {
 "curso": {
  "objetivo": "Al terminar el curso vas a poder elegir y poner en marcha el controlador correcto para cada cliente, adoptar equipos en el local y a distancia, segmentar la red con VLANs, zonas y perfiles de puerto, armar un WiFi con ancho, potencia y roaming bien elegidos, y sostener muchos sitios con Site Manager, actualizaciones por etapas y un método de diagnóstico.",
  "recorrido": "Arrancás por quién manda: dónde vive la configuración, cómo se adopta un equipo en la misma red y cómo llega uno remoto a su controlador. Después segmentás: una red por función con su zona, puertos que llevan solo lo que corresponde y una red de invitados aislada y probada. Con la red en orden, armás el WiFi: canales angostos, potencia baja y roaming probado con los equipos del cliente. Cerrás sosteniendo muchos clientes: Site Manager con la cuenta de la empresa, backups y actualizaciones por etapas, y un diagnóstico que mira el historial antes de tocar."
 },
 "modulos": [
  {"title": "El controlador y la adopción",
   "why": "Antes de tocar WiFi o VLANs hay que saber dónde vive la configuración y lograr que cada equipo llegue a su controlador. Primero se elige el host, después se adopta en la misma red y al final a distancia. Termina con AP adoptados en capa 2 y en capa 3.",
   "objetivos": [
    "Al terminar el módulo vas a poder elegir entre Cloud Gateway, CloudKey y UniFi OS Server sabiendo que cada equipo tiene un solo host.",
    "Al terminar el módulo vas a poder adoptar un equipo en capa 2 siguiendo el orden reset, misma red y firmware.",
    "Al terminar el módulo vas a poder llevar un equipo remoto a su controlador con option 43, DNS o set-inform, y configurar Inform Host."
   ],
   "lessons": ["1", "2", "3"]},
  {"title": "Segmentar la red",
   "why": "Con los equipos adoptados, cada obra se segmenta. Primero las redes y sus zonas, después los puertos que las llevan y al final la red de invitados, que usa las dos cosas. Termina con tres VLANs, puertos con perfil y un WiFi de invitados probado desde un celular.",
   "objetivos": [
    "Al terminar el módulo vas a poder crear una red por función con su VLAN, su DHCP y su zona, y leer la Zone Matrix.",
    "Al terminar el módulo vas a poder dejar puertos de equipo final con VLAN nativa y Block All, y troncales en AP y uplinks.",
    "Al terminar el módulo vas a poder entregar una red de invitados en zona Hotspot, con o sin portal, aislada y probada."
   ],
   "lessons": ["5", "6", "10"]},
  {"title": "WiFi bien hecho",
   "why": "Sobre la red ya segmentada va el plan de radio. El orden importa: primero ancho y canal, después potencia y recién al final roaming, porque Fast Roaming sobre una radio mal ajustada solo acelera el paso al AP equivocado. Termina con un WiFi medido y un SSID de prueba validado con los equipos del cliente.",
   "objetivos": [
    "Al terminar el módulo vas a poder elegir ancho y canal por banda según clientes y vecinos, con escaneo, Channel AI y criterio para DFS.",
    "Al terminar el módulo vas a poder bajar la potencia por banda y validarla con una caminata medida en dBm.",
    "Al terminar el módulo vas a poder activar BSS Transition y Fast Roaming solo después de probar cada tipo de equipo, con SSID aparte para legado."
   ],
   "lessons": ["7", "8", "9"]},
  {"title": "Muchos clientes sin sorpresas",
   "why": "Con un sitio bien hecho, el trabajo pasa a ser sostener muchos. Va al final porque usa todo lo anterior: el host de cada sitio, el inform para re-apuntar equipos y lo que se mira en canales, potencia y roaming. Termina con una planilla de sitios, un procedimiento de actualización y un método de soporte repetible.",
   "objetivos": [
    "Al terminar el módulo vas a poder ver todos los sitios en Site Manager con la cuenta de la empresa, técnicos con rol y una planilla de sitios.",
    "Al terminar el módulo vas a poder actualizar con backup fuera del equipo, notas de versión leídas y un sitio piloto.",
    "Al terminar el módulo vas a poder diagnosticar una queja de WiFi con el historial del cliente y Time Machine antes de tocar nada."
   ],
   "lessons": ["4", "11", "12"]}
 ],
 "lecciones": {
  "1": {
   "objetivos": [
    "Al terminar vas a poder explicar por qué la configuración vive en el controlador de cada sitio y Site Manager solo conecta.",
    "Al terminar vas a poder decidir quién es el host de cada equipo, sabiendo que un UDM o UCG no se gestiona desde un server externo.",
    "Al terminar vas a poder instalar UniFi OS Server en una VM Ubuntu 24.04 y anotar las versiones de UniFi OS y de Network."
   ],
   "sigue": "Ya sabés quién manda en cada sitio. La próxima hace entrar al primer equipo: la adopción en la misma red, con el orden que ahorra la primera hora de obra.",
   "requisitos": []
  },
  "2": {
   "objetivos": [
    "Al terminar vas a poder resetear un equipo y adoptarlo en capa 2, con un solo DHCP en la red.",
    "Al terminar vas a poder leer info por SSH para ver modelo, firmware, IP y URL de inform.",
    "Al terminar vas a poder resolver Update Required y el equipo que adopta y pasa a offline."
   ],
   "conecta": "En Quién manda elegiste el host de cada equipo. Acá ese host recibe su primer AP, en la misma red.",
   "sigue": "En la misma red el controlador encuentra solo al AP. La próxima resuelve el caso difícil: el AP en otro local y el controlador en tu oficina.",
   "requisitos": ["1"]
  },
  "3": {
   "objetivos": [
    "Al terminar vas a poder armar la DHCP option 43 en hexadecimal o el nombre DNS unifi para que el equipo encuentre al controlador.",
    "Al terminar vas a poder usar set-inform por SSH con la URL correcta como plan B.",
    "Al terminar vas a poder configurar Inform Host con Override y exponer el 8080 solo hacia tus sitios."
   ],
   "conecta": "En Adopción limpia viste la URL de inform en la salida de info. Cuando el equipo no comparte red con el controlador, esa URL es lo único que lo lleva a casa.",
   "sigue": "Los equipos ya llegan a su controlador, cerca o lejos. El próximo módulo empieza a ordenar la red de cada obra: una red por función.",
   "requisitos": ["2"]
  },
  "5": {
   "objetivos": [
    "Al terminar vas a poder crear redes Staff, Invitados y CCTV con su VLAN, su DHCP y su zona.",
    "Al terminar vas a poder reconocer si un sitio sigue en el firewall clásico y pasarlo a zonas.",
    "Al terminar vas a poder leer la Zone Matrix y explicar qué significa Allow Return."
   ],
   "conecta": "En el módulo anterior los equipos quedaron adoptados en su controlador. Ahora ese controlador reparte la red en partes que no se mezclan.",
   "sigue": "Las redes existen, pero todavía hay que decidir qué puerto lleva cuál. La próxima arma los perfiles de puerto: troncales para AP y uplinks, una sola red para cada cámara.",
   "requisitos": ["1"]
  },
  "6": {
   "objetivos": [
    "Al terminar vas a poder configurar un puerto de cámara con VLAN nativa CCTV y Block All, y verificar su IP.",
    "Al terminar vas a poder dejar AP y uplinks con todas las VLAN, incluido un switch de terceros en el medio.",
    "Al terminar vas a poder sumar MAC fija o Lock Port to UniFi Device en puertos expuestos."
   ],
   "conecta": "En VLAN por función creaste Staff 10, Invitados 20 y CCTV 30. Acá cada puerto del switch recibe solo las que le corresponden.",
   "sigue": "Con las redes y los puertos en su lugar, queda la red que más reclamos genera: la de invitados, que usa la zona Hotspot y el trunk del AP.",
   "requisitos": ["5"]
  },
  "10": {
   "objetivos": [
    "Al terminar vas a poder poner la red de invitados en zona Hotspot y elegir entre WiFi Standard y Hotspot.",
    "Al terminar vas a poder evitar la landing page que nadie pidió y generar vouchers con vencimiento y límite.",
    "Al terminar vas a poder probar desde un celular que el invitado no llega a nada interno."
   ],
   "conecta": "En VLAN por función la red Invitados quedó en zona Hotspot, y en Puertos con perfil el AP recibió el trunk con la VLAN 20. Acá se le da su WiFi y se prueba el aislamiento.",
   "sigue": "La red está segmentada y probada. El próximo módulo pasa a la radio: canales angostos según clientes y vecinos.",
   "requisitos": ["5", "6"]
  },
  "7": {
   "objetivos": [
    "Al terminar vas a poder escanear el entorno de RF sin cortar el servicio en horario de uso.",
    "Al terminar vas a poder fijar el ancho por banda según clientes y vecinos, y correr Channel AI.",
    "Al terminar vas a poder decidir si usar canales DFS y verificarlo en Time Machine."
   ],
   "conecta": "En el módulo anterior cada SSID quedó en su red. Ahora se decide por qué canal y con qué ancho salen esos SSID al aire.",
   "sigue": "Con buenos canales todavía puede pasar que el celular se quede en el AP lejano. La próxima ajusta la potencia.",
   "requisitos": ["2"]
  },
  "8": {
   "objetivos": [
    "Al terminar vas a poder explicar el cliente pegajoso y por qué la potencia alta frena a todos.",
    "Al terminar vas a poder fijar la potencia por banda como punto de partida con varios AP.",
    "Al terminar vas a poder validar el cambio con una caminata medida con WiFiman."
   ],
   "conecta": "En Canales angostos ordenaste quién usa qué canal. Ahora se achica cada celda para que el celular se pase al AP de al lado.",
   "sigue": "Con canal y potencia en orden, el cliente ya puede cambiar de AP. La próxima decide cuánto ayudarlo: BSS Transition, Fast Roaming y mínimo RSSI.",
   "requisitos": ["7"]
  },
  "9": {
   "objetivos": [
    "Al terminar vas a poder explicar qué hacen 802.11k, 802.11v y 802.11r y por qué el roaming lo decide el cliente.",
    "Al terminar vas a poder probar Fast Roaming en un SSID nuevo con un equipo de cada tipo del cliente.",
    "Al terminar vas a poder leer el historial de roaming y armar un SSID de legado en su propia VLAN."
   ],
   "conecta": "En Potencia baja las celdas quedaron del tamaño justo. Recién ahora tiene sentido acelerar el roaming, y en VLAN por función ya tenés dónde poner un SSID de legado.",
   "sigue": "El sitio quedó bien hecho de punta a punta. El último módulo lo multiplica: muchos clientes en Site Manager, empezando por la cuenta de la empresa.",
   "requisitos": ["8", "5"]
  },
  "4": {
   "objetivos": [
    "Al terminar vas a poder verificar Remote Management y los puertos de salida para que una consola aparezca en Site Manager.",
    "Al terminar vas a poder dejar cada consola en la cuenta de la empresa e invitar técnicos con rol limitado.",
    "Al terminar vas a poder armar la planilla de sitios con host, versiones, dueño, admins y último backup."
   ],
   "conecta": "En Quién manda viste que Site Manager es la puerta y no el cerebro. Acá esa puerta se ordena para muchos clientes a la vez.",
   "sigue": "La planilla tiene una columna de último backup y otra de versión. La próxima las pone a trabajar: backups y actualizaciones por etapas.",
   "requisitos": ["1"]
  },
  "11": {
   "objetivos": [
    "Al terminar vas a poder bajar un backup, guardarlo en dos lugares y restaurarlo en una VM de laboratorio.",
    "Al terminar vas a poder leer una nota de versión y anotar versión mínima, qué se elimina y qué se migra.",
    "Al terminar vas a poder actualizar por etapas: Official, espera, sitio piloto y el resto."
   ],
   "conecta": "En Muchos sitios armaste la planilla con versiones y último backup, y en Inform remoto aprendiste a re-apuntar equipos. Las dos cosas se usan al restaurar.",
   "sigue": "Aun con todo bien hecho, va a llegar el llamado de \"el WiFi anda mal\". La última lección arma el método para atenderlo.",
   "requisitos": ["3", "4"]
  },
  "12": {
   "objetivos": [
    "Al terminar vas a poder leer el historial de un cliente y reconocer roam, desconexión y ping-pong.",
    "Al terminar vas a poder revisar Time Machine de radios y puertos antes de tocar nada.",
    "Al terminar vas a poder escribir qué pasó y probar un solo cambio por vez, volviendo atrás si empeora."
   ],
   "conecta": "Los patrones que se buscan acá salen del módulo de WiFi: canal en Canales angostos, potencia en Potencia baja y roaming en Roaming sin magia.",
   "cierre": "Con esto recorriste UniFi completo: de elegir quién manda y adoptar el primer AP a sostener muchos clientes con backups, etapas y un método de soporte. La planilla de sitios, el backup fuera del equipo y la costumbre de mirar el historial antes de tocar son tu kit para la próxima obra.",
   "requisitos": ["7", "8", "9"]
  }
 },
 "avisos": [
  {"id": "5,6,10,4", "archivo": "card.md y script.txt",
   "texto": "El título \"# Lección N.\" de la tarjeta y la primera línea del guion (\"Lección N...\") usan el número de carpeta.",
   "sugerencia": "Si el portal muestra la posición y no el id, renumerar: 5→4, 6→5, 10→6, 4→10. Las lecciones 1, 2, 3, 7, 8, 9, 11 y 12 conservan su número."},
  {"id": "5", "archivo": "script.txt",
   "texto": "A: Lección cinco. Martín, ¿cuál es la red más común que encontramos en un cliente chico?",
   "sugerencia": "A: Lección cuatro. Martín, ¿cuál es la red más común que encontramos en un cliente chico?"},
  {"id": "6", "archivo": "script.txt",
   "texto": "A: Lección seis. Te cuento una escena.",
   "sugerencia": "A: Lección cinco. Te cuento una escena."},
  {"id": "10", "archivo": "script.txt",
   "texto": "A: Lección diez. Red de invitados.",
   "sugerencia": "A: Lección seis. Red de invitados."},
  {"id": "4", "archivo": "script.txt",
   "texto": "A: Lección cuatro. Martín, ¿cuántos sitios UniFi tenemos?",
   "sugerencia": "A: Lección diez. Martín, ¿cuántos sitios UniFi tenemos?"}
 ]
}
out = "/home/claude/ies-training/ilustraciones/unifi/estructura.json"
json.dump(E, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
s = json.dumps(E, ensure_ascii=False)
print("ok", out, "dashes:", "—" in s or "–" in s)
