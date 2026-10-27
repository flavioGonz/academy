# Lección 13. Primero el TBL

**Escuchá:** primero-el-tbl.mp3 (2 min)

**La idea, en tres líneas**
- TBL muestra grupos de fallas; cada número abre su submenú. Los que más aparecen: 2 (2.1 batería, 2.2 AC, 2.3 sobrecarga AUX), 3 campana, 4 comunicación, 5 tamper o cableado de zona, 8 pérdida de reloj, 10 módulo del bus sin respuesta.
- La falla de un módulo quitado del bus no la limpia el reset: se borra en [955]. La falla de AC se ve enseguida, pero se reporta después del retardo de [839] (15 min de fábrica).
- LED de estado de la placa: un destello por segundo es normal; un segundo encendido y uno apagado indica falla.

**Impacto:** muchas llamadas por "pitidos" se resuelven por teléfono o en una visita corta.

**Quién lo dice:** 4 de 4 fuentes coinciden (guías de instalación y programación SP+, guía rápida K32LCD+, guía EVOHD+). Todas del fabricante o su distribuidor; no se encontró quien discrepe.

**Laboratorio** · Campo · 20 min
Central SP+ de banco con teclado, sirena o resistencia de campana y un ZX8. Después de cada paso: TBL, número de grupo, anotá el submenú, y volvé a dejar todo normal.
```text
Acción en el banco                    Grupo esperado en TBL
Sacar la batería                      2, submenú 1 (batería de la central)
Cortar la red de 16,5 Vac             2, submenú 2 (falla de AC)
Sacar la resistencia de BELL          3, submenú 1 (campana desconectada)
Abrir la tapa del ZX8                 6, submenú 3 (tamper de módulo ZX8)
Desconectar el ZX8 del bus            10, submenú 3 (supervisión de módulo)
Cortar red y batería, y volver        8 (pérdida de reloj)
```
1. Para la pérdida de reloj, cargá fecha y hora desde el menú rápido ("Time and Date" en la guía de programación) o desde BabyWare.
2. Si dejás el ZX8 afuera definitivamente, limpiá su falla:
```text
[ENTER] + código de instalador + [955]
```
3. Mirá el LED de estado de la placa en cada paso y anotá cuándo pasa de un destello por segundo a un segundo encendido y uno apagado.
4. Con un K32LCD+ la falla aparece en texto: TBL y flechas para recorrerla.

⚠️ Si la central reporta a monitoreo, avisá antes: varias de estas pruebas generan reportes de falla y de tamper.

**Regla para quedarse**
Ningún diagnóstico arranca sin mirar el TBL.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Tabla completa de la pantalla de fallas y LED de estado (guía de instalación SP+): https://www.paradox.com/Downloader/?ID=11662
- Secciones 950, 955 y 960 (guía de programación SP+): https://www.paradox.com/Downloader/?ID=11650
- Puesta en marcha con solo pérdida de reloj y campana ausente (guía EVOHD+): https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf
- Fallas en el K32LCD+ (guía rápida): https://store.tremtech.com/content/K32LCDPlus_Installation_Guide_En.pdf
