# Lección 12. Día y noche

**Escuchá:** dia-noche.mp3 (2 min)

**La idea, en tres líneas**
- El AVENAR ofrece las opciones de EN 54-2: retardo de transmisión, dependencia de más de una señal (tipos A, B y C), contador de alarmas y modo día; con teclas programables se pasa de día a noche o a sensibilidad alternativa.
- Estrategias habituales: alarma demorada para investigar (BS 5839-1 la limita a 6 min y el pulsador la anula), confirmación por segundo detector, prealarma y día/noche. La IT-11 uruguaya de 2010 admite preseñal de hasta 2 min en locales concurridos.
- La verificación del monitoreo es otra cosa: NFPA 72 la permite solo si bomberos la pide, con 90 s como máximo y aviso simultáneo al despacho, y sigue siendo polémica.

**Impacto:** menos evacuaciones inútiles sin demorar un fuego real más allá de lo que firmó el proyecto.

**Quién lo dice:** 3 de 4 fuentes coinciden en que todo retardo se acuerda con la autoridad y no se aplica a pulsadores (System manual, FIA, Security Sales); la misma nota de Security Sales recoge a quienes ven en la verificación un riesgo de demora.

**Laboratorio** · Foco · 15 min
Diseño en papel para un local comercial:
```text
Evento              | Modo día                            | Modo noche
1 detector          | prealarma, personal investiga 3 min | alarma general + transmisión
2 detectores        |                                     |
1 pulsador          | alarma general inmediata            | alarma general inmediata
Falla de red        |                                     |
Cambio día/noche    | tecla de función / horario: ______  |
```
1. Completá cada celda con la acción y el retardo.
2. Verificá: ningún retardo sobre pulsadores, ningún retardo mayor al que permita el proyecto.
3. Llevá la tabla al técnico registrado para que la valide antes de programarla.
⚠️ Un retardo mal configurado demora la evacuación en un fuego real. Solo se programa lo que está en el proyecto firmado y aceptado por la autoridad.

**Regla para quedarse**
Ningún retardo sin firma del técnico registrado, y nunca sobre pulsadores.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Estrategias de respuesta a la alarma (FIA): https://www.fia.uk.com/static/uploaded/4ddbff0f-557d-496b-b62b716a1761b77d.pdf
- La verificación de alarma en NFPA 72 y su polémica: https://www.securitysales.com/contributed/alarm-verification-remains-a-polarizing-proposition/
- Opciones EN 54-2 del AVENAR (System manual, apéndice): https://media.boschsecurity.com/fs/media/pb/media/extranet/fire_alarm_system/documentation/avenar_panel_system_information/BDL_SYM_AVENAR_panel_F01U378910_05_en.pdf
