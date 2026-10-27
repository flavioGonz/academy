# Lección 4. Lazo cerrado

**Escuchá:** lazo-cerrado.mp3 (2 min)

**La idea, en tres líneas**
- Cada elemento LSN trae aislador entre b1 y b2: en lazo (clase A, o X por los aisladores) el panel parte el lazo ante un corte o un corto y todo sigue andando; en ramal (clase B) se pierde lo que queda detrás de la falla.
- Los ramales de un solo elemento conectados solo a b1 no aíslan, y las mallas dentro de un lazo o ramal están prohibidas.
- EN 54-2: una falla no puede dejar fuera más de 512 detectores y pulsadores; un panel con más de 512 pide controlador redundante. La autoridad local puede exigir un tope menor.

**Impacto:** una perforación o un corto en obra se vuelve un aviso de avería y no un piso sin detección.

**Quién lo dice:** 3 de 3 fuentes coinciden en el comportamiento (System manual, Selection guide, guía sobre NFPA 72); la guía NFPA aclara que la norma no impone clase y que la B es la más común, así que la elección es del proyecto.

**Laboratorio** · Foco · 15 min
Material: panel de banco, módulo LSN, tres detectores cableados en lazo.
1. Verificá que el lazo esté normal en el panel.
2. Desconectá un conductor entre el detector 1 y el 2.
3. Anotá el mensaje de avería y probá los tres detectores con aerosol en modo revisión: los tres responden.
4. Reconectá y reponé la avería.
5. Desconectá el retorno del lazo en el panel (ahora es un ramal) y repetí el corte entre 1 y 2.
6. Anotá cuántos detectores se pierden:
```text
Lazo con corte:   avería, detectores activos: __ de 3
Ramal con corte:  avería, detectores activos: __ de 3
```
7. Volvé a cerrar el lazo y reponé.
⚠️ Hacelo solo en banco. En una instalación real, abrir el lazo deja parte del edificio sin detección o en avería: requiere aviso al monitoreo y al responsable del edificio.

**Regla para quedarse**
Lazo siempre que se pueda; ramal solo si el proyecto lo justifica y nunca ramales de un elemento sin aislar.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Topologías, aisladores y manejo de fallas en LSN (System manual): https://media.boschsecurity.com/fs/media/pb/media/extranet/fire_alarm_system/documentation/avenar_panel_system_information/BDL_SYM_AVENAR_panel_F01U378910_05_en.pdf
- Clases A, B, X y N explicadas: https://open-exam-prep.com/study-guides/cfps-fire/detection-and-alarm/fire-alarm-system-fundamentals
- Características del LSNi según el fabricante: https://media.boschbuildingtechnologies.com/fs/media/pb/images/news/rethink_the_magazine/avenar_detector_4000_series/Selection_Guide_.pdf?collection=bosch-bt-lifesafetysystems
