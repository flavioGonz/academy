# Lección 11. Abonado y receptora

**Escuchá:** abonado-y-receptora.mp3 (2 min)

**La idea, en tres líneas**
- Formato en [810] (un dígito por teléfono): 4 = Contact ID, 5 = SIA. Por IP o GPRS, SIA no está soportado; IP180 e IP150M reportan solo Contact ID.
- Abonado por partición: [811]/[812] para teléfono, [918]/[919] para IP. Receptor IP 1 en [929] a [935], receptor 2 en [936] a [942], respaldo en [943] a [949].
- La receptora da: abonado, IP y puerto, contraseña (solo legado) y perfil. Con IPC10 los perfiles son fijos: 01 = 1200 s, 02 = 600 s, 03 = 300 s, 04 = 90 s.

**Impacto:** cada evento llega identificado, la supervisión avisa si el módulo se cae, y la prueba diaria confirma que el canal vive.

**Quién lo dice:** 4 de 7 fuentes coinciden en Contact ID y abonado por partición (guía de programación SP+, finmon, manuales IP180 e IPC10); discrepan en SIA el manual del IPR512 (lo acepta) y la guía de instalación SP+ (lo soporta por teléfono). 5 de 7 coinciden en elegir receptora según el módulo.

**Laboratorio** · Foco · 20 min
Central SP o MG con módulo IP de banco. Valores de ejemplo: receptor 203.0.113.10, abonado 1A01. Pedí los reales a la empresa de monitoreo.
1. Formato y abonados:
```text
[ENTER] + código de instalador + [810]  44        Contact ID en los dos teléfonos
[CLEAR] [811] 1A01                                abonado partición 1
[CLEAR] [812] 1A01                                abonado partición 2 (aunque no esté particionada)
[CLEAR] [918] 1A01                                abonado IP partición 1
[CLEAR] [919] 1A01                                abonado IP partición 2
```
2. Receptor IP 1 (cada número de la IP con tres dígitos):
```text
[CLEAR] [929] 203 000 113 010     IP del receptor (WAN1)
[CLEAR] [930] 10000               puerto (el que indique la receptora)
[CLEAR] [933] ......              contraseña de receptor (solo IPR512; IPC10 no la usa)
[CLEAR] [934] 02                  perfil de supervisión
[CLEAR] [935] [ARM]               registra el módulo y muestra el estado
```
3. Prueba automática diaria a las 13:00:
```text
[CLEAR] [840] 001                 cada 1 día
[CLEAR] [850] 1300                hora (formato 24 h)
```
4. Con el operador en línea, generá un evento de prueba y confirmá abonado, zona y partición.

⚠️ No dejes el abonado de ejemplo ni el de otra obra: un evento con abonado equivocado puede terminar en el cliente equivocado.

**Regla para quedarse**
El abonado va en cada partición y en cada canal.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Formatos, abonados, receptores IP y tabla de estados (guía de programación SP+): https://www.paradox.com/Downloader/?ID=11650
- Receta de campo para MG5050 y SP6000 (finmon): https://www.finmon.co.za/kb/books/gsm-communicator-programming-manual/page/paradox-mg5050-and-sp6000-programming
- Receptor IPR512 en español: perfiles, registro y formatos de salida: https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Receptoras/Manual_IPR512.pdf
- Conversor IPC10 (MQTT): cuentas, buffer y salida a software de monitoreo: https://www.paradox.com/Downloader/?ID=12343
