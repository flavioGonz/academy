# Notes: batch d (Safe Mode, lección 23)
Pages read: 10 (9 nuevas y la página congelada de Configuration Management ya en raw/). With notes: 10. Skipped: 0.

Páginas: manual.mikrotik.com 7.25 (Configuration Management, WinBox), help.mikrotik.com congelado (Configuration Management, Command Line Interface), forum.mikrotik.com (Safe mode in webfig, Safe Mode Powercycle, A Better Safe Mode, How to execute risky commands safely), cyberlab.pacific.edu (guía de laboratorio universitaria), mikrotikdocs.fyi (Winbox and WebFig).

## T13 Backups, export y gestión de cambios (Safe Mode)
- d:N1. Safe Mode existe porque un cambio puede dejar el router inaccesible salvo por consola local, y una vez cortada la conexión no hay forma de deshacer el último cambio.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/configuration-management/  Quote: "there is no way to undo the last change when the connection to the router is already cut"
  - Kind: definition
  - Level: foundation
- d:N2. Se activa con el botón Safe Mode de WinBox, o en la CLI con Ctrl+X o F4. Aparece el mensaje "Safe Mode taken" y el prompt suma <SAFE>.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/configuration-management/  Quote: "the prompt changes to reflect that the session is now in safe mode"
  - Kind: technique
  - Level: foundation
  - Also: T01
- d:N3. Todos los cambios hechos mientras el router está en Safe Mode, también desde otras sesiones, se deshacen solos si la sesión dueña del Safe Mode termina de forma anormal. Se ven con flag F (floating-undo) en /system/history.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/configuration-management/  Quote: "also from other login sessions"
  - Kind: technique
  - Level: core
- d:N4. Si se corta la conexión, la reversión llega "después de un rato": la documentación da el timeout TCP de 9 minutos como referencia.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/configuration-management/  Quote: "TCP timeout is 9 minutes"
  - Kind: number
  - Level: core
- d:N5. Ctrl+D también deshace todo lo hecho en Safe Mode; /quit no lo deshace (cuenta como salida normal). Ctrl+X otra vez sale del modo seguro conservando los cambios.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/configuration-management/  Quote: "Exiting the session by [Ctrl]+[D] also undoes all safe mode changes, while /quit does not"
  - Kind: technique
  - Level: foundation
- d:N6. Una guía de laboratorio universitaria lo resume igual: Ctrl+X de nuevo guarda y sale, Ctrl+D sale sin guardar, quit es salida normal y guarda.
  - Source: https://cyberlab.pacific.edu/courses/comp177/resources/routeros-overview  Quote: "quit is considered as a normal termination"
  - Kind: technique
  - Level: foundation
- d:N7. Si otro usuario quiere tomar el Safe Mode, RouterOS pregunta unroll, release o don't take: u deshace los cambios del otro y toma el modo, r los conserva y toma el modo (el dueño anterior ve "Safe mode released by another user"), d no toca nada.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/configuration-management/  Quote: "Hijacking Safe Mode from someone"
  - Kind: technique
  - Level: core
- d:N8. El historial guarda las 100 acciones más recientes; si en Safe Mode se hacen más cambios de los que entran, la sesión sale sola del modo seguro y no se deshace nada. Conviene trabajar en pasos chicos; apretar Ctrl+X dos veces vacía la lista de acciones del modo seguro.
  - Source: https://manual.mikrotik.com/docs/7.25/getting-started/configuration-management/  Quote: "currently history keeps up to the 100 most recent actions"
  - Kind: mistake
  - Level: core
- d:N9. WinBox 4: la barra superior tiene Undo y Redo (máximo 100 comandos deshacibles) y el interruptor Safe Mode.
  - Source: https://manual.mikrotik.com/docs/7.25/management-tools/winbox  Quote: "Maximum possible amount of the commands that can be undone is 100"
  - Kind: definition
  - Level: foundation
  - Also: T01
- d:N10. Según la página de CLI, en Safe Mode la configuración se guarda en disco recién cuando se apaga el modo seguro. Atajos: Ctrl+X o F4 alternan Safe Mode.
  - Source: https://help.mikrotik.com/docs/spaces/ROS/pages/328134/Command+Line+Interface  Quote: "the configuration is saved to disk only after the safe mode is turned off"
  - Kind: definition
  - Level: core
- d:N11. Un usuario probó Safe Mode en WinBox: quitar la IP y esperar 10 minutos devolvió la configuración; quitar la IP y cortar la energía dejó el cambio aplicado (otro usuario lo confirma en 6.40.4). En equipos locales la reversión llegaba en segundos o menos de 30 s; por WAN tardaba más.
  - Source: https://forum.mikrotik.com/t/safe-mode-powercycle-useless/105625  Quote: "Powercycle Device → Stupid config change seems to be committed"
  - Kind: story
  - Level: core
- d:N12. Safe Mode se dispara por el cierre de la sesión, no por un temporizador: si el cambio que hacés corta tu sesión a propósito (cambiar el túnel por el que entrás), se deshace igual. Un veterano lo señala como su límite.
  - Source: https://forum.mikrotik.com/t/safe-mode-powercycle-useless/105625  Quote: "rolls back all changes when the login session (telnet, webfig, winbox) is inadvertently closed"
  - Kind: mistake
  - Level: advanced
- d:N13. Para lo que Safe Mode no cubre, un veterano propone backup más un scheduler que lo restaura a los 5 minutos si no lo borrás a tiempo.
  - Source: https://forum.mikrotik.com/t/how-to-execute-risky-mikrotik-commands-safely/165189  Quote: "create a job that resore automatically the backup"
  - Kind: technique
  - Level: advanced
- d:N14. En WebFig también hay Safe Mode. Ejemplo de un empleado de MikroTik: con Safe Mode, agregar un drop en input; WebFig queda bloqueado y al minuto reconecta con la regla borrada. Cada sesión es independiente: el Safe Mode de WebFig no vigila la sesión SSH.
  - Source: https://forum.mikrotik.com/t/safe-mode-in-webfig/92508  Quote: "after a minute, it will reconnect and the rule will be gone"
  - Kind: story
  - Level: foundation
- d:N15. El botón de WinBox a veces queda apretado sin que el equipo haya entrado en modo seguro (enlaces malos); la sugerencia es usar Ctrl+X en la terminal de WinBox, donde el prompt confirma. La prueba de banco: deshabilitar a propósito la interfaz por la que entrás.
  - Source: https://forum.mikrotik.com/t/a-better-safe-mode/85802  Quote: "You will get immediate confirmation that Safe Mode took effect when the CLI prompt changes"
  - Kind: test
  - Level: core
- d:N16. Una guía de practicantes dice que la reversión llega "en unos 9 minutos (configurable)" y que los cambios quedan "en una cola pendiente". La documentación oficial no menciona un timeout configurable, y los cambios se aplican en el acto (por eso te cortan).
  - Source: https://mikrotikdocs.fyi/management-tools/winbox-webfig/  Quote: "approximately 9 minutes (configurable)"
  - Kind: definition
  - Level: core
  - Bias: guía no oficial; contradice a la documentación en dos detalles.

## Disagreements seen
- Corte de energía en Safe Mode: la página de CLI dice que la configuración se guarda en disco recién al salir del modo seguro (https://help.mikrotik.com/docs/spaces/ROS/pages/328134/Command+Line+Interface); usuarios del foro vieron el cambio confirmado después de cortar la energía en 6.40.4 (https://forum.mikrotik.com/t/safe-mode-powercycle-useless/105625). Para RouterOS 7 no hay confirmación leída.
- Tiempo de reversión: la documentación da 9 minutos de timeout TCP; el foro reporta segundos en local, un minuto en WebFig y más por WAN. mikrotikdocs.fyi lo llama configurable, cosa que la documentación no dice.
- Cuánto tiempo quedarse en Safe Mode: la guía universitaria propone entrar al empezar el laboratorio y salir al final; la documentación y un veterano del foro piden pasos chicos y alternar Safe Mode entre pasos, por el tope de 100 acciones.
- Otras sesiones: la documentación dice que se deshacen también los cambios de otras sesiones; un empleado de MikroTik aclara que solo se vigila la sesión que tomó el Safe Mode. Se complementan: lo que vigila es una sesión, lo que deshace es todo lo marcado con F.

## Best stories
- Drop en input con Safe Mode en WebFig: te bloquea y al minuto reconecta con la regla borrada (https://forum.mikrotik.com/t/safe-mode-in-webfig/92508).
- Quitar la IP en Safe Mode y cortar la energía: el cambio quedó (https://forum.mikrotik.com/t/safe-mode-powercycle-useless/105625).
- El botón de WinBox apretado sin modo seguro real en un radioenlace malo (https://forum.mikrotik.com/t/a-better-safe-mode/85802).
