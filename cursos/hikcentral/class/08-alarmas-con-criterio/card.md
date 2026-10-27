# Lección 8. Alarmas con criterio

**Escuchá:** alarmas-con-criterio.mp3 (2 min)

**La idea, en tres líneas**
- Evento = disparador + fuente + horario de recepción + acciones. Con Trigger Alarm pasa a ser alarma, con prioridad y destinatarios.
- Bajá el ruido con Ignore Repetitive Events (por ejemplo 30 s) y Delay Alarm para cámara offline.
- Para alarmas reales, Trigger Recording con pre y post evento y Lock Video Files para que el clip no se sobrescriba.

**Impacto:** el operador atiende alarmas que importan y mantenimiento ve solo cámaras realmente caídas.

**Quién lo dice:** 2 de 2 fuentes de eventos (manual del Web Client V2.6.1 y FAQ V2.5.500, ambos de Hikvision); evidencia fina pero concreta. No se encontró quien discrepe.

**Laboratorio** · Foco · 20 min
1. Web Client > Event and Alarm > Normal Event and Alarm > Add (en V2.6.1 dentro de Security Monitoring).
2. Regla 1, evento de mantenimiento:
```text
Triggering Event:  Camera Offline (Maintenance)
Source:            CAM-01..CAM-04
Delay Alarm:       120 s
Trigger Alarm:     off  (queda como evento)
```
3. Regla 2, alarma real:
```text
Triggering Event:  Alarm Input
Source:            Entrada 1 del NVR (contacto de puerta)
Ignore Repetitive: 30 s
Trigger Recording: Source/related camera CAM-02, pre 10 s, post 30 s
Lock Video Files:  7 días
Trigger Alarm:     on, prioridad alta, destinatario: usuario guardia
```
4. Confirmá que CAM-02 tenga calendario de grabación; si no, el sistema marca excepción de regla.
5. Probá: desconectá CAM-01 30 s (no debería avisar) y después 3 min (debería aparecer el evento). Cerrá el contacto de la entrada 1 y revisá el clip en el Control Client.

**Regla para quedarse**
Si nadie la va a atender, no es alarma: es evento.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Disparadores, acciones, ignorar repetidos y demora de alarma (manual del Web Client V2.6.1): https://pinfo.hikvision.com/hkwsen/unzip/20240822164538_35347_doc/GUID-7C8C6C1B-5438-4C6B-8C71-B042A25AE1BB.html
- Límite de eventos con imagen por segundo y reconocimiento en lote (FAQ V2.5.500): https://pinfo.hikvision.com/hkwsen/unzip/20240603152919_44907_doc/UD38113B_HikCentral%20Professional%20V2.5.500_FAQ_V2.5.500_20240603.pdf
