# Lección 5. Grabación y hora

**Escuchá:** grabacion-y-hora.mp3 (2 min)

**La idea, en tres líneas**
- Cada cámara LPR va vinculada a un NVR y a un canal: es lo que permite abrir el video en el segundo exacto de la lectura, bajar el clip y armar el ZIP de evidencia. Sin canal, el historial dice "sin NVR".
- En Dispositivos: Detectar grabaciones busca la IP de cada cámara en los canales de todos los NVR, Calcular retención dice cuántos días guarda ese canal y Sincronizar hora muestra el desfase de cada cámara y NVR y pregunta antes de corregir.
- Cámara, NVR y servidor con la misma hora: la hora del servidor se empuja sin internet, o se usa NTP si hay un servidor de hora en la red. Con más de 120 segundos de diferencia se abre una alerta.

**Impacto:** la evidencia que se entrega coincide con el evento y el disco alcanza para la retención que se le prometió al cliente.

**Quién lo dice:** 4 de 4 fuentes coinciden en que sin hora sincronizada la grabación pierde valor de prueba (Mobatime, CCTV Camera World, Fora Soft y el Manual del Instalador). Discrepan en el método: las de video recomiendan NTP; OmniAccess agrega empujar la hora del servidor, que anda en redes sin internet.

**Laboratorio** · Admin · 15 min
En una instalación de prueba con al menos una cámara LPR y un NVR dados de alta.
1. Dispositivos → vista Cámaras LPR → botón Detectar grabaciones. Cada cámara tiene que quedar "Vinculada a" un NVR y un canal.
2. Abrí la ficha de una cámara → Calcular retención. Anotá cuántos días guarda ese canal.
3. Botón Sincronizar hora: anotá el desfase de cada cámara y NVR. Si alguno pasa los 120 segundos, confirmá poner la hora del servidor.
4. Abrí una lectura reciente → Grabación. Compará la hora impresa en el video con la hora del evento: tienen que coincidir al segundo.
5. Configuración → Sistema → Almacenamiento: anotá la retención de fotos y de clips y hacé la cuenta del disco.
```text
fotos por día (8 cámaras, tráfico normal, según el manual): 3 a 4 GB
3,5 GB x 30 días de retención = 105 GB solo de fotos (el manual redondea a 120 GB)
```
⚠️ Bajar la retención para que entre en el disco es perder evidencia: si falta espacio, se agranda el disco.

**Regla para quedarse**
Misma hora en cámara, NVR y servidor, y lo verifico en cada visita de mantenimiento.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Por qué la hora exacta decide si una grabación sirve de prueba: https://mobatime.com/support/faq/why-is-time-important-for-cctv
- Sincronizar con la PC o con NTP, y qué pasa con cada uno: https://www.cctvcameraworld.com/security-cameras-must-show-accurate-time-for-court/
- La deriva de reloj entre cámaras, en una línea: https://www.forasoft.com/learn/video-surveillance/glossary/terms-vms/time-sync
