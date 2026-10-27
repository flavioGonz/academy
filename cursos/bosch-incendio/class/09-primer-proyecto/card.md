# Lección 9. Primer proyecto

**Escuchá:** primer-proyecto.mp3 (2 min)

**La idea, en tres líneas**
- FSP-5000-RPS se baja de la extranet de Bosch con usuario habilitado; la versión vigente a octubre de 2026 es 5.15.28 (5.15.27 y 5.14.17 tenían un problema con el FLM-420-RLE-S). Corre en Windows 11 24H2 de 64 bits.
- La cuenta de configuración 4.8 corresponde al firmware 4.8 y agrega Uruguay a la lista de países; de 3.x a 4.x se sube en tres pasos (a 3.5, cambiar nodos a AVENAR, subir a 4.x).
- Secuencia de puesta en marcha: alimentar, calibrar pantalla, fecha, hora, número de nodo (PNA) y red, reiniciar, USB, autodetección, editar, descargar, walk test, pruebas y diagnóstico guardado como acta.

**Impacto:** la primera descarga sale bien y queda un acta que respalda la puesta en marcha.

**Quién lo dice:** 3 de 3 fuentes coinciden (System manual, TI 2715 y TI 2739); sin discrepancias. La ayuda completa de RPS solo está en la extranet.

**Laboratorio** · Admin · 20 min
Sin panel, en la oficina:
1. Abrí FSP-5000-RPS y verificá la versión (5.15.28 o posterior).
2. Creá una configuración nueva y elegí:
```text
Versión de cuenta: AVENAR panel 4.8
País: Uruguay
Nodo 1: AVENAR panel 2000 (PNA 1)
Módulos: LSN 0300 A en la primera posición del riel
Lazo: 10 x FAP-425-O-R en direcciones 1 a 10 (dirección manual, T-tap marcado)
```
3. Corré el chequeo de consistencia y anotá cada error, advertencia y pista.
4. Guardá y exportá una copia con fecha en el nombre.
5. Escribí tu checklist de obra:
```text
[ ] Copia de la configuración del panel antes de tocar
[ ] Set Panel Time
[ ] Chequeo de consistencia sin errores
[ ] Descarga
[ ] Walk test y pruebas
[ ] Diagnóstico guardado como acta
[ ] Copia de la configuración final
```
⚠️ Una descarga cambia el comportamiento de un sistema de seguridad de vida: en un sitio ocupado se hace con el monitoreo avisado y con prueba funcional después.

**Regla para quedarse**
Antes de cada descarga: copia de la configuración, Set Panel Time y consistencia sin errores.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Firmware 4.8.1, RPS 5.15.27, país Uruguay y problemas conocidos (TI 2715): https://media.boschbuildingtechnologies.com/fs/media/pb/media/extranet/fire_alarm_system/tech_info_en/2715_2026_TI_AVENAR_FW-4.8.1__FSO-5000-RPS_5.15.27.pdf?collection=bosch-bt-lifesafetysystems
- Guía de puesta en marcha (System manual): https://media.boschsecurity.com/fs/media/pb/media/extranet/fire_alarm_system/documentation/avenar_panel_system_information/BDL_SYM_AVENAR_panel_F01U378910_05_en.pdf
- RPS 5.15.28 en la TI de septiembre 2026: https://media.boschbuildingtechnologies.com/fs/media/pb/media/extranet/fire_alarm_system/tech_info_en/2739_2026_TI_2739_2026_TI_FSP-5000-RPS_EN.pdf?collection=bosch-bt-lifesafetysystems
