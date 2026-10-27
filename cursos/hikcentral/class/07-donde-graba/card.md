# Lección 7. Dónde graba

**Escuchá:** donde-graba.mp3 (2 min)

**La idea, en tres líneas**
- Al dar de alta se elige por cámara dónde graba: en el equipo (NVR, tarjeta) o en almacenamiento central (pStor, pStor Cluster, Hybrid SAN, Cloud Storage Server).
- Cada opción tiene límites: por dominio o Hik-Connect no se graba en Hybrid SAN ni Cloud Storage; pStor Cluster no hace grabación por movimiento.
- "Get Device's Recording Settings" toma el calendario que ya tiene el NVR para no pisarlo.

**Impacto:** cada cámara graba donde el diseño dice y se detectan antes las que no graban.

**Quién lo dice:** 3 de 3 fuentes de grabación coinciden en decidir por cámara al dar de alta (manual del Web Client, FAQ, página de eventos; todas de Hikvision). La división está en el criterio: grabar en sitio o central depende del enlace y de quién mantiene el servidor.

**Laboratorio** · Foco · 15 min
1. Armá la tabla de grabación de una obra (planilla o texto):
```text
Cámara   Alta por     Graba en         Motivo
CAM-01   IP           NVR sitio        enlace de 20 Mbps al centro
CAM-02   ISUP         NVR sitio        sin IP fija
CAM-09   IP           pStor central    retención 90 días pedida
```
2. Revisá cada fila contra los límites: si "Alta por" es dominio o Hik-Connect, "Graba en" no puede ser Hybrid SAN ni Cloud Storage.
3. En el Web Client, abrí la configuración de grabación de una cámara de laboratorio y confirmá ubicación y plantilla (en V2.x: Recording, con plantillas de calendario).
4. Buscá el estado de grabación de los recursos en Maintenance (Search for Recording Status of Resource en V2.6.1) y anotá las que no graban.

⚠️ Cambiar la ubicación de grabación de una cámara en producción no mueve el video viejo: anotá dónde quedó el histórico.

**Regla para quedarse**
La ubicación de la grabación se decide por cámara, por escrito, antes del alta.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Opciones de almacenamiento al dar de alta (manual del Web Client): https://enpinfo.hikvision.com/hkwsen/unzip/20230830144955_12918_doc/GUID-76D11646-EA40-4EDA-88DD-38821CB5826E.html
- Límites de Cloud Storage, Hybrid SAN y pStor Cluster (FAQ V2.5.500): https://pinfo.hikvision.com/hkwsen/unzip/20240603152919_44907_doc/UD38113B_HikCentral%20Professional%20V2.5.500_FAQ_V2.5.500_20240603.pdf
