# Lección 7. IVR con horario

**Escuchá:** ivr-horario.mp3 (2 min)

**La idea, en tres líneas**
- Cada tecla del IVR admite hasta cinco destinos con condición de horario: un solo IVR para día, noche y feriados.
- El que no marca nada o marca mal también necesita destino: operadora, grupo o buzón.
- Si se permite marcar internas, lista blanca de las alcanzables desde el IVR.

**Impacto:** ninguna llamada termina en silencio o cortada por un menú mal cerrado.

**Quién lo dice:** 2 de 2 fuentes de Grandstream coinciden; difieren en el límite de anidado (5 niveles en un post viejo del blog, 64 IVR anidados en el manual actual).

**Laboratorio** · Foco · 15 min
1. Definí horario de oficina y un feriado de prueba:
```text
System Settings > Time Settings > Office Time/Holiday
```
2. Subí un mensaje de bienvenida (WAV) en:
```text
PBX Settings > Voice Prompt > Custom Prompt
```
3. Creá el IVR:
```text
Basic Call Features > IVR > Add
Name: principal   Extension: 7000   Prompt: (tu archivo)
Tecla 1: Office Time -> Ring Group ventas | Out of Office Time -> Voicemail 1001
Tecla 2: All Time -> Extension 1002
Response Timeout: destino Ring Group recepción
Invalid: destino Ring Group recepción
```
4. Si habilitás Dial Other Extensions, activá la lista blanca y dejá solo las internas públicas.
5. Llamá al 7000 en horario y fuera de horario (cambiá el horario de oficina para probar) y no marques nada: tiene que ir a recepción.

**Regla para quedarse**
Todo IVR tiene destino para el que no marca nada y para el que marca mal.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- IVR, eventos de tecla y condiciones de horario: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/
- Funciones de call center de la UCM según Grandstream: https://blog.grandstream.com/company/news/blog/how-to-use-the-ucm-ip-pbxs-call-center-features
