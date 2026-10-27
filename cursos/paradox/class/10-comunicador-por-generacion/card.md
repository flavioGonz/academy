# Lección 10. Comunicador por generación

**Escuchá:** comunicador-por-generacion.mp3 (2 min)

**La idea, en tres líneas**
- Legado (TURN): IP150 hasta V5, IP150+, PCS250/260/265, PCS265 LTE y V7. Reportan a IPR512/IPRS-7, conectan por Swan o IP estática, con Insite Gold o BlueEye.
- MQTT: IP180, IP150+MQ, IP150M (IP150 a V6.50) y PCS265 V8. Reportan solo Contact ID a IPC10/VIPC20, solo con BlueEye, sin conexión por IP estática. No se mezclan con legado en la misma central.
- Salida a internet que piden IP180 e IP150M: TCP 8883 (MQTT), TCP 443 (firmware), UDP 53, UDP 123, UDP 5683 y el puerto del correo.

**Impacto:** no rompés el monitoreo ni le cambiás el plan al cliente por una actualización hecha a ciegas.

**Quién lo dice:** 4 de 6 fuentes coinciden (manuales IP180 e IP150M, guía del menú instalador BlueEye, ficha IP150+ de CSD); ninguna discrepa. Todas son del fabricante o de un distribuidor.

**Laboratorio** · Admin · 15 min
1. Identificá el módulo y su firmware: etiqueta del módulo, o en BlueEye, menú instalador, detalles del sitio (tipo y versión de módulo y central).
2. Ubicalo en la tabla:
```text
Módulo              Generación   Receptora           App
IP150 (V1 a V5)     TURN         IPR512 / IPRS-7     Insite Gold, BlueEye
IP150+ (V4/V5)      TURN         IPR512 / IPRS-7     Insite Gold, BlueEye
PCS265 LTE / V7     TURN         IPR512 / IPRS-7     Insite Gold, BlueEye
IP180               MQTT         IPC10 / VIPC20      BlueEye
IP150+MQ (V6)       MQTT         IPC10 / VIPC20      BlueEye
IP150M (V6.50)      MQTT         IPC10               BlueEye (Swan pago)
PCS265 V8           MQTT         IPC10 / VIPC20      BlueEye
```
3. Preguntá a la empresa de monitoreo qué receptora tiene (IPR512, IPRS-7, IPC10).
4. Preguntá al cliente quién usa Insite Gold y si tiene cámaras HD78/HD88 en la app.
5. Pasale al informático la lista de salida y verificá desde una notebook en la misma red:
```powershell
Resolve-DnsName paradox.com
Test-NetConnection paradox.com -Port 443
```
Para TCP 8883 de salida, pedí que confirmen la regla en el firewall.
6. En una central plus, el módulo principal va al serie 1 y el de respaldo al serie 2, de la misma generación.

⚠️ Pasar un IP150 a MQTT (IP150M V6.50) es irreversible y, según su manual, exige sitio Swan pago para toda comunicación. No lo hagas sin acuerdo del cliente y de monitoreo.

**Regla para quedarse**
Primero sé qué generación de módulo hay, después actualizás.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- IP180: MQTT, puertos, serie 1 y 2, reporte a IPC10 (manual V1.00.063): https://www.paradox.com/Downloader/?ID=12435
- IP150M V6.50: Swan pago, irreversible, sin Insite Gold: https://www.paradox.com/Downloader/?ID=11873
- TURN contra MQTT y configuración de módulos (guía del menú instalador BlueEye V2.0): https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Software/BlueEye/BlueEye_Installer_Menu_v2.0%20.pdf
