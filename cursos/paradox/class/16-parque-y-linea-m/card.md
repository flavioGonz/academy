# Lección 16. Parque y línea M

**Escuchá:** parque-y-linea-m.mp3 (2 min)

**La idea, en tres líneas**
- La M25 / M25 LTE (según su ficha): PoE, batería de litio interna, Wi-Fi, Ethernet y LTE; 200 zonas, 10 particiones, inalámbrico M y hasta 45 dispositivos por Ethernet; programación por BlueEye o software web; reporte directo a receptora en hasta 4 canales; servicios de app con Swan 4G por suscripción.
- En el parque SP, MG y EVO, desde firmware 7.50 (primero EVO, después las plus) el puerto serie solo trabaja con dispositivos Paradox; para terceros hay un código de desbloqueo oficial pago (5 USD), cargado en [300] (MG/SP+) o [3000] (EVO).
- La decisión es por sitio: actualizar, desbloquear, migrar o dejar, sabiendo qué integración se corta.

**Impacto:** ninguna actualización deja a un cliente sin su integración, y la migración a M se propone con datos, no con folleto.

**Quién lo dice:** la línea M sale de 1 fuente (ficha de producto Paradox), evidencia fina. Puerto serie: la guía de BlueEye describe el bloqueo y el desbloqueo pago; PAI discrepa y recomienda no actualizar EVO a 7.50 o más si se usa conexión serie.

**Laboratorio** · Admin · 15 min
1. Elegí tres sitios de la cartera y completá:
```text
Sitio  Central / firmware  Módulo / generación  Integración serie  Receptora  App   Decisión
A      EVO192 / ____       IP150+ / TURN        sí / no            IPR512     ____  ________
B      SP6000+ / ____      IP180 / MQTT         sí / no            IPC10      ____  ________
C      obra nueva          no aplica            no aplica          ____       ____  ________
```
2. Reglas para decidir:
- Integración serie de terceros y firmware por debajo de 7.50: no actualizar sin plan; si hace falta actualizar, presupuestar el código de desbloqueo oficial.
- Desbloqueo: se compra en BlueEye (menú instalador, tres puntos, "Unlock Panel") y se carga con TM50, TM70, K641+ o K32LCD+, que admiten letras:
```text
MG/SP+:  [ENTER] + código de instalador + [300] + código de desbloqueo
EVO:     mantener [0] + código de instalador + [3000] + código de desbloqueo
```
- Obra nueva sin cableado: evaluar M25 en banco antes de ofrecerla (PoE, inalámbrico, suscripción Swan 4G, receptora compatible).
- Obra con cableado y bus existentes: SP+ o EVO siguen siendo la opción natural.
3. Anotá la decisión y quién la aprobó.

⚠️ No actualices firmware de central o módulo en un sitio con integración serie sin avisar al cliente: después de 7.50 la integración deja de funcionar hasta cargar el desbloqueo.

**Regla para quedarse**
Actualizo firmware sabiendo qué integración se puede cortar.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Ficha de la M25 / M25 LTE: https://www.paradox.com/web/product/m25-m25-lte/
- Bloqueo del puerto serie y desbloqueo pago (guía del menú instalador BlueEye V2.0): https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Software/BlueEye/BlueEye_Installer_Menu_v2.0%20.pdf
- La voz en contra: no actualizar EVO a 7.50 con conexión serie (PAI): https://www.mintlify.com/ParadoxAlarmInterface/pai/connection/overview
