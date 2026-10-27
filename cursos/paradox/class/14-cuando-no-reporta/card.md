# Lección 14. Cuando no reporta

**Escuchá:** cuando-no-reporta.mp3 (2 min)

**La idea, en tres líneas**
- Orden de diagnóstico: serie (LED RX/TX del módulo), red (cable, IP, salida a internet), puertos de salida, receptora.
- En SP/MG, la sección del estado del receptor ([935]) muestra el registro IP/GPRS: grupo 2 errores del módulo, grupo 3 programación incompleta, grupo 4 errores de registro. ARM registra cuando no hay errores.
- Al cambiar un módulo, el receptor puede seguir atado a la MAC anterior; reiniciar el módulo desde BlueEye tarda hasta 5 min (firmware 4.xx) o 15 min (5.xx).

**Impacto:** dejás de reiniciar a ciegas y llegás a la causa con un número del teclado y una llamada a monitoreo.

**Quién lo dice:** 4 de 6 fuentes coinciden (guía de programación SP+, guía del menú instalador BlueEye, manual IP180, foro openHAB); ninguna discrepa. El límite de una conexión por vez es experiencia de usuarios del foro.

**Laboratorio** · Foco · 20 min
Central SP o MG con IP150+ o IP180 y reporte IP ya programado (lección 11).
1. Leé el estado:
```text
[ENTER] + código de instalador + [935]
```
Tabla de la guía de programación SP+:
```text
Grupo  Qué es                         Submenú
1      Estado de registro             apagado = sin registrar, titila = registrando, fijo = OK
2      Error del módulo               7 sin módulo, 8 cable desenchufado (PCS sin servicio), 9 sin IP / sin red GPRS
3      Error de programación          7 sin IP, 8 sin puerto, 9 sin abonado, 10 sin APN (GPRS)
4      Error de registro              7 no conecta, 8 perfil inválido, 9 formato inválido, 10 abonado registrado con otra MAC
```
2. Desenchufá el cable de red y mirá el grupo 2. Volvé a enchufar.
3. Borrá el puerto en [930] y mirá el grupo 3. Volvé a cargarlo.
4. Poné un perfil que la receptora no tenga en [934] y mirá el grupo 4. Corregilo.
5. Sin errores, en [935] apretá ARM para registrar y confirmá con el operador.
6. Desde BlueEye (menú instalador, programación de módulos, reinicio) reiniciá el módulo y cronometrá hasta que vuelva.
7. Si aparece "abonado registrado con otra MAC" después de cambiar un módulo, pedile a monitoreo que libere el abonado del módulo anterior.

⚠️ En un IP180 sin Ethernet, el módulo abre un punto de acceso propio (IP180 más número de serie, 192.168.180.1) para cargar el Wi-Fi: no lo dejes así en obra.

**Regla para quedarse**
De la central hacia afuera: serie, red, puertos, receptora.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Tabla de estados de registro IP/GPRS y secciones de receptor (guía de programación SP+): https://www.paradox.com/Downloader/?ID=11650
- Reinicio de módulo y tiempos de sondeo (guía del menú instalador BlueEye): https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Software/BlueEye/BlueEye_Installer_Menu_v2.0%20.pdf
- LEDs, puertos y punto de acceso del IP180: https://www.paradox.com/Downloader/?ID=12435
