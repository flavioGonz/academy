# Plan: HikCentral Professional: videovigilancia y control de acceso centralizado

Público: técnicos instaladores y de soporte de IES Training, con base de redes. Nivel inicial a intermedio. 12 lecciones en 3 arcos de 4. Fuentes: 23 páginas en raw/web (17 oficiales de Hikvision: manual del Web Client V2.x, Quick Start Guide, FAQ V2.5.500, Communication Matrix V2.4.1, System Requirements V2.4.510 y artículos del soporte de Hikvision USA; 6 de terceros: learncctv, VXG, SecurityInformed, Benchmark).

Versiones: la línea vigente a octubre 2026 es HikCentral Professional V3.x. La documentación leída es V2.4 a V2.6.1 porque las páginas de V3 en hikvision.com no se pudieron leer (desafío JavaScript). Los conceptos (SYS, licencias, ISUP, áreas, niveles de acceso) se mantienen; las rutas de menú pueden cambiar de nombre en V3 y cada tarjeta lo avisa.

Cómo leer "N de M": M son las páginas que tocan el subtema, N las que sostienen la idea. Como casi todo es documentación del mismo fabricante, el acuerdo indica coherencia de Hikvision más que consenso independiente; cada lección lo dice.

## Arco 1. Fundamentos: el servidor bien parado
Por qué este arco: antes de agregar una sola cámara, la plataforma tiene que estar bien dimensionada, instalada, licenciada y con un plan para cuando haya que tocar el servidor. Cierra con un servidor de laboratorio activado y respaldado.

### Lección 1. Mapa de capas
- Quién lo dice: 3 de 4 fuentes de arquitectura (TH02); la familia HikCentral, 2 de 2 (TH01), evidencia fina.
- Idea: el SYS gestiona, el Streaming Gateway o Server reenvía video, el Web Client configura y el Control Client opera; Professional es el hermano mayor de la familia (Lite y Access Control para sitios chicos, Connect y FocSign en otros nichos).
- Por qué importa: cada falla cae en una capa; saber cuál ahorra horas.
- Historia: el SYS trae un gateway que según el FAQ sirve hasta 200 cámaras; por eso el Streaming Server nunca va en la misma máquina. Y el error VSM217 cuando el Control Client no es de la misma versión que el SYS. https://pinfo.hikvision.com/hkwsen/unzip/20240603152919_44907_doc/UD38113B_HikCentral%20Professional%20V2.5.500_FAQ_V2.5.500_20240603.pdf
- Laboratorio: Rápido, 10 min. Abrir Service Manager en el servidor de laboratorio, anotar servicios y puertos, comparar versión del SYS y del Control Client, dibujar el diagrama de capas de una obra.
- Regla: antes de diagnosticar, ubicá la capa.

### Lección 2. Servidor a medida
- Quién lo dice: 2 de 4 (TH05) y 2 de 2 (TH07, TH08). Discrepa VXG: el costo real está en operar el servidor.
- Idea: dimensionar con la guía de requisitos (perfil bajo i5, 8 GB, 650 GB; Xeon y 16 a 32 GB para cargas altas), instalar como administrador, típico o personalizado, verificar MD5, usar el Service Manager.
- Historia: puerto en rojo en el Service Manager, resuelto con netstat y tasklist. https://pinfo.hikvision.com/hkwsen/unzip/20230911113416_60121_doc/pdf.pdf
- Laboratorio: Foco, 20 min. VM de laboratorio, verificar hash del instalador, instalación típica, revisar puertos con netstat.
- Regla: instalador verificado, permisos de admin y Control Client nunca en VM.

### Lección 3. Licencia sin sorpresas
- Quién lo dice: 2 de 5 (TH10, TH11); los códigos de error salen de una sola fuente (TH13).
- Idea: primero una licencia base, después expansiones; online si el SYS tiene internet, offline con archivo de pedido y respuesta dentro de 24 h y hora correcta; registrar el email del admin.
- Historia: error 1105 por usar una respuesta vieja o hacer doble clic al exportar el pedido; 1113 por activar expansión sin base. https://pinfo.hikvision.com/hkwsen/unzip/20240603152919_44907_doc/UD38113B_HikCentral%20Professional%20V2.5.500_FAQ_V2.5.500_20240603.pdf
- Laboratorio: Admin, 15 min. Verificar hora del servidor, recorrer el panel de activación offline, armar la ficha de licencia de la obra.
- Regla: base primero, hora en hora, y la ficha de licencia en la carpeta de la obra.

### Lección 4. Antes de tocar
- Quién lo dice: 4 de 5 sobre desactivar antes de cambiar hardware (TH12); 3 de 4 sobre backups (TH33).
- Idea: antes de cambiar hardware, migrar o actualizar: backup del sistema copiado fuera del SYS y licencia desactivada.
- Historia: SYS que alterna Starting y Stopped tras un cambio de hardware; la migración de VM rompe la verificación de licencia. https://pinfo.hikvision.com/hkwsen/unzip/20230911113613_29615_doc/HikCentral%20Professional_System%20Requirements%20and%20Performance_V2.4.510_20230907.pdf
- Laboratorio: Admin, 15 min. Programar backup semanal, hacer uno ahora, copiarlo fuera del servidor, escribir el checklist de cambio.
- Regla: antes de tocar el servidor, backup afuera y licencia desactivada. Siempre.

## Arco 2. Operación diaria: equipos, video y alarmas
Por qué este arco: es lo que se hace en cada obra: dar de alta equipos, ordenarlos, decidir dónde graban y qué avisa. Cierra con un sitio de laboratorio con cámaras en áreas, grabando y con alarmas útiles.

### Lección 5. Tres formas de alta
- Quién lo dice: IP 3 de 7 (TH14), ISUP 2 de 7 (TH15), Hik-Connect 2 de 7 (TH16). Discrepa learncctv, que enseña port forwarding directo.
- Idea: IP o dominio cuando hay IP fija (puerto 8000, 8443 cifrado); ISUP cuando el equipo no tiene IP fija y registra hacia el SYS (puerto 7660); Hik-Connect como atajo con límites de grabación.
- Historia: el manual presenta ISUP como la opción "costo efectiva" sin IP fija. https://enpinfo.hikvision.com/hkwsen/unzip/20230830144955_12918_doc/GUID-5A97A28D-C1DB-4653-B440-FAAC67F3FDE2.html
- Laboratorio: Campo, 20 min. Habilitar registro ISUP, configurar la cámara de laboratorio con Device ID y clave, agregarla por Device ID.
- Regla: IP fija, por IP; sin IP fija, ISUP; Hik-Connect solo si aceptás sus límites.

### Lección 6. Áreas primero
- Quién lo dice: 3 de 7 sobre importar a un área (TH17); áreas hijas y vistas con evidencia fina (TH19, TH20, TH30).
- Idea: un equipo sin canales en un área no tiene vivo ni reproducción; las cámaras van en el área donde se usan; vistas públicas para el puesto, privadas por operador; E-map para planos, GIS para geografía.
- Historia: "There is no camera in this area" por tener las cámaras en el área hija. https://pinfo.hikvision.com/hkwsen/unzip/20240603152919_44907_doc/UD38113B_HikCentral%20Professional%20V2.5.500_FAQ_V2.5.500_20240603.pdf
- Laboratorio: Rápido, 15 min. Árbol de áreas por edificio y piso, importar canales, vista pública de cuatro cámaras.
- Regla: el árbol de áreas se diseña antes de dar de alta el primer equipo.

### Lección 7. Dónde graba
- Quién lo dice: 3 de 3 (TH21). Limitaciones de Hik-Connect y dominio (TH16).
- Idea: al dar de alta se decide si graba el equipo (NVR) o un almacenamiento central (pStor, Hybrid SAN, Cloud Storage), y cada opción tiene límites.
- Historia: los equipos agregados por dominio o Hik-Connect no graban en Hybrid SAN ni Cloud Storage; pStor Cluster no hace grabación por movimiento. https://pinfo.hikvision.com/hkwsen/unzip/20240603152919_44907_doc/UD38113B_HikCentral%20Professional%20V2.5.500_FAQ_V2.5.500_20240603.pdf
- Laboratorio: Foco, 15 min. Tabla de decisión para una obra y verificación del estado de grabación.
- Regla: la ubicación de la grabación se decide por cámara, por escrito, antes del alta.

### Lección 8. Alarmas con criterio
- Quién lo dice: 2 de 2 (TH23), evidencia fina; ruido y pre/post evento salen del manual de eventos (TH24, TH25).
- Idea: evento es disparador más acción; alarma solo lo que alguien atiende; ignorar repetidos y demorar la de cámara offline.
- Historia: Delay Alarm para que mantenimiento vea las cámaras realmente caídas; más de 20 eventos con foto por segundo traban el Web Client. https://pinfo.hikvision.com/hkwsen/unzip/20240822164538_35347_doc/GUID-7C8C6C1B-5438-4C6B-8C71-B042A25AE1BB.html
- Laboratorio: Foco, 20 min. Evento de cámara offline con demora y alarma de entrada con grabación pre y post y bloqueo.
- Regla: si nadie la va a atender, no es alarma: es evento.

## Arco 3. Acceso, gestión y troubleshooting
Por qué este arco: el control de acceso y la asistencia son donde más llamadas de soporte aparecen, y el troubleshooting cierra el curso con un método. Cierra con un circuito completo: persona, puerta, marca, rol y diagnóstico.

### Lección 9. Niveles de acceso
- Quién lo dice: 1 de 3 sobre aplicar (TH26), 1 de 3 sobre una sola fuente de personas (TH27); fuente oficial única, evidencia fina.
- Idea: persona con credencial, nivel de acceso (puertas más plantilla de horario), asignación y, siempre, aplicar a los dispositivos; "Apply (Initial)" deja las puertas offline.
- Historia: durante el aplicado inicial las controladoras quedan offline y nadie pasa. https://enpinfo.hikvision.com/hkwsen/unzip/20230830144955_12918_doc/GUID-3F50D8C7-95C9-478B-B4D5-189A09C3D708.html
- Laboratorio: Campo, 20 min. Persona con tarjeta, nivel con plantilla de días hábiles, aplicar cambios, probar en la lectora.
- Regla: nada cambia en la puerta hasta que aplicás, y el aplicado inicial va fuera de horario.

### Lección 10. Asistencia y hora
- Quién lo dice: 1 de 2 (TH29) y 1 de 3 sobre zona horaria (TH28); evidencia fina.
- Idea: puntos de marca, regla general, plantilla de turno, turno, asignación; todo con la misma hora y zona en controladoras y SYS.
- Historia: turno Man-Hour de 8 a 17 con primera entrada y última salida; pasadas que no aparecen en vivo por zona horaria distinta. https://supportusa.hikvision.com/support/solutions/articles/17000120924-time-and-attendance-setup-on-hikcentral
- Laboratorio: Admin, 20 min. Configurar asistencia para un grupo de prueba y ver el registro del día siguiente.
- Regla: primero la hora, después los turnos.

### Lección 11. Roles y cuentas
- Quién lo dice: 2 de 5 (TH31) y 4 de 5 sobre endurecer (TH32). Voz crítica: learncctv sobre el historial de seguridad de Hikvision.
- Idea: roles a medida con áreas visibles y horario de permisos; contraseña fuerte, HTTPS con certificado propio, nada expuesto sin necesidad.
- Historia: el certificado embebido muestra "No seguro" hasta subir un .pem firmado. https://supportusa.hikvision.com/support/solutions/articles/17000110020-how-to-generate-and-install-https-certificate-for-hikcentral
- Laboratorio: Admin, 15 min. Rol "Guardia" con un área y horario, usuario de prueba, fuerza de contraseña en Strong.
- Regla: cada persona su usuario, cada usuario el rol mínimo.

### Lección 12. Offline de abajo arriba
- Quién lo dice: 4 de 8 (TH35) y 3 de 8 sobre puertos (TH34). Learncctv enfoca en abrir puertos de los equipos.
- Idea: diagnosticar de abajo hacia arriba (cable, IP y gateway, DNS, servicio, puertos) y validar puertos contra la Communication Matrix.
- Historia: vivo que anda en IE pero no en Chrome por el puerto 559; NVR que llega a 128 conexiones. https://supportusa.hikvision.com/support/solutions/articles/17000146654-troubleshooting-platform-access-offline-on-device
- Laboratorio: Campo, 15 min. Checklist con ping, Test-NetConnection a 8000, 7660 y 559, revisar log de online/offline.
- Regla: de abajo hacia arriba, y cada puerto contra la matriz.

## Divisiones (decisiones, no lecciones)
- Acceso remoto: port forwarding directo (https://learncctv.com/hikvision-port-forwarding/) contra registro saliente por ISUP o Hik-Connect (https://enpinfo.hikvision.com/hkwsen/unzip/20230830144955_12918_doc/GUID-5A97A28D-C1DB-4653-B440-FAAC67F3FDE2.html). Cómo decidir: con IP fija y VPN, por IP sobre la VPN; sin IP fija, ISUP; abrir puertos a internet como último recurso y con contraseñas fuertes.
- Dónde grabar: en el NVR del sitio contra central (pStor, Hybrid SAN). Cómo decidir: si el enlace al centro es chico o inestable, en el sitio; si hace falta retención y redundancia central y hay ancho de banda, central, revisando las limitaciones del FAQ.
- On-premises contra nube: VXG (https://www.videoexpertsgroup.com/glossary/hikcentral-professional) dice que operar el servidor es la carga principal. Cómo decidir: si el cliente o el integrador no puede mantener backups, parches y licencias, presupuestá ese mantenimiento o evaluá otra arquitectura.
- Personas en plataforma o en equipo: el FAQ pide una sola fuente. Cómo decidir: con HikCentral, alta en la plataforma y aplicar a equipos; en sitios sin servidor permanente, en el equipo.

## Huecos
- Sin documentación V3.x leída; las rutas de menú son de V2.x.
- Foros independientes (ipcamtalk) no accesibles a scripts; la voz de practicantes es fina.
- T07, T09, T11 y T12 con evidencia fina; restauración y plantillas de horario de acceso sin página propia en raw/.
- Precios y contratos de mantenimiento de licencias fuera de alcance.

## Entrega
12 carpetas class/NN-handle con script.txt, card.md y quiz.json; class/course.json con la ficha. El audio lo renderiza el orquestador.
