# Lección 8. Menos potencia

**Escuchá:** menos-potencia.mp3 (2 min)

**La idea, en tres líneas**
- 2,4 GHz: solo 1, 6 y 11 a 20 MHz. 5 GHz: 40 MHz de arranque; 20 con mucha interferencia, 80 o más solo en ambiente limpio.
- Más potencia no es mejor: con APs a menos de 12 m, bajá (ejemplo oficial: de 28 a 25 dBm y probar). APs muy juntos también frenan el roaming.
- WLAN Optimization (RRM) corta internet varios minutos mientras escanea: programala de madrugada, separada al menos 10 minutos del reinicio programado. La región define canales y potencia legales.

**Impacto:** menos quejas de "WiFi lento" en oficinas con varios APs, sin comprar equipos nuevos.

**Quién lo dice:** 2 de 3 fuentes sobre RF coinciden (guía de optimización y guía de roaming de TP-Link); no se encontró discrepancia. La advertencia sobre el corte durante la optimización viene de una sola fuente oficial.

**Laboratorio** · Campo · 15 min
Con dos EAP adoptados y un celular con una app de análisis WiFi:
1. Medí antes: canal, ancho y señal (dBm) de cada AP desde tres puntos del lugar. Anotalo.
2. **Devices > (EAP 1) > Config > Radios**:
```text
2.4 GHz: canal 1, ancho 20 MHz, potencia Medium
5 GHz:   canal 36, ancho 40 MHz, potencia Medium
```
3. **Devices > (EAP 2) > Config > Radios**:
```text
2.4 GHz: canal 6 (o 11), ancho 20 MHz, potencia Medium
5 GHz:   canal 44 (o 149), ancho 40 MHz, potencia Medium
```
4. Verificá en la configuración del sitio que la región sea **Uruguay**.
5. Medí después desde los mismos tres puntos y compará. Si en algún punto la señal quedó por debajo de -70 dBm, subí un escalón la potencia solo de ese AP.
6. Opcional: **Network Config > Network Settings > WLAN > WLAN Optimization**, programala para las 3:30 y verificá que el reinicio programado de APs quede a otra hora.
⚠️ Ejecutar WLAN Optimization en horario de trabajo deja a los clientes sin internet varios minutos.

**Regla para quedarse**
Primero canal y ancho, después potencia, y la optimización automática de madrugada.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Cómo optimizar el rendimiento inalámbrico de los EAP (v6.2.10 y posteriores): https://www.tp-link.com/us/support/faq/2511
- APs demasiado juntos o separados y su efecto en el roaming: https://support.omadanetworks.com/en/document/13229/
- La región en el asistente define canales y potencia legales: https://computingforgeeks.com/omada-controller-docker/
