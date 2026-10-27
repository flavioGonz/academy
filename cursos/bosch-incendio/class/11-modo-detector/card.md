# Lección 11. Modo del detector

**Escuchá:** modo-detector.mp3 (2 min)

**La idea, en tres líneas**
- En los AVENAR detector 4000 se programa el lugar de instalación (oficina modo día, sala de servidores, garaje, cocina en servicio...), y eso fija cómo pesa cada sensor. Valores de fábrica: OT y DOT en "oficina modo día", DOTC en "oficina con fumadores / sala de espera / restaurante", ópticos en sensibilidad media, térmico en A2R.
- Los multisensores admiten apagar sensores (solo óptico, solo térmico A2R o A2S); algunas combinaciones del DOTC-R dejan de cumplir EN 54-7.
- Multisensor u óptico: el multisensor rechaza mejor las falsas alarmas porque espera más; esa espera es su costo.

**Impacto:** menos falsas alarmas sin perder detección, y un modo que cualquier técnico puede auditar.

**Quién lo dice:** 3 de 4 fuentes apoyan el multisensor contra falsas alarmas (estudio BRE, resumen en pbctoday, FIA con la advertencia de que todo filtro demora un fuego real); la columna sobre BS 5839-1 prefiere CO donde hay vapor y aerosoles.

**Laboratorio** · Rápido · 10 min
1. Abrí una configuración real en FSP-5000-RPS (copia, no la del panel en servicio).
2. Listá los detectores:
```text
Dirección lógica | Modelo         | Lugar de instalación (modo) | ¿Elegido o de fábrica? | Ambiente real
3.1              | FAP-425-OT-R   | Oficina (modo día)          | de fábrica              | cocina de piso
3.2              | FAP-425-DOTC-R |                             |                         |
```
3. Marcá los que quedaron en el modo de fábrica sin decisión documentada.
4. Para cada uno, anotá qué modo correspondería según la tabla de la guía (por ejemplo, "Cocina/casino/restaurante en operación").
⚠️ Cambiar el modo de un detector cambia su respuesta al fuego: se acuerda con el proyecto y se prueba después.

**Regla para quedarse**
Ningún detector queda en el modo de fábrica sin que alguien lo haya decidido y escrito.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Tablas de lugares de instalación y sensibilidades (guía de operación AVENAR detector 4000): https://armosystems.ru/upload/iblock/a58/a58a375f59a20cf60064da272d2b6fd9.pdf
- El estudio BRE de multisensores frente a ópticos: https://bregroup.com/documents/d/bre-group/_6-2018-march-multi-sensors-in-fire-and-false-alarm-tests
- Resumen del estudio: https://www.pbctoday.co.uk/news/health-safety-news/reduction-of-false-alarms-when-multi-sensor-detectors-used/40842/
